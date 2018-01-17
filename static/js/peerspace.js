var vars = sendVar()

if (vars.tags) { $('#tags').tagit() }

if (vars.page === 'postFeed' || vars.page === 'profileUser') {
    riot.mount('post-feed', {callback:postFeedCallBack});
    riot.mount('follower', {callback:followerCallBack})
} else if (vars.page === 'postDetail') {
    riot.mount('post-feed', {callback:postFeedCallBack})
}


// Gets comments
function getComments(postId, userId) {
    $.ajax({
        type: "GET",
        url: "/posts/api/v1/" + postId + "/comment/",
        dataType: "json",
        success: function(comments) {
            $('.comment-list-' + postId).html('');
            if (comments.length === 0) {
                $('.comment-form-' + postId).fadeIn()
            }
            $.each(comments, function(i,e) {
                var commentHTML = '<li class="media comment-block py-3" commentid=' + e.comment_id + '>';
                commentHTML += '<img class="media-object comment-pic d-flex align-self-start mr-3" src="' + e.user_pic_url + '">';
                commentHTML += '<div class="media-body">';
                commentHTML += '<strong>' + e.user_name + ': </strong>';
                commentHTML += e.comment;
                if (userId === e.user_id) {
                    //Handle the deleting of comments here
                    commentHTML += '</div><button class="btn delete-comment-btn delete-comment-btn-' + e.comment_id + ' btn-outline-danger" style="float:right; ';
                    commentHTML += 'padding:0px 3px;" href="#" onClick="deleteComment('+ e.comment_id +',' + postId + ',' + userId + ')"><span class="icon icon-cross"></span></button>'
                }
                commentHTML += '</li>';
                if (comments.length > i + 1) {
                    commentHTML += '<hr>'
                }
                // I can get the callback from a function by calling it in a console.log()
                $('.comment-list-' + postId).append(commentHTML)
            });
            $('.js-comments-stat-' + postId).html('');
            if (comments.length) {
                $('.js-comments-stat-' + postId).html('<span class="icon icon-message"> ' + comments.length)
            } else {
                $('.js-comments-stat-' + postId).html('')
            }
            $('.comment-container-' + postId).fadeIn();
            $('.comment-form-' + postId).fadeIn()
        }
    });
}


// Deletes a comment
function deleteComment(commentId, postId, userId) {
    $.ajax({
        url: "/posts/api/v1/comments/" + commentId + "/",
        type: "DELETE",
        // This MUST be in the callback due to the asynchronous nature of javascript
        success: function() {getComments(postId, userId)}
    });
}


//Sends like
$(document).ready(function() {
    $(document).on('click', '.like-btn', function(e) {
        // Stop the page refreshing when the button is clicked
        e.preventDefault();
        const this_button = $(this);
        $.ajax({
            url: "/posts/api/v1/" + this_button.attr('id') + "/like/",
            method: "GET",
            dataType: "json",
            success: function(data) {
                if (data.likes) {
                    $('.js-likes-stat-' + this_button.attr('id')).html('<span class="icon icon-heart"> ' + data.likes)
                } else {
                    $('.js-likes-stat-' + this_button.attr('id')).html('')
                }
                if (data.liked) {
                    this_button.css('color', '#007bff');
                    this_button.html('<span class="icon icon-heart"></span> Like');
                } else {
                    this_button.css('color', 'grey');
                    this_button.html('<span class="icon icon-heart-outlined"></span> Like')
                }
            }
        })
    });
});


// Opens comment section
$(document).on('click', '.comment-btn', function(e) {
    //Stop the page refreshing when the button is clicked
    e.preventDefault();
    const postId = $(this).attr("post-id");
    const commentsOpen = $('.comment-container-' + postId).attr('commentsopen');
    if (commentsOpen === 'true') {
        $('.comment-container-' + postId).fadeOut(function() {
            $('.comment-container-' + postId).attr('commentsopen', 'false');
            $('.comment-btn-' + postId).css('color', 'grey')
        });
        $('.comment-form-' + postId).fadeOut()
    } else {
        $('.comment-container-' + postId).attr('commentsopen', 'true');
        $('.comment-btn-' + postId).css('color', '#007bff');
        getComments(postId, vars.userId)
    }
});


//Sends comment
$(document).on("keydown", ".comment", function (e) {
    if (e.which === 13 && $(this).val()) {
        const postId = $(this).attr("post-id");
        var data = {
            comment: $(this).val(),
            post: postId
        };
        $.ajax({
            url: "/posts/api/v1/" + postId + "/comment/",
            method: "POST",
            data: data,
            success: function() {
                //Load all comments
                getComments(postId, vars.userId)
            }
        });
        $(this).val('')
    }
});


