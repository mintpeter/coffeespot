<%inherit file="base.mako"/>

<%def name="title()">Editing ${user.name}'s Profile</%def>

<form method="POST" action="${request.route_url('edit_user', uid=user.id)}">
    <fieldset>
        <legend>${form.name.label}</legend>
        %if form.name.errors:
            %for error in form.name.errors:
            <span class="error">${error}</span>
            %endfor
        %endif
        ${form.name(value=user.name)}
    </fieldset>
    
    <fieldset>
        <legend>${form.password.label}</legend>
        <em>This will reset your password.</em><br>
        %if form.password.errors:
            %for error in form.name.errors:
            <span class="error">${error}</span>
            %endfor
        %endif
        ${form.password()}
    </fieldset>

    <fieldset>
        <legend>${form.delete.label}</legend>
        Delete this user? ${form.delete()}
    </fieldset>
    
    ${form.user_id(value=user.id)}
    ${form.group(value=user.group)}

    ${form.submit()}
</form>
