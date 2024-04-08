from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/', UserDetailsView.as_view(), name='user-details'),
    path('referrals/', UserReferralsView.as_view(), name='referrals'),
]