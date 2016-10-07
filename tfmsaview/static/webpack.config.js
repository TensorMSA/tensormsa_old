var path = require('path');
var webpack = require('webpack');

var envPlugin = new webpack.DefinePlugin({
    __API_SERVER__: JSON.stringify(process.env.API_SERVER)
});

module.exports = {
    entry: {
        TensorMSA: './js/app.js',
        playground: './ts/playground.ts'
    }, // Multiple Entry
    devtool: 'sourcemaps',
    cache: true,
    debug: true,
    output: {
        path: __dirname,
        filename: './../static/dist/[name].js' // Output for the multiple entry
    },
    resolve: {
        // Add `.ts` and `.tsx` as a resolvable extension. 
        extensions: ['', '.webpack.js', '.web.js', '.js', '.ts', '.tsx']
    },  
    // When to use Minification, 
    plugins : [
        envPlugin
        //new webpack.optimize.UglifyJsPlugin()
    ]  ,
    module: { // An array of extensions that should be used to resolve modules.
        loaders: [
            { 
                test: /\.jsx?$/,         // Match both .js and .jsx files
                exclude: /node_modules/, 
                loader: "babel", 
                query:
                {
                    presets:['es2015','react']
                }
            },
            {
                // test: A condition that must be met <-> exclude
                test: /\.ts$/,
                exclude: /node_modules/,  
                loader: 'ts-loader'
            }
        ]
    },
    ts : { // set compiler which is used by ts-loader
        compiler : 'typescript'
    }
};
