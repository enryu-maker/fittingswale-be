from django.db import connection

def delete_migration_records(app_name):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM django_migrations WHERE app=%s", [app_name])

# Usage
delete_migration_records('accounts')
