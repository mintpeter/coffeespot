<%inherit file="base.mako"/>

<%!
    import markdown
    from markupsafe import Markup
    import datetime
    from pyramid.security import authenticated_userid
%>

<%block name="title">home</%block>

%for post, user in posts:
<div class="post">
    <h3>${post.title}</h2>
    <span class="datetime">
        posted by ${user.name.capitalize()} on
        ${datetime.datetime.fromtimestamp(post.date).strftime("%d %B %Y %I:%M %p")}
        </span>
    ${Markup(markdown.markdown(post.post))}
    %if authenticated_userid(request):
        <a href="${request.route_url('edit_post', pid=post.id)}">edit post</a>; 
        <a href="${request.route_url('delete_post', pid=post.id)}">delete post</a>;
    %endif
        <a href="${request.route_url('view_post', pid=post.id)}#disqus_thread">comments</a>
</div>
%endfor

<script type="text/javascript">
    var disqus_shortname = 'zackmarvel'; // required: replace example with your forum shortname
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = '//' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
</script>
