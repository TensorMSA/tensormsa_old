require('es6-promise').polyfill();
require('isomorphic-fetch');

import EnvConstants from './../constants/EnvConstants';

function Api() {

}

Api.prototype.get = function (url, params) {
    console.log(EnvConstants.getApiServerUrl() + url + params)
    return fetch(
        EnvConstants.getApiServerUrl() + url + params,
        {
            method: 'GET',
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }
    ).then(function(response) {
        return response.json();
    }).then(function(json) {
        return json;
    }).catch(function(e) {
        console.log("An Error has occurred" + e);
    });
};

Api.prototype.post = function (url, params) {
    console.log(EnvConstants.getApiServerUrl());
    return fetch(
        EnvConstants.getApiServerUrl() + url,
        {
            method: 'POST',
            body: JSON.stringify(params),
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }
    ).then(function(response) {
        return response.json();
    }).then(function(json) {
        return json;
    }).catch(function(e) {
        console.log("An Error has occurred :" +e);
    });
};

Api.prototype.put = function (url, params) {
    console.log(EnvConstants.getApiServerUrl());
    return fetch(
        EnvConstants.getApiServerUrl() + url,
        {
            method: 'PUT',
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

Api.prototype.delete = function (url, params) {
    console.log(EnvConstants.getApiServerUrl());
    return fetch(
        EnvConstants.getApiServerUrl() + url,
        {
            method: 'DELETE',
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