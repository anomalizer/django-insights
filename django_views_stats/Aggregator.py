class ViewsStatsMiddleware(object):
    def __init__(self):
        self.view_map = {}

    def process_request(self, request):
        print 'processing request'

    def process_view(self, request, view_func, view_args, view_kwargs):
        request.__view = view_func

    def process_response(self, request, response):
        view_func = None
        try:
            view_func = request.__view
            print 'processing response %s' % view_func
        except AttributeError:
            view_func = unknown
            print 'aieee, no view for you'

        if(view_func in self.view_map):
            counter = self.view_map[view_func]
        else:
            counter = HttpStatusCounter()
            self.view_map[view_func] = counter
        
        counter.record_request(response.status_code, 1) #TODO: real time taken
        for k, v in self.view_map.iteritems():
            print "%s => %s" % (k, v)
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
