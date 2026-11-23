import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage as ndi

OUT=r'C:\Users\hp2\Downloads\app4\ABCFunSchoolBus\assets\resources\textures'
PREV=r'C:\Users\hp2\Downloads\app4\letters_preview'
os.makedirs(PREV,exist_ok=True)
FONT=r'C:\Windows\Fonts\ariblk.ttf'
S=1024
COL={'A':'#FF4D4D','B':'#FFC400','C':'#2FB8FF','D':'#3DDC55','E':'#FF8A1F','F':'#FF6FB5','G':'#9B59FF','H':'#9BE000',
'I':'#FFAA00','J':'#00D3C8','K':'#E0299F','L':'#E8343C','M':'#FFD500','N':'#2F6BFF','O':'#10C57A','P':'#B58CFF',
'Q':'#FF7A66','R':'#FF9A1A','S':'#18C5B5','T':'#8E3BFF','U':'#5FE0A0','V':'#4B4FD6','W':'#FFA94D','X':'#B8E01A',
'Y':'#FF4F8B','Z':'#1F7BFF'}
def hexrgb(h): h=h.lstrip('#'); return np.array([int(h[i:i+2],16) for i in (0,2,4)],float)/255

def mask_for(ch):
    best=None
    size=860
    while size>400:
        f=ImageFont.truetype(FONT,size)
        im=Image.new('L',(S,S),0); d=ImageDraw.Draw(im)
        bb=d.textbbox((0,0),ch,font=f)
        w,h=bb[2]-bb[0],bb[3]-bb[1]
        if w<=820 and h<=820:
            d.text(((S-w)/2-bb[0],(S-h)/2-bb[1]),ch,font=f,fill=255)
            return np.array(im).astype(float)/255
        size-=20
    raise Exception('size')

def render(ch):
    m=mask_for(ch)
    # round the shape (soft inflate)
    m=ndi.gaussian_filter(m,7); m=(m>0.5).astype(float)
    m=ndi.gaussian_filter(m,2.0)
    inside=m>0.5
    dist=ndi.distance_transform_edt(inside)
    R=52.0
    h=np.sqrt(np.clip(dist/R,0,1))            # puffy profile
    h=ndi.gaussian_filter(h,6)*R*1.0
    gy,gx=np.gradient(h)
    nz=np.ones_like(h); nx=-gx; ny=gy*1.0*-1+0   # y down image; flip so light from top
    nx=-gx*1.7; ny=-gy*1.7
    n=np.sqrt(nx**2+ny**2+nz**2); nx/=n; ny/=n; nz/=n
    L=np.array([-0.45,-0.65,0.62]); L/=np.linalg.norm(L)
    diff=np.clip(nx*L[0]+ny*L[1]+nz*L[2],0,1)
    Hh=L+np.array([0,0,1.0]); Hh/=np.linalg.norm(Hh)
    spec=np.clip(nx*Hh[0]+ny*Hh[1]+nz*Hh[2],0,1)**60
    base=hexrgb(COL[ch])
    # vertical gradient: lighter top
    yy=np.linspace(0,1,S)[:,None]
    light=np.clip(base*1.15+0.16,0,1); dark=np.clip(base*0.92,0,1)
    grad=light[None,None,:]*(1-yy[...,None])+dark[None,None,:]*yy[...,None]
    rim=np.clip(1-nz,0,1)**1.5   # edge darkening
    col=grad*(0.62+0.62*diff[...,None])
    col=col*(1-0.22*rim[...,None])+(base*0.55)[None,None,:]*0.0
    # soft bounce light from below-right
    bounce=np.clip(nx*0.5+ny*0.6,0,1)**2
    col+=bounce[...,None]*light[None,None,:]*0.18
    spec2=np.clip(nx*Hh[0]+ny*Hh[1]+nz*Hh[2],0,1)**14
    col+=spec[...,None]*1.0+spec2[...,None]*0.22
    # glossy top streak
    streak=ndi.gaussian_filter(((dist>R*0.55)&(dist<R*1.1)).astype(float),6)
    st=np.clip(streak*np.clip(-ny,0,1),0,1)*0.22
    col+=st[...,None]
    col=np.clip(col,0,1)
    # outline: darker outer ring + white sticker rim
    alpha=np.clip((m-0.5)*6+0.5,0,1)
    d_out=ndi.distance_transform_edt(~inside)
    ring1=(d_out>0)&(d_out<=6)           # dark rim
    ring2=(d_out>6)&(d_out<=16)          # white rim
    out=np.zeros((S,S,4))
    dk=base*0.62
    out[ring2,:3]=1.0; out[ring2,3]=1.0
    out[ring1,:3]=dk; out[ring1,3]=1.0
    out[inside,:3]=col[inside]; out[inside,3]=1.0
    # antialias edges by blurring alpha slightly
    a=ndi.gaussian_filter(out[...,3],1.1)
    out[...,3]=a
    # sparkles
    img=Image.fromarray((out*255).astype('uint8'),'RGBA')
    d=ImageDraw.Draw(img)
    ys,xs=np.where(inside)
    def star(cx,cy,r,fill=(255,224,70,255)):
        pts=[]
        for k in range(8):
            ang=math.pi/4*k-math.pi/2
            rr=r if k%2==0 else r*0.28
            pts.append((cx+rr*math.cos(ang),cy+rr*math.sin(ang)))
        d.polygon(pts,fill=fill,outline=(255,255,255,255))
    x0,x1,y0,y1=xs.min(),xs.max(),ys.min(),ys.max()
    star(x1-10,y0+4,46); star(x0+16,y1-10,30)
    bb=img.getbbox(); img=img.crop(bb)
    img.thumbnail((512,512),Image.LANCZOS)
    return img

import sys
letters=sys.argv[1] if len(sys.argv)>1 else 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
for ch in letters:
    im=render(ch); im.save(os.path.join(OUT,f'letter_{ch}.png')); print(ch,im.size)
# preview sheet
cols=9; cell=180; rows=3
sheet=Image.new('RGB',(cols*cell,rows*cell),(120,180,235))
for i,ch in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    p=os.path.join(OUT,f'letter_{ch}.png')
    if not os.path.exists(p): continue
    im=Image.open(p); im.thumbnail((cell-12,cell-12))
    sheet.paste(im,((i%cols)*cell+6,(i//cols)*cell+6),im)
sheet.save(os.path.join(PREV,'sheet.png'))

