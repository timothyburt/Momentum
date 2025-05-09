import flet as ft
from Engine.themes import ThemeFactory

class ActivitiesPage:
    def __init__(self, current_theme):
        self.current_theme = ThemeFactory.dark_theme() if current_theme == "dark" else ThemeFactory.light_theme()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Activities Page", size=24, weight=ft.FontWeight.BOLD, color=self.current_theme.text_color),
                    ft.Text("This is the Activities page of the app.", size=16, color=self.current_theme.text_color),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            alignment=ft.alignment.center,
            expand=True,
        )