import os

from invoke import ctask


def get_project_root(path=__file__):
    directory = os.path.dirname(path)

    while directory != '/':
        p = os.path.join(directory, 'requirements.txt')
        if os.path.isfile(p):
            return directory
        else:
            directory = os.path.dirname(directory)

    return None


def _exec_db_task(ctx, command):
    migration_dir = os.path.join(get_project_root(__file__), os.path.pardir, 'stock-migrations')

    ctx.run('cd {} && ./run.sh alembic {}'.format(migration_dir, command))


@ctask
def migrate(ctx):
    _exec_db_task(ctx, 'upgrade head')


@ctask
def downgrade(ctx, revision):
    _exec_db_task(ctx, 'downgrade {}'.format(revision))
