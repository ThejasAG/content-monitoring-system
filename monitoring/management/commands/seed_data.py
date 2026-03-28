from django.core.management.base import BaseCommand
from django.utils import timezone
from monitoring.models import Keyword, ContentItem

class Command(BaseCommand):
    help = 'Seed the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")
        
        # Create Keywords
        k1, _ = Keyword.objects.get_or_create(name='Django')
        k2, _ = Keyword.objects.get_or_create(name='Python')
        k3, _ = Keyword.objects.get_or_create(name='REST')

        # Create ContentItems
        # Exact title match for 'Django'
        ContentItem.objects.get_or_create(
            title='Django',
            body='Django is a high-level Python web framework.',
            source='Official Site',
            last_updated=timezone.now()
        )
        
        # Partial title match for 'Python'
        ContentItem.objects.get_or_create(
            title='Learning Python Basics',
            body='A great guide for beginners.',
            source='Education',
            last_updated=timezone.now()
        )
        
        # Match in body for 'REST'
        ContentItem.objects.get_or_create(
            title='API Standards',
            body='Representational State Transfer (REST) is an architectural style.',
            source='Tech Blog',
            last_updated=timezone.now()
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded sample data'))