// Will fade the delete button in and out when the user hovers over their own comment
$(document).on('mouseenter', '.comment-block', function() {
    var commentId = $(this).attr('commentid');
    $('.delete-comment-btn-' + commentId).fadeIn();
});
$(document).on('mouseleave', '.comment-block', function() {
    var commentId = $(this).attr('commentid');
    $('.delete-comment-btn-' + commentId).fadeOut();
});


// Sends verification
$(document).on('click', '.verify-btn', function(e) {
    e.preventDefault();
    const postId = $(this).attr("post-id");
    const this_button = $(this);
    $.ajax({
        url: "/posts/api/v1/" + postId + "/verify/",
        method: "GET",
        dataType: "json",
        success: function(data) {
            if (data.verified_user) {
                this_button.css('color', '#007bff');
                this_button.html('<span class="icon icon-shield"></span> Verified (' + data.verifications + '/5)')
            } else {
                this_button.css('color', 'grey');
                this_button.html('<span class="icon icon-shield"></span> Verify (' + data.verifications + '/5)')
            }
            if (data.verifications >= 5) {
                $('.verify-btn-' + postId).hide();
                $('.awaiting-verifcation-' + postId).hide();
                var statusHTML = '<p class="float-right completion-status completed-{post.id} mr-3 pt-1" style="color: green;"><span class="icon icon-check"></span> Completed</p>';
                $('.completion-status-container-' + postId).html(statusHTML)
            }
        }
    })
});


// Callback for post-feed tag
function postFeedCallBack(theTag) {
    var postData = [];
    var postIds = [];
    var pageNumber = 0;
    var url;
    var reachedBottom = false;
    // Gets posts
    if (vars.page === 'postFeed') {
        url = "/posts/api/v1/feed/" + vars.userId + "/0/"
    } else if (vars.page === 'profileUser') {
        url = "/posts/api/v1/profile/" + vars.userId + "/0/"
    } else if (vars.page === 'postDetail') {
        url = "/posts/api/v1/detail/" + vars.userId + "/" + vars.postId + "/";
        reachedBottom = true
    }
    $.ajax({
        type: "GET",
        url: url,  // Start with page 0 (the first page)
        dataType: 'json',
        success: function(data) {
            postData = data;
            $.each(postData, function(i, post) {
                postIds.push(post.id)
            });
            theTag.trigger('data_loaded', data, vars.userId);
            $('.loading-circle-posts').hide()
        }, error: function() {
            console.log('Error loading posts...')
        }
    });
    $(window).scroll(function() {
        var toScroll = $(document).height() - $(window).height() - 100;
        if ($(this).scrollTop() > toScroll && !reachedBottom) {
            pageNumber++;
            reachedBottom = true;
            //Show loading gif
            $('.loading-circle-posts').show();
            //Gets more posts
            $.ajax({
                type: "GET",
                url: url + pageNumber + "/",
                dataType: 'json',
                success: function(data) {
                    $.each(data, function(i, post) {
                        if ($.inArray(post.id, postIds) === -1) {
                            postData.push(post)
                        }
                    });
                    if (data.length === 10) {
                        reachedBottom = false
                    } else {
                        reachedBottom = true;
                        console.log('No more posts')
                    }
                    theTag.trigger('data_loaded', postData, vars.userId);
                    //Hide loading gif
                    $('.loading-circle-posts').hide()
                }, error: function() {
                    console.log('Error loading posts...')
                }
            })
        }
    });
    // Sends post
    $('#post').click(function(e) {
        // Get the entered tags as a list
        var tags = $("#tags").tagit("assignedTags");
        var data = {
            user: vars.userId,
            title: $('#title').val(),
            description: $('#desc').val(),
            tags: tags.join(', '),
            deadline: $('#deadline').val()
        };
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/posts/api/v1/",
            data: data,
            success: function(data) {
                postData.unshift(data);
                pageNumber = 0;
                theTag.trigger('data_loaded', postData, vars.userId);
                $('#title').val('');
                $('#desc').val('');
                $("#tags").tagit("removeAll");
                $('.form-group-hidden').hide()
            }
        });
    });

    // Shows post form
    var formGroup = $('.form-group-hidden').hide();
    $(document).on('focus', '#title', function() {
        formGroup.fadeIn()
    });
    // Hides post form
    $(document).on('click', '#cancel-post', function(e) {
        e.preventDefault();
        $('.form-group-hidden').fadeOut()
    });
    // User search
    $(document).on("keydown", ".search-input", function (e) {
        if (e.which === 13 && $(this).val()) {
            e.preventDefault();
            var searchTerm = $('.search-input').val();
            if (searchTerm) {
                // Show loading circle
                $('.loading-circle-posts').show();
                $('.no-search-results').hide();
                // Get search term
                var pageSize = 10;
                $('.create-post').hide();
                $.ajax({
                    type: "GET",
                    url: "/search/" + vars.userId + "/" + searchTerm + "/" + pageSize + "/",
                    dataType: 'json',
                    success: function(data) {
                        if (!data.length) {
                            $('.no-search-results').show()
                        } else {
                            $('.no-search-results').hide()
                        }
                        theTag.trigger('data_loaded', data, vars.userId);
                        $('.loading-circle-posts').hide()
                    }, error: function() {
                        console.log('Error searching for posts...')
                    }
                })
            }
        }
    })
}


