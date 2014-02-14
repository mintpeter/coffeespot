<%inherit file="base.mako"/>

<%block name="title">Delete Post<%/block>

<span class="message">${message}</span>

% if post:
<form action="${url}" method="post">
    <input type="submit" name="submitted" value="Yes"/>
    <input type="submit" name="no_delete" value="No"/>
</form>

% else:
Click <a href="${url}">here</a> to go home.

% endif
