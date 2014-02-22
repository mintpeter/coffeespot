<%!
    from pyramid.security import authenticated_userid
    from coffeespot.models import DBSession, Categories
%>

<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet"  type="text/css" href="/css/style.css"/>
    <title><%block name="title"/></title>
</head>
<body>
    <div id="container">
        <h1 id="header">Zack Marvel</h1>
        <div id="navigation">
            Pages
            <ul>
                <li><a href="/">Home</a></li>
%if userid:
                <li><a href="/post/new/">New Post</a></li>
                <li><a href="/logout/">Log Out</a></li>
%else:
                <li><a href="/login/">Log In</a></li>
%endif
            </ul>
            Categories
            <ul>
%for category in DBSession.query(Categories).all():
                <li><a href="${request.route_url('view_category', cid=category.id)}">${category.name.capitalize()}</a></li>
%endfor
%if userid:
                <li><a href="${request.route_url('new_category')}">New Category</a>
%endif
            </ul>
        </div>
        <div id="main">
            ${self.body()}
        </div>
    </div>
</body>
</html>
