# Create the Builder class to assist with dynamic Page construction
from .routes import Routes

class Builder:
	def __init__(self, page):
		self.page = page

	def build_page(self, route):
		"""Constructs a page dynamically based on the route."""
		if route == Routes.HOME:
			return self._build_home_page()
		elif route == Routes.ACTIVITIES:
			return self._build_activities_page()
		elif route == Routes.FOCUS:
			return self._build_focus_page()
		elif route == Routes.SKILLS:
			return self._build_skills_page()
		else:
			raise ValueError(f"Unknown route: {route}")

	def _build_home_page(self):
		# Logic to construct the Home page
		return "Home Page Content"

	def _build_activities_page(self):
		# Logic to construct the Activities page
		return "Activities Page Content"

	def _build_focus_page(self):
		# Logic to construct the Focus page
		return "Focus Page Content"

	def _build_skills_page(self):
		# Logic to construct the Skills page
		return "Skills Page Content"