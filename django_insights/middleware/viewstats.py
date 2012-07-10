import logging
from time import time

class ViewsStatsMiddleware(object):
    def __init__(self):
        self.view_map = {}

    def _get_request_millis(self, request):
        t2 = time()
        t1 = request.__start_time
        return (t2 - t1) * 1000

    def _seed_request(self, request):
        request.__start_time = time()

    def process_request(self, request):
        self._seed_request(request)
        logging.debug('processing request')

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.__view = view_func

    def process_response(self, request, response):
        view_func = None
        try:
            view_func = request.__view
            logging.debug('processing response %s',view_func)
        except AttributeError:
            view_func = unknown
            logging.debug('aieee, no view for you')

        if(view_func in self.view_map):
            counter = self.view_map[view_func]
        else:
            counter = HttpStatusCounter()
            self.view_map[view_func] = counter
        
        elapsed = self._get_request_millis(request)
        counter.record_request(response.status_code, elapsed) #TODO: real time taken
        for k, v in self.view_map.iteritems():
            logging.debug("%s => %s", k, v)
        return response

def unknown():
    pass

class HttpStatusCounter(object):
    def __init__(self):
        self.code_count = {}
        self.code_time = {}

    def record_request(self, status_code, millis):
        if(status_code not in self.code_count):
            self.code_count[status_code] = 1
            self.code_time[status_code] = millis
        else:
            self.code_count[status_code] = self.code_count[status_code] + 1
            self.code_time[status_code] = self.code_time[status_code] + millis

    def get_counts(self):
        return self.code_count

    def get_cumulative_duration(self):
        return self.code_time

    def __str__(self):
        return 'invocations: %s, cumulative millis %s' % (self.code_count, self.code_time)
