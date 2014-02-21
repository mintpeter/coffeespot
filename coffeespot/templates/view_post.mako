<%inherit file="base.mako"/>

<%block name="title">View Post</%block>

%if post:
<h3>${post.title}</h3>

${post.post}

<div id="disqus_thread"></div>
<script type="text/javascript">
    var disqus_shortname = 'zackmarvel';
    var disqus_identifier = '${post.id}';
    var disqus_title = '${post.title}';
    var disqus_url = '${request.route_url('view_post', pid=post.id)}';
    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
<a href="http://disqus.com" class="dsq-brlink">comments powered by <span class="logo-disqus">Disqus</span></a>
                                                                                                    

%else:
<h3>Post Not Found</h3>

<span class="message">${message}</span>

%endif
