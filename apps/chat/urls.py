from django.urls import path

from apps.chat.views import HomeView, GroupChatView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("groups/<uuid:uuid>/", GroupChatView.as_view(), name="group"),
]
