# filepath: flet-mobile-app/src/main.py
# Imports
import flet as ft
from components import *
from pages import *
from utils import *

def main(page: ft.Page):
    page.title = "Flet Mobile App"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Set up the main layout
    page.add(
        ft.AppBar(title=ft.Text("Welcome to Flet Mobile App")),
        ft.Column([
            ft.Text("This is the main page of the app."),
            ft.ElevatedButton("Go to Page 1", on_click=lambda e: page.go("/page1")),
            ft.ElevatedButton("Go to Page 2", on_click=lambda e: page.go("/page2")),
        ])
    )

    # Define navigation
    page.on_route_change = lambda e: page.go(e.route)

    # Add routes
    page.add_route("/page1", Page1)
    page.add_route("/page2", Page2)

if __name__ == "__main__":
    ft.app(target=main)