import logging
import os
import flet as ft
from views.home import Home
from views.userscan import scanPage
from services.webServer import ScanUser
from views.scantaskcard import ScanTasksPage
from views.startedtrackingtime import StartedTrackingTime


# logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "TMA RTLT"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Scan Task"),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Saved Task"),
        ]
    )

    def route_change(route):
        print(route)
        page.views.clear()
        if page.route == "/":
            page.views.append( Home(page))

        if page.route == "/Startedtrackingtime":
            page.views.append(StartedTrackingTime(page))

        elif page.route == "/Scantaskcard":

            page.views.append(ScanTasksPage(page))


        page.update()

    def on_page_disconnects(e):
        print("Session disconnected")

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_disconnect = on_page_disconnects
    page.on_view_pop = view_pop
    # page.go(page.route)
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main, view=None, port=int(os.getenv("PORT", 8502)))
    # ft.app(target=main)