<post-feed>
  <div each={post in opts.posts}>
    <li class="media post post-{post.id} list-group-item p-4 my-3">
      <img class="media-object mr-3 align-self-start" src="{ post.user_url }">
      <div class="media-body">
        <div class="media-heading">
          <small class="float-right text-muted">{post.days_since} days</small>
          <h6><a href="{root_url}/users/{post.user}">{post.user_name}</a> made the commitment: <a href="{root_url}/posts/{post.id}">{post.title}</a></h6>
        </div>
        <p>
          {post.description}
        </p>
      </div>
    </li>
    <div if={post.proof_description && post.proof_pic} id="accordion{post.id}" role="tablist">
      <div class="card">
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
  </div>
  <div class="post-footer pb-3">
    <a href="#" class="ml-3 pt-3 like-btn" style="color: #007bff;" id="{post.id}" show={post.likes.includes(user_id)}><span class="icon icon-thumbs-up"></span> Liked ({post.likes.length})</a>
    <a href="#" class="ml-3 pt-3 like-btn" id="{post.id}" hide={post.likes.includes(user_id)}><span class="icon icon-thumbs-up"></span> Like ({post.likes.length})</a>
    <a class="ml-3 pt-3 comment-btn comment-btn-{post.id}" post-id="{post.id}" href="#"><span class="icon icon-message"></span> Comment ({post.comments.length})</a>
    <a if={(!post.completed && (post.proof_description || post.proof_pic)) && post.verifications.includes(user_id)} class="ml-3 pt-3 verify-btn verify-btn-{post.id}" post-id="{post.id}" style="color:#007bff;" href="#"><span class="icon icon-shield"></span> Verified ({post.verifications.length}/5)</a>
    <a if={(!post.completed && (post.proof_description || post.proof_pic)) && !post.verifications.includes(user_id)} class="ml-3 pt-3 verify-btn verify-btn-{post.id}" post-id="{post.id}" style="color:grey;" href="#"><span class="icon icon-shield"></span> Verify ({post.verifications.length}/5)</a>
    <div class="completion-status-container-{post.id}" style="display:inline;">
      <p if={!post.completed && !(post.proof_description || post.proof_pic)} class="float-right completion-status mr-3 pt-1" style="color: red;"><span class="icon icon-cross"></span> Not completed</p>
      <p if={!post.completed && (post.proof_description || post.proof_pic)} class="float-right completion-status awaiting-verifcation-{post.id} mr-3 pt-1" style="color: #FFBF00; margin-bottom:0px;"><span class="icon icon-hour-glass"> Awaiting Verification</span></p>
      <p if={post.completed} class="float-right completion-status completed-{post.id} mr-3 pt-1" style="color: green;"><span class="icon icon-check"></span> Completed</p>
    </div>
  </div>
  <div class="comment-container comment-container-{post.id}" commentsopen="false" style="display:none;">
    <ul class="media-list comment-list comment-list-{post.id} mx-auto d-block my-0" style="width:95%;">
    </ul>
  </div>
  <div class="comment-form comment-form-{post.id}" style="display:none;">
      <div class="form-group">
        <input type="text" class="form-control comment" post-id="{post.id}" placeholder="Comment">
      </div>
  </div>
</div>
  <script>
    this.on('mount', function() {
      opts.callback(this)
    })
    // this.on('update')
    this.on('data_loaded', function(data, user_id) {
      opts.posts = data
      // root_url = 'https://127.0.0.8:8000'
      root_url = 'https://peerspace.herokuapp.com'
      this.update()
    })
  </script>
</post-feed>
