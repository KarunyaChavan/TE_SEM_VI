angular.module("bookstoreApp").controller("ProfileController", function($scope, $location, AuthService) {
  const user = AuthService.getCurrentUser();
  $scope.user = user || { username: "Guest", email: "N/A" };
  $scope.lentBooks = AuthService.getLentBooks();

  $scope.logout = function () {
      AuthService.logout();
      $location.path("/");
  };

  $scope.returnBook = function(book) {
      AuthService.removeLentBook(book);
      $scope.lentBooks = AuthService.getLentBooks(); // refresh list
  };
});
