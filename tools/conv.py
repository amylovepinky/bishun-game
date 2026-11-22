import json,glob,os,sys
src=sys.argv[1]; out=sys.argv[2]
R=lambda v: str(round(v/4))
def path(ol):
    s=[]
    for p in ol:
        t=p['type']
        if t in('M','L'): s.append(t+R(p['x'])+' '+R(p['y']))
        elif t=='Q': s.append('Q'+R(p['begin']['x'])+' '+R(p['begin']['y'])+' '+R(p['end']['x'])+' '+R(p['end']['y']))
        elif t=='C': s.append('C'+' '.join(R(p[k][a]) for k in('begin','mid','end') for a in 'xy'))
    return ''.join(s)+'Z'
N=32; chunks=[{} for _ in range(N)]; allc=[]
for f in glob.glob(src+'/*.json'):
    cp=int(os.path.basename(f)[:-5],16); ch=chr(cp)
    d=json.load(open(f))
    strokes=[]
    for st in d:
        tr=[]
        for t in st['track']: tr+=[round(t["x"]/4),round(t["y"]/4)]
        strokes.append([path(st['outline']),tr])
    chunks[cp%N][ch]=strokes; allc.append(ch)
tot=0
for i,c in enumerate(chunks):
    s=json.dumps(c,ensure_ascii=False,separators=(',',':'))
    open(f'{out}/s{i}.json','w').write(s); tot+=len(s.encode())
open(out+'/../all.json','w').write(json.dumps(chunks[0] and {k:v for c in chunks for k,v in c.items()},ensure_ascii=False,separators=(',',':')))
print(len(allc), tot/1e6,'MB')
