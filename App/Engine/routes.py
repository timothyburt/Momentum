# Imports
import flet as ft
from Engine.page import Page
from Pages.home import HomePage
from Pages.activities import ActivitiesPage
from Pages.focus import FocusPage
from Pages.skills import SkillsPage
from User.profile import ProfilePage
from Components.nav import NavigationBar
from Engine.themes import ThemeFactory

class Routes(Page):
    def __init__(self, page, current_theme=None):
        self.page = page
        self.current_theme = current_theme or ThemeFactory.dark_theme()
        self.navigation_bar = NavigationBar(page, "dark")  # or use self.current_theme if you want dynamic

    def path(self):
        context = {
            '/': ft.View(
                route='/',
                controls=[
                    HomePage(self.page).build()
                ]
            ),
            '/activities': ft.View(
                route='/activities',
                controls=[
                    ActivitiesPage(self.page).build()
                ]
            ),
            '/focus': ft.View(
                route='/focus',
                controls=[
                    FocusPage(self.page).build()
                ]
            ),
            '/skills': ft.View(
                route='/skills',
                controls=[
                    SkillsPage(self.page).build()
                ]
            ),
            '/profile': ft.View(
                route='/profile',
                controls=[
                    ProfilePage(self.page).build()
                ]
            ),
        }
        return context