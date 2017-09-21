from openpyxl import Workbook
from openpyxl.chart import (
    LineChart,
    BarChart,
    Reference,
    Series,
)

wb = Workbook()
ws = wb.active

rows = [
    ['Aliens', 2, 3, 4, 5, 6, 7],
    ['Humans', 1000, 4000, 5000, 2000, 1000, 5000],
]

for row in rows:
    ws.append(row)

c1 = BarChart()
v1 = Reference(ws, min_col=1, min_row=1, max_col=7)
c1.add_data(v1, titles_from_data=True, from_rows=True)

c1.x_axis.title = 'time'
c1.y_axis.title = 'Aliens'
c1.y_axis.majorGridlines = None
c1.title = 'Survey results'


# Create a second chart
c2 = LineChart()
v2 = Reference(ws, min_col=1, min_row=2, max_col=7)
c2.add_data(v2, titles_from_data=True, from_rows=True)
c2.y_axis.axId = 200
c2.y_axis.title = "Humans"

# Display y-axis of the second chart on the right by setting it to cross the x-axis at its maximum
c1.y_axis.crosses = "max"
c1 += c2

ws.add_chart(c1, "D4")

ws2 = wb.create_sheet(title="second sheet")

rows2 = [
    ['rtt', 'loss', 'jitter'],
    [10, 10, 10000],
    [20, 8, 38888],
    [30, 20, 40000],
    [25, 40, 12000],
    [12, 20, 50000],
]

for row in rows2:
    ws2.append(row)

c1 = BarChart()
v1 = Reference(ws2, min_col=1, min_row=1, max_row=6,max_col=2)
c1.add_data(v1, titles_from_data=True)

c1.x_axis.title = 'time'
c1.y_axis.title = 'loss'
c1.y_axis.majorGridlines = None
c1.title = 'Survey results'


# Create a second chart
c2 = LineChart()
v2 = Reference(ws2, min_col=3, min_row=1, max_row=6,max_col=3)
c2.add_data(v2, titles_from_data=True)
c2.y_axis.axId = 200
c2.y_axis.title = "jitter"

# Display y-axis of the second chart on the right by setting it to cross the x-axis at its maximum
c1.y_axis.crosses = "max"
c1 += c2

ws2.add_chart(c1, "E8")

wb.save("secondary.xlsx")