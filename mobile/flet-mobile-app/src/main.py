# Imports
import flet as ft
from components import *
from pages import *
from utils import *


def main(page: ft.Page):
	page.title = "Activtity Planner App"
	page.vertical_alignment = ft.MainAxisAlignment.START

	# Create the avatar, username, and notification bell layout
	avatar = ft.CircleAvatar(
		foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
		content=ft.Text("U"),
		radius=30,
	)

	# Create a column to stack the username and byline
	username = ft.Text("Username", size=14, weight=ft.FontWeight.BOLD)
	byline = ft.Text("Byline", size=12, color=ft.Colors.GREY_400)
	user_info = ft.Column(
		[
			username,
			byline,
		],
		spacing=2,  # Adjust spacing between the texts
	)

	notification_bell = ft.Icon(ft.Icons.NOTIFICATIONS, size=30)

	# Create a row to align them horizontally
	header_row = ft.Row(
		[
			avatar,
			ft.Container(user_info, padding=ft.Padding(left=10, top=10, right=10, bottom=10)),
			ft.Container(notification_bell, alignment=ft.alignment.center_right, expand=True),
		],
		alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
		vertical_alignment=ft.CrossAxisAlignment.CENTER,
	)

	# Bottom navigation bar
	page.navigation_bar = ft.NavigationBar(
		destinations=[
			ft.NavigationBarDestination(
				icon=ft.Icons.HOME_FILLED, 
				label="Home"),
			ft.NavigationBarDestination(
				icon=ft.Icons.CALENDAR_MONTH_OUTLINED, 
				label="Activities"),
			ft.NavigationBarDestination(
				icon=ft.Icons.FITNESS_CENTER_ROUNDED,
				label="Workout"),
			ft.NavigationBarDestination(
    			icon=ft.Icons.BAR_CHART_ROUNDED,
				label="Skills",
			),
		]
	)


	# Add the header row to the page
	page.add(header_row)
	page.update()


if __name__ == "__main__":
	ft.app(target=main)