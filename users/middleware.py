import time

from django.db import connection


class AdvancedTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()

        response = self.get_response(request)

        total_time = int((time.time() - start) * 1000)

        # DB time
        db_time = sum(float(q['time']) for q in connection.queries) * 1000

        response["x-envoy-upstream-service-time"] = str(total_time)
        response["x-db-time"] = str(int(db_time))

        return response