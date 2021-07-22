# load modules
from urllib.request import Request, urlopen
import pandas as pd
import json

# set url info
user_agent = "bs-bad-rating-playlist/1.0.0"
url = "https://cdn.wes.cloud/beatstar/bssb/v2-all.json"

# load json
req = Request(url, headers={'User-Agent': user_agent})
response = urlopen(req).read()
data = json.loads(response)
df = pd.DataFrame.from_dict(data, orient="index")
df['ID'] = data.keys()
df = df.drop(["mapper", "song"], axis=1)
df = df[df['uploaddate'].notnull()]

# output csv
df_csv = df.drop(["diffs"], axis=1)
df_csv.to_csv("dist/all.csv", index=False)

# output json
with open('img/u20.txt', 'r') as f:
    img = f.read()
u20 = {
    "playlistTitle": "under 20%",
    "playlistAuthor": "",
    "playlistDescription": "",
    "songs": list(df[(df['downVotes'] > 0) & (df['rating'] < 0.2) & (df['downloadCount'] > 1000) & (df['automapper'].isnull())]['ID']),
    "image": img
}
with open('dist/u20.json', 'w') as f:
    json.dump(u20, f)
