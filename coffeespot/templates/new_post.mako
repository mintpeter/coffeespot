<%inherit file="base.mako"/>

<%block name="title">new post</%block>

%if message == '':
<form action="${url}" method="post">
    Title:<br/>
    <input type="text" name="title"/><br/>
    Category:<br/>
    <select name="category">
    %for category in categories:
        <option value="${category.id}">${category.name}</option>
    %endfor
    </select><br/>
    Post:<br/>
    <textarea name="post_content"></textarea><br/>
    <input type="submit" name="submitted" value="Add Post"/>
</form>
%else:
<span class="message">${message}</span><br/>
${post}
%endif


