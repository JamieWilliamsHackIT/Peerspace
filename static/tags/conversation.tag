<conversation>
  <div each={message in opts.messages}>
    <li if={message.user_id == userId} class="media media-current-user mb-4">
      <div class="media-body">
        <div class="media-body-text">
          {message.body}
        </div>
        <div class="media-footer">
          <small class="text-muted">
            <a href="/users/{message.user_id}">{message.user_name}</a>
            <div style="display: inline;" if={message.time_ago < 60}> {Math.round(message.time_ago)} second<span if={Math.round(message.time_ago) !== 1}>s</span> ago</div>
            <div style="display: inline;" if={message.time_ago >= 60 && message.time_ago < 3600}> {Math.round(message.time_ago / 60)} min<span if={Math.round(message.time_ago / 60) !== 1}>s</span> ago</div>
            <div style="display: inline;" if={message.time_ago >= 3600 && message.time_ago < (24 * 3600)}> {Math.round(message.time_ago / 3600)} hour<span if={Math.round(message.time_ago / 3600) !== 1}>s</span> ago</div>
            <div style="display: inline;" if={message.time_ago >= (24 * 3600)}> {Math.round(message.time_ago / (3600 * 24))} day<span if={Math.round(message.time_ago / (3600 * 24)) !== 1}>s</span> ago</div>
          </small>
        </div>
      </div>
      <img class="rounded-circle media-object ml-3 profile-pic" src="{message.profile_pic_url}">
    </li>
    <li if={message.user_id !== userId} class="media mb-4">
      <img class="rounded-circle media-object mr-3 profile-pic" src="{message.profile_pic_url}">
      <div class="media-body">
        <div class="media-body-text">
          {message.body}
        </div>
        <div class="media-footer">
          <small class="text-muted">
            <a href="/users/{message.user_id}">{message.user_name}</a>
            <div style="display: inline;" if={message.time_ago < 60}> {Math.round(message.time_ago)} second<span if={Math.round(message.time_ago) !== 1}>s</span> ago</div>
            <div style="display: inline;" if={message.time_ago >= 60 && message.time_ago < 3600}> {Math.round(message.time_ago / 60)} min<span if={Math.round(message.time_ago / 60) !== 1}>s</span> ago</div>
            <div style="display: inline;" if={message.time_ago >= 3600 && message.time_ago < (24 * 3600)}> {Math.round(message.time_ago / 3600)} hour<span if={Math.round(message.time_ago / 3600) !== 1}>s</span> ago</div>
            <div style="display: inline;" if={message.time_ago >= (24 * 3600)}> {Math.round(message.time_ago / (3600 * 24))} day<span if={Math.round(message.time_ago / (3600 * 24)) !== 1}>s</span> ago</div>
          </small>
        </div>
      </div>
    </li>
  </div>
  <script>
    this.on('mount', function() {
      opts.callback(this)
    });
    this.on('data_loaded', function(data, userId) {
      opts.messages = data;
      this.update()
    })
  </script>
</conversation>
