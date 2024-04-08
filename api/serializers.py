from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    referred_by = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='referral_code', required=False)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'referral_code', 'referred_by')

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'referral_code', 'date_joined')

class ReferralSerializer(serializers.ModelSerializer):
    registration_date = serializers.DateTimeField(source='date_joined', read_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'registration_date', 'referral_code')