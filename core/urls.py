from django.urls import path
from .views import IndexView, ReviewsAPIView, ChatbotAPIView

urlpatterns = [
    path("",               IndexView.as_view(),    name="index"),
    path("api/reviews/",   ReviewsAPIView.as_view(), name="api-reviews"),
    path("api/chatbot/",   ChatbotAPIView.as_view(), name="api-chatbot"),
]
