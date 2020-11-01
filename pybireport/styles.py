import copy

#
# Styles
#
def new_style(default, props):
    style = copy.copy(default)

    for k, v in props.items():
        style[k] = v

    return style


style_default = {
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

	"border": 0,
	"bottom": 0,
	"top": 0,
	"left": 0,
	"right": 0,
	"border_color": "#000000",
	"bottom_color": "#000000",
	"top_color": "#000000",
	"left_color": "#000000",
	"right_color": "#000000",
	"num_format": "General"
}


style_title = new_style(style_default, {
	"font_size": 18,
	"font_color": "#FFFFFF",
	"bold": True,
	"align": "center",
	"bg_color": "003300"
})


