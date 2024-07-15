import flet as ft

class Home(ft.View):
    def __init__(self, page, websession):
        super().__init__()
        self.page = page
        self.web_session = websession
        self.route = "/"
        self.user_id_txt = ft.TextField(
            hint_text="User ID",
            expand=True,
            border=ft.InputBorder.NONE,
            hint_style=ft.TextStyle(
                italic=True
            ),
            text_style=ft.TextStyle(
                size=18,
                color=ft.colors.WHITE,
                weight=ft.FontWeight.W_600,
            ),
            on_change=self.on_user_input


        )

        self.controls = [
            ft.AppBar(title=ft.Text("TMA RTLT"), bgcolor=ft.colors.SURFACE_VARIANT),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Card(
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        # welcome message
                                        ft.Text(
                                            "WELCOME TO TMA RTLT",
                                            size=20,
                                            weight="bold",
                                        ),
                                        # company logo
                                        ft.Container(
                                            ft.Image(
                                                src="./assets/logo.png",
                                            ),
                                            padding=20,
                                        ),
                                        #user input
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Text("EC", weight=ft.FontWeight.W_600, size=18),
                                                    self.user_id_txt,
                                                ],
                                                vertical_alignment=ft.CrossAxisAlignment.CENTER
                                            ),
                                            padding=10,
                                            margin=10,
                                            border=ft.border.all(2, ft.colors.RED_ACCENT_100),
                                            border_radius=10,

                                        ),
                                        # submit button
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.icons.LOGIN_OUTLINED),
                                                    ft.Text(
                                                        "Continue",
                                                        size=14,
                                                    )
                                                ],
                                                alignment=ft.MainAxisAlignment.CENTER
                                            ),
                                            padding=8,
                                            border=ft.border.all(2, ft.colors.RED_ACCENT_100),
                                            border_radius=20,
                                            bgcolor=ft.colors.SURFACE_VARIANT,
                                            width=150,
                                            on_click=self.on_submit
                                        )

                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=20,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                padding=20
                            ),
                            margin=20,
                            width=450,

                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    expand=True,
                ),
                padding=16,
                alignment=ft.alignment.center,
                expand=True,
            ),
        ]
    def on_submit(self, e):
        if self.web_session.scan(self.user_id_txt.value):
            self.page.go("/scanned")
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid User ID"),
            )
            self.page.snack_bar.open = True
            self.page.update()

    def on_user_input(self, e):
        if not e.control.value.isnumeric():
            print("Invalid input")
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Invalid User ID"),
                action="Alright!",
            )
            self.page.snack_bar.open = True
            self.user_id_txt.value = ''
            self.user_id_txt.focus()
            self.page.update()