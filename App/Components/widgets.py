# Imports
import flet as ft

class Widgets:
    @staticmethod
    def search_bar():
        return ft.Container(
            content=ft.TextField(
                hint_text="Search Goals, Tasks, Workouts, etc",
                suffix_icon=ft.Icons.SEARCH,
                focused_border_color=ft.Colors.GREEN,
                bgcolor=ft.Colors.GREY_900,
                cursor_color=ft.Colors.WHITE,
                color=ft.Colors.WHITE,
                height=30,
                text_size=10,
                border_radius=10,
            ),
            padding=ft.Padding(left=25, right=25, top=0, bottom=20),
        )
