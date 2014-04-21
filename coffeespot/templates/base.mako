<%!
    from coffeespot.models import DBSession, Categories
%>

<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="/css/style.css"/>
    <link href='http://fonts.googleapis.com/css?family=Mako' rel='stylesheet' type='text/css'>
    <title><%block name="title"/></title>
</head>
<body>
    <header>
        <h1 id="header">Zack Marvel</h1>
    </header>
    
    <nav>
    <span>Pages</span>
        <ul class="navigation">
            <li><a href="${request.route_url('home')}">Home</a></li>
%if c.userid:
            <li><a href="${request.route_url('new_post')}">New Post</a></li>
            <li><a href="${request.route_url('logout')}">Log Out</a></li>
%else:
            <li><a href="${request.route_url('login')}">Log In</a></li>
%endif
        </ul>
    <span>Categories</span>
        <ul class="navigation">
%for category in DBSession.query(Categories).all():
            <li><a href="${request.route_url('view_category', cid=category.id)}">
                ${category.name.capitalize()}
            </a></li>
%endfor
%if c.userid:
            <li><a href="${request.route_url('new_category')}">New Category</a>
%endif
        </ul>
    </nav>
    <div id="main">
        ${self.body()}
        <div class="clear">&nbsp;</div>
    </div>
</body>
</html>
