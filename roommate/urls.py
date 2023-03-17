from django.urls import path
from roommate import views
from django.conf.urls.static import static
from django.conf import settings

from roommate.views import ApartmentCreateView, ApartmentDetailView, UserProfileView

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile-edit/<int:pk>/', views.UserProfileUpdateView.as_view(), name='profile_edit'),
    path('post-room/', ApartmentCreateView.as_view(), name='post_room'),
    path('browse-rooms/', views.browse_rooms, name='browse_rooms'),
    path('apartment/<int:pk>/', ApartmentDetailView.as_view(), name='apartment_detail'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
