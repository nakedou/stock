from os.path import expanduser

from invoke import ctask

from task.db import get_project_root


def remove_useless_files(ctx, app_dir):
    ctx.run('python -m compileall {}/app'.format(app_dir))
    ctx.run("""bash -c '
    cd {}/app
    for pyc in $(find . -name "*.pyc"); do
        new_pyc=$(echo $pyc|sed s#__pycache__/##|sed s#.cpython-34##)
        mv $pyc $new_pyc
    done
    '""".format(app_dir))
    ctx.run('find {}/app -name "*.py" -delete'.format(app_dir))


@ctask
def docker(ctx, p='app'):
    project_root = get_project_root()
    user_home = expanduser('~')
    package_name = p

    build_root = '{project_root}'.format(**locals())
    app_dir = '{build_root}/docker/app'.format(**locals())
    pip = '{app_dir}/virtualenv/bin/pip'.format(**locals())

    ctx.run('cp -r app run_with_tornado.py {app_dir}/'.format(**locals()))
    ctx.run('cp -r scripts/ {app_dir}/'.format(**locals()))
    ctx.run('cp -r ngx-runtime/ {app_dir}/'.format(**locals()))
    remove_useless_files(ctx, app_dir)

    ctx.run('virtualenv -p `which python3.4` --always-copy {app_dir}/virtualenv'.format(**locals()))
    ctx.run('{pip} install -r requirements.txt'.format(**locals()))
