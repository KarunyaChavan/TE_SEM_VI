angular.module("bookstoreApp").controller("AuthController", function($scope, $location, AuthService) {
    $scope.user = {};
  
    $scope.login = function () {
      if (AuthService.login($scope.user)) {
        $location.path("/profile");
      } else {
        alert("Invalid credentials");
      }
    };
  
    $scope.register = function () {
      AuthService.register($scope.user);
      alert("Registered successfully. Please login.");
      $location.path("/");
    };
  });
  