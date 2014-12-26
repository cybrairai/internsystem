(function() {
    'use strict';

    var module = angular.module('cyb.varer', [
        'ui.router',
        'ngResource',
        'react'
    ]);

    module.config(function ($resourceProvider) {
        $resourceProvider.defaults.stripTrailingSlashes = false;
    });

})();