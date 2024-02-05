from django.contrib import admin
from app import models


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', )


@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'region')


@admin.register(models.School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'district')


@admin.register(models.Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'school',)


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'pupil', 'total_answers', 'correct_answers', 'percent')


