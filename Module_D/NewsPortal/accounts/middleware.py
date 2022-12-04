from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest
from datetime import datetime, timedelta
import pytz


class TimeoutLogout:

    def __init__(self, get_response):
        self.get_response = get_response
        self.ttl = settings.LOGOUT_TIMEOUT

    def __call__(self, request: HttpRequest):
        user = request.user
        tz_0 = pytz.timezone('UTC')

        if (
                not user.is_anonymous
                and user.last_login < tz_0.localize(datetime.utcnow()) - timedelta(seconds=self.ttl)
        ):
            logout(request)

        response = self.get_response(request)

        return response
