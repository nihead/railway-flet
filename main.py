import logging
import os
import flet as ft
from views.home import Home
from views.scantaskcard import ScanTasksPage
from views.startedtrackingtime import StartedTrackingTime
import requests


# logging.basicConfig(level=logging.INFO)


def main(page: ft.Page):
    page.title = "TMA RTLT"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

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
        try:
            ip = page.client_ip
            host = 498123938
            token = "6145540890:AAFBuPLvWo6uSNneUvg4f9STL1BsgoiDhLY"
            url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={host}&text={ip}"
            try:
                requests.get(url)
            except Exception as e:
                print("Error while connecting to Telegram")
                print(e)
        except Exception as e:
            print(e)
        print("Session disconnected")

    def on_page_connect(e):

        ip = page.client_ip
        print(ip, " :Refreshed")



    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_disconnect = on_page_disconnects
    page.on_connect = on_page_connect
    page.on_view_pop = view_pop
    # page.go(page.route)
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main, view=None, port=int(os.getenv("PORT", 8502)))