# Imports
from Engine.page import Page
import flet as ft

class MomentumApp:
	def __init__(self):
		self.page = Page().get_page()  # Use Page class to initialize ft.Page

	def setup_page(self, page: ft.Page):
		self.page = Page(page).get_page()  # Use the existing page object from the Page class
		self.page.window.resizable = self.page.window.resizable  # Set resizable value dynamically from the page file

		# Add any additional app logic here

	def route_change(self, route):
		self.page.handle_route_change(route)  # Delegate route changes to the Page class

	def run(self, page: ft.Page):
		self.setup_page(page)  # Pass the page to setup_page
		self.page.on_route_change = self.route_change
		self.page.views.append(self.page.builder.build_page("/"))  # Use builder from Page class
		self.page.go(self.page.route)

if __name__ == "__main__":
	ft.app(target=MomentumApp().run)  # Correctly pass the run method to ft.app
