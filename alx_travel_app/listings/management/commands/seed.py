from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from listings.models import Listing

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **options):
        # Ensure we have at least one host user
        host, created = User.objects.get_or_create(
            username="demo_host",
            defaults={"email": "host@example.com", "password": "password123"},
        )

        listings_data = [
            {
                "title": "Cozy Apartment in Nairobi",
                "description": "A nice apartment in the city center",
                "price_per_night": 5000.00,
                "location": "Nairobi",
                "host": host,
            },
            {
                "title": "Beach House in Mombasa",
                "description": "Beautiful beachside property",
                "price_per_night": 12000.00,
                "location": "Mombasa",
                "host": host,
            },
            {
                "title": "Safari Lodge in Maasai Mara",
                "description": "Experience the wild in comfort",
                "price_per_night": 15000.00,
                "location": "Maasai Mara",
                "host": host,
            },
        ]

        for data in listings_data:
            Listing.objects.get_or_create(
                title=data["title"], defaults=data
            )

        self.stdout.write(
            self.style.SUCCESS("Successfully seeded sample listings")
        )
