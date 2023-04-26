# myapp/management/commands/init_db.py
from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Initializes the database by running 'makemigrations', 'migrate', and 'loaddata' commands."

    def handle(self, *args, **options):
        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", "initial_data")  # Replace with your fixture name
        self.stdout.write(self.style.SUCCESS("Database successfully initialized."))