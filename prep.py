import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
from collections import deque
src=r'C:\Users\hp2\Downloads\app4\assets'
out=r'C:\Users\hp2\Downloads\app4\ABCFunSchoolBus\assets\resources\textures'
os.makedirs(out,exist_ok=True)
def cut(im,thr=236):
    a=np.array(im.convert('RGB')).astype(int)
    h,w,_=a.shape
    white=(a.min(axis=2)>=thr)
    vis=np.zeros((h,w),bool)
    dq=deque()
    for x in range(w):
        for y in (0,h-1):
            if white[y,x] and not vis[y,x]: vis[y,x]=True; dq.append((y,x))
    for y in range(h):
        for x in (0,w-1):
            if white[y,x] and not vis[y,x]: vis[y,x]=True; dq.append((y,x))
    while dq:
        y,x=dq.popleft()
        for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
            ny,nx=y+dy,x+dx
            if 0<=ny<h and 0<=nx<w and white[ny,nx] and not vis[ny,nx]:
                vis[ny,nx]=True; dq.append((ny,nx))
    alpha=Image.fromarray(((~vis)*255).astype('uint8'))
    alpha=alpha.filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    rgba=im.convert('RGBA'); rgba.putalpha(alpha)
    bb=rgba.getbbox()
    return rgba.crop(bb) if bb else rgba
names=[]
for f in sorted(os.listdir(src)):
    n,e=os.path.splitext(f)
    if e.lower() not in('.jpg','.webp'): continue
    im=Image.open(os.path.join(src,f))
    r=cut(im)
    r.thumbnail((512,512))
    r.save(os.path.join(out,n.replace('asset_','')+'.png'))
    names.append((n,r.size))
print(names)
# contact sheet
files=sorted(os.listdir(out))
cols=6; cell=250
rows=(len(files)+cols-1)//cols
sheet=Image.new('RGB',(cols*cell,rows*cell),(120,170,220))
d=ImageDraw.Draw(sheet)
for i,f in enumerate(files):
    im=Image.open(os.path.join(out,f)); im.thumbnail((cell-10,cell-30))
    x=(i%cols)*cell+5; y=(i//cols)*cell+5
    sheet.paste(im,(x,y),im); d.text((x,y+cell-25),f,fill=(0,0,0))
sheet.save(r'C:\Users\hp2\Downloads\app4\sheet.png')
