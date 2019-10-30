from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('reach-us/', views.reach_us_view, name='reach_us'),
]
