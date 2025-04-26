angular.module("bookstoreApp").factory("AuthService", function () {
    return {
      login: function (user) {
        const users = JSON.parse(localStorage.getItem("users")) || [];
        const found = users.find(u => u.username === user.username && u.password === user.password);
        if (found) {
          localStorage.setItem("currentUser", JSON.stringify(found));
          return true;
        }
        return false;
      },
  
      logout: function () {
        localStorage.removeItem("currentUser");
      },
  
      register: function (user) {
        const users = JSON.parse(localStorage.getItem("users")) || [];
        users.push(user);
        localStorage.setItem("users", JSON.stringify(users));
      },
  
      getCurrentUser: function () {
        return JSON.parse(localStorage.getItem("currentUser"));
      },
  
      addLentBook: function (book) {
        let lentBooks = JSON.parse(localStorage.getItem("lentBooks")) || [];
        if (!lentBooks.some(b => b.title === book.title && b.author === book.author)) {
          lentBooks.push(book);
          localStorage.setItem("lentBooks", JSON.stringify(lentBooks));
        }
      },
  
      getLentBooks: function () {
        return JSON.parse(localStorage.getItem("lentBooks")) || [];
      },

      removeLentBook: function(book) {
        let lentBooks = JSON.parse(localStorage.getItem("lentBooks")) || [];
        lentBooks = lentBooks.filter(b => !(b.title === book.title && b.author === book.author));
        localStorage.setItem("lentBooks", JSON.stringify(lentBooks));
      }
    };

    
  });
  