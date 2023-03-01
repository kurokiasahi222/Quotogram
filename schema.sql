CREATE TABLE users (
    user_id VARCHAR(250) PRIMARY KEY,
    username VARCHAR(250) NOT NULL,
    first_name VARCHAR(250) NOT NULL,
    last_name VARCHAR(250) NOT NULL,
    profile_image TEXT NOT NULL,
    email VARCHAR(250) NOT NULL
);

CREATE TABLE followers (
    follower_id VARCHAR(250) NOT NULL,
    followed_id VARCHAR(250) NOT NULL,
    FOREIGN KEY(follower_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(followed_id) REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY(follower_id,followed_id)
);

CREATE TABLE post (
    post_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(250) NOT NULL,
    quote VARCHAR(500) NOT NULL,
    quote_author VARCHAR(250) NOT NULL DEFAULT 'Anonymous',
    context VARCHAR(1000),
    creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE post_following (
    user_id VARCHAR(250) NOT NULL,
    post_id BIGINT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY(user_id,post_id)
);

CREATE TABLE post_category (
    post_id BIGINT,
    category VARCHAR(250),
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY(post_id,category)
);

CREATE TABLE post_like (
    post_id BIGINT NOT NULL,
    user_id VARCHAR(250) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY(user_id,post_id)
);
WITH nonzero_like_posts AS (
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
),
posts_added AS (
    SELECT * FROM post p WHERE p.user_id = 'USER1234'
    UNION
    SELECT * FROM post p
    WHERE p.post_id IN (
        SELECT pf.post_id 
        FROM post_following pf 
        WHERE pf.user_id = 'USER1234'
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