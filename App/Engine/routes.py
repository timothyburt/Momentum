class Routes:
	HOME = "/"
	ACTIVITIES = "/activities"
	FOCUS = "/focus"
	SKILLS = "/skills"

class RouteHandler:
	def __init__(self, page, builder):
		self.page = page
		self.builder = builder

	def handle_route_change(self, route):
		"""Handles route changes dynamically using Builder."""
		self.page.views.clear()
		self.page.views.append(self.builder.build_page(route))
		self.page.update()