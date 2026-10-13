#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sporbar kildekode: integrerer delrapport 08 i statisk HTML og byggepipeline."""
from pathlib import Path
import re
root=Path(__file__).parent
b=root/'kildekode'/'bygg_publisering.py'
s=b.read_text('utf-8')

def repl(a,b):
    global s
    assert a in s, f'Expected builder substring missing: {a[:140]}'
    s=s.replace(a,b)

repl("DATE = '2026-10-12'\nVERSION = 'v0.9.0'", "DATE = '2026-10-13'\nVERSION = 'v1.0.0'")
repl("'kontrollert':'2026-10-12'", "'kontrollert':'2026-10-13'")
repl("assert len(sources)==136, f'forventet 136 kilder, fant {len(sources)}'", "assert len(sources)==151, f'forventet 151 kilder, fant {len(sources)}'")
repl("'rapportversjon':'0.9.0',", "'rapportversjon':'1.0.0',")
# Fix pre-existing missing comma in math substitutions.
# Add original data 08: no *generated scenario* rows as observations.
anchor="with (DATA/'observasjoner.csv').open('w',encoding='utf-8-sig',newline='') as f:"
newblock='''# Forskningstråd 08: official past data, budget estimates and separately declared forecast assumptions.
# The 444 synthetic scenario observations belong ONLY to scenarier_08, never observasjoner.csv.
FONDSBRUK08=json.loads((ROOT/'data'/'fondsbruk_08.json').read_text('utf-8'))
PETROL08=json.loads((ROOT/'data'/'petroleum_08.json').read_text('utf-8'))
FUND08=json.loads((ROOT/'data'/'fondsverdi_08.json').read_text('utf-8'))
UTTAK08=json.loads((ROOT/'data'/'uttaksprosent_historikk_08.json').read_text('utf-8'))
BUDSJ08=json.loads((ROOT/'data'/'regnskapsbegreper_08.json').read_text('utf-8'))
HOVED08=json.loads((ROOT/'data'/'hovedindikatorer_08.json').read_text('utf-8'))
SCEN08=json.loads((ROOT/'data'/'scenarieoppsummering_08.json').read_text('utf-8'))
for r in FONDSBRUK08:
    year=r['aar']
    for label, field, unit in [('Strukturelt oljekorrigert underskudd','strukturelt_underskudd_lopende_mrd','mrd. kroner'),('Andel trend-Fastlands-BNP','andel_trend_fastlands_bnp_prosent','prosent'),('Andel statens utgifter','andel_statsbudsjettets_utgifter_prosent','prosent'),('Andel beregnet inngangs-SPU','andel_fondsverdi_prosent','prosent')]:
        put('fondsbruk_08','Statsfinanser',label,year,'Nasjonalbudsjettet 2027-vintage',r[field],unit,r['kilde_id'],r['observasjonsstatus'],r['merknad'])
for r in PETROL08:
    put('petroleum_08','Petroleum','Netto petroleumskontantstrøm: '+r['komponent'],r['aar'],'Staten',r['milliarder_kroner_lopende'],'mrd. kroner',r['kilde_id'],r['status'],r['merknad'])
for r in FUND08:
    put('fondsverdi_08','Statsfinanser','SPU, markedsverdi',r['periode'],'NBIM',r['fond_mrd_nok'],'mrd. kroner',r['kilde_id'],r['status'],r['merknad'])
for r in UTTAK08:
    put('uttaksprosent_08','Statsfinanser','Strukturelt uttak av inngangs-SPU',r['aar'],'Nasjonalbudsjett, historisk figur',r['uttaksprosent'],'prosent',r['kilde_id'],r['status'],r['merknad'])
for r in BUDSJ08:
    put('regnskap_08','Statsfinanser',r['indikator'],r['aar'],'Budsjettforslag/anslag',r['milliarder_kroner_lopende'],'mrd. kroner',r['kilde_id'],r['status'],'Kontantpost eller strukturindikator; se originaldefinisjon')
for r in HOVED08:
    put('hovedindikatorer_08','Statsfinanser',r['indikator'],r['periode'],'Norge',r['verdi'],r['enhet'],r['kilde_id'],r['status'],r['merknad'])

'''
repl(anchor,newblock+anchor)
repl("for traad in ('02','03','04','05','06','07'):","for traad in ('02','03','04','05','06','07','08'):")
# Extend nested ternary adding 08 override separately after item creation to avoid disrupting existing anchors.
anchor2="assert len(hypotheses)==81, f'Uventet antall hypoteser: {len(hypotheses)}'"
repl(anchor2,"""# Report 08 has a dedicated chapter; not a subchapter of taxation.
for hypo in hypotheses:
    if hypo['id'].startswith('H08-'):
        hypo['ankerkobling']='#rapport-19-forskningstrad-08-petroleum-spu-og-finanspolitisk-baerekraft'
assert len(hypotheses)==95, f'Uventet antall hypoteser: {len(hypotheses)}'""")
repl("+ json.loads((ROOT/'data'/'evidensregister_07.json').read_text('utf-8'))\nassert len(evidence)==204, f'evidens: {len(evidence)}'", "+ json.loads((ROOT/'data'/'evidensregister_07.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_08.json').read_text('utf-8'))\nassert len(evidence)==236, f'evidens: {len(evidence)}'")
repl("  '@@HOVED07@@':json.dumps(HOVED07,ensure_ascii=False).replace('<','\\u003c'),", """  '@@HOVED07@@':json.dumps(HOVED07,ensure_ascii=False).replace('<','\\u003c'),
  '@@FONDSBRUK08@@':json.dumps(FONDSBRUK08,ensure_ascii=False).replace('<','\\u003c'),
  '@@PETROL08@@':json.dumps(PETROL08,ensure_ascii=False).replace('<','\\u003c'),
  '@@FUND08@@':json.dumps(FUND08,ensure_ascii=False).replace('<','\\u003c'),
  '@@UTTAK08@@':json.dumps(UTTAK08,ensure_ascii=False).replace('<','\\u003c'),
  '@@BUDSJ08@@':json.dumps(BUDSJ08,ensure_ascii=False).replace('<','\\u003c'),
  '@@HOVED08@@':json.dumps(HOVED08,ensure_ascii=False).replace('<','\\u003c'),
  '@@SCEN08@@':json.dumps(SCEN08,ensure_ascii=False).replace('<','\\u003c'),""")
