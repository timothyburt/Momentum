import flet as ft
from Engine.themes import ThemeFactory

class ProfilePage:
    def __init__(self, current_theme):
        self.current_theme = ThemeFactory.dark_theme() if current_theme == "dark" else ThemeFactory.light_theme()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("User Profile", size=24, weight=ft.FontWeight.BOLD, color=self.current_theme.text_color),
                    ft.Text("Name: Blabber Fatmouth", size=18, color=self.current_theme.text_color),
                    ft.Text("Role: Novice", size=18, color=self.current_theme.text_color)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            expand=True,
        )