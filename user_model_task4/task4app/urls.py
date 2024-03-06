from django.urls import path
from .views import ctreate_task,details_api

urlpatterns =[
    path('task/',ctreate_task),
    path('details/<int:pk>/',details_api)
]