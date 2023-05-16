# load modules
import asyncio
import json
import os

import BSAPI.beatsaver as beatsaver
import pandas as pd

from version import VERSION

os.environ['USER_AGENT'] = f'{VERSION} (+contact twitter/@aruru_bs discord/あるる#1137)'


async def main():

    rate_criteria = [
        [0, 0.1],
        [0.1, 0.15]
    ]

    for minRating, maxRating in rate_criteria:

        # init
        page = 0
        IDs = []
        songs = []

        while (True):

            # increment
            page += 1
            print(
                f'minRating={int(minRating*100)}%, maxRating={int(maxRating*100)}%, page={page:03}')

            # get ranked maplist
            searchResponse = await beatsaver.search_maps(minRating=minRating, maxRating=maxRating, page=page)

            # set songs
            if searchResponse is not None:
                if (searchResponse.docs is not None) and len(searchResponse.docs) > 0:
                    # get
                    IDs += [x.id for x in searchResponse.docs]
                    songs += [{
                        "songName": x.metadata.songName,
                        "levelAuthorName": x.metadata.levelAuthorName,
                        "hash": x.versions[0].hash,
                        "levelid": f"custom_level_{x.versions[0].hash}"
                    } for x in searchResponse.docs]
                else:
                    break
            else:
                break

            await asyncio.sleep(1/200)

        # del duplicated element
        slct_index = [not b for b in list(pd.Index(IDs).duplicated())]
        songs = [e for e, i in zip(songs, slct_index) if i]

        # read image
        with open('imgs/u20.txt', 'r') as f:
            img = f.read()

        # gen playlist
        fname = f'rating-{int(minRating*100)}percent-to-{int(maxRating*100)}percent-playlist.bplist'
        playlist = {
            "customData": {
                "syncURL": f"https://github.com/jundoll/bs-bad-rating-playlist/releases/latest/download/{fname}"
            },
            "playlistTitle": f'rating-{int(minRating*100)}percent-to-{int(maxRating*100)}percent',
            "playlistAuthor": "",
            "songs": songs,
            #"image": img
        }

        # save
        with open(f'out/{fname}', 'w') as f:
            json.dump(playlist, f)

if __name__ == '__main__':
    asyncio.run(main())
