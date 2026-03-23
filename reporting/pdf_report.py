from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


class PDFReport:

    def __init__(self, filepath):
        self.filepath = filepath
        self.styles = getSampleStyleSheet()

    # --------------------------------------------------
    def generate(self, summary, dataframe):

        doc = SimpleDocTemplate(self.filepath, pagesize=A4)

        elements = []

        # --- Title ---
        elements.append(Paragraph("Composite Tooling Cost Report", self.styles["Title"]))
        elements.append(Spacer(1, 20))

        # --- Summary ---
        elements.append(Paragraph("Project Summary", self.styles["Heading2"]))
        elements.append(Spacer(1, 10))

        summary_data = [
            ["Total Cost (€)", f"{summary['total_cost']:.2f}"],
            ["Total Volume (m³)", f"{summary['total_volume']:.3f}"],
            ["Total Boards", f"{summary['total_boards']}"],
            ["Number of Components", f"{summary['num_components']}"],
        ]

        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        # --- Component Table ---
        elements.append(Paragraph("Component Breakdown", self.styles["Heading2"]))
        elements.append(Spacer(1, 10))

        # Convert dataframe to table
        table_data = [list(dataframe.columns)] + dataframe.values.tolist()

        comp_table = Table(table_data)
        comp_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(comp_table)

        # --- Build PDF ---
        doc.build(elements)