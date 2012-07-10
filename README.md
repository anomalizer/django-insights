django-views-stats
==================

A set of tools that helps you monitor & debug django applications in production setups

Middlewares
-----------

### HostnameCommentMiddleware
Appends the server's hostname as a html comment at the end of the response. This helps in situations where the application is deployed on multiple servers that are sitting behind a load balancer and we need to figure out which specific machine served this response

### ViewsStatsMiddleware
Aggregates the response times and status codes of each django view
