(function(){
    "use strict";
    var app = angular.module("hillsbook", []);
    app.controller("UsersCtrl", ["$scope", "$http",usersCtrl]);

    function usersCtrl($scope, $http){

        $scope.reloadUsers = function(){
            $http.get('/users/').
                success(function(data) {
                    $scope.users = data.users;
                    $scope.reloadUser();
                });
        };
        $scope.reloadUser = function(){
            $http.get('/users/' + $scope.userId).
            success(function(data) {
                $scope.user = data;
            });
        };
        $scope.loadFriendsTab = function(tab_id){
            alert(tab_id);
        };
        $scope.editUser = function(){
            $scope.newUser = angular.copy($scope.user);
        };

        $scope.savePersonEdit = function(){

            if ($scope.newUser.id){
                // edit user
                $http.put('/users/' + $scope.newUser.id, $scope.newUser)
                    .success(function(data) {
                        $scope.reloadUsers();
                        $scope.dismissDialog();
                    }).error(function(){
                        alert("Data couldn't be saved. Please try again.");
                    });
            } else {
                // add new user
                $http.post('/users/', $scope.newUser)
                    .success(function(data) {
                        $scope.reloadUsers();
                        $scope.dismissDialog();
                    }).error(function(){
                        alert("Data couldn't be saved. Please try again.");
                    });
            }
        };

        $scope.dismissPersonEdit = function(tab_id){
            $scope.newUser = {};
        };

        $scope.reloadUsers();

        $scope.userId = 1;
        $scope.user = {};
        $scope.user_friends = [];
        $scope.user_fof = [];
        $scope.user_suggestions = [];

        $scope.reloadUser();
    }

    app.directive('myModal', function() {
       return {
         restrict: 'A',
         link: function(scope, element, attr) {
           scope.dismissDialog = function() {
               element.modal('hide');
           };
         }
       }
    });
}());