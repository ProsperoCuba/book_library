from rest_framework import serializers

from core.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer to created and update model Author"""

    class Meta:
        model = Author
        fields = ["full_name"]


class BookSerializer(serializers.ModelSerializer):
    """Serializer to created and update model Book"""
    author = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = "__all__"

    def get_author(self, obj):
        return AuthorSerializer(instance=obj.author, many=True).data
