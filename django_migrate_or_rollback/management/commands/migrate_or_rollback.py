from django.db.migrations.recorder import MigrationRecorder
from django.db.migrations.loader import MigrationLoader
from django.core.management import call_command
from django.conf import settings
from django.core.management.commands import migrate
from django.db import connections

from pprint import pprint


class Command(migrate.Command):
    def handle(self, *args, **options):
        db = options.get('database')
        connection = connections[db]
        connection.prepare_database()
        loader = MigrationLoader(connection, ignore_no_migrations=True)
        loader.applied_migrations
        
        extant_migrations = {k[0]: v for k, v in loader.applied_migrations.items() if k in loader.graph.nodes}
        last_migrations = {}
        for app, migration in extant_migrations.items():
            if app not in last_migrations or migration.applied > last_migrations[app].applied:
                last_migrations[app] = migration
        last_migration_names = {app: migration.name for app, migration in last_migrations.items()}
        
        try:
            super().handle(*args, **options)
        except Exception:
            print("\n\nMigrating failed; rolling back to last migration state:\n")
            pprint(last_migration_names)
            print()
            for app, migration_name in last_migration_names.items():
                call_command("migrate", app, migration_name)
            print("\Rollback successful\n")
            raise
