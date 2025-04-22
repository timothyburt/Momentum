import flet as ft

def header_row():
    # Create the avatar, username, and notification bell layout
    avatar = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=ft.Text("U"),
        radius=30,
        width=40,
        height=40,
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

    notification_bell = ft.Icon(
        ft.Icons.NOTIFICATIONS,
        size=30,
        color=ft.Colors.WHITE,
        badge=ft.Badge(small_size=10, bgcolor=ft.Colors.GREEN),
    )

    # Wrap the header row in a container with padding
    return ft.Container(
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