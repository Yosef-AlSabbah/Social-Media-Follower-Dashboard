from django.urls import path
from .views import (
    PlatformList,
    AnalyticsSummaryView,
    GrowthTrendsView,
    DailyMetricsView,
)

app_name = "metrics"

urlpatterns = [
    # Platform endpoints
    path("platforms/", PlatformList.as_view(), name="platform-list"),
    # Analytics endpoints
    path(
        "analytics/summary/", AnalyticsSummaryView.as_view(), name="analytics-summary"
    ),
    path("analytics/growth-trends/", GrowthTrendsView.as_view(), name="growth-trends"),
    path("analytics/daily-metrics/", DailyMetricsView.as_view(), name="daily-metrics"),
]
