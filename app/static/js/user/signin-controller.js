angular.module('stock', []).controller('signinCtrl', function($scope) {
    $scope.user = {username: '', password: '', remember: false}
    $scope.signin = function() {
        console.log($scope.user)
    }
});