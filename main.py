import flet as ft,asyncio
import os,sys
import maps,snake,fruits,base
import time
from functools import partial

start = False
first = 1
bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
map_1 = maps.Map("Map_01")
snakes = snake.Snake("Snake_01",map_1)

async def update_fps():
    global start
    prev_time = time.time()
    frame_count = 0

    while True:
        frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - prev_time

        if elapsed_time >= 1.0:  # Update FPS every second
            fps = frame_count / elapsed_time
            print(f"FPS: {fps:.2f}")
            prev_time = current_time
            frame_count = 0  # Reset frame count

        await asyncio.sleep(0.008)  # Approx. 60 FPS (1/60 = 0.016 sec)

async def update_snake(start,page,snakes,map_container,snake_container_images,final_stack):
    while True:
        try:
            if snakes.moving:
                snakes.move()
                print("bro")
                for i in snake_container_images:
                    final_stack.controls.remove(i)
                snake_container_images = snakes.draw(map_container[1],map_container[2],map_container[3])
                for i in snake_container_images:
                    final_stack.controls.append(i)
                print("bro")
        except snake.GameOver as g:
                game_over = ft.Text(
                    spans=[
                        ft.TextSpan(
                            "GAME OVER",
                            ft.TextStyle(
                                size=40,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=2,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                    text_align = ft.TextAlign.CENTER,
                    bgcolor = ft.Colors.TEAL_ACCENT_200
                )
                new = ft.Container(game_over,alignment=ft.alignment.center)
                final_stack.controls.append(new)
                snakes.moving = False
        except Exception as e:
            pass
        page.update()
        await asyncio.sleep(0.5)

async def main(page: ft.Page):
    global map_1,snakes
    start = False
    page.adaptive = True
    page.title = "Hi man"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.maximizable = False
    page.window.resizable = False
    print("maggi")
    img = ft.Image(
        src ="background.jpeg", 
        expand=True,
        width = page.width,
        height = page.height,
        fit = ft.ImageFit.FILL,
    )
    def update_stuff(e):
        img.width = page.width
        img.height = page.height

    instruction = ft.Text(
                    spans=[
                        ft.TextSpan(
                            "PRESS 'F' to start",
                            ft.TextStyle(
                                size=40,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=2,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                    top = 50,
                    left = 10,
                    bgcolor = ft.Colors.TEAL_ACCENT_200
                )
    instruction2 = ft.Text(
                    spans=[
                        ft.TextSpan(
                            "Use Arrow Keys\nto navigate :)",
                            ft.TextStyle(
                                size=40,
                                foreground=ft.Paint(
                                    color=ft.Colors.BLUE_700,
                                    stroke_width=2,
                                    stroke_join=ft.StrokeJoin.ROUND,
                                    style=ft.PaintingStyle.STROKE,
                                ),
                            ),
                        ),
                    ],
                    top = 130,
                    left = 10,
                    bgcolor = ft.Colors.TEAL_ACCENT_200
                )
    page.on_resized = update_stuff
    map_container = map_1.get_container(page.width,page.height)
    snake_container_images = snakes.draw(map_container[1],map_container[2],map_container[3])
    final_stack = ft.Stack(controls=[img,instruction,instruction2, map_container[0]])
    for i in snake_container_images:
        final_stack.controls.append(i)
    page.add(final_stack)
    print("reached here")
    async def on_key(event: ft.KeyboardEvent):
        print(event.key)
        if event.key=="Arrow Up" and snakes.direction!="DOWN":
            print("hi")
            snakes.direction_pt = (0,-1)
            snakes.direction = "UP"
        elif event.key=="Arrow Down" and snakes.direction!="UP":
            snakes.direction_pt = (0,1)
            snakes.direction = "DOWN"
        elif event.key=="Arrow Left" and snakes.direction!="RIGHT":
            snakes.direction_pt = (-1,0)
            snakes.direction = "LEFT"
        elif event.key=="Arrow Right" and snakes.direction!="LEFT":
            snakes.direction_pt = (1,0)
            snakes.direction = "RIGHT"
        elif event.key=="F":
            print("paji")
            asyncio.create_task(update_snake(start,page,snakes,map_container,snake_container_images,final_stack))
    page.on_keyboard_event = on_key
    page.update()
    print("reached here toooooooooo")
    asyncio.create_task(update_fps())

app = ft.app(main, export_asgi_app=True, assets_dir="static")