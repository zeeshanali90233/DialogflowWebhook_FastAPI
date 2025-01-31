from utils.text import clean_text
from fpdf import FPDF

def create_content_pdf(title, content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    title = clean_text(title)
    content = clean_text(content)

    pdf.cell(200, 10, title, ln=True, align="C")
    pdf.ln(10)  # Line break
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, content)

    filename = f"{title.replace(' ', '_').replace('\n','')}.pdf"
    pdf.output(filename, "F")
    return filename
