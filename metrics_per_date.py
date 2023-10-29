import matplotlib.pyplot as plt

from datetime import date, timedelta, datetime
from matplotlib.dates import DateFormatter

from metric import Metric

class MetricsPerDate(Metric):
    def __init__(self, service):
        super().__init__(service)
    

    def _get_query_body(self):
        end = date.today()
        start = end - timedelta(days = 28)

        return {
            'startDate': start.strftime('%Y-%m-%d'),
            'endDate': end.strftime('%Y-%m-%d'),
            'dimensions': ['date']
        }
    

    def _process(self, raw_data):
        return [{'date': row['keys'][0], 'impressions': row['impressions']} for row in raw_data['rows']]
    

    def _display(self, data):
        x = [datetime.strptime(element['date'], '%Y-%m-%d').date() for element in data]
        y = [element['impressions'] for element in data]

        _, ax = plt.subplots()
        ax.plot(x, y)
        ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))

        plt.show()
