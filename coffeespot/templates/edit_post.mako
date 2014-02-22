<%inherit file="base.mako"/>

<%block name="title">Edit Post</%block>

% if post:
<form action="${url}" method="post">
    Title:<br/>
    <input type="text" name="title" value="${post.title}"/><br/>
    Category:<br/>
    <select name="category">
    %for category in categories:
        %if category.id == post.categoryid:
            <option value="${category.id}" selected>${category.name}</option>
        %else:
            <option value="${category.id}">${category.name}</option>
        %endif
    %endfor
    </select><br/>
    Post:<br/>
    <textarea name="post_content">${post.post}</textarea><br/>
    <input type="submit" name="submitted" value="Submit Changes"/>
</form>

% else:
<span class="message">${message}</span>

%endif
