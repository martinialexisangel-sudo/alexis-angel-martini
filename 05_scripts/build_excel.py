import csv,re
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
wb=Workbook(); H=Font(bold=True,color="FFFFFF"); F=PatternFill("solid",fgColor="1F3864")
def sheet(name,rows,widths,first=False):
    ws=wb.active if first else wb.create_sheet(); ws.title=name
    for r in rows: ws.append(r)
    for c in ws[1]: c.font=H; c.fill=F
    ws.freeze_panes="A2"; ws.auto_filter.ref=ws.dimensions
    for i,w in enumerate(widths,1): ws.column_dimensions[get_column_letter(i)].width=w
    for row in ws.iter_rows():
        for c in row: c.alignment=Alignment(wrap_text=True,vertical="top")
sheet("Lisez-moi",[["Élément","Description"],
["Objet","PRISME — collation EDCS (base v2.0) / EDB (Epigraphic Database Bari), avec appoint de l'EDH ; lots 1-5, 14 oct. 2026"],
["Niveau de preuve","Collation base contre base : ni ICVR imprimée, ni photographie, ni autopsie"],
["Bilan","456/478 notices appariées (281 concordantes, 137 à examiner, 38 divergentes) ; 16 absentes de la liste publique EDB ; 6 introuvables"],
["Corpus","473 textes distincts datés de 340-403 (doublons 106, 282, 329 fusionnés ; 393+394 = un texte ; n° 98 hors période, 461/482)"],
["Consuls (lot 5)","Fondement de l'année de 457 textes à datation directe : A lu 338, B partiel 97, C initiales 2, R restitué 20 ; 30 faux consuls de la v2.0 (feuilles Consuls_lus_restitues, Faux_consuls_v2)"],
["Licences","EDB et EDH : CC BY-SA 4.0"],
["Source","PR martinialexisangel-sudo/alexis-angel-martini#1"]],[22,110],True)
C=list(csv.DictReader(open('02_verifications/collation_edcs_edb.csv')))
X={r['n']:r['source'] for r in csv.DictReader(open('05_scripts/mapping_extra.csv'))}
absent={'12','13','25','26','45','65','116','117','149','161','202','212','374','406','407','452'}
lab=['N°','ICUR','EDCS-ID','Année v2.0','EDB','ICVR (EDB)','Provenance (EDB)','Conservation (EDB)','Date (EDB)','Bibliographie EDB','Statut','Similarité','Appariement hors ICUR','Texte EDCS (v2.0)','Texte EDB']
rows=[lab]
for r in C:
    st=r['statut']
    if r['n'] in absent: st='absent de la liste publique EDB'
    if r['n'] in ('106','282','329'): st='doublon (fusionné)'
    if r['n']=='394': st+=' ; fusionné avec 393 (fragments)'
    if r['n']=='98': st='HORS CORPUS (461/482) ; '+st
    cl=lambda x:x.replace('\\-','-').replace('**More**','[tronqué : More]')
    rows.append([int(r['n']),r['icur'],r['edcs'],int(float(r['annee'])),r['edb_id'],r['edb_icvr'],cl(r['edb_pert']),cl(r['edb_cons']),r['edb_date'],cl(r['edb_bib']),st,float(r['ratio']) if r['ratio'] else None,X.get(r['n'],''),r['edcs_text'],cl(r['edb_text'])])
sheet("Collation",rows,[6,22,15,9,11,10,30,28,12,25,28,9,30,60,60])
ch=[["N°","EDB","Signes décrits par l'EDB"]]
for r in C:
    k=[x for x in re.findall(r'\(\(([^)]*)\)\)',r['edb_text']) if 'monogramma Christi' in x or 'crux' in x]
    if k: ch.append([int(r['n']),r['edb_id'],' ; '.join(k)])
