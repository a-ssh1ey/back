from django.db import models
import uuid
from django.utils import timezone

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.telegram_id)

class Deal(models.Model):
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals_created')
    code = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class DealParticipant(models.Model):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals_participated')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return f'{self.user} - {self.role}'

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('released', 'Released'),
    ]

    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.deal} - {self.amount}'
