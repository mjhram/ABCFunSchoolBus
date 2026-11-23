import os
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage as ndi
SRC=r'C:\Users\hp2\Downloads\app4\assets_new'
OUT=r'C:\Users\hp2\Downloads\app4\ABCFunSchoolBus\assets\resources\textures'
REV=r'C:\Users\hp2\Downloads\app4\review'
PICKS={ # output name : source file
 'kid_boy_backpack':'kid_boy_backpack_v1','kid_boy_glasses':'kid_boy_glasses_v1','kid_girl_curly':'kid_girl_curly_v1',
 'kid_girl_pigtails':'kid_girl_pigtails_v1','kid_girl_scarf':'kid_girl_scarf_v2','kid_toddler_teddy':'kid_toddler_teddy_v1',
 'prop_balloon_arch':'prop_balloon_arch_v1','prop_barrier':'prop_barrier_v1','prop_bus_shelter':'prop_bus_shelter_v1',
 'prop_bus_stop_sign':'prop_bus_stop_sign_v2','prop_cone':'prop_cone_v1','prop_cone_pair':'prop_cone_pair_v1',
 'prop_cow_road':'prop_cow_road_v1','prop_crossing_sign':'prop_crossing_sign_v1','prop_duck_family':'prop_duck_family_v1',
 'prop_finish_arch':'prop_finish_arch_v2','prop_hay':'prop_hay_v2','prop_puddle':'prop_puddle_v2','prop_sheep':'prop_sheep_v1',
 'prop_star_gate':'prop_star_gate_v2','prop_stop_sign':'prop_stop_sign_v1'}
def cutout(im):
    a=np.asarray(im.convert('RGB')).astype(float)
    h,w,_=a.shape
    border=np.concatenate([a[0],a[-1],a[:,0],a[:,-1]])
    bg=np.median(border,axis=0)
    white = bg.min()>225
    tol = 48 if white else 80
    d=np.sqrt(((a-bg)**2).sum(axis=2))
    cand=d<tol
    if white:   # soft grey shadows: low-saturation light pixels also count as background
        cand |= ((a.min(axis=2)>205)&((a.max(axis=2)-a.min(axis=2))<16))
    lab,n=ndi.label(cand)
    edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
    bgmask=np.isin(lab,list(edge))
    fg=~bgmask
    fg=ndi.binary_opening(fg,iterations=1)
    lab2,n2=ndi.label(fg)
    if n2>1:   # keep components bigger than 0.3% of the image (drops stray specks)
        sizes=ndi.sum(fg,lab2,range(1,n2+1)); keep=[i+1 for i,s in enumerate(sizes) if s>0.003*h*w]
        fg=np.isin(lab2,keep)
    fg=ndi.binary_fill_holes(fg) if False else fg
    fg=ndi.binary_erosion(fg,iterations=1)
    alpha=ndi.gaussian_filter(fg.astype(float),1.1)
    rgba=np.dstack([a,alpha*255]).astype('uint8')
    img=Image.fromarray(rgba,'RGBA'); bb=img.getbbox(); return img.crop(bb)
done=[]
for out,src in PICKS.items():
    im=Image.open(os.path.join(SRC,'asset_'+src+'.webp'))
    r=cutout(im); r.thumbnail((512,512),Image.LANCZOS); r.save(os.path.join(OUT,out+'.png')); done.append((out,r))
# review sheet on a dark road-grey + a light sky background
cell=210; cols=7; rows=(len(done)+cols-1)//cols
sh=Image.new('RGB',(cols*cell,rows*(cell+14)),(70,70,85)); dr=ImageDraw.Draw(sh)
for i,(n,im) in enumerate(done):
    t=im.copy(); t.thumbnail((cell-8,cell-8)); x=(i%cols)*cell+4; y=(i//cols)*(cell+14)+2
    sh.paste(t,(x,y),t); dr.text((x,y+cell-4),n,fill=(255,255,255))
sh.save(os.path.join(REV,'picks_dark.jpg'),quality=88)
print(len(done),'imported')
