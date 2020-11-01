import xlsxwriter

from pybireport.styles import DefaultStyle



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
        # default format for the Viz
        self._style = DefaultStyle()

        # how to place the Viz
        self._placement = Viz.PLACE_ABSOLUTE
        self._pcol, self._prow = (1, 1)

        # reference Viz
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

    def style(self, style):
        self._style = style

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


class VizMerge(Viz):
    def __init__(self):
        super().__init__()

        # merge info
        self._merge_rows = 1
        self._merge_cols = 1

    def merge_cols(self, cols=1):
        self._merge_cols = cols
        return self

    def merge_rows(self, rows=1):
        self._merge_rows = rows
        return self


class Text(VizMerge):
    def __init__(self, text):
        super().__init__()

        self._text = text

    def _format(self, wb):
        # setup all formats
        self._fmt_text = wb.add_format(self._style.text)

    def _generate(self, wb, ws):
        # prepare the format
        self._format(wb)

        # write the text
        if self._merge_cols > 1 or self._merge_rows > 1:
            ws.merge_range(self._prow, self._pcol, self._prow + self._merge_rows - 1, self._pcol + self._merge_cols - 1, self._text, self._fmt_text)
        else:
            ws.write_string(self._prow, self._pcol, self._text, self._fmt_text)

        # compute the occupied area
        self._tl_col, self._tl_row = self._pcol, self._prow
        self._br_col, self._br_row = self._pcol + self._merge_cols, self._prow + self._merge_rows


class Title(Text):
    def _format(self, wb):
        # setup all formats
        self._fmt_text = wb.add_format(self._style.title)


class Legend(Text):
    def _format(self, wb):
        # setup all formats
        self._fmt_text = wb.add_format(self._style.legend)


class Table(Viz):
    def __init__(self, title, data):
        super().__init__()

        self._title = title
        self._data = data

        # default parameters
        self._merge_title = True
        self._zebra = False

        # [TBD] allow a specific format for each column (inherit from row, row_odd, row_even)


    def _format(self, wb):
        # setup all formats
        self._fmt_title = wb.add_format(self._style.table_title)
        self._fmt_header = wb.add_format(self._style.table_header)
        self._fmt_row = wb.add_format(self._style.table_row)
        self._fmt_row_odd = wb.add_format(self._style.table_row_odd)
        self._fmt_row_even = wb.add_format(self._style.table_row_even)

    def _generate(self, wb, ws):
        self._format(wb)

        # start cell
        (r, c) = self._prow, self._pcol

        # write the title
        if self._merge_title:
            ws.merge_range(r, c, r, c + len(self._data.columns) - 1, self._title, self._fmt_title)
        else:
            ws.write_string(r, c, self._title, self._fmt_title)

        # [TBD] this spacer should be configured in the future
        r += 2

        # write the header
        for (i, col) in enumerate(self._data.columns):
            # [TBD] allow a specific format for each header column
            ws.write_string(r, c + i, col, self._fmt_header)

        r += 1

        # write the data
        for (i, values) in enumerate(self._data.values):
            if self._zebra:
                if i % 2 == 0:
                    fmt_cell = self._fmt_row_odd
                else:
                    fmt_cell = self._fmt_row_even
            else:
                fmt_cell = self._fmt_row

            for (j, value) in enumerate(values):
                # Convert the date string into a datetime object.
                # date = datetime.strptime(date_str, "%Y-%m-%d")

                # [TBD] use a class parameter "col_type"
                ws.write_string(r + i, c + j, str(value), fmt_cell)

                #worksheet.write_datetime(row, col + 1, date, date_format )
                #worksheet.write_number  (row, col + 2, cost, money_format)
                #row += 1

        # compute the occupied area
        self._tl_col, self._tl_row = self._pcol, self._prow
        self._br_col, self._br_row = self._pcol + len(self._data.columns), self._prow + len(self._data) + 3

    def zebra(self, on):
        self._zebra = on



class Form(Viz):
    def __init__(self, title, data):
        super().__init__()

        self._title = title
        self._data = _data

    def _generate(self, wb, ws):
        print("Generate Label")
        print("\t'%s'" % self._title)
        for (k, v) in self._data.items():
            print("\t%s: %s" % (k, str(v)))

        # compute the occupied area
        self._tl_col, self._tl_row = self._pcol, self._prow
        self._br_col, self._br_row = self._pcol + 2, self._prow + len(self._data.keys()) + 2



