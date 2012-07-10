class ViewsStatsMiddleware(object):
    def __init__(self):
        self.view_map = {}

    def process_request(self, request):
        print 'processing request'

    def process_view(self, request, view_func, view_args, view_kwargs):
        view_name = '%s.%s' % (view_func.__module__, view_func.__name__) 
        request.__view_name = view_name
        print 'processing view %s' % view_name

    def process_response(self, request, response):
        try:
            view_name = request.__view_name
            print 'processing response %s' % view_name
        except AttributeError:
            print 'aieee, no view for you'
        finally:
            return response
