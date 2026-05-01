from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView , TokenVerifyView
from .views import MyView, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', TokenObtainPairView.as_view(), name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='auth-token-verify'),
    path('me/', MyView.as_view(), name='auth-me'),
]