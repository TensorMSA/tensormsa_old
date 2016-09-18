var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: './js/app.js',
    devtool: 'sourcemaps',
    cache: true,
    debug: true,
    output: {
        path: __dirname,
        filename: './../dist/TensorMSA.js'
    },
    module: {
        loaders: [
            { 
                test: /\.jsx?$/,         // Match both .js and .jsx files
                exclude: /node_modules/, 
                loader: "babel", 
                query:
                {
                    presets:['es2015','react']
                }
            }
        ]
    }
};
