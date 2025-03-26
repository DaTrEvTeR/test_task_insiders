from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        """
        Проверка существования пользователя и валидации токена.
        """
        uidb64 = self.context.get("uidb64")
        token = self.context.get("token")

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise ValidationError({"uidb64": "Неверный идентификатор пользователя."})

        if not default_token_generator.check_token(user, token):
            raise ValidationError({"token": "Недействительный токен."})

        self.context["user"] = user  # Сохраняем пользователя для использования в `save()`
        return data

    def save(self):
        """
        Устанавливает новый пароль пользователю.
        """
        user = self.context["user"]
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
