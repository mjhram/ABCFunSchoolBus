import glob, os
from PIL import Image, ImageDraw
d=r'C:\Users\hp2\Downloads\app4\assets_new'
os.makedirs(r'C:\Users\hp2\Downloads\app4\review',exist_ok=True)
def sheet(files,out,cols,cell):
    rows=(len(files)+cols-1)//cols
    sh=Image.new('RGB',(cols*cell,rows*(cell+16)),(205,205,215))
    dr=ImageDraw.Draw(sh)
    for i,f in enumerate(files):
        im=Image.open(f).convert('RGB'); im.thumbnail((cell-6,cell-6))
        x=(i%cols)*cell+3; y=(i//cols)*(cell+16)+3
        sh.paste(im,(x,y)); dr.text((x,y+cell-2),os.path.basename(f).replace('asset_','').replace('.webp',''),fill=(0,0,0))
    sh.save(out,quality=85)
kids=sorted(glob.glob(d+r'\asset_kid_*.webp')); sheet(kids,r'C:\Users\hp2\Downloads\app4\review\kids.jpg',6,230)
props=sorted(glob.glob(d+r'\asset_prop_*.webp'))
sheet(props[:20],r'C:\Users\hp2\Downloads\app4\review\props1.jpg',5,250)
sheet(props[20:],r'C:\Users\hp2\Downloads\app4\review\props2.jpg',5,250)
print(len(kids),len(props))
