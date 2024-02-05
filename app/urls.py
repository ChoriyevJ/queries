from django.urls import path
from app import views

urlpatterns = [
    path('regions/avg/', views.RegionResultsAvgView.as_view()),
    path('regions/score/', views.RegionScoreView.as_view()),
    path('region/<int:pk>/district/avg/', views.DistrictResultAvgView.as_view()),
    path('district/<int:pk>/school/avg/', views.SchoolResultsAvgView.as_view()),
    path('region/month/<int:month>/avg/', views.RegionResultsAvgInMonthView.as_view()),
]


