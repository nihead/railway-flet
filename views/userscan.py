import flet as ft


class Drops():
    def __init__(self):
        pass

class scanPage(ft.Container):
    def __init__(self, page, web_session):
        super().__init__()
        self.page = page
        self.web_session = web_session
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

                #Buttons
                ft.Divider(height=9, thickness=3),
                ft.Text(
                    value="Work Completed?",
                    size=20,
                    italic=True
                ),
                ft.Row(
                    controls=[
                        ft.TextButton(
                            text="YES",
                            on_click= self.on_update,

                        ),
                        ft.TextButton(
                            text="NO",
                            on_click=self.on_update,

                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_AROUND
                )

            ]
        )

    def on_update(self, e):
        print(e.control.text)
        if e.control.text == "YES":
            self.web_session.update_work_on(e.control.text)
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("OK... Continue working please")
            )
            self.page.snack_bar.open = True
            self.page.update()