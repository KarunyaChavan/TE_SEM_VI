angular.module("bookstoreApp", ["ngRoute"])
.config(function($routeProvider) {
  $routeProvider
    .when("/", {
      templateUrl: "app/views/login.html",
      controller: "AuthController"
    })
    .when("/register", {
      templateUrl: "app/views/register.html",
      controller: "AuthController"
    })
    .when("/books", {
      templateUrl: "app/views/books.html",
      controller: "BooksController"
    })
    .when("/profile", {
      templateUrl: "app/views/profile.html",
      controller: "ProfileController"
    })
    .otherwise({ redirectTo: "/" });
});
