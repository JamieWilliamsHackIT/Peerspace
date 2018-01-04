riot.tag2('notification', '<div each="{notif in opts.notifs}"> <li class="list-group-item media p-4 notification"> <div class="media-body"><small class="text-muted float-right" if="{notif.time_ago < 60}">{Math.round(notif.time_ago)} second<span if="{Math.round(notif.time_ago) !== 1}">s</span> ago</small> <div class="media-body"><small class="text-muted float-right" if="{notif.time_ago >= 60 && notif.time_ago < 3600}">{Math.round(notif.time_ago / 60)} min<span if="{Math.round(notif.time_ago / 60) !== 1}">s</span> ago</small> <div class="media-body"><small class="text-muted float-right" if="{notif.time_ago >= 3600 && notif.time_ago < (24 * 3600)}">{Math.round(notif.time_ago / 3600)} hour<span if="{Math.round(notif.time_ago / 3600) !== 1}">s</span> ago</small> <div class="media-body"><small class="text-muted float-right" if="{notif.time_ago >= (24 * 3600)}">{Math.round(notif.time_ago / (24 * 3600))} day<span if="{Math.round(notif.time_ago / (24 * 3600)) !== 1}">s</span> ago</small> <div class="media-heading"> <a class="user-link" href="/users/{notif.user_tx_id}"><img riot-src="{notif.user_tx_pic_url}"><strong>{notif.user_tx_name}</strong></a> <span if="{notif.type == \'like\'}"> liked your <a href="/posts/{notif.post_id}">post</a></span> <span if="{notif.type == \'comment\'}"> commented on your <a href="/posts/{notif.post_id}">post</a></span> <p if="{notif.type == \'comment\'}" style="display: block; margin-left: 32px; color: grey; font-style: italic;" class="my-1"><small>"{notif.comment}"</small></p> <span if="{notif.type == \'verified\'}"> verified your <a href="/posts/{notif.post_id}">post</a><p style="display: block; margin-left: 32px;"><small>{notif.post_title}</small></p> </div> </div> </li> </div>', '', '', function(opts) {
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data) {
      opts.notifs = data

      this.update()
    })
});
