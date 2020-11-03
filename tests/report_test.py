# [TBD] improve the test to get 100% coverage of the report.
import pandas as pd

from pybireport.report import Report, Page, Text, Table
#from pybireport.styles import DefaultStyleSheet


data = pd.DataFrame({
	'Produto': ['xx', 'a', 'yy'],
	'Volume': [1, 2, 3],
	'Qty': [4, 2, 3]})


rep = Report("output/test_report.xlsx")

p1 = rep.add(Page("sheet_1"))

vtitle = p1.add(Text("This is my first report")) \
	.format("title") \
	.place_at(0, 0) \
	.merge_cols(4)

vtable = p1.add(Table(data)) \
	.place_bellow(vtitle, rows=2) \
	.title("Contagens*") \
	.legend("*Small legend at the bottom", {'italic': True, 'bold': True}) \
	.format("row_even", {'bold': True, 'bg_color': '#f0f0f0'}) \
	.zebra(True)


p2 = rep.add(Page("sheet_2"))

p2.add(vtable)


rep.generate()