import flet as ft
from Engine.themes import ThemeFactory
from Engine.page import Page
from Engine.builder import PageBuilder
from Engine.settings import Config as cogs

class MomentumApp:
    def __init__(self, page: ft.Page):
        self.page = page # Use Page class to initialize ft.Page
        self.current_theme = ThemeFactory.dark_theme()  # Use ThemeFactory for dark theme
        self.page_builder = PageBuilder(self)  # Use PageBuilder class

    def route_change(self, route):
        self.page.views.clear()
        self.page.views.append(self.page_builder.build_page(route))
        self.page.update()

    def run(self):
        self.page.on_route_change = self.route_change
        self.page.views.append(self.page_builder.build_page("/"))
        self.page_builder.apply_theme()
        self.page.go(self.page.route)


# Fix the TypeError by passing the required `page` argument to MomentumApp
def main():
    ft.app(target=lambda page: MomentumApp(page).run())  # Pass the `page` argument to MomentumApp


if __name__ == "__main__":
    main()
