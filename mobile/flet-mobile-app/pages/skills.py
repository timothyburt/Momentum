import flet as ft

def skills_page():
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "Skills Page",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    "This is where the skills content will go.",
                    size=14,
                    color=ft.Colors.GREY_400,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.padding.all(20),
        bgcolor=ft.Colors.GREY_900,
        border_radius=10,
    )