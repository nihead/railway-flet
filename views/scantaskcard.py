import flet as ft
from dataclasses import dataclass
from services.webServer import ScanUser
@dataclass
class Task:
    task_id: str
    task_desc: str


class ScanTasksPage(ft.View):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.overlay.clear()
        if self.page.client_storage.contains_key("winair_response"):
            self.local_strorage = self.page.client_storage.get("winair_response")
        else:
            self.local_strorage = {
                    "uid": "None",
                    "name":  "None",
                    "total_lt":  "00:00",
                    "task_lt":  "00:00",
                    "page_title":  "None",
                    "work_on": "None",
                    "work_on_code":  "None"
                                   }

        # self.web_session = web_session
        # print(f"current user is {self.web_session.user.name}")
        # if not self.web_session.user.name:
        #     self.page.go("/")
        #     exit()

        # view parameters
        if self.page.client_storage.contains_key('saved_tasks'):
            self.saved_tasks = self.page.client_storage.get('saved_tasks')
        else:
            self.saved_tasks = []

        self.body_saved_list =ft.ListView(
            expand=True,
            # visible=1,
            spacing=10,
            padding=20,
            auto_scroll=True,
            controls=[

            ],
        )
        self.empty_list = SavedEmpty()
        # self.page.client_storage.set("saved_tasks", [{"task_id":"1001", "task_desc":"Task 1"},
        #                                              {"task_id":"1002", "task_desc":"Task 2"}])

        # saved task declaration
        if self.page.client_storage.contains_key('saved_tasks'):
            print("Storage exists")
            self.saved_tasks = self.page.client_storage.get('saved_tasks')
            if len(self.saved_tasks) > 0:
                self.empty_list.visible = 0
                # self.body_saved.controls.clear()
                for saved_task in self.saved_tasks:
                    self.body_saved_list.controls.append(
                        TaskContainer(self.on_task_done, saved_task["task_id"], saved_task["task_desc"], self.on_saved_task_click)
                    )
                self.page.update()
            print("client storage updated!")
        else:
            self.saved_tasks = []


        self.add_task_form_task_id = ft.TextField(
            hint_text="Task ID",
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
            autofocus=True
        )

        self.add_task_form_task_desc = ft.TextField(
            hint_text="Task Description (optional)",
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
        )

        #tasl list header
        self.task_list_header = ft.Container(
            padding=ft.padding.only(top=10),
            content=ft.Column(
                controls=[
                    ft.Row(
                        [ft.Text(
                            "Pending Tasks",
                            size=25,
                            weight=ft.FontWeight.W_600,
                            color=ft.colors.RED_ACCENT_700
                        )],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ]
            )
        )
        self.add_task_card = ft.Container(
            visible=False,
            padding=16,
            expand=True,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Card(
                        opacity=1,
                        content=ft.Container(
                            padding=ft.padding.symmetric(horizontal=23),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    # top container
                                    ft.Container(
                                        opacity=0.6,
                                        width=100,
                                        height=4,
                                        bgcolor=ft.colors.WHITE,
                                        border_radius=2,
                                        margin=4
                                    ),
                                    ft.Text(
                                        "Add Task",
                                        size=25,
                                        italic=True,
                                    ),
                                    ft.Container(
                                        content=ft.Row(
                                            [ft.Text(
                                                value="TC",
                                                size=20,
                                                weight=ft.FontWeight.W_400,
                                            ),
                                            self.add_task_form_task_id]
                                        ),
                                        bgcolor=ft.colors.SURFACE_VARIANT,
                                        padding=ft.padding.symmetric(horizontal=12),
                                        border_radius=12
                                    ),
                                    ft.Container(
                                        content=self.add_task_form_task_desc,
                                        bgcolor=ft.colors.SURFACE_VARIANT,
                                        padding=ft.padding.symmetric(horizontal=12),
                                        border_radius=12
                                    ),
                                    ft.Divider(thickness=2),
                                    ft.Row(
                                        controls=[
                                            ft.ElevatedButton(
                                                text="Cancel",
                                                icon=ft.icons.CANCEL,
                                                style=ft.ButtonStyle(),
                                                on_click=self.on_add_task_cancel
                                            ),
                                            ft.ElevatedButton(
                                                text="SAVE",
                                                icon=ft.icons.SAVE,
                                                on_click=self.on_save
                                            ),
                                            ft.ElevatedButton(
                                                text="SUBMIT",
                                                icon=ft.icons.START_ROUNDED,
                                                on_click=self.on_task_submit
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_EVENLY
                                    ),
                                    ft.Container(
                                        height=20
                                    )
                                ]
                            )
                        )
                    )
                ]
            )

        )
        #dummy container
        self.dummy_container = ft.Container(
            expand=True,
            opacity=0.3,
            bgcolor=ft.colors.RED,
            content=None,
            visible=False
        )

        # saved Task confirm box declair
        self.saved_task_confirm_box = ConfirmTaskStart(self.on_task_start)

        # self.expand = True
        self.route = "/Startedtrackingtime"
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.spacing= 0
        self.padding= 0

        self.controls = [
            ft.Container(
                content=ft.Stack(
                    [
                        ft.Column(
                            spacing=8,
                            controls=[
                                #header
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Text(
                                                "RTLT Task Manager",
                                                size=40,
                                                weight=ft.FontWeight.W_900,
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                    # expand=True,
                                    height=80,
                                    bgcolor=ft.colors.GREY_800,
                                    padding=10,
                                    alignment=ft.alignment.center
                                ),
                                # user info
                                UserInfo(self.local_strorage['name'], self.local_strorage['total_lt']),
                            #body
                            ft.Container(
                                bgcolor=ft.colors.GREY_500,
                                margin=ft.margin.symmetric(horizontal=16),
                                border_radius=ft.border_radius.only(top_left=20,top_right=20),
                                padding=5,
                                expand=True,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        self.task_list_header,
                                        ft.Divider(thickness=3, height=9),
                                        ft.Container(
                                            expand=True,
                                            content=ft.Stack(
                                            [
                                                ft.Container(
                                                    # List view update area
                                                    expand=True,
                                                    content=ft.Stack(
                                                        [self.body_saved_list,
                                                         self.empty_list]
                                                    ),

                                                ),
                                                # add button
                                                ft.FloatingActionButton(
                                                    icon=ft.icons.STAR,
                                                    right=5,
                                                    bottom=10,
                                                    shape=ft.CircleBorder(),
                                                    on_click=self.on_add_task_form
                                                )
                                            ]
                                        ),
                                        )
                                    ]
                                ),
                            )
                            ],
                        ),
                        # main stack item 2
                        self.dummy_container,
                        # main stack item 3
                        self.add_task_card,
                        # save confirm
                        self.saved_task_confirm_box,
                    ]
                ),
                bgcolor=ft.colors.GREY_400,
                expand=True,
                margin=0,
                padding=0,
                width=700

            )
        ]


    def on_save(self, e):
        try:
            if self.page.client_storage.contains_key("saved_tasks"):
                self.saved_tasks = self.page.client_storage.get("saved_tasks")
            else:
                self.saved_tasks = [{"task_id": "", "task_desc": ""}]
            print("try saving")
            if self.add_task_form_task_id.value not in [ta["task_id"] for ta in self.saved_tasks]:
                print('Saving ...')

                u = Task(self.add_task_form_task_id.value, self.add_task_form_task_desc.value)
                self.saved_tasks.append(u)
                print(u)
                self.page.client_storage.set('saved_tasks', self.saved_tasks)
                self.body_saved_list.controls.append(
                    TaskContainer(self.on_task_done, u.task_id, u.task_desc, self. on_saved_task_click)
                )

                if self.empty_list.visible:
                    self.empty_list.visible = 0
                    self.page.update()

                else:
                    self.page.update()
            else:
                print('Task already Duplicate Tasks')
                self.snack_disp("Duplicate tasks found.. last task not Saved")
        except Exception as e:
            print(f'Error while save {e}')
            self.page.update()

        #POP UP CLEAR
        self.on_add_task_cancel("e")

    def on_add_task_form(self,e):
        self.add_task_card.visible = True
        self.dummy_container.visible = True
        self.page.update()

    def on_add_task_cancel(self, e):
        self.add_task_form_task_id.value = ''
        self.add_task_form_task_desc.value = ''
        self.add_task_card.visible = False
        self.dummy_container.visible = False
        self.page.update()

    def on_task_done(self, e):
        self.body_saved_list.controls.remove(e)
        self.saved_tasks = self.page.client_storage.get("saved_tasks")
        if isinstance(e, ft.Container):
            t = e.content.controls[0].controls[0].content.controls[0].value
        else:
            t = e
        task_index = next((index for index, task in enumerate(self.saved_tasks) if task["task_id"] == t), -1)
        del self.saved_tasks[task_index]
        self.page.client_storage.set("saved_tasks", self.saved_tasks)
        self.snack_disp(f"Task deletedw")

        print(self.saved_tasks)

        if len(self.saved_tasks) == 0:
            print("No tasks saved")
            self.empty_list.visible = 1
            self.empty_list.update()
            self.body_saved_list.update()
            self.page.update()

        self.page.update()

    def on_task_submit(self, e):
        print("Submitting....", self.add_task_form_task_id.value)
        tid = self.add_task_form_task_id.value
        self.on_add_task_cancel(tid)
        self.on_task_start(tid)
        print("end of  Submit ", tid)

    def on_saved_task_click(self, e):
        clicked_task  = e.content.controls[0].controls[0].content.controls[0].value
        clicked_task_desc = e.content.controls[0].controls[0].content.controls[1].value
        self.saved_task_confirm_box.content.controls[1].content.controls[0].content.content.controls[1].controls[0].value = clicked_task
        self.saved_task_confirm_box.content.controls[1].content.controls[0].content.content.controls[1].controls[2].value = clicked_task_desc
        self.saved_task_confirm_box.visible = True
        self.update()
        self.page.update()


        print("You clicked Task")
        print(e.content.controls[0].controls[0])

    def on_task_start(self, tid):
        self.saved_task_confirm_box.visible = False
        self.dummy_container.visible = False
        self.page.update()
        print("Starting working on ",tid)

        try:
            save = ScanUser(self.page)
            saved, msg = save.start_task(tid)
            print(saved)
        except Exception as e:
            print("error while saving", e)
            self.snack_disp(f"Error while saving:-> {e}")
        finally:
            save.on_close()
            del save

        if saved:
            self.page.go("/Startedtrackingtime")
        else:
            self.snack_disp(f"Failed to start!.. {msg}")

    def snack_disp(self, msg):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg)
        )
        self.page.snack_bar.open = True
        self.page.update()

