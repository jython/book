<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    "http://www.w3.org/TR/html4/loose.dtd">


<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Jython JSP Test</title>
    </head>
    <body>
        <form method="GET" action="/AddToPage">
            <input type="text" name="p">
            <input type="submit">
        </form>

        <% Object page_text = request.getAttribute("page_text");
           Object sum = request.getAttribute("sum");

           if(page_text == null){
               page_text = "";
           }

           if(sum == null){
               sum = "";
           }
        %>

        <br/>

            <p><%= page_text %></p>

        <br/>

        <form method="GET" action="/AddNumbers">
            <input type="text" name="x">
            +
            <input type="text" name="y">
            =
            <%= sum %>
            <br/>
            <input type="submit" title="Add Numbers">


        </form>

        

       
    </body>
</html>
