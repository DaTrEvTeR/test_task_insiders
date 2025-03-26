from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import generics, permissions, status, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .serializers import UserSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer


User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class PasswordResetAPIView(views.APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            User = get_user_model()

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("User with this email not found.")

            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(str(user.pk).encode())

            reset_link = request.build_absolute_uri(f"api/v1/auth/reset/{uidb64}/{token}/")

            send_mail(
                "Reset password",
                f"Follow the link to reset your password: {reset_link}",
                "no-reply@yourdomain.com",
                [email],
            )

            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(views.APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data, context={"uidb64": uidb64, "token": token})

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password successfully changed."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
