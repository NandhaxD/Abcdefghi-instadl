from instagrapi import Client
import requests
import os
import re
from urllib.parse import urlparse

class InstaAPI:
    def __init__(self, username, password):
        self.client = Client()
        self.client.login(username, password)
        self.regex = r'https?://(www\.)?instagram\.com/([a-zA-Z0-9_.]+(/)?|p/[a-zA-Z0-9_-]+(/)?|reel/[a-zA-Z0-9_-]+(/)?|tv/[a-zA-Z0-9_-]+(/)?|stories/[a-zA-Z0-9_.]+/[0-9]+(/)?|[a-zA-Z0-9_.]+/channel/(\?igshid=[a-zA-Z0-9_-]+)?)'

    def exists(self, link):
        if re.search(self.regex, link):
            return True
        else:
            return False

    def is_valid_instagram_story_url(self, url):
        pattern = r"^https://www\.instagram\.com/stories"
        return bool(re.match(pattern, url))

    def filter_instagram_story_url(self, url):
        url_parts = url.split('?')
        base_url = url_parts[0]
        return base_url

    def info(self, url):
        if not self.exists(url):
            return "Link does not exist"
        
        if self.is_valid_instagram_story_url(url):
            video_url, photo_url, name, typee = self.insta_story(url)
        else:
            video_url, photo_url, name, typee = self.insta_post(url)
        
        return video_url, photo_url, name, typee

    def insta_post(self, url):
        media_id = self.client.media_pk_from_url(url)
        info = self.client.media_info(media_id)
        video_url = None
        photo_url = None
        if info.media_type == 1:
            photo_url = info.image_versions2["candidates"][0]["url"]
        elif info.media_type == 2:
            video_url = info.video_url
        elif info.media_type == 8:
            photo_url = info.image_versions2["candidates"][0]["url"]
        name = "{}".format(info.user.username)
        return video_url, photo_url, name, info.media_type

    def insta_story(self, url):
        media_id = self.client.story_pk_from_url(url)
        info = self.client.story_info(media_id)
        video_url = None
        photo_url = None
        if info.media_type == 1:
            photo_url = info.image_versions2["candidates"][0]["url"]
        elif info.media_type == 2:
            video_url = info.video_url
        elif info.media_type == 8:
            photo_url = info.image_versions2["candidates"][0]["url"]
        name = "{}".format(info.user.username)
        return video_url, photo_url, name, info.media_type

    def extract_info_and_download(self, url, save_dir=None):
        url = str(url)
        parse_result = urlparse(url)
        filename = os.path.basename(parse_result.path)
        file_extension = os.path.splitext(filename)[1]
        if save_dir:
            save_path = os.path.join(save_dir, filename)
        else:
            save_path = filename
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        f.write(chunk)
                return save_path
            else:
                return f"Failed to download file from {url}. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {e}"

    def instadl(self, url):
        if not self.exists(url):
            return "Link does not exist"
        
        if self.is_valid_instagram_story_url(url):
            video_url, photo_url, name, typee = self.insta_story(url)
        else:
            video_url, photo_url, name, typee = self.insta_post(url)
        
        res = self.extract_info_and_download(video_url or photo_url, save_dir=f'{os.getcwd()}/downloads')
        return name, res
