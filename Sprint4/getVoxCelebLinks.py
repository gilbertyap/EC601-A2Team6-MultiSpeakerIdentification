import os

linkPrefix = 'https://www.youtube.com/watch?v='

idGroupList = os.listdir('./txt/')
for item in idGroupList:
    if not os.path.isdir(item):
        idGroupList.remove(item)
idGroupList.sort()
videoList = []

for idGroup in idGroupList:
    itemList = os.listdir('./txt/'+idGroup)
    itemList.sort()
    for item in itemList:
        videoList.append(linkPrefix+item+'\n')

with open('voxCeleb1_links.txt','w') as f:
    f.writelines(videoList)