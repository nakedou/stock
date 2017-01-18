require('angular')
require('angular-route')

angular.module('common', ['ngRoute'])
    .config(($interpolateProvider) ->
        $interpolateProvider.startSymbol "[["
        $interpolateProvider.endSymbol "]]"
    )