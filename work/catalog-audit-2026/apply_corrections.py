from pathlib import Path
from html.parser import HTMLParser
from html import escape,unescape
from urllib.parse import urlsplit,unquote
import re,json,os,hashlib
from correction_content import *
ROOT=Path.cwd();D=ROOT/'work/catalog-audit-2026'
META=json.loads((D/'pages.json').read_text(encoding='utf8'))
RATINGS=json.loads((D/'ratings.json').read_text(encoding='utf8'))['ratings']
class E:
 def __init__(self,tag='',attrs=(),parent=None,start=0,inner=0):self.tag=tag;self.a=dict(attrs);self.parent=parent;self.start=start;self.inner=inner;self.close=inner;self.end=inner;self.children=[]
 def all(self,tag=None,cls=None):
  found=[]
  for e in self.children:
   if (not tag or e.tag==tag) and (not cls or cls in e.a.get('class','').split()):found.append(e)
   found+=e.all(tag,cls)
  return found
 def one(self,tag=None,cls=None):return next(iter(self.all(tag,cls)),None)
class DOM(HTMLParser):
 def __init__(self,text):
  super().__init__();self.text=text;self.lines=[0];self.lines += [m.end() for m in re.finditer('\n',text)];self.root=E();self.cur=self.root;self.feed(text)
 def pos(self):l,c=self.getpos();return self.lines[l-1]+c
 def handle_starttag(self,t,a):
  start=self.pos();e=E(t,a,self.cur,start,start+len(self.get_starttag_text()));self.cur.children.append(e)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.cur=e
  else:e.end=e.inner
 def handle_startendtag(self,t,a):self.handle_starttag(t,a);self.handle_endtag(t)
 def handle_endtag(self,t):
  n=self.cur
  while n.parent and n.tag!=t:n=n.parent
  if n.tag==t:n.close=self.pos();n.end=self.text.find('>',n.close)+1;self.cur=n.parent

def plain(t):return re.sub(r'\s+',' ',unescape(re.sub(r'<[^>]*>',' ',t))).strip()
def ntext(t,e):return plain(t[e.inner:e.close])
def nodes(t,cls):return DOM(t).root.all(cls=cls)
ROLES={'desc':tr('Descrizione|Description|Beschreibung|Description|Descripción'),'features':tr('CARATTERISTICHE PRINCIPALI|MAIN FEATURES|HAUPTMERKMALE|CARACTÉRISTIQUES PRINCIPALES|CARACTERÍSTICAS PRINCIPALES'),'options':tr('OPZIONI|OPTIONS|OPTIONEN|OPTIONS|OPCIONES'),'technical':tr('Caratteristiche tecniche|Technical characteristics|Technische Eigenschaften|Caractéristiques techniques|Características técnicas'),'temp':tr('Temperatura|Temperature|Temperatur|Température|Temperatura')}
def findblock(t,role,lang):
 for b in nodes(t,'acc-item'):
  h=b.one(cls='acc-title')
  if h and ntext(t,h).casefold()==ROLES[role][lang].casefold():return b
 return None

def body(t,role,lang,html,add=False):
 b=findblock(t,role,lang)
 content='<div class="description">'+html+'</div>'
 if b:
  target=b.one(cls='acc-body');assert target
  return t[:target.inner]+content+t[target.close:]
 assert add,(role,lang)
 acc=next(a for a in nodes(t,'accordion') if a.parent and a.parent.tag=='aside')
 new='\n        <div class="acc-item"><div class="acc-head"><div class="acc-title">'+escape(ROLES[role][lang])+'</div><div class="acc-icon">+</div></div><div class="acc-body">'+content+'</div></div>\n'
 return t[:acc.close]+new+t[acc.close:]
def list_html(items):return '<ul style="list-style:none;padding:0;margin:0">'+''.join('<li style="margin-bottom:8px">• '+escape(x)+'</li>' for s in items for x in s.split(';'))+'</ul>'
def getitems(t,role,lang):
 b=findblock(t,role,lang);assert b,(role,lang)
 return [ntext(t,li).lstrip('• ').strip() for li in b.all(tag='li')]
def pp(code,lang):return next(ROOT/p['file'] for p in META if p['code']==code and p['lang']==lang and not ('RAGAZZI EN' in p['file'] and (code.startswith('W66') or code in ['W0274','W2632'])))
changed=set();details=[]
def read(f):return f.read_bytes().decode('utf8')
def write(f,t):
 if read(f)!=t:f.write_bytes(t.encode('utf8'));changed.add(str(f.relative_to(ROOT)))

