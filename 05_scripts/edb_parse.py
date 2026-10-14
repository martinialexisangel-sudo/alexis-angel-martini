import json,sys,re,glob,csv,os
"""Parse EDB quick-search result pages (Parallel web_fetch JSON dumps) into rows."""
rows={};pages={}
for f in sorted(glob.glob(sys.argv[1]+'/*.json')):
    d=json.load(open(f))
    for r in d.get('results',[]):
        url=r['url']; m=re.search(r'page=(\d+)',url)
        if not m or 'search/quick/do' not in url: continue
        p=int(m.group(1)); fc=r.get('full_content') or ''
        i=fc.find('|ID |ICVR'); 
        if i<0: continue
        j=fc.find('\nx\n',i); seg=fc[i:j if j>0 else None]
        parts=re.split(r'\n\|(?=\d+ \|)',seg)[1:]
        prow=[]
        for pt in parts:
            cells=[c.strip().replace('\n',' ; ') for c in pt.split(' |')]
            # cells: id, icvr, bib, pertinence, conservation, date, text, action
            idd=cells[0]; icvr=cells[1].replace('\\','')
            mm=re.search(r'epigraph/(\d+)',pt)
            # text is cell before action (last with link)
            txt=cells[6] if len(cells)>6 else ''
            rec=dict(page=p,edb=idd,icvr=icvr,bib=cells[2] if len(cells)>2 else '',pert=cells[3] if len(cells)>3 else '',cons=cells[4] if len(cells)>4 else '',date=cells[5] if len(cells)>5 else '',text=txt,src=os.path.basename(f),fetched=r.get('publish_date'))
            rows[idd]=rec; prow.append(icvr)
        if prow: pages[p]=(prow[0],prow[-1],len(prow))
import os
mf=os.path.join(os.path.dirname(sys.argv[2]),'manual_rows.csv')
if os.path.exists(mf):
    for r in csv.DictReader(open(mf)): rows[r['edb']]=r
w=csv.DictWriter(open(sys.argv[2],'w',newline=''),fieldnames=['page','edb','icvr','bib','pert','cons','date','text','src','fetched'])
w.writeheader()
for k in sorted(rows,key=lambda k:int(rows[k]['page'])): w.writerow(rows[k])
for p in sorted(pages): print(p,pages[p])
print('rows',len(rows))
