import flet as ft
from Engine.themes import ThemeFactory

class HomePage:
    def __init__(self, page: ft.Page, navigation_bar, current_theme):
        self.page = page
        self.navigation_bar = navigation_bar
        self.current_theme = ThemeFactory.dark_theme() if current_theme == "dark" else ThemeFactory.light_theme()

    def create_search_bar(self):
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
            padding=ft.padding.only(left=25, right=25, bottom=20),
        )

    def create_daily_overview(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Daily Progress",
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                                size=14,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("Tasks", color=ft.Colors.GREY_400, size=10),
                                    ft.Text("50%", weight=ft.FontWeight.BOLD, size=8, color=ft.Colors.GREEN),
                                    ft.Text("Goals", color=ft.Colors.GREY_400, size=10),
                                    ft.Text("15%", weight=ft.FontWeight.BOLD, size=8, color=ft.Colors.BLUE),
                                    ft.Text("Levels", color=ft.Colors.GREY_400, size=10),
                                    ft.Text("5%", weight=ft.FontWeight.BOLD, size=8, color=ft.Colors.RED),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=5,
                            ),
                            ft.Column(
                                [
                                    ft.ProgressBar(
                                        value=0.5,
                                        bgcolor=ft.Colors.GREY_800,
                                        color=ft.Colors.GREEN,
                                        height=10,
                                        width=150,
                                        border_radius=10,
                                    ),
                                    ft.ProgressBar(
                                        value=0.4,
                                        bgcolor=ft.Colors.GREY_800,
                                        color=ft.Colors.BLUE,
                                        height=10,
                                        width=150,
                                        border_radius=10,
                                    ),
                                    ft.ProgressBar(
                                        value=0.1,
                                        bgcolor=ft.Colors.GREY_800,
                                        color=ft.Colors.RED,
                                        height=10,
                                        width=150,
                                        border_radius=10,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                                spacing=20,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
            bgcolor=ft.Colors.GREY_900,
            border_radius=10,
            height=150,
            padding=10,
        )

    def create_skills_section(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Popular Skills",
                                weight=ft.FontWeight.BOLD,
                                color=self.current_theme.text_color,
                                size=14,
                            ),
                            ft.TextButton(
                                "View All",
                                on_click=lambda e: [
                                    setattr(self.navigation_bar, "selected_index", 3),
                                    self.page.go("/skills"),
                                ],
                                style=ft.ButtonStyle(
                                    color=self.current_theme.accent_color,
                                    padding=ft.padding.only(left=10, right=10),
                                    text_style=ft.TextStyle(size=10),
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Stack(
                                    controls=[
                                        ft.Image(
                                            src=f"https://picsum.photos/200/200?0",
                                            width=100,
                                            height=75,
                                            fit=ft.ImageFit.COVER,
                                            border_radius=ft.border_radius.all(10),
                                        ),
                                        ft.Text(
                                            "Wellness",
                                            size=12,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                ),
                                padding=ft.padding.only(left=25),
                            ),
                            *[
                                ft.Stack(
                                    controls=[
                                        ft.Image(
                                            src=f"https://picsum.photos/200/200?{i}",
                                            width=100,
                                            height=75,
                                            fit=ft.ImageFit.COVER,
                                            border_radius=ft.border_radius.all(10),
                                        ),
                                        ft.Text(
                                            skill_name,
                                            size=12,
                                            color=ft.Colors.WHITE,
                                            weight=ft.FontWeight.BOLD,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                )
                                for i, skill_name in enumerate([
                                    "Mental Health",
                                    "Career",
                                    "Fitness",
                                    "Habits",
                                ], start=1)
                            ],
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        scroll="always",
                    ),
                ],
                spacing=10,
            ),
            padding=ft.padding.only(left=25, right=25),
        )

    def create_recommended_tasks(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Recommended Tasks",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                        size=14,
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN, size=20),
                                        ft.Text(
                                            "Complete 5 tasks today",
                                            color=ft.Colors.WHITE,
                                            size=12,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                padding=ft.padding.all(10),
                                bgcolor=ft.Colors.GREY_900,
                                border_radius=ft.border_radius.all(10),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.FITNESS_CENTER, color=ft.Colors.BLUE, size=20),
                                        ft.Text(
                                            "Do a 30-minute workout",
                                            color=ft.Colors.WHITE,
                                            size=12,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                padding=ft.padding.all(10),
                                bgcolor=ft.Colors.GREY_900,
                                border_radius=ft.border_radius.all(10),
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(ft.Icons.BOOKMARK_OUTLINE, color=ft.Colors.YELLOW, size=20),
                                        ft.Text(
                                            "Read 10 pages of a book",
                                            color=ft.Colors.WHITE,
                                            size=12,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                padding=ft.padding.all(10),
                                bgcolor=ft.Colors.GREY_900,
                                border_radius=ft.border_radius.all(10),
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
            ),
            padding=ft.padding.only(left=25, right=25, top=20),
        )

    def build(self):
        return ft.Column(
            [
                self.create_search_bar(),
                ft.Container(
                    self.create_daily_overview(),
                    padding=ft.padding.only(left=25, right=25),
                ),
                self.create_skills_section(),
                self.create_recommended_tasks(),
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
        )