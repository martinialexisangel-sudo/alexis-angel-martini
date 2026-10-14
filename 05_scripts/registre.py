import json,glob,os,csv,sys,re,datetime
SP=sys.argv[1]; OUT=sys.argv[2]
rows=[]
for f in sorted(glob.glob(SP+'/edb/*.json')):
    d=json.load(open(f)); ts=os.path.getmtime(f)
    acc=datetime.datetime.fromtimestamp(ts,datetime.UTC).strftime('%Y-%m-%d')
    for r in d.get('results',[]):
        fc=r.get('full_content') or ''
        n=len(re.findall(r'epigraph/\d+',fc))
        rows.append(dict(date_acces=acc,outil='Parallel Search web_fetch (relais de lecture ; pas d’accès direct depuis le conteneur)',url=r['url'],extract_id=d.get('extract_id',''),resultat=f'page lue ; {n} fiches listées',date_page_signalee=r.get('publish_date') or '',usage='collation EDCS/EDB (liste de résultats EDB triée par n° ICVR)'))
    for e in d.get('errors',[]) or []:
        rows.append(dict(date_acces=acc,outil='Parallel Search web_fetch',url=e['url'],extract_id=d.get('extract_id',''),resultat='échec : '+str(e.get('error_type')),date_page_signalee='',usage='—'))
extra=[
('2026-10-14','curl (conteneur)','https://db.edcs.eu/epigr/epi.php','refusé par le proxy du conteneur (CONNECT 403)','—'),
('2026-10-14','curl (conteneur)','https://www.edb.uniba.it/','refusé par le proxy du conteneur','—'),
('2026-10-14','curl (conteneur)','http://www.edr-edr.it/default/index.php','refusé par le proxy du conteneur','—'),
('2026-10-14','curl (conteneur)','https://archive.org ; https://gallica.bnf.fr ; https://www.persee.fr ; https://zenon.dainst.org ; https://api.crossref.org ; https://www.jstor.org ; https://catalog.hathitrust.org ; https://www.worldcat.org ; https://kvk.bibliothek.kit.edu','refusés par le proxy du conteneur','—'),
('2026-10-14','curl (conteneur)','https://zenodo.org/records/3575485 (EDB, EpiDoc, CC BY 4.0, DOI 10.5281/zenodo.3575485)','refusé par le proxy ; jeu de données identifié mais non téléchargé','à télécharger hors de cet environnement'),
('2026-10-14','WebFetch','https://db.edcs.eu/epigr/edcs_id_en.php?p_edcs_id=EDCS-34200654','échec DNS (ENOTFOUND)','—'),
('2026-10-14','WebFetch','https://www.edb.uniba.it/epigraph/1','échec DNS (ENOTFOUND)','—'),
('2026-10-14','WebFetch','https://zenodo.org/api/records/3575485 ; https://archive.org/advancedsearch.php','échec DNS (ENOTFOUND)','—'),
('2026-10-14','Parallel Search web_fetch','https://www.edb.uniba.it/epigraph/1000 ; /epigraph/30458 ; /epigraph/30464','fiches lues (tests de structure)','méthode'),
('2026-10-14','Parallel Search web_fetch','https://www.trismegistos.org/dataservices/texrelations/edcs/34200654','réponse incohérente (TM_ID 0) : concordance EDCS→EDB inutilisable par cette voie','—'),
('2026-10-14','WebSearch (résumé de moteur, pages non ouvertes)','Brill/De Gruyter Brill ; EFR ; Brepols ; PIAC ; politique IA De Gruyter Brill','extraits de résultats seulement ; à vérifier sur les pages officielles','dossier de soumission'),
('2026-10-14','Google Drive (connecteur)','PRISME_BASE_SCIENTIFIQUE_V2 (1Y4JYDJSP_43O4cU57mbsi7D6Cz90k25W3WiZr62s820) ; PRISME_MONOGRAPHIE_REVISEE.pdf (1FgjEwWhfmYP0lp7VCbPBzC0mFrg8Aw-A) ; État critique… (1EK6eph6evZrC_lOwfYa3DuYj4_uwsWURaGsFirfglUA)','téléchargés ; aucune version 3.1 (696 p.) trouvée dans le Drive','base de travail'),
]
for p,ex in [(256,'extract_e53036d833e754d4e9ff1ed7c1138d83'),(257,'extract_e53036d833e754d4e9ff1ed7c1138d83'),(264,'extract_e53036d833e754d4e9ff1ed7c1138d83'),(266,'extract_e53036d833e754d4e9ff1ed7c1138d83'),(271,'extract_e53036d833e754d4e9ff1ed7c1138d83'),(290,'extract_c8179d80a9fe6ef6b8f37b8e761f3945'),(291,'extract_c8179d80a9fe6ef6b8f37b8e761f3945'),(301,'extract_c8179d80a9fe6ef6b8f37b8e761f3945'),(339,'extract_c8179d80a9fe6ef6b8f37b8e761f3945'),(340,'extract_c8179d80a9fe6ef6b8f37b8e761f3945')]:
    rows.append(dict(date_acces='2026-10-14',outil='Parallel Search web_fetch (réponse reçue en ligne, non archivée en fichier ; bornes et fiche utile recopiées à la main)',url=f'https://www.edb.uniba.it/search/quick/do?page={p}',extract_id=ex,resultat='page lue ; 20 fiches',date_page_signalee='',usage='repérage (bornes ICVR) ; p. 301 : fiche EDB21460 = ICVR 5935'))
for a,o,u,res,us in extra: rows.append(dict(date_acces=a,outil=o,url=u,extract_id='',resultat=res,date_page_signalee='',usage=us))
w=csv.DictWriter(open(OUT,'w',newline=''),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows))
