import os,json,base64,urllib.request,io
from pathlib import Path
from PIL import Image
ROOT=Path('flipgold/assets')
im=Image.open('.github/art/special-coins-generated-v6.png').convert('RGBA')
names=['clover','sun','royal','mushroom','berry','bloom','honey','rabbit','river','pearl','shell','tide','crystal','ember','rune','amber','frost','pine','feather','glacier','star','wind','moon','cloud','dawn','aurora','eclipse','dragon','clock','unity']
sheet=Image.new('RGBA',(6*36,5*36))
manifest=json.loads((ROOT/'sprout-v5.json').read_text());manifest['version']=6
for n,name in enumerate(names):
 x=n%6;y=n//6
 crop=im.crop((round(x*im.width/6),round(y*im.height/5),round((x+1)*im.width/6),round((y+1)*im.height/5)))
 bounds=crop.getbbox()
 if bounds:crop=crop.crop(bounds)
 crop.thumbnail((32,32),Image.Resampling.NEAREST)
 tx=x*36+2+(32-crop.width)//2;ty=y*36+2+(32-crop.height)//2
 sheet.paste(crop,(tx,ty))
 manifest['frames']['special/'+name]={'atlas':'special-v6','x':tx,'y':ty,'w':crop.width,'h':crop.height}
sheet.save(ROOT/'special-v6.png',optimize=True)
manifest['sources'].append({'group':'special-v6','author':'Generated for Flipgold','method':'New image generated with image_gen, then individual frames cropped and sampled with nearest-neighbor for game integration','sprites':names})
(ROOT/'sprout-v6.json').write_text(json.dumps(manifest,ensure_ascii=False,separators=(',',':')))
s=base64.b64encode((ROOT/'special-v6.png').read_bytes()).decode();print('SPECIAL_ATLAS:'+s,flush=True)
repo=os.environ['GITHUB_REPOSITORY'];branch=os.environ['GITHUB_REF_NAME'];token=os.environ['GH_TOKEN']
if branch!='flipgold-growth-v6':raise RuntimeError('Staging branch required')
def api(path,data=None,method=None):
 req=urllib.request.Request('https://api.github.com/repos/'+repo+'/'+path,data=None if data is None else json.dumps(data).encode(),method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'Flipgold-special-pack'})
 with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
entries=[]
for f in [ROOT/'special-v6.png',ROOT/'sprout-v6.json']:
 b=api('git/blobs',{'content':base64.b64encode(f.read_bytes()).decode(),'encoding':'base64'});entries.append({'path':str(f),'mode':'100644','type':'blob','sha':b['sha']})
head=api('git/ref/heads/'+branch)['object']['sha'];commit=api('git/commits/'+head);tree=api('git/trees',{'base_tree':commit['tree']['sha'],'tree':entries})
new=api('git/commits',{'message':'Package thirty generated collectible coin faces into the game atlas','tree':tree['sha'],'parents':[head]});api('git/refs/heads/'+branch,{'sha':new['sha'],'force':False},'PATCH')
print('SPECIAL_PACK_COMMIT:'+new['sha'],flush=True)
