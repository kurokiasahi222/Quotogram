# Get all the user's post
USER_POSTS = """SELECT * FROM post p WHERE p.user_id = '{user_id}' """

# Get the posts which the user follows
POSTS_FOLLOWING = """SELECT *
FROM post p
WHERE p.post_id IN (
    SELECT pf.post_id 
    FROM post_following pf 
    WHERE pf.user_id = '{user_id}'
    )"""

# Get the posts of the user's followers
FOLLOWER_POSTS  = """SELECT *
FROM post p
WHERE p.user_id IN (
    SELECT f.followed_id
    FROM followers f 
    WHERE f.follower_id = '{user_id}'
    )"""
## print(FOLLOWER_POSTS.format(user_id="hello"))

# Getting all the posts from the above categories (user's, their following posts, and their follower's posts)
ALL_POSTS = USER_POSTS + """\nUNION\n"""+ POSTS_FOLLOWING  + """\nUNION\n"""+ FOLLOWER_POSTS 

# Get a post by a category:
POSTS_BY_CATEGORY = """SELECT *
FROM post p
WHERE p.post_id IN (
    SELECT pc.post_id
    FROM post_category pc
    where pc.category = '{post_category}')"""
## print(POSTS_BY_CATEGORY.format(post_category="inspirational"))

# Get the most popular posts (largest likes) and their likes
POSTS_BY_POPULARITY = """WITH likes_per_post AS (
    SELECT post_id, COUNT(*) AS likes
    FROM post_like
    GROUP BY  post_id
)
SELECT *
FROM post p, likes_per_post l
WHERE p.post_id = l.post_id
ORDER BY l.likes DESC
LIMIT {limit} OFFSET {offset}"""
## print(POSTS_BY_POPULARITY.format(limit=10,offset=0)) # Get top 10 quotes 

ADD_USER = """INSERT INTO users (user_id,username,first_name,last_name,profile_image,email)
VALUES ('{user_id}','{username}','{first_name}','{last_name}','{profile_image}','{email}')"""

ADD_BOARD = """INSERT INTO board (user_id,title) VALUES ('{user_id}','{title}')"""