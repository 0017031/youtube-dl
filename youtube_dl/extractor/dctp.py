# encoding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class DctpTvIE(InfoExtractor):
    _VALID_URL = r'^http://www.dctp.tv/(#/)?filme/(?P<id>.+?)/$'
    _TEST = {
        'url': 'http://www.dctp.tv/filme/videoinstallation-fuer-eine-kaufhausfassade/',
        'info_dict': {
            'id': 'videoinstallation-fuer-eine-kaufhausfassade',
            'ext': 'flv',
            'title': 'Videoinstallation für eine Kaufhausfassade'}
        }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        base_url = 'http://dctp-ivms2-restapi.s3.amazonaws.com/'
        version_json = self._download_json(base_url + 'version.json', video_id)
        version = version_json['version_name']
        info_json = self._download_json(
            '{}{}/restapi/slugs/{}.json'.format(base_url, version, video_id), video_id)
        object_id = info_json['object_id']
        meta_json = self._download_json(
            '{}{}/restapi/media/{}.json'.format(base_url, version, object_id), video_id)
        uuid = meta_json['uuid']
        title = meta_json['title']
        wide = meta_json['is_wide']
        if wide:
            ratio = '16x9'
        else:
            ratio = '4x3'
        play_path = 'mp4:{}_dctp_0500_{}.m4v'.format(uuid, ratio)

        servers_json = self._download_json('http://www.dctp.tv/streaming_servers/', video_id)
        url = servers_json[0]['endpoint']

        return {
            'id': video_id,
            'title': title,
            'format': 'rtmp',
            'url': url,
            'play_path': play_path,
            'real_time': True,
            'ext': 'flv'
        }

