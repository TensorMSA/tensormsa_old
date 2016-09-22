require('es6-promise').polyfill();
require('isomorphic-fetch');

import EnvConstants from './../constants/EnvConstants';

function Api() {

}

Api.prototype.get = function (url) {
    return fetch(EnvConstants.getApiServerUrl() + url).then(function(response) {
        return response.json();
    }).then(function(json) {
        return json;
    }).catch(function() {
        console.log("An Error has occurred");
    });
};

Api.prototype.post = function (url, params) {
    console.log(EnvConstants.getApiServerUrl());
    return fetch(
        EnvConstants.getApiServerUrl() + url,
        {
            method: 'post',
            body: JSON.stringify(params),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }
    ).then(function(response) {
        return response.json();
    }).then(function(json) {
        return json;
    }).catch(function() {
        console.log("An Error has occurred");
    });
};

export default Api;