class TaskContainer(ft.Container):
    def __init__(self, on_delete, task_id, task_desc, on_Task_click):
        super().__init__()
        self.on_task_clicked = on_Task_click
        self.delete = on_delete
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.padding = ft.padding.symmetric(vertical=10, horizontal=25)
        self.border_radius = 20
        # self.on_click = self.on_task_click
        # self.expand= True
        self.height = 60
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Text(task_id),
                                    ft.Text(task_desc) if task_desc else ft.Text(),
                                ],
                                expand=True
                            ),
                            on_click=self.on_task_click,
                            expand=True
                        ),

                            ft.IconButton(
                                icon=ft.icons.DELETE_SWEEP,
                                on_click=self.on_delete
                            ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=8,
                    expand=True

                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True
        )

    def on_delete(self, e):
        self.delete(self)

    def on_task_click(self,e):
        self.on_task_clicked(self)


class UserInfo(ft.Container):
    def __init__(self, user_id, total_lt):
        super().__init__()
        self.user_id = user_id
        self.total_lt = total_lt
        self.bgcolor = ft.colors.GREY_900
        self.opacity =0.6
        self.padding = 25
        self.border_radius = 20
        self.margin= 16
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.PERSON_OUTLINED),
                        ft.Text(
                            value=self.user_id,
                            size=20,
                            color=ft.colors.WHITE,
                            weight="bold",
                            italic=True
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.TIMER_OUTLINED),
                        ft.Text(
                            value="Total Time: ",
                            size=20,
                            color=ft.colors.WHITE,
                            italic=True

                        ),
                        ft.Text(
                            value=self.total_lt,
                            size=30,
                            color=ft.colors.WHITE,
                            weight="bold",
                        )
                    ]
                )
            ]
        )

