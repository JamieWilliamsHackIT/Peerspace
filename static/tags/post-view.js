riot.tag2('post-view', '<li class="media list-group-item p-4 mt-4"> <img class="media-object mr-3 align-self-start" riot-src="http://127.0.0.1:8000{opts.post.user_url}"> <div class="media-body"> <div class="media-heading"> <small class="float-right text-muted">{opts.post.days_since} days</small> <h6><a href="http://127.0.0.1:8000/users/{opts.post.user}">{opts.post.user_name}</a> made the commitment: {opts.post.title}</h6> </div> <p> {opts.post.description} </p> </div> </li> <div class="post-footer pb-3"> <a href="#" class="ml-3 pt-3 like-btn" style="color: #007bff;" id="{opts.post.id}" show="{opts.post.likes.includes(opts.user_id)}"><span class="icon icon-thumbs-up"></span> Like</a> <a href="#" class="ml-3 pt-3 like-btn" id="{opts.post.id}" hide="{opts.post.likes.includes(opts.user_id)}"><span class="icon icon-thumbs-up"></span> Like</a> <a href="#" class="ml-3 pt-3 like-btn"><span class="icon icon-message"> Comment</a> </div>', '', '', function(opts) {
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data, user_id) {
      opts.post = data
      opts.user_id = user_id
      console.log(data)

      this.update()
    })
});
