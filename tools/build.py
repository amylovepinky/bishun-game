import json,glob,re,sys
G=sys.argv[1]
src=open(G+'/src.html').read()
d={}
for f in glob.glob(G+'/d/*.json'): d.update(json.load(open(f)))
js=src[src.index('const BASIC'):src.index('const tint')]
need=set(re.findall(r"'(\S)'",js))|set('永')
lv=src[src.index('const DEFAULT_LEVELS'):]
lv=lv[:lv.index('\n')]
need|=set(''.join(re.findall(r"chars:'([^']*)'",lv)))
need={c for c in need if c in d}
data={c:d[c] for c in sorted(need)}
out=src.replace('/*DATA*/{}',json.dumps(data,ensure_ascii=False,separators=(',',':')))
open(G+'/index.html','w').write(out)
print(len(data),'chars inline', len(out.encode())//1024,'KB')
