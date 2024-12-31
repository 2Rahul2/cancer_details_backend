from django.urls import path
from .views import UserRegisterView ,UserLoginView  ,TokenVerificationView ,UserDataView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('api/verify-token/', TokenVerificationView.as_view()),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Login (get access & refresh tokens)
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),

    path('user-data/<str:id>' , UserDataView.as_view()),
]
