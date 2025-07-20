from django.urls import path
from .views import (
    PlatformListView,
    PlatformRetrieveView,
    AnalyticsSummaryView,
    GrowthTrendsView,
    DailyMetricsView,
    InvalidateCacheView,
    ForceRefreshView,
)

app_name = "metrics"

urlpatterns = [
    # Platform endpoints
    path("platforms/", PlatformListView.as_view(), name="platform-list"),
    path("platforms/<uuid:pk>/", PlatformRetrieveView.as_view(), name="platform-detail"),
    # Analytics endpoints
    path(
        "analytics/summary/", AnalyticsSummaryView.as_view(), name="analytics-summary"
    ),
    path("analytics/growth-trends/", GrowthTrendsView.as_view(), name="growth-trends"),
    path("analytics/daily-metrics/", DailyMetricsView.as_view(), name="daily-metrics"),
    path(
        "analytics/invalidate-cache/",
        InvalidateCacheView.as_view(),
        name="invalidate-cache",
    ),
    path(
        "analytics/force-refresh/",
        ForceRefreshView.as_view(),
        name="force-refresh",
    ),
]
