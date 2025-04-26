<%@ page import="java.sql.*" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Student Information</title>
    <link rel="stylesheet" href="css/bootstrap.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        h2 {
            text-align: center;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>Student Information</h2>

    <%
        Connection conn = null;
        PreparedStatement stmt = null;
        ResultSet rs = null;

        String url = "jdbc:mysql://localhost:3306/studentdb";
        String user = "root";
        String password = "root";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            conn = DriverManager.getConnection(url, user, password);

            String query = "SELECT * FROM student_info";
            stmt = conn.prepareStatement(query);
            rs = stmt.executeQuery();
    %>

    <table>
        <thead>
            <tr>
                <th>Student ID</th>
                <th>Student Name</th>
                <th>Class</th>
                <th>Division</th>
                <th>City</th>
            </tr>
        </thead>
        <tbody>
            <%
                while (rs.next()) {
            %>
            <tr>
                <td><%= rs.getInt("stud_id") %></td>
                <td><%= rs.getString("stud_name") %></td>
                <td><%= rs.getString("class") %></td>
                <td><%= rs.getString("division") %></td>
                <td><%= rs.getString("city") %></td>
            </tr>
            <%
                }
            %>
        </tbody>
    </table>

    <%
        } catch (Exception e) {
            e.printStackTrace();
    %>
        <p>Error: <%= e.getMessage() %></p>
    <%
        } finally {
            if (rs != null) rs.close();
            if (stmt != null) stmt.close();
            if (conn != null) conn.close();
        }
    %>
</div>
</body>
</html>
