# middleware.py

import time
import json
import uuid
from django.contrib.auth.models import AnonymousUser

class HttpTraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Generate trace and span IDs
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())

        # Capture the start time of the request
        start_time = time.time()

        response = self.get_response(request)

        # Capture the end time of the request
        end_time = time.time()

        # Calculate the request duration
        duration = int((end_time - start_time) * 1000)  # Convert to milliseconds

        # Extract session and principal information
        session_info = self.serialize_session(request.session) if hasattr(request, 'session') else None
        principal_info = self.serialize_user(request.user) if hasattr(request, 'user') else None

        # Create a dictionary with the trace log information
        trace_log = {
            "traces": [
                {
                    "traceId": trace_id,
                    "spanId": span_id,
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
                    "principal": principal_info,
                    "session": session_info,
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
            ]
        }

        # Write the trace log to the logger.json file
        with open('logger.json', 'a') as file:
            file.write(json.dumps(trace_log, indent=2))
            file.write('\n')

        return response

    def serialize_user(self, user):
        # Serialize user information to a format that can be JSON serialized
        if user is None or isinstance(user, AnonymousUser):
            return None
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            # Add any other user attributes you want to include
        }

    def serialize_session(self, session):
        # Serialize session information to a format that can be JSON serialized
        if session is None:
            return None
        # Example: Extract session key and other relevant data
        return {
            "session_key": session.session_key,
            "custom_data": session.get("custom_data", None),
            # Add any other session attributes you want to include
        }
