
from datetime import datetime, timedelta



# stock_items_collection = StockItems.query.all()
# items_list = []
#
# for i in stock_items_collection:
#     items_list.append({"id": i.id,
#                        "product_name": i.product_name,
#                        "quantity": i.quantity,
#                        "expiration_date": i.expiration_date.strftime('%d-%b-%Y'),
#                        "warehouse_id": i.warehouse_id,
#                        "product_code": i.product_code})



class ExpirationCalculator:
    def __init__(self, exp_date):
        self.exp_date = exp_date

    def show_days_left(self):
        future_date = datetime.strptime(self.exp_date, '%d-%b-%Y').date()

        days_left = str(future_date - datetime.now().date())
        days_left = int(days_left.split("days,")[0])
        return days_left









