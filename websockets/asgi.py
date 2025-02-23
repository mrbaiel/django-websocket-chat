import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import apps.chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websockets.settings")

asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    "http": asgi_application,
    "websocket":
        AllowedHostsOriginValidator(  # проверяет источник подключения к веб-сокету
            AuthMiddlewareStack(  # заполнит метаданные о соединении с экземпляром пользователя
                URLRouter(apps.chat.routing.websocket_urlpatterns)
            )
        )

})

'''
Эти два класса, AllowedHostsOriginValidator и AuthMiddlewareStack, играют важную роль в безопасности и управлении аутентификацией WebSocket-соединений в Django Channels. Оба используются для настройки промежуточного слоя (middleware), который добавляет дополнительные проверки или возможности для WebSocket-запросов.

1. AllowedHostsOriginValidator

Этот класс проверяет, что WebSocket-запросы поступают с допустимых хостов, указанных в настройках Django (переменной `ALLOWED_HOSTS`).

- Роль: 
  Он обеспечивает безопасность, защищая ваше приложение от запросов с недопустимых доменов (например, запросов с чужих сайтов или поддельных источников). Это важно, чтобы избежать атаки типа Cross-Site WebSocket Hijacking, когда злоумышленник пытается использовать ваше приложение через незарегистрированный хост.

- Как работает: 
  Перед тем как установить WebSocket-соединение, AllowedHostsOriginValidator проверяет, что исходный хост, с которого отправлен запрос, включен в `ALLOWED_HOSTS`. Если хост не разрешен, соединение WebSocket отклоняется.

Пример:
'websocket': AllowedHostsOriginValidator(
    AuthMiddlewareStack(
        URLRouter(chat.routing.websocket_urlpatterns)
    ),
),

Здесь, если хост, с которого приходит запрос на WebSocket, не указан в `ALLOWED_HOSTS`, соединение WebSocket не будет установлено.

2. AuthMiddlewareStack

AuthMiddlewareStack — это класс, который добавляет стандартный механизм аутентификации Django в WebSocket-соединения. Это делает возможным использование пользовательских сессий, куки и других элементов стандартной аутентификации для WebSocket-запросов.

- Роль:
  AuthMiddlewareStack автоматически извлекает аутентификационные данные из HTTP-сессии, связывает пользователя с WebSocket-соединением и передает эту информацию вашему WebSocket-коду (например, потребителям).

- Как работает:
  Когда клиент устанавливает WebSocket-соединение, AuthMiddlewareStack проверяет, аутентифицирован ли пользователь с использованием стандартных механизмов Django, таких как сессии или токены. После аутентификации пользователь будет доступен через self.scope['user'] в WebSocket-потребителях, как в обычных Django запросах через request.user.

Пример:
'websocket': AuthMiddlewareStack(
    URLRouter(chat.routing.websocket_urlpatterns)
),
 

Здесь, при каждом WebSocket-запросе проверяется, аутентифицирован ли пользователь, и передается эта информация в WebSocket-потребители (consumers). Это позволяет использовать WebSocket-соединения только для авторизованных пользователей и работать с их данными.
'''
