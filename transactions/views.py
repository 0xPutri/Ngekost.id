from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Q
from .models import Booking, PaymentProof
from .serializers import BookingSerializer, PaymentProofSerializer

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Booking.objects.select_related('room__kost', 'tenant').prefetch_related('payment_proof')

        if user.role == 'tenant':
            return qs.filter(tenant=user)
        elif user.role == 'owner':
            return qs.filter(room__kost__owner=user)
        elif user.role == 'admin':
            return qs.all()
        return qs.none()
    
    def perform_create(self, serializer):
        with transaction.atomic():
            booking = serializer.save(tenant=self.request.user)
            room = booking.room
            room.status = 'booked'
            room.save()

    @action(detail=True, methods=['post'], parser_classes=[parsers.MultiPartParser, parsers.FormParser])
    def upload_payment(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.tenant:
            return Response({"pesan": "Anda tidak berhak mengakses transaksi ini."}, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status != 'pending_payment':
            return Response({"pesan": "Transaksi ini tidak dalam status menunggu pembayaran."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PaymentProofSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(booking=booking)
            booking.status = 'waiting_verification'
            booking.save()
            return Response({"pesan": "Bukti pembayaran berhasil diunggah. Menunggu verifikasi owner.", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        booking = self.get_object()

        if request.user != booking.room.kost.owner:
            return Response({"pesan": "Hanya pemilik kost yang dapat memverifikasi."}, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status != 'waiting_verification':
            return Response({"pesan": "Transaksi belum memiliki bukti pembayaran untuk diverifikasi."}, status=status.HTTP_400_BAD_REQUEST)
        
        action_type = request.data.get('action')

        with transaction.atomic():
            room = booking.room
            if action_type == 'approve':
                booking.status = 'paid'
                room.status = 'occupied'
                pesan = "Pembayaran disetujui. Kamar sekarang dihuni."
            elif action_type == 'reject':
                booking.status = 'rejected'
                room.status = 'available'
                pesan = "Pembayaran ditolak. Pesanan dibatalkan dan kamar kembali tersedia."
            else:
                return Response({"pesan": "Parameter 'action' harus bernilai 'approve' atau 'reject'."}, status=status.HTTP_400_BAD_REQUEST)
            
            booking.save()
            room.save()

        return Response({"pesan": pesan, "status_baru": booking.status})