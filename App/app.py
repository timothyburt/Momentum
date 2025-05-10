# Imports
import flet as ft
from Engine.themes import ThemeFactory
from Components.header import Header
from Components.nav import NavigationBar
from Engine.page import Page

class MomentumApp(Page):
    def __init__(self, page):
        self.page = page
        self.build(self.page)
        self.current_theme = ThemeFactory.dark_theme()
        self.header = Header(self, self.current_theme)
        self.navigation_bar = NavigationBar(self, self.current_theme)
        # This will hold the dynamic page content
        self.content_container = ft.Container(expand=True)

    def route_change(self, route):
        # Get the content control for the current route
        context = self.get_content_for_route(self.page.route)
        self.content_container.content = context
        self.page.update()

    def get_content_for_route(self, route):
        if route == "/activities":
            from Pages.activities import ActivitiesPage
            return ActivitiesPage(self.page).build()
        elif route == "/focus":
            from Pages.focus import FocusPage
            return FocusPage(self.page).build()
        elif route == "/skills":
            from Pages.skills import SkillsPage
            return SkillsPage(self.page).build()
        elif route == "/profile":
            from User.profile import ProfilePage
            return ProfilePage(self.page).build()
        else:
            from Pages.home import HomePage
            return HomePage(self.page, self.navigation_bar.navigation_bar, self.current_theme).build()

    def run(self):
        self.page.on_route_change = self.route_change
        # Build the persistent layout
        self.page.add(
            ft.Column(
                [
                    self.header.create_header(),
                    self.content_container,
                    self.navigation_bar.get_navigation_bar_container(),
                ],
                expand=True,
            )
        )
        # Set initial content
        self.route_change(self.page.route)
        self.page.go('/')

def main():
    ft.app(target=lambda page: MomentumApp(page).run())

if __name__ == "__main__":
    main()
