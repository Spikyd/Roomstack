from django.urls import path
from roommate import views
from django.conf.urls.static import static
from django.conf import settings

from roommate.views import ApartmentCreateView, ApartmentDetailView, UserProfileView, ApartmentUpdateView, \
    UserProfileUpdateView, MatchFinder, UnreadMessagesView

urlpatterns = [
    path('', views.HomeTemplateView.as_view(), name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('settings/', UserProfileUpdateView.as_view(), name='settings'),
    path('post-room/', ApartmentCreateView.as_view(), name='post_room'),
    path('browse-rooms/', views.browse_rooms, name='browse_rooms'),
    path('apartment/<int:pk>/', ApartmentDetailView.as_view(), name='apartment_detail'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('manage-apartment/<int:pk>/', ApartmentUpdateView.as_view(), name='manage_apartment'),
    path('delete-apartment/<int:pk>/', views.delete_apartment, name='delete_apartment'),
    path('favorite_rooms/', views.favorite_rooms, name='favorite_rooms'),
    path('matched_users/', MatchFinder.as_view(), name='matched_users'),
    path('messages/<int:user_id>/', views.messages_view, name='messages_view'),
    path('unread_messages/', UnreadMessagesView.as_view(), name='unread_messages'),
    path('messages/', views.conversations_view, name='conversations_view'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
