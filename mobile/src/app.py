import flet as ft
from App.Engine.themes import ThemeFactory
from components.page import Page
from App.Engine.builder import PageBuilder
from Settings.config import Config as cogs  # Use alias cogs

class MomentumApp:
    def __init__(self):
        self.page = Page().get_page()  # Use Page class to initialize ft.Page
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


def main():
    app = MomentumApp()
    ft.app(target=app.run)


if __name__ == "__main__":
    main()
