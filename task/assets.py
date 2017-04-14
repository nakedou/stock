from invoke import ctask as task


@task
def compile(ctx, **kwargs):
    ctx.run('node_modules/gulp/bin/gulp.js ci')
