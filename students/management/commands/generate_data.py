from django.core.management.base import BaseCommand

from faker import Faker

from students.models import Student, Group

import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])
        
        groups = list(Group.objects.all())
        
        for _ in range(10):
            Student.objects.create(
                name = fake.name(),
                group = random.choice(groups)
            )