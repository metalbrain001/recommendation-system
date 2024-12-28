"""
This file contains chatbot urls.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from chatbot import views

router = DefaultRouter()
router.register("chatbot", views.ChatbotViewSet, basename="chatbot")

app_name = "chatbot"

urlpatterns = [
    path("", include(router.urls)),
]
