from django.core.management.base import BaseCommand
from store.models import Stock


class Command(BaseCommand):
    help = 'Updates all stock quantities to 15'

    def handle(self, *args, **options):
        # Update all stock quantities to 15
        updated = Stock.objects.all().update(quantity=15)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated} stock records to quantity 15')
        )
