var glob = require("glob")
var gulp = require('gulp')
var coffee = require('gulp-coffee')
var rename = require('gulp-rename');
var gutil = require('gulp-util')
var uglify = require('gulp-uglify');
var browserify = require('gulp-browserify');
var sass = require('gulp-sass')
var minifyCss = require('gulp-minify-css');
var gif = require('gulp-if');
var bless = require('gulp-bless');
var exec = require('child_process').exec;
var workerFarm = require('worker-farm');

var assetUtil = require('./asset-util.js');
var shimConfig = require('./browserify-shim.js');


var isProductionMode = false;


gulp.task('clean', function (done) {
    exec('rm -rf  app/static/*  build/coffeeify', function(err, stdout, stderr) {
        if (err) throw err;
        done();
    });
});

var coffeeCompiled = false;
gulp.task('coffeeifyjs', function (done) {
    if(!coffeeCompiled){
        coffeeCompiled = true;
        return gulp.src('assets/js/**/*.coffee')
            .pipe(coffee({bare: true}).on('error', gutil.log))
            .pipe(gulp.dest('build/coffeeify/js'))
    }else{
        done();
    }
});

gulp.task('vendorjs', ['coffeeifyjs'], function browserifyVendorjs () {
    return gulp.src(['build/coffeeify/js/vendor.js'])
        .pipe(browserify({
            insertGlobals: false,
            debug: !isProductionMode,
            shim: shimConfig.vendorShims
        }))
        .pipe(gif(isProductionMode, uglify()))
        .pipe(gulp.dest('app/static/js'));
});

gulp.task('appjs', ['coffeeifyjs'], function browserifyAppjs (done) {
    var workers = workerFarm(require.resolve('./asset-util.js'), ['compileSingleScript']);
    var entries = glob.sync('build/coffeeify/js/**/main-*.js'), count = 0;
    entries.forEach(function(entry) {
        workers.compileSingleScript(entry, 'app/static/js', {
            debug: !isProductionMode,
            rename: entry.replace("build/coffeeify/js/", "")
        }, function() {
            count = count + 1;
            if (count === entries.length) {
                workerFarm.end(workers);
                done();
            }
        });
    });
});

gulp.task('image', function(done) {
   gulp.src('assets/images/**/*').pipe(gulp.dest('app/static/images'))
});

gulp.task('css', function sassToCss(done) {
    var cssStream = gulp.src('assets/scss/**/*.scss')
        .pipe(sass({errLogToConsole: true, sourceComments: !isProductionMode ? 'map' : null}));

    if(isProductionMode){
        cssStream = cssStream.pipe(gif(isProductionMode, minifyCss({keepSpecialComments: 0})))
        .pipe(bless({cacheBuster: true, imports: true}))
    }
    cssStream.pipe(gulp.dest('app/static/css'));

    return cssStream;
});

gulp.task('watchScss', function (done) {
    gulp.watch('assets/scss/**/*.scss', ['css']);
    done();
});

gulp.task('watchCoffee', function (done) {
    gulp.watch('assets/js/**/*.coffee', ['appjs']);
    done();
});

gulp.task('watch', ['watchScss', 'watchCoffee'])

gulp.task('server', function(done) {
    assetUtil.startServer({
        'assetsDir': 'assets',
        'port': 8888
    });
    done();
});

gulp.task('default', ['clean', 'vendorjs', 'appjs', 'image', 'css', 'server', 'watch']);