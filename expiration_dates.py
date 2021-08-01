
from datetime import datetime, timedelta






class ExpirationCalculator:
    def __init__(self, exp_date):
        self.exp_date = exp_date

    def show_days_left(self):
        future_date = datetime.strptime(self.exp_date, '%d-%m-%Y').date()
        if future_date <= datetime.now().date():
            days_left = 1
        else:
            days_left = str(future_date - datetime.now().date())
            days_left = int(days_left.split("days,")[0])
        return days_left







