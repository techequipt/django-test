import os
import json
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from django_test.users.models import User
from django_test.real_estates.models import Property

class Command(BaseCommand):
    help = 'Seed data from seed_test_data.json for a quick check'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Start seeding'))
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        seed_file_path = os.path.join(current_dir_path, 'seed_real_estates.json')

        # Load seed data json file
        with open(seed_file_path) as json_file:
            seed_data = json.load(json_file)
            seed_users = seed_data['users']
            seed_properties = seed_data['properties']
        self.stdout.write(self.style.SUCCESS('Loaded seed data'))

        # Seed into DB, with rollback on errors
        try:
            with transaction.atomic():
                user_ids = []
                self.stdout.write(self.style.NOTICE('Seeding users'))
                for seed_user in seed_users:
                    existing_user = User.objects.filter(email=seed_user['email']).first()

                    if existing_user:
                        user_ids.append(existing_user.id)
                        continue

                    seed_user['password'] = make_password(seed_user['password'])
                    new_user = User.objects.create(**seed_user)
                    user_ids.append(new_user.id)
                    self.stdout.write(self.style.SUCCESS(f"Created user {seed_user['email']}"))

                self.stdout.write(self.style.WARNING('Cleaning up old properties for these users'))
                Property.objects.filter(created_by_id__in=user_ids).delete()

                self.stdout.write(self.style.NOTICE('Seeding properties'))
                for seed_property in seed_properties:
                    # in case user_ids are not 1 and 2 for 1 represents first user id, 2 for second user id
                    seed_property['created_by_id'] = user_ids[seed_property['created_by_id'] - 1]
                    Property.objects.create(**seed_property)
                    self.stdout.write(self.style.SUCCESS(
                        f"Created property {seed_property['address']}"
                        f" for user #{seed_property['created_by_id']}"
                    ))

                self.stdout.write(self.style.SUCCESS('Done seeding'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Rolling back due to error: {e}'))
            transaction.set_rollback(True)
