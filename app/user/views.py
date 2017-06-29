from flask import render_template

from app.user import bp


@bp.route('/readme', methods=['GET'])
def readme():
    return render_template('user/about_me.html')