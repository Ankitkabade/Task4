from django.urls import path
from .views import user_api,userAccountActivate,details_api


urlpatterns=[
    path('create_user/',user_api),
    path('details/<int:pk>/',details_api),
    path('activate/<uid>/<token>/',userAccountActivate,name='activate')
]