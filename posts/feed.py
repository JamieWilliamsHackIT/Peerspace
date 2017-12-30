# Input: a user
# Output: a prediction of the most relevent posts

# Get the user's tags
# Get the post's tags
# Compare tags
# If tags match multiply score by tag's weight
# Multiply score by output of the date relevence function

def get_most_relevent(user_pk):
    from users.models import UserPreferenceTag
    from posts.models import Post

    import math
    import random
    import decimal

    #Get all user's tags
    user_tags = UserPreferenceTag.objects.filter(user=user_pk)
    # Get all posts (in last x amount of time)
    posts = Post.objects.order_by('created_at')#[:20]

    # Initialise the results dictionary
    score_dict = {}
    # Gives a list of all the user's tags
    user_tag_list = []
    for tag in user_tags:
        user_tag_list.append(tag.tag.lower())

    for post in posts:
        # Get all of the current post's tags
        post_tag_list = post.tags.split(",")
        # Lower case all tags with a list comprehension
        post_tag_list = [tag.lower() for tag in post_tag_list]

        # Initialise some varibles
        total_score = 0
        tag_score = 0
        num_tags_match = 0
        count = 0
        num_days = post.time_since_creation

        for user_tag in user_tag_list:
            if user_tag in post_tag_list:
                # Normalise the weight (make sure it is in range 0 to 1) by using
                # the logistic sigmoid
                tag_score += (1 / (1 + math.exp(-user_tags[count].weight)))
                num_tags_match += 1
            count += 1

        if num_tags_match == 0:
            # If no tags match then give the post a random score. This may
            # introduce the user to a new area of interest
            wildcard_score = random.random() * 0.5
            # This is the same date relevence and normalisation process as seen
            # below
            wildcard_score *= math.exp((-1/4) * num_days)
            total_relevence = 1 / (1 + math.exp(-wildcard_score))
            score_dict.update({post.id: total_relevence})
        else:
            total_relevence = decimal.Decimal(tag_score)
            # Multiply the total relevence by a funtion that is large for a
            # small number of days and small for a large number of days
            total_relevence *= decimal.Decimal(math.exp((-1/4) * num_days))
            # Output scores to a dictionary
            score_dict.update({post.id: total_relevence})
        # print(('Id: {}, title: {} and score: {}. {} tags matched.').format(post.id, post.title, total_relevence, num_tags_match))

    # Order score_dict by value and give an ordered list of post ids
    output = {}
    sorted_score_dict = sorted(score_dict, key=score_dict.__getitem__)
    for k in sorted_score_dict:
        output.update({k: score_dict})
    post_ids = list(output.keys())
    post_ids = post_ids[::-1]#[:10]
    print(post_ids)

    # When considering efficieny this function queries the database 2 + n times
    # where n is the number of posts in the last 10 days

    return post_ids
