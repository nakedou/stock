var gulp = require('gulp')
var coffee = require('gulp-coffee')
var gutil = require('gulp-util')
var sass = require('gulp-sass')
var minifyCss = require('gulp-minify-css');
var gif = require('gulp-if');
var bless = require('gulp-bless');


var isProductionMode = false;


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

gulp.task('default', function() {
    gulp.series(
        'coffeeifyjs',
        'css'
    )
});