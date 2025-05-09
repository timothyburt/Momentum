import flet as ft
from Engine.themes import ThemeFactory

class SkillsPage:
    def __init__(self, current_theme):
        self.current_theme = ThemeFactory.dark_theme() if current_theme == "dark" else ThemeFactory.light_theme()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text("Skills Page", size=24, weight=ft.FontWeight.BOLD, color=self.current_theme.text_color),
                    ft.ListView(
                        controls=[
                            ft.Text("1. Wellness - Focus on maintaining physical and mental well-being.", size=18, color=self.current_theme.text_color),
                            ft.Text("2. Mental Health - Strategies to improve emotional and psychological resilience.", size=18, color=self.current_theme.text_color),
                            ft.Text("3. Career - Tips and tools for professional growth and success.", size=18, color=self.current_theme.text_color),
                            ft.Text("4. Fitness - Activities and routines to stay physically active and healthy.", size=18, color=self.current_theme.text_color),
                            ft.Text("5. Habits - Focused on Home and domestic chores", size=18, color=self.current_theme.text_color),
                        ],
                        spacing=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20,
            ),
            expand=True,
        )