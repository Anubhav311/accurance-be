from docx.shared import Inches, Cm, Pt
from border_style import set_table_borders

def build_attendance_table(doc, directors):
    subdoc = doc.new_subdoc()
    table = subdoc.add_table(rows=1, cols=4)

    set_table_borders(table)
    table.autofit = False

    column_widths = [Cm(2), Inches(2.5), Inches(1.5), Inches(1.5)]

    # Header
    headers = [
        "S. No.",
        "Name of the Directors/Attendees",
        "Mode of Attendance",
        "Signature",
    ]

    hdr_cells = table.rows[0].cells
    for i, text in enumerate(headers):
        hdr_cells[i].text = text

    # Data rows
    for idx, d in enumerate(directors, start=1):
        row = table.add_row().cells
        row[0].text = str(idx)
        row[1].text = f"{d['name']} - {d['designation']} ({d['din']})"

    # Force column widths AFTER rows exist
    for row in table.rows:
        for i, width in enumerate(column_widths):
            row.cells[i].width = width

    return subdoc
