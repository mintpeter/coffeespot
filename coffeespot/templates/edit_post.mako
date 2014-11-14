<%inherit file="base.mako"/>

<%block name="title">edit post</%block>



%if post:
<form action="${request.route_url('new_post')}" method="POST">
    <fieldset>
        <legend>${form.title.label}</legend>
        %if form.title.errors:
            %for error in form.title.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.title(value=post.title)}
    </fieldset>

    <fieldset>
        <legend>${form.category.label}</legend>
        %if form.category.errors:
            %for error in form.category.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.category(value=post.categoryid)}
    </fieldset>

    <fieldset>
        <legend>${form.post_content.label}</legend>
        %if form.post_content.errors:
            %for error in post_content.errors:
        <span class="error">${error}</span>
            %endfor
        %endif
        ${form.post_content(value=post.post)}
    </fieldset>

    ${form.submit()}
</form>

% else:
<span class="message">The post you requested was not found. If a link on this
website sent you here, head to the contact us page.</span>

%endif
