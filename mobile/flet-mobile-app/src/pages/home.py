import flet as ft

def home_page(page: ft.Page, navigation_bar):

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
									height=10,
									width=150,
									border_radius=10,
								),
								# Second ProgressBar
								ft.ProgressBar(
									value=0.4,  # Set progress value (40%)
									bgcolor=ft.Colors.GREY_800,
									color=ft.Colors.BLUE,
									height=10,
									width=150,
									border_radius=10,
								),
								# Third ProgressBar
								ft.ProgressBar(
									value=0.1,  # Set progress value (10%)
									bgcolor=ft.Colors.GREY_800,
									color=ft.Colors.RED,
									height=10,
									width=150,
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
							on_click=lambda e: [
								setattr(navigation_bar, "selected_index", 3),  # Update the selected index to Skills
								page.go("/skills"),  # Navigate to the Skills page
							],
							style=ft.ButtonStyle(
								color=ft.Colors.GREEN,
								padding=ft.padding.only(left=10, right=10),
								text_style=ft.TextStyle(size=10),
							),
						),
					],
					alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
				),
				ft.Row(
					controls=[
						ft.Container(
							content=ft.Image(
								src=f"https://picsum.photos/200/200?0",
								width=100,
								height=75,
								fit=ft.ImageFit.COVER,
								border_radius=ft.border_radius.all(10),
							),
							padding=ft.padding.only(left=25),
						),
						*[
							ft.Image(
								src=f"https://picsum.photos/200/200?{i}",
								width=100,
								height=75,
								fit=ft.ImageFit.COVER,
								border_radius=ft.border_radius.all(10),
							)
							for i in range(1, 5)  # Add more images for scrolling
						],
					],
					alignment=ft.MainAxisAlignment.START,
					scroll="always",  # Enable horizontal scrolling
				),
			],
			spacing=10,
		),
		padding=ft.padding.only(left=25, right=25),
	)

	# Recommended Tasks
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
					spacing=10,
				),
			],
			spacing=10,
		),
		padding=ft.padding.only(left=25, right=25, top=20),
	)

	# Combine all sections into the home page layout
	return ft.Column(
		[
			search_bar,
			ft.Container(
				daily_overview,
				padding=ft.padding.only(left=25, right=25),
			),
			skills_section,
			recommended_tasks,
		],
		spacing=10,
		alignment=ft.MainAxisAlignment.START,
		scroll=ft.ScrollMode.AUTO,
	)