<conversations>
  <div each={convo in opts.convos}>
    <li class="list-group-item conversation" data-id={convo.id}>
      <div class="media w-100">
        <img class="media-object rounded-circle mr-3" src="{convo.users[1].profile_pic_url}">
        <div class="media-body align-self-center">
          <strong>{convo.name}</strong>
          <small></small>
        </div>
      </div>
    </li>
  </div>
  <script>
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data, user_id) {
      opts.convos = data
      this.update()
    })
  </script>
</conversations>
