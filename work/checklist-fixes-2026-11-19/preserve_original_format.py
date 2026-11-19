from pathlib import Path
from difflib import SequenceMatcher
import json,re,zipfile

ROOT=Path.cwd();OUT=ROOT/'work/checklist-fixes-2026-11-19'
events=json.loads((OUT/'changes.json').read_text(encoding='utf-8'))

def normalized_with_offsets(raw):
    chars=[];offsets=[];i=0
    while i<len(raw):
        offsets.append(i)
        if raw[i:i+2]=='\r\n':chars.append('\n');i+=2
        else:chars.append(raw[i]);i+=1
    offsets.append(len(raw));return ''.join(chars),offsets

with zipfile.ZipFile(OUT/'before-html.zip') as backup:
    for event in events:
        rel=event['file'];original_bytes=backup.read(rel)
        original=original_bytes.decode('utf-8-sig')
        current=(ROOT/rel).read_bytes().decode('utf-8-sig').replace('\r\n','\n')
        if event['code']=='W6012':
            assert current.count('        \n</div>')==1,rel
            current=current.replace('        \n</div>','\n</div>')
        old,offsets=normalized_with_offsets(original)
        crlf=original.count('\r\n');lf=original.count('\n')-crlf
        ending='\r\n' if crlf>lf else '\n'
        result=[]
        for tag,a,b,c,d in SequenceMatcher(None,old,current).get_opcodes():
            if tag=='equal':result.append(original[offsets[a]:offsets[b]])
            elif tag in {'replace','insert'}:result.append(current[c:d].replace('\n',ending))
        text=''.join(result)
        assert text.replace('\r\n','\n')==current,rel
        scripts=lambda s:re.findall(r'<script\b[^>]*>[\s\S]*?</script>',s,re.I)
        styles=lambda s:re.findall(r'<style\b[^>]*>[\s\S]*?</style>',s,re.I)
        assert scripts(original)==scripts(text),rel+' script bytes differ'
        assert styles(original)==styles(text),rel+' style bytes differ'
        prefix=b'\xef\xbb\xbf' if original_bytes.startswith(b'\xef\xbb\xbf') else b''
        (ROOT/rel).write_bytes(prefix+text.encode('utf-8'))
print('Original script/style blocks and unchanged-region formatting preserved in',len(events),'HTML files.')
