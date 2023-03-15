# Get all the user's post
USER_POSTS = """SELECT * FROM post p WHERE p.user_id = %s """

# Get the posts which the user follows
POSTS_FOLLOWING = """SELECT *
FROM post p
WHERE p.post_id IN (
    SELECT pf.post_id 
    FROM post_following pf 
    WHERE pf.user_id = %s
    )"""

# Get the posts of the user's followers
FOLLOWER_POSTS  = """SELECT *
FROM post p
WHERE p.user_id IN (
    SELECT f.followed_id
    FROM followers f 
    WHERE f.follower_id = %s
    )"""

# Getting all the posts from the above categories (user's, their following posts, and their follower's posts)
ALL_POSTS = USER_POSTS + """\nUNION\n"""+ POSTS_FOLLOWING  + """\nUNION\n"""+ FOLLOWER_POSTS 

# Get all the post user is following
# including their own posts (you follow your own posts by default)
USER_ALL_FOLLOWING_POSTS = """ 
WITH all_posts_following AS (
    SELECT post.post_id, post.user_id, 
    post.quote, post.quote_author, post.context, post.creation_time, true as quote_added
    FROM post_following
    JOIN post using(post_id)
    WHERE post_following.user_id = %s
    ), 
likes_per_post AS ( 
    SELECT a.post_id, COUNT(post_like.user_id) AS num_likes
    FROM all_posts_following a
    LEFT JOIN post_like ON a.post_id = post_like.post_id
    GROUP BY a.post_id), 
all_posts_following_with_likes AS (
    SELECT *
    FROM all_posts_following
    JOIN likes_per_post USING(post_id)
), 
all_posts_following_with_userinfo AS (
    SELECT *
    FROM all_posts_following_with_likes
    JOIN users USING(user_id)
)
SELECT row_to_json(a)
FROM all_posts_following_with_userinfo a; 
"""

# Get followers of a user
GET_FOLLOWERS = """
WITH user_followers AS (
SELECT *
FROM users 
JOIN followers ON users.user_id = followers.follower_id)
SELECT *
FROM user_followers
WHERE followed_id = %s
"""

# Get following of a user
GET_FOLLOWING = """
WITH user_followers AS (
SELECT *
FROM users 
JOIN followers ON users.user_id = followers.followed_id)
SELECT *
FROM user_followers
WHERE follower_id = %s
"""

GET_USER_INFO = """
SELECT row_to_json(t)
FROM (
    SELECT u.user_id, u.username, u.first_name, u.last_name, u.profile_image, u.email
    FROM users u
    WHERE u.user_id = %s
)
AS t
"""


# Get users posts from username
USER_POSTS_FROM_USERID = """
SELECT row_to_json(p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, p.num_likes, p.quote_added, u.profile_image, u.username)
FROM post p, users u WHERE p.user_id = u.user_id AND u.username = %s 
"""

# Get the number of peole user is following
NUMBER_FOLLOWING = "SELECT COUNT(*) FROM followers WHERE follower_id = %s"

ADD_USER = """INSERT INTO users (user_id,username,first_name,last_name,profile_image,email)
VALUES (%s,%s,%s,%s,%s,%s)"""

POST_LIKES_HEADER = """WITH nonzero_like_posts AS (
    SELECT post_id, COUNT(*) AS num_likes
    FROM post_like
    GROUP BY  post_id
),
zero_like_posts AS (
    SELECT post_id FROM post 
    EXCEPT 
    SELECT post_id FROM nonzero_like_posts
),
likes_for_all_posts_id AS (
    SELECT * FROM nonzero_like_posts
    UNION
    SELECT post_id, 0 as num_likes FROM zero_like_posts
)"""

POSTS_NOT_LOGGED_IN = POST_LIKES_HEADER + """
SELECT p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, l.num_likes, false as quote_added, u.profile_image, u.username
FROM post p, likes_for_all_posts_id l, users u
WHERE p.post_id = l.post_id AND p.user_id = u.user_id
ORDER BY p.creation_time DESC, l.num_likes DESC, p.post_id DESC
LIMIT %s OFFSET %s"""

POSTS_LOGGED_IN = POST_LIKES_HEADER + """,
posts_added AS (
    SELECT * FROM post p WHERE p.user_id = %s
    UNION
    SELECT * FROM post p
    WHERE p.post_id IN (
        SELECT pf.post_id 
        FROM post_following pf 
        WHERE pf.user_id = %s
    )
),
posts_not_added AS (
    SELECT * FROM post p 
    EXCEPT
    SELECT * FROM posts_added 
),
all_posts AS (
    SELECT p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, l.num_likes, false as quote_added
    FROM posts_not_added p , likes_for_all_posts_id l
    WHERE p.post_id = l.post_id
    UNION
    SELECT p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, l.num_likes, true as quote_added
    FROM posts_added p, likes_for_all_posts_id l
    WHERE p.post_id = l.post_id
)
SELECT  p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, p.num_likes, p.quote_added, u.profile_image, u.username
FROM all_posts p , users u
WHERE p.user_id = u.user_id
ORDER BY p.creation_time DESC, p.num_likes DESC, p.post_id DESC
LIMIT %s OFFSET %s"""

POST_LIKES = """SELECT COUNT(*) AS num_likes
                FROM post_like
                WHERE post_id = %s"""

