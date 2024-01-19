import time
import json
import uuid

class HttpTraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the trace ID is present in the request headers
        trace_id = request.headers.get('X-Trace-ID')

        # If not present, generate a new trace ID
        if not trace_id:
            trace_id = str(uuid.uuid4())

        # Generate span ID for the current request
        span_id = str(uuid.uuid4())

        # Capture the start time of the request
        start_time = time.time()

        response = self.get_response(request)

        # Capture the end time of the request
        end_time = time.time()

        # Calculate the request duration
        duration = int((end_time - start_time) * 1000)  # Convert to milliseconds

        # Add or update the trace ID in the response headers
        response['X-Trace-ID'] = trace_id

        # Create a dictionary with the trace log information
        trace_log = {
            "traceId": trace_id,
            "spanId": span_id,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
            "principal": None,  # Customize based on your authentication system
            "session": None,  # Customize based on your session handling
            "request": {
                "method": request.method,
                "uri": request.build_absolute_uri(),
                "headers": {k: v for k, v in request.headers.items()},
                "remoteAddress": None,  # Customize based on your needs
            },
            "response": {
                "status": response.status_code,
                "headers": {k: v for k, v in response.headers.items()},
            },
            "timeTaken": duration,
        }

        # Write the trace log to the logger.json file
        with open('logger.json', 'a') as file:
            file.write(json.dumps(trace_log, indent=2))
            file.write('\n')

        return response
