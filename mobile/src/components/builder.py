import flet as ft
from pages.home import HomePage
from pages.activities import ActivitiesPage
from pages.focus import FocusPage
from pages.skills import SkillsPage
from components.header import Header
from components.nav import NavigationBar
from settings.themes import ThemeFactory
from components.page import Page

class PageBuilder(Page):
    def __init__(self, app):
        super().__init__()  # Initialize the Page class
        self.app = app
        self.current_theme = ThemeFactory.dark_theme()  # Use ThemeFactory for dark theme
        self.header = Header(app)
        self.navigation_bar = NavigationBar(app)

    def toggle_theme(self):
        self.current_theme = (
            ThemeFactory.light_theme() if self.current_theme == ThemeFactory.dark_theme() else ThemeFactory.dark_theme()
        )
        self.apply_theme()

    def apply_theme(self):
        self.page.bgcolor = self.current_theme.bgcolor
        self.page.views.clear()  # Clear and re-render views to apply theme changes
        self.page.views.append(self.build_page(self.page.route))  # Reapply the current route
        self.page.update()

    def build_page(self, route):
        current_theme = self.current_theme

        if route == "/activities":
            return ft.View(
                route="/activities",
                controls=[
                    ft.Column(
                        [
                            self.header.create_header(),
                            ft.Container(
                                content=ActivitiesPage(current_theme).build(),
                                expand=True,
                            ),
                            self.navigation_bar.get_navigation_bar_container(),
                        ],
                        expand=True,
                    ),
                ],
            )
        elif route == "/focus":
            return ft.View(
                route="/focus",
                controls=[
                    ft.Column(
                        [
                            self.header.create_header(),
                            ft.Container(
                                content=FocusPage(current_theme).build(),
                                expand=True,
                            ),
                            self.navigation_bar.get_navigation_bar_container(),
                        ],
                        expand=True,
                    ),
                ],
            )
        elif route == "/skills":
            return ft.View(
                route="/skills",
                controls=[
                    ft.Column(
                        [
                            self.header.create_header(),
                            ft.Container(
                                content=SkillsPage(current_theme).build(),
                                expand=True,
                            ),
                            self.navigation_bar.get_navigation_bar_container(),
                        ],
                        expand=True,
                    ),
                ],
            )
        else:
            return ft.View(
                route="/",
                controls=[
                    ft.Column(
                        [
                            self.header.create_header(),
                            ft.Container(
                                content=HomePage(self.page, self.navigation_bar.navigation_bar, current_theme).build(),
                                expand=True,
                            ),
                            self.navigation_bar.get_navigation_bar_container(),
                        ],
                        expand=True,
                    ),
                ],
            )