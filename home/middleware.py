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

        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        # Get user session hash
        session = request.session
        session_hash = session.get('_auth_user_hash', "NON LOGGED IN USER")

        # Get username
        username = request.user.username if request.user.is_authenticated else "NON LOGGED IN USER"
        
        # Create a dictionary with the trace log information
        trace_log = [{
            "traceId": trace_id,
            "spanId": span_id,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
            "principal": username,  # Customize based on your authentication system
            "session": session_hash, 
            "username": username,
            "ip": ip,
            "request": {
                "method": request.method,
                "uri": request.build_absolute_uri(),
                "headers": dict(request.headers),
                "remoteAddress": ip,  # Customize based on your needs
            },
            "response": {
                "status": response.status_code,
                "headers": dict(response.headers),
            },
            "timeTaken": duration,
        }]

        try:
            with open('logger.json', 'r') as file:
                existing_logs = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_logs = []

        # Combine existing logs with new logs
        combined_logs = existing_logs + trace_log

        # Write the combined logs back to the file
        with open('logger.json', 'w') as file:
            file.write(json.dumps(combined_logs, indent=2))
            file.write('\n')

        return response
