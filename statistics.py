import datetime
import numpy
import threading


class StatisticsManager:
    sales_amount: numpy.array
    order_amount: numpy.array
    total_sales_amount: float
    average_amount_per_order: float
    last_second: int

    def __init__(self):
        self.sales_amount = numpy.zeros(60)
        self.order_amount = numpy.zeros(60)
        self.last_second = -1
        self.last_minute = -1
        self.total_sales_amount = 0.0
        self.average_amount_per_order = 0.0

    def start_compute_statistic(self):
        threading.Timer(1 - datetime.datetime.now().microsecond/1000000, self.compute_statistic).start()

    def compute_statistic(self):
        threading.Timer(1.0, self.compute_statistic).start()
        total_sales_amount = numpy.sum(self.sales_amount)
        order_amount = numpy.sum(self.order_amount)
        if order_amount > 0:
            average_amount_per_order = numpy.sum(self.sales_amount) / order_amount
        else:
            average_amount_per_order = 0
        self.sales_amount[datetime.datetime.now().second] = 0.0
        self.order_amount[datetime.datetime.now().second] = 0.0
        self.total_sales_amount = float(total_sales_amount)
        self.average_amount_per_order = average_amount_per_order

    def add_statistic(self, amount):
        time = datetime.datetime.now()
        second = time.second
        self.sales_amount[second] += amount
        self.order_amount[second] += 1

    def get_statistic(self):
        statistic_dict = (
            {
                "total_sales_amount": "{:0.2f}".format(self.total_sales_amount),
                "average_amount_per_order": "{:0.2f}".format(self.average_amount_per_order)
            }
        )
        return statistic_dict

    def check_time(self):
        time = datetime.datetime.now()
        second = time.second
        last_second = time.second + time.minute * 60 + time.hour * 3600 + time.day * 86400
        if last_second != self.last_second:
            self.compute_statistic(second)
            self.last_second = last_second
        return second
