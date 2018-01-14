<leaderboard>
  <div each={slot in opts.slots}>
    <li if={slot.id == user_id} class="slot slot-user">
      <a href="/users/{slot.id}"><img class="profile-pic" src="{slot.profile_pic_url}"><span class="username ml-2">{slot.name}</a></span>
      <div class="stats">
        <span class="text-muted icon icon-globe mr-1 text-center"></span>{slot.position}
        <span class="text-muted icon icon-medal ml-3 mr-1 text-center"></span>{slot.points}
        <span class="text-muted icon icon-check ml-3 mr-1 text-center"></span>{slot.completion_index}
      </div>
    </li>
    <li if={slot.id !== user_id} class="slot">
      <a href="/users/{slot.id}"><img class="profile-pic" src="{slot.profile_pic_url}"><span class="username ml-2">{slot.name}</a></span>
      <div class="stats">
        <span class="text-muted icon icon-globe mr-1 text-center"></span>{slot.position}
        <span class="text-muted icon icon-medal ml-3 mr-1 text-center"></span>{slot.points}
        <span class="text-muted icon icon-check ml-3 mr-1 text-center"></span>{slot.completion_index}
      </div>
    </li>
  </div>
  <script>
    this.on('mount', function() {
      opts.callback(this)
    });;
    this.on('data_loaded', function(data, user_id) {
      opts.slots = data;;
      this.update()
    })
  </script>
</leaderboard>
