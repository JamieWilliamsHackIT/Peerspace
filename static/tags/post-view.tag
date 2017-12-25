<post-view>
  <li class="media list-group-item p-4 mt-4">
    <img class="media-object mr-3 align-self-start" src="http://127.0.0.1:8000{ opts.post.user_url }">
    <div class="media-body">
      <div class="media-heading">
        <small class="float-right text-muted">{opts.post.days_since} days</small>
        <h6><a href="http://127.0.0.1:8000/users/{opts.post.user}">{opts.post.user_name}</a> made the commitment: {opts.post.title}</h6>
      </div>
      <p>
        {opts.post.description}
      </p>
    </div>
  </li>
  <div if={post.completed} id="accordion{post.id}" role="tablist">
    <div class="card">
      <div class="card-header" role="tab" id="heading{post.id}">
        <h5 class="mb-0">
          <a data-toggle="collapse" href="#collapse{post.id}" aria-expanded="true" aria-controls="collapse{post.id}">
            {post.user_name} completed their commitment, it took {post.days_taken} days.
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
    <a href="#" class="ml-3 pt-3 like-btn" style="color: #007bff;" id="{opts.post.id}" show={opts.post.likes.includes(opts.user_id)}><span class="icon icon-thumbs-up"></span> Like</a>
    <a href="#" class="ml-3 pt-3 like-btn" id="{opts.post.id}" hide={opts.post.likes.includes(opts.user_id)}><span class="icon icon-thumbs-up"></span> Like</a>
    <a href="#" class="ml-3 pt-3 like-btn"><span class="icon icon-message"> Comment</a>
  </div>
  <script>
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data, user_id) {
      opts.post = data
      opts.user_id = user_id
      console.log(data)
      // console.log(opts)
      this.update()
    })
  </script>
</post-view>
