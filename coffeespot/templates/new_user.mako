<%inherit file="base.mako"/>

<%def name="title()">New User</%def>

<form method="POST" action="${request.route_url('new_user')}">
    <fieldset>
        <legend>${form.name.label}</legend>
        %if form.name.errors:
            %for error in form.name.errors:
            <span class="error">${error}</span>
            %endfor
        %endif
        ${form.name()}
    </fieldset>
    
    <fieldset>
        <legend>${form.password.label}</legend>
        %if form.password.errors:
            %for error in form.name.errors:
            <span class="error">${error}</span>
            %endfor
        %endif
        ${form.password()}
    </fieldset>

    <fieldset>
        <legend>${form.group.label}</legend>
        ${form.group()}
    </fieldset>

    ${form.submit()}
</form>
