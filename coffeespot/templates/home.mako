<%inherit file="base.mako"/>

<%!
    from markdown import markdown
    import datetime
    from pyramid.security import authenticated_userid
%>

<%block name="title">home</%block>
%if posts:
    %if 'cid' in request.matchdict:
       Click <a href="${request.route_url('edit_category', cid=request.matchdict['cid'])}">
       here</a> to edit this category.
    %endif

    %for post, user, category in posts:
    <div class="post">
        <h3>${post.title}</h2>
        <span class="datetime">
            posted by ${user.name.capitalize()} in "${category.name}" on
            ${datetime.datetime.fromtimestamp(post.date).strftime("%d %B %Y %I:%M %p")}
            </span>
        ${markdown(post.post) | n}
        %if userid:
            <a href="${request.route_url('edit_post', pid=post.id)}">edit post</a>; 
            <a href="${request.route_url('delete_post', pid=post.id)}">delete post</a>;
        %endif
            <a href="${request.route_url('view_post', pid=post.id)}#disqus_thread">comments</a>
    </div>
    <hr/>
    %endfor
%else:
    The posts you have specified do not exist. Click <a href="${request.route_url('home')}"
    here</a> to go home.
%endif

<script type="text/javascript">
    var disqus_shortname = 'zackmarvel'; // required: replace example with your forum shortname
    (function () {
        var s = document.createElement('script'); s.async = true;
        s.type = 'text/javascript';
        s.src = '//' + disqus_shortname + '.disqus.com/count.js';
        (document.getElementsByTagName('HEAD')[0] || document.getElementsByTagName('BODY')[0]).appendChild(s);
    }());
</script>
