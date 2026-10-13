from pathlib import Path
import re
R=Path('/mnt/data/_arbeid_norsk_080')
p=R/'kildekode'/'bygg_publisering.py'
s=p.read_text('utf-8')
s=s.replace("VERSION = 'v0.7.0'","VERSION = 'v0.8.0'")
s=s.replace("assert len(sources)==92, f'forventet 92 kilder, fant {len(sources)}'","assert len(sources)==112, f'forventet 112 kilder, fant {len(sources)}'")
s=s.replace("'rapportversjon':'0.7.0'","'rapportversjon':'0.8.0'")
s=s.replace("for traad in ('02','03','04','05'):","for traad in ('02','03','04','05','06'):")
s=s.replace("'16-forskningstrad-05-entreprenorskap-skalering-og-unges-arbeidsmarked'))})","'16-forskningstrad-05-entreprenorskap-skalering-og-unges-arbeidsmarked' if traad=='05' else '17-forskningstrad-06-skatt-eierskap-kapitalmobilitet-og-utflytting'))})")
s=s.replace('assert len(hypotheses)==55,','assert len(hypotheses)==67,')
s=s.replace("+ json.loads((ROOT/'data'/'evidensregister_05.json').read_text('utf-8'))","+ json.loads((ROOT/'data'/'evidensregister_05.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_06.json').read_text('utf-8'))")
s=s.replace('assert len(evidence)==130,','assert len(evidence)==164,')
needle="with (DATA/'observasjoner.csv').open('w',encoding='utf-8-sig',newline='') as f:"
assert needle in s
new='''# Tråd 06: separate populasjoner, registre og skatteforslag; aldri likestill latent gevinst med realkapitalflukt.
FLYT06=json.loads((ROOT/'data'/'utflyttere_formuende_06.json').read_text('utf-8'))
EXIT06=json.loads((ROOT/'data'/'utflyttingsskatt_latent_06.json').read_text('utf-8'))
SAT06=json.loads((ROOT/'data'/'formueskatt_sats_06.json').read_text('utf-8'))
NOU06=json.loads((ROOT/'data'/'skattekommisjon_scenario_06.json').read_text('utf-8'))
HOVED06=json.loads((ROOT/'data'/'hovedindikatorer_06.json').read_text('utf-8'))
for r in FLYT06:
    put('utflytting_formuende_06','Eierskap og skatt','Registrert utflytting i utvalgt formuespopulasjon',r['aar'],'Utvalg 3 565 personer',r['utflyttere_antal'],'personer','K97','NOU tabell 3.2 / administrativt utvalg','Ikke alle utflyttere og ikke skatteindusert kausalt antall')
    put('innflytting_formuende_06','Eierskap og skatt','Registrert innflytting i utvalgt formuespopulasjon',r['aar'],'Utvalg 3 565 personer',r['innflyttere_antal'],'personer','K97','NOU tabell 3.3 / administrativt utvalg','Avgrenset utvalg; forskjellig flytteår')
    put('formuesskatt_utflyttede_06','Eierskap og skatt','Formuesskatt betalt foregående år av utflyttere',r['aar'],'Utvalg 3 565 personer',r['formuesskatt_forrige_aar_mill_kr'],'mill. kr','K97','NOU tabell 3.2','Historisk skatt på personer som flyttet, IKKE kausalt fremtidig skattetap')
for r in EXIT06:
    put('utflyttingsskatt_saker_06','Eierskap og skatt','Antall utflyttingsskattesaker',r['aar'],'Skattedirektoratets utflyttingsskattesaker',r['antall_saker'],'saker','K97','NOU tabell 3.4','Skattedata ikke samme populasjon som flytteutvalget')
    put('latent_gevinst_06','Eierskap og skatt','Fastsatt latent gevinst i utflyttingsskattesaker',r['aar'],'Skattedirektoratets utflyttingsskattesaker',r['latent_gevinst_mill_kr'],'mill. kr','K97','NOU tabell 3.4','Latent gevinst er IKKE kapital som er flyttet, skattebetaling eller reelt norsk investeringstap')
for r in SAT06:
    put('formelle_formueskattesatser_06','Skatt','Illustrert effektiv marginalsats etter formell rabatt',2026,r['eiendel'],r['effektiv_sats_trinn1_prosent'],'prosent verdigrunnlag, trinn 1','K93','Vedtak 2026, beregnet','Før bunnfradrag, gjeld og avvik mellom skattemessig verdsetting og markedsverdi')
    put('formelle_formueskattesatser2_06','Skatt','Illustrert effektiv marginalsats etter formell rabatt',2026,r['eiendel'],r['effektiv_sats_trinn2_prosent'],'prosent verdigrunnlag, trinn 2','K93','Vedtak 2026, beregnet','Før bunnfradrag, gjeld og avvik mellom skattemessig verdsetting og markedsverdi')
for r in NOU06:
    put('nou_formuesskatt_scenario_06','Skattereform','Anslått statisk provenyendring i NOU-skattesats',2026,f"Utredet sats {r['sats_prosent']} %",r['anslatt_statisk_provenyendring_mrd_kr'],'mrd. kr','K98','NOU 2026:9, scenarioberegning','Forslag, IKKE vedtatt; ingen modellering av atferd eller BNP')
for r in HOVED06:
    put('indikator_06','Eierskap og skatt',r['indikator'],r['periode'],r['populasjon'],r['verdi'],r['enhet'],r['kilde_id'],r['status'],r['merknad'])

'''
s=s.replace(needle,new+needle)
# Add human-readable mathematical alternatives for report 06.
s=s.replace("\n]\nix=[0]", "\n    'Utbytteskatt + selskapsskatt: 1 − (1 − 0,22) × (1 − 0,3784) = 51,5152 %. Gjelder fullt utdelt overskudd uten skjerming.',\n    'Skattepliktig aksjeverdi = 10 mill. × 0,8 = 8 mill. kr.\\nFormuesskatt = (8 mill. − 1,9 mill.) × 1 % = 61 000 kr.\\nBrutto utbytte uten skjerming = 61 000 / 0,6216 ≈ 98 134 kr.\\nOverskudd før selskapsskatt = 98 134 / 0,78 ≈ 125 813 kr.'\n]\nix=[0]",1)
# Add new JSON bindings by locating the end of the substitutions dict.
bindings = ''.join(f"  '@@{key}@@':json.dumps({value},ensure_ascii=False).replace('<', '\\\\u003c'),\n" for key,value in [('FLYT06','FLYT06'),('EXIT06','EXIT06'),('SAT06','SAT06'),('NOU06','NOU06')])
# Explicit insertion avoids ambiguous Python escaping of JSON escape sequences.
pos = s.index("\n}\nfor key,val in subst.items():")
s=s[:pos]+"\n"+bindings.rstrip("\n")+s[pos:]
assert "'@@FLYT06@@'" in s
s=s.replace("(' *_01.*','*_02.*'", "(' *_01.*','*_02.*'") if False else s
s=s.replace("(' *_01.*'", "('*_01.*'") if False else s
s=s.replace("(' *_01.*'", "('*_01.*'") if False else s
s=s.replace("(' *_01.*'", "('*_01.*'") if False else s
s=s.replace("(' *_01.*'", "('*_01.*'") if False else s
s=s.replace("(' *_01.*'", "('*_01.*'") if False else s
s=s.replace("(' *_01.*'", "('*_01.*'") if False else s
s=s.replace("for pattern in ('*_01.*','*_02.*','*_03.*','*_04.*','*_05.*'):","for pattern in ('*_01.*','*_02.*','*_03.*','*_04.*','*_05.*','*_06.*'):")
s=s.replace("copy_if_different(ROOT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md',SITE/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md')", "copy_if_different(ROOT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md',SITE/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md')\ncopy_if_different(ROOT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md',SITE/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')")
s=s.replace("copy_if_different(ROOT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md',OUT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md')", "copy_if_different(ROOT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md',OUT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md')\ncopy_if_different(ROOT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md',OUT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')")
# refresh manifest (exclude manifest itself) before zip. Note README includes scheme references.
s=s.replace("zipf=OUT/f'Norsk_Okonomi_Nettside_Publisering_{DATE}_{VERSION}.zip'", '''# Oppdater SHA-256-manifestet før publiseringsarkivet pakkes, for hver fil som skal med.
import hashlib
manifest=[]
for file in sorted(SITE.rglob('*')):
    if file.is_file() and file.name != 'MANIFEST-SHA256.txt':
        manifest.append(f"{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.relative_to(SITE).as_posix()}")
(SITE/'MANIFEST-SHA256.txt').write_text('\\n'.join(manifest)+'\\n',encoding='utf-8')
zipf=OUT/f'Norsk_Okonomi_Nettside_Publisering_{DATE}_{VERSION}.zip' ''')
p.write_text(s,'utf-8')

