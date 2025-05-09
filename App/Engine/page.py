# Update Page to handle route changes and integrate with Builder
import flet as ft
from .settings import Config as cogs, Device as viewport
from .builder import Builder
from .routes import Routes, RouteHandler

class Page:
	def __init__(self, page: ft.Page):
		self.page = page
		self.page.title = cogs.APP_TITLE
		self.page.vertical_alignment = ft.MainAxisAlignment.START
		self.page.padding = cogs.APP_PADDING

		# Call the device check method directly
		device_dimensions = viewport.mobile()
		self.page.window.height = device_dimensions["app_height"]
		self.page.window.width = device_dimensions["app_width"]
		self.page.window.resizable = device_dimensions["app_resizable"]
		self.page.window.maximizable = device_dimensions["app_maximize"]

		self.builder = Builder(self.page)  # Integrate with Builder

	def get_page(self):
		return self.page

	def handle_route_change(self, route):
		RouteHandler.handle_route_change(self.page, self.builder, route)  # Delegate to Routes