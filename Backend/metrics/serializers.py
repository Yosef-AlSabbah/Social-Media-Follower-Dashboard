from rest_framework import serializers

from .models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    """
    Serializer for the Platform model.
    Converts Platform model instances to JSON format and vice versa.
    """

    class Meta:
        model = Platform
        fields = (
            "id",
            "name",
            "name_ar",
            "followers",
            "delta",
            "color",
            "is_active",
            "last_updated",
        )
        read_only_fields = (
            "followers",
            "delta",
            "last_updated",
        )


class TopPlatformSerializer(serializers.Serializer):
    """
    Serializer for top performing platform data.
    Used as a nested serializer in analytics summary.
    """

    id = serializers.UUIDField()
    name = serializers.CharField()
    name_ar = serializers.CharField()
    followers = serializers.IntegerField(min_value=0)


class AnalyticsSummarySerializer(serializers.Serializer):
    """
    Serializer for analytics summary data.
    Contains aggregated metrics and top platform information.
    """

    total_followers = serializers.IntegerField(min_value=0)
    top_platform = TopPlatformSerializer()
    daily_growth = serializers.IntegerField()
    weekly_growth = serializers.IntegerField()
    monthly_growth = serializers.IntegerField()

    def validate(self, data):
        """
        Additional validation to ensure growth values make sense
        """
        # Monthly growth should be greater than or equal to weekly growth
        if abs(data["monthly_growth"]) < abs(data["weekly_growth"]):
            raise serializers.ValidationError(
                "Monthly growth cannot be less than weekly growth"
            )
        # Weekly growth should be greater than or equal to daily growth
        if abs(data["weekly_growth"]) < abs(data["daily_growth"]):
            raise serializers.ValidationError(
                "Weekly growth cannot be less than daily growth"
            )
        return data


class DailyDataPointSerializer(serializers.Serializer):
    """
    Serializer for individual day data points in growth trends.
    """

    day = serializers.CharField(help_text="Day name in Arabic")
    value = serializers.IntegerField(
        min_value=0, help_text="Follower count for that day"
    )
    date = serializers.DateField(help_text="Date in YYYY-MM-DD format")


class GrowthTrendSerializer(serializers.Serializer):
    """
    Serializer for platform growth trend data.
    """

    platform_id = serializers.UUIDField(help_text="Platform UUID reference")
    data = DailyDataPointSerializer(many=True, help_text="Array of daily data points")


class DailyMetricSerializer(serializers.Serializer):
    """
    Serializer for daily metrics data.
    """

    date = serializers.DateField(help_text="Date in YYYY-MM-DD format")
    new_followers = serializers.IntegerField(
        help_text="Number of new followers on this date"
    )
