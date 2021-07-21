
from datetime import datetime, timedelta





class ExpirationCalculator:
    def __init__(self, exp_date):
        self.exp_date = exp_date

    def show_days_left(self):
        future_date = datetime.strptime(self.exp_date, '%d-%b-%Y').date()

        days_left = str(future_date - datetime.now().date())
        days_left.split(",")
        return days_left[0]








