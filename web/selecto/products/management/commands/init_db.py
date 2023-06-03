# myapp/management/commands/init_db.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Initializes the database by running 'makemigrations', 'migrate', and 'loaddata' commands."

    def add_arguments(self, parser):
        # Replace the default with your fixture name
        parser.add_argument('fixture', nargs='?', default='initial_data', help="Specify the fixture to load (default: 'initial_data')")

    def handle(self, *args, **options):
        fixture = options['fixture']

        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", fixture)  
        self.stdout.write(self.style.SUCCESS("Database successfully initialized."))