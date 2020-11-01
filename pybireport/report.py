import xlsxwriter

import copy




class Report:
    def __init__(self, fname):
        self._fname = fname
        self._pages = []

    def add_page(self, page):
        # TBD: check if a page w/ the same name exists
        self._pages.append(page)

        return page

    def generate(self):
        # Create a workbook and add a worksheet.
        wb = xlsxwriter.Workbook(self._fname)

        for page in self._pages:
            page.generate(wb)

        wb.close()


class Page:
    def __init__(self, name):
        self._name = name
        self._vizs = []

    def add(self, viz):
        self._vizs.append(viz)

        return viz

    def generate(self, wb):
        ws = wb.add_worksheet(self._name)

        for viz in self._vizs:
            viz._generated = False
        
        for (i, viz) in enumerate(self._vizs):
            viz.generate(wb, ws)


class Viz:
    PLACE_ABSOLUTE = 1
    PLACE_BELLOW = 2
    PLACE_ABOVE = 3
    PLACE_LEFT = 4
    PLACE_RIGHT = 5

    def __init__(self):
        self._placement = Viz.PLACE_ABSOLUTE
        self._pcol, self._prow = (1, 1)

        self._ref = None
        self._spacer_rows = 0
        self._spacer_cols = 0

        self._generated = False

        self._tl_col, self._tl_row = (1, 1)
        self._br_col, self._br_row = (1, 1)

    def place_at(self, pcol, prow):
        self._placement = Viz.PLACE_ABSOLUTE
        self._pcol = pcol
        self._prow = prow
        return self

    def place_bellow(self, viz, rows=1, align="left"):
        self._placement = Viz.PLACE_BELLOW
        self._ref = viz
        self._spacer_rows = rows
        return self

    def place_left(self, viz, cols=1, align="top"):
        self._placement = Viz.PLACE_LEFT
        self._ref = viz
        self._spacer_cols = cols
        return self

    def merge_cols(self, cols=1):
        self._merge_cols = cols
        return self

    def merge_rows(self, rows=1):
        self._merge_rows = rows
        return self

    def format(self, style):
        self._style = new_style(self._style, style)

    def _generate(self, wb, ws):
        print("Abstract class error")
        quit()

    def generate(self, wb, ws):
        if not self._generated:
            self._generated = True

            # compute the relative positioning
            if self._placement != Viz.PLACE_ABSOLUTE:
                # generate the reference viz (if not already)
                self._ref.generate(wb, ws)
                (ul_col, ul_row, br_col, br_row) = self._ref.get_coords()

                if self._placement == Viz.PLACE_BELLOW:
                    # TBD: honor the align parameter to compute the _pcol
                    self._pcol = ul_col
                    self._prow = br_row + 1 + self._spacer_rows
                
                elif self._placement == Viz.PLACE_LEFT:
                    # TBD: honor the align parameter to compute the _pcol
                    self._pcol = br_col + 1 + self._spacer_cols
                    self._prow = br_row

            # generate it's own
            print("Viz: Create the viz on (%d, %d)" % (self._pcol, self._prow))
            self._generate(wb, ws)
        else:
            print("Done")

    def get_coords(self):
        return self._tl_col, self._tl_row, self._br_col, self._br_row


class Title(Viz):
    def __init__(self, text):
        super().__init__()

        self._text = text
        self._style = style_title

    def _generate(self, wb, ws):
        # Format the title cells
        fmt = wb.add_format(self._style)

        # write the title
        ws.write_string(self._prow, self._pcol, self._text, fmt)

        if self._merge_cols > 0 or self._merge_rows > 0:
            ws.merge_range(self._prow, self._pcol, self._prow + self._merge_rows, self._pcol + self._merge_cols)

        # compute the occupied area
        self._tl_col, self._tl_row = self._pcol, self._prow
        self._br_col, self._br_row = self._pcol + self._merge_cols, self._prow + self._merge_rows


class Table(Viz):
    def __init__(self, title, data, col_types={}, legend=""):
        super().__init__()

        self._title = title
        self._data = data
        self._legend = legend

        # create the default col_types 'str'
        self._col_types = dict(zip(data.columns.values, [str] * len(data.columns)))

        # [TBD] merge the default _col_types w/ the coltypes passed by param
        for k, v in col_types.items():
            self._col_types[k] = v


    def _generate(self, wb, ws):
        (r, c) = self._prow, self._pcol

        # write the title
        ws.write_string(r, c, self._title)

        # [TBD] this space can be configured in the future
        r += 1       

        # write the header
        for (i, col) in enumerate(self._data.columns):
            ws.write_string(r, c + i, col)

        r += 1

        # write the data
        for (i, values) in enumerate(self._data.values):
            for (j, value) in enumerate(values):
                # Convert the date string into a datetime object.
                # date = datetime.strptime(date_str, "%Y-%m-%d")

                # [TBD] use a class parameter "col_type"
                ws.write_string(r + i, c + j, str(value))

                #worksheet.write_datetime(row, col + 1, date, date_format )
                #worksheet.write_number  (row, col + 2, cost, money_format)
                #row += 1

        # [TBD] this space can be configured in the future
        r += len(self._data) + 2

        # write the table legend
        ws.write_string(r, c, self._legend)



        # compute the occupied area
        self._tl_col, self._tl_row = self._pcol, self._prow
        self._br_col, self._br_row = self._pcol + len(self._data.columns), self._prow + len(self._data) + 2


class VTable(Viz):
    def __init__(self, title, data, legend=""):
        super().__init__()

        self._title = title
        self._data = _data

    def _generate(self, wb, ws):
        print("Generate Label")
        print("\t'%s'" % self._title)
        for (k, v) in self._data.items():
            print("\t%s: %s" % (k, str(v)))
        print("\t'%s'" % self._legend)

        # compute the occupied area
        self._tl_col, self._tl_row = self._pcol, self._prow
        self._br_col, self._br_row = self._pcol + 2, self._prow + len(self._data.keys()) + 2



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

