import os
import django
import random
from faker import Faker # type: ignore

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spam_detector.settings')
django.setup()

from api.models import User, Contact, SpamReport

fake = Faker()

def create_users(num_users=50):
    users = []
    for _ in range(num_users):
        username = fake.user_name()
        phone_number = fake.phone_number()
        email = fake.email()
        user = User.objects.create_user(username=username, phone_number=phone_number, email=email, password='testpass123')
        users.append(user)
    return users

def create_contacts(users, num_contacts=200):
    for _ in range(num_contacts):
        user = random.choice(users)
        name = fake.name()
        phone_number = fake.phone_number()
        email = fake.email()
        Contact.objects.create(user=user, name=name, phone_number=phone_number, email=email)

def create_spam_reports(users, num_reports=100):
    for _ in range(num_reports):
        user = random.choice(users)
        phone_number = fake.phone_number()
        SpamReport.objects.create(reported_by=user, phone_number=phone_number)

if __name__ == '__main__':
    print("Creating users...")
    users = create_users()
    print("Creating contacts...")
    create_contacts(users)
    print("Creating spam reports...")
    create_spam_reports(users)
    print("Database population complete!")