import flet as ft, asyncio
import os, sys
import maps, snake, fruits, base
import time
from functools import partial


async def update_snake(page):
    game_over = ft.Text(
        "GAME OVER !",
        text_align=ft.TextAlign.CENTER,
        bgcolor=ft.Colors.TEAL_ACCENT_200,
        size=35
    )
    game_over = ft.Container(game_over,alignment=ft.alignment.center)
    snake_container_images = []
    page.session.set("score",0)
    while True:
        try:
            if page.session.get("snakes").moving:
                try:
                    if game_over in page.session.get("final_stack").controls:
                        page.session.get("final_stack").controls.remove(game_over)
                except Exception as e:
                    print(e)
                    pass
                page.session.get("snakes").move()
                try:
                    for i in page.session.get("snake_container_images"):
                        if i in page.session.get("final_stack").controls:
                            page.session.get("final_stack").controls.remove(i)
                except Exception as e:
                    print(e)
                    pass
                if page.session.get("fruit").location==page.session.get("snakes").locations[0]:
                    page.session.get("final_stack").controls.remove(page.session.get("fruit_image"))
                    page.session.get("fruit").randomize()
                    page.session.set("fruit_image",page.session.get("fruit").draw(page.session.get("map_container")[1],page.session.get("map_container")[2],page.session.get("map_container")[3]))
                    page.session.get("final_stack").controls.append(page.session.get("fruit_image"))
                    page.session.set("score",page.session.get("score")+1)
                snake_container_images = page.session.get("snakes").draw(
                    page.session.get("map_container")[1],
                    page.session.get("map_container")[2],
                    page.session.get("map_container")[3]
                )
                page.session.set("snake_container_images",snake_container_images)
                for i in page.session.get("snake_container_images"):
                    page.session.get("final_stack").controls.append(i)
        except snake.GameOver:
            print("GAME OVER")
            page.session.get("final_stack").controls.append(game_over)
            for i in page.session.get("snake_container_images"):
                if i in page.session.get("final_stack").controls:
                    page.session.get("final_stack").controls.remove(i)
            try:
                page.session.get("final_stack").controls.remove(page.session.get("fruit_image"))
            except Exception as e:
                print(e)
                pass
            page.session.get("snakes").moving = False
            page.update()
            return
        except Exception as g:
            print(g)
            pass
        page.update()
        await asyncio.sleep(0.3)


async def main(page: ft.Page):
    def recreate(e=None):
        print("recreated page")
        page.session.clear()
        map_1 = maps.Map("Map_01")
        snakes = snake.Snake("Snake_01", map_1)
        fruit_guy = fruits.Fruits("Fruit_01",map_1,snakes)
        page.session.set("fruit",fruit_guy)
        page.session.set("map", map_1)
        page.session.set("snakes", snakes)
        img = ft.Image(
            src="background.jpeg",
            expand=True,
            width=page.width,
            height=page.height,
            fit=ft.ImageFit.FILL,
        )
        async def start_snake(e=None):
            page.session.get("snakes").moving = True
            try:
                for i in page.session.get("temp_images"):
                    page.session.get("final_stack").controls.remove(i)
            except Exception as e:
                pass
            page.update()
            asyncio.create_task(update_snake(page=page))

        
        async def restart(e):
            if page.session.get("snakes").first:
                try:
                    for i in page.session.get("snake_prev_images"):
                        if i in page.session.get("final_stack").controls:
                            page.session.get("final_stack").controls.remove(i)
                except Exception as e:
                    print(e)
                    pass
            page.session.get("final_stack").controls.pop(-1)
            page.session.get("snakes").reset()
            snake_container_images = page.session.get("snakes").draw(
                page.session.get("map_container")[1],
                page.session.get("map_container")[2],
                page.session.get("map_container")[3]
            )
            page.session.get("snakes").prev_images = snake_container_images
            page.session.set("temp_images",snake_container_images)
            for i in page.session.get("temp_images"):
                page.session.get("final_stack").controls.append(i)
            page.session.set("snake_prev_images", snake_container_images)
            page.session.get("snakes").moving = True
            page.session.get("snakes").move_allowed = True
            page.session.get("fruit").randomize()
            page.session.set("fruit_image",page.session.get("fruit").draw(
                page.session.get("map_container")[1],
                page.session.get("map_container")[2],
                page.session.get("map_container")[3]
            ))
            page.session.get("final_stack").controls.append(page.session.get("fruit_image"))
            page.update()


        page.session.set("background_image", img)
        map_container = page.session.get("map").get_container(page.width, page.height)
        page.session.set("map_container", map_container)
        snake_container_images = page.session.get("snakes").draw(
            page.session.get("map_container")[1],
            page.session.get("map_container")[2],
            page.session.get("map_container")[3]
        )
        page.session.set("snake_container_images", snake_container_images)
        page.session.set("snake_prev_images", snake_container_images)
        final_stack = ft.Stack()
        page.session.set("final_stack", final_stack)
        play_button = ft.ElevatedButton("Play")
        restart_button = ft.ElevatedButton("Restart")
        page.session.set("play_button", play_button)
        page.session.set("restart_button", restart_button)

        tutorial = ft.AlertDialog(
            title=ft.Text("Instructions"),
            content=ft.Text("Use Arrow Keys for navigation :)"),
            open=True
        )
        page.session.get("final_stack").controls.append(page.session.get("background_image"))
        page.session.get("final_stack").controls.append(page.session.get("map_container")[0])
        for i in snake_container_images:
            page.session.get("final_stack").controls.append(i)
        page.session.get("final_stack").controls.append(tutorial)
        page.session.get("final_stack").controls.append(ft.Container(play_button, left=page.width/4, top=100))
        page.session.get("final_stack").controls.append(ft.Container(restart_button, left=page.width*3/4-60, top=100))
        getthefruit= page.session.get("fruit").draw(
            page.session.get("map_container")[1],
            page.session.get("map_container")[2],
            page.session.get("map_container")[3]
        )
        page.session.set("fruit_image",getthefruit)
        page.session.get("final_stack").controls.append(page.session.get("fruit_image"))
        page.session.set("start", "false")
        page.session.get("play_button").on_click = start_snake
        page.session.get("restart_button").on_click = restart
    
        page.add(page.session.get("final_stack"))
        page.update()
    page.session.clear()
    async def session_clear(e):
        page.controls.clear()
        page.session.clear()
    page.on_close = session_clear
    page.on_disconnect = session_clear
    page.adaptive = True
    page.on_connect = recreate
    page.title = "Hi man"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.maximizable = False
    page.window.resizable = False
    recreate()

    async def on_key(event: ft.KeyboardEvent):
        if event.key == "Arrow Up" and page.session.get("snakes").direction != "DOWN":
            page.session.get("snakes").direction_pt = (0, -1)
            page.session.get("snakes").direction = "UP"
        elif event.key == "Arrow Down" and page.session.get("snakes").direction != "UP":
            page.session.get("snakes").direction_pt = (0, 1)
            page.session.get("snakes").direction = "DOWN"
        elif event.key == "Arrow Left" and page.session.get("snakes").direction != "RIGHT":
            page.session.get("snakes").direction_pt = (-1, 0)
            page.session.get("snakes").direction = "LEFT"
        elif event.key == "Arrow Right" and page.session.get("snakes").direction != "LEFT":
            page.session.get("snakes").direction_pt = (1, 0)
            page.session.get("snakes").direction = "RIGHT"
    page.on_keyboard_event = on_key
    page.update()

app = ft.app(main, export_asgi_app=True, assets_dir="static", view=ft.AppView.WEB_BROWSER)
