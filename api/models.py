from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone_number = PhoneNumberField()
    email = models.EmailField(blank=True, null=True)

    class Meta:
        unique_together = ['user', 'phone_number']

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class SpamReport(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spam_reports')
    phone_number = PhoneNumberField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['reported_by', 'phone_number']

    def __str__(self):
        return f"Spam report for {self.phone_number}"