// Callback for follower tag
function followerCallBack(theTag) {
    var followerData = [];
    var pageNumberFollowers = 0;
    var reachedBottomFollowers = false;
    var type;
    // Handle the followers and following modals
    $(document).on('click', '#followers, #following', function() {
        $('.loading-circle-followers').show();
        $('#followersModal').modal('toggle');
        // Get all of the user's followers
        var userId = vars.userId;
        type = $(this).attr('data-modal-type');
        pageNumberFollowers = 0;
        reachedBottomFollowers = false;
        $('#followers-modal-content div').remove();
        $.ajax({
            type: "GET",
            url: "/users/api/v2/" + vars.userId + "/followers/" + type + "/" + pageNumberFollowers + "/",
            dataType: "json",
            success: function(data) {
                $.each(data, function(i, user) {
                    followerData.push(user)
                });
                theTag.trigger('data_loaded', followerData);
                $('.loading-circle-followers').hide()
            }
        });
    });
    $('#followers-modal-content').scroll(function() {
        if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight && !reachedBottomFollowers) {
            $('.loading-circle-followers').show();
            pageNumberFollowers++
            reachedBottomFollowers = true;
            //Show loading gif
            $('.loading-circle-followers').show();
            //Gets more posts
            $.ajax({
                type: "GET",
                url: "/users/api/v2/" + vars.userId + "/followers/" + type + "/" + pageNumberFollowers + "/",
                dataType: 'json',
                success: function(data) {
                    $.each(data, function(i, follower) {
                        followerData.push(follower)
                    });
                    if (data.length === 10) {
                        reachedBottomFollowers = false
                    } else {
                        reachedBottomFollowers = true;
                        console.log('No more followers')
                    }
                    theTag.trigger('data_loaded', followerData);
                    //Hide loading gif
                    $('.loading-circle-followers').hide()
                }, error: function() {
                    console.log('Error loading followers...')
                }
            })
        }
    });
    //Sends follow
    $(document).on('click', '.follow-btn', function(e) {
        e.preventDefault();
        var this_button = $(this);
        $.ajax({
            type: "GET",
            url: "/users/api/v2/" + this_button.attr('userid') + "/follow/",
            dataType: "json",
            success: function(data) {
                if (data.following) {
                    this_button.html('<span class="icon icon-check"></span> Following')
                } else {
                    this_button.html('<span class="icon icon-add-user"></span> Follow')
                }
            }
        })
    })
}


// Handles messages
$(document).on('click', '.message-btn', function() {
    $.ajax({
        type: "GET",
        url: "/messages/api/v5/messages/redirect/1/",
        dataType: "json",
        success: function(data) {
            window.location.href = "/messages/" + data.conversation_id
        }
    })
});


// Get user proof images
if (vars.page === 'profileUser') {
    $.ajax({
        url: "/posts/api/v1/proof_images/" + vars.userId + "/10/",
        method: "GET",
        dataType: "json",
        success: function(data) {
            $.each(data, function(i, e) {
                $('.images').append('<img href="' + e.post_url + '" class="img-fluid image" style="padding: 10px;" data-width="' + e.proof_pic_width + '" data-height="' + e.proof_pic_height + '" src="' + e.proof_pic_url + '">')
            });
            $('.loading-circle-images').hide()
        }
    });
}


$(document).on('click', '.image', function() {
    window.location.href = ($(this).attr('href')).toString();
});


// Sends motivations
$(document).on('click', '.motivate-btn', function(e) {
    e.preventDefault()
    var this_button = $(this);
    var postId = this_button.attr('post-id');
    $.ajax({
        type: "GET",
        url: "/posts/api/v1/" + postId + "/motivate/",
        dataType: "json",
        success: function(data) {
            if (data.motivations) {
                $('.js-motivations-stat-' + postId).html('<span class="icon icon-flash">' + data.motivations);
                this_button.css('color', '#007bff')
            } else {
                $('.js-motivations-stat-' + postId).html('');
                this_button.css('color', 'grey')
            }
        }
    })
});
