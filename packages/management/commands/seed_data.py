import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from packages.models import Destination, TourPackage, Review
from bookings.models import Booking

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with initial destinations, packages, users, and reviews."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        
        # 1. Create Users
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@aethervoyage.com",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True
            }
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write("Created admin user (pw: admin123)")

        staff_user, created = User.objects.get_or_create(
            username="staff",
            defaults={
                "email": "staff@aethervoyage.com",
                "role": "staff",
                "is_staff": True
            }
        )
        if created:
            staff_user.set_password("staff123")
            staff_user.save()
            self.stdout.write("Created staff user (pw: staff123)")

        customer_user, created = User.objects.get_or_create(
            username="customer",
            defaults={
                "email": "customer@aethervoyage.com",
                "role": "customer"
            }
        )
        if created:
            customer_user.set_password("customer123")
            customer_user.save()
            self.stdout.write("Created customer user (pw: customer123)")

        # 2. Create Destinations
        dest_kyoto, created = Destination.objects.get_or_create(
            name="Kyoto",
            defaults={
                "location": "Japan",
                "description": "The historical heart of Japan, famous for its classical Buddhist temples, gardens, imperial palaces, Shinto shrines, and traditional wooden houses."
            }
        )
        if created:
            try:
                dest_kyoto.image.name = "destinations/kyoto.png"
                dest_kyoto.save()
            except Exception as e:
                self.stdout.write(f"Could not attach Kyoto image: {e}")
            self.stdout.write("Created Kyoto destination")

        dest_alps, created = Destination.objects.get_or_create(
            name="Swiss Alps",
            defaults={
                "location": "Switzerland",
                "description": "High mountain peaks, green pastures, and crystal-clear lakes. Perfect for hiking, alpine fresh air, and picturesque villages."
            }
        )
        if created:
            try:
                dest_alps.image.name = "destinations/alps.png"
                dest_alps.save()
            except Exception as e:
                self.stdout.write(f"Could not attach Alps image: {e}")
            self.stdout.write("Created Swiss Alps destination")

        # 3. Create Packages
        pkg_kyoto, created = TourPackage.objects.get_or_create(
            title="Autumn in Kyoto",
            defaults={
                "destination": dest_kyoto,
                "description": "Experience the stunning autumn leaves of Kyoto. Visit the iconic Fushimi Inari Shrine, walk through Arashiyama bamboo forest, and taste authentic multi-course kaiseki dining.\n\nIncludes 3-star boutique hotel lodging, daily guided walks, and local transit passes.",
                "price": 1450.00,
                "duration_days": 6,
                "start_date": datetime.date.today() + datetime.timedelta(days=30),
                "end_date": datetime.date.today() + datetime.timedelta(days=36),
                "max_slots": 12,
                "available_slots": 10,
                "is_active": True
            }
        )
        if created:
            try:
                pkg_kyoto.image.name = "destinations/kyoto.png"
                pkg_kyoto.save()
            except Exception as e:
                pass
            self.stdout.write("Created Kyoto Autumn Package")

        pkg_alps, created = TourPackage.objects.get_or_create(
            title="Alpine Hiking Adventure",
            defaults={
                "destination": dest_alps,
                "description": "A breathtaking guided hike through the valleys of Lauterbrunnen and Zermatt. Enjoy clean mountain air, rustic chalet lodging, and traditional Swiss fondue under the shadow of the Matterhorn.",
                "price": 2100.00,
                "duration_days": 8,
                "start_date": datetime.date.today() + datetime.timedelta(days=45),
                "end_date": datetime.date.today() + datetime.timedelta(days=53),
                "max_slots": 8,
                "available_slots": 8,
                "is_active": True
            }
        )
        if created:
            try:
                pkg_alps.image.name = "destinations/alps.png"
                pkg_alps.save()
            except Exception as e:
                pass
            self.stdout.write("Created Alpine Hiking Package")

        # 4. Create Reviews
        Review.objects.get_or_create(
            package=pkg_kyoto,
            user=customer_user,
            defaults={
                "rating": 5,
                "comment": "Absolutely magical! The Kyoto autumn colors are unmatched, and the guide's knowledge of quiet temples made all the difference."
            }
        )
        self.stdout.write("Created test review for Kyoto package")

        self.stdout.write("Database seeding complete!")
