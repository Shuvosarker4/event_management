import os
import django
from faker import Faker
from random import choice, randint
from datetime import date, timedelta, time

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

# Import models
from events.models import Category, Participant, Event

# Initialize Faker
fake = Faker()

# Create Categories
def create_categories():
    for _ in range(5):  # Create 5 categories
        Category.objects.create(
            name=fake.word().capitalize(),
            description=fake.paragraph()
        )
    print("Categories created!")

# Create Participants
def create_participants():
    for _ in range(20):  # Create 20 participants
        Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
    print("Participants created!")

# Create Events
def create_events():
    categories = Category.objects.all()
    participants = Participant.objects.all()
    
    if not categories or not participants:
        print("Ensure categories and participants exist before creating events.")
        return

    for _ in range(10):  # Create 10 events
        event = Event.objects.create(
            name=fake.sentence(nb_words=4),
            description=fake.paragraph(),
            date=fake.date_between(start_date=date.today(), end_date=date.today() + timedelta(days=365)),
            time=fake.time(),
            location=fake.address(),
            category=choice(categories)
        )
        # Add random participants to the event
        event.participant.set(fake.random_elements(participants, length=randint(5, 15), unique=True))
        event.save()

    print("Events created!")

# Run the script
if __name__ == "__main__":
    create_categories()
    create_participants()
    create_events()
    print("Database populated successfully!")
