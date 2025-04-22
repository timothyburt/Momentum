import flet as ft
from pages.home import home_page
from pages.activities import activities_page
from pages.focus import focus_page
from pages.skills import skills_page
from settings.themes import light_theme, dark_theme
from components.header import header_row  # Import the header row

def main(page: ft.Page):
    # Set default theme to dark
    current_theme = dark_theme

    # Function to toggle themes
    def toggle_theme():
        nonlocal current_theme
        current_theme = light_theme if current_theme == dark_theme else dark_theme
        apply_theme()

    # Function to apply the current theme
    def apply_theme():
        page.bgcolor = current_theme.bgcolor
        navigation_bar.bgcolor = current_theme.nav_bgcolor
        navigation_bar.indicator_color = current_theme.indicator_color
        page.update()

    page.title = "Activity Planner App"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 0
    page.window.height = 700
    page.window.width = 350
    page.window.resizable = False

    # Bottom navigation bar
    navigation_bar = ft.NavigationBar(
        bgcolor=current_theme.nav_bgcolor,
        indicator_color=current_theme.indicator_color,
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
                                header_row(),  # Add the header row
                                ft.Container(
                                    content=activities_page(),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                    transition=ft.PageTransitionTheme.OPEN_UPWARDS,  # Set transition to fade
                )
            )
        elif page.route == "/focus":
            page.views.append(
                ft.View(
                    route="/focus",
                    controls=[
                        ft.Column(
                            [
                                header_row(),  # Add the header row
                                ft.Container(
                                    content=focus_page(),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                    transition=ft.PageTransitionTheme.OPEN_UPWARDS,  # Set transition to fade
                )
            )
        elif page.route == "/skills":
            page.views.append(
                ft.View(
                    route="/skills",
                    controls=[
                        ft.Column(
                            [
                                header_row(),  # Add the header row
                                ft.Container(
                                    content=skills_page(),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                    transition=ft.PageTransitionTheme.OPEN_UPWARDS,  # Set transition to fade
                )
            )
        else:
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Column(
                            [
                                header_row(),  # Add the header row
                                ft.Container(
                                    content=home_page(page, navigation_bar),
                                    expand=True,  # Make the content scrollable
                                ),
                                ft.Container(
                                    content=navigation_bar,
                                    alignment=ft.alignment.bottom_center,
                                ),
                            ],
                            expand=True,  # Ensure the column takes up the full height
                        ),
                    ],
                    transition=ft.PageTransitionTheme.OPEN_UPWARDS,  # Set transition to fade
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

    # Add a toggle theme button
    toggle_theme_button = ft.FloatingActionButton(
        icon=ft.Icons.LIGHT_MODE if current_theme == dark_theme else ft.Icons.DARK_MODE,
        on_click=lambda _: toggle_theme(),
    )

    # Set up routing
    page.on_route_change = route_change
    page.views.append(
        ft.View(
            route="/",
            controls=[
                ft.Column(
                    [
                        header_row(),  # Add the header row
                        ft.Container(
                            content=home_page(page, navigation_bar),
                            expand=True,  # Make the content scrollable
                        ),
                        ft.Container(
                            content=navigation_bar,
                            alignment=ft.alignment.bottom_center,
                        ),
                    ],
                    expand=True,  # Ensure the column takes up the full height
                ),
                toggle_theme_button,  # Add the toggle theme button
            ],
            transition=ft.PageTransitionTheme.OPEN_UPWARDS,  # Set transition to fade
        )
    )
    apply_theme()  # Apply the initial theme
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)
