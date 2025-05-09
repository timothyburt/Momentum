import flet as ft

def skills_page():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Skills Page", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.ListView(
                    controls=[
                        ft.Text("1. Wellness - Focus on maintaining physical and mental well-being.", size=18, color=ft.Colors.WHITE),
                        ft.Text("2. Mental Health - Strategies to improve emotional and psychological resilience.", size=18, color=ft.Colors.WHITE),
                        ft.Text("3. Career - Tips and tools for professional growth and success.", size=18, color=ft.Colors.WHITE),
                        ft.Text("4. Fitness - Activities and routines to stay physically active and healthy.", size=18, color=ft.Colors.WHITE),
                        ft.Text("5. Habits - Focused on Home and domestic chores", size=18, color=ft.Colors.WHITE),
                    ],
                    spacing=10,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        ),
        alignment=ft.alignment.center,
        expand=True,
    )