#from database import StockItems, ProductCodes, Sales
#from sklad import app


# sale_list = []
# sales = Sales.query.filter(Sales.user_id == 1).filter(Sales.sale_date == '2021-08-01').all()
# for i in sales:
#     sale_list.append({'id':i.product_id, 'quantity':i.sold_quantity})



class SalesDateQuantity:

    def __init__(self, date, user_id, model):
        self.date = date
        self.user_id = user_id
        self.model = model

    def show_sales(self):
        if self.date == "all":
            sales = self.model.query.filter(self.model.user_id == self.user_id).order_by(self.model.sale_date)
        else:
            sales = self.model.query.filter(self.model.user_id == self.user_id).filter(self.model.sale_date == self.date).all()

        sale_list = []
        for i in sales:
            sale_list.append({'id': i.product_id, 'quantity': i.sold_quantity, 'sale_date':i.sale_date.strftime('%d-%m-%Y')})

        return sale_list

# data = SalesDateQuantity('2021-08-01', 1)
# data2 = SalesDateQuantity("all", 1)
#
# print(data2.show_sales())







