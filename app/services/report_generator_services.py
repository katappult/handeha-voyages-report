from fpdf import FPDF


def add_intro(pdf, debut_date, fin_date):
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, "Bonjour voyagiste,", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Voici votre récapitulatif de la semaine du {debut_date} au {fin_date}.")
    pdf.ln(10)


def add_table(pdf, voyages):
    # Header of the table
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Circuit ou séjour', 1)
    pdf.cell(30, 10, 'Référence', 1)
    pdf.cell(30, 10, 'Nombre de vues', 1)
    pdf.cell(50, 10, 'Nombre de demandes de devis', 1)
    pdf.cell(30, 10, 'Nombre de ventes', 1)
    pdf.ln()

    # Table body
    pdf.set_font('Arial', '', 12)
    for voyage in voyages:
        pdf.cell(40, 10, voyage['circuitOuSejour'], 1)
        pdf.cell(30, 10, voyage['reference'], 1)
        pdf.cell(30, 10, str(voyage['nombreVue']), 1)
        pdf.cell(50, 10, str(voyage['nombreDemandeDevis']), 1)
        pdf.cell(30, 10, str(voyage['nombreVente']), 1)
        pdf.ln()


def add_chart(pdf, image_path):
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Résumé graphique', ln=True, align='C')
    pdf.ln(5)
    pdf.image(image_path, x=60, y=pdf.get_y(), w=90)  # Adding the chart image
    pdf.ln(10)


def add_footer_text(pdf):
    pdf.ln(10)
    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, "L'équipe handeha-voyages.com")


def create_pdf(image_path, output_path, rapport):
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Récapitulatif de la semaine", ln=True, align='C')
    pdf.ln(10)

    # Intro
    add_intro(pdf, rapport['debutDate'], rapport['finDate'])

    # Table
    add_table(pdf, rapport['voyages'])

    # Image (Chart)
    add_chart(pdf, image_path)

    # Footer Text
    add_footer_text(pdf)

    # Output the PDF to file
    pdf.output(output_path)


# Sample usage
if __name__ == "__main__":
    rapport = {
        'debutDate': '01/09/2024',
        'finDate': '07/09/2024',
        'voyages': [
            {
                'circuitOuSejour': 'Paris Tour',
                'reference': 'REF123',
                'nombreVue': 100,
                'nombreDemandeDevis': 5,
                'nombreVente': 2,
            },
            {
                'circuitOuSejour': 'Rome Getaway',
                'reference': 'REF456',
                'nombreVue': 150,
                'nombreDemandeDevis': 7,
                'nombreVente': 3,
            },
        ],
    }
    image_path = 'path/to/chart_image.png'  # Replace with the path to your image
    output_path = 'recap_semaine.pdf'

    generator = ReportGenerator()
    create_pdf(image_path, output_path, rapport)