sheet("Chrismes_croix",ch,[6,11,80])
sheet("Divergences_dates",[["N°","EDB","Année v2.0","Date EDB","Commentaire"],
[98,"EDB20076",366,"461 ; 482","Severinus lu, Dagalaiphi restitué : HORS CORPUS (CLRE p. 680 cité par l'EDB)"],
[40,"EDB30464",353,"352","CLRE p. 636 (cité par l'EDB) : 352 ; v2.0 : 353"],
[141,"EDB9633",370,"370 ; 387","CLRE p. 644 : « Year doubtful: 387 possible »"],
[206,"EDB880",370,"377","Valentinien III et Valens III = 370 ; erreur probable de l'EDB (inscription peinte)"],
[278,"EDB3285",383,"385","Merobaudes II et Saturninus = 383 ; incohérence interne de l'EDB probable"],
[311,"EDB22064",388,"389","Maximo cons. ; « Transcription different from ICVR »"],
[314,"EDB39579",390,"389-390","Note EDB : le frère est mort avant ; restitution 390 contradictoire"],
[328,"EDB17191",381,"390","…terio lu seul : Eucherio (381) ou Neoterio (390)"],
[434,"EDB34468",397,"399","p.c. Arcadi IIII = 397 ; à vérifier"]],[6,11,10,10,80])
sheet("Dossiers",[["Dossier","Notices","Conclusion","Certitude","Preuve"],
["A006 doublon","329 / 336","Fusion dans 336 ; 2 fragments (Treia, Ostie) ; âge L[X]V restitué","certain","EDB10126 ; EDH HD009698"],
["A007 doublon","106 / 120","Fusion dans 120 ; variante c(iu)esq(it)/recessit en apparat","certain","EDH HD030246 ; EDB13167"],
["A008 doublon","282 / 288","Fusion dans 288 ; variante An]iciae (EDH) / Euticiae","certain","EDH HD021839 ; EDB11278"],
["A009","313 / 314","Un monument, deux commémorations ; date de (b) incertaine","très probable / incertain","EDB39579"],
["A010","393 / 394","Deux fragments d'une même plaque ; un seul texte daté 396 (lecture Ferrua)","très probable","EDB39590"],
["Hors corpus","98","Severinus lu → 461/482","très probable","EDB20076 ; EDH HD028015"],
["Provenance","439","Provenance non établie (Tibur ?) ; pierre perdue","probable","EDB33162"],
["Provenance","369","Incertae originis ; conservée à Valencia","à vérifier","EDB42064"],
["Interprétation","38","Chr(isti) = chrisme","très probable","EDB17657"],
["Interprétation","474","Lecture identique ; portée nicéenne = hypothèse ; pierre perdue","lecture certaine (2 bases)","EDB35329"],
["A016 datations","51, 84, 180, 214, 268, 388, 445, 447","Formule consulaire transmise par l'EDB, absente de l'EDCS","lue ou restituée","fiches EDB"],
["A016 datations","123, 326, 435, 457","Restitutions consulaires conjecturales","conjectural","fiches EDB"]],[18,24,60,22,28])
sheet("Registre_consultations",list(csv.reader(open('02_verifications/REGISTRE_CONSULTATIONS.csv'))),[12,30,60,25,30,14,30])
sheet("Statistiques",[["Mesure","Valeur","Dénominateur"],["Textes distincts datés 340-403",473,478],["Lectures stabilisées (concordantes)",279,474],
["Années 340",16,279],["Années 350",10,279],["Années 360",46,279],["Années 370",49,279],["Années 380",72,279],["Années 390",64,279],["400-403",22,279],
["in pace (texte EDB, approx.)",94,279],["Chrisme ou croix (lectures stabilisées)",27,279],["Chrisme ou croix (toutes notices appariées)",47,456],
["Datation directe : nom consulaire lu (A)",338,457],["Datation directe : lecture partielle (B)",97,457],["Datation directe : initiales (C)",2,457],["Datation directe : consulat restitué (R)",20,457],["Faux consuls dans la liste v2.0",30,"29 notices"]],[45,10,14])
K=list(csv.DictReader(open('02_verifications/consuls_lus_restitues.csv')))
sheet("Consuls_lus_restitues",[["N°","Année v2.0","Noms consulaires et état (auto)","Niveau automatique","Niveau final","Relu à la main","Justification","Texte EDCS (v2.0)"]]+
  [[int(r['n']),int(float(r['annee'])),r['consuls'],r['niveau_auto'],r['niveau_final'],r['revu_main'],r['justification'],r['texte']] for r in K],[6,9,45,30,30,8,60,80])
sheet("Faux_consuls_v2",list(csv.reader(open('02_verifications/consuls_faux_positifs_v2.csv'))),[6,9,14,40,45,35])
wb.save('06_livrables/PRISME_collation_EDCS_EDB.xlsx')
