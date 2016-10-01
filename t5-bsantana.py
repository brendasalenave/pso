#!/usr/bin/envpython3

import os, requests, bs4, re

url = 'http://phdcomics.com'
#url = 'http://xkcd.com'
os.makedirs('phd', exist_ok=True)
print('Downloading page %s...'% url)
res=requests.get(url)
res.raise_for_status()

soup=bs4.BeautifulSoup(res.text,"lxml")

for fig in soup.find_all('img', src=re.compile('http://www.phdcomics.com/comics/archive/' + 'phd.*gif$')):
    comicUrl=fig.get('src')
    #print('Downloading image %s...' % (comicUrl))
    res=requests.get(comicUrl)
    res.raise_for_status()
    imgFile=open(os.path.join('phd',
    os.path.basename(comicUrl)),'wb')
    for chunk in res.iter_content(100000):
        imgFile.write(chunk)
    imgFile.close()

id_ = re.findall(r'\d+', comicUrl)
id_fig = int(id_[0])

count = 0
for u in range(50):
    id_fig = id_fig - 1
    comicUrl = 'http://www.phdcomics.com/comics/archive/phd0' + str(id_fig) + 's.gif'
    res=requests.get(comicUrl)
    if (count >= 7): break
    if(res.status_code != 404) and (count < 4):
        res.raise_for_status()
        imgFile=open(os.path.join('phd',
        os.path.basename(comicUrl)),'wb')
        for chunk in res.iter_content(100000):
            imgFile.write(chunk)
        imgFile.close()
        count += 1

imgs = os.listdir('phd')
print(len(imgs))
if (len(imgs) > 5):
    t = len(imgs)
    for i in os.walk('phd'):
        for u in range(5, t):
            os.remove(imgs[u])
        break
        
print('Done!')
