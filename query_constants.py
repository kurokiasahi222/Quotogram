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

# Also maybe you could also work on modifying the query constant ALL_POSTS to have only user posts and their 
# follower posts (you would have to modify the queries to add the num_likes to the data). 
# This way we can call get_posts (db.py) to display the posts of the user on the profile page (which is when the user is logged in).

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
SELECT p.post_id,p.user_id,p.quote,p.context, p.creation_time, l.num_likes, false as quote_added
FROM post p, likes_for_all_posts_id l
WHERE p.post_id = l.post_id"""

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
)

SELECT p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, l.num_likes, false as quote_added
FROM posts_not_added p , likes_for_all_posts_id l
WHERE p.post_id = l.post_id
UNION
SELECT p.post_id,p.user_id,p.quote,p.quote_author,p.context, p.creation_time, l.num_likes, true as quote_added
FROM posts_added p, likes_for_all_posts_id l
WHERE p.post_id = l.post_id"""

POST_LIKES = """SELECT COUNT(*) AS num_likes
                FROM post_like
                WHERE post_id = %s"""
