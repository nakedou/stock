var http = require('http');
var path = require('path');
var fs = require('fs');
var zlib = require('zlib');
var spawn = require('child_process').spawn;
var gulp = require('gulp');
var browserify = require('browserify');
var watchify = require('watchify');
var cachingCoffeeify = require('caching-coffeeify');
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');
var rename = require('gulp-rename');
var extend = require('extend');
var gif = require('gulp-if');
var uglify = require('gulp-uglify');
var shimConfig = require('./browserify-shim.js');

var globalConfig = {};
var compileTasks = {};

function compileSingleScript(entry, outputDir, options, callback){
    var config = extend({
        entries: [entry],
        insertGlobals: false,
        debug: options.debug, // supportSourceMap,
        paths: options.paths || ['./'] // an array of directories that browserify searches when looking for modules which are not referenced using relative path.
    }, options);

    if(options.doCoffeeify){
        config.extensions = ['.coffee'];
    }

    options.useWatchMode && extend(config, {
        cache: {},
        packageCache: {},
        fullPaths: true,
        plugin: [watchify],
    });

    var browserifyInstance = browserify(config);
    
    options.doCoffeeify && browserifyInstance.transform(cachingCoffeeify, {
        bare: true
    });

    browserifyInstance.external(shimConfig.vendorExternals);

    if(options.isForTest){
        browserifyInstance.external('angular-mocks');
    }

    var updated = false;
    function bundleEntry(){
        compileTasks[entry] = {
            status: 'pending'
        };

        var timer = 'bundle entry: ' + entry;
        console.time(timer);
        var stream = browserifyInstance.bundle(function(err, content) {
            if (err) {
                console.error('failed to bundle ' + entry , err);
            }

            compileTasks[entry].status = 'finished';
            compileTasks[entry].content = content;
        })
        .pipe(source(entry))
        .pipe(buffer())
        .pipe(gif(!options.debug, uglify({mangle: false})));

        if(outputDir){
            var renameFunction = function(entry){
                return typeof config.rename === 'function' ? config.rename(entry) : config.rename;
            }
            stream.pipe(rename(config.rename ? renameFunction(entry) : entry.replace('assets/js/', '').replace('jstests/', '').replace(/\.coffee$/, '.js')))
                .pipe(gulp.dest(outputDir));
        }

        stream.on('end', function(){
            updated && console.timeEnd(timer);
            callback && callback(entry);
        });

        return stream;
    }

    options.useWatchMode && browserifyInstance.on('update', function(){
        updated = true;
        bundleEntry();
    });
    
    return bundleEntry();
}

module.exports = {
    compileSingleScript: compileSingleScript,

    // browserify && coffeeify && uglify if needed \\
    buildJavaScript: function(coffeeFiles, outputDir, options){
        return coffeeFiles.map(function(entry) {
            return compileSingleScript(entry, outputDir, options);
        });
    },
    
    startServer: function startServer(options) {
        globalConfig = options;
        server.listen(globalConfig.port, '0.0.0.0', 128, function(x){
            console.log('assets server (pid: ' + process.pid + ') started at http://0.0.0.0:' + globalConfig.port);
        });
    }
};

function pollingCompiledContent(file, res){
    if(compileTasks[file].status === 'pending'){
        return setTimeout(pollingCompiledContent.bind(null, file, res), 5);
    }

    if(compileTasks[file].status === 'finished'){
        zlib.gzip(compileTasks[file].content, function(err, content){
            if(err){
                throw err;
            }
            res.writeHead(200, {
                'Content-Encoding': 'gzip',
                'Content-Type': 'application/x-javascript;Charset=UTF-8'
            });
            res.end(content);
        });
    }
}

var server = http.createServer(function(req, res) {
    var file = path.join(globalConfig.assetsDir, req.url.split('?')[0]);
    file = file.replace('/static/', '/').replace(/\.js$/, '.coffee');
    if( !fs.existsSync(file) ){
        res.statusCode = 404;
        return res.end(file + ' does not exists!');
    }

    if(!compileTasks[file]){
        compileSingleScript(file, null, {
            doCoffeeify: true,
            useWatchMode: true
        });
    }

    pollingCompiledContent(file, res);
});

server.on('error', function (e) {
    if (e.code == 'EADDRINUSE') {
        console.log("restart assets server...")
        spawn("/bin/bash", ["-c", "kill -9 $(lsof -t -i:" + globalConfig.port + " -sTCP:LISTEN)"]).on('close', function (code) {
            setTimeout(function(){
                module.exports.startServer(globalConfig);
            }, 1000);
        });
    }
});
