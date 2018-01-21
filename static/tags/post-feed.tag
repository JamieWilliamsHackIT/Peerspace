<post-feed>
    <div class="mb-3" each={post in opts.posts}>
        <li class="media post post-{post.id} list-group-item p-4">
            <a href="/users/{post.user}" data-user-id={post.user}><img class="media-object mr-3 align-self-start profile-pic" src="{post.user_url}"></a>
            <div class="media-body">
                <div class="media-heading">
                    <small class="text-muted float-right" if={post.time_ago < 60}>{Math.round(post.time_ago)} second<span if={Math.round(post.time_ago) !== 1}>s</span></small>
                    <small class="text-muted float-right" if={post.time_ago >= 60 && post.time_ago < 3600}>{Math.round(post.time_ago / 60)} min<span if={Math.round(post.time_ago / 60) !== 1}>s</span></small>
                    <small class="text-muted float-right" if={post.time_ago >= 3600 && post.time_ago < (24 * 3600)}>{Math.round(post.time_ago / 3600)} hour<span if={Math.round(post.time_ago / 3600) !== 1}>s</span></small>
                    <small class="text-muted float-right" if={post.time_ago >= (24 * 3600)}>{Math.round(post.time_ago / (24 * 3600))} day<span if={Math.round(post.time_ago / (24 * 3600)) !== 1}>s</span></small>


                    <small class="text-muted float-right updates-stat">{post.progress_updates.length} update<span if={post.progress_updates.length !== 1}>s</span></small>
                    <h6><a href="/users/{post.user}">{post.user_name}</a> made the commitment: <br><br><a href="/posts/{post.id}">{post.title}</a></h6>
                </div><hr>
                <p>
                    {post.description}
                </p>
                <p if={post.tags} each={tag in post.tags.split(', ')} class="tags">
                #{tag}
                </p><br><br>
                <p if={!post.completed} class="post-stats">
                    <span class="js-likes-stat-{post.id}"><span if={post.likes.length}><span class="icon icon-heart"> </span>{post.likes.length} </span></span>
                    <span class="js-comments-stat-{post.id}"><span if={post.comments.length} class="pl-1"><span class="icon icon-message"> </span>{post.comments.length} </span></span>
                    <span class="js-motivations-stat-{post.id}"><span if={post.motivations.length}><span class="icon icon-flash">{post.motivations.length} </span></span></span>
                </p>
            </div>
        </li>
        <div if={post.proof_description && post.proof_pic} id="accordion{post.id}" role="tablist" style="position: relative">
            <div class="card pb-4">
                <div class="card-header" role="tab" id="heading{post.id}">
                    <h5 class="mb-0">
                        <a data-toggle="collapse" href="#collapse{post.id}" aria-expanded="true" aria-controls="collapse{post.id}">
                            {post.user_name} submitted proof, it took {post.days_taken} days.
                        </a>
                    </h5>
                </div>
                <div id="collapse{post.id}" class="collapse show" role="tabpanel" aria-labelledby="heading{post.id}" data-parent="#accordion{post.id}">
                    <div class="card-body">
                        <div class="post-proof">
                            <p>{post.proof_description}</p>
                            <img class="img-fluid d-block m-auto" src="{post.proof_pic}">
                        </div>
                    </div>
                </div>
            </div>
            <p if={post.completed} class="post-stats-completed">
                <span class="js-likes-stat-{post.id}"><span if={post.likes.length}><span class="icon icon-heart"> </span>{post.likes.length} </span></span>
                <span class="js-comments-stat-{post.id}"><span if={post.comments.length} class="pl-1"><span class="icon icon-message"> </span>{post.comments.length} </span></span>
                <span class="js-motivations-stat-{post.id}"><span if={post.motivations.length}><span class="icon icon-flash">{post.motivations.length} </span></span></span>
            </p>
        </div>
        <div class="post-footer pb-3">
            <a href="#" class="ml-3 pt-3 like-btn" style="color: #007bff;" id="{post.id}" show={post.likes.includes(opts.userViewingId)}><span class="icon icon-heart"></span> Like</a>
            <a href="#" class="ml-3 pt-3 like-btn" id="{post.id}" hide={post.likes.includes(opts.userViewingId)}><span class="icon icon-heart-outlined"></span> Like</a>
            <a class="ml-3 pt-3 comment-btn comment-btn-{post.id}" data-open="false" data-post-id={post.id} if={post.page != 'detail'}><span class="icon icon-message"></span> Comment</a>
            <a class="ml-auto pt-3 motivate-btn motivate-btn-{post.id}" style="color: #007bff;" post-id="{post.id}" show={post.motivations.includes(opts.userViewingId)} if={!post.completed} href="#"><span class="icon icon-flash"></span> Motivate</a>
            <a class="ml-auto pt-3 motivate-btn motivate-btn-{post.id}" post-id="{post.id}" hide={post.motivations.includes(opts.userViewingId)} if={!post.completed} href="#"><span class="icon icon-flash"></span> Motivate</a>
            <a if={(!post.completed && (post.proof_description || post.proof_pic)) && post.verifications.includes(opts.userViewingId)} class="ml-3 pt-3 verify-btn verify-btn-{post.id}" post-id="{post.id}" style="color:#007bff;" href="#"><span class="icon icon-shield"></span> Verified ({post.verifications.length}/5)</a>
            <a if={(!post.completed && (post.proof_description || post.proof_pic)) && !post.verifications.includes(opts.userViewingId)} class="ml-3 pt-3 verify-btn verify-btn-{post.id}" post-id="{post.id}" style="color:grey;" href="#"><span class="icon icon-shield"></span> Verify ({post.verifications.length}/5)</a>
            <div class="completion-status-container-{post.id}" style="display:inline;">
                <p if={!post.completed && !(post.proof_description || post.proof_pic)} class="float-right completion-status mr-3 pt-1" style="color: red;"><span class="icon icon-cross"></span><span class="d-none d-sm-inline"> Not completed</span></p>
                <p if={post.completed} class="float-right completion-status completed-{post.id} mr-3 pt-1" style="color: green;"><span class="icon icon-check"></span><span class="d-none d-sm-inline"> Completed</span></p>
            </div>
        </div>
        <div if={post.page != 'detail'}>

            <div class="comment-container comment-container-{post.id}" style="display:none;">
                <div class="comment-form comment-form-{post.id} py-2 mx-3 style="display:none;">
                    <div class="form-group mb-0 d-flex">
                        <img class="media-object comment-pic d-flex align-self-start mr-3" src="{post.user_viewing_url}">
                        <textarea type="text" class="form-control comment d-flex" data-post-id="{post.id}" placeholder="Write comment" rows="1"></textarea>
                    </div>
                </div>
                <ul class="media-list comment-list comment-list-{post.id} mx-auto d-block my-0" style="width:95%;">
                </ul>
                <a if={post.comments.length > 5} class="ml-3 pb-2 d-block js-load-comments js-load-comments-{post.id} load-comments" data-post-id="{post.id}">Load more comments</a>
            </div>
        </div>
        <div if={post.page == 'detail'} class="mt-4">
        <div each={progress in post.progress_updates} id="accordion{progress.id}" role="tablist">
            <div class="card">
                <div class="card-header" role="tab" id="heading{progress.id}">
                    <h5 class="mb-0">
                        <a data-toggle="collapse" href="#collapse{progress.id}" aria-expanded="true" aria-controls="collapse{progress.id}">
                            {post.user_name} add a progress update
                            <span if={progress.time_ago < 60}>{Math.round(progress.time_ago)} second<span if={Math.round(progress.time_ago) !== 1}>s </span> ago</span>
                            <span if={progress.time_ago >= 60 && progress.time_ago < 3600}>{Math.round(progress.time_ago / 60)} min<span if={Math.round(progress.time_ago / 60) !== 1}>s </span> ago</span>
                            <span if={progress.time_ago >= 3600 && progress.time_ago < (24 * 3600)}>{Math.round(progress.time_ago / 3600)} hour<span if={Math.round(progress.time_ago / 3600) !== 1}>s </span> ago</span>
                            <span if={progress.time_ago >= (24 * 3600)}>{Math.round(progress.time_ago / (24 * 3600))} day<span if={Math.round(progress.time_ago / (24 * 3600)) !== 1}>s </span> ago</span>
                        </a>
                    </h5>
                </div>
                <div id="collapse{progress.id}" class="collapse show" role="tabpanel" aria-labelledby="heading{progress.id}" data-parent="#accordion{progress.id}">
                    <div class="card-body">
                        <div class="post-proof">
                            <p>{progress.description}</p>
                            <img class="img-fluid d-block m-auto" src="{progress.progress_pic}">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </div>
    <script>
        this.on('mount', function() {
            opts.callback(this)
        });
        this.on('data_loaded', function(data, userId, userViewingId) {
            opts.posts = data;
            opts.userId = userId;
            opts.userViewingId = userViewingId;
            this.update()
        })
    </script>
</post-feed>
