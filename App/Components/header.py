# Imports
import flet as ft
from Engine.themes import ThemeFactory
from Engine.settings import Config as cogs

class Header:
    def __init__(self, app, current_theme):
        self.app = app
        self.page = ft.Page
        self.current_theme = ThemeFactory.dark_theme() if current_theme == "dark" else ThemeFactory.light_theme()

    # Ensure the `view_profile` method navigates to the `/profile` route
    def view_profile(self):
        self.page.go("/profile")  # Navigate to the profile route
        self.page.update()

    def toggle_theme(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("Themes: Switching theme."))
        self.page.snack_bar.open()
        self.app.page_builder.toggle_theme()  # Call the toggle_theme method from PageBuilder
        self.page.update()

    def logout(self):
        self.page.snack_bar = ft.SnackBar(ft.Text("Logout: You have been logged out."))
        self.page.snack_bar.open()
        self.page.update()

    # Modify the snack menu to include Profile, Themes, and Logout
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
                    text="Profile",
                    on_click=lambda e: self.view_profile(),
                ),
                ft.PopupMenuItem(
                    text="Themes",
                    icon=ft.Icons.PALETTE,
                    on_click=lambda e: self.toggle_theme(),
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
                    ft.Container(notification_bell,expand=True),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=cogs.APP_SPACING,
            border_radius=30,
        )