import pandas as pd

from pybireport.report import Report, Page, Title, Table, Legend
from pybireport.styles import DefaultStyle


data = pd.DataFrame({
	'a': [1, 2, 3],
	'b': [4, 2, 3],
	'c': [1, 'a', 3]})


rep = Report("output/test_report.xlsx")

p1 = rep.add_page(Page("sheet_1"))
p2 = rep.add_page(Page("sheet_2"))

vtitle = p1.add(Title("This is my first report")) \
	.place_at(1, 1) \
	.merge_cols(4)

vtable = p1.add(Table("Count of stuff*", data)) \
	.place_bellow(vtitle, rows=2)

vlegend = p1.add(Legend("*Small legend at the bottom")) \
	.place_bellow(vtable) \
	.merge_cols(3)

vtitle2 = p1.add(Title("Other title")) \
	.place_left(vtitle, cols=4)



rep.generate()