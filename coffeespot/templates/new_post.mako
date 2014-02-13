<%inherit file="base.mako"/>

<%block name="title">Edit Post</%block>

% if message == '':
<form action="${url}" method="post">
    <input type="text" name="title"/><br/>
    <textarea name="post_content"></textarea>
    <input type="submit" name="submitted" value="Add Post"/>
</form>
% else:
<span class="message">${message}</span><br/>
${post}
% endif


