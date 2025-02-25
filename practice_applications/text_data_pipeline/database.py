from dataclasses import dataclass
from datetime import datetime as dt
from os import getenv
from dotenv import load_dotenv
from sqlalchemy.orm import mapped_column, DeclarativeBase, Session, Mapped
from sqlalchemy.sql.expression import select
from sqlalchemy import create_engine

load_dotenv()


class Base(DeclarativeBase):
    pass


@dataclass
class VideoData:
    video_id: str
    title: str
    published_at: dt
    playlist_id: str
    likes: int
    views: int
    comments: int

    def to_dict(self):
        return {
            "video_id": self.video_id,
            "title": self.title,
            "published_at": self.published_at,
            "playlist_id": self.playlist_id,
            "likes": self.likes,
            "views": self.views,
            "comments": self.comments,
        }

    @staticmethod
    def from_dict(params: dict):
        # TODO: add validations on fields
        return VideoData(
            video_id=params.get("video_id"),
            title=params.get("title"),
            published_at=dt.fromisoformat(params.get("published_at")),
            playlist_id=params.get("playlist_id"),
            likes=params.get("likes"),
            views=params.get("views"),
            comments=params.get("comments"),
        )


class VideosOfInterest(Base):
    __tablename__ = "videos_of_interest"
    video_id: Mapped[str] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    published_at: Mapped[dt] = mapped_column(nullable=False)
    playlist_id: Mapped[str]
    likes: Mapped[int]
    views: Mapped[int]
    comments: Mapped[int]


class PostgresConnector:
    def __init__(
        self,
        username: str,
        password: str,
        database_name: str,
        host: str = "localhost",
        debug: bool = False
    ):
        db_url = f"postgresql://{username}:{password}@{host}/{database_name}"
        if debug:
            self.db_url = db_url
        self.engine = create_engine(db_url)
        self.local_session = Session(bind=self.engine, autocommit=False, autoflush=False)


def write_to_database(data: dict):
    video_data: VideoData = VideoData.from_dict(data)
    pg_conn = PostgresConnector(
        username=getenv("DATABASE_USER"),
        password=getenv("DATABASE_PASS"),
        database_name=getenv("DATABASE_NAME"),
    )
    statement = select(VideosOfInterest).where(
        VideosOfInterest.video_id == video_data.video_id
    )
    existing_record = pg_conn.local_session.scalars(statement).first()
    if existing_record:
        print(f"Record already exists with this ID: {video_data.video_id}")
    else:
        record = VideosOfInterest(
            video_id=video_data.video_id,
            title=video_data.title,
            published_at=video_data.published_at,
            playlist_id=video_data.playlist_id,
            likes=video_data.likes,
            views=video_data.views,
            comments=video_data.comments,
        )
        pg_conn.local_session.add(record)
        pg_conn.local_session.commit()
