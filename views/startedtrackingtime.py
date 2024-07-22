import flet as ft
from time import sleep
from services.webServer import ScanUser

class StartedTrackingTime(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.overlay.clear()
        self.on_loading = PageLoading()
        self.page.overlay.append(self.on_loading)

        self.route = "/Startedtrackingtime"
        self.spacing = 0
        self.padding = 0
        self.get_saved()

        #declarations
        self.page_body = PageBody(self.page)

        self.controls = [
            ft.Container(
                expand=True,
                content=ft.Stack(
                    expand=True,
                    controls=[
                        PageHeader(self.page, self.updater),
                       self.page_body,
                    ]
                )
            )

        ]

    def updater(self, e):
        print("updater")
        self.on_loading.visible = True

        try:
            session = ScanUser(self.page)
            login = session.login(self.winSaved['uid'])
            if login:
                self.get_saved()
                sleep(1)
                self.page_body.username.value = self.winSaved['name']
                self.page_body.total_lt.value = self.winSaved['total_lt']
                self.page_body.task_lt.value = self.winSaved['task_lt']
                self.page_body.username.update()
                self.page_body.total_lt.update()
                self.page_body.task_lt.update()
                self.on_loading.visible = False
            else:
                self.on_loading.visible = False
                self.page.snack_bar = InfoDisplay(f"Error While Loading Page")
                self.page.snack_bar.open = True
                self.page.update()


        except Exception as e:
            self.on_loading.visible = False
            self.page.snack_bar = InfoDisplay(f"Error Updataing: {e}")
            self.page.snack_bar.open = True
            self.page.update()
            print(e)
        finally:
            self.on_loading.visible = False
            session.on_close()
            del session


    def save_response(self, obj):
        self.page.client_storage.set("winair_response", obj)
    def get_saved(self):
        if self.page.client_storage.contains_key("winair_response"):
            self.winSaved = self.page.client_storage.get("winair_response")
            print(self.winSaved)
            self.page.update()
        else:
            self.page.go("/")
            # self.winSaved = {
            #         "uid": "None",
            #         "name":  "None",
            #         "total_lt":  "00:00",
            #         "task_lt":  "00:00",
            #         "page_title":  "None",
            #         "work_on": "None",
            #         "work_on_code":  "None"
            #                        }

class PageHeader(ft.Container):
    def __init__(self, page, updater):
        super().__init__()
        self.page = page
        self.updater = updater

        self.bgcolor = ft.colors.RED_ACCENT_700
        self.padding = ft.padding.symmetric(horizontal=10)
        self.height =70
        self.content = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.END,
            controls=[
                ft.Row(
                    expand=True,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.icons.AIRPLANE_TICKET_OUTLINED, size=50),
                                ft.Text(
                                    value="Tracking Time",
                                    style=ft.TextStyle(24),
                                )
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.icons.REFRESH_OUTLINED,
                            icon_size=40,

                            on_click=self.updater
                        ),
                    ]
                )
            ]
        )


