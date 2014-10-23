<%inherit file="base.mako"/>

<%block name="title">Login</%block>

<span class="message">${message}</span>

<form method="POST" action="${request.route_url('login')}">
    <fieldset>
        <legend>${form.username.label}</legend>
        %if form.username.errors:
            %for error in form.username.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.username()}
    </fieldset>

    <fieldset>
        <legend>${form.password.label}</legend>
        %if form.password.errors:
            %for error in form.password.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.password()}
    </fieldset>

    ${form.came_from(value=came_from)}

    ${form.submit()}
</form>
