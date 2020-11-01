import pandas as pd

from pybireport.report import Report, Page, Title, Table, Legend
from pybireport.styles import DefaultStyle


data = pd.DataFrame({
	'Produto': ['xx', 'a', 'yy'],
	'Volume': [1, 2, 3],
	'Qty': [4, 2, 3]})


rep = Report("output/test_report.xlsx")

p1 = rep.add_page(Page("sheet_1"))

vtitle = p1.add(Title("This is my first report")) \
	.place_at(1, 1) \
	.merge_cols(4)

vtable = p1.add(Table("Contagens*", data)) \
	.place_bellow(vtitle, rows=2)

vlegend = p1.add(Legend("*Small legend at the bottom")) \
	.place_bellow(vtable) \
	.merge_cols(len(data.columns))

p2 = rep.add_page(Page("sheet_2"))

p2.add(vtable)


rep.generate()