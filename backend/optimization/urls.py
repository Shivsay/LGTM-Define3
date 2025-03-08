from django.urls import path
from .views import optimize_tail_assignment

urlpatterns = [
    path("optimize/", optimize_tail_assignment, name="optimize"),
]
