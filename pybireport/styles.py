#
# Styles
#
class Style:
    def __init__(self):
        self.base = {}

#
# An opinionated DefaultStyle
#
class DefaultStyle(Style):
    def __init__(self):
        super().__init__()

        self.base = {**self.base, **{
            "font_name": "Arial",
            "font_size": 11,
            "font_color": "#000000",
            "bold": False,
            "italic": False,
            "underline": False,
            "font_strikeout": False,

            "align": "left",                 # "center", "right", "fill", "justify", "center_across", "distributed"
            "valign": "vcenter",             # "top", "bottom", "vjustify", "vdistributed"
            "rotation": 0,
            "text_wrap": False,
            "shrink": False,

            "pattern": 1,
            "bg_color": "#FFFFFF",

            "border": 1,
            # "bottom": 1,
            # "top": 1,
            # "left": 1,
            # "right": 1,
            "border_color": "#cccccc",
            #"bottom_color": "#000000",
            #"top_color": "#000000",
            #"left_color": "#000000",
            #"right_color": "#000000"

            "num_format": "General"
        }}

        self.text = {**self.base, **{
            "font_size": 11
        }}

        self.title = {**self.text, **{
            "font_size": 18,
            "font_color": "#FFFFFF",
            "bold": True,
            "align": "center",
            "bg_color": "#003300"
        }}

        self.legend = {**self.text, **{
            "font_size": 9
        }}

        self.table_title = {**self.base, **{
            "font_size": 16,
            "bold": True,
            "align": "center"
        }}

        self.table_data = {**self.base, **{
            "border_color": "#000000",
        }}

        self.table_header = {**self.table_data, **{
            "font_size": 12,
            "bold": True,
            "align": "center",
            "bg_color": "#808080"
        }}

        self.table_row = {**self.table_data, **{
            "font_size": 11,
            "align": "center"
        }}

        self.table_row_odd = {**self.table_row, **{}}

        self.table_row_even = {**self.table_row, **{
            "bg_color": "#F0F0F0"
        }}

#
# Alternate style just to show how to do it
#
class AlternateStyle(Style):
    def __init__(self):
        super().__init__()

        self._title = {**self._title, **{
            "font_size": 16
        }}