def update_metrics(t,code,lang):
 side=DOM(t).root.one(cls='sidebar');metrics=side.all(cls='metric')
 values=RATINGS[code]
 if metrics:
  for m,n in reversed(list(zip(metrics,values))):
   bars=m.one(cls='bars');assert bars
   new=''.join('<span'+(' class="on"' if i<n else '')+'></span>' for i in range(5))
   t=t[:bars.inner]+new+t[bars.close:]
  return t
 b=findblock(t,'temp',lang);assert b,(code,lang)
 labels={'it':['Vestibilità','Traspirabilità','Elasticità'],'en':['Fit','Breathability','Elasticity'],'de':['Passform','Atmungsaktivität','Elastizität'],'fr':['Coupe','Respirabilité','Élasticité'],'es':['Ajuste','Transpirabilidad','Elasticidad']}[lang]
 temp=ntext(t,b.one(cls='acc-body'));new='<div class="metric-grid">'
 for label,n in zip(labels,values):
  new+='<div class="metric"><div class="label">'+label+'</div><div class="bars">'+''.join('<span'+(' class="on"' if i<n else '')+'></span>' for i in range(5))+'</div></div>'
 new+='</div><div class="temp"><div class="temp-head"><div class="temp-title">'+ROLES['temp'][lang]+'</div><div class="temp-chip">'+escape(temp)+'</div></div></div>'
 a=b.one(cls='acc-body');t=t[:a.inner]+new+t[a.close:]
 b=findblock(t,'temp',lang);h=b.one(cls='acc-title');return t[:h.inner]+ROLES['technical'][lang]+t[h.close:]

NEW_CODES=['W6004','W6038','W6040','W6045','W6046','W6047','W6308','W6526','W6529','W6534','W6535','W6541']
TEMPS={'W6515':(15,30),'W6047':(18,35),**{c:(15,30) for c in ['W7200','W7201','W7202','W7203','W7204','W7205']}}
for code,(low,high) in TEMPS.items():
 for lang in LANGS:
  f=pp(code,lang);t=read(f)
  pattern=r'(<div class="temp-chip">)[\s\S]*?(</div>)'
  if re.search(pattern,t):
   t=re.sub(pattern,lambda m:m[1]+f'+{low} / +{high} °C'+m[2],t)
   t=re.sub(r'(<div class="temp-range">)[\s\S]*?(</div>)',lambda m:m[1]+f'+{low}°C<span style="margin:0 8px;">—</span>+{high}°C'+m[2],t)
  else:t=body(t,'temp',lang,escape(f'+{low} / +{high} °C'))
  write(f,t)
for code in ['W6301','W6512']+NEW_CODES:
 for lang in LANGS:
  f=pp(code,lang);write(f,update_metrics(read(f),code,lang))
for code,descs in DESC.items():
 for lang in LANGS:
  f=pp(code,lang);write(f,body(read(f),'desc',lang,escape(descs[lang])))
for lang in LANGS:
 # Echelon: updated printing material in options, preserving pad and fabric choices.
 f=pp('W6005',lang);t=read(f);items=getitems(t,'options',lang);items[0]=DTF[lang]
 t=body(t,'options',lang,list_html(items));write(f,t)
 # Echelon Air: replace obsolete construction details and 2026/2027 options.
 f=pp('W6028',lang);t=read(f)
 t=body(t,'features',lang,list_html([x[lang] for x in AIR_FEATURES]))
 items=getitems(t,'options',lang);items[:2]=[DTF[lang],COLORS[lang]]
 t=body(t,'options',lang,list_html(items));write(f,t)
 # CYCLE-01: printable front and updated colours; retain the chamois section.
 f=pp('W6036',lang);t=read(f);items=getitems(t,'features',lang);items[0]=PRINT_FRONT[lang]
 t=body(t,'features',lang,list_html(items));items=getitems(t,'options',lang);items[0]=COLORS[lang]
 t=body(t,'options',lang,list_html(items));write(f,t)
 # APEX women: add anatomical fit and options from the current catalog.
 for code in ['W6514','W6515']:
  f=pp(code,lang);t=read(f);items=getitems(t,'features',lang);items.insert(0,WOMEN_FIT[lang])
  if code=='W6515':
   for i,item in enumerate(items):
    if 'X-Stra' in item:
     additions=tr('Fondello X-Stra specifico donna|Women-specific X-Stra pad|X-Stra-Damensitzpolster|Peau X-Stra spécifique femme|Badana X-Stra específica para mujer')
     item=re.sub(r'(?i)(?:Fondello|Peau|Badana) X-Stra|X-Stra (?:chamois|Sitzpolster)',additions[lang],item,count=1);items[i]=item
  t=body(t,'features',lang,list_html(items))
  if code=='W6514':t=body(t,'options',lang,list_html(JERSEY_OPTIONS[lang].split(';')),add=True)
  else:
   pads=tr('Fondello Road Performance Force, configurazione donna.;Fondello Ghost Air Gel, configurazione donna.;Fondello Core Evo, configurazione donna.|Road Performance Force pad, women-specific configuration.;Ghost Air Gel pad, women-specific configuration.;Core Evo pad, women-specific configuration.|Road Performance Force-Sitzpolster, Damenausführung.;Ghost Air Gel-Sitzpolster, Damenausführung.;Core Evo-Sitzpolster, Damenausführung.|Peau Road Performance Force, configuration femme.;Peau Ghost Air Gel, configuration femme.;Peau Core Evo, configuration femme.|Badana Road Performance Force, configuración femenina.;Badana Ghost Air Gel, configuración femenina.;Badana Core Evo, configuración femenina.')
   t=body(t,'options',lang,list_html([NAVY[lang],pads[lang]]))
  write(f,t)
 # Restore non-pad options omitted from the chrono skinsuit and tights.
 f=pp('W6012',lang);write(f,body(read(f),'options',lang,list_html([LOGO_WHITE[lang],NAVY[lang]]),add=True))
 f=pp('W6518',lang);t=read(f);items=getitems(t,'options',lang);items.insert(0,LOGO_WHITE[lang]);write(f,body(t,'options',lang,list_html(items)))