repl("'*_07.*'):","'*_07.*','*_08.*'):")
repl("copy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',SITE/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')", "copy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',SITE/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')\ncopy_if_different(ROOT/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md',SITE/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md')")
repl("copy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',OUT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')", "copy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',OUT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')\ncopy_if_different(ROOT/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md',OUT/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md')")
# Avoid packing historic obsolete duplicate test scripts in the public zip, keep rebuild code and data.
repl("not f.name.startswith(('qa_06_', '_test_web06'))", "not f.name.startswith(('qa_06_', '_test_web06', 'qa_08_', '_test_web08'))")
b.write_text(s,'utf-8')

# Correct references to the 2026 H1 return, which must cite [K140] rather than theoretical [K149].
for name in ('08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md','Norsk_Okonomi_Forskningsrapport_2026-10-13_v1.0.0.md'):
    f=root/name;t=f.read_text('utf-8')
    old='som om den var garantert. [K141](#k141) [K149](#k149) [K144](#k144)'
    assert old in t
    t=t.replace(old,'som om den var garantert. [K141](#k141) [K140](#k140) [K144](#k144)')
    f.write_text(t,'utf-8')

# Publish site, new chart, model and downloads. Build from one editable template.
t=root/'kildekode'/'mal_nettside.html'
h=t.read_text('utf-8')
h=h.replace('2026-10-12','2026-10-13').replace('0.9.0','1.0.0')
h=h.replace('06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v1.0.0.md','06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')
h=h.replace('<a href="#offentlig07">Offentlig 07</a>', '<a href="#offentlig07">Offentlig 07</a><a href="#olje08">Petroleum 08</a>')
h=h.replace('fra tråd 01–07.','fra tråd 01–08.').replace('fra alle sju delrapporter','fra alle åtte delrapporter')
h=h.replace('statsbudsjettets utgifter', 'statsbudsjettets utgifter')
# Reflect newest confirmed October 2026 budget vintage in the hero KPI, leaving earlier vintage in the historical article.
h=h.replace('Strukturelt oljekorrigert underskudd · 2026</div><strong>579 mrd.</strong><div class="meta">Revidert budsjettanslag · <a href="#k05">[K05]</a>', 'Strukturelt oljekorrigert underskudd · forslag 2027</div><strong>608,4 mrd.</strong><div class="meta">Nasjonalbudsjettet 2027 · <a href="#k137">[K137]</a>')
h=h.replace('Første offentlig forskningsdelrapport.', 'Åtte kildedokumenterte delrapporter under utvikling.')
h=h.replace('Nettstedet inneholder ingen tredjepartssporing', 'Nettstedet inneholder ingen tredjepartssporing')
h=h.replace('id="evidensregister_07.csv"', 'id="evidensregister_07.csv"')
h=h.replace('<a href="data/evidensregister_07.csv" download>CSV tråd 07</a>', '<a href="data/evidensregister_07.csv" download>CSV tråd 07</a><a href="data/evidensregister_08.csv" download>CSV tråd 08</a><a href="data/hypoteseregister_08.csv" download>Hypoteser 08</a><a href="08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md" download>Delrapport 08</a>')
h=h.replace('fra tråd 01–07', 'fra tråd 01–08')
h=h.replace('Forskning under utvikling; ikke fagfellevurdert.', 'Kildedokumentert arbeid under utvikling; ikke fagfellevurdert.')
h=h.replace('La', 'La')
# Add section styling before </style>
css='''
/* Forskningstråd 08: visning av budsjettkilder og eksplisitt betingede modeller. */
.spu08-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:18px 0 25px}
.spu08-kpi{padding:18px;border:1px solid var(--line);background:var(--card);border-radius:8px;min-width:0;display:grid;gap:8px}
.spu08-kpi span{font-size:12px;line-height:1.42;color:var(--muted)}
.spu08-kpi b{font-family:Georgia,serif;font-weight:600;font-size:clamp(22px,2vw,30px);color:var(--ink)}
.spu08-grid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:18px;margin-bottom:18px}
.spu08-chart{width:100%;min-height:280px}.spu08-chart svg{width:100%;max-height:380px;display:block}
.spu08-panel label{display:block;color:var(--ink2);font-size:13px;margin:0 0 8px}
.spu08-inputs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;margin:14px 0}
.spu08-inputs label{padding:12px;border:1px solid var(--line);border-radius:6px;display:grid;gap:8px;margin:0}
.spu08-inputs output{font-weight:700;color:var(--main2)}
.spu08-inputs input{width:100%}
.spu08-notice{background:var(--soft);border-left:3px solid var(--main);padding:13px 15px;line-height:1.65;font-size:13px;margin:15px 0}
.spu08-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.spu08-stat{background:var(--soft);padding:13px;border-radius:7px}
.spu08-stat small{display:block;font-size:12px;color:var(--muted)}
.spu08-stat strong{display:block;font-size:clamp(17px,2vw,22px);color:var(--ink);margin-top:7px}
.spu08-note{color:var(--muted);line-height:1.6;font-size:13px}
.spu08-graph-title{font-weight:600;font-size:18px;margin:16px 0 8px;color:var(--ink)}
@media(max-width:900px){.spu08-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.spu08-grid{grid-template-columns:1fr}}
@media(max-width:500px){.spu08-kpis,.spu08-inputs{grid-template-columns:1fr}.spu08-stats{grid-template-columns:1fr}}
'''
assert '</style>' in h
h=h.replace('</style>',css+'</style>')

