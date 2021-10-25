# coding: utf-8
import musicbrainzngs 
import pandas as pd

# HACK: This allows to use https without verify the certificate WARNING
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


df = pd.read_csv('albums5000.zip')
df['Release Date'] =  pd.to_numeric(df['Release Date'].str[-4:])

def get_my_year_album(n:int):
	return df[df['Release Date'] == n][['Album','Artist Name','Release Date']].head(1).to_dict('records')[0]


musicbrainzngs.set_useragent('Kinda figure it out' , 'v0.0.2', 'Music Analista')
#pd_query = {'Album': 'OK Computer', 'Artist Name': 'Radiohead', 'Release Date': 1997}
pd_query = {'Album': 'Vespertine', 'Artist Name': 'Björk', 'Release Date': 2001}


def get_musicbrainz_info(pd_query:dict):
    releases = musicbrainzngs.search_releases(pd_query['Album'], date=pd_query['Release Date'], artist=pd_query['Artist Name'])
    eureka = {}
    for release in releases['release-list']:
        print('voy a ir a buscar...')
        release_query = musicbrainzngs.get_release_by_id(release['id'], includes=['recordings'])
        print('ya regrese')

        if 'cover-art-archive' in release_query['release']:
            artwork = release_query['release']['cover-art-archive']['artwork']
            if artwork == 'true':
                image_list = musicbrainzngs.get_image_list(release['id'])
                for i in image_list['images']:
                    if (i['approved'] == True) and (i['front'] == True):
                        print('Intenta esta: ', i['image'])
                        pd_query['release_id'] = release['id']
                        pd_query['cover_art_url'] = i['image']
                        eureka = release_query
                        break
                if eureka != {}:
                    break

            else:
                print('La que sigue..')
                continue

    track_list=[]
    for song in eureka['release']['medium-list'][0]['track-list']:
        print(song['position'],song['recording']['title'])
        track_list.append({'position': song['position'], 'title':song['recording']['title']})
    pd_query['track_list'] = track_list

    return pd_query