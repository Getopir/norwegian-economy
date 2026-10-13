#!/usr/bin/env python3
"""Kontrollerte utdrag fra offentlige primærkilder, ingen fiktive paneldata."""
from pathlib import Path
import csv,json
R=Path(__file__).resolve().parent; D=R/'data';D.mkdir(exist_ok=True)

def export(name,rows):
    assert rows
    with (D/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (D/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n','utf8')
    print(name,len(rows))
    return rows

migrants=[(2021,16,22,14,27),(2022,46,285,10,16),(2023,46,130,8,24),(2024,16,57,5,14),(2025,17,55,9,None)]
export('utflyttere_formuende_06',[dict(aar=yr,utflyttere_antal=out,formuesskatt_forrige_aar_mill_kr=tax,innflyttere_antal=in_,formuesskatt_innflyttingsaar_mill_kr=in_tax if in_tax is not None else '',kilde_id='K97',kilde_tabell='NOU 2026:9, kap 3, tabell 3.2 og 3.3',populasjon='Spesialutvalg 3565 personer: nettoformue > 100 mill. kr eller Kapitals topp 400 i minst ett år 2021–2025',definisjon='Folkeregisterstatus; ikke identifisert skattemotivert flytting',begrensning='Ikke alle formuende og ikke representativt utvalg; 2025 innflytter-skatt ikke fastsatt') for yr,out,tax,in_,in_tax in migrants])
exitdata=[(2020,53,3301),(2021,52,9900),(2022,167,133800),(2023,187,44284),(2024,100,5420)]
export('utflyttingsskatt_latent_06',[dict(aar=yr,antall_saker=cases,latent_gevinst_mill_kr=latent,kilde_id='K97',kilde_tabell='NOU 2026:9, kap 3, tabell 3.4',populasjon='Skattedirektoratets utflyttingsskattesaker i inntektsåret, ikke samme personliste som 3.2',definisjon='Samlet fastsatt latent gevinst; ikke faktisk flyttet kapital eller skatteinnbetalt beløp',begrensning='Administrative opplysninger ikke samlet inn for statistikkformål; 2025 mangler') for yr,cases,latent in exitdata])
assets=[('Bankinnskudd og obligasjoner',0,100),('Aksjer',20,80),('Direkte eide driftsmidler',30,70),('Primærbolig, verdi opp til 14 mill.',75,25),('Sekundærbolig',0,100),('Næringseiendom',20,80)]
export('formueskatt_sats_06',[dict(aar=2026,eiendel=asset,formell_rabatt_prosent=disc,formell_verdsettingsandel_prosent=val,effektiv_sats_trinn1_prosent=round(val*0.01,4),effektiv_sats_trinn2_prosent=round(val*0.011,4),kilde_id='K93 K98',populasjon='Personlig skattepliktig nettoformue i 2026',merknad='Sats kun på formell verdsettingsandel, før bunnfradrag; ikke effektiv skatt på reell markedsverdi for alle objekter, gjeld eller særregler') for asset,disc,val in assets])
scenario=[(0.25,-25.2),(0.40,-19.5),(0.50,-15.7),(0.60,-12.0),(0.75,-6.3)]
export('skattekommisjon_scenario_06',[dict(sats_prosent=r,anslatt_statisk_provenyendring_mrd_kr=v,generelt_bunnfradrag_kr=2000000,ekstra_primarboligfradrag_kr=7000000,verdsettingsrabatter_fjernes='Ja',aar_referanse=2026,kilde_id='K98',kilde_tabell='NOU 2026:9, tabell 6.2, raden særskilt boligfradrag=7 mill.',status='FORSLAG / STATISK MODELL — IKKE VEDTATT',begrensning='Ikke atferdstilpasninger, ikke alle særregler eller framtidig BNP-effekt') for r,v in scenario])
export('forskningsestimater_06',[
 dict(studie='Jakobsen mfl. (2026), AER',utfall='Bestand formuende skattytere',effekt=-2.0,enhet='prosent ved +1 prosentpoeng toppformuesskatt',horisont='Studiedesign og skatteendringens rammer',type='Identifikasjonsbasert kausalt estimat',kilde_id='K103',sammenlignbar_med_annen_rad='Nei: utfallsenhet/horisont ulik'),
 dict(studie='Jakobsen mfl. (2026), AER',utfall='Sysselsetting',effekt=-0.02,enhet='prosent ved +1 prosentpoeng toppformuesskatt',horisont='Aggregert modellestimat',type='Aggregert beregnet effekt',kilde_id='K103',sammenlignbar_med_annen_rad='Nei: annen utfallsenhet'),
 dict(studie='Jakobsen mfl. (2026), AER',utfall='Investering',effekt=-0.07,enhet='prosent ved +1 prosentpoeng toppformuesskatt',horisont='Aggregert modellestimat',type='Aggregert beregnet effekt',kilde_id='K103',sammenlignbar_med_annen_rad='Nei: annen utfallsenhet'),
 dict(studie='Jakobsen mfl. (2026), AER',utfall='Verdiskaping',effekt=-0.10,enhet='prosent ved +1 prosentpoeng toppformuesskatt',horisont='Aggregert modellestimat',type='Aggregert beregnet effekt',kilde_id='K103',sammenlignbar_med_annen_rad='Nei: annen utfallsenhet'),
 dict(studie='Blandhol (2025), arbeidsnotat',utfall='Langsiktig aggregert produksjon',effekt=-1.3,enhet='prosent, strukturell likevektsmodell',horisont='Lang sikt',type='Modellsimulert langsiktseffekt',kilde_id='K104',sammenlignbar_med_annen_rad='Nei: annen skattereform og modellhorisont'),
 dict(studie='Blandhol (2025), arbeidsnotat',utfall='Omsetning hos utvandrede eieres foretak',effekt=-12.6,enhet='prosent mot kontroll',horisont='Studievindu',type='Hendelsesstudie',kilde_id='K104',sammenlignbar_med_annen_rad='Nei: foretak hos utflyttere'),
])
export('hovedindikatorer_06',[
 dict(indikator='Formuesskatt bunnfradrag enslig',periode='2026',populasjon='Personlige skattytere',verdi=1900000,enhet='NOK',kilde_id='K93',status='Vedtak 2026',merknad='Skattemessig nettoformue'),
 dict(indikator='Formuesskatt første marginaltrinn',periode='2026',populasjon='Personlige skattytere',verdi=1.0,enhet='prosent',kilde_id='K93',status='Vedtak 2026',merknad='1,9–21,5 mill. skattepliktig nettoformue'),
 dict(indikator='Formuesskatt topptrinn',periode='2026',populasjon='Personlige skattytere',verdi=1.1,enhet='prosent',kilde_id='K93',status='Vedtak 2026',merknad='Over 21,5 mill.'),
 dict(indikator='Utbytteskatt etter skjerming',periode='2026',populasjon='Personlige skattytere',verdi=37.84,enhet='prosent',kilde_id='K94',status='Vedtak 2026',merknad='Sats på skattepliktig utbytte'),
 dict(indikator='Selskapsskatt',periode='2026',populasjon='Vanlige aksjeselskaper, alminnelig inntekt',verdi=22,enhet='prosent',kilde_id='K109',status='Vedtak 2026',merknad='Andre sektorspesifikke regler finnes'),
 dict(indikator='Formuesskattebetalere',periode='2024',populasjon='Bosatte personer 17+ år',verdi=701482,enhet='personer',kilde_id='K101',status='Historisk registertall',merknad='Ikke 2026-prognose'),
 dict(indikator='Gjennomsnittlig formuesskatt blant betalere',periode='2024',populasjon='Bosatte personer med positiv formuesskatt',verdi=44300,enhet='NOK',kilde_id='K101',status='Historisk registertall',merknad='Ikke median'),
 dict(indikator='Formuesskatt anslag samlet',periode='2026',populasjon='Personlige og upersonlige skattytere',verdi=36,enhet='mrd. NOK',kilde_id='K110',status='Anslag i forslag til budsjett 2027',merknad='Omtrent, prognose'),
 dict(indikator='Anslått andel personlig formuesskatt',periode='2026',populasjon='Personlige skattytere',verdi=15.2,enhet='prosent',kilde_id='K110',status='Anslag',merknad='Ikke basert på 2024 antall'),
 dict(indikator='Personer i spesialutvalg',periode='2021–2025',populasjon='NOU utvalg med høy formue',verdi=3565,enhet='personer',kilde_id='K97',status='NOU populasjon',merknad='Utvalg, ikke Norges befolkning'),
 dict(indikator='Utflyttere i spesialutvalg sum',periode='2021–2025',populasjon='NOU utvalg med høy formue',verdi=141,enhet='personer',kilde_id='K97',status='Kohortens registrerte utflyttere',merknad='Ikke skattedrevet kausalt antall'),
 dict(indikator='Innflyttere i spesialutvalg sum',periode='2021–2025',populasjon='NOU utvalg med høy formue',verdi=46,enhet='personer',kilde_id='K97',status='Kohortens registrerte innflyttere',merknad='Ikke samme som samlet formuendemigrasjon'),
 dict(indikator='Samlet latent gevinst i skattesaker',periode='2022',populasjon='Utflyttingsskattesaker',verdi=133800,enhet='mill. NOK',kilde_id='K97',status='Administrativt fastsatt latent gevinst',merknad='Ikke realisert kapitalflukt'),
])
proveniens={
 'traad':'06','dato':'2026-10-12','versjon':'0.8.0','sprak':'nb-NO',
 'kilder':{'K93':'https://www.skatteetaten.no/satser/formuesskatt/?year=2026','K94':'https://www.skatteetaten.no/satser/faktor-for-oppjustering-av-gevinsttap-eller-utbytte-pa-aksjer','K97':'https://www.regjeringen.no/no/dokumenter/nou-2026-9/id3167167/?ch=4','K98':'https://www.regjeringen.no/no/dokumenter/nou-2026-9/id3167167/?ch=7','K101':'https://www.ssb.no/inntekt-og-forbruk/skatt-for-personer/statistikk/skatt-for-personer/','K103':'https://doi.org/10.1257/aer.20241596','K104':'https://cblandhol.github.io/JMP/blandhol_JMP.pdf'},
 'henteprotokoll':'Manuell avskrift fra tabell 3.2–3.4 og tabell 6.1–6.2 i NOU 2026:9, gjeldende satser i Skatteetatens register og SSB 2024 statistikk. Tallserie i denne distribusjonen er et verifiserbart kildeutdrag, ikke ny registerkjøring.',
 'forskningsstandard':'Hver rad inneholder tidsdefinisjon, populasjon, enhet, kilde og forbehold. Ingen interpolering og ingen kausale effekter gitt ved summering.',
 'avgrensninger':['3 565-personers utvalget ikke representativt for alle formuende','Latent gevinst er ikke kapital som forlater Norge','SSB siste endelige skatteår 2024, 2026 er anslag','NOU proveny er statisk modell og forslag','Ingen direkte replisering av mikrodata eller forskningsartiklers regresjoner'],
 'ki_erklæring':'ChatGPT (OpenAI) og KI-assistert research, syntese, analyse, kontroll og kode. Primærkildene, ikke KI, er faktagrunnlag.',
 'regnemodeller':'Skattekalkulator er illustrasjon for enslig eier, alle aksjer, ingen gjeld, ingen skjerming, ingen annen skatteformue, faste regler 2026; skatten er personlig og avhenger av skattemessige aksjeverdier før formell rabatt.',
 'oppdatert':'2026-10-12'
}
(D/'proveniens_06.json').write_text(json.dumps(proveniens,ensure_ascii=False,indent=2)+'\n','utf8')
