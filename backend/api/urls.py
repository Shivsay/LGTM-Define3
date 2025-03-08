from django.urls import path
from . import views

urlpatterns = [
    path('example/', views.example_view, name='example'),
    path('put-aircraft/', views.aircraft_post_view, name='put-aircraft'),
    path('solve/', views.solve_assignment, name='solve-assignment'),
    path('get-aircraft/', views.aircraft_list, name='aircraft_list'),
]

