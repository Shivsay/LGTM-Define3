from django.urls import path
from . import views

urlpatterns = [
    path('example/', views.example_view, name='example'),
    path('put-aircraft/', views.aircraft_post_view, name='put-aircraft'),
]

