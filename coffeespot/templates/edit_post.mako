<%inherit file="base.mako"/>

<%block name="title">Edit Post</%block>

% if post:
<form action="${request.route_url('edit_post')}" method="post">
    <fieldset>
        <legend>${form.title.label}</legend>
        %if form.title.errors:
            %for error in form.title.errors:
            ${error}
            %endfor
        %endif
        ${form.title()}
    </fieldset>

    <fieldset>
        <legend>${form.category.label}</legend>
        %if form.category.errors:
            %for error in form.category.errors:
            ${error}
            %endfor
        %endif
        ${form.category()}
    </fieldset>

    <fieldset>
        <legend>${form.post_content.label}</legend>
        %if form.post_content.errors:
            %for error in form.post_content.errors:
            ${error}
            %endfor
        %endif
        ${form.post_content()}
    </fieldset>

    ${form.submit()}
</form>

% else:
<span class="message">The post you requested wasn't found. If a link on this
website led you here, please file a bug report.</span>

%endif
