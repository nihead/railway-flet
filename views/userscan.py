import flet as ft
from services.webServer import ScannedUser, ScanUser
class scanPage(ft.Container):
    def __init__(self, page, web_session):
        super().__init__()
        self.page = page
        self.web_session: ScannedUser = web_session
        self.auth = self.web_session.get_user()
        self.expand = True
        self.width = 700

        self.content = ft.Column(
            controls=[
                ft.Text(self.web_session.user.name, size=30),
                ft.Divider(height=9, thickness=3),

                ft.Text(
                    value= "You are working on task: " if self.web_session.user.c_page == "Started tracking time" else "You are Not tracking Time",
                    size=20,
                    italic=True
                ),
                ft.Text(self.web_session.user.work_on),
                ft.Text(self.web_session.user.work_on_code),

                ft.Divider(height=9, thickness=3),
                ft.Text(
                    value= "Total time Tracking",
                    size=20,
                    italic=True
                ),
                ft.Text(
                    self.web_session.user.total_lt,
                    size=30,
                    weight=ft.FontWeight.BOLD
                ),

            ]
        )

