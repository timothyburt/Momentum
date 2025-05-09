# Imports
import flet as ft
from settings.themes import ThemeFactory
from components.page import Page
from components.builder import PageBuilder

class Header:
    def __init__(self, app):
        self.app = app
        self.page = Page().get_page()
        self.current_theme = PageBuilder(app).current_theme  # Get current theme from PageBuilder

    def view_profile(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("Viewing Profile"))
        self.page.snack_bar.open()
        self.page.update()

    def open_settings(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("Opening Settings"))
        self.page.snack_bar.open()
        self.page.update()

    def logout(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("Logging Out"))
        self.page.snack_bar.open()
        self.page.update()

    def create_header(self):
        popup_menu = ft.PopupMenuButton(
            content=ft.CircleAvatar(
                foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
                content=ft.Text("U"),
                radius=30,
                width=40,
                height=40,
            ),
            items=[
                ft.PopupMenuItem(
                    text="View Profile",
                    on_click=lambda e: self.view_profile(),
                ),
                ft.PopupMenuItem(
                    text="Settings",
                    on_click=lambda e: self.open_settings(),
                ),
                ft.PopupMenuItem(
                    text="Light Theme" if self.current_theme == ThemeFactory.dark_theme() else "Dark Theme",
                    icon=ft.Icons.LIGHT_MODE if self.current_theme == ThemeFactory.dark_theme() else ft.Icons.DARK_MODE,
                    on_click=lambda e: self.app.page_builder.toggle_theme(),  # Use the existing PageBuilder instance
                ),
                ft.PopupMenuItem(
                    text="Logout",
                    on_click=lambda e: self.logout(),
                ),
            ],
        )

        username = ft.Text(
            "Blabber Fatmouth".upper(),
            size=12,
            weight=ft.FontWeight.BOLD,
            color=self.current_theme.accent_color,
        )
        title = ft.Text("Novice", size=10, color=self.current_theme.text_color)
        user_info = ft.Column(
            [
                username,
                title,
            ],
            spacing=2,
        )

        notification_bell = ft.Icon(
            ft.Icons.NOTIFICATIONS,
            size=30,
            color=self.current_theme.text_color,
            badge=ft.Badge(small_size=10, bgcolor=ft.Colors.GREEN),
        )

        return ft.Container(
            content=ft.Row(
                [
                    popup_menu,
                    ft.Container(user_info, padding=2.5),
                    ft.Container(notification_bell, alignment=ft.alignment.center, expand=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
        )