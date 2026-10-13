#!/usr/bin/env python3
"""Maskinlesbare transkripsjoner: tråd 05, datagrense 12.10.2026.
Ingen interpolasjon, ingen syntetisk person/foretaksdata. Kildene kontrollert mot offentlige publiseringer.
"""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parent; D=R/'data'
D.mkdir(exist_ok=True)
def out(name,rows):
 assert rows and isinstance(rows,list),name
 fields=list(rows[0]);assert all(list(row)==fields for row in rows),name
 (D/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n','utf8')
 with (D/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,delimiter=';');w.writeheader();w.writerows(rows)
 print(name,len(rows))
q=[('2024-K4',15625,6729,8604),('2025-K1',16525,7907,8424),('2025-K2',14112,6217,7681),('2025-K3',16276,7197,8842),('2025-K4',15495,7112,8183),('2026-K1',18092,8669,9252),('2026-K2',17052,7327,9604)]
out('foretak_kvartal_05',[dict(periode=k,totalt=n,aksjeselskap=as_,enkeltpersonforetak=enk,kilde_id='K77',kilde_tabell='SSB 08076',status='Observerte kvartalsregistreringer',merknad='Ikke identisk med aktive nyetablerte foretak; SSB kvartalsmetodikk er endret i 2026; kategori AS og ENK summerer ikke fullt opp til I alt.') for k,n,as_,enk in q])
venture=[('Norge',170),('Danmark',530),('Sverige',1200)]
out('venture_norden_05',[dict(land=land,aar=2025,mill_eur=val,kilde_id='K82',fase='Tidligfaseselskaper',status='Avrundet bransjeobservasjon',definisjon='Nordisk investeringsoversikt: porteføljeselskapets hjemland; fondenes nasjonalitet og tilordning følger PEREP/Invest Europe',forbehold='Kilde fra bransjeforening; ikke alle finansieringsformer; ikke BNP-justert; øvrig Norden ikke uttømmende') for land,val in venture])
out('etablerere_alder_05',[dict(aar=2024,gruppe=gruppe,andel_prosent=val,kilde_id='K81',utvalg='64 622 personlige etablerere av foretak',status='Foreløpige estimater, usikkerhet større enn endelige',merknad='Personer, ikke foretak. Aldersandeler avrundet.') for gruppe,val in [('16–24 år',11.9),('25–44 år',53.8),('45–66 år',30.2),('67 år+',4.1)]])
out('etablerere_kjonn_05',[dict(aar=2024,gruppe=gruppe,andel_prosent=val,kilde_id='K81',utvalg='64 622 personlige etablerere',status='Foreløpig, estimerte andeler') for gruppe,val in [('Kvinner',31.2),('Menn',68.8)]])
# SSBs formidlingsartikkel publiserer *omtrentlige* fortsettende vekstandeler.
out('lovende_startups_05',[dict(aar_etter=aar,fortsatt_vekst_prosent=vekst,blitt_scaleup_prosent=scaleup,kilde_id='K79',populasjon='Selektert gruppe norske lovende startups; ikke alle foretak',status='Avrundet fra forskningsformidling',merknad='Omtrentlige andeler; scaleup-andelen inngår i vekstgruppen; de skal ikke summeres') for aar,vekst,scaleup in [(3,23,6),(6,15,3),(9,10,2.5)]])
out('ungdomsarbeid_05',[dict(aar=yr,ledighet_15_24_prosent=led,kilde_id='K87',gruppe='15–24 år',definisjon='AKU arbeidsledige som andel av arbeidsstyrken, ikke alle personer i aldersgruppen',status='Publisert SSB undervisningsserie') for yr,led in [(2023,11.1),(2024,12.1),(2025,14.0)]])
# Only transcribe the explicitly validated 2024/2025 observations. Historical gaps remain missing.
out('nyutdannede_05',[dict(aar=yr,andel_sysselsatt_prosent=work,andel_akademiske_yrker_prosent=academic,kilde_id='K88',gruppe='20–34 år, nylig avsluttet utdanning',status='AKU observasjon',merknad='Andel i akademiske yrker gjelder nyutdannede med høyere utdanning; annen populasjonsnevner enn sysselsettingsandelen') for yr,work,academic in [(2024,89.9,83.0),(2025,88.6,78.8)]])
out('hovedindikatorer_05',[
 dict(indikator='Nye registrerte foretak',periode='2026-K2',gruppe='Norge',verdi=17052,enhet='foretak',kilde_id='K77',merknad='Kvartal, 20,8% over 2025-K2, metodeendring i 2026'),
 dict(indikator='Registreringer foretak',periode='2025-K2',gruppe='Norge',verdi=14112,enhet='foretak',kilde_id='K77',merknad='Sammenligningskvartal'),
 dict(indikator='Aktive foretak',periode='2023',gruppe='Norge',verdi=333846,enhet='foretak',kilde_id='K77',merknad='Årsstatistikk; ulik populasjon fra kvartalsregistreringer'),
 dict(indikator='Aktive foretak uten ansatte eller rapportering',periode='2023',gruppe='Norge',verdi=149303,enhet='foretak',kilde_id='K77',merknad='Kategori summerer ikke med øvrige foretak i figurer uten samme tabell'),
 dict(indikator='Aktive nyetablerte 2018',periode='2018',gruppe='Norge',verdi=29481,enhet='foretak',kilde_id='K77',merknad='Egen årsdemografikohort, ikke 2026-kvartalsregistrering'),
 dict(indikator='Overlevd fem år i 2018-kohorten',periode='2018+5',gruppe='Norge',verdi=14097,enhet='foretak',kilde_id='K77',merknad='SSB tabell 5, femårs overlevelse'),
 dict(indikator='Personlige etablerere 2024',periode='2024',gruppe='Norge',verdi=64622,enhet='personer',kilde_id='K81',merknad='Foreløpige anslag'),
 dict(indikator='Foretakenes egenutførte FoU',periode='2024',gruppe='Norge',verdi=46.6,enhet='mrd. kroner',kilde_id='K84',merknad='Foretak med minst ti sysselsatte'),
 dict(indikator='Reell FoU-endring',periode='2024',gruppe='Norge',verdi=-6,enhet='prosent',kilde_id='K84',merknad='2023 til 2024 realendring'),
 dict(indikator='FoU-årsverk',periode='2024',gruppe='Norge',verdi=25600,enhet='årsverk',kilde_id='K84',merknad='Omtrent 25 600'),
 dict(indikator='Innovasjonsaktivitet',periode='2022–2024',gruppe='Foretak i SSBs innovasjonsundersøkelse',verdi=60,enhet='prosent',kilde_id='K85',merknad='5+ sysselsatte; alle næringer i utvalget'),
 dict(indikator='Produkt- eller prosessinnovasjon',periode='2022–2024',gruppe='Foretak i SSBs innovasjonsundersøkelse',verdi=57,enhet='prosent',kilde_id='K85',merknad='Overlapp med andre innovasjonsmål'),
 dict(indikator='NEET personer',periode='2025',gruppe='15–29 år',verdi=105318,enhet='personer',kilde_id='K86',merknad='Registerbasert NEET, ikke AKU-ledige'),
 dict(indikator='NEET-andel',periode='2025',gruppe='15–29 år',verdi=10.1,enhet='prosent',kilde_id='K86',merknad='Registerbasert populasjon'),
 dict(indikator='Sysselsetting nyutdannede',periode='2025',gruppe='20–34 år',verdi=88.6,enhet='prosent',kilde_id='K88',merknad='AKU nyutdannede, ned 1.3 prosentpoeng'),
 dict(indikator='Pensjonskapital fondsandel',periode='2026-studie',gruppe='Norge',verdi=18,enhet='prosent av kapital i PE/VC-fond',kilde_id='K83',merknad='Oppdragsfinansiert bransjerapport, ikke andel av pensjonsformuen'),
 dict(indikator='Pensjonskapital fondsandel',periode='2026-studie',gruppe='Danmark',verdi=21.3,enhet='prosent av kapital i PE/VC-fond',kilde_id='K83',merknad='Samme studie/definisjon'),
 dict(indikator='Pensjonskapital fondsandel',periode='2026-studie',gruppe='Sverige',verdi=25.7,enhet='prosent av kapital i PE/VC-fond',kilde_id='K83',merknad='Samme studie/definisjon'),
 dict(indikator='Pensjonskapital fondsandel',periode='2026-studie',gruppe='Finland',verdi=27.8,enhet='prosent av kapital i PE/VC-fond',kilde_id='K83',merknad='Samme studie/definisjon'),
])
# Details at original publication URL by id
SOURCES={
'K77':'https://www.ssb.no/virksomheter-foretak-og-regnskap/virksomheter-og-foretak/statistikk/foretak',
'K78':'https://www.ssb.no/virksomheter-foretak-og-regnskap/virksomheter-og-foretak/artikler/fra-oppstart-til-vekst',
'K79':'https://www.ssb.no/virksomheter-foretak-og-regnskap/virksomheter-og-foretak/artikler/fra-potensial-til-realisering-hva-skjer-med-lovende-startups-over-tid',
'K80':'https://www.oecd.org/en/publications/oecd-economic-surveys-norway-2026_5cc02644-en/full-report/resetting-regulatory-frameworks-to-revive-business-dynamism_4501d1ee.html',
'K81':'https://www.ssb.no/virksomheter-foretak-og-regnskap/eierskap-og-roller/statistikk/etablerere-i-naeringslivet',
'K82':'https://nvca.no/uploads/157/NVCA-aktivitetsundersokelse-2025-FINAL.pdf',
'K83':'https://nvca.no/wp-content/uploads/2026/05/NVCA-rapport-om-pensjonskapital-2026-Kartlegging-av-pensjonskapital-i-norsk-PE-og-VC-2.pdf',
'K84':'https://www.ssb.no/teknologi-og-innovasjon/forskning-og-innovasjon-i-naeringslivet/statistikk/forskning-og-utvikling-i-naeringslivet/artikler/nedgang-i-naeringslivets-fou-2024',
'K85':'https://www.ssb.no/teknologi-og-innovasjon/informasjons-og-kommunikasjonsteknologi-ikt/statistikk/innovasjon-i-naeringslivet',
'K86':'https://www.ssb.no/arbeid-og-lonn/faktaside/hva-er-neet',
'K87':'https://www.ssb.no/ssb-skole/undervisningsopplegg/det-norske-arbeidsmarkedet/unge-som-verken-er-i-jobb-eller-utdanning.hva-er-arbeidsledighet',
'K88':'https://www.ssb.no/arbeid-og-lonn/sysselsetting/statistikk/arbeidskraftundersokelsen/artikler/flere-nyutdannede-ser-etter-ny-jobb',
'K89':'https://www.ssb.no/teknologi-og-innovasjon/forskning-og-innovasjon-i-naeringslivet/artikler/resultater-av-forskningsradets-naeringsrettede-virksomhet-i-perioden-2006-2024',
'K90':'https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/globale-verdikjeder-og-outsourcing',
'K91':'https://www.ssb.no/nasjonalregnskap-og-konjunkturer/okonomiske-analyser/okonomiske-analyser-2-2026-utsyn-over-aret-2025',
'K92':'https://www.oecd.org/en/publications/benchmarking-government-support-for-venture-capital_81e53985-en.html'}
proveniens={'delrapport':'05','versjon':'0.7.0','datagrense':'2026-10-12','dataopphav':SOURCES,'hentemetode':'Manuell transkripsjon fra kontrollerte publiserte originale webtabeller og rapporter; ingen automatisk datavask/API','datasett':{
'foretak_kvartal_05':{'kilde':'K77','tabell':'SSB 08076','observasjoner':len(q),'enhet':'antall foretak per kvartal','status':'Deskriptivt, metodeendring fra 2026'},
'venture_norden_05':{'kilde':'K82','figur':'3–5','observasjoner':len(venture),'enhet':'avrundede millioner euro 2025','status':'Bransjeestimat, ikke etterspørselsside, ikke normalisert'},
'etablerere_alder_05':{'kilde':'K81','tabell':'SSB 14613','observasjoner':4,'enhet':'andel personlige etablerere','status':'Foreløpig 2024'},
'lovende_startups_05':{'kilde':'K79','observasjoner':3,'enhet':'prosent av selekterte lovende startups','status':'Avrundet i originalartikkel'},
'ungdomsarbeid_05':{'kilde':'K87','observasjoner':3,'enhet':'prosent av aldersgruppens arbeidsstyrke','status':'AKU'},
'nyutdannede_05':{'kilde':'K88','observasjoner':2,'enhet':'prosent av definerte nyutdannede','status':'AKU 2024/2025; ulike populasjoner for 2 mål'},
'hovedindikatorer_05':{'kilder':'K77–K89','observasjoner':19,'status':'Utvalgte, ikke harmonisert panel'},
},'forskningsetikk':'KI-verktøy inkludert ChatGPT brukt til struktur, kode og kildesøk. Kildene (ikke modellutdata) er faktagrunnlag. Sikkerhetskopiering anbefales.',
'begrensninger':['Ingen koblet firmadata eller persondata','Kapitalkilder er ufullstendige','Ingen harmonisert nordisk oppstartsserie','Ingen egen kausal estimering']}
(D/'proveniens_05.json').write_text(json.dumps(proveniens,ensure_ascii=False,indent=2)+'\n','utf8')
print('kildeantall',len(SOURCES))
