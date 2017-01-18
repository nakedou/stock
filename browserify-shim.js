// related file: assets/js/vendor.coffee

exports.vendorShims = {
    jquery: {
        path: 'bower_components/jquery/dist/jquery.js',
        exports: '$'
    },
    angular: {
        path: 'bower_components/angular/angular.js',
        exports: 'angular',
        depends: {
            jquery: '$'
        }
    },
    'angular-route': {
        path: 'bower_components/angular-route/angular-route.js',
        exports: null,
        depends: {
            angular: 'angular'
        }
    },
    'moment': {
        path: 'bower_components/moment/min/moment.min.js',
        exports: 'moment'
    },
    toastr: {
        path: 'bower_components/toastr/toastr.js',
        exports: null
    },
    'jquery-ui': {
        path: 'bower_components/jquery-ui/jquery-ui.js',
        exports: null
    }
};

exports.vendorExternals = Object.keys(exports.vendorShims);