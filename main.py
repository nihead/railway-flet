import logging
import flet as ft
import os


logging.basicConfig(level=logging.INFO)

import flet as ft
from flet import (Row,
                  Column,
                  Container,
                  UserControl,
                  ControlEvent,
                  Page,
                  Text,
                  ElevatedButton,
                  BottomSheet,
                  TextField, )



class Counter(UserControl):
    def __init__(self, name: str, start_counter: int = 0) -> None:
        super().__init__()
        self.name = Text(
            name,
            size=25,
            weight=ft.FontWeight.W_300,
            color=ft.colors.RED_400
        )
        self.counter = start_counter
        self.counter_text = Text(str(self.counter), size=50, color='blue')

    def counter_add(self, e: ControlEvent) -> None:
        self.counter += 1
        self.counter_text.value = str(self.counter)
        self.update()

    def counter_sub(self, e: ControlEvent) -> None:
        self.counter -= 1
        self.counter_text.value = str(self.counter)
        self.update()

    def build(self) -> Container:
        return Container(
            content=Column(
                controls=[
                    # Counter header Row
                    Row(
                        controls=[self.name],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Counter control row
                    Row(
                        controls=[
                            ElevatedButton(
                                text="Add",
                                on_click=self.counter_add,
                            ),
                            self.counter_text,
                            ElevatedButton(
                                text="Sub",
                                on_click=self.counter_sub,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        spacing=20,
                        width=500
                    ),
                ],
            ),
            bgcolor=ft.colors.GREY_50,
            border_radius=25,
            padding=12,
            # height=100,
        )


def input_name(page, e: ControlEvent) -> ft.BottomSheet:
    counter_name = TextField(
        hint_text="counter name",

    )

    def dismissed() -> None:
        pass

    def on_save(name: str, e: ControlEvent) -> None:
        page.close(bt)
        page.add(Counter(name, start_counter=0))

    bt = BottomSheet(
        on_dismiss=dismissed(),
        content=Column(
            controls=[
                Container(
                    content=None,
                    width=100,
                    height=6,
                    border_radius=3,
                    bgcolor=ft.colors.GREY_50,
                    margin=5,
                    on_click=lambda e: page.close(bt),
                ),
                Row(
                    controls=[
                        Text(
                            "Create name for counter",
                            size=25,
                            weight=ft.FontWeight.W_300,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                Container(
                    content=counter_name,
                    padding=16,
                ),
                ElevatedButton(
                    text="Save",
                    on_click=lambda e: on_save(counter_name.value, e),
                    width=150,
                    height=50,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,

        )
    )

    return bt


def main(page: Page):
    page.title = "Faseyha Counter"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        Counter("Today"),
        Counter("Yesterday"),
        ft.FloatingActionButton(
            icon=ft.icons.ADD,
            on_click=lambda _: page.open(input_name(page, _))
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=None, port=int(os.getenv("PORT", 8502)))