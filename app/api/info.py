from app.api.response_helper import success
from . import bp


@bp.route('/info/holders-rank', methods=['GET'])
def get_info():
    return success({})
