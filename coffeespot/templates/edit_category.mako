<%inherit file="base.mako"/>

<%block name="title">edit category</%block>

%if category:
<form action="${url}" method="post">
    <input type="test" name="category_name" value="${category.name}"/><br/>
    <input type="checkbox" name="delete_category"/><br/>
    <input type="submit" name="submitted" value="Submit Changes"/>
</form>
%else:
The category you specified does not exist. Click
<a href="${request.route_url('home')}">here</a> to go home.
%endif
