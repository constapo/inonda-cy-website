// INONDA LTD Carpentry UX smoke test and screenshots, for the PR preview only.
// Does not interact with production, accounts or live customers.
import assert from 'node:assert/strict';
import {chromium} from 'playwright';
import fs from 'node:fs';
const base='http://127.0.0.1:8899/';
fs.mkdirSync('carpentry-screenshots',{recursive:true});
const browser=await chromium.launch({headless:true});
async function openPage(locale,path='',size={width:1440,height:960}){
 const page=await browser.newPage({viewport:size,reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(base+locale+'/carpentry/'+path,{waitUntil:'domcontentloaded',timeout:30000});
 await page.locator('main h1').waitFor();
 assert.equal(await page.locator('html').getAttribute('lang'),locale);
 assert.equal(await page.locator('html').getAttribute('dir'),locale==='he'?'rtl':'ltr');
 assert.equal(await page.locator('header .brand img').count(),1);
 assert.equal(await page.locator('.langsel').count(),1);
 assert.equal(await page.locator('main h1').count(),1);
 assert.ok(await page.locator('a[href*="inonda.homes"]').count()>0);
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth-innerWidth);
 assert.ok(overflow<=4,locale+' '+path+' horizontal overflow: '+overflow);
 assert.deepEqual(errors,[],locale+' '+path+' JavaScript errors');
 return page;
}
try{
 for(const lang of ['el','en','ru','uk','he','ro']){
  const page=await openPage(lang,'',lang==='he'?{width:390,height:844}:{width:1440,height:960});
  assert.equal(await page.locator('.inonda-wood-card').count(),10,lang+' categories');
  for(const href of ['doors-frames','timber-windows-shutters','kitchen-utility-cabinets','wardrobes-storage','shelving-fitted-furniture','wall-panelling-trim','stairs-balustrades','outdoor-carpentry','repairs-alterations','custom-projects']){
   assert.ok(await page.locator('a[href*="/carpentry/'+href+'/"]').count()>=1,lang+':'+href);
  }
  if(lang==='en')await page.screenshot({path:'carpentry-screenshots/desktop-en-overview.png',fullPage:true});
  if(lang==='he')await page.screenshot({path:'carpentry-screenshots/mobile-he-overview.png',fullPage:true});
  await page.close();
 }
 for(const [lang,slug,size,shot] of [
  ['en','doors-frames/',{width:1440,height:960},'desktop-en-doors.png'],
  ['en','kitchen-utility-cabinets/',{width:390,height:844},'mobile-en-kitchen.png'],
  ['el','repairs-alterations/',{width:390,height:844},'mobile-el-repairs.png'],
  ['he','stairs-balustrades/',{width:390,height:844},'mobile-he-stairs.png']
 ]){
  const page=await openPage(lang,slug,size);
  assert.ok(await page.locator('details').count()>=4,lang+slug+' FAQ');
  assert.ok(await page.locator('.inonda-wood-list li').count()>=5,lang+slug+' work scope');
  assert.ok((await page.locator('a[href*="wa.me/35794091616?text="]').count())>0,lang+slug+' quote action');
  assert.ok((await page.locator('a[href*="inonda.homes/?lang='+lang+'"]').count())>0,lang+slug+' estimator action');
  await page.screenshot({path:'carpentry-screenshots/'+shot,fullPage:true});
  await page.close();
 }
 console.log('PASS: 6 languages, 10 category links, desktop/mobile/RTL, FAQ, contact and responsive layout.');
}finally{await browser.close();}
