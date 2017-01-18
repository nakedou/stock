moment = require('moment')

module.exports = ['$scope', '$q', ($scope, $q) ->
    startDate = moment().subtract(30, 'days').format('YYYY-MM-DD')
    endDate = moment().format('YYYY-MM-DD')

    $scope.ui = {
        pageIndex: 1
    }

    $scope.changePage = (pageIndex) ->
        $scope.ui.pageIndex = pageIndex
        requestStocks()

    sendRequest = (defer) ->
        $.ajax({
            url: 'http://lhb.ipail.com/w8/api/index.php'
            type: 'POST'
            data: {
                c: 'YiDianCangWei'
                a: 'GuDongRenShu'
                StratDate: startDate
                EndDate: endDate
                Order:  1
                Tag: 0
                Index: ($scope.ui.pageIndex-1) * 9
            }
            success: (res) ->
                result = JSON.parse(res)
                defer.resolve result.List
            error: ->
                defer.resolve []
        })

    requestStocks = ->
        deferStocks = $q.defer()
        sendRequest(deferStocks)
        deferStocks.promise.then((stocks) ->
            $scope.stocks = stocks
        )

    requestStocks()

]