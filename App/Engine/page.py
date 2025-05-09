# Imports
import flet as ft
from .settings import Config as cogs, Device as viewport

# Fix the Page class to correctly use an ft.Page object
class Page:
	def __init__(self, page: ft.Page):
		self.page = page  # Use the existing ft.Page object passed as an argument
		self.page.title = cogs.APP_TITLE
		self.page.vertical_alignment = ft.MainAxisAlignment.START
		self.page.padding = cogs.APP_PADDING
		
		# Call the device check method directly
		device_dimensions = viewport.mobile()
		self.page.window.height = device_dimensions["app_height"]
		self.page.window.width = device_dimensions["app_width"]
		self.page.window.resizable = device_dimensions["app_resizable"]
		self.page.window.maximizable = device_dimensions.get("app_maximize", True)

	def get_page(self):
		return self.page
