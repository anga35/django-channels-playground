from django.urls import path

from api.views import GetUnreadMessages


urlpatterns = [
    path('get_unread/',GetUnreadMessages.as_view())
]