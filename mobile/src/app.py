import flet as ft
from pages.home import HomePage
from pages.activities import ActivitiesPage
from pages.focus import FocusPage
from pages.skills import SkillsPage
from settings.themes import ThemeFactory
from components.header import Header

class MomentumApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.current_theme = ThemeFactory.dark_theme()  # Use ThemeFactory for dark theme
        self.navigation_bar = None
        self.navigation_bar_container = None
        self.header = Header(self)  # Initialize the Header class

    def toggle_theme(self):
        self.current_theme = (
            ThemeFactory.light_theme() if self.current_theme == ThemeFactory.dark_theme() else ThemeFactory.dark_theme()
        )
        self.apply_theme()

    def apply_theme(self):
        self.page.bgcolor = self.current_theme.bgcolor
        self.navigation_bar_container.bgcolor = self.current_theme.nav_bgcolor
        self.navigation_bar.indicator_color = self.current_theme.indicator_color
        self.page.views.clear()  # Clear and re-render views to apply theme changes
        self.route_change(self.page.route)  # Reapply the current route
        self.page.update()

    def setup_navigation_bar(self):
        self.navigation_bar = ft.NavigationBar(
            bgcolor=self.current_theme.nav_bgcolor,
            indicator_color=self.current_theme.indicator_color,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.Icons.HOME_ROUNDED,
                    label="Home",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
                    label="Activities",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.TIMER,
                    label="Focus",
                ),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BAR_CHART_ROUNDED,
                    label="Skills",
                ),
            ],
            selected_index=0,  # Default to the first tab
            on_change=lambda e: self.navigate_to(e.control.selected_index),  # Handle navigation
        )

        self.navigation_bar_container = ft.Container(
            content=self.navigation_bar,
            bgcolor=self.current_theme.nav_bgcolor  # Match the theme's navigation bar color
        )

    def route_change(self, route):
        self.page.views.clear()
        if self.page.route == "/activities":
            self.page.views.append(
                ft.View(
                    route="/activities",
                    controls=[
                        ft.Column(
                            [
                                self.header.create_header(),  # Use Header class
                                ft.Container(
                                    content=ActivitiesPage(),
                                    expand=True,
                                ),
                                ft.Container(
                                    content=self.navigation_bar_container,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,
                        ),
                    ],
                )
            )
        elif self.page.route == "/focus":
            self.page.views.append(
                ft.View(
                    route="/focus",
                    controls=[
                        ft.Column(
                            [
                                self.header.create_header(),  # Use Header class
                                ft.Container(
                                    content=FocusPage(),
                                    expand=True,
                                ),
                                ft.Container(
                                    content=self.navigation_bar_container,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,
                        ),
                    ],
                )
            )
        elif self.page.route == "/skills":
            self.page.views.append(
                ft.View(
                    route="/skills",
                    controls=[
                        ft.Column(
                            [
                                self.header.create_header(),  # Use Header class
                                ft.Container(
                                    content=SkillsPage(),
                                    expand=True,
                                ),
                                ft.Container(
                                    content=self.navigation_bar_container,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,
                        ),
                    ],
                )
            )
        else:
            self.page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Column(
                            [
                                self.header.create_header(),  # Use Header class
                                ft.Container(
                                    content=HomePage(self.page, self.navigation_bar, self.current_theme),
                                    expand=True,
                                ),
                                ft.Container(
                                    content=self.navigation_bar_container,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,
                        ),
                    ],
                )
            )
        self.page.update()

    def navigate_to(self, index):
        if index == 0:
            self.page.go("/")
        elif index == 1:
            self.page.go("/activities")
        elif index == 2:
            self.page.go("/focus")
        elif index == 3:
            self.page.go("/skills")

    def run(self):
        self.page.title = "Momentum App"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.padding = 0
        self.page.window.height = 700
        self.page.window.width = 350
        self.page.window.resizable = False

        self.setup_navigation_bar()

        self.page.on_route_change = self.route_change
        self.page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.Column(
                        [
                            self.header.create_header(),  # Use Header class
                            ft.Container(
                                content=HomePage(self.page, self.navigation_bar, self.current_theme),
                                expand=True,
                            ),
                            ft.Container(
                                content=self.navigation_bar_container,
                                alignment=ft.alignment.bottom_center,
                            ),
                        ],
                        expand=True,
                    ),
                ],
            )
        )
        self.apply_theme()
        self.page.go(self.page.route)


def main(page: ft.Page):
    app = MomentumApp(page)
    app.run()


if __name__ == "__main__":
    ft.app(target=main)
