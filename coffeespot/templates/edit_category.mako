<%inherit file="base.mako"/>

<%block name="title">edit category</%block>

%if category:
<form action="${url}" method="post">
    <fieldset>
        <legend>Category Name</legend>
        <input type="test" name="category_name" value="${category.name}">
    </fieldset>

    <fieldset>
        <legend>Delete Category?</legend>
        <input type="checkbox" name="delete_category">
    </fieldset>
    <input type="submit" name="submitted" value="Submit Changes">
</form>
%else:
The category you specified does not exist. Click
<a href="${request.route_url('home')}">here</a> to go home.
%endif
