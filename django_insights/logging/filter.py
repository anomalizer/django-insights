from logging import Filter

# BROKEN!!!!

class HttpTracerFilter(Filter):
    TRACER_HEADER = 'X-Trace-Log'

    def filter(self, record):
        request = record.request
        is_debug = request.META.get(self.TRACER_HEADER)
        return is_debug