html='''<section class="section" id="olje08">
 <div class="section-heading"><div><p class="eyebrow-dark">08 / Petroleumsformue og bærekraft</p><h2>Kan oljefondet finansiere fremtidens Norge?</h2></div><p class="section-note">Skill mellom petroleumsinnskudd, faktiske kontantuttak, strukturelle budsjettall, fondskapital og fremtidige offentlige forpliktelser. Alle kildedata kan kontrolleres i tabellen.</p></div>
 <div class="spu08-kpis" aria-label="Nøkkeltall fra Nasjonalbudsjettet 2027">
  <div class="spu08-kpi"><span>Strukturelt underskudd · forslag 2027</span><b>608,4 mrd.</b><span>Styringsmål, ikke faktiske fondskontanter <a href="#k137">[K137]</a></span></div>
  <div class="spu08-kpi"><span>Faktisk budsjettert uttak · 2027</span><b>561,7 mrd.</b><span>Oljekorrigert kontantunderskudd <a href="#k139">[K139]</a></span></div>
  <div class="spu08-kpi"><span>Andel av statsbudsjettets utgifter · 2027</span><b>26,6 %</b><span>Strukturelt underskudd / statsutgifter <a href="#k137">[K137]</a></span></div>
  <div class="spu08-kpi"><span>Langsiktig finansieringsgap · 2060</span><b>5,8 %</b><span>Av Fastlands-BNP i betinget referansebane <a href="#k137">[K137]</a></span></div>
 </div>
 <div class="spu08-grid">
  <div class="panel spu08-panel"><label for="spu08-valg">Velg datagrunnlag fra primærkilder</label>
   <select id="spu08-valg" aria-label="Velg datavisning for petroleum og oljefondet">
    <option value="budsjett">Fondsbruk som del av statens utgifter 2025–2027</option>
    <option value="fondsverdi">SPUs markedsverdi ved års-/halvårsslutt</option>
    <option value="uttak">Strukturell uttaksprosent av inngangsfond 2001–2027</option>
    <option value="kontanter">Kontantunderskudd mot strukturelt underskudd</option>
    <option value="petroleum">Statens netto petroleumskontantstrøm 2026–2027</option>
    <option value="gap">Reviderte anslag for finansieringsgapet i 2060</option>
   </select>
   <div id="spu08-tittel" class="spu08-graph-title">Historisk og budsjettert fondsbruk</div>
   <div id="spu08-graf" class="spu08-chart" role="img" aria-label="Figur for valgte, dokumenterte tall" aria-live="polite"></div>
   <p id="spu08-merknad" class="spu08-note" aria-live="polite"></p>
   <p class="spu08-note"><a id="spu08-kilde" href="#k137">Primærkilde K137</a> · <a href="#rapport-19-forskningstrad-08-petroleum-spu-og-finanspolitisk-baerekraft">Vitenskapelig metode i delrapport 08</a></p>
  </div>
  <div class="panel"><h3>Dokumenterte verdier</h3>
   <p class="panel-sub">Samme kildekoblede verdier som figuren. Budsjettanslag og historiske observasjoner merkes forskjellig.</p>
   <div class="data-box" id="spu08-tabell"></div>
   <button type="button" class="pill-button" id="spu08-csv">Last ned tabellen (CSV)</button>
   <p class="spu08-notice"><strong>Viktig:</strong> Budsjettforslag for 2027 er ikke vedtatt statsregnskap. Beregningsteknisk fondsverdi 1.1.2027 er ikke målt. Høy historisk avkastning er ikke garanti for forventet 3 % realavkastning.</p>
  </div>
 </div>
 <div class="spu08-grid">
  <div class="panel spu08-panel">
   <h3>Langsiktig fondsstresstest 2027–2100</h3>
   <p class="spu08-note">Transparent, deterministisk beregningsmodell. Utgangspunktet er beregnet fondsverdi 22 400 mrd., statens forventede netto petroleumsinnskudd 568,4 mrd. og faktisk kontantuttak 561,7 mrd. i 2027. Verken budsjettets strukturelle underskudd på 608,4 mrd. eller prognostisert fremtidig valutakurs brukes som kontantuttak.</p>
   <label for="spu08-scenario">Seks eksempelscenarioer / egne innstillinger</label>
   <select id="spu08-scenario"><option value="A">A – mekanisk referanse</option><option value="B">B – lav realavkastning</option><option value="C">C – raskere vekst i uttak</option><option value="D">D – initialt fondssjokk</option><option value="E">E – raskt fall i petroleum</option><option value="F">F – kombinert belastning</option><option value="egen">Egne forutsetninger</option></select>
   <div class="spu08-inputs">
    <label>Årlig realavkastning <output id="spu08-r-v">3,0 %</output><input id="spu08-r" type="range" min="-1" max="6" step="0.5" value="3"></label>
    <label>Årlig vekst i kontantuttak <output id="spu08-g-v">1,5 %</output><input id="spu08-g" type="range" min="0" max="5" step="0.5" value="1.5"></label>
    <label>Årlig fall i petroleumstilførsel <output id="spu08-d-v">6,0 %</output><input id="spu08-d" type="range" min="0" max="15" step="0.5" value="6"></label>
    <label>Engangsfall i startfondet <output id="spu08-s-v">0,0 %</output><input id="spu08-s" type="range" min="0" max="40" step="5" value="0"></label>
   </div>
   <div class="spu08-stats" aria-live="polite"><div class="spu08-stat"><small>Fondsverdi ved utgangen av 2060</small><strong id="spu08-2060">–</strong></div><div class="spu08-stat"><small>Fondsverdi ved utgangen av 2100</small><strong id="spu08-2100">–</strong></div><div class="spu08-stat"><small>Første år med uttak større enn 3 % av inngangsfond</small><strong id="spu08-3p">–</strong></div></div>
   <div class="spu08-chart" id="spu08-scenariograf" role="img" aria-label="Simulert fondsbane 2027–2100; kun scenario"></div>
   <p class="spu08-note">Beregning i faste, hypotetiske modellkroner uten egen valutakurs-/realnivåbro. Formel: neste fondsverdi = maksimum av null og (årets fond × (1 + realavkastning) + petroleumstilførsel − kontantuttak). Fra nullsaldo registreres et eventuelt teknisk udekket finansieringsbehov. Statens øvrige inntekter og utgifter er ikke modellert; resultatene er <strong>ikke</strong> prognoser eller sannsynlighetsanslag.</p>
   <button type="button" id="spu08-modellcsv" class="pill-button">Last ned simulert årsbane (CSV)</button>
  </div>
  <div class="panel"><h3>Hva stresstesten kan og ikke kan konkludere med</h3>
    <div class="spu08-notice"><strong>Fondet og statsfinansene er ikke samme størrelse.</strong> Selv om markedsverdien vokser, kan pensjoner, helse, omsorg, forsvar og øvrige realressurskrav vokse raskere. Omvendt er ikke et tenkt fall i fondet en automatisk statsfinansiell krise.</div>
    <p class="spu08-note">Kontantstrømmer, kjøpekraft, skattebase, kostnader, valuta og framtidige politiske tilpasninger er vesentlige usikkerhetskilder. Finansdepartementets 2060-gapanalyse er en egen makroframskriving; denne nettsidens mekaniske fondsmodell <em>reproduserer ikke</em> regjeringens modell.</p>
    <div class="data-box" id="spu08-modelltabell"></div>
    <p class="spu08-note"><a href="data/scenarier_08.csv" download>Alle seks forhåndsberegnede scenarier (CSV)</a> · <a href="data/scenarieoppsummering_08.json" download>Forutsetninger og resultater (JSON)</a> · <a href="kildekode/modell_08.py" download>Beregningskode (Python)</a></p>
    <p class="spu08-note">For kausale spørsmål om omstilling, generasjonsregnskap og «hollandsk syke» viser evidensregisteret hvilke tester som ennå mangler.</p>
  </div>
 </div>
 <p class="chart-note"><a href="08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md" download>Last ned delrapport 08</a> · <a href="data/hypoteseregister_08.csv" download>Hypoteser (CSV)</a> · <a href="data/evidensregister_08.csv" download>Evidens (CSV)</a> · <a href="data/proveniens_08.json" download>Kildeproveniens (JSON)</a>. Modellerte scenarioverdier er ikke tatt med i tallet for dokumenterte observasjoner.</p>
</section>

'''
assert '<section class="section" id="stresstest">' in h
h=h.replace('<section class="section" id="stresstest">',html+'<section class="section" id="stresstest">')
h=h.replace('Oljefondet: 30-års stresstest', 'Arkivert enkeltmodell for fondet, 2025–2055')
h=h.replace('Start 2025: 21 268 mrd. kroner. Første uttak: 579 mrd. kroner. Alle beløp i forenklede faste kroner.', 'Tidligere illustrasjon. Start 2025: 21 268 mrd. kroner; 579 mrd. er <em>strukturelt</em> budsjettunderskudd fra RNB 2026, ikke faktisk netto kontantuttak. Bruk <a href="#olje08">den forbedrede modellen i delrapport 08</a> for korrekte 2027-budsjettstrømmer.')
# Embedded sources arrays
anchor='const HOVED_07 = @@HOVED07@@;'
assert anchor in h
h=h.replace(anchor,anchor+'''
// 2027-budget vintage, NBIM valuation history and scenario assumptions – thread 08.
const FONDSBRUK_08 = @@FONDSBRUK08@@;
const PETROL_08 = @@PETROL08@@;
const FUND_08 = @@FUND08@@;
const UTTAK_08 = @@UTTAK08@@;
const BUDSJ_08 = @@BUDSJ08@@;
const HOVED_08 = @@HOVED08@@;
const SCEN_08 = @@SCEN08@@;
''')
# Insert JavaScript right before final init call. Keep all controls functional.
js=r'''
// Studie 08 – kildedrevne figurer og egne, tydelig merkede scenarioer.
let valgt08=[];
function kildeFigur08(key){return {budsjett:'K137',fondsverdi:'K140',uttak:'K147',kontanter:'K137',petroleum:'K142',gap:'K137'}[key]||'K137';}
function dataFigur08(mode){
 const f=(r,v)=>({label:String(r),value:Number(v)});
 if(mode==='budsjett')return {title:'Strukturelt underskudd i prosent av statens utgifter',unit:'prosent',type:'bar',ref:'K137',note:'Tall for 2025–2027 i samme Nasjonalbudsjett 2027-vintage. 2027 er et budsjettforslag. Andelen bruker departementets statsbudsjettdefinisjon, ikke hele offentlig forvaltning.',data:FONDSBRUK_08.map(r=>f(r.aar,r.andel_statsbudsjettets_utgifter_prosent))};
 if(mode==='fondsverdi')return {title:'SPUs markedsverdi i løpende norske kroner',unit:'mrd. NOK',type:'line',ref:'K140',note:'Årsverdier fra NBIM 2016–2025. 2026-H1 er 30. juni, ikke årsslutt. Fondsverdien påvirkes av valutakurs, netto tilførsel og avkastning; ingen reell avkastning kan utledes fra figuren alene.',data:FUND_08.map(r=>f(r.periode,r.fond_mrd_nok))};
 if(mode==='uttak')return {title:'Strukturelt underskudd i prosent av inngangsfondet',unit:'prosent',type:'line',ref:'K147',note:'Historiske publiserte uttaksprosenter, supplert med 2027-forslaget fra Nasjonalbudsjettet 2027. Tallene er ikke fondets investeringsavkastning. Handlingsregelens referanse gikk fra 4 % til 3 % fra 2018.',data:UTTAK_08.map(r=>f(r.aar,r.uttaksprosent))};
 if(mode==='kontanter')return {title:'2026–2027: kontantuttak og strukturelle indikatorer',unit:'mrd. kr',type:'bar',ref:'K137',note:'Regnskapsteknisk forskjellige størrelser: kontantunderskudd er budsjettert overføring, strukturelt underskudd er styringsmål. Den særlige skattetrekkskontoendringen påvirker kontantunderskuddet i 2026.',data:BUDSJ_08.filter(r=>r.aar===2026||r.aar===2027).filter(r=>/Oljekorrigert kontantunderskudd|Strukturelt oljekorrigert underskudd/.test(r.indikator)).map(r=>f(`${r.aar} ${r.indikator.includes('Strukturelt')?'Struktur':'Kontant'}`,r.milliarder_kroner_lopende))};
 if(mode==='petroleum')return {title:'Statens netto petroleumskontantstrøm',unit:'mrd. kr',type:'bar',ref:'K142',note:'Anslag fra Nasjonalbudsjettet 2027, ikke endelige kontantregnskaper. Lavere petroleumsinnskudd til SPU er ikke det samme som at fondsverdien automatisk synker.',data:PETROL_08.filter(r=>/Netto kontantstrøm|Sum|Total/.test(r.komponent)).map(r=>f(r.aar,r.milliarder_kroner_lopende))};
 return {title:'Finansdepartementets alternative vintager for samme 2060-gap',unit:'prosent av Fastlands-BNP',type:'bar',ref:'K137',note:'Disse verdiene er ulike publiseringer av ANSLAG FOR SAMME ÅR 2060 (2024, 2025, 2026). Ikke utvikling i observerte år og ikke fondets egen kapitalbane.',data:[f('PM 2024',6.2),f('NB 2026',5.9),f('NB 2027',5.8)]};
}
function graf08(data,type,unit){
 if(!data.length)return '<p>Ingen datapunkter i denne figuren.</p>';
 const W=740,H=322,L=65,R=20,T=31,B=58;
 const nums=data.map(r=>r.value);const max=Math.max(...nums,0,1),min=Math.min(0,...nums),high=max*1.14||1,range=high-min;
 const sy=v=>H-B-(v-min)/range*(H-T-B),sx=i=>L+(i+.5)*(W-L-R)/data.length;
 let g=`<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(unit)}; ${data.length} verdier. Se tabellen ved siden av." xmlns="http://www.w3.org/2000/svg">`;
 for(let j=0;j<=4;j++){const v=min+(range*j/4),y=sy(v);g+=`<line x1="${L}" x2="${W-R}" y1="${y}" y2="${y}" stroke="var(--line)"/><text x="${L-9}" y="${y+4}" text-anchor="end" font-size="11" fill="var(--muted)">${esc(nfmt(v,v<20?1:0))}</text>`;}
 const tickEach=Math.max(1,Math.ceil(data.length/7));
 if(type==='line'){
   g+=`<polyline fill="none" stroke="var(--main)" stroke-width="3" points="${data.map((v,i)=>`${sx(i)},${sy(v.value)}`).join(' ')}"/>`;
   data.forEach((r,i)=>{g+=`<circle cx="${sx(i)}" cy="${sy(r.value)}" r="3.6" fill="var(--main)"><title>${esc(r.label)}: ${esc(nfmt(r.value,1))} ${esc(unit)}</title></circle>`;
    if(i%tickEach===0 || i===data.length-1)g+=`<text x="${sx(i)}" y="${H-B+22}" text-anchor="middle" font-size="11" fill="var(--muted)">${esc(r.label)}</text>`;});
 }else{
   const cw=(W-L-R)/data.length,bw=Math.min(70,cw*.56);data.forEach((r,i)=>{const x=sx(i)-bw/2,y=sy(Math.max(0,r.value)),zero=sy(0);g+=`<rect x="${x}" y="${y}" height="${Math.max(1,zero-y)}" width="${bw}" rx="3" fill="${i===0?'var(--main)':'#69a8a3'}"><title>${esc(r.label)}: ${esc(nfmt(r.value,1))} ${esc(unit)}</title></rect><text x="${sx(i)}" y="${Math.max(15,y-8)}" text-anchor="middle" font-size="12" font-weight="600" fill="var(--ink)">${esc(nfmt(r.value,r.value<20?1:0))}</text><text x="${sx(i)}" y="${H-B+22}" font-size="11" text-anchor="middle" fill="var(--muted)">${esc(r.label.length>16?r.label.slice(0,14)+'…':r.label)}</text>`;});
 }
 return g+'</svg>';
}
function tabell08(rows,unit){return '<table><thead><tr><th>År / kategori</th><th>Verdi</th><th>Enhet</th></tr></thead><tbody>'+rows.map(r=>'<tr><td>'+esc(r.label)+'</td><td>'+nfmt(r.value,2)+'</td><td>'+esc(unit)+'</td></tr>').join('')+'</tbody></table>';}
function csv08(headers,rows){const q=v=>'"'+String(v).replace(/"/g,'""')+'"';return '\uFEFF'+[headers,...rows].map(row=>row.map(q).join(';')).join('\r\n')+'\r\n';}
function oppdater08(){
 const mode=el('spu08-valg').value,c=dataFigur08(mode);valgt08=c.data;
 el('spu08-tittel').textContent=c.title;
 el('spu08-graf').innerHTML=graf08(c.data,c.type,c.unit);
 el('spu08-tabell').innerHTML=tabell08(c.data,c.unit);
 el('spu08-merknad').textContent=c.note;
 el('spu08-kilde').textContent='Primærkilde ['+c.ref+']';el('spu08-kilde').href='#'+c.ref.toLowerCase();
 el('spu08-csv').onclick=()=>lastNedTekst(csv08(['År eller kategori','Verdi','Enhet','Kilde-ID','Status'],c.data.map(r=>[r.label,r.value,c.unit,c.ref,c.note])),'norsk-okonomi-del08-'+mode+'.csv');
}
const spuPresets08={A:[3,1.5,6,0],B:[1,1.5,6,0],C:[3,3,6,0],D:[3,1.5,6,25],E:[3,1.5,10,0],F:[1.5,2.5,10,25]};
let spuModel08=[];
function beregn08(){
 const r=Number(el('spu08-r').value)/100,g=Number(el('spu08-g').value)/100,d=Number(el('spu08-d').value)/100,shock=Number(el('spu08-s').value)/100;
 ['r','g','d','s'].forEach((key,i)=>{el('spu08-'+key+'-v').textContent=nfmt(Number(el('spu08-'+key).value),1)+' %';});
 let fund=22400*(1-shock),firstHigh=null,firstZero=null;const arr=[];
 for(let year=2027;year<=2100;year++){
   const n=year-2027,start=fund,pet=568.4*Math.pow(1-d,n),uttak=561.7*Math.pow(1+g,n);
   if(firstHigh===null && (start===0 || 100*uttak/start>3))firstHigh=year;
   if(firstZero===null && start<=0)firstZero=year;
   const raw=start*(1+r)+pet-uttak;fund=Math.max(0,raw);
   arr.push({label:String(year),value:fund,year,opening:start,peteroleum:pet,uttak:uttak,unmet:Math.max(0,-raw)});
 }
 spuModel08=arr;
 const a60=arr.find(x=>x.year===2060),a100=arr.find(x=>x.year===2100);
 el('spu08-2060').textContent=nfmt(a60.value,0)+' mrd.';
 el('spu08-2100').textContent=nfmt(a100.value,0)+' mrd.';
 el('spu08-3p').textContent=firstHigh||'Ingen t.o.m. 2100';
 el('spu08-scenariograf').innerHTML=graf08(arr.filter((v,i)=>i%3===0||i===arr.length-1),'line','mrd. modellkroner');
 const s=[2027,2030,2040,2050,2060,2070,2100].map(year=>arr.find(r=>r.year===year));
 el('spu08-modelltabell').innerHTML='<table><thead><tr><th>År</th><th>Fond utgang, mrd.</th><th>Petroleum, mrd.</th><th>Kontantuttak, mrd.</th></tr></thead><tbody>'+s.map(a=>`<tr><td>${a.year}</td><td>${nfmt(a.value,0)}</td><td>${nfmt(a.peteroleum,1)}</td><td>${nfmt(a.uttak,1)}</td></tr>`).join('')+'</tbody></table>'+(firstZero?'<p class="spu08-note">Første år med teknisk nullsaldo ved inngangen: '+firstZero+'. Modellen registrerer ikke det fullstendige udekkede finansieringsbehovet i øvrige statsfinanser.</p>':'');
 el('spu08-modellcsv').onclick=()=>lastNedTekst(csv08(['År','Fond ved inngang mrd.','Petroleum mrd.','Kontantuttak mrd.','Fond ved utgang mrd.','Udekket beløp mrd.','Modelltype'],arr.map(x=>[x.year,x.opening.toFixed(3),x.peteroleum.toFixed(3),x.uttak.toFixed(3),x.value.toFixed(3),x.unmet.toFixed(3),'D – illustrasjon, ikke prognose'])),'norsk-okonomi-del08-eget-scenario.csv');
}
el('spu08-scenario').addEventListener('change',()=>{const key=el('spu08-scenario').value,params=spuPresets08[key];if(params){['r','g','d','s'].forEach((id,i)=>el('spu08-'+id).value=params[i]);}beregn08();});
['r','g','d','s'].forEach(id=>el('spu08-'+id).addEventListener('input',()=>{el('spu08-scenario').value='egen';beregn08();}));
el('spu08-valg').addEventListener('change',oppdater08);
oppdater08();beregn08();
'''
# Important JS strings should contain '\uFEFF' escape literal and '\r\n' escape literal; literal control chars would break JS. Convert escaped pairs back to JS escape notation if necessary.
# The raw-string is authored with double slashes for Python literal conservation; JS should evaluate code points only when invoked.
js=js.replace('\\uFEFF','\\uFEFF').replace('\\r\\n','\\r\\n')
anchor='oppdaterUtvidetLandpanel();oppdaterFigur();oppdaterLandpanel();oppdaterBnpPanel();oppdaterFond();oppdaterBolig();oppdaterHypoteser();oppdaterEvidens();highlightTOC();'
assert anchor in h
h=h.replace(anchor,js+'\n'+anchor)
# update 08 fav link in hero and old 06 file link
assert '@@ARTIKKEL@@' in h
# static page meta metadata and OpenGraph date
h=h.replace('"version":"0.9.0"', '"version":"1.0.0"')
t.write_text(h,'utf-8')
print('Patched build engine, master and source template for report 08')
