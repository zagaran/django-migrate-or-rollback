# django-migrate-or-rollback

While single migrations in Django are atomic (as long as they have the default `atomic=True`),
a group of migrations are not.  Thus, when running migrations, you can have a partial
failure where some but not all of your migrations succeed.  This library fixes that.

This library provides a new management command `migrate_or_rollback`.  It's a drop-in
replacement for the Django builtin management command `migrate`.  Here's how it works:

1. Checks your database and current migration files for the latest migrations run per Django app.
2. Runs migrations as normal.
3. If migrations fail, it rolls back to the migrations identified in step 1.

## Instalation

`pip install django-migrate-or-rollback`

Alternatively, add `django-migrate-or-rollback` to your requirements.txt file.

Then, add `"django_migrate_or_rollback"` to your `INSTALLED_APPS` in settings.py, like so:

```
# settings.py
INSTALLED_APPS = [
    # ...
    "django_migrate_or_rollback",
]
```

## Usage

Run `python manage.py migrate_or_rollback` instead of the standard `migrate` command.

In particular, you should use `migrate_or_rollback` in place of `migrate` in your deployment scripts or CI/CD system.

`migrate_or_rollback` has all of the same options as `migrate`, such as the `--noinput` flag.


## Warning

This library assumes that your migrations are reversable.  Not all migrations are reversible.  Additionally, rolling back migrations only reverses schema doesn't rewind the database contents.

In particular:
* Deleted data (such as dropping columns or tables) won't be restored by rolling
back the migration that deletes it.  To avoid this, you should make fields
nullable in one deploy and delete them in the next.
* `RunPython` statements that are missing a `reverse` function will error on
rollback.  At a minimum, add `migrations.RunPython.noop` as a reverse function.
Additionally, RunPython reverse functions can be used to rewind changes to
database contents on migration rollback.
* A migration that deletes a non-nullable field will error on rollback.
To avoid this, make the field nullable in one deploy and delete it in the next.

