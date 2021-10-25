import musicbrainzngs 

musicbrainzngs.set_useragent(
    "python-musicbrainzngs-example",
    "0.1",
    "https://github.com/alastair/python-musicbrainzngs/",
)

def get_tracklist(artist, album):
    result = musicbrainzngs.search_releases(artist=artist, release=album, limit=1)
    id = result["release-list"][0]["id"]
    print(id)
    
    #### get tracklist
    new_result = musicbrainzngs.get_release_by_id(id, includes=["recordings"])
    t = (new_result["release"]["medium-list"][0]["track-list"])
    for x in range(len(t)):
        line = (t[x])
        print(f'{line["number"]}. {line["recording"]["title"]}')
