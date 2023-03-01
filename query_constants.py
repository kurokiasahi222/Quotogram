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
)
SELECT row_to_json(t) FROM results t """