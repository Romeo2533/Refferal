from rest_framework import generics, permissions,status
from rest_framework.response import Response
from api.utils import StandardResultsSetPagination
from .models import User
from .serializers import *

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Custom success message
        return Response({"message": "User has been created"}, status=status.HTTP_201_CREATED, headers=headers)

class UserDetailsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer

    def get_object(self):
        return self.request.user

class UserReferralsView(generics.ListAPIView):
    serializer_class = ReferralSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(referred_by=user)