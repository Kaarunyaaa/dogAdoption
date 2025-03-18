from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='user')
    phNo = models.CharField(max_length=15, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True) 
    is_verified = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if self.user_type == 'admin':
            self.is_staff = True  # Admin users should have staff privileges
        else:
            self.is_staff = False  # Regular users should not have staff privileges
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


class Dog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    dog_name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    vaccinated = models.BooleanField(default=False)
    training = models.BooleanField(default=False)
    reason = models.TextField()

    dog_image = models.ImageField(upload_to="dog_images/", null=True, blank=True)
    is_rehomed = models.BooleanField(default=False)  # Track adoption status
    created_at = models.DateTimeField(auto_now_add=True)  # Store post time
    verification = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.dog_name} ({self.breed})"


class AdoptionRequest(models.Model):
    adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="adoption_requests")
    dog = models.ForeignKey("Dog", on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dog_owners")
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Accepted", "Accepted"), ("Rejected", "Rejected")], default="Pending")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Adoption Request: {self.adopter} for {self.dog}"
    
    

from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    adoption_request = models.OneToOneField('AdoptionRequest', on_delete=models.CASCADE, related_name='chat_room')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat Room for {self.adoption_request}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')  # ✅ Add this field
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