class PageBody(ft.Container):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.on_loading = PageLoading
        self.get_saved()
        #variables
        self.username = ft.Text(
                            value=self.winSaved['name'],
                            size=32,
                            italic=True,
                            weight=ft.FontWeight.W_400
                        )
        self.total_lt =ft.Text(
                            value=self.winSaved['total_lt'],
                            size=50,
                            weight=ft.FontWeight.BOLD
                        )
        self.task_lt = ft.Text(
            self.winSaved['task_lt'],
            size=28,
            weight=ft.FontWeight.W_700,
        )

        self.bgcolor = "#645757"
        self.margin = ft.margin.only(top=60)
        self.padding = ft.padding.symmetric(vertical=16)
        self.border_radius = ft.border_radius.vertical(top=15)
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            src="./assets/logo.png",
                            width=150,
                        )
                    ]

                ),
                # Duser name info
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.username
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Total Time",
                            size=24,
                        )
                    ]
                ),
                ## Total_lt display
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        self.total_lt
                    ]
                ),
                ft.Container(height=15),
                # Task Card info
                PageBodyCard(self.page, self.task_lt),
                ft.Container(height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            border_radius=16,
                            width=450,
                            margin=ft.margin.symmetric(horizontal=30),
                            padding=ft.padding.symmetric(vertical=16, horizontal=5),
                            border=ft.border.all(2, ft.colors.WHITE),
                            content=ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                "Task Completed?...",
                                                size=24,
                                                weight=ft.FontWeight.W_600,
                                                italic=True,
                                                color = ft.colors.RED_ACCENT_400
                                            )
                                        ]
                                    ),
                                    ft.Container(
                                        padding=20,
                                        content=ft.Row(
                                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                            controls=[
                                                ft.Container(
                                                    on_click=self.on_btn_clicked,
                                                    on_hover=self.on_btn_hover,
                                                    border_radius=16,
                                                    bgcolor="#F24444",
                                                    padding=ft.padding.symmetric(vertical=16, horizontal=40),
                                                    # height=32,
                                                    content=ft.Row(
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Text(
                                                                "NO",
                                                                color="#FFFFFF",
                                                                weight=ft.FontWeight.BOLD
                                                            )
                                                        ]
                                                    )
                                                ),
                                                ft.Container(
                                                    on_click=self.on_btn_clicked,
                                                    on_hover=self.on_btn_hover,
                                                    border_radius=16,
                                                    bgcolor="#F24444",
                                                    padding=ft.padding.symmetric(vertical=16, horizontal=40),
                                                    # height=32,
                                                    content=ft.Row(
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        controls=[
                                                            ft.Text(
                                                                "YES",
                                                                color="#FFFFFF",
                                                                weight=ft.FontWeight.BOLD
                                                            )
                                                        ]
                                                    )
                                                )
                                            ]
                                        )
                                    ),
                                ]
                            )
                        ),
                    ]
                )
            ]

        )

    def save_response(self, obj):
        self.page.client_storage.set("winair_response", obj)

    def get_saved(self):
        if self.page.client_storage.contains_key("winair_response"):
            self.winSaved = self.page.client_storage.get("winair_response")
        else:
            self.page.go("/")
            # self.winSaved = {
            #     "uid": "None",
            #     "name": "None",
            #     "total_lt": "00:00",
            #     "task_lt": "00:00",
            #     "page_title": "None",
            #     "work_on": "None",
            #     "work_on_code": "None"
            # }

    def on_btn_clicked(self, e):
        self.on_loading.visible = True
        self.page.update()
        btn = e.control.content.controls[0].value
        try:
            print("tring...")
            w_obj = ScanUser(self.page)
            # print(f'uid: {self.winSaved['uid']}')
            w_login = w_obj.login(self.winSaved['uid'])
            self.get_saved()
            print(w_login)
            print(self.winSaved)
            if w_login:
                # print(f"page title: {self.winSaved['page_title']}")
                if  w_obj.update_work_on(btn):
                    if btn == "YES":
                        self.on_loading.visible = False
                        self.page.update()
                        InfoDisplay("Please delete Saved Task from pending task list")
                        self.page.snack_bar.open= True
                        self.page.update()
                        sleep(3)
                        self.page.go("/Scantaskcard")

                else:
                    self.on_loading.visible = False
                    self.page.update()
                    print("work update failed")
                    self.page.snack_bar = InfoDisplay("update Failed...try again")
                    self.page.snack_bar.open = True
                    self.page.update()
            else:
                self.on_loading.visible = False
                self.page.update()
                print("login failed")
                self.page.snack_bar = InfoDisplay("Login Failed...")
                self.page.snack_bar.open = True
                self.page.update()
                sleep(3)
                self.page.go("/")

        except Exception as e:
            print("onerror")
            print(e)
            self.page.snack_bar = InfoDisplay(f"ERROR...{e}")
            self.page.snack_bar.open = True
            self.page.update()
            sleep(3)
            self.page.go("/")
        finally:
            w_obj.on_close()
            del w_obj
        print(f"You Clicked: {btn}")

    def on_btn_hover(self, e):
        if e.data == "true":
            e.control.bgcolor = ft.colors.RED_ACCENT_700
            self.update()
        else:

            e.control.bgcolor = "#F24444"
            self.update()


class PageBodyCard(ft.Card):
    def __init__(self, page, task_lt):
        super().__init__()
        self.page = page
        self.get_saved()
        self.working_task = ft.Text(
            value=self.winSaved['work_on'],
            size=24,
            italic=True
        )
        self.working_task_code = ft.Text(
            value=self.winSaved['work_on_code'],
            size=24,
            italic=True,
            weight=ft.FontWeight.W_600
        )
        self.this_task_time= task_lt
        self.margin = ft.margin.symmetric(horizontal=30)
        self.content = ft.Container(
            border=ft.border.all(2,ft.colors.RED_ACCENT_100),
            border_radius=6,
            padding=16,
            expand=True,
            margin=8,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[ft.Text(
                            "This Task",
                            size=24,
                            weight=ft.FontWeight.W_400,
                            color=ft.colors.RED_ACCENT_400,
                        )],
                    ),

                    # work info
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.Column(
                                spacing=0,
                                controls=[
                                    self.working_task_code,
                                    self.working_task,
                                ]
                            )
                        ],
                    ),
                    ft.Row(

                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "This Task Time",
                                size=24,
                                weight=ft.FontWeight.W_400,
                                color=ft.colors.RED_ACCENT_400,
                            )],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[self.this_task_time],
                    ),
                ]
            )
        )

    def save_response(self, obj):
        self.page.client_storage.set("winair_response", obj)

    def get_saved(self):
        if self.page.client_storage.contains_key("winair_response"):
            self.winSaved = self.page.client_storage.get("winair_response")
        else:
            self.page.go("/")
            # self.winSaved = {
            #         "uid": "None",
            #         "name":  "None",
            #         "total_lt":  "00:00",
            #         "task_lt":  "00:00",
            #         "page_title":  "None",
            #         "work_on": "None",
            #         "work_on_code":  "None"
            #                        }


class InfoDisplay(ft.SnackBar):
    def __init__(self, msg):
        super().__init__()
        self.controls = ft.Text(msg)

class PageLoading(ft.Container):
    def __init__(self):
        super().__init__()
        self.visible = False
        self.expand = True
        self.content=ft.Stack(
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=ft.colors.BLACK87,
                    opacity=0.9,
                ),
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.icons.RUN_CIRCLE_OUTLINED,
                                    size=90,
                                    color=ft.colors.RED_ACCENT_400,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,

                        ),
                        ft.Text("Loading..", size=40, weight="bold", color=ft.colors.RED_ACCENT_400),

                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )

            ]
        )
