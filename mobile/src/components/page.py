import flet as ft

class Page:
    def __init__(self):
        self.page = ft.Page()
        self.page.title = "Momentum App"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.padding = 0
        self.page.window.height = 700
        self.page.window.width = 350
        self.page.window.resizable = False

    def get_page(self):
        return self.page
