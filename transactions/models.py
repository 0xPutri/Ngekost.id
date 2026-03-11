from django.db import models
from django.contrib.auth import get_user_model
from kosts.models import Room

User = get_user_model()

class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending_payment', 'Menunggu Pembayaran'),
        ('waiting_verification', 'Menunggu Verifikasi'),
        ('paid', 'Lunas'),
        ('rejected', 'Ditolak'),
    )

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    start_date = models.DateField()
    duration_months = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending_payment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} - {self.tenant.username} - {self.room.room_number}"
    
    def save(self, *args, **kwargs):
        if not self.total_price and self.room:
            self.total_price = self.room.price * self.duration_months
        super().save(*args, **kwargs)

class PaymentProof(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment_proof')
    image = models.ImageField(upload_to='payments/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bukti Pembayaran - Booking #{self.booking.id}"