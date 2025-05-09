# Imports
import flet as ft
from Engine.themes import ThemeFactory  # Updated path
from Engine.settings import Config as cogs  # Use alias cogs
from Engine.page import Page
from Engine.builder import PageBuilder

class NavigationBar:
    def __init__(self, app):
        self.app = app
        self.page = Page().get_page()  # Use Page class to initialize ft.Page
        self.current_theme = PageBuilder(app).current_theme  # Get current theme from PageBuilder
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
            on_change=lambda e: self.navigate_to(e.control.selected_index),  # Handle navigation
        )

        self.navigation_bar_container = ft.Container(
            content=self.navigation_bar,
            bgcolor=self.current_theme.nav_bgcolor  # Match the theme's navigation bar color
        )

    def navigate_to(self, index):
        if index == 0:
            self.page.go("/")
        elif index == 1:
            self.page.go("/activities")
        elif index == 2:
            self.page.go("/focus")
        elif index == 3:
            self.page.go("/skills")

    def get_navigation_bar_container(self):
        if not self.navigation_bar_container:
            self.setup_navigation_bar()
        return self.navigation_bar_container