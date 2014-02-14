<%inherit file="base.mako"/>

<%block name="title">Edit Post</%block>

% if post:
<form action="${url}" method="post">
    <input type="text" name="title" value="${post.title}"/><br/>
    <textarea name="post_content">${post.post}</textarea>
    <input type="submit" name="submitted" value="Submit Changes"/>
</form>

% else:
<span class="message">${message}</span>

%endif
