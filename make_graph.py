# coding:utf-8
import os
from googleapiclient.discovery import build
import pandas as pd
import re
import collections

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

f = open('./data/graph_test.txt', 'a')


def YoutubeTopVideo(id_, API_KEY):
    # 再生回数順に動画情報を取得
    # 引数はチャンネルID
    responses = []
    counts = 0
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    youtube = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
    search_response = youtube.search().list(
        part='snippet',
        channelId=id_,
        order='viewCount',
        maxResults=20,
    ).execute()
    responses.extend(search_response['items'])
    counts += len(search_response['items'])
    print('load '+str(counts)+' videos...')

    return responses


def YoutubeGetDescription(video_id_, API_KEY):
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id_,
    ).execute()
    return video_response


def RegexForDescript(descript_list_):
    # 概要欄のlistを受け取って、チャンネルIDを返す関数
    # チャンネルidのlist seedの動画sの概要欄に貼ってあるチャンネルのチャンネルID
    channel_id_list = list()
    # URLの正規表現のパターン
    pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
    word_pat = "[\w|\d|-]+"  # ?sub_confirmation=1などの余分な要素を削除するためのパターン
    for descript in descript_list_:
        # 各動画の概要欄に貼ってある全てのURLを取得
        channel_url_list = re.findall(pattern, descript)
        for url in channel_url_list:
            # 正規表現で取り出したURLからチャンネルIDを取得
            channel_ids = re.search(
                r'(https://www\.youtube\.com/channel/)(.*)', url)
            if channel_ids != None:
                # 正規表現の漏れ,チャンネルID以外の要素を削除
                regexed_channel_id = re.search(word_pat, channel_ids.group(2))
                # チャンネルIDのみになった
                channel_id_list.append(regexed_channel_id.group(0))
    return channel_id_list


def NoDuplicateChannelId(channel_id_list_):
    # チャンネルidのlistを受け取って、重複なし、かつ[('UCHVXbQzkl3rDfsXWo8xi2qw', 3), ...]のチャンネルIDと重複数で返す
    no_duplicate_channel_id_list = collections.Counter(channel_id_list_)
    c_list = list(no_duplicate_channel_id_list.items())
    return c_list


# 皇女殿下のチャンネルID,seedとなるチャンネルのチャンネルID
#rize_id = "UCZ1xuCK1kNmn5RzPYIZop3w"
# rize_id = "UC1opHUrw8rvnsadT-iGp7Cg" # akua
# rize_id = "UCSFCh5NL4qXrAy9u-u2lX3g"    # kuzuha
# rize_id = "UCZlDXzGoo7d44bwdNObFacg"  # 天音かなた
# rize_id = "UCZYyhgoV314CM14zBD6vd4A"  # 天開司
# rize_id = "UCkngxfPbmGyGl_RIq4FA3MQ"  # 西園チグサ
# rize_id = "UCj_KuUzpOXAliYEesJwdrbw"  # 伊東ライフ
rize_id = "UC0Owc36U9lOyi9Gx9Ic-4qg"  # 因幡はねる

# 再生数上位の動画(概要欄全文を含むjsonデータ)を取得
topvideos = YoutubeTopVideo(rize_id, YOUTUBE_API_KEY)

# ビデオのidのlist(これを用いて概要欄全文を取得する(YoutubeGetDescription を使用して))
video_id_list = list()
# 概要欄のlist
descript_list = list()
# チャンネル名のlist
channel_name_set = list()
# 既に調査したユーザーのset
searched_user = set()  # チャンネル名かチャンネルIDどっちにしようか,チャンネル名を獲得するのにAPIを叩くからチャンネルIDの方が良い？
# 既に調査したユーザーのset
searched_user.add(rize_id)


# videoIdとチャンネル名の取得
for video in topvideos:
    videoId = video['id'].get('videoId')
    channel_name = video['snippet'].get('channelTitle')
    # なぜかvideoIdがないものは除外
    if videoId != None:
        video_id_list.append(videoId)
    # channel_name_set.append(channel_name)

#print("video_id_list : ", video_id_list)
#print("channel_name_set : ", channel_name_set)

# 概要欄全文の取得
for video_id in video_id_list:
    description = YoutubeGetDescription(video_id, YOUTUBE_API_KEY)
    descript_list.append(description['items'][0]['snippet']['description'])

channel_id_list = RegexForDescript(descript_list_=descript_list)
c_list = NoDuplicateChannelId(channel_id_list_=channel_id_list)
print("c_list", c_list)
for channel in c_list:
    #print(rize_id, channel[0], channel[1])
    f.write(rize_id + " " + channel[0] + " " + str(channel[1]) + "\n")
############################
# ここまでseedユーザの調査
############################
f.write("those are writed by seed user\n")


for channel_id_set in c_list:
    channel_id = channel_id_set[0]
    searched_user.add(channel_id)
    each_topvideos = YoutubeTopVideo(channel_id, YOUTUBE_API_KEY)
    # 動画IDのlist
    each_video_id_list = list()
    # 概要欄のlist
    each_descript_list = list()
    # videoIdとチャンネル名の取得
    for video in each_topvideos:
        videoId = video['id'].get('videoId')
        channel_name = video['snippet'].get('channelTitle')
        # なぜかvideoIdがないものは除外
        if videoId != None:
            each_video_id_list.append(videoId)
    # 概要欄全文の取得
    for video_id in each_video_id_list:
        each_description = YoutubeGetDescription(video_id, YOUTUBE_API_KEY)
        each_descript_list.append(
            each_description['items'][0]['snippet']['description'])

    each_channel_id_list = RegexForDescript(descript_list_=each_descript_list)
    each_c_list = NoDuplicateChannelId(channel_id_list_=each_channel_id_list)
    print("each_c_list", each_c_list)
    for e_channel in each_c_list:
        #print(channel_id, channel[0], channel[1])
        f.write(channel_id + " " +
                e_channel[0] + " " + str(e_channel[1]) + "\n")
f.close()
print("searched_user\n", searched_user)
