<comments>
    <div each={comment in opts.comments}>
        <li class="media comment-block comment-block-detail py-3" commentid="{comment.comment_id}">
            <a href="/users/{comment.user_id}/"><img class="media-object comment-pic d-flex align-self-start mr-3" src="{comment.user_pic_url}"></a>
            <div class="media-body">
                <a href="/users/{comment.user_id}/"><strong>{comment.user_name}: </strong></a>{comment.comment}
            </div>
            <button class="btn delete-comment-btn delete-comment-btn-{comment.comment_id} btn-outline-danger" style="float:right;
        padding:0 3px;" href="#" onClick="deleteComment({comment.comment_id},{opts.postId},{opts.userId})"><span class="icon icon-cross"></span></button>
        </li>
        <hr>
    </div>
    <script>
        this.on('mount', function() {
            opts.callback(this)
        });
        this.on('data_loaded', function(data, postId, userId) {
            opts.comments = data;
            opts.postId = postId;
            opts.userId = userId;
            this.update()
        })
    </script>
</comments>
