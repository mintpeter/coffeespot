<%inherit file="base.mako"/>

<%block name="title">home</%block>

This is the body of the page. Here is some more body. And some more body. User is
% if username != [] :
    ${username}.
% else:
    not logged in.
% endif

<br/><br/>

% for post in posts:
    ${post.title}<br/><br/>
    <p>${post.post}</p><br/><br/>
% endfor
