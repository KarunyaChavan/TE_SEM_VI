angular.module("bookstoreApp").controller("BooksController", function($scope, AuthService) {
    $scope.searchText = "";

    $scope.books = [
      { title: "Operating System Concepts", author: "Abraham Silberschatz", category: "Operating Systems" },
      { title: "Modern Operating Systems", author: "Andrew S. Tanenbaum", category: "Operating Systems" },
      { title: "Database System Concepts", author: "Henry F. Korth", category: "Databases" },
      { title: "Fundamentals of Database Systems", author: "Ramez Elmasri", category: "Databases" },
      { title: "Computer Networking: A Top-Down Approach", author: "Kurose & Ross", category: "Computer Networks" },
      { title: "Data Communications and Networking", author: "Behrouz Forouzan", category: "Computer Networks" },
      { title: "Artificial Intelligence: A Modern Approach", author: "Russell & Norvig", category: "AI" },
      { title: "Machine Learning", author: "Tom Mitchell", category: "ML" },
      { title: "Python Machine Learning", author: "Sebastian Raschka", category: "ML" },
      { title: "Software Engineering", author: "Ian Sommerville", category: "Software Engineering" },
      { title: "The Mythical Man-Month", author: "Frederick P. Brooks", category: "Software Engineering" },
      { title: "Introduction to Algorithms", author: "CLRS", category: "DSA" },
      { title: "Data Structures Using C", author: "Reema Thareja", category: "DSA" },
      { title: "Object-Oriented Analysis & Design", author: "Grady Booch", category: "OOP" },
      { title: "Computer Organization and Design", author: "David A. Patterson", category: "Computer Architecture" },
      { title: "Cryptography and Network Security", author: "William Stallings", category: "Security" },
      { title: "Computer Security: Principles and Practice", author: "William Stallings", category: "Security" },
      { title: "Cloud Computing: Theory and Practice", author: "Dan C. Marinescu", category: "Cloud Computing" },
      { title: "Internet of Things", author: "Arshdeep Bahga", category: "IoT" },
      { title: "Compiler Design", author: "Aho, Lam, Sethi, Ullman", category: "Compilers" }
    ];

    $scope.save = function(book) {
        alert("Book saved: " + book.title);
        AuthService.addLentBook(book); // now this works correctly
    };
});