class SavedEmpty(ft.Column):
    def __init__(self):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.CENTER
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.expand = True

        self.controls = [
            ft.Container(
                bgcolor=ft.colors.RED_ACCENT_100,
                padding=ft.padding.symmetric(vertical=40, horizontal=20),
                margin=20,
                border_radius=40,
                opacity=0.6,
                content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.icons.ADD_TASK,size=50),
                            ]
                        ),

                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Text(
                                    value="Add Task to Save",
                                    size=30,
                                    italic=True,
                                    color=ft.colors.RED_ACCENT_700,
                                )
                            ]
                        )
                    ]
                )
            )
        ]


class ConfirmTaskStart(ft.Container):
    def __init__(self, started):
        super().__init__()
        self.on_start = started
        self.visible = False
        # self.padding = 35
        self.expand = True
        self.content = ft.Stack(
            [
                ft.Container(
                    expand=True,
                    padding=40,
                    bgcolor=ft.colors.RED_ACCENT_100,
                    opacity=0.6,
                ),
                ft.Container(
                    expand=True,
                    padding=40,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Card(
                                content=ft.Container(
                                    padding= ft.padding.symmetric(vertical=40, horizontal=20),
                                    content=ft.Column(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text(
                                                        value="Start Work On",
                                                        size=20,
                                                        weight="bold",
                                                    )
                                                ]
                                            ),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.Text(
                                                        value="task_id",
                                                        size=20,
                                                        weight=ft.FontWeight.W_400,
                                                        italic=True
                                                    ),
                                                    ft.Text(
                                                        value="  ",
                                                        size=20,
                                                        weight=ft.FontWeight.W_400,
                                                        italic=True
                                                    ),
                                                    ft.Text(
                                                        value="[Description]",
                                                        size=20,
                                                        weight=ft.FontWeight.W_400,
                                                        italic=True
                                                    ),
                                                ]
                                            ),
                                            ft.Divider(thickness=3, height=25),
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                controls=[
                                                    ft.ElevatedButton(
                                                        icon=ft.icons.CANCEL,
                                                        text="Cancel",
                                                        on_click=self.on_start_task_cancel
                                                    ),
                                                    ft.ElevatedButton(
                                                        icon=ft.icons.START_ROUNDED,
                                                        text="Start",
                                                        on_click=self.on_btn_start_click
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def on_btn_start_click(self, e):
        tid = self.content.controls[1].content.controls[0].content.content.controls[1].controls[0].value
        self.on_start(tid)

    def on_start_task_cancel(self, e):
        self.visible = False
        self.update()




