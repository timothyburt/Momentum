# Imports
import flet as ft
from components import *
from pages import *
from utils import *


def main(page: ft.Page):
	page.title = "Activtity Planner App"
	page.vertical_alignment = ft.MainAxisAlignment.START
	page.bgcolor = "#0d0d0d"
	page.adaptive = True
	page.padding = 0
	page.window.height = 700
	page.window.width = 350
	page.window.resizable = False

	# Create the avatar, username, and notification bell layout
	avatar = ft.CircleAvatar(
		foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
		content=ft.Text("U"),
		radius=30,
		width = 40,
		height = 40
	)

	# Create a column to stack the username and byline
	username = ft.Text(
		"Blabber Fatmouth".upper(),
		size=12,
		weight=ft.FontWeight.BOLD,
		color=ft.Colors.GREEN,
	)
	title = ft.Text("Novice", size=10, color=ft.Colors.GREY_400)
	user_info = ft.Column(
		[
			username,
			title,
		],
		spacing=2,  # Adjust spacing between the texts
	)

	notification_bell = ft.Icon(ft.Icons.NOTIFICATIONS, size=30, color=ft.Colors.WHITE, badge=ft.Badge(small_size=10, bgcolor=ft.Colors.GREEN))

	# Wrap the header row in a container with padding
	header_row = ft.Container(
		content=ft.Row(
			[
				avatar,
				ft.Container(user_info, padding=2.5),
				ft.Container(notification_bell, alignment=ft.alignment.center_right, expand=True),
			],
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			vertical_alignment=ft.CrossAxisAlignment.CENTER,
		),
		padding=10,  # Add 10 padding around the header row
	)

	# Create a search bar
	search_bar = ft.Container(
		content=ft.TextField(
			hint_text="Search Goals, Tasks, Workouts, etc",
			suffix_icon=ft.Icons.SEARCH,
			focused_border_color=ft.Colors.GREEN,
			bgcolor=ft.Colors.GREY_900,
			cursor_color=ft.Colors.WHITE,
			color=ft.Colors.WHITE,
			height=30,
			text_size=10,
			border_radius=10,
		),
		padding=ft.padding.only(left=25, right=25, bottom=20),
	)

	# Daily Progress Overview
	daily_overview = ft.Container(
		content=ft.Column(
			[
				ft.Row(
					[
						ft.Text(
							"Daily Progress",
							weight=ft.FontWeight.BOLD,
							color=ft.Colors.WHITE,
							size=14,
							),
					],
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Space between text and progress bar
				),
				ft.Row(
					[
						# Stats Column
						ft.Column(
							[
								ft.Text("Tasks", color=ft.Colors.GREY_400, size=10),
								ft.Text("50%", weight=ft.FontWeight.BOLD, size=8, color=ft.Colors.GREEN),
								ft.Text("Goals", color=ft.Colors.GREY_400, size=10),
								ft.Text("15%", weight=ft.FontWeight.BOLD, size=8, color=ft.Colors.BLUE),
								ft.Text("Levels", color=ft.Colors.GREY_400, size=10),
								ft.Text("5%", weight=ft.FontWeight.BOLD, size=8, color=ft.Colors.RED),
							],
							alignment=ft.MainAxisAlignment.START,
							spacing=5,
						),
						# Bar Graph Column with Percentage Text
						ft.Column(
							[
								# First ProgressBar
								ft.ProgressBar(
									value=0.5,  # Set progress value (50%)
									bgcolor=ft.Colors.GREY_800,  # Background color of the progress bar
									color=ft.Colors.GREEN,  # Progress color
									height=10,  # Height of the progress bar
									width=150,  # Width of the progress bar
									border_radius=10,
								),
								# Second ProgressBar
								ft.ProgressBar(
									value=0.4,  # Set progress value (40%)
									bgcolor=ft.Colors.GREY_800,  # Background color of the progress bar
									color=ft.Colors.BLUE,  # Progress color
									height=10,  # Height of the progress bar
									width=150,  # Width of the progress bar
									border_radius=10,
								),
								# Third ProgressBar
								ft.ProgressBar(
									value=0.1,  # Set progress value (10%)
									bgcolor=ft.Colors.GREY_800,  # Background color of the progress bar
									color=ft.Colors.RED,  # Progress color
									height=10,  # Height of the progress bar
									width=150,  # Width of the progress bar
									border_radius=10,
								),
							],
							alignment=ft.MainAxisAlignment.START,
							spacing=20,
						),
					],
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
				),
			],
			alignment=ft.MainAxisAlignment.CENTER,
			spacing=10,
		),
		bgcolor=ft.Colors.GREY_900,
		border_radius=10,
		height=150,
		padding=10,
	)

	# Skills Carousel
	skills_section = ft.Container(
		content=ft.Column(
			[
				ft.Row(
					controls=[
						ft.Text(
							"Popular Skills",
							weight=ft.FontWeight.BOLD,
							color=ft.Colors.WHITE,
							size=14,
						),
						ft.TextButton(
							"View All",
							on_click=lambda e: print("View All clicked"),  # Add your action here
							style=ft.ButtonStyle(
								color=ft.Colors.GREEN,
								padding=ft.padding.only(left=10, right=10),
								text_style=ft.TextStyle(size=10),  # Make the text smaller
							),
						),
					],
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Align "Popular Skills" and "View All"
				),
				ft.Row(
					controls=[
						ft.Container(  # Add padding to the first image
							content=ft.Stack(
								[
									# Image
									ft.Image(
										src=f"https://picsum.photos/200/200?0",
										width=100,
										height=75,
										fit=ft.ImageFit.COVER,
										repeat=ft.ImageRepeat.NO_REPEAT,
										border_radius=ft.border_radius.all(10),
									),
									# Semi-transparent overlay
									ft.Container(
										bgcolor=ft.Colors.BLACK,
										opacity=.40,  # Set transparency
										border_radius=ft.border_radius.all(10),
										expand=True,  # Cover the entire image
									),
									# Text (Skill Name and Stat)
									ft.Container(
										content=ft.Column(
											[
												ft.Text(
													"Wellness",
													size=12,
													weight=ft.FontWeight.BOLD,
													color=ft.Colors.WHITE,
													text_align=ft.TextAlign.LEFT,
												),
												ft.Text(
													"50% Complete",
													size=10,
													color=ft.Colors.GREEN,
													text_align=ft.TextAlign.LEFT,
												),
											],
											spacing=2,
										),
										alignment=ft.alignment.bottom_left,  # Align text to bottom-left
										padding=ft.padding.only(left=3, bottom=5),  # Add padding for spacing
									),
								]
								),
								padding=ft.padding.only(left=25),  # Padding on the left
						),
						*[
							ft.Stack(
								[
									# Image
									ft.Image(
										src=f"https://picsum.photos/200/200?{i}",
										width=100,
										height=75,
										fit=ft.ImageFit.COVER,
										repeat=ft.ImageRepeat.NO_REPEAT,
										border_radius=ft.border_radius.all(10),
									),
									# Semi-transparent overlay
									ft.Container(
										bgcolor=ft.Colors.BLACK,
										opacity=.40,  # Set transparency
										border_radius=ft.border_radius.all(10),
										expand=True,  # Cover the entire image
									),
									# Text (Skill Name and Stat)
									ft.Container(
										content=ft.Column(
											[
												ft.Text(
													f"Skill {i + 1}",
													size=12,
													weight=ft.FontWeight.BOLD,
													color=ft.Colors.WHITE,
													text_align=ft.TextAlign.LEFT,
												),
												ft.Text(
													f"{(i + 1) * 20}% Complete",
													size=10,
													color=ft.Colors.GREEN,
													text_align=ft.TextAlign.LEFT,
												),
											],
											spacing=2,
										),
										alignment=ft.alignment.bottom_left,  # Align text to bottom-left
										padding=ft.padding.only(left=3, bottom=5),  # Add padding for spacing
									),
								]
							)
							for i in range(1, 3)
						],
					],
					alignment=ft.MainAxisAlignment.CENTER,  # Center the images
					expand=1,
					wrap=False,
					scroll="always",
				),
			],
			spacing=10,  # Space between the text and the carousel
			alignment=ft.MainAxisAlignment.CENTER,
		),
		padding=ft.padding.only(left=25, right=25),  # Add padding around the skills section
	)

	# Recommended Tasks to Focus on
	recommended_tasks = ft.Container(
		content=ft.Column(
			[
				ft.Text(
					"Recommended Tasks",
					weight=ft.FontWeight.BOLD,
					color=ft.Colors.WHITE,
					size=14,
				),
				ft.Column(
					[
						ft.Container(
							content=ft.Row(
								[
									ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, color=ft.Colors.GREEN, size=20),
									ft.Text(
										"Complete 5 tasks today",
										color=ft.Colors.WHITE,
										size=12,
									),
								],
								alignment=ft.MainAxisAlignment.START,
							),
							padding=ft.padding.all(10),
							bgcolor=ft.Colors.GREY_900,
							border_radius=ft.border_radius.all(10),
						),
						ft.Container(
							content=ft.Row(
								[
									ft.Icon(ft.Icons.FITNESS_CENTER, color=ft.Colors.BLUE, size=20),
									ft.Text(
										"Do a 30-minute workout",
										color=ft.Colors.WHITE,
										size=12,
									),
								],
								alignment=ft.MainAxisAlignment.START,
							),
							padding=ft.padding.all(10),
							bgcolor=ft.Colors.GREY_900,
							border_radius=ft.border_radius.all(10),
						),
						ft.Container(
							content=ft.Row(
								[
									ft.Icon(ft.Icons.BOOKMARK_OUTLINE, color=ft.Colors.YELLOW, size=20),
									ft.Text(
										"Read 10 pages of a book",
										color=ft.Colors.WHITE,
										size=12,
									),
								],
								alignment=ft.MainAxisAlignment.START,
							),
							padding=ft.padding.all(10),
							bgcolor=ft.Colors.GREY_900,
							border_radius=ft.border_radius.all(10),
						),
					],
					spacing=10,  # Space between tasks
				),
			],
			spacing=10,  # Space between the title and the list
		),
		padding=ft.padding.only(left=25, right=25, top=20),  # Add padding around the section
	)

	# Bottom navigation bar with rounded corners and gradient
	navigation_bar = ft.Container(
		content=ft.NavigationBar(
			bgcolor="#0d0d0d",
			indicator_color=ft.Colors.GREY_900,
			destinations=[
				ft.NavigationBarDestination(
					icon=ft.Icons.HOME_ROUNDED,
					label="Home"
				),
				ft.NavigationBarDestination(
					icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
					label="Activities"
				),
				ft.NavigationBarDestination(
					icon=ft.Icons.FITNESS_CENTER_ROUNDED,
					label="Workout"
				),
				ft.NavigationBarDestination(
					icon=ft.Icons.BAR_CHART_ROUNDED,
					label="Skills"
				),
			]
		),
		height=60,
		border_radius=ft.border_radius.only(top_left=20, top_right=20),
	)

	# Add the header row, search bar, daily overview, skills section, recommended tasks, and navigation bar to the page
	page.add(
		ft.Column(
			[
				ft.Container(
					content=ft.Column(
						[
							header_row,
							search_bar,
							ft.Container(
								daily_overview,
								padding=ft.padding.only(left=25, right=25),  # Same padding as the search bar
							),
							skills_section,  # Add the skills section here
							recommended_tasks,  # Add the recommended tasks section here
						],
						spacing=10,  # Space between sections
						alignment=ft.MainAxisAlignment.START,
						scroll=ft.ScrollMode.AUTO,
					),
					expand=True,  # Allow the scrollable container to take up available space
				),
				ft.Container(
					navigation_bar,
					alignment=ft.alignment.bottom_center,  # Fix the navigation bar at the bottom
				),
			],
			expand=True,  # Make the column take up the full height of the page
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # Ensure proper spacing between content and nav bar
		)
	)
	page.update()


if __name__ == "__main__":
	ft.app(target=main)