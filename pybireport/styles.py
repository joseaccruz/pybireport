
class Style:
    def __init__(self, name, prop={}):
        self.name = name
        self.prop = prop

    def format(self, value):
        if type(value) is str:
            self.name = value
        elif type(value) is dict:
            self.prop = value

#
# Styles
#
class StyleSheet:
    def __init__(self):
        self._styles = {}

    def inherit(self, parent, child):
        return {**self._styles.get(parent, {}), **child}

    def get(self, style):
        return {**self._styles.get(style.name, {}), **style.prop}

#
# An opinionated DefaultStyle
#
class DefaultStyleSheet(StyleSheet):
    def __init__(self):
        super().__init__()

        self._styles = {}

        self._styles["base"] = {
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
        }

        self._styles["text"] = self.inherit("base", {
            "font_size": 11
        })

        self._styles["title"] = self.inherit("text", {
            "font_size": 18,
            "font_color": "#FFFFFF",
            "bold": True,
            "align": "center",
            "bg_color": "#003300"
        })

        self._styles["legend"] = self.inherit("text", {
            "font_size": 9
        })

        self._styles["table_title"] = self.inherit("text", {
            "font_size": 16,
            "bold": True,
            "align": "center"
        })

        self._styles["table_cell"] = self.inherit("base", {
            "border_color": "#000000",
        })

        self._styles["table_header"] = self.inherit("table_cell", {
            "font_size": 12,
            "bold": True,
            "align": "center",
            "bg_color": "#808080"
        })

        self._styles["table_row"] = self.inherit("table_cell", {
            "font_size": 11,
            "align": "center"
        })

        self._styles["table_row_odd"] = self.inherit("table_row", {})

        self._styles["table_row_even"] = self.inherit("table_row", {
            "bg_color": "#F0F0F0"
        })

#
# Alternate style just to show how to do it
#
class AlternateStyleSheet(DefaultStyleSheet):
    def __init__(self):
        super().__init__()

        self._styles["title"] = self.inherit("title", {
            "font_size": 16
        })



