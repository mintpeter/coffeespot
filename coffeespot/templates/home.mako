<%inherit file="base.mako"/>

<%block name="title">home</%block>

This is the body of the page. Here is some more body. And some more body.

% for post in posts:
    ${post.title}
% endfor
