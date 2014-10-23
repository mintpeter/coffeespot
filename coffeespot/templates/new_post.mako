<%inherit file="base.mako"/>

<%block name="title">new post</%block>


%if post:
${post}
%else:
<form action="${request.route_url('new_post')}" method="POST">
    <fieldset>
        <legend>${form.title.label}</legend>
        %if form.title.errors:
            %for error in form.title.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.title()}
    </fieldset>

    <fieldset>
        <legend>${form.category.label}</legend>
        %if form.category.errors:
            %for error in form.category.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.category()}
    </fieldset>

    <fieldset>
        <legend>${form.post_content.label}</legend>
        %if form.post_content.errors:
            %for error in post_content.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.post_content()}
    </fieldset>

    ${form.submit()}
</form>
%endif
