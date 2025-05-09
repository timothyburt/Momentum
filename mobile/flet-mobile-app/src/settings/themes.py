class Theme:
    def __init__(self, bgcolor, text_color, indicator_color, nav_bgcolor, accent_color):
        self.bgcolor = bgcolor
        self.text_color = text_color
        self.indicator_color = indicator_color
        self.nav_bgcolor = nav_bgcolor
        self.accent_color = accent_color  # Add accent color


# Light Theme
light_theme = Theme(
    bgcolor="#FFFFFF",  # White background
    text_color="#000000",  # Black text
    accent_color="#008000",  # Green accent color
    indicator_color="#000000",  # Black indicator
    nav_bgcolor="#000000",  #White BG
)

# Dark Theme
dark_theme = Theme(
    bgcolor="#121212",  # Dark background
    text_color="#FFFFFF",  # White text
    accent_color="#00FF00",  # Bright green accent color for dark theme
    indicator_color="#4D4D4D",  # Dark gray indicator
    nav_bgcolor="#1a1a1a",  # Dark navigation bar
)