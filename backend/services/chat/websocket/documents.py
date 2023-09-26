from django.conf import settings
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Message

# store messages in elastic database as backups


class MessageDocument(Document):
    class Index:
        name = "chat_app_messages"

        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Message
        fields = [
            "from_author",
            "to_author",
            "message",
            "created_at",
        ]


if not settings.DEBUG:
    registry.register_document(MessageDocument)
