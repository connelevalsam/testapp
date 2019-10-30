from fpdf import FPDF


class PDFS(FPDF):
    def header(self):
        # logo
        self.image('pages/static/img/logo.png', 20, 8, 33)
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(100)
        # Title
        self.cell(0, 0, 'Invoice', 0, 0, 'R')

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-25)
        # Arial Bold 13
        self.set_font('Arial', 'B', 13)
        self.cell(0, 5, "30 wetheral road, Owerri Imo state", 0, 1, 'C')
        self.set_font('Times', '', 12)
        self.cell(0, 5, "www.smartalaba.com", 0, 1, 'C')
        # Page number
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 1, 'C')


class PdfCreate:
    def __init__(self):
        pass

    def create_invoice_file(self, title, address, site, phone, email, user_name, user_address, description, discount,
                            send_date, quantity, unit_price, total_price, issue_date, due_date, net_total, total_amount_due, payment_details, payment_terms):
        # creating the PDF
        pdf = PDFS()
        pdf.alias_nb_pages()
        pdf.add_page()

        pdf.ln(5)
        pdf.cell(100)
        pdf.set_font('Times', '', 14)
        pdf.cell(0, 0, 'Invoice Date: ' + str(issue_date), 0, 0, 'R')
        pdf.ln(5)
        pdf.cell(100)
        pdf.cell(0, 0, 'Due Date: ' + str(due_date), 0, 0, 'R')
        pdf.ln(30)

        pdf.cell(20)
        pdf.set_font('Arial', 'B', 13)
        pdf.cell(0, 5, title)
        pdf.cell(-20, 5, user_name, 0, 1, 'R')
        pdf.cell(20)
        pdf.set_font('Times', '', 12)
        pdf.cell(0, 5, address)
        pdf.cell(-80)
        pdf.multi_cell(70, 5, user_address, 0, 1, 'C')
        pdf.cell(20)
        pdf.cell(0, 5, phone)
        pdf.ln(5)
        pdf.cell(20)
        pdf.cell(0, 5, email)
        pdf.ln(5)
        pdf.cell(20)
        pdf.cell(0, 5, site)

        pdf.ln(20)
        # Effective page width, or just epw
        epw = pdf.w - 2*pdf.l_margin
        col_width = epw/5
        data = [['Description', 'Date', 'Qty', 'Unit Price', 'Total'],
                [description, send_date, quantity, unit_price, total_price]
                ]
        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, 'Details', align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(5)
        th = pdf.font_size
        iss = 1
        for row in data:
            for datum in row:
                # Enter data in colunms
                iss = iss + 1
                if iss < 7:
                    pdf.set_font('Arial', 'B', 12)
                    pdf.set_fill_color(211, 211, 211)
                    pdf.cell(col_width, 2*th, str(datum), border=0, fill=True)
                else:
                    pdf.set_font('Times', '', 10.0)
                    pdf.cell(col_width, 2*th, str(datum), border=1)

            pdf.ln(2*th)

        pdf.ln(5)
        pdf.cell(100)
        pdf.set_font('Arial', 'B', 12)
        top = pdf.y
        offset = pdf.x + 50
        pdf.multi_cell(40, 3, 'Net Total:', 0, 0)
        pdf.y = top
        pdf.x = offset
        pdf.multi_cell(100, 3, str(net_total)+'0NGA', 0, 0)

        pdf.ln(2)
        pdf.cell(100)
        top = pdf.y
        offset = pdf.x + 50
        pdf.multi_cell(40, 3, 'Discount:', 0, 0)
        pdf.y = top
        pdf.x = offset
        pdf.multi_cell(100, 3, str(discount)+'%', 0, 0)

        pdf.ln(2)
        pdf.cell(100)
        top = pdf.y
        offset = pdf.x + 50
        pdf.multi_cell(60, 3, 'Total Amount Due:', 0, 0)
        pdf.y = top
        pdf.x = offset
        pdf.multi_cell(100, 3, str(total_amount_due)+'0NGA', 0, 0)
        pdf.ln(1)
        pdf.cell(50)
        top = pdf.y
        offset = pdf.x + 50
        pdf.line(offset, top, 205, top)

        pdf.ln(5)
        pdf.cell(20)
        pdf.set_font('Times', '', 13.0)
        # Save top coordinate
        top = pdf.y
        # Calculate x position of next cell
        offset = pdf.x + 40
        pdf.multi_cell(40, 5, 'Payment details:', 0, 0)
        # Reset y coordinate
        pdf.y = top
        # Move to computed offset
        pdf.x = offset
        pdf.multi_cell(80, 5, payment_details, 0, 0)
        pdf.ln(5)
        pdf.cell(20)
        # Save top coordinate
        top = pdf.y
        # Calculate x position of next cell
        offset = pdf.x + 40
        pdf.multi_cell(40, 3, 'Payment terms:', 0, 0)
        # Reset y coordinate
        pdf.y = top
        # Move to computed offset
        pdf.x = offset
        pdf.multi_cell(80, 3, payment_terms, 0, 0)
        pdf.ln(5)
        pdf.cell(20)
        # Save top coordinate
        top = pdf.y
        # Calculate x position of next cell
        offset = pdf.x + 40
        pdf.multi_cell(40, 3, 'Due date:', 0, 0)
        # Reset y coordinate
        pdf.y = top
        # Move to computed offset
        pdf.x = offset
        pdf.multi_cell(80, 3, str(due_date), 0, 0)

        file_name = user_name + '.pdf'
        pdf.output('docs/invoice/' + file_name, 'F')

