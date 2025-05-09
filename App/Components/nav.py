# Imports
import flet as ft
from Engine.themes import ThemeFactory
from Engine.settings import Config as cogs

class NavigationBar:
    def __init__(self, app, current_theme):
        self.app = app
        self.page = ft.Page
        self.current_theme = ThemeFactory.dark_theme() if current_theme == "dark" else ThemeFactory.light_theme()
        self.navigation_bar = None
        self.navigation_bar_container = None

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
            on_change=lambda e: self.log_and_navigate(e),  # Handle navigation with logging
        )

        self.navigation_bar_container = ft.Container(
            content=self.navigation_bar,
            bgcolor=self.current_theme.nav_bgcolor,  # Match the theme's navigation bar color
            padding=cogs.PAD_LR,
            border_radius=10
        )

    # Ensure the `navigate_to` method correctly updates the route
    def navigate_to(self, index):
        print(f"Selected index: {index}")  # Debugging statement to log the selected index
        if index == 0:
            self.page.go("/")
        elif index == 1:
            self.page.go("/activities")
        elif index == 2:
            self.page.go("/focus")
        elif index == 3:
            self.page.go("/skills")
        self.page.update()  # Ensure the page is updated after navigation

    def log_and_navigate(self, e):
        print(f"NavigationBar on_change triggered. New selected index: {e.control.selected_index}")
        self.navigate_to(e.control.selected_index)

    def get_navigation_bar_container(self):
        if not self.navigation_bar_container:
            self.setup_navigation_bar()
        return self.navigation_bar_container