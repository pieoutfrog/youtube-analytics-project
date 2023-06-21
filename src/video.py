import os
from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        try:
            self.__video_id = video_id
            video_info = Video.get_service().videos().list(id=self.__video_id, part='snippet, statistics').execute()
            self.title = video_info['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/channel/{self.__video_id}'
            self.view_count = video_info['items'][0]['statistics']['viewCount']
            self.like_count = video_info['items'][0]['statistics']['likeCount']
        except (KeyError, IndexError, TypeError):
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__video_id = video_id
        self.playlist_id = playlist_id
        plv_video_info = Video.get_service().videos().list(id=self.__video_id, part='snippet, statistics').execute()
        self.title = plv_video_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/channel/{self.__video_id}'
        self.view_count = plv_video_info['items'][0]['statistics']['viewCount']
        self.like_count = plv_video_info['items'][0]['statistics']['likeCount']
