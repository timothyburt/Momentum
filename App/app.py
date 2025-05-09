# Imports
from Engine.page import Page
import flet as ft

class MomentumApp:
	def __init__(self):
		self.page = None  # Initialize page as None

	def setup_page(self, page: ft.Page):
		self.page = Page(page).get_page()  # Pass the `page` argument to the Page class
		self.page.window.resizable = self.page.window.resizable  # Set resizable value dynamically from the page file
		self.page.window.maximizable = self.page.window.maximizable

		# Add any additional app logic here

	def route_change(self, route):
		self.page.handle_route_change(route)  # Page handles route changes using Routes

	def run(self, page: ft.Page):
		self.setup_page(page)  # Pass the page to setup_page
		self.page.on_route_change = self.route_change
		self.page.go(self.page.route)

if __name__ == "__main__":
	ft.app(target=MomentumApp().run)  # Correctly pass the run method to ft.app
