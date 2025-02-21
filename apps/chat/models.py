from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


User = get_user_model()


class Group(models.Model):
    """ Групповая модель в которой несколько человек могут преписыватся"""
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=32)
    members = models.ManyToManyField(User)

    def __str__(self):
        return "Группа {self.name} - {self.uuid}"

    def get_absolute_url(self):
        return reverse('group', args=[str(self.uuid)])

    def add_user_to_group(self, user: User):
        self.members.add(user)
        self.event_set.create('Join', user=user) # Устанавливаем значение join в поле type
        self.save()

    def remove_user_from_group(self, user: User):
        self.members.remove(user)
        self.event_set.create('Left', user=user) # Устанавливаем значение left в поле type
        self.save()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author}:- {self.content} в {date} {time.hour}:{time.minute}"


class Event(models.Model):
    CHOICES = [
        ('Join', 'join'),
        ('Left', 'left'),
    ]
    type = models.CharField(choices=CHOICES, max_length=5)
    description = models.CharField(help_text='Описание произошедшего события',\
                                   max_length=50, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.type.lower() == 'join':
            action = 'присоединился в группу'
        elif self.type.lower() == 'left':
            action = 'вышел из группы'

        self.description = f"{self.user} {action} «{self.group}»"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.description}"
