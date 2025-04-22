class Theme:
    def __init__(self, bgcolor, text_color, indicator_color, nav_bgcolor):
        self.bgcolor = bgcolor
        self.text_color = text_color
        self.indicator_color = indicator_color
        self.nav_bgcolor = nav_bgcolor


# Light Theme
light_theme = Theme(
    bgcolor="#FFFFFF",  # White background
    text_color="#000000",  # Black text
    indicator_color="#000000",  # Black indicator
    nav_bgcolor="#F0F0F0",  # Light gray navigation bar
)

# Dark Theme
dark_theme = Theme(
    bgcolor="#121212",  # Dark background
    text_color="#FFFFFF",  # White text
    indicator_color="#4D4D4D",  # White indicator
    nav_bgcolor="#1a1a1a",  # Dark navigation bar
)