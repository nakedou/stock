from app.api.response_helper import success
from app.models import StockHolder
from . import bp


@bp.route('/holders-rank', methods=['GET'])
def get_holders_rank():
    stocks = StockHolder.query.all()

    return success({'a': len(stocks)})
