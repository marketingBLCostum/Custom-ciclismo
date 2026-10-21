from pathlib import Path
import subprocess,re
root=Path.cwd();git=r'C:\Users\Libia\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\git\cmd\git.exe'
result=subprocess.run([git,'-c','core.safecrlf=false','diff','--check'],capture_output=True,text=True,encoding='utf8')
for name,line in re.findall(r'^(.+\.html):(\d+): trailing whitespace\.$',result.stdout,re.M):
 f=root/name;parts=f.read_bytes().decode('utf8').splitlines(keepends=True);i=int(line)-1
 assert parts[i].strip()=='', (name,line,parts[i])
 parts[i]='\r\n' if parts[i].endswith('\r\n') else '\n';f.write_bytes(''.join(parts).encode('utf8'))
print('Removed introduced whitespace-only lines.')
