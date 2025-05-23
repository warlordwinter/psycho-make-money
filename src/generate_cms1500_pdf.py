from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import json

def load_form_data(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

def draw_label_value(c, x, y, label, value, width=2.5*inch):
    """Draw a label and its value in a neat format."""
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.black)
    c.drawString(x, y + 12, label)

    c.setFont("Helvetica", 10)
    if isinstance(value, list):
        value = ", ".join(str(v) for v in value)
    c.drawString(x, y, str(value)[:50])  # truncate if too long

def draw_section_separator(c, y):
    """Draw a horizontal line to separate sections with padding."""
    c.setStrokeColor(colors.gray)
    c.setLineWidth(0.5)
    # Add padding above and below the line
    y += 0.1 * inch  # Space above
    c.line(0.75*inch, y, 7.5*inch, y)
    y -= 0.2 * inch  # Space below
    return y  # Return the new y position

def generate_cms1500_pdf(form_data, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle("CMS-1500 Form")

    # Title - Center justified
    c.setFont("Helvetica-Bold", 16)
    title = "CMS-1500 (02/12) Medical Claim Form"
    title_width = c.stringWidth(title, "Helvetica-Bold", 16)
    c.drawString((letter[0] - title_width) / 2, 10.5 * inch, title)

    y = 10 * inch
    section_spacing = 0.6 * inch
    field_spacing = 2.7 * inch
    left_margin = 0.75 * inch

    def draw_section_title(title):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left_margin, y, title)
        y -= 0.3 * inch

    # Patient Info
    draw_section_title("Patient Information")
    draw_label_value(c, left_margin, y, "Name", form_data["patient_name"])
    draw_label_value(c, left_margin + field_spacing, y, "DOB", form_data["patient_dob"])
    draw_label_value(c, left_margin + 2 * field_spacing, y, "Sex", form_data["patient_sex"])
    y -= section_spacing
    

    draw_label_value(c, left_margin, y, "Address", form_data["patient_address"])
    draw_label_value(c, left_margin + field_spacing, y, "City", form_data["patient_city"])
    draw_label_value(c, left_margin + 2 * field_spacing, y, "State", form_data["patient_state"])
    draw_label_value(c, left_margin + 3 * field_spacing, y, "ZIP", form_data["patient_zip"])
    y -= section_spacing
    y = draw_section_separator(c, y)

    # Insurance Info
    draw_section_title("Insurance Information")
    draw_label_value(c, left_margin, y, "Insurance Type", form_data["insurance_type"])
    draw_label_value(c, left_margin + field_spacing, y, "Insured ID", form_data["insured_id_number"])
    y -= section_spacing

    draw_label_value(c, left_margin, y, "Insured Name", form_data["insured_name"])
    draw_label_value(c, left_margin + field_spacing, y, "DOB", form_data["insured_dob"])
    draw_label_value(c, left_margin + 2 * field_spacing, y, "Sex", form_data["insured_sex"])
    y -= section_spacing
    y = draw_section_separator(c, y)

    # Service Info
    draw_section_title("Service Information")
    draw_label_value(c, left_margin, y, "Service Date", form_data["service_date"])
    draw_label_value(c, left_margin + field_spacing, y, "Place of Service", form_data["place_of_service"])
    draw_label_value(c, left_margin + 2 * field_spacing, y, "Procedure Codes", form_data["procedure_codes"])
    y -= section_spacing

    draw_label_value(c, left_margin, y, "Diagnosis Codes", form_data["diagnosis_codes"])
    draw_label_value(c, left_margin + field_spacing, y, "Charge Amount", form_data["charge_amount"])
    draw_label_value(c, left_margin + 2 * field_spacing, y, "Units", form_data["service_units"])
    y -= section_spacing
    y = draw_section_separator(c, y)

    # Provider Info
    draw_section_title("Provider Information")
    draw_label_value(c, left_margin, y, "Rendering Provider NPI", form_data["rendering_provider_npi"])
    draw_label_value(c, left_margin + field_spacing, y, "Billing Provider Name", form_data["billing_provider_name"])
    y -= section_spacing

    draw_label_value(c, left_margin, y, "Billing Address", form_data["billing_provider_address"])
    draw_label_value(c, left_margin + field_spacing, y, "City", form_data["billing_provider_city"])
    draw_label_value(c, left_margin + 2 * field_spacing, y, "State", form_data["billing_provider_state"])
    draw_label_value(c, left_margin + 3 * field_spacing, y, "ZIP", form_data["billing_provider_zip"])
    y -= section_spacing
    y = draw_section_separator(c, y)

    # Additional Info
    draw_section_title("Additional Information")
    draw_label_value(c, left_margin, y, "Prior Authorization Number", form_data["prior_authorization_number"])
    draw_label_value(c, left_margin + field_spacing, y, "Accept Assignment", form_data["accept_assignment"])
    y -= section_spacing
    y = draw_section_separator(c, y)

    # Facility Info
    draw_section_title("Service Facility")
    draw_label_value(c, left_margin, y, "Facility Name", form_data["service_facility_name"])
    draw_label_value(c, left_margin + field_spacing, y, "NPI", form_data["service_facility_npi"])

    c.save()

def main():
    form_data = load_form_data("src/form-info.json")
    output_path = "cms1500_form.pdf"
    generate_cms1500_pdf(form_data, output_path)
    print(f"Generated CMS-1500 form at: {output_path}")

if __name__ == "__main__":
    main()
