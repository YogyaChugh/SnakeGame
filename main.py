import flet as ft
import json

def main(page: ft.Page):
    page.title = "Maggi is gold"
    with open("saved_stuff/saved_maps.json") as file:
        data = json.load(file)
    data = data["Map_01"]

    the_map = ft.GridView(
        expand=1,
        runs_count=len(data["locations"][0]),
        run_spacing=0,
        scale=1.0,
        padding=0,
        spacing=0,
        width =650,
        on_scroll=None
    )
    allowed_image = ft.Image(src=data["allowed_blocks"][0][1],width=50,height=50,fit=ft.ImageFit.CONTAIN)
    disallowed_image = ft.Image(src=data["disallowed_blocks"][0][1],width=50,height=50,fit=ft.ImageFit.CONTAIN)

    for i in data["locations"]:
        for j in i:
            if j==1:
                the_map.controls.append(
                    allowed_image
                )
            else:
                the_map.controls.append(
                    disallowed_image
                )

    page.add(the_map)

ft.app(main)