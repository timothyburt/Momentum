import flet as ft

def activities_page():
	return ft.Container(
		content=ft.Column(
			[
				ft.Text("Activities Page", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
				ft.Text("This is the Activities page of the app.", size=16, color=ft.Colors.GREY_400),
			],
			alignment=ft.MainAxisAlignment.CENTER,
			spacing=10,
		),
		alignment=ft.alignment.center,
		expand=True,
	)