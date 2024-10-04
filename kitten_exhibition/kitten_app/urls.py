from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import MyTokenObtainPairView

urlpatterns = [
    path('kittens/breeds/', views.get_breeds_list, name='breeds-list'),
    path('kittens/', views.get_kittens_list, name='kittens-list'),
    path('kittens/<int:pk>/', views.get_kitten_by_id, name='kitten-detail'),
    path('kittens/create/', views.create_kitten, name='kitten-create'),
    path('kittens/<int:pk>/update/', views.update_kitten, name='kitten-update'),
    path('kittens/<int:pk>/delete/', views.delete_kitten, name='kitten-delete'),
    path('rates/create/', views.rate_kitten, name='rate-create'),
    path('rates/<int:pk>/', views.get_rate, name='kitten-rate'),
    path('rates/delete/', views.delete_rate, name='rate-delete'),

    path('register/', views.UserCreateAPIView.as_view(), name='register'),
    path('profile/<int:pk>/', views.get_profile, name='profile'),
    path('profile/update/', views.update_profile, name='profile-update'),

    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
