import flet as ft,asyncio
from src.Maps import maps
from src.Snake import snake

async def main(page: ft.Page):
    map_1 = maps.Map("Map_01")
    page.adaptive = True
    page.title = "Hi man"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.maximizable = False
    page.window.resizable = False
    img = ft.Image(
        src = "map_01/background.jpeg",
        expand=True,
        width = page.width,
        height = page.height,
        fit = ft.ImageFit.FILL,
    )
    def update_stuff(e):
        img.width = page.width
        img.height = page.height
    page.on_resized = update_stuff
    map_container = map_1.get_container(page.width,page.height)
    snakes = snake.Snake("Snake_01",map_1)
    snake_container_images = snakes.draw(map_container[1],map_container[2],map_container[3])
    final_stack = ft.Stack(controls=[img, map_container[0]])
    for i in snake_container_images:
        final_stack.controls.append(i)
    page.add(final_stack)
    page.update()

ft.app(main)