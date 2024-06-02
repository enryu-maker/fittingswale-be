# reset_migrations_app/management/commands/reset_migrations.py

from django.core.management.base import BaseCommand
from django.db import connection

def delete_migration_records(app_name):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app=%s", [app_name])

class Command(BaseCommand):
    help = 'Delete migration records for a specific app'

    def handle(self, *args, **options):
        app_name = 'accounts'
        delete_migration_records(app_name)
        self.stdout.write(self.style.SUCCESS('Migration records deleted for app "%s"' % app_name))
