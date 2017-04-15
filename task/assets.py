from invoke import ctask


@ctask
def compile(ctx, **kwargs):
    ctx.run('node_modules/gulp/bin/gulp.js ci')