# Correct a sports-name typo inherited from the PDF; images and seat pad establish cycling use.
for lang,old,new in [('en','Winter running tights','Winter cycling bib tights'),('fr','Collant de running d’hiver','Collant de cyclisme d’hiver'),('de','Winter-Lauftights','Winter-Radträgerhose'),('es','Mallas largas de running de invierno','Mallas largas de ciclismo de invierno con tirantes')]:
 f=pp('W6009',lang);t=read(f);assert old in t;write(f,t.replace(old,new,1))
# Spanish accessory size labels.
for code in ['W0274','W2632','W6600','W6601','W6602','W6603']:
 f=pp(code,'es');write(f,read(f).replace('Größe:','Talla:').replace('EINHEITSGRÖSSE','TALLA ÚNICA'))
# Repair unused legacy copies from the canonical English accessory pages.
for p in META:
 if p['lang']=='en' and 'RAGAZZI EN' in p['file'] and (p['code'].startswith('W66') or p['code'] in ['W0274','W2632']):
  dest=ROOT/p['file'];source=pp(p['code'],'en');t=read(source)
  def rebase(m):
   u=urlsplit(m[2])
   if u.scheme or u.netloc or not u.path:return m[0]
   target=(source.parent/unquote(u.path)).resolve();href=os.path.relpath(target,dest.parent).replace('\\','/')
   return m[1]+'"'+href+('#'+u.fragment if u.fragment else '')+'"'
  t=re.sub(r'((?:href|src)\s*=\s*)"([^"]+)"',rebase,t);write(dest,t)
# Global safe interaction and contact destinations. Keep the existing navigation and form scripts.
all_html=[f for f in ROOT.rglob('*.html') if 'work' not in f.relative_to(ROOT).parts]
for f in all_html:
 t=read(f);rel=f.relative_to(ROOT);lang={'INGLESE':'en','FRANCESE':'fr','TEDESCO':'de','SPAGNOLO':'es'}.get(rel.parts[0],'it')
 langroot=ROOT/rel.parts[0] if lang!='it' else ROOT;home=langroot/'index.html'
 def contact(m):
  value=m[1];u=urlsplit(value)
  if u.scheme or u.netloc or u.fragment not in ['contatti','kontakt']:return m[0]
  target=(f.parent/unquote(u.path)).resolve() if u.path else f
  if target.exists() and re.search(r'(?:id|name)=["\']'+re.escape(u.fragment)+r'["\']',read(target)):return m[0]
  dest=os.path.relpath(home,f.parent).replace('\\','/')+'#contatti'
  return 'href="'+dest+'"'
 t=re.sub(r'href="([^"]+)"',contact,t)
 t=re.sub(r"(const accIcon = this\.querySelector\('\.acc-icon'\);)(?!\s*if \(!accIcon)",r'\1\n      if (!accIcon || !accBody) return;',t)
 css=os.path.relpath(ROOT/'catalog-fixes.css',f.parent).replace('\\','/')
 if 'catalog-fixes.css' not in t:t=t.replace('</head>',f'  <link rel="stylesheet" href="{css}">\n</head>',1)
 write(f,t)
(D/'corrected-files.json').write_text(json.dumps(sorted(changed),ensure_ascii=False,indent=2),encoding='utf8')
print('Updated HTML files:',len(changed))
