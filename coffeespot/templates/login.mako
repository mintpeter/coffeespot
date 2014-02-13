<%inherit file="base.mako"/>

<%block name="title">Login</%block>

<span class="message">${message}</span>

<form action="${url}" method="post">
    <input type="hidden" name="came_from" value="${came_from}"/>
    <input type="text" name="username" value="${username}"/><br/>
    <input type="password" name="password"/><br/>
    <input type="submit" name="submitted" value="Log In"/>
</form>
