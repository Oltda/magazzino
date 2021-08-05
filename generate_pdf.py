from fpdf import FPDF
import random
from database import StockItems, ProductCodes
from flask import make_response


class PdfSheet:


    def __init__(self, user_id):
        self.user_id = user_id
        #self.selection = selection


    def to_pdf(self):
        random_id = ''.join((random.choice('abcdxyzpqr') for i in range(5)))
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family='Times', size=12, style='B')

        stock = StockItems.query.filter(StockItems.user_id == self.user_id).order_by(StockItems.id.asc())

        code = ProductCodes.query.filter(ProductCodes.user_id == self.user_id).all()

        pdf.cell(w=100, h=40, border=1, txt="Product", align="C", ln=0)
        pdf.cell(w=100, h=40, border=1, txt="Quantity", align="C", ln=0)
        pdf.cell(w=100, h=40, border=1, txt="Unit", align="C", ln=0)
        pdf.cell(w=100, h=40, border=1, txt="Product Code", align="C", ln=0)
        pdf.cell(w=100, h=40, border=1, txt="Expiration Date", align="C", ln=1)

        pdf.set_font(family='Times', size=12)

        for i in stock:
            pdf.cell(w=100, h=40, border=1, txt=i.product_name, align="C", ln=0)
            pdf.cell(w=100, h=40, border=1, txt=str(i.quantity), align="C", ln=0)

            for x in code:
                if i.product_code == x.id:
                    pdf.cell(w=100, h=40, border=1, txt=x.unit, align="C", ln=0)
                    pdf.cell(w=100, h=40, border=1, txt=str(x.product_code), align="C", ln=0)

            pdf.cell(w=100, h=40, border=1, txt=str(i.expiration_date), align="C", ln=1)



        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers.set('Content-Disposition', 'attachment', filename=random_id + '.pdf')
        response.headers.set('Content-Type', 'application/pdf')

        return response