q=R/'kildekode'/'mal_nettside.html'
h=q.read_text('utf-8')
h=h.replace('0.7.0','0.8.0')
h=h.replace('href="#entreprenorskap05">Entreprenørskap 05</a>', 'href="#entreprenorskap05">Entreprenørskap 05</a><a href="#skatt06">Skatt 06</a>')
# Add CSS immediately ahead of close style.
css='''
/* Forskningstråd 06 – skatt, registrert flytting, latente gevinster og forslag måles separat */
.tax06-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:18px}
.tax06-card{border:1px solid var(--line);background:var(--card);padding:16px;border-radius:8px}
.tax06-card b{display:block;font:600 28px Georgia,serif;margin:6px 0;color:var(--main2)}
.tax06-card span{font-size:12px;line-height:1.6;color:var(--muted)}
.tax06-grid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,.85fr);gap:16px;margin-bottom:16px}
.tax06-input{width:100%;accent-color:var(--main)}
.tax06-panel{padding:17px;border:1px solid var(--line);background:var(--card);border-radius:8px}
.tax06-control{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:12px}
.tax06-control select{padding:10px;max-width:100%;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:5px}
.tax06-graph svg{display:block;width:100%;height:auto}
.tax06-tabell{overflow:auto;max-height:340px}
.tax06-calcout{font-size:13px;line-height:1.85;padding:13px;background:var(--soft);border-left:3px solid var(--main)}
.tax06-warning{font-size:12px;line-height:1.7;color:var(--muted)}
@media(max-width:950px){.tax06-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.tax06-grid{grid-template-columns:1fr}}
@media(max-width:510px){.tax06-card{padding:11px}.tax06-card b{font-size:22px}.tax06-control{display:block}.tax06-control select{display:block;width:100%;margin-top:7px}}
'''
assert '</style>' in h
h=h.replace('</style>', css+'</style>',1)
section='''
<section class="section" id="skatt06">
 <div class="section-heading"><div><p class="eyebrow-dark">06 / Eierskap og skatter</p><h2>Hvor stor er skattedrevet kapitalflukt?</h2></div>
 <p class="section-note">Kildebasert gjennomgang av rettsregler, folkeregistrert flytting, latent gevinst og forslag til skattereform. Figurenes forskjellige måleenheter kan ikke summeres.</p></div>
 <div class="tax06-kpis">
  <div class="tax06-card"><span>Formuesskatt 2026, nedre marginaltrinn</span><b>1,0 %</b><span>På skattepliktig nettoformue over 1,9 mill. kr <a href="#k93">[K93]</a></span></div>
  <div class="tax06-card"><span>Registrerte utflyttere 2021–2025</span><b>141</b><span>Avgrenset utvalg på 3 565 formuende personer; ikke kausalt anslag <a href="#k97">[K97]</a></span></div>
  <div class="tax06-card"><span>Fastsatt latent gevinst 2022</span><b>133,8 mrd.</b><span>Utflyttingsskattesaker; ikke faktisk overført kapital <a href="#k97">[K97]</a></span></div>
  <div class="tax06-card"><span>Reformsatser vurdert i NOU 2026: 9</span><b>0,25–0,75 %</b><span>Forslag og statiske scenarier, ikke vedtatte satser <a href="#k98">[K98]</a></span></div>
 </div>
 <div class="tax06-grid">
  <div class="tax06-panel">
   <div class="tax06-control"><label for="tax06-valg" class="small-label">Vis dataserie</label><select id="tax06-valg">
    <option value="flytting">Registrert flytting i definert formuesgruppe, 2021–2025</option>
    <option value="latent">Latente gevinster i utflyttingsskattesaker, 2020–2024</option>
    <option value="satser">Formelle verdsettingsrabatter og marginalskatt, 2026</option>
    <option value="nou">Skattekommisjonens statiske provenyscenarier, 2026</option>
   </select></div>
   <h3 id="tax06-tittel">Registrert flytting</h3>
   <div id="tax06-graf" class="tax06-graph" role="img" aria-label="Figur med tabell under"></div>
   <p id="tax06-merknad" class="tax06-warning" aria-live="polite"></p>
   <p class="tax06-warning"><a id="tax06-kilde" href="#k97">Se kilde K97</a> · <a href="#rapport-17-forskningstrad-06-skatt-eierskap-kapitalmobilitet-og-utflytting">Hele analysen i kapittel 17</a></p>
  </div>
  <div class="tax06-panel">
   <h3>Observasjoner og kildedefinisjoner</h3>
   <div id="tax06-tabell" class="data-box tax06-tabell"></div>
   <button type="button" class="pill-button" id="tax06-csv">Last ned viste data (CSV)</button>
   <p class="tax06-warning">Utvalget av personflyttere har annen definisjon og referanseperiode enn utflyttingsskattesakene. Latent gevinst er en skattemessig beregning, ikke strøm av realkapital.</p>
  </div>
 </div>
 <div class="tax06-grid">
   <div class="tax06-panel">
    <h3>Illustrasjon: formuesskatt på aksjeformue</h3>
    <label for="tax06-verdi" class="small-label">Verdsettelsesgrunnlag for aksjer før formell rabatt: <output id="tax06-verdi-tekst">10 mill. kr</output></label>
    <input type="range" class="tax06-input" id="tax06-verdi" min="0" max="100" step="1" value="10" aria-label="Aksjeformue i millioner kroner">
    <div id="tax06-beregning" class="tax06-calcout" aria-live="polite"></div>
    <p class="tax06-warning">Forenklet enslig aksjonær, bare aksjer, ingen gjeld, 20 % formell rabatt, 2026-satser, utbytteskatt 37,84 % over skjerming, 22 % selskapsskatt. Skattemessig verdsettelse av unoterte aksjer kan avvike vesentlig fra markedsverdi. Dette er ikke et individuelt skattevedtak eller prognose.</p>
   </div>
   <div class="tax06-panel">
    <h3>Hva forskning ennå ikke har vist</h3>
    <p>Det er dokumentert at skatter kan endre bostedsvalg. Det er <strong>ikke</strong> dermed dokumentert at all verdi i utflyttingsskattesaker forsvinner fra norsk økonomi, eller at alle eierstyrte investeringer faller.</p>
    <p>Den nordiske AER-studien, norsk analyse av 2021–2024-reformene og en langsiktig modellstudie gir ulike effektmål og analysehorisonter. Disse holdes eksplisitt adskilt. <a href="#k102">[K102]</a> <a href="#k103">[K103]</a> <a href="#k104">[K104]</a></p>
    <p class="tax06-warning"><a href="06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md" download>Last ned delrapport 06 (Markdown)</a> · <a href="data/evidensregister_06.csv" download>Evidens 06</a> · <a href="data/hypoteseregister_06.csv" download>Hypoteser 06</a> · <a href="data/proveniens_06.json" download>Dataproveniens</a></p>
   </div>
 </div>
</section>

'''
assert '<section class="section" id="stresstest">' in h
h=h.replace('<section class="section" id="stresstest">',section+'<section class="section" id="stresstest">',1)
h=h.replace('<a href="data/evidensregister_05.csv" download>CSV tråd 05</a>','<a href="data/evidensregister_05.csv" download>CSV tråd 05</a><a href="data/evidensregister_06.csv" download>CSV tråd 06</a><a href="06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md" download>Delrapport 06</a>')
h=h.replace('Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.7.0.md','Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.8.0.md')
assert 'const STARTUP_NYUTD05 = @@NYUTD05@@;' in h
h=h.replace('const STARTUP_NYUTD05 = @@NYUTD05@@;', '''const STARTUP_NYUTD05 = @@NYUTD05@@;
const TAX_FLYT06 = @@FLYT06@@;
const TAX_EXIT06 = @@EXIT06@@;
const TAX_SAT06 = @@SAT06@@;
const TAX_NOU06 = @@NOU06@@;''')
script='''
// Tråd 06. Kategorier fra ulike registre og ulike rettslige statuser kan ikke summeres.
function tegnSkatt06(){
 const mode=el('tax06-valg').value;
 let title='',note='',unit='',key='K97',data=[],headers=[],rows=[];
 if(mode==='flytting'){
  title='Flyttinger i utvalg av 3 565 formuende, 2021–2025';unit='personer';key='K97';
  data=TAX_FLYT06.map(r=>({label:String(r.aar),value:Number(r.utflyttere_antal),other:Number(r.innflyttere_antal)}));
  headers=['År','Utflyttere','Innflyttere'];rows=TAX_FLYT06.map(r=>[r.aar,r.utflyttere_antal,r.innflyttere_antal]);
  note='Utvalg fra NOU 2026: 9, tabell 3.2–3.3. 141 registrerte utflyttere og 46 innflyttere. IKKE samlet migrasjon blant rike, IKKE kausalt antall skatteutflyttere. Andre populasjoner og datoer kan gi andre tall.';
 }else if(mode==='latent'){
  title='Latente gevinster, utflyttingsskattesaker';unit='mrd. kr, urealisert';key='K97';
  data=TAX_EXIT06.map(r=>({label:String(r.aar),value:Number(r.latent_gevinst_mill_kr)/1000}));
  headers=['År','Saker','Fastsatt latent gevinst (mill. kr)'];rows=TAX_EXIT06.map(r=>[r.aar,r.antall_saker,r.latent_gevinst_mill_kr]);
  note='NOU tabell 3.4. Beløp gjelder fastsatte latente gevinster; ingen av søylene viser faktiske kapitaltransaksjoner ut av Norge, skattebetaling eller bedrifter som flyttet.';
 }else if(mode==='satser'){
  title='Verdsetting og sats på formell beregningsverdi, 2026';unit='% før bunnfradrag';key='K93';
  data=TAX_SAT06.map(r=>({label:r.eiendel,value:Number(r.effektiv_sats_trinn1_prosent),other:Number(r.effektiv_sats_trinn2_prosent)}));
  headers=['Formuesobjekt','Formell rabatt (%)','Nedre marginaltrinn (%)','Øvre marginaltrinn (%)'];rows=TAX_SAT06.map(r=>[r.eiendel,r.formell_rabatt_prosent,r.effektiv_sats_trinn1_prosent,r.effektiv_sats_trinn2_prosent]);
  note='Vedtak 2026. Regnestykket multipliserer bare formell verdsettingsandel og marginalsats. Faktisk skatt påvirkes av bunnfradrag, gjeld, særregler og skattemessig verdsettelse; dette er ikke en beregning av effektiv skatt for alle skattytere.';
 }else{
  title='Statiske provenyendringer i Skattekommisjonens reformscenarier';unit='mrd. kr lavere årlig proveny';key='K98';
  data=TAX_NOU06.map(r=>({label:String(r.sats_prosent).replace('.',',')+' %',value:Math.abs(Number(r.anslatt_statisk_provenyendring_mrd_kr))}));
  headers=['Foreslått enhetssats (%)','Anslått statisk provenyendring (mrd. kr)'];rows=TAX_NOU06.map(r=>[r.sats_prosent,r.anslatt_statisk_provenyendring_mrd_kr]);
  note='NOU 2026: 9, tabell 6.2. Foreslåtte satser for utvidet skattegrunnlag, bunnfradrag 2 mill. kr og ekstra boligfradrag 7 mill. kr. Tallene er statiske budsjettscenarier, ikke vedtatt rett eller estimert BNP-effekt.';
 }
 el('tax06-tittel').textContent=title;
 el('tax06-merknad').textContent=note+' Enhet: '+unit+'.';
 el('tax06-kilde').textContent='Se kilde ['+key+']';el('tax06-kilde').href='#'+key.toLowerCase();
 const W=760,H=323,L=64,R=22,T=42,B=80,M=Math.max(1,...data.map(r=>Math.max(r.value,r.other??0)))*1.14;
 const cw=(W-L-R)/data.length,bar=Math.min(58,cw*(mode==='satser'||mode==='flytting'?.25:.5));
 const sy=v=>H-B-(v/M)*(H-T-B);
 let svg=`<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(title)}. Tabell med tall følger.">`;
 for(let k=0;k<=4;k++){const v=M*k/4,y=sy(v);svg+=`<line x1="${L}" x2="${W-R}" y1="${y}" y2="${y}" stroke="var(--line)"/><text x="${L-7}" y="${y+4}" text-anchor="end" font-size="11" fill="var(--muted)">${esc(nfmt(v,v>=100?0:1))}</text>`;}
 if(data.some(r=>r.other!==undefined))svg+=`<rect x="${L+4}" y="6" width="11" height="11" fill="var(--main)"/><text x="${L+22}" y="16" fill="var(--ink2)" font-size="12">${mode==='flytting'?'Utflytting':'Nedre trinn'}</text><rect x="${L+166}" y="6" width="11" height="11" fill="#bc854b"/><text x="${L+185}" y="16" fill="var(--ink2)" font-size="12">${mode==='flytting'?'Innflytting':'Øvre trinn'}</text>`;
 data.forEach((r,i)=>{
   const cx=L+cw*(i+.5),w=r.other===undefined?bar*1.6:bar;
   const col=r.other===undefined?[{x:cx-w/2,v:r.value,c:'var(--main)'}]:[{x:cx-w-1,v:r.value,c:'var(--main)'},{x:cx+1,v:r.other,c:'#bc854b'}];
   col.forEach(a=>{const y=sy(a.v),height=Math.max(2,H-B-y);svg+=`<rect x="${a.x}" y="${y}" width="${w}" height="${height}" rx="2" fill="${a.c}"><title>${esc(r.label)}: ${nfmt(a.v,a.v>=50?0:2)} ${esc(unit)}</title></rect>`;});
   svg+=`<text x="${cx}" y="${H-B+24}" text-anchor="middle" font-size="${data.length>6?10:12}" fill="var(--muted)">${esc(r.label.length>16?r.label.slice(0,15)+'…':r.label)}</text>`;
 });
 svg+='</svg>';el('tax06-graf').innerHTML=svg;
 el('tax06-tabell').innerHTML='<table><thead><tr>'+headers.map(k=>'<th>'+esc(k)+'</th>').join('')+'</tr></thead><tbody>'+rows.map(r=>'<tr>'+r.map(v=>'<td>'+esc(String(v))+'</td>').join('')+'</tr>').join('')+'</tbody></table>';
 const csvQ=v=>'"'+String(v).replace(/"/g,'""')+'"';
 const csv='\\uFEFF'+[headers,...rows].map(r=>r.map(csvQ).join(';')).join('\\r\\n')+'\\r\\n';
 el('tax06-csv').onclick=()=>lastNedTekst(csv,'norsk-okonomi-del06-'+mode+'.csv');
}
function beregnSkatt06(){
 const market=Number(el('tax06-verdi').value)*1e6, taxable=market*.8;
 const t1=Math.max(0,Math.min(taxable,21.5e6)-1.9e6)*.01;
 const t2=Math.max(0,taxable-21.5e6)*.011;
 const total=t1+t2,div=total/.6216,pre=div/.78;
 el('tax06-verdi-tekst').textContent=nfmt(market/1e6,0)+' mill. kr';
 el('tax06-beregning').innerHTML='<strong>Skattemessig aksjeformue etter formell 20 % rabatt:</strong> '+nfmt(taxable,0)+' kr<br><strong>Beregnet formuesskatt:</strong> '+nfmt(total,0)+' kr<br><strong>Illustrativt brutto utbytte ved full finansiering fra utbytte:</strong> '+nfmt(div,0)+' kr<br><strong>Illustrert nødvendig selskapoverskudd før 22 % selskapsskatt:</strong> '+nfmt(pre,0)+' kr';
}
el('tax06-valg').addEventListener('change',tegnSkatt06);
el('tax06-verdi').addEventListener('input',beregnSkatt06);
tegnSkatt06();beregnSkatt06();
'''
assert 'tegnStartups05();' in h
h=h.replace('tegnStartups05();\n\noppdaterUtvidetLandpanel()', 'tegnStartups05();\n'+script+'\noppdaterUtvidetLandpanel()')
assert 'function tegnSkatt06' in h
q.write_text(h,'utf-8')
print('Oppdaterte byggekode og nettmal 06:',len(s),len(h))
