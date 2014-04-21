<%inherit file="base.mako"/>

<%block name="title">Edit Post</%block>

% if post:
<form action="${url}" method="post">
    <fieldset>
        <legend>Post Title</legend>
        <input type="text" name="title" value="${post.title}">
    </fieldset>

    <fieldset>
        <legend>Category</legend>
        <select name="category">
%for category in categories:
    %if category.id == post.categoryid:
            <option value="${category.id}" selected>${category.name}</option>
    %else:
            <option value="${category.id}">${category.name}</option>
    %endif
%endfor
        </select>
    </fieldset>

    <fieldset>
        <legend>Post</legend>
        <textarea name="post_content">${post.post}</textarea>
    </fieldset>
    <input type="submit" name="submitted" value="Submit Changes">
</form>

% else:
<span class="message">${message}</span>

%endif
