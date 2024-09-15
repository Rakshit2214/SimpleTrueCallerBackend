import random
from django.core.management.base import BaseCommand
from contact_validation_api.models import AuthDetailStore, RegisteredAppUser, ContactStoreBO
from contact_validation_api.serializers import AuthDetailStoreSerializer, RegisteredAppUserSerializer, ContactStoreBOSerializer


class Command(BaseCommand):
    help = 'Populates the database with sample data'
    registered_entries = 100
    contact_entries = 300

    def handle(self, *args, **options):
        usernames = [f"user{i}" for i in range(self.registered_entries)]
        passwords = [f"pass{i}" for i in range(self.registered_entries)]

        for i in range(self.registered_entries):
            username = usernames[i]
            name = f"Name{i}"
            registered_user_number = f"{1000000000 + i}"
            email_id = f"{name}@example.com"
            password = passwords[i]

            serializer = RegisteredAppUserSerializer(data={
                'name': name,
                'username': {'username': username, 'password': password},
                'registeredUserNumber': registered_user_number,
                'userEmailId': email_id,
            })
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully created {name}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to create {name}: {serializer.errors}'))

        for i in range(self.contact_entries):
            owner_number = f"{1000000000 + random.randint(0, self.registered_entries - 1)}"
            contact_name = f"Contact{i}"
            contact_number = f"{2000000000 + i}"
            contact_email_id = f"{contact_name}@example.com"
            spam_value = round(random.uniform(0, 10), 2)
            is_spam = bool(random.getrandbits(1))

            try:
                owner = RegisteredAppUser.objects.get(registeredUserNumber=owner_number)
                serializer = ContactStoreBOSerializer(data={
                    'registeredContactOwner': owner.id,
                    'ContactName': contact_name,
                    'ContactNumber': contact_number,
                    'ContactEmailId': contact_email_id,
                    'ContactSpamValue': spam_value,
                    'ContactIsSpam': is_spam,
                })
                if serializer.is_valid():
                    serializer.save()
                    self.stdout.write(self.style.SUCCESS(f'Successfully created contact for {owner.name}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to create contact for {owner.name}: {serializer.errors}'))
            except RegisteredAppUser.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Owner with number {owner_number} does not exist'))
