from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import LANGUAGE_SESSION_KEY
from django.utils.translation import activate as activate_language
from django.utils.translation import get_language
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import SelectLanguageSerializer


class SelectLanguageViewSet(GenericViewSet):
    """ViewSet for handle system language"""

    permission_classes = (AllowAny,)
    serializer_class = SelectLanguageSerializer

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def select_language(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_language = serializer.validated_data.get("language", settings.LANGUAGE_CODE)
        if request.user.is_authenticated:
            user = request.user
            user.language = user_language
            user.save()
        activate_language(user_language)
        request.session[LANGUAGE_SESSION_KEY] = user_language

        request.LANGUAGE_CODE = user_language
        response = Response({"language": get_language()})
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)
        return response

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny])
    def get_language(self, request):
        return Response({"language": get_language()})


class ServerTimeViewSet(GenericViewSet):
    """ViewSet for get server time info"""

    permission_classes = (AllowAny,)
    serializer_class = None

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny])
    def info(self, request):
        today = now()
        data = {
            "datetime": today.strftime("%Y-%m-%d %H:%M:%S"),
            "date": today.strftime("%Y-%m-%d"),
            "time": today.strftime("%H:%M:%S"),
            "timestamp": int(today.timestamp()),
        }

        return Response(data)
