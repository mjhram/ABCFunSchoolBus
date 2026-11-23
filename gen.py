import json, uuid, os, random, string
root=r'C:\Users\hp2\Downloads\app4\ABCFunSchoolBus'
B64='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
def compress(u):
    h=u.replace('-','')
    out=h[:5]
    rest=h[5:]
    for i in range(0,len(rest),3):
        v=int(rest[i:i+3],16)
        out+=B64[v>>6]+B64[v&63]
    return out
def rid(): return compress(str(uuid.uuid4()))
script_uuid='7c1d2a10-3b4e-4f5a-8c9d-0e1f2a3b4c5d'
scene_uuid='5e8f9a01-2b3c-4d5e-9f60-71829304a5b6'
cls=compress(script_uuid)
def meta(importer,u,ver,extra=None):
    m={"ver":ver,"importer":importer,"imported":True,"uuid":u,"files":[".json"] if importer in('scene','typescript') else [],"subMetas":{},"userData":{}}
    if extra: m.update(extra)
    return m
def w(p,o):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    open(p,'w',encoding='utf8').write(json.dumps(o,indent=2))
w(root+r'\package.json',{"_version":"1.0.0","name":"abc-fun-school-bus","uuid":str(uuid.uuid4()),"creator":{"version":"3.8.8"},"type":"2d"} )
w(root+r'\assets\scripts\GameMain.ts.meta',meta('typescript',script_uuid,'4.0.24'))
w(root+r'\assets\scenes\main.scene.meta',meta('scene',scene_uuid,'1.1.50'))
for d in ('scenes','scripts','resources','resources/textures'):
    p=os.path.join(root,'assets',d)
    # folder metas (directory importer)
    w(p+'.meta',{"ver":"1.2.0","importer":"directory","imported":True,"uuid":str(uuid.uuid4()),"files":[],"subMetas":{},"userData":{}} )
V3=lambda x,y,z:{"__type__":"cc.Vec3","x":x,"y":y,"z":z}
Q={"__type__":"cc.Quat","x":0,"y":0,"z":0,"w":1}
def node(name,parent,children,comps,pos,layer):
    return {"__type__":"cc.Node","_name":name,"_objFlags":0,"__editorExtras__":{},"_parent":{"__id__":parent} if parent is not None else None,"_children":[{"__id__":c} for c in children],"_active":True,"_components":[{"__id__":c} for c in comps],"_prefab":None,"_lpos":pos,"_lrot":Q,"_lscale":V3(1,1,1),"_mobility":0,"_layer":layer,"_euler":V3(0,0,0),"_id":rid()}
comp=lambda t,n,**k: dict({"__type__":t,"_name":"","_objFlags":0,"__editorExtras__":{},"node":{"__id__":n},"_enabled":True,"__prefab":None},**k,_id=rid())
arr=[
 {"__type__":"cc.SceneAsset","_name":"main","_objFlags":0,"__editorExtras__":{},"_native":"","scene":{"__id__":1}},
 {"__type__":"cc.Scene","_name":"main","_objFlags":0,"__editorExtras__":{},"_parent":None,"_children":[{"__id__":2}],"_active":True,"_components":[],"_prefab":None,"_lpos":V3(0,0,0),"_lrot":Q,"_lscale":V3(1,1,1),"_mobility":0,"_layer":1073741824,"_euler":V3(0,0,0),"autoReleaseAssets":False,"_id":str(uuid.uuid4())},
 node("Canvas",1,[3],[4,5,6],V3(640,360,0),33554432),
 node("Camera",2,[],[7],V3(0,0,1000),1073741824),
 comp("cc.UITransform",2,_contentSize={"__type__":"cc.Size","width":1280,"height":720},_anchorPoint={"__type__":"cc.Vec2","x":0.5,"y":0.5}),
 comp("cc.Canvas",2,_cameraComponent={"__id__":7},_alignCanvasWithScreen=True),
 comp(cls,2),
 comp("cc.Camera",3,_projection=0,_priority=0,_fov=45,_fovAxis=0,_orthoHeight=360,_near=1,_far=2000,_color={"__type__":"cc.Color","r":135,"g":206,"b":235,"a":255},_depth=1,_stencil=0,_clearFlags=7,_rect={"__type__":"cc.Rect","x":0,"y":0,"width":1,"height":1},_aperture=19,_shutter=7,_iso=0,_screenScale=1,_visibility=1108344832,_targetTexture=None,_postProcess=None,_usePostProcess=False,_cameraType=-1,_trackingType=0),
]
w(root+r'\assets\scenes\main.scene',arr)
print('class id',cls)
