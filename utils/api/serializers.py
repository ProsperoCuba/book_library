from rest_framework import serializers

from config.settings import LANGUAGES


class SelectLanguageSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=LANGUAGES)
