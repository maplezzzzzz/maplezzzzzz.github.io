import os,json,urllib.request,urllib.parse,io,base64,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path('flipgold/assets');ROOT.mkdir(parents=True,exist_ok=True)
PRE=Path('pixel-previews');PRE.mkdir(exist_ok=True)
base='https://raw.githubusercontent.com/cbouwense/yafs/d68c9ca212214629c2b1e6301c3e5ae09f3d2681/resources/sprout-lands-sprites/'
sources=[];ims={};frames={};outputs=[]
def get(path):
 data=urllib.request.urlopen(base+urllib.parse.quote(path),timeout=40).read()
 sources.append({'file':path,'author':'Cup Nooble','url':base+urllib.parse.quote(path),'sha256':hashlib.sha256(data).hexdigest()})
 im=Image.open(io.BytesIO(data)).convert('RGBA');print('PIXEL_SOURCE:'+path+':'+str(im.size),flush=True)
 return im
def put(key,im,rect=None):
 ims[key]=im.copy() if rect is None else im.crop((rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3]))
grass=get('Tilesets/Grass.png');dirt=get('Tilesets/Tilled_Dirt.png')
for g,im in [('grass',grass),('dirt',dirt)]:
 for j in range(3):
  for i in range(3):put(g+str(i)+str(j),im,(i*16,j*16,16,16))
water=get('Tilesets/Water.png')
for n in range(4):put('water'+str(n),water,(n*16,0,16,16))
biom=get('Objects/Basic_Grass_Biom_things.png')
for key,rect in {'treeSlim':(0,0,16,32),'tree':(16,0,32,32),'treeFruit':(48,0,32,32),'bush':(16,48,16,16),'bushFruit':(0,48,16,16),'rock':(128,16,16,16),'flowerPink':(80,0,16,16),'flowerPurple':(96,0,16,16),'flowerBlue':(112,0,16,16),'sunflower':(128,32,16,32),'wood':(64,32,16,16),'mushroom':(48,48,16,16),'lily':(96,64,16,16),'grassTuft':(48,64,16,16)}.items():put(key,biom,rect)
house=get('Objects/Free_Chicken_House.png');put('cottage',house)
fence=get('Tilesets/Fences.png')
for n,rect in enumerate([(16,0,16,16),(32,0,16,16),(0,0,16,16),(16,16,16,16),(32,16,16,16)]):put('fence'+str(n),fence,rect)
tools=get('Objects/Basic_tools_and_materials.png')
for key,rect in {'watering':(0,0,16,16),'shovel':(16,0,16,16),'pick':(32,0,16,16),'pail':(0,16,16,16),'axe':(16,16,16,16),'seedBag':(32,16,16,16)}.items():put(key,tools,rect)
plants=get('Objects/Basic_Plants.png')
for key,rect in {'seedling':(16,0,16,16),'wheat':(32,0,16,16),'corn':(48,0,16,16),'eggplant':(80,0,16,16),'carrot':(80,16,16,16),'seed':(0,0,16,16)}.items():put(key,plants,rect)
furniture=get('Objects/Basic_Furniture.png');put('paper',furniture,(0,0,16,16))
char=get('Characters/basic-character-spritesheet.png')
for row in range(4):
 for col in range(4):put('hero'+str(row)+str(col),char,(col*48+8,row*48+8,32,32))
act=get('Characters/basic-character-actions.png')
for row in range(12):
 for col in range(2):put('action'+str(row)+'_'+str(col),act,(col*48,row*48,48,48))
chicken=get('Characters/free-chicken-sprites.png')
for row in range(2):
 for col in range(4):put('chicken'+str(row)+str(col),chicken,(col*16,row*16,16,16))
cow=get('Characters/free-cow-sprites.png')
for row in range(2):
 for col in range(3):put('cow'+str(row)+str(col),cow,(col*32,row*32,32,32))
nest=get('Characters/egg-and-nest.png');put('nest',nest,(48,0,16,16))
ch=get('Objects/Chest.png')
for col in range(3):put('sproutChest'+str(col),ch,(col*48,0,48,48))
bridge=get('Objects/Wood_Bridge.png');put('bridge',bridge,(32,0,48,32))
url='https://raw.githubusercontent.com/linuskar/DATX11-DIT561-Bachelor-Project-Group-48/cc41c8474e12fff716ef0af9770cd1ed702eb187/assets/coins-chests-etc-2-0.png'
data=urllib.request.urlopen(url,timeout=40).read();money=Image.open(io.BytesIO(data)).convert('RGBA')
sources.append({'author':'greatdocbrown','license':'CC0','url':url,'sha256':hashlib.sha256(data).hexdigest()})
print('PIXEL_SOURCE:coins:'+str(money.size),flush=True)
for row in range(4):
 for n in range(6):put('coin'+str(row)+'_'+str(n),money,(64+n*16,16+row*16,16,16))
