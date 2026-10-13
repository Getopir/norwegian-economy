#!/usr/bin/env python3
"""Legg til publiserbar, responsiv tråd 05 samt data i eksisterende nettsidemal."""
from pathlib import Path
R=Path(__file__).resolve().parent
path=R/'kildekode'/'mal_nettside.html'
s=path.read_text('utf8')
s=s.replace('0.6.0','0.7.0').replace('entreprenørskap, generasjoner, demografi','entreprenørskap, generasjoner, demografi')
s=s.replace('<a href="#generasjonsstudie">Generasjoner 04</a>', '<a href="#generasjonsstudie">Generasjoner 04</a><a href="#entreprenorskap05">Entreprenørskap 05</a>')
s=s.replace('fra tråd 01–04','fra tråd 01–05')
s=s.replace('<a href="data/evidensregister_04.csv" download>CSV tråd 04</a>', '<a href="data/evidensregister_04.csv" download>CSV tråd 04</a><a href="data/evidensregister_05.csv" download>CSV tråd 05</a><a href="05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md" download>Delrapport 05</a>')
# semantic metadata, include entrepreneurs in description
s=s.replace('boligformue, generasjoner, demografi og reformhypoteser','boligformue, generasjoner, entreprenørskap, ungdomsarbeid og reformhypoteser')
newcss='''
/* Forskningstråd 05 — interaktive primærkilder, ingen nettilkobling nødvendig */
.startup05-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-bottom:18px}
.startup05-kpi{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:17px;min-height:126px}
.startup05-kpi b{font-family:Georgia,serif;display:block;font-size:29px;font-weight:600;color:var(--main2);margin:5px 0}
.startup05-kpi span{font-size:12px;color:var(--muted);line-height:1.5;display:block}
.startup05-row{display:grid;grid-template-columns:1.35fr .8fr;gap:16px}
.startup05-controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:15px}
.startup05-controls label{font-size:12px;font-weight:700;color:var(--ink2)}
.startup05-controls select{min-width:235px;max-width:100%;padding:10px;border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:5px}
.startup05-chart{min-height:250px;overflow:auto}
.startup05-chart svg{display:block;width:100%;height:auto}
.startup05-datatable{max-height:350px;overflow:auto}
.startup05-note{font-size:12px;line-height:1.7;color:var(--muted);margin-top:11px}
.startup05-method{background:var(--soft);border-left:3px solid var(--main);padding:12px 16px;margin-top:18px;font-size:13px;color:var(--ink2)}
@media(max-width:1000px){.startup05-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.startup05-row{grid-template-columns:1fr}}
@media(max-width:520px){.startup05-kpis{grid-template-columns:1fr 1fr}.startup05-kpi{min-height:138px;padding:13px}.startup05-kpi b{font-size:24px}.startup05-controls{display:block}.startup05-controls select{width:100%;margin-top:7px}}
@media print{.startup05-row{grid-template-columns:1fr}.startup05-controls{display:none}}
'''
assert '</style>' in s
s=s.replace('</style>',newcss+'</style>',1)
newsection='''
<section class="section" id="entreprenorskap05">
 <div class="section-heading"><div><p class="eyebrow-dark">05 / Entreprenørskap og arbeid</p><h2>Fra etablering til produktive arbeidsplasser</h2></div><p class="section-note">Interaktiv utforsking av publiserte SSB- og NVCA/Menon-data. Velg indikator, kontroller populasjon og last ned eksakt tabellgrunnlag. Figurenes størrelser kan ikke kobles som om de er samme kohort.</p></div>
 <div class="startup05-kpis" aria-label="Fire viktige funn fra delrapport 05">
  <div class="startup05-kpi"><span>Nyregistrerte foretak, 2026-K2</span><b>17 052</b><span>SSB, kvartalstabell <a href="#k77">[K77]</a></span></div>
  <div class="startup05-kpi"><span>«Scaleups» etter 9 år</span><b>2–3 %</b><span>Selektert gruppe lovende startups, SSB <a href="#k79">[K79]</a></span></div>
  <div class="startup05-kpi"><span>Tidligfasekapital i Norge, 2025</span><b>170 mill. €</b><span>Avrundet bransjerapport, NVCA/Menon <a href="#k82">[K82]</a></span></div>
  <div class="startup05-kpi"><span>Unge utenfor jobb og utdanning, 2025</span><b>10,1 %</b><span>15–29 år, registerbasert NEET, SSB <a href="#k86">[K86]</a></span></div>
 </div>
 <div class="startup05-row">
  <div class="panel">
   <div class="startup05-controls"><label for="startup05-valg">Utforsk en datakategori</label>
    <select id="startup05-valg"><option value="registrering">Nye foretak, kvartal 2024–2026</option><option value="venture">Tidligfaseinvesteringer 2025, Norden</option><option value="vekst">Lovende startups: vekst og scaleup</option><option value="alder">Personlige etablerere etter alder</option><option value="ledig">Ungdomsledighet 15–24 år</option><option value="yrkesmatch">Nyutdannede i akademiske yrker</option></select>
   </div>
   <h3 id="startup05-tittel">Nye foretak etter kvartal</h3>
   <div id="startup05-graf" class="startup05-chart" role="img" aria-label="Observasjoner fra valgt dataserie"></div>
   <p class="startup05-note" id="startup05-forklaring" aria-live="polite"></p>
   <p class="startup05-note"><a id="startup05-kilde" href="#k77">Se referanse [K77]</a> · <a href="#rapport">Les forskningsområde 05 og metode i full rapport</a></p>
  </div>
  <div class="panel">
   <h3>Alle viste datapunkter</h3>
   <div id="startup05-tabell" class="data-box startup05-datatable"></div>
   <p class="startup05-note">Tabellen er fasit for valgt figur. Teksten nedenfor dokumenterer nevner, populasjon og begrensninger.</p>
   <button type="button" class="pill-button" id="startup05-csv">Last ned synlige verdier (CSV)</button>
   <div class="startup05-method"><strong>Forskningsetisk avgrensning.</strong> Registrerte foretak, personlig etablering, valgt oppstartsforløp, kapital, AKU og NEET måler ulike fenomener. Omtrentlig 2–3 % scaleup er ikke nasjonal niårs-overlevelse. Årsaksvirkninger av skatt og kapitaltilgang er ennå ikke identifisert.</div>
  </div>
 </div>
 <p class="chart-note"><a href="05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md" download>Last ned delrapport 05</a> · <a href="data/hypoteseregister_05.csv" download>Hypoteser, CSV</a> · <a href="data/evidensregister_05.csv" download>Evidens, CSV</a> · <a href="data/proveniens_05.json" download>Dataproveniens, JSON</a>. Figurenes tall er også gjengitt i den kanoniske Markdown-rapporten.</p>
</section>
'''
assert '<section class="section" id="stresstest">' in s
s=s.replace('<section class="section" id="stresstest">',newsection+'\n<section class="section" id="stresstest">',1)
const='''const STARTUP_FORETAK05 = @@FORETAK05@@;
const STARTUP_VC05 = @@VENTURE05@@;
const STARTUP_ALDER05 = @@ETABALDER05@@;
const STARTUP_VEKST05 = @@VEKST05@@;
const STARTUP_LEDIG05 = @@LEDIG05@@;
const STARTUP_NYUTD05 = @@NYUTD05@@;
'''
assert 'const KOHORT04 = @@KOHORT04@@;' in s
s=s.replace('const KOHORT04 = @@KOHORT04@@;', 'const KOHORT04 = @@KOHORT04@@;\n'+const,1)
render_js=r'''
// Tråd 05: verdier fra eksplisitte datasett. De separate kategoriene sammenslås aldri.
function tegnStartups05(){
 const mode=el('startup05-valg').value;
 let title='',note='',unit='',key='K77',data=[];
 if(mode==='registrering'){
  title='Nyregistrerte foretak per kvartal';unit='foretak';key='K77';
  data=STARTUP_FORETAK05.map(r=>({label:r.periode,value:Number(r.totalt)}));
  note='SSB tabell 08076. Antall nye registreringer per kvartal, ikke antall overlevende arbeidsgiverforetak. Metodeendring fra 2026 må hensyntas.';
 } else if(mode==='venture'){
  title='Investert tidligfasekapital i 2025';unit='millioner euro';key='K82';
  data=STARTUP_VC05.map(r=>({label:r.land,value:Number(r.mill_eur)}));
  note='NVCA/Menon: avrundede investeringer i selskaper etter porteføljeselskapets hjemland, slik bransjerapporten oppgir dem. Ikke BNP-justert; fondsdatadekning og investordefinisjon setter grenser for sammenligningen.';
 } else if(mode==='vekst'){
  title='Lovende startups etter 3, 6 og 9 år';unit='prosent av utvalgt startuppopulasjon';key='K79';
  data=STARTUP_VEKST05.map(r=>({label:r.aar_etter+' år',value:Number(r.fortsatt_vekst_prosent),other:Number(r.blitt_scaleup_prosent)}));
  note='SSB forløpsanalyse: primærserie er fortsatt vekst; andelen scaleups er inkludert i og IKKE lagt til primærserien. Omtrentlig for selekterte lovende oppstartsforetak — ikke overlevelse blant alle nyregistrerte.';
 } else if(mode==='alder'){
  title='Aldersfordeling blant personlige etablerere, 2024';unit='prosent av personlige etablerere';key='K81';
  data=STARTUP_ALDER05.map(r=>({label:r.gruppe,value:Number(r.andel_prosent)}));
  note='SSB: 64 622 personlige etablerere totalt. Foreløpige anslag og avrundet aldersfordeling; dette er ikke foretak eller aldersspesifikk etableringsrate.';
 } else if(mode==='ledig'){
  title='AKU-arbeidsledighet 15–24 år';unit='prosent av arbeidsstyrken';key='K87';
  data=STARTUP_LEDIG05.map(r=>({label:String(r.aar),value:Number(r.ledighet_15_24_prosent)}));
  note='SSBs AKU-ledighet for unge. Nevner er arbeidsstyrken 15–24 år; skal ikke settes lik eller summeres med register-NEET for 15–29-åringer.';
 } else {
  title='Nyutdannede med høyere utdanning i akademiske yrker m.m.';unit='prosent av høyere utdannede nyutdannede';key='K88';
  data=STARTUP_NYUTD05.map(r=>({label:String(r.aar),value:Number(r.andel_akademiske_yrker_prosent)}));
  note='SSB/AKU figur 4. Andelen i yrkesgrupper med akademisk innhold, ikke samlet sysselsetting. Tidsserie her viser bare 2024/2025 med eksplisitt kildegrunnlag.';
 }
 el('startup05-tittel').textContent=title;
 el('startup05-forklaring').textContent=note+' Enhet: '+unit+'.';
 el('startup05-kilde').textContent='Kilde ['+key+']';el('startup05-kilde').href='#'+key.toLowerCase();
 const max=Math.max(1,...data.map(x=>x.value))*1.13,W=750,H=328,L=65,R=20,T=40,B=65,usable=W-L-R,cw=usable/data.length,bar=Math.min(66,cw*.53);
 const Y=v=>H-B-(v/max)*(H-T-B);
 let svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(title)}. Kilde ${key}.">`;
 for(let tick=0;tick<=4;tick++){const v=max*tick/4,yy=Y(v);svg+=`<line x1="${L}" x2="${W-R}" y1="${yy}" y2="${yy}" stroke="var(--line)"/><text x="${L-8}" y="${yy+4}" text-anchor="end" font-size="11" fill="var(--muted)">${esc(nfmt(v,v>=100?0:1))}</text>`;}
 data.forEach((r,i)=>{
  const cx=L+cw*(i+.5),x=cx-bar/2,y=Y(r.value),h=Math.max(2,H-B-y);
  svg+=`<rect x="${x}" y="${y}" width="${bar}" height="${h}" fill="var(--main)" rx="2"><title>${esc(r.label)}: ${esc(nfmt(r.value,r.value>=100?0:1))} ${esc(unit)}</title></rect>`;
  if(r.other!==undefined){const w=Math.max(6,bar*.39),h2=Math.max(2,H-B-Y(r.other));svg+=`<rect x="${cx+bar*.28}" y="${Y(r.other)}" width="${w}" height="${h2}" fill="#bd8648" rx="2"><title>${esc(r.label)}: ${esc(nfmt(r.other,1))} % ble scaleups</title></rect>`;}
  svg+=`<text x="${cx}" y="${Math.max(17,y-8)}" text-anchor="middle" fill="var(--ink)" font-size="12" font-weight="650">${esc(nfmt(r.value,r.value>=100?0:1))}</text>`;
  svg+=`<text x="${cx}" y="${H-B+21}" text-anchor="middle" fill="var(--muted)" font-size="${r.label.length>11?10:12}">${esc(r.label)}</text>`;
 });
 if(mode==='vekst')svg+=`<rect x="${L+8}" y="5" width="11" height="11" fill="var(--main)"/><text x="${L+26}" y="15" font-size="12" fill="var(--ink)">Fortsatt vekst</text><rect x="${L+150}" y="5" width="11" height="11" fill="#bd8648"/><text x="${L+168}" y="15" font-size="12" fill="var(--ink)">Blitt scaleup (inngår i vekst)</text>`;
 svg+='</svg>';el('startup05-graf').innerHTML=svg;
 el('startup05-tabell').innerHTML=`<table><thead><tr><th>Kategori</th><th>${esc(unit)}</th>${mode==='vekst'?'<th>Scaleup (inngår)</th>':''}</tr></thead><tbody>${data.map(r=>`<tr><td>${esc(r.label)}</td><td>${esc(nfmt(r.value,r.value>=100?0:1))}</td>${mode==='vekst'?`<td>${esc(nfmt(r.other,1))} %</td>`:''}</tr>`).join('')}</tbody></table>`;
 const output=data.map(r=>({kategori:r.label,verdi:r.value,enhet:unit,kilde_id:key,...(mode==='vekst'?{blitt_scaleup_prosent:r.other}:{})}));
 el('startup05-csv').onclick=()=>lastNedTekst(lagCSV(output),'norsk-okonomi-del05-'+mode+'.csv');
}
el('startup05-valg').addEventListener('change',tegnStartups05);
tegnStartups05();
'''
assert 'oppdaterUtvidetLandpanel();oppdaterFigur();' in s
s=s.replace('oppdaterUtvidetLandpanel();oppdaterFigur();',render_js+'\noppdaterUtvidetLandpanel();oppdaterFigur();',1)
path.write_text(s,'utf8');print('nettsidemal bytes',len(s))
