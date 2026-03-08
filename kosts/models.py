from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Kost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kosts')
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    facilities = models.TextField(help_text="Pisahkan dengan koma, misal: WiFi, AC, Kamar Mandi Dalam")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
    

class Room(models.Model):
    STATUS_CHOICES = (
        ('available', 'Tersedia'),
        ('booked', 'Dipesan'),
        ('occupied', 'Dihuni'),
    )

    kost = models.ForeignKey(Kost, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']
        unique_together = ('kost', 'room_number')

    def __str__(self):
        return f"Kamar {self.room_number} - {self.kost.name}"
