from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from services.models import Service
from stylists.models import Stylist
from appointments.models import Appointment
from rest_framework.test import APIClient
from rest_framework import status

class AppointmentTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(username='customer', email='cust@test.com', password='password', role='customer')
        self.staff = User.objects.create_user(username='staff', email='staff@test.com', password='password', role='staff')
        self.service = Service.objects.create(name='Haircut', price=100, duration=60)
        self.stylist = Stylist.objects.create(user=self.staff, nickname='John Do')
        self.client = APIClient()

    def test_create_appointment_success(self):
        self.client.force_authenticate(user=self.customer)
        start_time = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        data = {
            'service': self.service.id,
            'stylist': self.stylist.id,
            'start_time': start_time.isoformat()
        }
        res = self.client.post('/appointments/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_create_appointment_overlap(self):
        self.client.force_authenticate(user=self.customer)
        start_time = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0) + timedelta(days=1)
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            stylist=self.stylist,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=60),
            status='confirmed'
        )
        
        data = {
            'service': self.service.id,
            'stylist': self.stylist.id,
            'start_time': (start_time + timedelta(minutes=30)).isoformat()
        }
        res = self.client.post('/appointments/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_working_hours_validation(self):
        self.client.force_authenticate(user=self.customer)
        # Attempt to book at 7 AM
        start_time = timezone.now().replace(hour=7, minute=0, second=0, microsecond=0) + timedelta(days=1)
        data = {
            'service': self.service.id,
            'stylist': self.stylist.id,
            'start_time': start_time.isoformat()
        }
        res = self.client.post('/appointments/', data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cancel_appointment(self):
        self.client.force_authenticate(user=self.customer)
        start_time = timezone.now() + timedelta(days=2)
        appt = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            stylist=self.stylist,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=60),
            status='confirmed'
        )
        res = self.client.put(f'/appointments/{appt.id}/cancel/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        appt.refresh_from_db()
        self.assertEqual(appt.status, 'cancelled')
