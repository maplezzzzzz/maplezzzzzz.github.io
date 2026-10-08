
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const URL='http://127.0.0.1:4173/flipgold/';
require('fs').mkdirSync('game-previews',{recursive:true});
let activeChecks=[];
const emitImage=name=>{const fs=require('fs'),p='game-previews/'+name+'.jpg';if(!fs.existsSync(p))return;const b=fs.readFileSync(p).toString('base64');for(let i=0;i<b.length;i+=5000)console.log('ADVENTURE_IMAGE:'+name+':'+(i/5000)+':'+b.slice(i,i+5000));};
(async()=>{
 const browser=await chromium.launch({headless:true});
 const errors=[],checks=activeChecks;
 const report=c=>{checks.push(c);console.log('PASSED:'+c);};
 const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
 const page=await context.newPage();page.on('pageerror',e=>{errors.push(e.message);console.log('PAGE_ERROR:'+e.message);});
 const open=async p=>{const r=await p.goto(URL,{waitUntil:'domcontentloaded',timeout:30000});assert.equal(r.status(),200);await p.waitForFunction(()=>typeof Town==='function'&&artReady,{timeout:15000});};
 const tap=async(id,p=page)=>{
  await p.waitForTimeout(90);
  if(!await p.evaluate(id=>hits.some(h=>h.id===id),id)){
   await p.evaluate(()=>{if(scrollArea)scroll=maxScroll;});await p.waitForTimeout(100);
  }
  try{await p.waitForFunction(id=>hits.some(h=>h.id===id),id,{timeout:5000});}catch(e){console.log('TAP_DIAG:'+JSON.stringify(await p.evaluate(()=>({hits:hits.map(h=>h.id),intro,started,lockBlocked,lockOwned,TAB_ID,lock:localStorage.getItem(LOCK_KEY),hidden:document.hidden,H,screenH,scale,lastOwnSave:!!lastOwnSave,storedMatches:localStorage.getItem(STORE_KEY)===lastOwnSave,artReady}))));await snap('failure',p);emitImage('failure');throw e;}
  const v=await p.evaluate(id=>{const h=hits.find(h=>h.id===id);return{x:ox+(h.x+h.w/2)*scale,y:oy+(h.y+h.h/2)*scale};},id);
  await p.touchscreen.tap(v.x,v.y);await p.waitForTimeout(160);
 };
 const snap=async(name,p=page)=>p.screenshot({path:'game-previews/'+name+'.jpg',type:'jpeg',quality:65});
 await open(page);assert.equal(await page.evaluate(()=>BUILD),'庭院奇遇 · 3.0');await snap('intro');await tap('start');
 let p=await page.evaluate(()=>{const p=pos(0);return{x:ox+p.x*scale,y:oy+p.y*scale};});
 await page.touchscreen.tap(p.x,p.y);await page.waitForTimeout(100);
 assert.equal(await page.evaluate(()=>town.s.manual),1);assert.ok(await page.evaluate(()=>flying.length&&floaters.length));
 assert.equal(await page.evaluate(()=>audio.ctx.state),'running');report('real touch flip, moving rewards and audio');
 await page.evaluate(()=>{town.cd.fill(0);town.shiny={i:0,start:time,until:time+5000};});
 const sparkBefore=await page.evaluate(()=>town.s.play.sparkHits);
 await page.touchscreen.tap(p.x,p.y);await page.waitForTimeout(150);
 assert.equal(await page.evaluate(()=>town.s.play.sparkHits),sparkBefore+1);
 assert.ok(await page.evaluate(()=>floaters.some(f=>f.text==='闪光 ×3')));report('targeted sparkling coin');
 await page.evaluate(()=>town.gain(6000));await tap('quickCoin');await tap('quickCoin');await tap('nav-tools');await tap('buy-shovel');
 assert.equal(await page.evaluate(()=>modal.id),'shovel');await tap('upgradeOK');await tap('nav-pet');await tap('recruit');await tap('upgradeOK');
 assert.equal(await page.evaluate(()=>modal.kind),'choice');await snap('gift-choice');await tap('chooseNest');
 assert.equal(await page.evaluate(()=>town.s.play.charm),'nest');await page.waitForTimeout(1400);
 assert.ok(await page.evaluate(()=>town.s.petFlips>=1));await tap('feed');assert.ok(await page.evaluate(()=>town.feedUntil>time));report('early animal, playstyle choice and feeding');
 await page.evaluate(()=>{modal=null;cinema=null;town.cd.fill(0);});
 p=await page.evaluate(()=>{const p=pos(0);return{x:ox+p.x*scale,y:oy+p.y*scale};});
 await page.mouse.move(p.x,p.y);await page.mouse.down();await page.waitForTimeout(90);await page.mouse.move(5,100);await page.waitForTimeout(100);
 assert.equal(await page.evaluate(()=>hold),-1);
 const manual=await page.evaluate(()=>town.s.manual);await page.waitForTimeout(1100);assert.equal(await page.evaluate(()=>town.s.manual),manual);await page.mouse.up();report('dragging outside the garden stops repeated flips');
 await page.evaluate(()=>{town.visitor={kind:'gift',start:time-2000,until:time+10000};});
 const visits=await page.evaluate(()=>town.s.play.visits);await tap('visitor');assert.equal(await page.evaluate(()=>town.s.play.visits),visits+1);report('visitor reward');
 await tap('nav-tools');await tap('shopExplore');await tap('buy-land');
 for(let i=0;i<3;i++){await tap('dig');await page.waitForTimeout(230);}await snap('excavation');
 for(let i=0;i<2;i++){await tap('dig');await page.waitForTimeout(230);}
 await page.waitForFunction(()=>modal?.kind==='treasure',{timeout:5000});await snap('treasure-story');
 assert.equal(await page.evaluate(()=>town.s.land),1);assert.ok(await page.evaluate(()=>town.s.coins.includes('clover')));await tap('treasureOK');report('five excavation layers, lid animation and guaranteed rare coin');
 await tap('nav-tools');await tap('shopTools');await tap('buy-wide');await tap('upgradeOK');
 await page.evaluate(()=>{town.cd.fill(0);town.petFlight=null;town.petAt=time+2000;});
 const uses=await page.evaluate(()=>town.s.play.skillUses);await tap('skill');assert.equal(await page.evaluate(()=>town.s.play.skillUses),uses+1);assert.ok(await page.evaluate(()=>town.skillAt>time));
 await tap('nav-tools');await tap('shopTools');await tap('buy-power');await tap('nav-pet');await tap('petUpgrade');await tap('petUpgrade');await tap('charmSpark');await tap('nav-home');
 assert.equal(await page.evaluate(()=>town.s.pet),3);assert.equal(await page.evaluate(()=>town.s.play.charm),'spark');
 await page.evaluate(()=>{dialogue=null;dialogueQueue=[];toastState=null;town.shiny={i:4,start:time,until:time+5000};});
 await page.waitForTimeout(300);console.log('CANVAS_DIAG:'+JSON.stringify(await page.evaluate(()=>({w:canvas.width,h:canvas.height,H,screenH,rect:canvas.getBoundingClientRect().toJSON(),bottom:Array.from(cx.getImageData(195,H-30,1,1).data)}))));await snap('garden');report('wide shovel, active skill, animal wardrobe and free charm switch');
 await page.evaluate(()=>{town.visitor={kind:'rain',start:time-2000,until:time+10000};});await tap('visitor');assert.equal(await page.evaluate(()=>town.buff.kind),'rain');
 await page.evaluate(()=>{town.s.manual+=35;});await tap('nav-journal');await tap('deliver');
 assert.equal(await page.evaluate(()=>town.s.play.deliveries),1);report('rain changes coin recovery and repeatable commission pays');
 await tap('nav-tools');await tap('shopExplore');await tap('buy-land');
 for(let i=0;i<5;i++){await tap('dig');await page.waitForTimeout(230);}
 await page.waitForFunction(()=>modal?.kind==='treasure',{timeout:5000});await tap('treasureOK');await tap('nav-tools');await tap('shopTools');await tap('buy-magnet');await tap('upgradeOK');
 assert.ok(await page.evaluate(()=>town.targets(0).some(i=>SLOTS[i][1]!==SLOTS[0][1])));report('magnet reaches neighboring rows');
 await page.evaluate(()=>town.gain(7000));await tap('nav-tools');await tap('shopExplore');await tap('buy-clock');await page.waitForFunction(()=>modal?.kind==='victory',{timeout:6000});
 await snap('clock-letter');assert.ok(await page.evaluate(()=>town.s.clock));await tap('victoryOK');report('restored clock and final letter');
 await tap('settings');await tap('toggle-sound');await tap('settingsOK');
 const state=await page.evaluate(()=>{save();return {coins:town.s.coins.length,pet:town.s.pet,tool:town.s.tool,land:town.s.land,charm:town.s.play.charm,clock:town.s.clock,sound:town.s.sound};});
 await page.reload({waitUntil:'domcontentloaded'});await page.waitForFunction(()=>artReady);await tap('start');
 assert.deepEqual(await page.evaluate(()=>({coins:town.s.coins.length,pet:town.s.pet,tool:town.s.tool,land:town.s.land,charm:town.s.play.charm,clock:town.s.clock,sound:town.s.sound})),state);report('new mechanics survive reload');
 await page.setViewportSize({width:360,height:640});await page.waitForTimeout(250);await tap('nav-pet');await tap('nav-home');
 assert.ok(await page.evaluate(()=>hits.every(h=>h.x>=0&&h.x+h.w<=390&&h.y>=0&&h.y+h.h<=H)));await snap('phone360');report('360 by 640 and 390 by 844 mobile layouts');
 await page.setViewportSize({width:390,height:844});await page.waitForTimeout(150);
 const unit=await page.evaluate(()=>{
  const assert=(ok,m)=>{if(!ok)throw new Error(m);};const out=[];
  const bad=new Town().s;bad.coins=['constructor'];assert(!validV2(bad),'prototype types');
  const g=new Town(null,()=>.99);g.s.coins=['copper','copper','copper'];g.s.tool=2;g.s.land=1;g.s.pet=1;g.petFlight={i:0,arrive:650};g.cd[1]=g.cd[2]=10000;assert(g.skill(1).length===0&&g.skillAt===0,'no wasted skill');
  const fast=new Town(null,()=>.99),slow=new Town(null,()=>.99);
  for(const a of [fast,slow]){a.s.coins=['copper','copper','copper'];a.s.tool=1;a.s.pet=7;a.sparkAt=Infinity;a.visitAt=Infinity;}
  for(let n=0;n<=3600;n++)fast.tick(n*1000/60);for(let n=0;n<=60;n++)slow.tick(n*1000);
  assert(Math.abs(fast.s.petFlips-slow.s.petFlips)<=1,'pet clock');
  const d=new Town(null,()=>0);d.s.coins=['copper','copper','copper'];d.s.tool=1;d.s.pet=1;d.s.dig=5;
  assert(d.dig(0).remaining===4&&!d.dig(100),'dig cadence');for(let t=400;t<=1600;t+=400)d.dig(t);
  assert(d.s.coins.includes('clover')&&d.s.play.nuts===2,'guaranteed loot');assert(d.offline(-1)===0&&d.gain(Infinity)===0,'finite economy');
  d.setCharm('nest');d.s.play.nuts=1;assert(d.feed(2000)&&!d.feed(2100)&&d.s.play.nuts===0,'feed cost');
  return {fastPet:fast.s.petFlips,slowPet:slow.s.petFlips};
 });report('economy boundaries, skill reservation, feed cost and frame independent animal');
 // Two visible pages share one storage namespace; the second cannot overwrite the first.
 const second=await context.newPage();second.on('pageerror',e=>errors.push(e.message));await open(second);
 assert.equal(await second.evaluate(()=>lockBlocked),true);
 const rawBefore=await page.evaluate(()=>localStorage.getItem(STORE_KEY));assert.equal(await second.evaluate(()=>save()),false);assert.equal(await second.evaluate(()=>localStorage.getItem(STORE_KEY)),rawBefore);
 await page.evaluate(()=>{paused=true;});const lease=await page.evaluate(()=>JSON.parse(localStorage.getItem(LOCK_KEY)).until);
 await page.waitForTimeout(5500);assert.ok(await page.evaluate(()=>JSON.parse(localStorage.getItem(LOCK_KEY)).until)>lease);
 await second.evaluate(()=>{localStorage.setItem(LOCK_KEY,JSON.stringify({owner:'test-other-owner',until:Date.now()+30000}));const s=JSON.parse(localStorage.getItem(STORE_KEY));s.gold=Math.max(0,s.gold-1);localStorage.setItem(STORE_KEY,JSON.stringify(s));});
 await page.waitForTimeout(150);assert.equal(await page.evaluate(()=>lockBlocked),true);
 const latest=await second.evaluate(()=>localStorage.getItem(STORE_KEY));assert.equal(await page.evaluate(()=>save()),false);assert.equal(await page.evaluate(()=>localStorage.getItem(STORE_KEY)),latest);report('tab ownership, paused heartbeat and stale writer protection');
 const legacyContext=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 await legacyContext.addInitScript(()=>{
  const k='flipgold-mobile-v2';if(!localStorage.getItem(k))localStorage.setItem(k,JSON.stringify({v:2,gold:400,total:600,manual:100,petGold:50,petFlips:20,coins:['copper','copper','copper','copper','clover'],tool:1,power:2,land:1,dig:0,pet:2,clock:false,claimed:[0,1,2,3,4],started:true,seconds:100,sound:true,music:true,haptic:true,lastSeen:Date.now()-60000}));
 });
 const legacy=await legacyContext.newPage();legacy.on('pageerror',e=>errors.push(e.message));await open(legacy);
 assert.equal(await legacy.evaluate(()=>town.s.coins.length),5);assert.ok(await legacy.evaluate(()=>town.s.gold>400&&town.s.play.rev===3));assert.ok(await legacy.evaluate(()=>localStorage.getItem(STORE_KEY+'-before-adventure')));
 await tap('start',legacy);await tap('offlineOK',legacy);await tap('chooseNest',legacy);await legacy.evaluate(()=>save());await legacy.reload();await legacy.waitForFunction(()=>artReady);assert.equal(await legacy.evaluate(()=>town.s.play.charm),'nest');report('v2 progress migration and offline income');
 const pauseContext=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const pausePage=await pauseContext.newPage();pausePage.on('pageerror',e=>errors.push(e.message));await open(pausePage);await tap('start',pausePage);
 await pausePage.evaluate(()=>{town.s.coins=['copper','copper','copper'];town.s.tool=1;town.s.pet=1;town.s.play.charm='nest';save();});
 await tap('settings',pausePage);await tap('pause',pausePage);
 const pausedState=await pausePage.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>true});document.dispatchEvent(new Event('visibilitychange'));return {gold:town.s.gold,seconds:town.s.seconds};});
 await pausePage.waitForTimeout(1800);
 await pausePage.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,get:()=>false});document.dispatchEvent(new Event('visibilitychange'));});
 assert.deepEqual(await pausePage.evaluate(()=>({gold:town.s.gold,seconds:town.s.seconds})),pausedState);
 await tap('pause',pausePage);await pausePage.waitForTimeout(150);assert.ok(await pausePage.evaluate(s=>town.s.seconds-s<.8,pausedState.seconds));report('paused background pays nothing and does not double count elapsed time');
 assert.deepEqual(errors,[]);
 console.log('ADVENTURE_CHECK_RESULT:'+JSON.stringify({checks,unit,state,errors}));
 for(const name of ['intro','gift-choice','garden','phone360','treasure-story','clock-letter'])emitImage(name);
 await browser.close();
})().catch(e=>{console.error(e);console.log('ADVENTURE_PARTIAL_RESULT:'+JSON.stringify(activeChecks));const fs=require('fs');const p=['garden','treasure-story','gift-choice','intro'].map(n=>'game-previews/'+n+'.jpg').find(p=>fs.existsSync(p));if(p)emitImage(p.split('/').pop().replace('.jpg',''));process.exit(1);});
