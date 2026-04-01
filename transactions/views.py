import logging
from rest_framework import viewsets, status, parsers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.db.models import Q
from .models import Booking, PaymentProof
from .serializers import BookingSerializer, PaymentProofSerializer
from kosts.models import Room

logger = logging.getLogger('ngekost.transactions')

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
        if self.request.user.role != 'tenant':
            logger.warning(
                'Pembuatan booking ditolak karena peran pengguna tidak sesuai.',
                extra={'user_id_target': self.request.user.id, 'role_target': self.request.user.role},
            )
            raise PermissionDenied("Hanya tenant yang dapat membuat booking.")

        with transaction.atomic():
            requested_room = serializer.validated_data['room']
            room = Room.objects.select_for_update().get(pk=requested_room.pk)

            if room.status != 'available':
                logger.warning(
                    'Pembuatan booking ditolak karena kamar tidak tersedia.',
                    extra={'room_id': room.id, 'status_kamar': room.status},
                )
                raise ValidationError({"room": "Kamar ini tidak tersedia untuk dipesan."})

            booking = serializer.save(tenant=self.request.user, room=room)
            room.status = 'booked'
            room.save()
            logger.info(
                'Booking baru berhasil dibuat.',
                extra={
                    'booking_id': booking.id,
                    'room_id': room.id,
                    'tenant_id': self.request.user.id,
                    'status_booking': booking.status,
                },
            )

    @action(detail=True, methods=['post'], parser_classes=[parsers.MultiPartParser, parsers.FormParser])
    def upload_payment(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.tenant:
            logger.warning(
                'Unggah bukti pembayaran ditolak karena pengguna bukan tenant pemilik booking.',
                extra={'booking_id': booking.id, 'tenant_id': booking.tenant_id},
            )
            return Response({"pesan": "Anda tidak berhak mengakses transaksi ini."}, status=status.HTTP_403_FORBIDDEN)

        serializer = PaymentProofSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            locked_booking = Booking.objects.select_for_update().get(pk=booking.pk)

            if locked_booking.status != 'pending_payment':
                logger.warning(
                    'Unggah bukti pembayaran ditolak karena status booking tidak valid.',
                    extra={'booking_id': locked_booking.id, 'status_booking': locked_booking.status},
                )
                return Response(
                    {"pesan": "Transaksi ini tidak dalam status menunggu pembayaran."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            payment_proof = serializer.save(booking=locked_booking)
            locked_booking.status = 'waiting_verification'
            locked_booking.save()
            logger.info(
                'Bukti pembayaran berhasil diunggah.',
                extra={
                    'booking_id': locked_booking.id,
                    'payment_proof_id': payment_proof.id,
                    'status_booking': locked_booking.status,
                },
            )

        return Response({
            "pesan": "Bukti pembayaran berhasil diunggah. Menunggu verifikasi owner.",
            "data": serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def verify_payment(self, request, pk=None):
        booking = self.get_object()

        if request.user != booking.room.kost.owner:
            logger.warning(
                'Verifikasi pembayaran ditolak karena pengguna bukan pemilik kost.',
                extra={'booking_id': booking.id, 'owner_id_seharusnya': booking.room.kost.owner_id},
            )
            return Response({"pesan": "Hanya pemilik kost yang dapat memverifikasi."}, status=status.HTTP_403_FORBIDDEN)
        
        if booking.status != 'waiting_verification':
            logger.warning(
                'Verifikasi pembayaran ditolak karena status booking tidak siap diverifikasi.',
                extra={'booking_id': booking.id, 'status_booking': booking.status},
            )
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
                logger.warning(
                    'Verifikasi pembayaran ditolak karena parameter aksi tidak valid.',
                    extra={'booking_id': booking.id, 'aksi': action_type},
                )
                return Response({"pesan": "Parameter 'action' harus bernilai 'approve' atau 'reject'."}, status=status.HTTP_400_BAD_REQUEST)
            
            booking.save()
            room.save()
            logger.info(
                'Verifikasi pembayaran berhasil diproses.',
                extra={
                    'booking_id': booking.id,
                    'aksi': action_type,
                    'status_booking': booking.status,
                    'status_kamar': room.status,
                },
            )

        return Response({"pesan": pesan, "status_baru": booking.status})