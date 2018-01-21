// Gets comments
var commentData = [{}];
var commentsPageNumber = {};


function updateComments(comments, postId) {
    console.log(comments);
    $.each(comments, function(i,e) {
        var commentHTML = '<li class="media comment-block py-3" commentid=' + e.comment_id + '>';
        commentHTML += '<img class="media-object comment-pic d-flex align-self-start mr-3" src="' + e.user_pic_url + '">'
        commentHTML += '<div class="media-body">'
        commentHTML += '<strong>' + e.user_name + ': </strong>'
        commentHTML += e.comment
        if (vars.userId == e.user_id) {
            //Handle the deleting of comments here
            commentHTML += '</div><button class="btn delete-comment-btn delete-comment-btn-' + e.comment_id + ' btn-outline-danger" style="float:right; padding:0px 3px;" href="#" onClick="deleteComment('+ e.comment_id +',' + postId + ')"><span class="icon icon-cross"></span></button>'
        }
        commentHTML += '</li>'
        if (comments.length > i + 1) {
            commentHTML += '<hr>'
        }
        $('.comment-list-' + postId).append(commentHTML)
    })
}


function getComments(postId) {
    if (commentData[postId] === undefined) {
        $.ajax({
            type: "GET",
            url: "/posts/api/v1/" + postId + "/comment/0/",
            dataType: "json",
            success: function (comments) {
                commentData[postId] = {
                    comments: comments.comments,
                    total: comments.total
                }
                $('.comment-list-' + postId).html('')
                if (comments.length == 0) {
                    $('.comment-form-' + postId).fadeIn()
                }
                $('.comment-btn-' + postId).html('<span class="icon icon-message"></span> Comment (' + commentData[postId].total + ')')
                $('.comment-container-' + postId).fadeIn()
                $('.comment-form-' + postId).fadeIn();
                console.log(commentData);
                updateComments(commentData[postId].comments, postId)
            }
        });
    } else {
        console.log(commentData);
        updateComments(commentData[postId].comments, postId)
    }
}


$(document).on('click', '.comment-btn', function(e) {
    // Stop the page refreshing when the button is clicked
    e.preventDefault();
    var postId = $(this).attr("post-id");
    var commentsOpen = $('.comment-container-' + postId).attr('commentsopen');
    if (commentsOpen == 'true') {
        $('.comment-container-' + postId).fadeOut(function() {
            $('.comment-container-' + postId).attr('commentsopen', 'false');
            $('.comment-btn-' + postId).css('color', 'grey')
        });
        $('.comment-form-' + postId).fadeOut()
    } else {
        $('.comment-container-' + postId).attr('commentsopen', 'true');
        $('.comment-btn-' + postId).css('color', '#007bff');
        $('.comment-form-' + postId).fadeIn();
        $('.comment-container-' + postId).fadeOut();
        getComments(postId)
    }
});





// Opens comment section
$(document).on('click', '.comment-btn', function(e) {
    //Stop the page refreshing when the button is clicked
    e.preventDefault();
    const postId = $(this).attr("post-id");
    console.log(postId);
    const commentsOpen = $('.comment-container-' + postId).attr('commentsopen');
    $('.comment-form-' + postId).fadeOut()
    $('.comment-container').fadeOut(function() {
        $('.comment-btn-' + postId).css('color', 'grey')
    });
    $('.comment-btn-' + postId).css('color', '#007bff');
    getComments(postId, vars.userId)



    $('.comment-form').fadeOut();
    $('.comment-container').fadeOut(function() {
        $('.comment-btn-' + postId).css('color', 'grey')
    });
    if (commentsOpen === 'true') {
        $('.comment-container-' + postId).attr('commentsopen', 'false');
        $('.comment-form-' + postId).fadeOut();
    } else {
        $('.comment-container-' + postId).attr('commentsopen', 'true');
        $('.comment-btn-' + postId).css('color', '#007bff');
        $('.comment-container-' + postId).fadeIn();
        $('.comment-form-' + postId).fadeIn()
        console.log(postId)
        getComments(postId, vars.userId)
    }
});






function getComments(postId, userId) {
    if ($('.comment-list-' + postId).find('comments').length === 0) {
        $('.comment-list-' + postId).append('<comments class="js-comments-tag-' + postId + '"></comments>');
    }
    console.log(postId)
    riot.mount('.js-comments-tag-' + postId, {callback:commentsCallBack, postId:postId, userId:userId});
}















function commentsCallBack(theTag, postId, userId) {
    console.log('Callback', postId, userId)

    function updateComments(commentData) {
        console.log(commentData);
        theTag.trigger('data_loaded', commentData[postId].comments, postId, userId);
        $('.js-comments-stat-' + postId).html('');
        if (commentData[postId].comments.length) {
            //console.log(commentData[postId])
            $('.js-comments-stat-' + postId).html('<span class="icon icon-message ml-1"> ' + commentData[postId].comments[0].total)
        } else {
            $('.js-comments-stat-' + postId).html('')
        }

    }

    commentsPageNumber[postId] = 0;
    if (commentData[postId] === undefined) {
        $.ajax({
            type: "GET",
            url: "/posts/api/v1/" + postId + "/comment/0/",
            dataType: "json",
            success: function (comments) {
                commentData[postId] = {
                    comments: [],
                    total: 0
                };
                commentData[postId].comments = comments.comments;
                commentData[postId].total = comments.total;
                updateComments(commentData)
            }
        });
    } else {
        updateComments(commentData)
    }

    $(document).on('click', '.js-load-comments-' + postId, function(e) {
        commentsPageNumber[postId]++;
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: "/posts/api/v1/" + postId + "/comment/" + commentsPageNumber[postId] + "/",
            dataType: "json",
            success: function (comments) {
                $.each(comments.comments, function(i, comment) {
                    commentData[postId].comments.push(comment);
                });
                console.log(commentData);
                theTag.trigger('data_loaded', commentData[postId].comments, postId, userId);
            }
        })
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
                url: "/posts/api/v1/" + postId + "/comment/0/",
                method: "POST",
                data: data,
                success: function(comment) {
                    commentData[postId].comments.unshift(comment);
                    updateComments(commentData)
                }
            });
            $(this).val('')
        }
    });

    // Deletes a comment
    $(document).on('click', '.delete-comment-btn', function(e) {
        console.log('runs')
        console.log(commentData);
        e.preventDefault();
        var commentId = $(this).attr('data-comment-id');
        var postId = $(this).attr('data-post-id');
        $.ajax({
            url: "/posts/api/v1/comments/" + commentId + "/",
            type: "DELETE",
            // This MUST be in the callback due to the asynchronous nature of javascript
            success: function() {
                // Remove the comment from the object
                commentData[postId].comments = $.grep(commentData[postId]['comments'], function(e) {
                    return e.comment_id != commentId
                });
                //console.log(commentData)
                updateComments(commentData)
            }
        });
    });
}