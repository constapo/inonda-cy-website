/* Local presentation controls. No network calls, data collection or messaging. */
(function(){'use strict';
function init(){
var tabs=Array.from(document.querySelectorAll('[data-living-tab]'));
function select(tab,focus){
tabs.forEach(function(t){var on=t===tab;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;var p=document.getElementById(t.getAttribute('aria-controls'));if(p)p.hidden=!on;});
if(focus)tab.focus();
}
tabs.forEach(function(tab,index){
tab.addEventListener('click',function(){select(tab,false);});
tab.addEventListener('keydown',function(event){var next=null;if(event.key==='ArrowDown'||event.key==='ArrowRight')next=(index+1)%tabs.length;if(event.key==='ArrowUp'||event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;if(next!==null){event.preventDefault();select(tabs[next],true);}});
});
var toggle=document.getElementById('menuToggle'),panel=document.getElementById('mobilePanel');
document.addEventListener('keydown',function(event){if(event.key==='Escape'&&toggle&&panel&&panel.classList.contains('open')){panel.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.focus();}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
