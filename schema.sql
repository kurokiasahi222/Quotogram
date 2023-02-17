CREATE TABLE users (
    user_id VARCHAR(250) PRIMARY KEY,
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
    post_id BIGINT PRIMARY KEY,
    category VARCHAR(250),
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE
);

CREATE TABLE post_like (
    post_id BIGINT NOT NULL,
    user_id VARCHAR(250) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY(user_id,post_id)
);

CREATE TABLE board (
    board_id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(250) NOT NULL,
    title VARCHAR(250) NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE board_post (
    board_id BIGINT NOT NULL,
    post_id BIGINT NOT NULL,
    FOREIGN KEY(board_id) REFERENCES board(board_id) ON DELETE CASCADE,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    PRIMARY KEY(board_id,post_id)
);