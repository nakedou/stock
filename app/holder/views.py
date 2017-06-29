from flask import render_template

from app.holder import bp


@bp.route('/holder', methods=['GET'])
def holder():
    return render_template('holder/index.html')
