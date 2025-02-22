from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from apps.chat.models import Group


class HomeView(LoginRequiredMixin, ListView):
    model = Group
    template_name = 'chat/home.html'
    context_object_name = 'groups'

    def get_context_date(self, **kwargs):
        """ Добавляем текущего юзера в контекст """
        context = super().get_context_date(self, **kwargs)
        context["user"] = self.request.user
        return context


class GroupChatView(LoginRequiredMixin, DetailView):
    model = Group
    template_name = 'chat/groupchat.html'
    context_object_name = 'group'
    slug_field = 'uuid'  # Используем поле uuid для поиска группы
    slug_url_kwarg = 'uuid'  # Имя параметра в URL

    def get_object(self, queryset=None):
        """ получаем группу пщ uuid """

        uuid = self.kwargs.get('uuid')
        return get_object_or_404(Group, uuid=uuid)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        group = self.object

        if self.request.user not in group.members.all():
            return HttpResponseForbidden("Вы не являетесь участником этой группы!")

        # Получаем сообщения и события
        messages = group.message_set.all()
        events = group.event_set.all()

        message_and_event_list = [*messages, *events]
        sorted_message_event_list = sorted(message_and_event_list, key=lambda x: x.timestamp)

        context["message_and_event_list"] = sorted_message_event_list
        context["group_members"] = group.members.all()

        return context
