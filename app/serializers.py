from rest_framework import serializers
from app import models


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ('title', )


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.District
        fields = ('title', )


class MonthNameSerializer(serializers.Serializer):
    month = serializers.CharField(max_length=20)


class RegionResultAvgSerializer(serializers.ModelSerializer):
    percent = serializers.DecimalField(max_digits=5,
                                       decimal_places=2)

    class Meta:
        model = models.Region
        fields = ('title', 'percent')


class DistrictResultAvgSerializer(serializers.ModelSerializer):
    percent = serializers.DecimalField(max_digits=5,
                                       decimal_places=2)
    # region = RegionSerializer()

    class Meta:
        model = models.District
        fields = ('title', 'percent')


class SchoolResultAvgSerializer(serializers.ModelSerializer):
    percent = serializers.DecimalField(max_digits=5,
                                       decimal_places=2)
    district = DistrictSerializer()

    class Meta:
        model = models.District
        fields = ('title', 'percent', 'district')


class RegionScoreSerializer(serializers.ModelSerializer):
    total_score = serializers.FloatField()

    class Meta:
        model = models.Region
        fields = ('title', 'total_score')



