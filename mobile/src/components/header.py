import flet as ft
from settings.themes import light_theme, dark_theme

def header_row(page: ft.Page, toggle_theme, current_theme):
	# Define the popup menu items
	popup_menu = ft.PopupMenuButton(
		content=ft.CircleAvatar(  # Use content instead of icon
			foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
			content=ft.Text("U"),

			radius=30,
			width=40,
			height=40,
		),
		items=[
			ft.PopupMenuItem(
				text="View Profile",
				on_click=lambda e: view_profile(page),
			),
			ft.PopupMenuItem(
				text="Settings",
				on_click=lambda e: open_settings(page),
			),
			ft.PopupMenuItem(
				text="Light Theme" if current_theme == dark_theme else "Dark Theme",
				icon=ft.Icons.LIGHT_MODE if current_theme == dark_theme else ft.Icons.DARK_MODE,  # Add dynamic icon
				on_click=lambda e: toggle_theme(),
			),
			ft.PopupMenuItem(
				text="Logout",
				on_click=lambda e: logout(page),
			),
		],
	)

	# Function to handle "View Profile" action
	def view_profile(page):
		page.snack_bar = ft.SnackBar(ft.Text("Viewing Profile"))
		page.snack_bar.open()
		page.update()

	# Function to handle "Settings" action
	def open_settings(page):
		page.snack_bar = ft.SnackBar(ft.Text("Opening Settings"))
		page.snack_bar.open()
		page.update()

	# Function to handle "Logout" action
	def logout(page):
		page.snack_bar = ft.SnackBar(ft.Text("Logging Out"))
		page.snack_bar.open()
		page.update()

	# Create a column to stack the username and byline
	username = ft.Text(
		"Blabber Fatmouth".upper(),
		size=12,
		weight=ft.FontWeight.BOLD,
		color=current_theme.accent_color,  # Dynamic text color
	)
	title = ft.Text("Novice", size=10, color=current_theme.text_color)  # Dynamic text color
	user_info = ft.Column(
		[
			username,
			title,
		],
		spacing=2,  # Adjust spacing between the texts
	)

	notification_bell = ft.Icon(
		ft.Icons.NOTIFICATIONS,
		size=30,
		color=current_theme.text_color,  # Dynamic icon color
		badge=ft.Badge(small_size=10, bgcolor=ft.Colors.GREEN),
	)

	# Wrap the header row in a container with padding
	return ft.Container(
		content=ft.Row(
			[
				popup_menu,  # Use the popup menu with the Circle Avatar as the content
				ft.Container(user_info, padding=2.5),
				ft.Container(notification_bell, alignment=ft.alignment.center_right, expand=True),
			],
			alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
			vertical_alignment=ft.CrossAxisAlignment.CENTER,
		),
		padding=10,  # Add 10 padding around the header row
	)