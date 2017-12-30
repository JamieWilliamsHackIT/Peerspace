# Input: a user
# Output: a prediction of the most relevent posts

# Get the user's tags
# Get the post's tags
# Compare tags
# If tags match multiply score by tag's weight
# Multiply score by output of the date relevance function

from users.models import UserPreferenceTag
from users.models import User
from posts.models import Post

from django.shortcuts import get_object_or_404

import math
import random
import decimal

def get_most_relevent(user_pk, page_number, page_size):

    # Get user's information
    user = get_object_or_404(User, pk=user_pk)
    #Get all user's tags
    user_tags = UserPreferenceTag.objects.filter(user=user_pk)
    # Get all posts (in last x amount of time)
    post_slice1 = (page_number * page_size)
    post_slice2 = (page_number * page_size) + 10
    posts = Post.objects.order_by('-created_at')[post_slice1:post_slice2]

    # The slicing prevents the algorithm from re-running on the same posts twice

    # E.g.

    # No slicing
    # post_ids:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...]
    # first run:  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  ^  ^  ^  ^  ^  ^  ^  ^

    # With slicing
    # post_ids:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...]
    # first run:  ^ ^ ^ ^ ^ ^ ^ ^ ^

    # post_ids:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...]
    # second run:                   ^  ^  ^  ^  ^  ^  ^  ^  ^

    # Gives a list of all the user's tags
    user_tag_list = [tag.tag.lower() for tag in user_tags]

    # Initialise the results dictionary
    score_dict = {}
    runtimes = 0
    for post in posts:
        runtimes += 1
        # Initialise some varibles
        total_score = 0
        tag_score = 0
        num_tags_match = 0
        count = 0
        follower_tag_count = 0
        num_days = post.time_since_creation
        does_follow = False

        # Get the user object of the owner of the post
        post_owner = get_object_or_404(User, pk=post.user.id)

        # If the user follows the post owner then increase the relevance with each
        # preference tag that matches
        if post_owner in user.following.all():
            # Even if no preference tags match, increase base relevance
            tag_score = 0.15

            does_follow = True

            # Get post_owner's tags
            post_owner_tags = UserPreferenceTag.objects.filter(user=post_owner)
            post_owner_tags = [tag.tag.lower() for tag in post_owner_tags]

            # Add to the tag_score if any posts match
            for tag in post_owner_tags:
                if tag in user_tag_list:
                    tag_score += (1 / (1 + math.exp(-user_tags[count].weight)))
                    # print('Tag weigth: ', user_tags[count].weight, '+ ', (1 / (1 + math.exp(-user_tags[count].weight))) )
                follower_tag_count += 1
            # print(tag_score)
        # Get all of the current post's tags
        post_tag_list = post.tags.split(", ")
        # Lower case all tags with a list comprehension
        post_tag_list = [tag.lower() for tag in post_tag_list]
        for user_tag in user_tag_list:
            if user_tag in post_tag_list:
                # Normalise the weight (make sure it is in range 0 to 1) by using
                # the logistic sigmoid
                tag_score += (1 / (1 + math.exp(-user_tags[count].weight)))
                num_tags_match += 1
            count += 1
        # print(tag_score)

        if not num_tags_match:
            # If no tags match then give the post a random score. This may
            # introduce the user to a new area of interest
            wildcard_score = (random.random() * 0.4) + tag_score
            # This is the same date relevance and normalisation process as seen
            # below
            wildcard_score *= math.exp((-1/4) * num_days)
            total_relevance = 1 / (1 + math.exp(-wildcard_score))
            score_dict.update({post.id: total_relevance})
        else:
            total_relevance = decimal.Decimal(tag_score)
            # Multiply the total relevance by a funtion that is large for a
            # small number of days and small for a large number of days
            total_relevance *= decimal.Decimal(math.exp((-1/4) * num_days))
            # Output scores to a dictionary
            score_dict.update({post.id: total_relevance})
        # This line is extremely useful for development purposes.
        # print(('Id: {}, title: {}, score: {}. {} tags matched. User follows: {} and {} follower tags matched. Posted {} days(s) ago.').format(
        #                                                                                                             post.id,
        #                                                                                                             post.title,
        #                                                                                                             total_relevance,
        #                                                                                                             num_tags_match,
        #                                                                                                             does_follow,
        #                                                                                                             follower_tag_count,
        #                                                                                                             num_days,
        #                                                                                                         )
        #         )

    # Order score_dict by value and give an ordered list of post ids
    output = {}
    sorted_score_dict = sorted(score_dict, key=score_dict.__getitem__)
    for k in sorted_score_dict:
        output.update({k: score_dict})
    post_ids = list(output.keys())
    post_ids = post_ids[::-1]
    print(post_ids, runtimes)

    # When considering efficieny this function queries the database 2 + n times
    # where n is the number of posts in the last 10 days

    return post_ids
