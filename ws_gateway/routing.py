from django.urls import re_path
from ws_gateway import consumers

websocket_urlpatterns = [
    re_path("ws/echo/", consumers.EchoConsumer.as_asgi()),
    re_path("ws/dashboard-analytics/", consumers.DashboardAnalyticsConsumer.as_asgi()),
]
