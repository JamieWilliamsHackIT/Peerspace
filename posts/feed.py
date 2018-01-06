"""This is the Peerspace post relevance algorithm, it is the brain of Peerspace
----------------------------------------------------------------------------

The function in the file generates the relevance predictions for each post. Its
basic operation:

>   Take a user's id
<   Output a list of posts that are likely to be the relevant to the user

As Peerspace developes this is where most of the work will be done, this
algorithm is currently extremely simple and its predictions rely on data with
large amounts of information such as tags. In the future, alongside Django's
middleware I would like to make the algorithm rely less on user inputed data and
more so on user interaction. This would involve large data sets and ultimetly
some form of machine/deep learning algorithm.

What you see below is the entirity of my datascience knowledge, as I learn more
on the subject I will work to develope this algorithm.

My first step towards building a relevance algorithm that uses interaction data
was to give each user's tag a weight. As the user interacts with posts the weight
will be adjusted as so:

    If a user likes a post, any matching tag's weights will be increased by x

    If a user comments on a post, any matching tag's weights will be increased
    by y

I have made another assumption that y > x as a comment takes more time and
effort to write than it takes to simply like a post.

As users like and comment on posts their tags will be adjusted automatically in
the background, the objective is for the accuracy of the relevance algorithm to
improve as the time goes on. So once the user has been using the site for a
month for example their tag's weights will have adjusted to shape their
experience on the site.

"""

# Standard imports
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Mathematical imports
import math
import random
import decimal

# Import the User, UserPreferenceTag and Post models
from users.models import UserPreferenceTag
from users.models import User
from posts.models import Post

