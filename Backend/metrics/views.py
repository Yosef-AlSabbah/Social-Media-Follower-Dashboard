from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from core.utils.analytics import AnalyticsManager
from core.utils.logger import logger
from .models import Platform
from .serializers import (
    PlatformSerializer,
    AnalyticsSummarySerializer,
    GrowthTrendSerializer,
    DailyMetricSerializer,
)
from .tasks.tasks import execute_all_metrics_tasks


@extend_schema(
    operation_id="analytics_force_refresh",
    description="Trigger an immediate refresh of all platform metrics.",
    tags=["Analytics"],
    responses={
        202: OpenApiResponse(
            description="Refresh task has been successfully triggered."
        ),
        500: OpenApiResponse(description="Internal Server Error."),
    },
)
class ForceRefreshView(APIView):
    """
    An endpoint to trigger an on-demand refresh of all platform metrics.
    """

    def post(self, request):
        """
        Triggers the Celery task to refresh platform metrics in the background.
        """
        try:
            execute_all_metrics_tasks.apply_async(countdown=3)
            logger.info("Force refresh task triggered successfully via API.")
            return Response(
                {"message": "Platform metric refresh has been triggered."},
                status=status.HTTP_202_ACCEPTED,
            )
        except Exception as e:
            logger.error(f"Error triggering force refresh task via API: {e}")
            return Response(
                {"error": "Failed to trigger refresh task."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    operation_id="analytics_invalidate_cache",
    description="Invalidate all analytics-related caches.",
    tags=["Analytics"],
    responses={
        200: OpenApiResponse(description="Caches invalidated successfully."),
        500: OpenApiResponse(description="Internal Server Error."),
    },
)
class InvalidateCacheView(APIView):
    """
    An endpoint to manually invalidate all analytics-related caches.
    """

    def post(self, request):
        """
        Invalidates the cache for analytics summary, growth trends, and daily metrics.
        """
        try:
            AnalyticsManager.invalidate_analytics_cache()
            logger.info("Analytics cache invalidated successfully via API.")
            return Response(
                {"message": "Analytics caches have been successfully invalidated."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error invalidating cache via API: {e}")
            return Response(
                {"error": "Failed to invalidate caches."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    operation_id="platform_list",
    description="List all social media platforms.",
    tags=["Platforms"],
    responses={
        200: OpenApiResponse(
            description="List of platforms retrieved successfully.",
            response=PlatformSerializer(many=True),
        ),
    },
)
class PlatformListView(ListAPIView):
    """
    Platform API View that handles listing all platforms.

    GET /platforms/ - List all platforms
    """

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


@extend_schema(
    operation_id="platform_retrieve",
    description="Retrieve a single social media platform by ID.",
    tags=["Platforms"],
    responses={
        200: OpenApiResponse(
            description="Platform retrieved successfully.",
            response=PlatformSerializer,
        ),
        404: OpenApiResponse(description="Platform not found."),
    },
)
class PlatformRetrieveView(RetrieveAPIView):
    """
    Platform API View that handles retrieving a single platform.

    GET /platforms/{id}/ - Retrieve a specific platform by ID
    """

    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


@extend_schema(
    operation_id="analytics_summary",
    description="Retrieve a summary of analytics data, including total followers, top platform, and growth metrics.",
    tags=["Analytics"],
    responses={
        200: OpenApiResponse(
            description="Analytics summary retrieved successfully.",
            response=AnalyticsSummarySerializer,
        ),
        500: OpenApiResponse(description="Internal Server Error."),
    },
)
class AnalyticsSummaryView(APIView):
    """
    Analytics summary endpoint that returns cached data.
    GET /analytics/summary/

    Returns total followers, top platform, and growth metrics.
    """

    def get(self, request):
        """
        Retrieve analytics summary from cache.

        Returns:
            Response: Analytics summary data or error message
        """
        try:
            logger.info("Analytics summary requested")

            # Get cached data from AnalyticsManager
            summary_data = AnalyticsManager.get_analytics_summary()

            # Serialize the data for validation
            serializer = AnalyticsSummarySerializer(summary_data)

            logger.info("Analytics summary successfully retrieved")
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving analytics summary: {e}")
            return Response(
                {"error": "Failed to retrieve analytics summary"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    operation_id="analytics_growth_trends",
    description="Retrieve 7-day follower growth trends for all platforms.",
    tags=["Analytics"],
    responses={
        200: OpenApiResponse(
            description="Growth trends retrieved successfully.",
            response=GrowthTrendSerializer(many=True),
        ),
        500: OpenApiResponse(description="Internal Server Error."),
    },
)
class GrowthTrendsView(APIView):
    """
    Growth trends endpoint that returns cached data.
    GET /analytics/growth-trends/

    Returns 7-day follower trends for all platforms with Arabic day names.
    """

    def get(self, request):
        """
        Retrieve growth trends from cache.

        Returns:
            Response: Growth trends data for all platforms
        """
        try:
            logger.info("Growth trends requested")

            # Get cached data from AnalyticsManager
            trends_data = AnalyticsManager.get_growth_trends()

            # Serialize the data for validation
            serializer = GrowthTrendSerializer(trends_data, many=True)

            logger.info(
                f"Growth trends successfully retrieved for {len(trends_data)} platforms"
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving growth trends: {e}")
            return Response(
                {"error": "Failed to retrieve growth trends"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    operation_id="analytics_daily_metrics",
    description="Retrieve daily new follower counts for the last 30 days.",
    tags=["Analytics"],
    responses={
        200: OpenApiResponse(
            description="Daily metrics retrieved successfully.",
            response=DailyMetricSerializer(many=True),
        ),
        500: OpenApiResponse(description="Internal Server Error."),
    },
)
class DailyMetricsView(APIView):
    """
    Daily metrics endpoint that returns cached data.
    GET /analytics/daily-metrics/

    Returns daily new follower counts for the last 30 days.
    """

    def get(self, request):
        """
        Retrieve daily metrics from cache.

        Returns:
            Response: Daily metrics data for the last 30 days
        """
        try:
            logger.info("Daily metrics requested")

            # Get cached data from AnalyticsManager
            daily_data = AnalyticsManager.get_daily_metrics()

            # Serialize the data for validation
            serializer = DailyMetricSerializer(daily_data, many=True)

            logger.info(
                f"Daily metrics successfully retrieved for {len(daily_data)} days"
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving daily metrics: {e}")
            return Response(
                {"error": "Failed to retrieve daily metrics"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
