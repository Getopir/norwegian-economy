#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Statisk, tilgjengelig datadashbord for delrapport 07 (HTML/CSS/JS i én fil)."""
from pathlib import Path
import re
R=Path(__file__).resolve().parent
page=R/'kildekode'/'mal_nettside.html'
s=page.read_text('utf8')
assert 'id="offentlig07"' not in s
s=s.replace('0.8.0','0.9.0')
s=s.replace('<a href="#skatt06">Skatt 06</a>','<a href="#skatt06">Skatt 06</a><a href="#offentlig07">Offentlig 07</a>')
s=s.replace('fra tråd 01–05. Filtrer','fra tråd 01–07. Filtrer')
s=s.replace('<a href="data/evidensregister_06.csv" download>CSV tråd 06</a>','<a href="data/evidensregister_06.csv" download>CSV tråd 06</a><a href="data/evidensregister_07.csv" download>CSV tråd 07</a><a href="data/hypoteseregister_07.csv" download>Hypoteser tråd 07</a>')
s=s.replace('<a href="06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md" download>Delrapport 06</a>','<a href="07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md" download>Delrapport 07</a><a href="06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md" download>Delrapport 06</a>')
s=s.replace('const TAX_NOU06 = @@NOU06@@;','''const TAX_NOU06 = @@NOU06@@;
// Nye aggregerte norske datakilder, forskningstråd 07. Tallene finnes også som CSV/JSON.
const OFF_07 = @@OFF07@@;
const COFOG_07 = @@COFOG07@@;
const JOB_07 = @@JOB07@@;
const HOVED_07 = @@HOVED07@@;''')
css=r'''
/* Forskningstråd 07: lesbare grafer og transparent scenariointeraksjon. */
.off07-kpis{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:13px;margin-bottom:18px}
.off07-kpi{padding:20px 19px;border:1px solid var(--line);background:var(--card);border-radius:10px;display:flex;flex-direction:column;min-height:160px;gap:10px}
.off07-kpi span{font-size:12px;color:var(--muted);line-height:1.4}.off07-kpi b{font:500 clamp(24px,2.8vw,35px)/1.14 Georgia,serif;letter-spacing:-.035em;color:var(--ink)}.off07-kpi a{color:var(--main2)}
.off07-grid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(280px,.7fr);gap:17px;margin:17px 0}.off07-grid>.panel{min-width:0}
.off07-graph{min-height:350px;width:100%;margin:12px 0;overflow-x:auto}.off07-graph svg{width:100%;height:auto;display:block}
.off07-note{font-size:13px;color:var(--ink2);line-height:1.56}.off07-note strong{color:var(--ink)}
.off07-inputs{display:grid;gap:13px}.off07-inputs label{display:grid;gap:5px;font-size:13px;color:var(--ink2)}.off07-inputs label strong{color:var(--main2)}
.off07-result{padding:16px 18px;background:var(--soft);border-left:3px solid var(--main);border-radius:4px;margin-top:18px;font-size:14px;line-height:1.68}
.off07-result b{font-family:Georgia,serif;font-size:26px;letter-spacing:-.03em;font-weight:500;display:block;margin-bottom:4px}
@media(max-width:1100px){.off07-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}} 
@media(max-width:760px){.off07-grid{grid-template-columns:1fr}.off07-kpis{grid-template-columns:repeat(2,minmax(0,1fr))}.off07-graph{min-height:260px}}
@media(max-width:420px){.off07-kpis{grid-template-columns:1fr}.off07-kpi{min-height:auto}.off07-graph{min-height:220px}}
'''
assert '</style>' in s
s=s.replace('</style>',css+'</style>')
section=r'''
<section class="section" id="offentlig07">
 <div class="section-heading"><div><p class="eyebrow-dark">07 / Offentlig ressursbruk og effektivitet</p><h2>Hva koster staten — og hva får vi igjen?</h2></div><p class="section-note">Samlet offentlig forvaltning og SSBs COFOG-formål, ikke et isolert byråkratimål. Korrigerte årsserier, åpne kilde-ID-er og eksplisitte simuleringer.</p></div>
 <div class="off07-kpis">
   <div class="off07-kpi"><span>Samlede utgifter 2025</span><b>2 684,6 mrd.</b><span>Løpende kroner; SSB 2026-vintage <a href="#k113">[K113]</a></span></div>
   <div class="off07-kpi"><span>Utgiftsandel 2025</span><b>48,7 %</b><span>Av samlet BNP, ikke Fastlands-BNP <a href="#k134">[K134]</a></span></div>
   <div class="off07-kpi"><span>Offentlige jobbforhold 2025-K2</span><b>33,5 %</b><span>Andel stillingsforhold, ikke personer <a href="#k114">[K114]</a></span></div>
   <div class="off07-kpi"><span>COFOG sosial beskyttelse 2025</span><b>1 048,8 mrd.</b><span>Overføringer og tjenester, ikke administrasjonsutgift <a href="#k113">[K113]</a></span></div>
 </div>
 <div class="off07-grid">
  <div class="panel"><label class="small-label" for="off07-valg">Velg dokumentert dataserie</label>
   <select id="off07-valg">
    <option value="cofog">Utgifter fordelt på formål (COFOG), 2025</option>
    <option value="total">Samlede utgifter, 2021–2025</option>
    <option value="stilling">Offentlig andel av jobbforhold, 2016–2025</option>
    <option value="innkjop">Offentlige innkjøp, 2024–2025</option>
    <option value="helse">Helseutgifter per innbygger, OECD 2025</option>
   </select>
   <h3 id="off07-tittel" style="margin-top:20px">Offentlig ressursbruk</h3>
   <div id="off07-graf" class="off07-graph" role="img" aria-label="Valgt datagrunnlag visualisert; talltabell ved siden av"></div>
   <p id="off07-forklaring" class="off07-note" aria-live="polite"></p>
   <p class="off07-note"><a href="#k113" id="off07-kilde">Kilde K113</a> · <a href="#rapport-18-forskningstrad-07-offentlig-ressursbruk-effektivitet-og-baumols-kostnadssykdom">Metode og alternative forklaringer</a></p>
  </div>
  <div class="panel"><h3>Tallgrunnlag</h3><p class="panel-sub">Samme observasjoner som i den valgte figuren. Alle datapunktene har eget kildegrunnlag.</p><div id="off07-tabell" class="data-box"></div>
    <button type="button" id="off07-csv" class="pill-button" style="margin-top:17px">Last ned valgte tall (CSV)</button>
    <p class="off07-note"><strong>Metode:</strong> Høye utgifter dokumenterer ressursbruk, ikke ressurslekkasje. Offentlig forvaltnings utgifter må ikke summeres med innkjøpstall uten kontroll for dobbelttelling. Jobbandelen er ikke en produktivitetsserie.</p>
  </div>
 </div>
 <div class="off07-grid">
   <div class="panel"><h3>Baumol: relativ kostnadsutvikling</h3>
    <p class="off07-note">Betinget, stylisert modell: Samme årlige lønnsvekst i to sektorer; endringer i tjenestens relative enhetskostnad skyldes <strong>forskjellen i kvalitetsjustert produktivitetsvekst</strong>. Dette er ingen norsk effektberegning.</p>
    <div class="off07-inputs">
      <label for="off07-produktiv" >Produktivitetsvekst i referansesektoren <strong><output id="off07-produktiv-v">2,0 %</output></strong><input type="range" id="off07-produktiv" min="0" max="4" step="0.25" value="2"></label>
      <label for="off07-tjeneste">Produktivitetsvekst i tjenestesektoren <strong><output id="off07-tjeneste-v">0,5 %</output></strong><input type="range" id="off07-tjeneste" min="0" max="3" step="0.25" value="0.5"></label>
      <label for="off07-aar">Tidshorisont <strong><output id="off07-aar-v">20 år</output></strong><input type="range" id="off07-aar" min="5" max="40" step="5" value="20"></label>
    </div>
    <div id="off07-baumol-resultat" class="off07-result" aria-live="polite"></div><p class="off07-note">Beregning: ((1 + g_ref)/(1 + g_tjeneste))^år − 1. Modellen utelater sektorvekter, kapitalintensitet, teknologisprang, kvalitetsendringer og lønnspremier. Teoretisk bakgrunn <a href="#k120">[K120]</a>; målemetode <a href="#k119">[K119]</a>.</p>
   </div>
   <div class="panel"><h3>Innkjøp: rent hypotetisk beløp</h3>
    <p class="off07-note">DFØ oppgir omtrent 864 mrd. kr i offentlige innkjøp i 2025. Regnestykket viser hvor stor en gitt prosentandel er, <strong>ikke hvilke innsparinger som kan realiseres</strong>. Hele beløpet er ikke tilgjengelig for kutt.</p>
    <div class="off07-inputs"><label for="off07-innkjopandel">Andel av historisk kjøpsvolum <strong><output id="off07-innkjopandel-v">0,5 %</output></strong><input id="off07-innkjopandel" type="range" min="0" max="2" step="0.1" value="0.5"></label></div>
    <div id="off07-innkjop-resultat" class="off07-result" aria-live="polite"></div>
    <p class="off07-note"><strong>Ikke provenyanslag:</strong> En faktisk netto innsparing krever at samme kvalitet og leveringssikkerhet kan kjøpes billigere, at gjennomføringskostnader trekkes fra, at anskaffelser ikke dobbelttelles og at kontrollgruppen viser en forskjell. <a href="#k115">DFØ [K115]</a> · <a href="#k116">Riksrevisjonen [K116]</a>.</p>
   </div>
 </div>
 <p class="chart-note"><a href="07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md" download>Last ned delrapport 07 (Markdown)</a> · <a href="data/hypoteseregister_07.csv" download>Hypoteser, CSV</a> · <a href="data/evidensregister_07.csv" download>Evidens, CSV</a> · <a href="data/proveniens_07.json" download>Dataproveniens, JSON</a>. <strong>Forskningsstatus:</strong> deskriptiv og litteraturbasert; ingen selvstendige kausale analyser.</p>
</section>
'''
assert '<section class="section" id="stresstest">' in s
s=s.replace('<section class="section" id="stresstest">',section+'\n<section class="section" id="stresstest">')
js=r'''
// Delrapport 07: ulike regnskap, populasjoner og tjenestemål plottes aldri som én serie.
let avlest07=[],overskrift07='';
function datakilde07(mode){
 if(mode==='cofog')return {title:'COFOG-utgifter etter formål, 2025',unit:'mrd. kr',key:'K113',note:'Årsverdier i løpende kroner. COFOG viser formålet med utgiften; alminnelig offentlig tjenesteyting er ikke ensbetydende med administrasjon. Noe intern bruk av varer og tjenester inngår i disse formålene.',rows:COFOG_07.filter(r=>r.aar===2025).map(r=>({label:r.formaal,value:r.verdi_mill_kr/1000}))};
 if(mode==='total')return {title:'Samlede offentlige utgifter, 2021–2025',unit:'mrd. kr',key:'K113',note:'Nominell norsk total utgiftsserie fra SSBs reviderte 2026-vintage. Ingen inflasjonsjustering; endringer er ikke mål på administrativ vekst.',rows:OFF_07.filter(r=>r.indikator==='Totale utgifter').map(r=>({label:String(r.aar),value:r.verdi_mill_kr/1000}))};
 if(mode==='stilling')return {title:'Offentlig forvaltnings andel av jobbforhold',unit:'prosent',key:'K114',note:'Jobbforhold i 2. kvartal; samme person kan ha flere jobber. Andelen er ikke offentlig sysselsetting målt som personer eller årsverk.',rows:JOB_07.map(r=>({label:String(r.aar),value:r.offentlig_andel_jobber_prosent}))};
 if(mode==='innkjop')return {title:'Offentlige innkjøp, 2024–2025',unit:'mrd. kr',key:'K115',note:'Offentlige anskaffelser i definert SSB/DFØ-populasjon. Beløpene overlapper offentlige utgifter; skal ikke summeres og er ikke teoretisk sparepotensial.',rows:HOVED_07.filter(r=>r.indikator==='Offentlige innkjøp').map(r=>({label:String(r.periode),value:Number(r.verdi)}))};
 return {title:'Helseutgifter per innbygger, 2025',unit:'USD kjøpekraftskorrigert',key:'K121',note:'OECD Health at a Glance 2025. Omfatter samlede helseutgifter, også private, og er derfor forskjellig fra COFOG helseutgifter.',rows:HOVED_07.filter(r=>r.indikator==='Helseutgifter per innbygger PPP').map(r=>({label:r.gruppe,value:Number(r.verdi)}))};
}
function tegn07(){
 const mode=el('off07-valg').value, info=datakilde07(mode),data=info.rows;
 if(!data.length){el('off07-graf').textContent='Ingen registrerte data i valgt serie.';return;}
 overskrift07=info.title;avlest07=data;
 el('off07-tittel').textContent=info.title;
 el('off07-forklaring').textContent=info.note;
 el('off07-kilde').textContent='Kilde ['+info.key+']';el('off07-kilde').href='#'+info.key.toLowerCase();
 const W=815,left=260,right=100,step=data.length>6?37:50,top=29,H=top+data.length*step+36;
 const max=Math.max(1,...data.map(r=>r.value));const width=W-left-right;
 let svg=`<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(info.title)}; alle tall finnes i tabellen" viewBox="0 0 ${W} ${H}">`;
 for(let k=0;k<=4;k++){const v=max*k/4, x=left+width*k/4; svg+=`<line x1="${x}" x2="${x}" y1="${top-7}" y2="${H-24}" stroke="var(--line)"/><text x="${x}" y="${H-7}" font-size="11" text-anchor="middle" fill="var(--muted)">${esc(nfmt(v,v<10?1:0))}</text>`;}
 data.forEach((r,i)=>{const y=top+i*step,barw=Math.max(1,width*r.value/max), label=r.label.length>35?r.label.slice(0,34)+'…':r.label;
  svg+=`<text x="${left-12}" y="${y+15}" text-anchor="end" font-size="${data.length>6?12:14}" fill="var(--ink2)">${esc(label)}</text><rect x="${left}" y="${y}" width="${barw}" height="21" rx="3" fill="${i===0?'var(--main)':'#87aeb3'}"><title>${esc(r.label)}: ${esc(nfmt(r.value,r.value<10?1:0))} ${esc(info.unit)}</title></rect><text x="${left+barw+8}" y="${y+15}" font-size="12" font-weight="700" fill="var(--ink)">${esc(nfmt(r.value,r.value<10?2:1))}</text>`;
 });
 svg+='</svg>';el('off07-graf').innerHTML=svg;
 el('off07-tabell').innerHTML='<table><thead><tr><th>År / kategori</th><th>'+esc(info.unit)+'</th></tr></thead><tbody>'+data.map(r=>'<tr><td>'+esc(r.label)+'</td><td>'+esc(nfmt(r.value,2))+'</td></tr>').join('')+'</tbody></table>';
 const quote=v=>'"'+String(v).replace(/"/g,'""')+'"';
 el('off07-csv').onclick=()=>lastNedTekst('\uFEFF'+[['Kategori/år',info.unit,'Kilde-ID'],...data.map(r=>[r.label,String(r.value),info.key])].map(row=>row.map(quote).join(';')).join('\r\n')+'\r\n','norsk-okonomi-07-'+mode+'.csv');
}
function beregnBaumol07(){
 const g=Number(el('off07-produktiv').value),t=Number(el('off07-tjeneste').value),years=Number(el('off07-aar').value);
 for(const [id,v] of [['off07-produktiv-v',g],['off07-tjeneste-v',t]])el(id).textContent=nfmt(v,2)+' %';
 el('off07-aar-v').textContent=years+' år';
 const factor=Math.pow((1+g/100)/(1+t/100),years),pct=(factor-1)*100;
 el('off07-baumol-resultat').innerHTML='<b>'+esc((pct>0?'+':'')+nfmt(pct,1))+' %</b>Relativ tjenestekostnad etter '+years+' år i den stiliserte modellen. Faktor: '+esc(nfmt(factor,3))+' × referanseåret. Negativt resultat innebærer fallende relativ enhetskostnad, ikke nødvendigvis fallende nominell pris.';
}
function beregnInnkjop07(){
 const rate=Number(el('off07-innkjopandel').value),gross=864*rate/100;
 el('off07-innkjopandel-v').textContent=nfmt(rate,1)+' %';
 el('off07-innkjop-resultat').innerHTML='<b>'+esc(nfmt(gross,2))+' mrd. kr</b>Ren multiplikasjon: 864 mrd. × '+esc(nfmt(rate,1))+' %. Dette er ikke en dokumentert innsparing og kan ikke bokføres som effekt av reform.';
}
el('off07-valg').addEventListener('change',tegn07);
['off07-produktiv','off07-tjeneste','off07-aar'].forEach(id=>el(id).addEventListener('input',beregnBaumol07));
el('off07-innkjopandel').addEventListener('input',beregnInnkjop07);
tegn07();beregnBaumol07();beregnInnkjop07();
'''
needle='oppdaterUtvidetLandpanel();oppdaterFigur();oppdaterLandpanel();oppdaterBnpPanel();oppdaterFond();oppdaterBolig();oppdaterHypoteser();oppdaterEvidens();highlightTOC();'
assert needle in s
s=s.replace(needle,js+'\n'+needle)
# Tre interne kontrollfunn beholdes uansett eldre dashboarddata.
s=s.replace('Kilde- og metodekilder. Utgave','Kilde- og metodekilder. Utgave')
page.write_text(s,'utf8')
print('Nettsidemal oppdatert, inkludert nytt datasettvalg og to transparente simulatorer.')
