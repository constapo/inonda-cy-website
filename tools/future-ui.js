/* INONDA architectural UI: local, progressive enhancement; no tracking or pricing logic. */
(()=>{'use strict';
const body=document.body,site=body.dataset.inondaSite;
const hero=document.querySelector(site==='homes'?'.masthead':'main>.hero');
if(!hero||document.querySelector('.future-stage'))return;
const copy={
 en:['Property perspective','Illustrative architectural view','Model','Layers','Plan','Explore the building as a whole.','Separate the architectural layers.','Switch to a plan perspective.','Plan your property','Property','Services','Review','Explore services','Maintenance','Repairs','Renovation','Explore this service'],
 el:['Προοπτική ακινήτου','Ενδεικτική αρχιτεκτονική απεικόνιση','Μοντέλο','Επίπεδα','Κάτοψη','Δείτε το κτίριο ως σύνολο.','Διαχωρίστε τα αρχιτεκτονικά επίπεδα.','Επιλέξτε προοπτική κάτοψης.','Σχεδιάστε το ακίνητό σας','Ακίνητο','Υπηρεσίες','Επισκόπηση','Εξερευνήστε υπηρεσίες','Συντήρηση','Επισκευές','Ανακαίνιση','Δείτε την υπηρεσία'],
 ru:['Объект в перспективе','Условная архитектурная иллюстрация','Модель','Уровни','План','Рассмотрите здание целиком.','Разделите архитектурные уровни.','Переключитесь на вид плана.','План вашей недвижимости','Объект','Услуги','Обзор','Изучите услуги','Обслуживание','Ремонт','Обновление','Подробнее об услуге'],
 uk:['Об’єкт у перспективі','Умовна архітектурна ілюстрація','Модель','Рівні','План','Розгляньте будівлю цілком.','Розділіть архітектурні рівні.','Перейдіть до вигляду плану.','План вашої нерухомості','Об’єкт','Послуги','Огляд','Дослідіть послуги','Обслуговування','Ремонт','Оновлення','Докладніше про послугу'],
 he:['מבט על הנכס','המחשה אדריכלית לדוגמה','מודל','שכבות','תוכנית','צפו במבנה השלם.','הפרידו בין השכבות האדריכליות.','עברו למבט תוכנית.','תכננו את הנכס','הנכס','שירותים','סקירה','גלו את השירותים','תחזוקה','תיקונים','שיפוץ','פרטים על השירות'],
 ro:['Perspectiva proprietății','Ilustrație arhitecturală orientativă','Model','Niveluri','Plan','Explorează clădirea în ansamblu.','Separă nivelurile arhitecturale.','Treci la perspectiva de plan.','Planifică proprietatea','Proprietate','Servicii','Revizuire','Explorează serviciile','Întreținere','Reparații','Renovare','Vezi serviciul']};
const lang=()=>copy[document.documentElement.lang]?document.documentElement.lang:'en';
const svg=`<svg viewBox="0 0 560 420" aria-hidden="true" focusable="false"><defs><linearGradient id="future-wall" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#2bb8e5" stop-opacity=".16"/><stop offset="1" stop-color="#0077b6" stop-opacity=".02"/></linearGradient></defs><g fill="none" stroke="#4696b2" stroke-width=".6" opacity=".42"><path d="M35 300 280 160 525 300 280 440Z M65 315 310 175 M100 335 345 195 M135 355 380 215 M170 375 415 235 M205 395 450 255 M240 415 485 275 M70 280 315 420 M105 260 350 400 M140 240 385 380 M175 220 420 360 M210 200 455 340 M245 180 490 320"/></g><g class="model-floor" data-layer="roof"><path d="M118 162 278 70 446 166 286 258Z"/><path d="M118 162v18l168 96 160-92v-18M286 258v18"/><path d="M166 160 278 96 398 165 286 230Z" stroke-dasharray="4 5" fill="none"/><path d="M278 70v26M446 166l-48-1M118 162l48-2M286 258v-28" fill="none"/></g><g class="model-floor" data-layer="upper"><path d="M137 198 278 117 425 202 284 283Z"/><path d="M137 198v64l147 85 141-81v-64M284 283v64" fill="url(#future-wall)"/><path d="M160 229v26l39 23v-26Z M210 258v26l42 24v-26Z M307 284v29l39-23v-29Z M361 253v29l40-23v-29Z" fill="#3fd5ff30"/><path d="M278 117v63l147 86M137 262l141-82 6 167" stroke-dasharray="4 5" fill="none"/></g><g class="model-floor active" data-layer="ground"><path d="M137 267 278 186 425 271 284 352Z"/><path d="M137 267v53l147 85 141-81v-53M284 352v53" fill="url(#future-wall)"/><path d="M160 297v23l39 23v-23Z M210 326v23l42 24v-23Z M307 352v26l39-23v-26Z M361 321v26l40-23v-26Z" fill="#3fd5ff30"/><path d="M278 186v52l147 86M137 320l141-82 6 167" stroke-dasharray="4 5" fill="none"/></g><g fill="none" stroke="#9cecff" stroke-width=".8" opacity=".7"><path d="M104 180 68 199v121l36 21 M460 190l32 18v118l-32 18M68 255h30M492 264h-30"/><circle cx="68" cy="255" r="3"/><circle cx="492" cy="264" r="3"/><path d="M228 38h105M280 20v36"/></g></svg>`;
const stage=document.createElement('section');stage.className='future-stage';stage.dataset.noI18n='';stage.innerHTML=`<div class="future-stage-head"><span data-future-label="0"></span><span>INONDA / ${site==='site'?'01':site==='org'?'02':'03'}</span></div><div class="future-model" data-view="model">${svg}</div><div class="future-stage-controls" role="group"><button type="button" data-view="model" aria-pressed="true"></button><button type="button" data-view="layers" aria-pressed="false"></button><button type="button" data-view="plan" aria-pressed="false"></button></div><p class="future-stage-caption"><span data-future-label="1"></span> · <span data-future-state></span></p>`;
hero.append(stage);
let mode='model';
stage.querySelectorAll('button').forEach((button,index)=>button.addEventListener('click',()=>{
 mode=button.dataset.view;stage.querySelector('.future-model').dataset.view=mode;
 stage.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 stage.querySelectorAll('.model-floor').forEach((floor,i)=>{floor.classList.toggle('active',mode==='layers'||i===index);floor.style.transform=mode==='layers'?`translateY(${(i-2)*28}px)`:'';});
 refresh();
}));
let workflow;
if(site==='homes'){
 workflow=document.createElement('nav');workflow.className='future-workflow';workflow.dataset.noI18n='';workflow.innerHTML='<a href="#property"><span>01</span><b></b></a><a href="#services"><span>02</span><b></b></a><a href="#review"><span>03</span><b></b></a>';
 document.querySelector('.estimator-frame')?.prepend(workflow);
}
if(site==='org'){
 stage.querySelector('.future-model').insertAdjacentHTML('beforeend','<img class="future-material" alt="" decoding="async"><a class="future-service-link"></a>');
 const modes=[['maintenance-plans/','maintenance.webp'],['plumbing-services/','plumbing.webp'],['home-renovation/','kitchen.webp']];
 stage.querySelectorAll('button').forEach((button,i)=>button.addEventListener('click',()=>{
   const image=stage.querySelector('.future-material');image.src='https://www.inonda.org/assets/img/'+modes[i][1];
   const link=stage.querySelector('.future-service-link');link.href=modes[i][0];stage.dataset.service=String(i);refresh();
 }));
 stage.dataset.service='0';stage.querySelector('.future-material').src='https://www.inonda.org/assets/img/maintenance.webp';stage.querySelector('.future-service-link').href=modes[0][0];
}
function refresh(){
 const c=copy[lang()];stage.setAttribute('aria-label',c[site==='org'?12:0]);stage.querySelector('[data-future-label="0"]').textContent=c[site==='org'?12:0];stage.querySelector('[data-future-label="1"]').textContent=c[1];
 stage.querySelector('.future-stage-controls').setAttribute('aria-label',c[0]);
 stage.querySelectorAll('button').forEach((b,i)=>b.textContent=c[(site==='org'?13:2)+i]);
 stage.querySelector('[data-future-state]').textContent=c[5+['model','layers','plan'].indexOf(mode)];
 if(workflow){workflow.setAttribute('aria-label',c[8]);workflow.querySelectorAll('b').forEach((b,i)=>b.textContent=c[9+i]);}
 if(site==='org'){stage.querySelector('.future-service-link').textContent=c[16]+' ↗';stage.querySelector('[data-future-label="1"]').textContent=c[13+Number(stage.dataset.service)];stage.querySelector('[data-future-state]').textContent='INONDA LTD';}
}
refresh();new MutationObserver(refresh).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});document.addEventListener('inonda:language',refresh);
})();
