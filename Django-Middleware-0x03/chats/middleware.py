import logging
import time

from datetime import datetime
from django.http import HttpResponseForbidden
from djngo.http import HttpResponse

# Configure a dedicated logger for request logging
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")     # logs to file in project root
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware that logs each request with:
    - timestamp
    - user (authenticated or anonymous)
    - request path
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"

        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Restrict access to chat endpoints between 9PM (21:00)
        and 6AM (06:00).
        """
        current_hour = datetime.now().hour

        # Restricted period: 21:00 (9 PM) → 06:00 (6 AM)
        if (current_hour >= 21) or (current_hour < 6):
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>Chat access is restricted during this time.</p>"
            )

        return self.get_response(request)

class OffensiveLanguageMiddleware:
    """
    Tracks the number of POST requests (messages) from each IP.
    Allows only 5 requests per minute.
    """

    RATE_LIMIT = 5           # max messages
    TIME_WINDOW = 60         # seconds

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_history = {}    # {ip: [timestamps]}
    
    def __call__(self, request):
        # Only apply to POST requests (messages)
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR")
            now = time.time()

            # Initialize list for IP if none exists
            if ip not in self.ip_history:
                self.ip_history[ip] = []

            # Remove timestamps older than 60 seconds
            recent_requests = [
                t for t in self.ip_history[ip]
                if now - t < self.TIME_WINDOW
            ]

            self.ip_history[ip] = recent_requests

            # Check if limit exceeded
            if len(recent_requests) >= self.RATE_LIMIT:
                return HttpResponse(
                    "<h1>429 Too Many Requests</h1>"
                    "<p>You are sending messages too quickly. Try again later.</p>",
                    status=429
                )

            # Record this request
            self.ip_history[ip].append(now)

        return self.get_response(request)

class RolepermissionMiddleware:
    """
    Allows access ONLY if the user is admin or moderator.
    Blocks all other users with 403 Forbidden.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user

        # Allow unauthenticated users to reach login page or public routes
        if not user.is_authenticated:
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1><p>You must log in to access this section.</p>"
            )

        # Check if the user is an admin (superuser) or moderator (staff)
        # ALX typically expects: admin = superuser, moderator = staff
        if not (user.is_superuser or user.is_staff):
            return HttpResponseForbidden(
                "<h1>403 Forbidden</h1>"
                "<p>Your role does not have permission to access this section.</p>"
            )

        # User has required role
        return self.get_response(request)

