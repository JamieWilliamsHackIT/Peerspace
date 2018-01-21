<comments>
    <li each={comment, index in opts.comments} class="media comment-block comment-block-detail py-3" commentid="{comment.comment_id}">
        <a href="/users/{comment.user_id}/"><img class="media-object comment-pic d-flex align-self-start mr-3" src="{comment.user_pic_url}"></a>
        <div class="media-body comment-body">
            <a href="/users/{comment.user_id}/"><strong>{comment.user_name} </strong></a><span class="ml-1">{comment.comment}<span>
        </div>
        <button if={comment.user_id === opts.userId} class="btn btn-outline-danger delete-comment-btn delete-comment-btn-{comment.comment_id} ml-2" style="float:right;
        padding:0 3px;" href="#" data-post-id={opts.postId} data-comment-id={comment.comment_id}><span class="icon icon-cross"></span></button>
    </li>
    <script>
        this.on('mount', function() {
            opts.callback(this, opts.postId, opts.userId)
        });
        this.on('data_loaded', function(data, postId, userId) {
            opts.comments = data;
            opts.postId = postId;
            opts.userId = userId;
            this.update()
        })
    </script>
</comments>
