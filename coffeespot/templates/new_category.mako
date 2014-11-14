<%inherit file="base.mako"/>

<%block name="title">new category</%block>

<form action="${request.route_url('new_category')}" method="POST">
    <fieldset>
        <legend>${form.name.label}</legend>
        %if form.name.errors:
            %for error in form.name.errors:
            <span class="error">${error}</span>
            %endfor
        %endif
        ${form.name()}
    </fieldset>

    ${form.submit()}
</form>
