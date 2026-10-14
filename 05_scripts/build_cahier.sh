#!/bin/bash
set -e
R=/home/user/alexis-angel-martini; SP=/tmp/claude-0/-home-user-alexis-angel-martini/fdf41730-a49c-58dc-81a0-9336a7868929/scratchpad
cd $R
cat > $SP/meta.md <<'M'
---
title: "PRISME — Cahier de révision v3 (lots 1-5)"
subtitle: "Épitaphes chrétiennes datées de Rome (340–403) — consolidation documentaire"
author: "Alexis Angel Martini (auteur) ; consolidation assistée"
date: "14 octobre 2026"
lang: fr
---
M
FILES="$SP/meta.md README.md 03_dossiers_anomalies/DOSSIERS_ANOMALIES.md 03_dossiers_anomalies/CHAPITRE_5_4_CONFRONTATION_EDB.md 02_verifications/ETAT_COLLATION.md 02_verifications/STATISTIQUES_STABILISEES.md 03_dossiers_anomalies/AUDIT_ETAT_CRITIQUE.md 04_soumission/EVALUATION_SUR_20.md 04_soumission/CONSIGNES_EDITEURS.md 04_soumission/PROPOSITION_EDITORIALE.md JOURNAL_MODIFICATIONS.md"
pandoc $FILES --toc -s -o 06_livrables/PRISME_cahier_revision_v3_lot1.docx
pandoc $FILES --toc -s --metadata title="PRISME — Cahier de révision v3 (lots 1-5)" -c x.css -o $SP/cahier.html
python3 - <<'P'
p='/tmp/claude-0/-home-user-alexis-angel-martini/fdf41730-a49c-58dc-81a0-9336a7868929/scratchpad/cahier.html'
s=open(p).read()
css='<style>body{font-family:"DejaVu Serif",serif;font-size:10pt;max-width:none;margin:0} table{border-collapse:collapse;font-size:8.5pt;width:100%} td,th{border:1px solid #999;padding:2px 4px;vertical-align:top} code{font-family:"DejaVu Sans Mono";font-size:8pt;white-space:pre-wrap} h1{font-size:15pt;page-break-before:always} h2{font-size:12.5pt} h3{font-size:11pt} @page{size:A4;margin:18mm 16mm}</style>'
s=s.replace('<link rel="stylesheet" href="x.css" />',css)
open(p,'w').write(s)
P
cat > $SP/pdf.js <<'J'
const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('file://'+process.argv[2]);await p.pdf({path:process.argv[3],format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<span></span>',footerTemplate:'<div style="font-size:7pt;width:100%;text-align:center"><span class="pageNumber"></span>/<span class="totalPages"></span></div>',margin:{top:'18mm',bottom:'18mm',left:'16mm',right:'16mm'}});await b.close();})();
J
node $SP/pdf.js $SP/cahier.html $R/06_livrables/PRISME_cahier_revision_v3_lot1.pdf
ls -la 06_livrables
