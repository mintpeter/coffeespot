<%inherit file="base.mako"/>

<%block name="title">View Post</%block>

% if post:
<h3>${post.title}</h3>

${post.post}

% else:
<h3>Post Not Found</h3>

<span class="message">${message}</span>

% endif
