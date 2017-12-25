var this_js_script = $('script[src*=test.js]'); // or better regexp to get the file name..
var user_id = this_js_script.attr('date-user_id');
if (typeof my_var_1 === "undefined" ) {
}
$("#tags").tagit();
function tagCallBack(theTag) {
  $.ajax({
    type: "GET",
    url: "http://127.0.0.1:8000/posts/api/v1/{{ user.id }}",
    dataType: 'json',
    success: function(posts) {
      user_id = user_id,
      theTag.trigger('data_loaded', posts, user_id)
    }
  });
}
//Sends like
$(document).ready(function() {
  $(document).on('click', '.like-btn', function(e) {
    // Stop the page refreshing when the button is clicked
    e.preventDefault()
    var this_button = $(this)
    $.ajax({
      url: "http://127.0.0.1:8000/posts/api/v1/" + this_button.attr('id') + "/like",
      method: "GET",
      data: {},
      success: function(data) {
        if (data.liked) {
          this_button.css('color', '#007bff')
        } else {
          this_button.css('color', 'grey')
        }
      }, error: function(error) {
        //console.log('Error: ' + error)
      }
    })
  })
})
riot.mount('post-list', {callback:tagCallBack})
$('#post').click(function(e) {
  var tags = $("#tags").tagit("assignedTags");
  var data = {
    user: {{ user.id }},
    title: $('#title').val(),
    description: $('#desc').val(),
    tags: tags.join(", ")
  }
  e.preventDefault()
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8000/posts/api/v1/",
    data: data,
    success: function(postData) {
      riot.mount('post-list', {callback:tagCallBack})
      $('#title').val('')
      $('#desc').val('')
      $("#tags").tagit("removeAll");
    }
  });
})
