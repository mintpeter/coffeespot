<%inherit file="base.mako"/>

<%block name="title">new category</%block>

<form action="${url}" method="post">
    <input type="text" name="category_name"/><br/>
    <input type="submit" name="submitted" value="Add Category"/>
</form>
