<%inherit file="base.mako"/>

<%def name="title()">Viewing ${user.name}'s Profile</%def>

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
