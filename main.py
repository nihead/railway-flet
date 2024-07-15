import logging
import os
import flet as ft
from views.home import Home
from views.userscan import scanPage
from services.webServer import ScanUser

logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "TMA RTLT"
    page.theme_mode = ft.ThemeMode.DARK

    web_session = ScanUser()
    def route_change(route):
        print(route)
        page.views.clear()

        page.views.append(
            Home(page, web_session)
        )
        if page.route == "/scanned":
            page.views.append(
                ft.View(
                    "/scanned",
                    [
                        ft.AppBar(title=ft.Text("User Scan"), bgcolor=ft.colors.SURFACE_VARIANT),
                        scanPage(page, web_session),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )


        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    # ft.app(target=main, view=None, port=int(os.getenv("PORT", 8502)))
    ft.app(target=main)