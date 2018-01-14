riot.tag2('conversations', '<div each="{convo in opts.convos}"> <li class="list-group-item conversation conversation-{convo.id} mb-2" data-id="{convo.id}" user-id="{convo.user.id}" display-user="{convo.user.name}"> <div class="media w-100"> <img class="media-object rounded-circle mr-3 profile-pic" riot-src="{convo.user.profile_pic_url}"> <div class="media-body align-self-center"> <strong>{convo.user.name}</strong> <small></small> </div> </div> </li> </div>', '', '', function(opts) {
    this.on('mount', function() {
      opts.callback(this)
    });;
    this.on('data_loaded', function(data) {
      opts.convos = data;;
      this.update()
    })
});
