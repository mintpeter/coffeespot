<%inherit file="base.mako"/>

<%def name="title()">Viewing ${user.name}'s Profile</%def>

%if c.user.group == 0:
<p>
    <a href="${request.route_url('edit_user', uid=user.id)}">Edit this user</a>
</p>
%endif

${user.name}'s posts:
<ul>
    %for post in posts:
    <li>
        <a href="${request.route_url('view_post', pid=post.id)}">
            ${post.title}
        </a>
    </li>
    %endfor
</ul>
