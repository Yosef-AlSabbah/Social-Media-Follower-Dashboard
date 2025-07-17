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


class PlatformList(ListAPIView, RetrieveAPIView):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer


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
