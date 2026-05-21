import json, os, glob

files = glob.glob('/tmp/bird/*.json')
account_files = [f for f in files if not os.path.basename(f).startswith('search-') and f != '/tmp/bird/news.json']
print(f'Found {len(account_files)} account files')

for fpath in sorted(account_files):
    try:
        with open(fpath) as f:
            data = json.load(f)
        if not isinstance(data, list):
            continue
        acct_name = os.path.basename(fpath).replace('.json','')
        recent = []
        for t in data:
            ca = t.get('createdAt', '')
            if 'May 21' in ca:
                parts = ca.split()
                try:
                    time_str = parts[3]
                    hour = int(time_str.split(':')[0])
                    if 1 <= hour <= 7:
                        recent.append(t)
                except:
                    pass
        if recent:
            for t in recent[:5]:
                print(f'@{acct_name} | {t.get("likeCount",0)}L {t.get("retweetCount",0)}RT | {t["createdAt"]}')
                print(f'  {t["text"][:250]}')
                quoted = t.get('quotedTweet')
                if quoted:
                    print(f'  QT: @{quoted.get("author",{}).get("username","?")}: {quoted.get("text","")[:150]}')
                print()
    except Exception as e:
        pass
