# Imports
import flet as ft
from Settings.config import Config as cogs

class Page:
    def __init__(self):
        self.page = ft.Page()
        self.page.title = "Momentum App"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.padding = 0
        self.page.window.height = cogs.APP_HEIGHT  # Use alias cogs for height
        self.page.window.width = cogs.APP_WIDTH  # Use alias cogs for width
        self.page.window.resizable = False

    def get_page(self):
        return self.page
