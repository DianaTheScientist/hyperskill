import pandas as pd
import os
import requests
import sys
import pandas as pd

if __name__ == '__main__':
    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if 'Nobel_laureates.json' not in os.listdir('../Data'):
        sys.stderr.write("[INFO] Dataset is loading.\n")
        url = "https://www.dropbox.com/s/m6ld4vaq2sz3ovd/nobel_laureates.json?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/Nobel_laureates.json', 'wb').write(r.content)
        sys.stderr.write("[INFO] Loaded.\n")

    # write your code here

    df = pd.read_json('../Data/Nobel_laureates.json')
    if df.duplicated().any():
        print(True)
    else:
        print(False)

    df = df.dropna(subset='gender')
    df = df.reset_index(drop=True)
    df = df.loc[:19, ['country', 'name']].to_dict()
    print(df)


