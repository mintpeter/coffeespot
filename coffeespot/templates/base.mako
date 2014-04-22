<%!
    from coffeespot.models.tables import DBSession, Categories
%>

<%def name="title()"/>

<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <link rel="stylesheet" type="text/css" href="/css/style.css"/>
    <link href='http://fonts.googleapis.com/css?family=Mako' rel='stylesheet' type='text/css'>
    <title>${self.title()}</title>
</head>
<body>
    <header>
        <h1 id="header">Zack Marvel</h1>
    </header>
    
    <nav>
    <span>Pages</span>
        <ul class="navigation">
            <li><a href="${request.route_url('home')}">Home</a></li>
%if c.user:
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
%if c.user:
            <li><a href="${request.route_url('new_category')}">New Category</a>
%endif
        </ul>
%if c.user:
    <span>User Options</span>
    <ul>
        <li><a href="${request.route_url('view_user', uid=c.user.id)}">View Your Profile</a></li>
        <li><a href="${request.route_url('edit_user', uid=c.user.id)}">Edit Your Profile</a></li>
    %if c.user.group == 0:
        <li><a href="${request.route_url('new_user')}">New User</a></li>
    %endif
    </ul>
%endif
    </nav>
    <div id="main">
        ${self.body()}
        <div class="clear">&nbsp;</div>
    </div>
    <footer>
        Powered by <a href="http://python.org">Python</a> and
        <a href="http://pylonsproject.org">Pyramid</a>. Would you like to view
        <a href="https://github.com/mintpeter/coffeespot">the source</a>?
    </footer>
</body>
</html>
