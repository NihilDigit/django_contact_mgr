from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class User(AbstractUser):
    user_id = models.CharField(max_length=10, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['user_id', 'email']

    def __str__(self):
        return self.username


class Contact(models.Model):
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
    ]

    ct_id = models.CharField(max_length=10, primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ct_name = models.CharField(max_length=100)
    ct_phone = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', '请输入11位手机号码。')]
    )
    is_blocked = models.BooleanField(default=False)

    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='contact_avatars/', null=True, blank=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ct_name


class Todo(models.Model):
    contact = models.ForeignKey(Contact, related_name='todos', on_delete=models.CASCADE)
    event = models.CharField(max_length=200)
    time = models.DateTimeField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.event} - {self.time}"