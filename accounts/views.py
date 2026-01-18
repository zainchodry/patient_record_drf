from django.shortcuts import render
from rest_framework import permissions, status, generics
from . models import *
from . serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        if self.request.user.role in ['doctor', 'admin', 'nurse']:
            return PatientProfile.objects.all()
        return PatientProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            raise ValueError("Refresh Token Is Required")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail":"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"You Logout Successfully"}, status=status.HTTP_205_RESET_CONTENT)
        
class PasswordChangeView(APIView):
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        return Response({"detail":"Password Change Successfully"}, status=status.HTTP_200_OK)
    