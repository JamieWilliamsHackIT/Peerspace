function post(user_id)
// Will fade the delete button in and out when the user hovers over their own comment
$(document).on('mouseenter', '.comment-block', function() {
  var comment_id = $(this).attr('commentid')
  $('.delete-comment-btn-' + comment_id).fadeIn();
})
$(document).on('mouseleave', '.comment-block', function() {
  var comment_id = $(this).attr('commentid')
  $('.delete-comment-btn-' + comment_id).fadeOut();
})
function tagCallBack(theTag) {
  //Gets posts
  $.ajax({
    type: "GET",
    url: root_url + "/posts/api/v1/feed/" + user_id,
    dataType: 'json',
    success: function(data) {
      user_id = {{ user.id }}
      theTag.trigger('data_loaded', data, user_id)
    }
  });
}
function deleteComment(comment_id, post_id) {
  $.ajax({
    url: root_url + "/posts/api/v1/comments/" + comment_id,
    type: "DELETE",
    // This MUST be in the callback due to the asynchronus nature of javascript
    success: function() {getComments(post_id)}
  })
}
function getComments(post_id) {
  //Gets comments
  $.ajax({
    type: "GET",
    url: root_url + "/posts/api/v1/" + post_id + "/comment",
    dataType: "json",
    success: function(comments) {
      $('.comment-list-' + post_id).html('')
      if (comments.length == 0) {
        $('.comment-form-' + post_id).fadeIn()
      }
      $.each(comments, function(i,e) {
        var commentHTML = '<li class="media comment-block py-3" commentid=' + e.comment_id + '>';
        commentHTML += '<img class="media-object comment-pic d-flex align-self-start mr-3" src="' + e.user_pic_url + '">'
        commentHTML += '<div class="media-body">'
        commentHTML += '<strong>' + e.user_name + ': </strong>'
        commentHTML += e.comment
        if ({{user.id}} == e.user_id) {
          //Handle the deleting of comments here
          commentHTML += '</div><button class="btn delete-comment-btn delete-comment-btn-' + e.comment_id + ' btn-outline-danger" style="float:right; padding:0px 3px;" href="#" onClick="deleteComment('+ e.comment_id +',' + post_id + ')"><span class="icon icon-cross"></span></button>'
        }
        commentHTML += '</li>'
        if (comments.length > i + 1) {
          commentHTML += '<hr>'
        }
        $('.comment-list-' + post_id).append(commentHTML)
      })
      // I can get the callback from a function by calling it in a console.log()
      $('.comment-btn-' + post_id).html('<span class="icon icon-message"></span> Comment (' + comments.length + ')')
      $('.comment-container-' + post_id).fadeIn()
      $('.comment-form-' + post_id).fadeIn()
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
      url: root_url + "/posts/api/v1/" + this_button.attr('id') + "/like",
      method: "GET",
      data: {},
      success: function(data) {
        if (data.liked) {
          this_button.css('color', '#007bff')
          this_button.html('<span class="icon icon-thumbs-up"></span> Liked (' + data.likes + ')')
        } else {
          this_button.css('color', 'grey')
          this_button.html('<span class="icon icon-thumbs-up"></span> Like (' + data.likes + ')')
        }
      }
    })
  })
  //Sends comment
  $(document).on("keydown", ".comment", function (e) {
      if (e.which == 13 && $(this).val()) {
        post_id = $(this).attr("post-id")
        var data = {
          comment: $(this).val(),
          post: post_id
        }
        $.ajax({
          url: root_url + "/posts/api/v1/" + post_id + "/comment",
          method: "POST",
          data: data,
          success: function(data) {
            //Load all comments
            getComments(post_id)
          }
        })
        $(this).val('')
      }
  })
  $(document).on('click', '.comment-btn', function(e) {
    // Stop the page refreshing when the button is clicked
    e.preventDefault()
    post_id = $(this).attr("post-id")
    commentsOpen = $('.comment-container-' + post_id).attr('commentsopen')
    if (commentsOpen == 'true') {
      $('.comment-container-' + post_id).fadeOut(function() {
        $('.comment-container-' + post_id).attr('commentsopen', 'false')
        $('.comment-btn-' + post_id).css('color', 'grey')
      })
      $('.comment-form-' + post_id).fadeOut()
    } else {
      $('.comment-container-' + post_id).attr('commentsopen', 'true')
      $('.comment-btn-' + post_id).css('color', '#007bff')
      getComments(post_id)
    }
  })
  // Sends verification
  $(document).on('click', '.verify-btn', function(e) {
    e.preventDefault()
    post_id = $(this).attr("post-id")
    this_button = $(this)
    $.ajax({
      url: root_url + "/posts/api/v1/" + post_id + "/verify",
      method: "GET",
      dataType: "json",
      success: function(data) {
        if (data.verified_user) {
          this_button.css('color', '#007bff')
          this_button.html('<span class="icon icon-shield"></span> Verified (' + data.verifications + '/5)')
        } else {
          this_button.css('color', 'grey')
          this_button.html('<span class="icon icon-shield"></span> Verify (' + data.verifications + '/5)')
        }
        if (data.verifications >= 5) {
          $('.verify-btn-' + post_id).hide()
          $('.awaiting-verifcation-' + post_id).hide()
          var statusHTML = '<p class="float-right completion-status completed-{post.id} mr-3 pt-1" style="color: green;"><span class="icon icon-check"></span> Completed</p>'
          $('.completion-status-container-' + post_id).html(statusHTML)
        }
      }
    })
  })
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
      url: root_url + "/posts/api/v1/",
      data: data,
      success: function(postData) {
        riot.mount('post-feed', {callback:tagCallBack})
        $('#title').val('')
        $('#desc').val('')
        $("#tags").tagit("removeAll");
      }
    });
  })
})
