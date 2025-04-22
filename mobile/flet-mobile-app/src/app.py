import flet as ft
from pages.home import home_page
from pages.activities import activities_page
from pages.focus import focus_page
from pages.skills import skills_page

def main(page: ft.Page):
    page.title = "Activity Planner App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = "#1a1a1a"
    page.adaptive = True
    page.padding = 0
    page.window.height = 700
    page.window.width = 350
    page.window.resizable = False

    # Function to handle route changes
    def route_change(route):
        page.views.clear()
        if page.route == "/activities":
            page.views.append(
                ft.View(
                    route="/activities",
                    controls=[
                        ft.Column(
                            [
                                ft.Container(
                                    content=activities_page(),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,  # Removed padding
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                )
            )
        elif page.route == "/focus":
            page.views.append(
                ft.View(
                    route="/focus",
                    controls=[
                        ft.Column(
                            [
                                ft.Container(
                                    content=focus_page(),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,  # Removed padding
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                )
            )
        elif page.route == "/skills":
            page.views.append(
                ft.View(
                    route="/skills",
                    controls=[
                        ft.Column(
                            [
                                ft.Container(
                                    content=skills_page(),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,  # Removed padding
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                )
            )
        else:
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Column(
                            [
                                ft.Container(
                                    content=home_page(page, navigation_bar),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,  # Removed padding
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                )
            )
        page.update()

    # Function to navigate between pages
    def navigate_to(index):
        if index == 0:
            page.go("/")
        elif index == 1:
            page.go("/activities")
        elif index == 2:
            page.go("/focus")
        elif index == 3:
            page.go("/skills")

    # Bottom navigation bar
    navigation_bar = ft.NavigationBar(
        bgcolor="#1a1a1a",
        indicator_color=ft.Colors.GREY_900,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_ROUNDED,
                label="Home",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
                label="Activities",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.TIMER,
                label="Focus",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BAR_CHART_ROUNDED,
                label="Skills",
            ),
        ],
        selected_index=0,  # Default to the first tab
        on_change=lambda e: navigate_to(e.control.selected_index),  # Handle navigation
    )

    # Set up routing
    page.on_route_change = route_change
    page.views.append(
        ft.View(
            route="/",
            controls=[
                ft.Column(
                    [
                        ft.Container(
                            content=home_page(page, navigation_bar),
                            expand=True,  # Make the content scrollable
                        ),
                        ft.Container(
                            content=navigation_bar,  # Removed padding
                            alignment=ft.alignment.bottom_center,
                        ),
                    ],
                    expand=True,  # Ensure the column takes up the full height
                ),
            ],
        )
    )
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
