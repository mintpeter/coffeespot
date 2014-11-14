<%inherit file="base.mako"/>

<%block name="title">edit category</%block>

%if category:
<form action="${request.route_url('edit_category')}" method="post">
    <fieldset>
        <legend>${form.delete.label}</legend>
        %if form.delete.errors:
            %for error in form.delete.errors:
            ${error}
            %endfor
        %endif
        ${form.delete()}
    </fieldset>

    <fieldset>
        <legend>${form.name.label}</legend>
        %if form.name.errors:
            %for error in form.name.errors:
            ${error}
            %endfor
        %endif
        %{form.name()}
    </fieldset>

</form>
%else:
The category you specified does not exist. Click
<a href="${request.route_url('home')}">here</a> to go home.
%endif