QUOTE_FOLLOW_UNFOLLOW = """
DO
$$
DECLARE var_user_id VARCHAR := %s;
DECLARE var_quote_id BIGINT := %s;
BEGIN
    IF (
        SELECT COUNT(*) as count FROM post_following WHERE user_id = var_user_id AND post_id = var_quote_id
    ) = 0 THEN INSERT INTO post_following VALUES (var_user_id,var_quote_id);
    ELSE
        DELETE FROM post_following WHERE user_id = var_user_id and post_ID = var_quote_id;
    END IF;
END;
$$;
"""

FULL_TEXT_SEARCH = """
WITH text_search_categories AS (
    SELECT * FROM post
    WHERE post_id IN (
        SELECT post_id FROM post_category WHERE to_tsvector(category) @@ to_tsquery(%(search_query)s)
    )
),
text_search_posts AS (
    SELECT * FROM post WHERE to_tsvector(quote || ' ' || quote_author || ' ' || context) @@ to_tsquery(%(search_query)s)
),
results AS (
    SELECT t.post_id, t.user_id, t.quote, t.quote_author, t.context, t.creation_time,
        CASE 
            WHEN (SELECT COUNT(*) FROM post_following f WHERE f.post_id = t.post_id AND f.user_id = %(user_id)s) > 0 THEN true 
            ELSE false
        END AS is_following,
        CASE WHEN (SELECT COUNT(*) FROM post_like l WHERE l.post_id = t.post_id ) > 0
                THEN (SELECT COUNT(*)  FROM post_like l WHERE l.post_id = t.post_id) 
            ELSE 0
        END AS num_likes
    FROM  text_search_posts t

    UNION

    SELECT t.post_id, t.user_id, t.quote, t.quote_author, t.context, t.creation_time,
        CASE 
            WHEN (SELECT COUNT(*) FROM post_following f WHERE f.post_id = t.post_id AND f.user_id = %(user_id)s) > 0 THEN true 
            ELSE false
        END AS is_following,
        CASE WHEN (SELECT COUNT(*) FROM post_like l WHERE l.post_id = t.post_id ) > 0
                THEN (SELECT COUNT(*)  FROM post_like l WHERE l.post_id = t.post_id) 
            ELSE 0
        END AS num_likes
    FROM  text_search_categories t
),
posts_with_user_data AS (
    SELECT r.post_id, r.user_id, r.quote, r.quote_author, r.context, r.creation_time, r.is_following, r.num_likes, u.profile_image, u.username
    FROM results r, users u
    WHERE r.user_id = u.user_id
)
SELECT row_to_json(t) FROM posts_with_user_data t """

FOLLOW_UNFOLLOW_USER = """
DO
$$
DECLARE var_user_follower VARCHAR := %s;
DECLARE var_user_followed VARCHAR := %s;
BEGIN
    IF (
        SELECT COUNT(*) as count FROM followers WHERE follower_id = var_user_follower AND followed_id = var_user_followed
    ) = 0 THEN INSERT INTO followers VALUES (var_user_follower,var_user_followed);
    ELSE
        DELETE FROM followers WHERE follower_id = var_user_follower and followed_id = var_user_followed;
    END IF;
END;
$$;
"""

GET_POST_CATGEGORIES = """SELECT category FROM post_category WHERE post_id = %s"""

QOD_HEADER = """
WITH max_likes AS (
    SELECT MAX(likes) as max
    FROM (
        SELECT post_id, COUNT(*) AS likes
        FROM post_like
        GROUP BY post_id
    ) AS count_likes   
),
post_with_most_likes AS (
    SELECT post_id, COUNT(*) AS num_likes
    FROM post_like
    GROUP BY post_id
    HAVING COUNT(*) = (SELECT max FROM max_likes)
),
post_information AS (
    SELECT p.post_id, p.user_id, p.quote,p.quote_author,p.context, p.creation_time, pm.num_likes, u.profile_image, u.username
    FROM post p, post_with_most_likes pm, users u
    WHERE p.post_id = pm.post_id AND p.user_id = u.user_id
)"""

QOD_NOT_LOGGED_IN = QOD_HEADER + """SELECT row_to_json(t)
FROM (
    SELECT p.post_id, p.user_id, p.quote,p.quote_author,p.context, p.creation_time, p.num_likes, p.profile_image, p.username, false AS quote_added 
    FROM post_information p
) AS t"""

QOD_LOGGED_IN = QOD_HEADER + """
,
is_post_added AS (
    SELECT COUNT(*)
    FROM post_following f, post_information p 
    WHERE f.post_id = p.post_id AND f.user_id = %s
)
SELECT row_to_json(t)
FROM (
    SELECT p.post_id, p.user_id, p.quote,p.quote_author,p.context, p.creation_time, p.num_likes, p.profile_image, p.username, 
        CASE 
            WHEN i.count > 0 THEN true
            ELSE false
        END AS quote_added 
    FROM post_information p, is_post_added i
) AS t"""

IS_FOLLOWING = """
SELECT row_to_json(t) FROM (
    SELECT 
        CASE WHEN (SELECT COUNT(*) FROM followers f WHERE f.follower_id = %s AND f.followed_id = %s) > 0
                THEN true
            ELSE false
        END AS following
) AS t
"""
