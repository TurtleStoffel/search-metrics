class Metric:
    def __init__(self, service):
        self.service = service
    
    def calculate(self):
        body = self._get_query_body()
        data = self._query_search_analytics(body)
        processed_data = self._process(data)
        self._display(processed_data)
    
    def _get_query_body(self):
        raise NotImplementedError()
    
    def _process(self):
        raise NotImplementedError()
    
    def _display(self):
        raise NotImplementedError()
    
    def _query_search_analytics(self, body):
        return self.service.searchanalytics().query(
            siteUrl='sc-domain:turtlestoffel.com', body=body
        ).execute()

