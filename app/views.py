from datetime import datetime

from django.db.models import Avg, Count, Case, When, FloatField, Sum
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from app import models
from app import serializers


class RegionResultsAvgView(ListAPIView):
    serializer_class = serializers.RegionResultAvgSerializer

    def get_queryset(self):
        queryset = models.Region.objects.annotate(
            percent=Avg('districts__schools__pupils__tests__percent')
        )

        return queryset


class DistrictResultAvgView(ListAPIView):
    queryset = models.District.objects.all()
    serializer_class = serializers.DistrictResultAvgSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(region_id=self.kwargs.get('pk'))
        return queryset.annotate(
            percent=Avg('schools__pupils__tests__percent')
        ).order_by('-percent')[:3]

    def list(self, request, *args, **kwargs):
        serializer = super().get_serializer(self.get_queryset(), many=True)
        data = serializer.data
        data.append(serializers.RegionSerializer(
            models.Region.objects.get(pk=self.kwargs.get('pk'))
        ).data)
        return Response(data)


class SchoolResultsAvgView(ListAPIView):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolResultAvgSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            district_id=self.kwargs.get('pk')
        )
        return queryset.annotate(
            percent=Avg("pupils__tests__percent")
        ).order_by('-percent')

    def list(self, request, *args, **kwargs):
        serializer = super().get_serializer(self.get_queryset(), many=True)
        data = serializer.data
        data.append(serializers.RegionSerializer(
            models.District.objects.get(pk=self.kwargs.get('pk'))
        ).data)
        return Response(data)


class RegionResultsAvgInMonthView(ListAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionResultAvgSerializer

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            districts__schools__pupils__tests__date__month=self.kwargs.get('month')
        ).annotate(
            percent=Avg('districts__schools__pupils__tests__percent')
        )

        return queryset

    def list(self, request, *args, **kwargs):
        serializer = super().get_serializer(self.get_queryset(), many=True)
        data = serializer.data
        if data:
            month_name = datetime.strptime(str(self.kwargs.get('month')), "%m").strftime("%B")
            month_name_serial = serializers.MonthNameSerializer(data={'month': month_name})
            month_name_serial.is_valid(raise_exception=True)
            data.append(month_name_serial.data)
        return Response(data)


class RegionScoreView(ListAPIView):
    queryset = models.Region.objects.all()
    serializer_class = serializers.RegionScoreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tests = models.Test.objects.annotate(
            score=Case(
                When(percent__gt=80, then=1),
                When(percent__gt=50, then=0.5),
                default=0,
                output_field=FloatField()
            )
        )

        queryset = queryset.annotate(
            total_score=Sum('districts__schools__pupils__tests__score')
        )

        return queryset




