/**
 * Created by Michael on 08/05/2016.
 */
/* globals darts_app */
darts_app.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
darts_app.controller('ResultFormCtrl', function($scope, $http, $location) {
    $scope.messages = [];
    $scope.submit = function() {
        $http.post($location.absUrl(), $scope.result)
            .success(function(out_data) {
                var fixture_id = $scope.results_form.fixture.$viewValue;
                $('form select option[value="' + fixture_id + '"]').remove();
                $scope.messages.push(out_data.message);
            });
    };
});