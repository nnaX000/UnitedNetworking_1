from django.core.management.base import BaseCommand
from mainPage.models import Reservation

class Command(BaseCommand):
    help = 'Check all reservations and update expiration status'

    def handle(self, *args, **kwargs):
        reservations = Reservation.objects.filter(is_expired=False)
        print(reservations)
        for reservation in reservations:
            reservation.update_expiration_status()
        self.stdout.write(self.style.SUCCESS('Successfully updated reservations expiration status.'))
