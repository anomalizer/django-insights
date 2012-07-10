from socket import gethostname

class HostnameCommentMiddleware(object):
    def __init__(self):
        hostname = gethostname()
        self.html_comment = "\n<!-- %s -->" % hostname

    def process_response(self, request, response):
        content_type = response.get('Content-Type', '')
        if content_type.startswith('text/html'):
            response.content = response.content + self.html_comment
        return response
