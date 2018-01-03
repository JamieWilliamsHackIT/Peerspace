riot.tag2('conversation', '<div each="{message in opts.messages}"> <li if="{message.user_id == user_id}" class="media media-current-user mb-4"> <div class="media-body"> <div class="media-body-text"> {message.body} </div> <div class="media-footer"> <small class="text-muted"> <a href="/users/{message.user_id}">{message.user_name}</a> at {message.created_at} </small> </div> </div> <img class="rounded-circle media-object ml-3" riot-src="{message.profile_pic_url}"> </li> <li if="{message.user_id !== user_id}" class="media mb-4"> <img class="rounded-circle media-object mr-3" riot-src="{message.profile_pic_url}"> <div class="media-body"> <div class="media-body-text"> {message.body} </div> <div class="media-footer"> <small class="text-muted"> <a href="/users/{message.user_id}">{message.user_name}</a> at {message.created_at} </small> </div> </div> </li> </div>', '', '', function(opts) {
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data, user_id) {
      opts.messages = data
      console.log(data)
      this.update()
    })
});