for row in range(4):
 for n in range(6):put('gem'+str(row)+'_'+str(n),money,(80+n*16,368+row*16,16,16))
for n in range(4):put('chest'+str(n),money,(448+n*32,672,32,16))
for key,rect in {'star':(64,192,16,16),'heart':(320,192,16,16),'bag':(464,480,16,16),'key':(464,384,32,16),'book':(512,544,16,16),'lock':(720,384,16,16),'potion':(624,192,16,32),'note':(544,16,48,16)}.items():put(key,money,rect)
cols=12;cell=84;sheet=Image.new('RGBA',(cols*cell,((len(ims)+cols-1)//cols)*cell))
preview=Image.new('RGB',(cols*96,((len(ims)+cols-1)//cols)*96),'#eff0db');draw=ImageDraw.Draw(preview)
for n,(key,im) in enumerate(ims.items()):
 x=n%cols*cell+2;y=n//cols*cell+2;sheet.paste(im,(x,y))
 frames['pixel/'+key]={'atlas':'sprout-v5','x':x,'y':y,'w':im.width,'h':im.height}
 k=max(1,min(4,72//max(im.size)));thumb=im.resize((im.width*k,im.height*k),Image.Resampling.NEAREST)
 px=n%cols*96+(96-thumb.width)//2;py=n//cols*96+4;preview.paste(thumb,(px,py),thumb);draw.text((n%cols*96+3,n//cols*96+78),key,fill='#3f5d58')
file=ROOT/'sprout-v5.png';sheet.save(file,optimize=True);outputs.append(file)
file=ROOT/'sprout-v5.json';file.write_text(json.dumps({'version':5,'frames':frames,'sources':sources},ensure_ascii=False,separators=(',',':')));outputs.append(file)
file=ROOT/'CREDITS-Sprout.md';file.write_text('# Flipgold artwork 5.0\n\nSprout Lands Basic: Cup Nooble. https://cupnooble.itch.io/sprout-lands-asset-pack\nFree Basic license: non-commercial project use only. Modification allowed. No resale or redistribution as an asset pack. Credit Cup Nooble. Game-specific selected frames are packed into the application atlas; this is not a standalone asset pack. Commercial projects require the premium license.\n\nCoins & Gems & Chests & More: greatdocbrown. https://greatdocbrown.itch.io/coins-gems-etc\nCC0. Selected frames from coins-chests-etc-2-0.png.\n\nThe uploaded attachments could not be opened by the current file service. Equivalent Basic PNG sheets were obtained from a public game source mirror pinned by commit, and the author-provided PNG alternative was obtained from a public source mirror. File hashes and exact URLs are recorded in sprout-v5.json. No game code from those mirrors was copied.\n');outputs.append(file)
p=PRE/'contact.jpg';preview.save(p,quality=90);s=base64.b64encode(p.read_bytes()).decode()
for i in range(0,len(s),5000):print('PIXEL_PREVIEW:contact:'+str(i//5000)+':'+s[i:i+5000],flush=True)
repo=os.environ['GITHUB_REPOSITORY'];branch=os.environ['GITHUB_REF_NAME'];token=os.environ['GH_TOKEN']
if branch!='flipgold-sprout-v5':raise RuntimeError('Staging branch required')
def api(path,data=None,method=None):
 req=urllib.request.Request('https://api.github.com/repos/'+repo+'/'+path,data=None if data is None else json.dumps(data).encode(),method=method,headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'Flipgold-pixel-import'})
 with urllib.request.urlopen(req,timeout=45) as r:return json.load(r)
entries=[]
for file in outputs:
 blob=api('git/blobs',{'content':base64.b64encode(file.read_bytes()).decode(),'encoding':'base64'});entries.append({'path':str(file),'mode':'100644','type':'blob','sha':blob['sha']})
head=api('git/ref/heads/'+branch)['object']['sha'];commit=api('git/commits/'+head);tree=api('git/trees',{'base_tree':commit['tree']['sha'],'tree':entries})
new=api('git/commits',{'message':'Package selected Cup Nooble and greatdocbrown sprites for the pixel garden','tree':tree['sha'],'parents':[head]});api('git/refs/heads/'+branch,{'sha':new['sha'],'force':False},'PATCH')
print('PIXEL_IMPORT_COMMIT:'+new['sha'],flush=True)
