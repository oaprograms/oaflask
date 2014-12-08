(function () {
    "use strict";
    var app = angular.module("hillsbook", ["ui.bootstrap"]);
    app.controller("UsersCtrl", ["$scope", "$http", "$modal", "$log", usersCtrl]);

    function usersCtrl($scope, $http, $modal, $log) {
        var ctrl = this;

        $scope.reloadUsers = function (resetUser) {
            if (typeof(resetUser) === 'undefined')resetUser = false;
            $http.get('/users/').
                success(function (data) {
                    $scope.users = data.users;
                    if (resetUser)$scope.userId = $scope.users[0].id;
                    $scope.reloadUser();
                });
        };
        $scope.reloadUser = function () {
            $http.get('/users/' + $scope.userId).
                success(function (data) {
                    $scope.user = data;
                    $scope.userInfo = {};
                    $scope.reloadUserInfo($scope.tabId);
                    //TODO: set tab to 1
                });
        };
        $scope.searchUsers = function (query) {
            return $http.get('/users/search/' + query)
                .then(function (response) {
                    return response.data.users;
                });
        };
        $scope.reloadUserId = function (id) {
//            $scope.searchUserText = null;
            $scope.userId = id;
            $scope.reloadUser();
        };
        $scope.addFriend = function (friend_id) {
            $scope.addFriendId = 0;
            $http.put('/users/' + $scope.userId + '/friends/', {'friend': friend_id}).
                success(function (data) {
                    $scope.tabState='quiet';
                    $scope.reloadUserInfo($scope.tabId);
                });
        };
        $scope.removeFriend = function (friend_id) {
            $http.delete('/users/' + $scope.userId + '/friends/' + friend_id).
                success(function (data) {
                    $scope.tabState='quiet';
                    $scope.reloadUserInfo($scope.tabId);
                });
        };
        $scope.reloadFriends = function (quiet) {
            $http.get('/users/' + $scope.userId + '/friends/').
                success(function (data) {
                    $scope.userInfo.friends = data.users;
                    $scope.tabState = data.users.length ? '' : 'no-info';
                });
        };
        $scope.reloadFof = function (quiet) {
            $http.get('/users/' + $scope.userId + '/fof/').
                success(function (data) {
                    $scope.userInfo.fof = data.users;
                    $scope.tabState = data.users.length ? '' : 'no-info';
                });
        };
        $scope.reloadSuggestions = function (quiet) {
            $http.get('/users/' + $scope.userId + '/suggested/').
                success(function (data) {
                    $scope.userInfo.suggestions = data.users;
                    $scope.tabState = data.users.length ? '' : 'no-info';
                });
        };
        $scope.reloadUserInfo = function (tab_id) {
            $scope.tabId = tab_id;
            if ($scope.userId) {
                if($scope.tabState!='quiet')
                    $scope.tabState = 'loading';
                if ($scope.tabId == 1) {
                    $scope.reloadFriends();
                } else if ($scope.tabId == 2) {
                    $scope.reloadFof();
                } else if ($scope.tabId == 3) {
                    $scope.reloadSuggestions();
                }
            }
        };

        $scope.openUserEditModal = function () {
            $scope.newUser = angular.copy($scope.user);
            $scope.openUserModal();
        };

        $scope.openUserAddModal = function () {
            $scope.newUser = {};
            $scope.openUserModal();
        };

        $scope.openUserModal = function () {
            var modalInstance = $modal.open({
                templateUrl: 'userEditTemplate.html',
                controller: 'EditModalInstanceCtrl',
                resolve: {
                    parentScope: function () {
                        return $scope;
                    }
                }
            });
        };

        $scope.tabId = 1;
        $scope.reloadUsers(true);

        $scope.user = {gender: 'male'};
        $scope.userInfo = {};
//        $scope.reloadUser();


    }

////////////////////////////   Modal ctrl   ////////////////////

    app.controller('EditModalInstanceCtrl', function ($scope, $modalInstance, $http, parentScope) {
        $scope.newUser = parentScope.newUser;
        $scope.editMode = $scope.newUser.hasOwnProperty('id');

        $scope.userDelete = function () {
            if (confirm('Delete person: ' + $scope.newUser.first_name + ' ' + $scope.newUser.last_name + '?')) {
                $http.delete('/users/' + $scope.newUser.id)
                    .success(function (data) {
                        parentScope.reloadUsers(true);
                        $modalInstance.close('ok');
                    }).error(function () {
                        alert("User couldn't be deleted. Please try again.");
                    });
            }
        };

        $scope.savePersonEdit = function () {
            if ($scope.editMode) {
                // edit user
                $http.put('/users/' + $scope.newUser.id, $scope.newUser)
                    .success(function (data) {
                        parentScope.reloadUsers(false);
                        $modalInstance.close('ok');
                    }).error(function () {
                        alert("Data couldn't be saved. Please try again.");
                    });
            } else {
                // add new user
                $http.post('/users/', $scope.newUser)
                    .success(function (data) {
                        parentScope.reloadUsers(false);
                        $modalInstance.close('ok');
                    }).error(function () {
                        alert("Data couldn't be saved. Please try again.");
                    });
            }
        };

        $scope.userEditOk = function () {
            $scope.savePersonEdit();
        };

        $scope.userEditCancel = function () {
            $modalInstance.dismiss('cancel');
        };
    });

    app.directive('selectOnClick', function () {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                element.on('click', function () {
                    this.select();
                });
            }
        };
    });
}());