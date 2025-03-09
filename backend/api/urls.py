from django.urls import path
from . import views

urlpatterns = [
    path('example/', views.example_view, name='example'),
    path('put-aircraft/', views.aircraft_post, name='put-aircraft'),
    path('get-aircraft/', views.aircraft_list, name='aircraft-list'),
    path('put-flight/',views.flight_post, name='put-flight'),
    path('get-flight/', views.flight_list, name='flight-list'),
    path('del-all/', views.del_all, name='del-all'),



    path('solve/', views.solve_assignment, name='solve-assignment'),
]

