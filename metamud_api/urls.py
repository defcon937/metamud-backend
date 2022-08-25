from django.urls import path
from .views import (
    SwordListApiView,
)

urlpatterns = [
    path('sword', SwordListApiView.as_view()),
]
