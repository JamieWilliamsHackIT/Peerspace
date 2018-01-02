<leaderboard>
  <li each={slot in opts.slots} class="slot">
    <img class="profile-pic" src="{slot.profile_pic_url}"><span class="username ml-2">{slot.name}</span>
    <div class="stats">
      <span class="text-muted icon icon-globe mr-1 text-center"></span>
      <span class="text-muted icon icon-medal ml-3 mr-1 text-center"></span>{slot.points}
      <span class="text-muted icon icon-check ml-3 mr-1 text-center"></span>{slot.completion_index}
    </div>
  </li>
  <script>
    this.on('mount', function() {
      opts.callback(this)
    })
    this.on('data_loaded', function(data, user_id) {
      // console.log(data)
      opts.slots = data
      // root_url = 'http://127.0.0.1:8000'
      // root_url = 'https://peerspace.herokuapp.com'
      root_url = 'https://www.peerspace.io'
      this.update()
    })
  </script>
</leaderboard>
