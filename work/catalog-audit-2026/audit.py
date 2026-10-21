from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from collections import Counter,defaultdict
import re,json,hashlib
import pdfplumber
ROOT=Path.cwd(); OUT=ROOT/'work/catalog-audit-2026'
SOURCE=Path(r'\\Serverbl\dati\Documenti Comuni\_____ BICYCLE LINE\CATALOGHI\TEAM\CICLISMO_25\2026\per invio WeTransfer - alta risoluzione - HR\BL-CC_Custom Team 2026_EN_H-Res.pdf')
class N:
    def __init__(self,tag='',attrs=(),parent=None,line=0): self.tag=tag;self.a=dict(attrs);self.p=parent;self.line=line;self.c=[]
    def text(self): return re.sub(r'\s+',' ',''.join(c if isinstance(c,str) else c.text()+' ' for c in self.c)).strip()
    def findall(self,tag=None,cls=None):
        result=[]
        for c in self.c:
            if isinstance(c,N):
                if (not tag or c.tag==tag) and (not cls or cls in c.a.get('class','').split()):result.append(c)
                result+=c.findall(tag,cls)
        return result
    def find(self,tag=None,cls=None): return next(iter(self.findall(tag,cls)),None)
class P(HTMLParser):
    def __init__(self): super().__init__();self.root=N();self.cur=self.root
    def handle_starttag(self,t,a):
        n=N(t,a,self.cur,self.getpos()[0]);self.cur.c.append(n)
        if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.cur=n
    def handle_startendtag(self,t,a): self.handle_starttag(t,a);self.handle_endtag(t)
    def handle_endtag(self,t):
        n=self.cur
        while n.p and n.tag!=t:n=n.p
        if n.tag==t:self.cur=n.p
    def handle_data(self,d):self.cur.c.append(d)
def save(name,x): (OUT/name).write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
def langof(file):return {'INGLESE':'en','FRANCESE':'fr','TEDESCO':'de','SPAGNOLO':'es'}.get(file.parts[0],'it')
files=sorted(ROOT.rglob('*.html')); trees={}; pages=[];issues=[]
for f in files:
    if 'work' in f.relative_to(ROOT).parts:continue
    rel=f.relative_to(ROOT);txt=f.read_text(encoding='utf-8-sig');p=P();p.feed(txt);tree=p.root;trees[str(rel)]=tree
