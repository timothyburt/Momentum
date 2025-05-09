import flet as ft
from Pages.home import HomePage
from Pages.activities import ActivitiesPage
from Pages.focus import FocusPage
from Pages.skills import SkillsPage
from User.profile import ProfilePage
from Components.header import Header
from Components.nav import NavigationBar
from Engine.themes import ThemeFactory
from Engine.page import Page
from Engine.settings import Config as cogs

class Routes:
    def __init__(self, app, page, current_theme, header, navigation_bar):
        self.app = app
        self.page = page
        self.current_theme = current_theme
        self.header = header
        self.navigation_bar = navigation_bar

    def handle_route(self, route):
        if route == "/profile":
            from User.profile import ProfilePage
            return ft.View(
                route="/profile",
                controls=[
                    ProfilePage(self.page).build(),
                ],
            )
        elif route == "/activities":
            return ft.View(
                route="/activities",
                controls=[
                    ft.Column(
                        [
                            self.header.create_header(),
                            ft.Container(
                                content=ActivitiesPage(self.current_theme).build(),
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
                                content=FocusPage(self.current_theme).build(),
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
                                content=SkillsPage(self.current_theme).build(),
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
                                content=HomePage(self.page, self.navigation_bar.navigation_bar, self.current_theme).build(),
                                expand=True,
                            ),
                            self.navigation_bar.get_navigation_bar_container(),
                        ],
                        expand=True,
                    ),
                ],
            )

class PageBuilder:
    def __init__(self, app, page:ft.Page):
        self.app = app
        self.page = page
        super().__init__()
        self.current_theme = ThemeFactory.dark_theme()
        self.header = Header(app, self.current_theme)
        self.navigation_bar = NavigationBar(app, self.current_theme)
        self.routes = Routes(app, page, self.current_theme, self.header, self.navigation_bar)

    def toggle_theme(self):
        self.current_theme = (
            ThemeFactory.light_theme() if self.current_theme == ThemeFactory.dark_theme() else ThemeFactory.dark_theme()
        )
        self.apply_theme()

    def apply_theme(self):
        self.page.bgcolor = self.current_theme.bgcolor
        self.page.views.clear()
        self.page.views.append(self.build_page(self.page.route))
        self.page.update()

    def build_page(self, route):
        return self.routes.handle_route(route)