<%inherit file="base.mako"/>

<%!
    from markdown import markdown
    import datetime
%>

<%block name="title">home</%block>
%if posts:
    %if 'cid' in request.matchdict and c.user:
       Click <a href="${request.route_url('edit_category', cid=request.matchdict['cid'])}">
       here</a> to edit this category.
    %endif

    %for post, user, category in posts:
    <section class="post">
        <h3>${post.title}</h3>
        <span class="datetime">
            posted by <a href="${request.route_url('view_user', uid=user.id)}">${user.name}</a>
            in category <a href="${request.route_url('view_category', cid=category.id)}">${category.name}</a>
            on ${datetime.datetime.fromtimestamp(post.date).strftime("%d %B %Y %I:%M %p")}
            </span>
        ${markdown(post.post) | n}
        %if c.user:
            <a href="${request.route_url('edit_post', pid=post.id)}">edit post</a>; 
            <a href="${request.route_url('delete_post', pid=post.id)}">delete post</a>;
        %endif
            <a href="${request.route_url('view_post', pid=post.id)}#disqus_thread">comments</a>
    </section>
    %endfor
%else:
    The posts you have specified do not exist. Click <a href="${request.route_url('home')}">
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
