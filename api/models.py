import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username          = models.CharField(verbose_name="username", max_length = 25, unique=True)
    email             = models.EmailField(verbose_name='email address', max_length=60, unique=True)
    referral_code     = models.CharField(max_length=50, unique=True, null=True, blank=True)
    referred_by       = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    registration_date = models.DateTimeField(auto_now_add=True)
    groups            = models.ManyToManyField('auth.Group',verbose_name='groups',blank=True,help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',related_name="custom_user_set", related_query_name="custom_user",)
    user_permissions  = models.ManyToManyField('auth.Permission',verbose_name='user permissions',blank=True,help_text='Specific permissions for this user.',related_name="custom_user_set",  related_query_name="custom_user",)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            # Generate a unique referral code
            self.referral_code = str(uuid.uuid4())[:8]  # Simple example
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
