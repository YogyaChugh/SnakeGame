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
    page.session.get("score").content.content.subtitle = ft.Text(str(0))
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
                    page.session.get("score").content.content.subtitle = ft.Text(str(int(page.session.get("score").content.content.subtitle.value)+1))
                    page.session.get("snakes").increase_length()
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
    if page.platform == ft.PagePlatform.ANDROID:
        page.session.clear()
        page.controls.clear()
        page.title = "Platform Alert"
        page.bgcolor = "#1E1E2E"
        page.padding = 50

        heading = ft.Text(
            "Oops! This is not for Android/iOS",
            size=35,
            color="white",
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        message = ft.Text(
            "This application is designed for desktops only. Enjoy the full experience on your PC or laptop!",
            size=18,
            color="#D0D0D0",
            text_align=ft.TextAlign.CENTER,
        )

        card = ft.Container(
            content=ft.Column([
                heading,
                message,
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
            padding=30,
            width=500,
            border_radius=15,
            bgcolor="#282A36",
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=3, color="#5A5A5A"),
        )

        page.add(
            ft.Column(
                [card],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        return
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
        
        async def restart(e):
            if page.session.get("snakes").moving:
                return
            page.session.get("score").content.content.subtitle = ft.Text(str(0))
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
        restart_button = ft.ElevatedButton("Restart")
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
        page.session.get("final_stack").controls.append(ft.Container(restart_button, left=page.width*4/5+60, top=100))
        getthefruit= page.session.get("fruit").draw(
            page.session.get("map_container")[1],
            page.session.get("map_container")[2],
            page.session.get("map_container")[3]
        )
        page.session.set("fruit_image",getthefruit)
        page.session.get("final_stack").controls.append(page.session.get("fruit_image"))
        page.session.set("start", "false")
        page.session.get("restart_button").on_click = restart

        score = ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("SCORE"),
                            subtitle=ft.Text(
                                str(0)
                            ),
                        )
                ),
                width=300
            )
        page.session.set("score",score)
        page.session.get("final_stack").controls.append(page.session.get("score"))
    
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
    page.title = "Snake Hustler"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.maximizable = False
    page.window.resizable = False
    recreate()

    async def on_key(event: ft.KeyboardEvent):
        async def start_snake(e=None):
            page.session.get("snakes").moving = True
            try:
                for i in page.session.get("temp_images"):
                    page.session.get("final_stack").controls.remove(i)
            except Exception as e:
                pass
            page.update()
            asyncio.create_task(update_snake(page=page))
        if (event.key=="Arrow Up" or event.key=="Arrow Down" or event.key=="Arrow Left" or event.key=="Arrow Right") and not page.session.get("snakes").moving:
            await start_snake()
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