# The algorithm itself
def get_most_relevent(user_pk, page_number, page_size):

    # Get user's information
    user = get_object_or_404(User, pk=user_pk)
    # Get all user's tags
    user_tags = UserPreferenceTag.objects.filter(user=user_pk)
    # Form slices
    post_slice1 = (page_number * page_size)
    post_slice2 = (page_number * page_size) + page_size

    # The slicing prevents the algorithm from re-running on the same posts twice

    # E.g.

    # No slicing: every post's relevance is re-evaluated with each run

    # post_ids:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...]
    # first run:  ^ ^ ^ ^ ^ ^ ^ ^ ^ ^  ^  ^  ^  ^  ^  ^  ^  ^

    # With slicing: only the posts in question will have a relevance score
    # evaluated for them

    # post_ids:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...]
    # first run:  ^ ^ ^ ^ ^ ^ ^ ^ ^

    # post_ids:  [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18...]
    # second run:                   ^  ^  ^  ^  ^  ^  ^  ^  ^

    # Get the posts limited by the slice, this will prevent the algorithm running
    # on every post every time the function runs, this is key as it prevents the
    # server from becoming criplingly slow.

    # The Post.objects.order_by() call returns a queryset, this is NOT data, it
    # simply represents a prepared SQL statement. By slicing the query set this
    # limits the number of queries or hits on the database, thereby increasing
    # efficiency.

    # Get post objects from database
    posts = Post.objects.order_by('-created_at')[post_slice1:post_slice2]

    # Gives a list of all the user's tags. I have lowered each tag to make the
    # comparison case-insensitive
    user_tag_list = [tag.tag.lower() for tag in user_tags]

    # Initialise the results dictionary
    score_dict = {}
    # Runtimes was a performance metric, it stored how many times the function
    # ran, it is not relied on by the algorithm
    # runtimes = 0
    for post in posts:
        # runtimes += 1
        # Initialise some varibles
        total_score = 0
        tag_score = 0
        num_tags_match = 0
        count = 0
        follower_tag_count = 0
        num_days = post.time_since_creation / (3600 * 24)
        does_follow = False

        # Get the user object of the owner of the post
        post_owner = get_object_or_404(User, pk=post.user.id)

        # If the user follows the post owner then increase the relevance with each
        # preference tag that matches
        if post_owner in user.following.all():
            # Even if no preference tags match, increase base relevance. This
            # is based off the assumption that a post by a user that one follows
            # is off a little extra relevance
            tag_score = 0.15

            does_follow = True

            # Get post_owner's tags
            post_owner_tags = UserPreferenceTag.objects.filter(user=post_owner)
            post_owner_tags = [tag.tag.lower() for tag in post_owner_tags]

            # If any of the user's tags match those of the post owner then
            # increase the tag_score by the weight of the tag

            # For of the post owner's tags check if they match any of the user's
            # tags
            for tag in post_owner_tags:
                if tag in user_tag_list:
                    # If they match then increase the tag score. I decided that
                    # the number of that match should have more of an affect
                    # than one tag with a large weight, therefore each tag's
                    # weight is normalised using the logistic sigmoid function
                    # (I have gone through this in more detail in the docs)
                    tag_score += (1 / (1 + math.exp(-user_tags[count].weight)))
                    # print('Tag weigth: ', user_tags[count].weight, '+ ', (1 / (1 + math.exp(-user_tags[count].weight))) )
                follower_tag_count += 1

        # If the post is by the viewing user then ignore the tag system
        if not post.user == user:
            # Get all of the current post's tags
            if post.tags:
                # The tags for each post are stored as a comma-seperated list as
                # they have no weight attribute
                post_tag_list = post.tags.split(", ")
            else:
                post_tag_list = []
            # Make all tags lower case with a list comprehension
            post_tag_list = [tag.lower() for tag in post_tag_list]
        else:
            post_tag_list = []
        # This is a very similar process to the one seen above, it iterates
        # through the user's tags and compares them to the post's tags. If any
        # match then the user tag's weight is normalised and added to the tag
        # score
        for user_tag in user_tag_list:
            if user_tag in post_tag_list:
                # Normalise the weight (make sure it is in range 0 to 1) by using
                # the logistic sigmoid
                tag_score += (1 / (1 + math.exp(-user_tags[count].weight)))
                num_tags_match += 1
            count += 1
        # print(tag_score)

        # I did not want to completely disregard any posts where no tags matched
        # so I introduced a "wildcard score". This is a psuedo random score that
        # is assigned to the post, it means that some posts will appear higher
        # in the user's feed, this may introduce them to a new interest
        if not num_tags_match:
            # If no tags match then give the post a random score. Add the tag
            # score, as even though no post tags matched the score tag may be
            # non-zero as the post may be by someone the user followers and
            # some follower tags may have matched
            wildcard_score = (random.random() * 0.4) + tag_score
            # This is the same date relevance and normalisation process as seen
            # below
            # wildcard_score *= math.exp((-1/4) * num_days)
            if post.proved_at:
                num_days_since_proved = ((timezone.now() - post.proved_at).total_seconds() / (3600 * 24))
                wildcard_score *= math.exp((-1/4) * num_days_since_proved)
            else:
                wildcard_score *= (math.exp((-1/4) * num_days))
            total_relevance = wildcard_score
            score_dict.update({post.id: total_relevance})
        else:
            total_relevance = decimal.Decimal(tag_score)
            # Multiply the total relevance by a funtion that is large for a
            # small number of days and small for a large number of days
            if post.proof_description and post.proof_pic:
                num_days_since_proved = ((timezone.now() - post.proved_at).total_seconds() / (3600 * 24))
                total_relevance *= decimal.Decimal(math.exp((-1/4) * num_days_since_proved))
            else:
                total_relevance *= decimal.Decimal(math.exp((-1/4) * num_days))
            # Output scores to a dictionary
            score_dict.update({post.id: total_relevance})
        # This is extremely useful for development purposes.
        print(('''Id: {},
                  title: {},
                  score: {}.
                  {} tags matched.
                  User follows: {} and {} follower tags matched.
                  Posted {} days(s) ago.''').format(
                                                post.id,
                                                post.title,
                                                total_relevance,
                                                num_tags_match,
                                                does_follow,
                                                follower_tag_count,
                                                num_days,
                                            )
                )

    # Order score_dict by value and give an ordered list of post ids
    output = {}
    sorted_score_dict = sorted(score_dict, key=score_dict.__getitem__)
    for k in sorted_score_dict:
        output.update({k: score_dict})
    post_ids = list(output.keys())
    post_ids = post_ids[::-1]
    # Also useful for development
    # print(post_ids, runtimes)

    # Return a list of post ids sorted in descending order of relevance
    return post_ids
