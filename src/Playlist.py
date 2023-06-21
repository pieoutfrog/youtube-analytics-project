import os
import isodate
from googleapiclient.discovery import build
from datetime import timedelta


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        playlist_info = PlayList.get_service().playlists().list(id=self.__playlist_id,
                                                                part='snippet, contentDetails').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service

    def get_video_info(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                                  part='contentDetails', maxResults=50).execute()
        videos_id = []
        for video in playlist_videos['items']:
            videos_id.append(video['contentDetails']['videoId'])
            video_info = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(videos_id)
                                                          ).execute()
        return video_info

    @property
    def total_duration(self):
        total_duration = timedelta()
        total_duration = isodate.parse_duration("PT00M00S")
        video_info = PlayList.get_video_info(self)
        for i in video_info['items']:
            durations = i['contentDetails']['duration']
            duration = isodate.parse_duration(durations)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        r = PlayList.get_video_info(self)
        videos_url = []
        videos_like_count = []
        for video in r['items']:
            videos_like_count.append(video['statistics']['likeCount'])
            videos_url.append(f"https://youtu.be/{video['id']}")
        f = dict(zip(videos_like_count, videos_url))
        max_key = max(f, key=int)
        return f[max_key]