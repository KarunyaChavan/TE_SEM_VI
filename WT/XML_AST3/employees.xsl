<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
        <head>
            <title>IT Firm Employee Data</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    background-color: #f9f9f9; 
                    color: #333; 
                    padding: 20px; 
                }
                h2 { 
                    text-align: center; 
                    color: #2c3e50; 
                    margin-bottom: 20px; 
                }
                table { 
                    border-collapse: collapse; 
                    width: 100%; 
                    background-color: #fff; 
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
                    border-radius: 8px; 
                    overflow: hidden; 
                }
                th, td { 
                    border: 1px solid #ddd; 
                    padding: 12px; 
                    text-align: left; 
                }
                th { 
                    background-color: #34495e; 
                    color: white; 
                    text-transform: uppercase; 
                    letter-spacing: 1px; 
                    font-weight: bold; 
                }
                tr:nth-child(even) { 
                    background-color: #f4f4f4; 
                }
                tr:hover { 
                    background-color: #ecf0f1; 
                }
            </style>
        </head>
        <body>
            <h2>Employee Information - IT Firm</h2>
            <table>
                <tr>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Date of Birth</th>
                    <th>Contact Number</th>
                    <th>Address</th>
                    <th>Gender</th>
                    <th>Designation</th>
                    <th>Date of Joining</th>
                    <th>Salary ($)</th>
                    <th>Department</th>
                </tr>
                <xsl:for-each select="employees/employee">
                    <tr>
                        <td><xsl:value-of select="empName/fname"/></td>
                        <td><xsl:value-of select="empName/lname"/></td>
                        <td><xsl:value-of select="DOB"/></td>
                        <td><xsl:value-of select="contactNo"/></td>
                        <td><xsl:value-of select="address"/></td>
                        <td><xsl:value-of select="gender"/></td>
                        <td><xsl:value-of select="designation"/></td>
                        <td><xsl:value-of select="dateOfJoin"/></td>
                        <td><xsl:value-of select="salary"/></td>
                        <td><xsl:value-of select="department"/></td>
                    </tr>
                </xsl:for-each>
            </table>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
