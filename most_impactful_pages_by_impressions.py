from datetime import date, timedelta, datetime

from metric import Metric

class MostImpactfulPagesByImpressions(Metric):
    def __init__(self, service):
        super().__init__(service)


    def _get_query_body(self):
        end = date.today()
        start = end - timedelta(days = 28)

        return {
            'startDate': start.strftime('%Y-%m-%d'),
            'endDate': end.strftime('%Y-%m-%d'),
            'dimensions': ['page']
        }
    

    def _process(self, raw_data):
        total = sum([element['impressions'] for element in raw_data['rows']])

        data = [self._row_to_object(row, total) for row in raw_data['rows']]

        return sorted(data, key=lambda x: x['impressions'], reverse=True)
    
    def _row_to_object(self, row, total):
        return {
            'page': row['keys'][0],
            'impressions': row['impressions'],
            'percentage': (row['impressions']/total) * 100
        }
    

    def _display(self, data):
        print('-' * 20)
        print('Most impactful pages:')
        for page in data[:5]:
            print(f'Impressions: {page["impressions"]}\t({page["percentage"]:5.2f}%)\t{page["page"]}')
