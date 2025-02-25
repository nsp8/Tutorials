CREATE TABLE videos_of_interest (
    video_id VARCHAR(20) PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    published_at TIMESTAMP,
    playlist_id VARCHAR(50),
    likes INT,
    views INT,
    comments INT
)
