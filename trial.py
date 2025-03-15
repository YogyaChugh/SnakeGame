import flet as ft

def main(page: ft.Page):
    page.session.set("maggi",True)

    del page.session[0]

    page.add(ft.Text("hi"))

ft.app(main)