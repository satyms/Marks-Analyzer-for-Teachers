from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv, name='upload_csv'),
    path('analyze/', views.analyze_marks, name='analyze'),
    path('', views.analyze_marks, name='home'),
] 