for rel,tree in trees.items():
    f=ROOT/rel;lang=langof(Path(rel)); code=re.search(r'W\d{4}',f.name)
    for n in tree.findall():
        for key in ['src','href']:
            v=n.a.get(key)
            if not v:continue
            u=urlsplit(v)
            if u.scheme or u.netloc:continue
            target=(f.parent/unquote(u.path)).resolve() if u.path else f
            if not target.exists():issues.append(dict(type='missing-file',file=rel,line=n.line,value=v))
            elif key=='href' and u.fragment and target.suffix=='.html':
                target_tree=trees.get(str(target.relative_to(ROOT))) if target.is_relative_to(ROOT) else None
                if target_tree and not any(k.a.get('id')==unquote(u.fragment) or k.a.get('name')==unquote(u.fragment) for k in target_tree.findall()):
                    issues.append(dict(type='missing-anchor',file=rel,line=n.line,value=v))
    if not code:continue
    code=code[0];side=tree.find(cls='sidebar')
    if not side:issues.append(dict(type='missing-sidebar',file=rel));continue
    blocks=[]
    for a in side.findall(cls='acc-item'):
        head=a.find(cls='acc-title');body=a.find(cls='acc-body')
        if head and body:blocks.append(dict(title=head.text(),body=body.text(),line=head.line,items=[li.text() for li in body.findall(tag='li')]))
    metrics=[]
    for m in side.findall(cls='metric'):
        label=m.find(cls='label'); bars=m.find(cls='bars')
        if label and bars:metrics.append((label.text(),sum('on' in s.a.get('class','').split() for s in bars.findall(tag='span'))))
    gallery=tree.find(cls='gallery');dropdown=tree.find(cls='lang-dropdown')
    links=[]
    if dropdown:
        for a in dropdown.findall(tag='a'):
            target=(f.parent/unquote(urlsplit(a.a['href']).path)).resolve()
            targetcode=re.search(r'W\d{4}',target.name)
            l=langof(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else '?'
            links.append(dict(lang=l,href=a.a['href'],line=a.line))
            if not targetcode or targetcode[0]!=code:issues.append(dict(type='wrong-language-product',file=rel,line=a.line,value=a.a['href'],code=code))
        if sorted(x['lang'] for x in links)!=['de','en','es','fr','it']:issues.append(dict(type='language-coverage',file=rel,links=links))
    else:issues.append(dict(type='missing-language-menu',file=rel))
    h=side.find(tag='h1');ey=side.find(cls='eyebrow');sizes=side.find(cls='sizes')
    if h and code not in h.text():issues.append(dict(type='wrong-title-code',file=rel,line=h.line,title=h.text(),code=code))
    page=dict(file=rel,lang=lang,code=code,title=h.text() if h else '',eyebrow=ey.text() if ey else '',blocks=blocks,metrics=metrics,sizes=sizes.text() if sizes else '',gallery=[n.a.get('src','') for n in gallery.findall(tag='img')] if gallery else [],links=links,line=side.line)
    pages.append(page)
save('pages.json',pages);save('link-issues.json',issues)
refs={}; pdfpages=[]
with pdfplumber.open(SOURCE) as pdf:
    for i,p in enumerate(pdf.pages):
        text=p.extract_text() or '';pdfpages.append(text)
        if i<8:continue
        hits=[h for h in p.search(r'\bW\d{4}\b') if h['x0']<120 and 30<h['top']<790]
        # Only the model heading starts a product area.
        unique={}
        for h in hits:unique.setdefault(h['text'],h)
        hs=sorted(unique.values(),key=lambda h:h['top'])
        for j,h in enumerate(hs):
            end=next((k['top']-3 for k in hs[j+1:] if k['top']>h['top']+35),p.height-20)
            segment=p.crop((0,max(0,h['top']-2),p.width,end))
            entry=dict(page=i+1,top=h['top'],bottom=end,text=segment.extract_text(x_tolerance=2) or '',right=segment.crop((365,segment.bbox[1],p.width,end)).extract_text() or '')
            refs.setdefault(h['text'],[]).append(entry)
save('references.json',refs);save('pdf-pages.json',pdfpages)
# Cross-language technical token parity, without judging prose equivalence mechanically.
facts={}
patterns={'pad':r'(?i)road\s*performance\s*force|ghost\s*air\s*gel|x[\s-]*stra|core\s*evo|doge|naked|kid\s*pad', 'brand':r'(?i)mititech|brugnoli|explosive|thunderbike|cam\s*lock|ykk|skinlife|gore|windstopper|dtf|upf\s*50\+|event|bluesign|oeko[\s-]*tex', 'number':r'(?<![A-Za-z])(?:[+]?-?\d+(?:[.,]\d+)?)\s*(?:°\s*C|%|g\s*/\s*m[²2]|mm|cm|hours?|ore|heures?|stunden|horas)'}
for p in pages:
    text=' '.join(x['body'] for x in p['blocks'])
    facts[p['file']]={k:sorted(set(re.sub(r'\s+',' ',m.lower()) for m in re.findall(v,text))) for k,v in patterns.items()}
save('facts.json',facts)
print('HTML',len(trees),'PRODUCT PAGES',len(pages),'CODES',len(set(p['code'] for p in pages)),'LINK ISSUES',len(issues))
print('Issue types:',dict(Counter(x['type'] for x in issues)))
print('Product pages per language:',dict(Counter(x['lang'] for x in pages)))
print('PDF reference codes:',len(refs),'Missing references:',sorted(set(p['code'] for p in pages)-set(refs)))
print('PDF entries:',{k:[e['page'] for e in v] for k,v in refs.items()})


