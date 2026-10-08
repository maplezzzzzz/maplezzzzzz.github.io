import os,json,urllib.request,urllib.parse,zipfile,io,base64,hashlib,time
from pathlib import Path
from PIL import Image,ImageDraw
SPEC=json.loads(Path('.github/flipgold-asset-sources.json').read_text())
ROOT=Path('flipgold/assets');ROOT.mkdir(parents=True,exist_ok=True)
PRE=Path('asset-previews');PRE.mkdir(exist_ok=True)
def download(url):
 for attempt in range(3):
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Flipgold-asset-import/1.0'}),timeout=45) as r:return r.read()
  except Exception:
   if attempt==2:raise
   time.sleep(1)
def emit(name,data):
 s=base64.b64encode(data).decode()
 for i in range(0,len(s),5000):print('ASSET_IMAGE:'+name+':'+str(i//5000)+':'+s[i:i+5000],flush=True)
frames={};sources=[];outputs=[]
def atlas(group,images):
 images=sorted(images.items());cell=196;cols=8;rows=(len(images)+cols-1)//cols
 sheet=Image.new('RGBA',(cols*cell,rows*cell),(0,0,0,0))
 preview=Image.new('RGB',(8*112,rows*112),'#edf1e6');draw=ImageDraw.Draw(preview)
 for n,(name,im) in enumerate(images):
  bounds=im.getbbox()
  if bounds:im=im.crop(bounds)
  im.thumbnail((192,192),Image.Resampling.LANCZOS)
  x=n%cols*cell+2;y=n//cols*cell+2;sheet.paste(im,(x,y))
  frames[group+'/'+name]={'atlas':group,'x':x,'y':y,'w':im.width,'h':im.height}
  thumb=im.copy();thumb.thumbnail((76,76),Image.Resampling.LANCZOS)
  px=n%8*112+(112-thumb.width)//2;py=n//8*112+3;preview.paste(thumb,(px,py),thumb)
  label=name.replace('genericItem_color_','').replace('isometric','').replace('.png','')
  draw.text((n%8*112+4,n//8*112+82),label[:18],fill='#354335')
 file=ROOT/(group+'.png');sheet.save(file,optimize=True);outputs.append(file)
 p=PRE/(group+'.jpg');preview.save(p,quality=75);emit(group,p.read_bytes())
 print('ASSET_LIST:'+group+':'+json.dumps([n for n,_ in images]),flush=True)
 print('ASSET_ATLAS:'+json.dumps({'group':group,'count':len(images),'bytes':file.stat().st_size}),flush=True)
fluent=SPEC['fluent'];ims={}
for name in fluent['names']:
 slug=name.lower().replace(' ','_')
 url='https://raw.githubusercontent.com/microsoft/fluentui-emoji/'+fluent['commit']+'/assets/'+urllib.parse.quote(name)+'/3D/'+slug+'_3d.png'
 data=download(url);ims[slug+'.png']=Image.open(io.BytesIO(data)).convert('RGBA')
 sources.append({'key':'fluent/'+slug+'.png','author':'Microsoft','license':'MIT','url':url,'sha256':hashlib.sha256(data).hexdigest()})
atlas('fluent',ims)
lic=ROOT/'LICENSE-Fluent-MIT.txt';lic.write_bytes(download('https://raw.githubusercontent.com/microsoft/fluentui-emoji/'+fluent['commit']+'/LICENSE'));outputs.append(lic)
for pack in SPEC['packs']:
 raw=download(pack['url']);z=zipfile.ZipFile(io.BytesIO(raw));ims={}
 for info in z.infolist():
  p=info.filename
  if not p.lower().endswith('.png') or any(s in p.lower() for s in ['preview','sample','spritesheet','tilemap']):continue
  if pack['id']=='items' and 'Colored/' not in p and '/Colored/' not in p:continue
  if pack['id']=='farm':
   if not p.startswith('Angle/') or not p.endswith('_S.png'):continue
  elif '/PNG/' not in '/'+p and not p.startswith('PNG/'):continue
  name=p.split('/')[-1];im=Image.open(io.BytesIO(z.read(info))).convert('RGBA')
  if name not in ims or im.width>ims[name].width:ims[name]=im
 if not ims:raise RuntimeError('No sprites in '+pack['id']+' '+str(z.namelist()[:40]))
 atlas(pack['id'],ims)
 licenses=[i for i in z.namelist() if 'license' in i.lower() and i.lower().endswith('.txt')]
 if not licenses:raise RuntimeError('Missing original license')
 original=z.read(licenses[0]).decode('utf-8-sig')
 if 'CC0' not in original and 'Creative Commons Zero' not in original:raise RuntimeError('Unexpected license')
 file=ROOT/('LICENSE-Kenney-'+pack['id']+'.txt');file.write_text(original);outputs.append(file)
 sources.append({'group':pack['id'],'author':'Kenney','license':'CC0','page':pack['page'],'archive':pack['url'],'archiveSha256':hashlib.sha256(raw).hexdigest()})
manifest=ROOT/'sprites.json';manifest.write_text(json.dumps({'version':1,'frames':frames,'sources':sources},ensure_ascii=False,separators=(',',':')));outputs.append(manifest)
credits=ROOT/'CREDITS.md';credits.write_text('# Game assets\n\nMicrosoft Fluent Emoji: MIT. Copyright Microsoft Corporation. See LICENSE-Fluent-MIT.txt.\nhttps://github.com/microsoft/fluentui-emoji\n\nKenney: Isometric Miniature Farm, UI Pack RPG Expansion, Generic Items. CC0. Original licenses included.\nhttps://kenney.nl/assets\n\nSprites were cropped to transparent bounds, resized for mobile use, and packed into local PNG atlases. Download URLs and SHA-256 hashes are in sprites.json.\n');outputs.append(credits)
repo=os.environ['GITHUB_REPOSITORY'];branch=os.environ['GITHUB_REF_NAME'];token=os.environ['GH_TOKEN']
if branch!='flipgold-world-v4':raise RuntimeError('Import only allowed on the staging branch')
def api(path,data=None,method=None):
 req=urllib.request.Request('https://api.github.com/repos/'+repo+'/'+path,data=None if data is None else json.dumps(data).encode(),method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'Flipgold-asset-import'})
 with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
entries=[]
for file in outputs:
 blob=api('git/blobs',{'content':base64.b64encode(file.read_bytes()).decode(),'encoding':'base64'})
 entries.append({'path':str(file),'mode':'100644','type':'blob','sha':blob['sha']})
head=api('git/ref/heads/'+branch)['object']['sha'];commit=api('git/commits/'+head)
tree=api('git/trees',{'base_tree':commit['tree']['sha'],'tree':entries})
new=api('git/commits',{'message':'Import licensed Fluent and Kenney art as local mobile atlases','tree':tree['sha'],'parents':[head]})
api('git/refs/heads/'+branch,{'sha':new['sha'],'force':False},'PATCH')
print('ASSET_IMPORT_COMMIT:'+new['sha'],flush=True)
