riot.tag2('follower', '<div each="{user in opts.users}" class="mb-3"> <li class="list-group-item"> <div class="media w-100"> <img class="media-object d-flex align-self-start mr-3" riot-src="{user.profile_pic}"> <div class="media-body"> <button if="{user.user_viewing_follow_them && user.follow_button}" class="btn btn-primary follow-btn btn-sm float-right" userid="{user.id}" main-follow-btn="false"><span class="icon icon-check"></span> Following</button> <button if="{!user.user_viewing_follow_them && user.follow_button}" class="btn btn-primary follow-btn btn-sm float-right" userid="{user.id}" main-follow-btn="false"><span class="icon icon-add-user"></span> Follow</button> <strong>{user.name}</strong><p><small>Followers: {user.followers} | Points {user.points}</small></p> </div> </div> </li> </div>', '', '', function(opts) {
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data) {
      opts.users = data
      console.log(data)
      this.update()
    })
});
