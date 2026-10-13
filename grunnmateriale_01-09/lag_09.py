#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kildebasert delrapport 09 og åpne data. Datagrense 13. oktober 2026.
Kun kontrollerte publiserte tall; hypotetiske beregninger segregert fra observasjoner.
"""
from pathlib import Path
import json,csv
R=Path(__file__).resolve().parent
D=R/'data';D.mkdir(exist_ok=True)
DATE='2026-10-13'
SOURCES=[
(152,'Statistisk sentralbyrå (2026)','Nasjonale befolkningsframskrivinger, statistikk, oppdatert 12. juni 2026; tabell 14740/14742/14743/14744. https://www.ssb.no/befolkning/befolkningsframskrivinger/statistikk/nasjonale-befolkningsframskrivinger'),
(153,'Statistisk sentralbyrå (2026)','Regionale befolkningsframskrivinger, oppdatert 12. juni 2026; tabell 14746. https://www.ssb.no/befolkning/befolkningsframskrivinger/statistikk/regionale-befolkningsframskrivinger'),
(154,'Statistisk sentralbyrå (2026)','Fødte: 2025-tall, oppdatert 12. mars 2026; tabell 04232, 07872. https://www.ssb.no/befolkning/fodte-og-dode/statistikk/fodte'),
(155,'Statistisk sentralbyrå (2026)','Familier og husholdninger, oppdatert 30. september 2026; tabell 10986. https://www.ssb.no/befolkning/barn-familier-og-husholdninger/statistikk/familier-og-husholdninger'),
(156,'Statistisk sentralbyrå (2026)','Boliger, boligbestanden 2026, oppdatert 3. mars 2026; tabell 06265. https://www.ssb.no/bygg-bolig-og-eiendom/bolig-og-boforhold/statistikk/boliger'),
(157,'Statistisk sentralbyrå (2026)','Sjukeheimar, heimetenester og andre omsorgstenester: nøkkeltall 2025, oppdatert 15. juni 2026. https://www.ssb.no/helse/helsetjenester/statistikk/sjukeheimar-heimetenester-og-andre-omsorgstenester'),
(158,'Statistisk sentralbyrå (2026)','Sykehjem og hjemmetjenesten i Norge, endret 21. september 2026; tabell 12003, 06969 og 14740. https://www.ssb.no/helse/helsetjenester/artikler/sykehjem-og-hjemmetjenesten-i-norge'),
(159,'Helse- og omsorgsdepartementet (2026)','Meld. St. 11 (2025–2026), Helsepersonellplan 2040, publisert 12. juni 2026. https://www.regjeringen.no/no/dokumenter/meld.-st.-11-20252026/id3164917/'),
(160,'Helse- og omsorgsdepartementet (2026)','Slik skal regjeringen sikre nok helsepersonell, 12. juni 2026; framskrevet gap 42 400 personer/årsverk 2040, se hovedrapport for definisjon. https://www.regjeringen.no/no/aktuelt/slik-skal-regjeringen-sikre-nok-helsepersonell/id3165406/'),
(161,'Helsepersonellkommisjonen (2023)','NOU 2023: 4 Tid for handling, kapittel 13; HELSEMOD-framskrivinger etter datavintage 2019 og antakelser fra 2023. https://www.regjeringen.no/no/dokumenter/nou-2023-4/id2961552/?ch=14'),
(162,'Finansdepartementet (2026)','Meld. St. 1 (2026–2027): Nasjonalbudsjettet 2027, kapittel 3; oppdatert finansieringsbehov 2060. https://www.regjeringen.no/no/dokumenter/meld.-st.-1-20262027/id3175768/?ch=3'),
(163,'Fødselstallsutvalget (2026)','NOU 2026: 2 Politikk for nye generasjoner, 9. februar 2026, hovedbudskap og årsakshypoteser. https://www.regjeringen.no/no/dokumenter/nou-2026-2/id3148337/?ch=2'),
(164,'Statistisk sentralbyrå (2026)','Befolkningen eldes raskt de neste ti årene, 12. juni 2026; historisk trend, SSBs aldersgrupper og regionalt mønster. https://www.ssb.no/befolkning/befolkningsframskrivinger/statistikk/nasjonale-befolkningsframskrivinger/artikler/befolkningen-eldes-raskt-de-neste-ti-arene'),
(165,'Statistisk sentralbyrå (2026)','Nasjonale befolkningsframskrivinger 2026, rapport 2026/21 av Tømmerås mfl., publisert 12. juni 2026; forutsetninger og usikkerhet. https://www.ssb.no/befolkning/befolkningsframskrivinger/artikler/nasjonale-befolkningsframskrivinger-2026'),
(166,'Statistisk sentralbyrå (2026)','Befolkningsframskrivinger for kommunene 2026, rapport 2026/22 av Leknes og Løkken. https://www.ssb.no/befolkning/befolkningsframskrivinger/artikler/befolkningsframskrivinger-for-kommunene-2026'),
(167,'Fødselstallsutvalget (2025)','Fallende fødselstall i Norge: utvikling og mulige tiltak for unge voksne, 24. april 2025, særlig om ønsket og faktisk barnetall. https://www.regjeringen.no/no/dokumenter/fallende-fodselstall-i-norge-utvikling-og-mulige-tiltak-for-unge-voksne/id3097987/?ch=3'),
(168,'Finansdepartementet (2024)','Meld. St. 31 (2023–2024) Perspektivmeldingen 2024, kapittel 5 og 7, opprinnelig 2060-referansebane. https://www.regjeringen.no/no/dokumenter/meld.-st.-31-20232024/id3049290/?ch=7'),
(169,'Statistisk sentralbyrå (2026)','Slik lager SSB befolkningsframskrivinger; MMM/MMMM, usikkerhet, fruktbarhet, levealder og migrasjon. https://www.ssb.no/befolkning/befolkningsframskrivinger/artikler/slik-lager-ssb-befolkningsframskrivinger'),
(170,'Finansdepartementet (2024–2025)','Meld. St. 2 (2024–2025), revidert nasjonalbudsjett; Perspektivmeldingen 2024: økt yrkesdeltakelse blant eldre og årsaksmekanisme. https://www.regjeringen.no/no/dokumenter/meld.-st.-2-20242025/id3100887/?ch=2')
]

def save(stem,rows):
    (D/f'{stem}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    keys=list(dict.fromkeys(k for row in rows for k in row))
    with (D/f'{stem}.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=keys,delimiter=';');w.writeheader();w.writerows(rows)

years=[(2026,5627400,5627400,5627400), (2030,5751203,5663302,5822435),(2040,6027372,5634157,6383176),(2050,6214071,5499807,6911208),(2060,6305127,5256233,7413803),(2075,6391695,4761879,8289096),(2100,6384547,3827160,9712698)]
POP=[dict(aar=y,MMM=m,LLL=l,HHH=h,kilde_id='K152',status='Registrert folketall' if y==2026 else 'SSB 2026-framskriving',merknad='Alle tre alternativer starter ved registrert befolkning i 2026; valg av framtidige forutsetninger gir scenario-spredning') for y,m,l,h in years]
save('befolkningsbaner_09',POP)
region_data=[('Østfold',316448,359918),('Akershus',749207,898014),('Oslo',728714,844646),('Innlandet',379488,397124),('Buskerud',272981,307741),('Vestfold',259332,288054),('Telemark',177923,184526),('Agder',323930,359654),('Rogaland',508922,559177),('Vestland',658342,699100),('Møre og Romsdal',273169,277987),('Trøndelag',489166,531553),('Nordland',243272,235856),('Troms',171218,175965),('Finnmark',75288,76544)]
REG=[dict(fylke=k,observert_2026=a,framskrevet_2050=b,endring=b-a,prosent=round(100*(b/a-1),1),kilde_id='K153',status='2026 observert; 2050 SSB regionalt hovedalternativ MMMM') for k,a,b in region_data]
assert sum(x['observert_2026'] for x in REG)==5627400
# BEFREG/MMMM summerer ikke til BEFINN/MMM: SSB dokumenterer separat modellgrunnlag.
assert sum(x['framskrevet_2050'] for x in REG)==6195859
save('fylker_09',REG)
HH=[dict(type=k,antall=v,aar=2026,kilde_id='K155',status='SSB registeroppgave') for k,v in [('Aleneboende',1103955),('Par uten barn',648127),('Par med barn',611938),('En forelder med barn',176894),('Andre husholdninger',131137)]]
assert sum(x['antall'] for x in HH)==2672051
save('husholdningstyper_09',HH)
HOUSING=[dict(indikator='Registrerte boliger, bebodde og ubebodde',aar=2026,verdi=2762504,enhet='boliger',kilde_id='K156',status='Bestand; Matrikkelen, registreringsetterslep'),dict(indikator='Privathusholdninger',aar=2026,verdi=2672051,enhet='husholdninger',kilde_id='K155',status='Husholdninger, egen registreringsdefinisjon'),dict(indikator='Registrerte boliger, netto endring siste år',aar=2026,verdi=18761,enhet='boliger',kilde_id='K156',status='Netto bestandsendring; ikke ferdigstillelser')]
save('bolig_husholdning_09',HOUSING)
FERT=[dict(aar=2015,fruktbarhet=1.73,alder_mor_foerste=28.9,kilde_id='K154',status='SSB observasjon'),dict(aar=2024,fruktbarhet=1.44,alder_mor_foerste=30.4,kilde_id='K154',status='SSB observasjon'),dict(aar=2025,fruktbarhet=1.48,alder_mor_foerste=30.4,kilde_id='K154',status='SSB observasjon')]
save('fertilitet_09',FERT)
FERTF=[dict(aar=2026,MMM=1.50,LMM=1.43,HMM=1.55,kilde_id='K152',status='SSB hypotese'),dict(aar=2030,MMM=1.56,LMM=1.24,HMM=1.81,kilde_id='K152',status='SSB hypotese'),dict(aar=2050,MMM=1.63,LMM=1.19,HMM=1.87,kilde_id='K152',status='SSB hypotese'),dict(aar=2100,MMM=1.64,LMM=1.19,HMM=1.89,kilde_id='K152',status='SSB hypotese')]
save('fertilitetsforutsetninger_09',FERTF)
DEATH=[dict(aar=2025,dode=45040,status='Observert',kilde_id='K152'),dict(aar=2030,dode=47986,status='SSB MMM-betinget',kilde_id='K152'),dict(aar=2050,dode=60588,status='SSB MMM-betinget',kilde_id='K152'),dict(aar=2075,dode=67058,status='SSB MMM-betinget',kilde_id='K152'),dict(aar=2100,dode=70830,status='SSB MMM-betinget',kilde_id='K152')]
save('dodsfall_09',DEATH)
CARE=[
 dict(aar=2025,indikator='Årsverk i kommunale omsorgstjenester',verdi=163755,enhet='årsverk',kilde_id='K157',status='SSB observert'),
 dict(aar=2025,indikator='Brukere 80+ av hjemmetjenester',verdi=70662,enhet='personer',kilde_id='K158',status='SSB observert 31.12'),
 dict(aar=2025,indikator='Brukere 80+ av institusjonstjenester',verdi=27039,enhet='personer',kilde_id='K158',status='SSB observert 31.12'),
 dict(aar=2025,indikator='Plasser i sykehjem',verdi=39727,enhet='plasser',kilde_id='K157',status='SSB observert 31.12'),
 dict(aar=2025,indikator='Kommunale omsorgsutgifter',verdi=184.7,enhet='mrd. kr',kilde_id='K157',status='SSB observert'),
 dict(aar=2040,indikator='Anslått ubalanse helsepersonell, nasjonalt',verdi=42400,enhet='helsepersonell / modellgap',kilde_id='K160',status='Offentlig framskriving; IKKE en årverksprognose for kommunal omsorg alene'),
]
save('omsorgsnokkeltall_09',CARE)
OLDER=[dict(aar=2026,antall_80_pluss=284939,status='Observert 2026 (80–89 pluss 90+)',kilde_id='K158'),dict(aar=2040,antall_80_pluss=462000,status='SSB avrundet MMM-tall (omtrent)',kilde_id='K158'),dict(aar=2050,antall_80_pluss=round(6214071*.095),status='Egen omregning av SSBs ca. 9,5 % MMM; IKKE direkte tabelltall',kilde_id='K165')]
save('eldre80_09',OLDER)
# Study metadata: input shapes rather than purported official forecast.
PROV={
 'versjon':'1.1.0','datagrense':DATE,'forskningsomraade':'09 — demografi, boligetterspørsel, arbeidskraft og statsfinanser',
 'observasjon_og_modell':'Bare datamengdene *09.json og *09.csv ovenfor inneholder observerte tall eller framskrivinger, individuelt klassifisert. Ingen av nettstedets interaktive bolig-/omsorgskalkulatorutdata er SSB-prognoser.',
 'modeller':{
  'bolig_illustrasjon':'H(t) = H0*(P(t)/P0)*(s_eff_0/s_antatt_t); s_eff_0 = P0/H0 = 2.106; bruker nasjonalt folketall inkl. institusjonsbefolkning og er bare mekanisk følsomhet; ingen regional husholdningsmodell. H0 = 2 672 051; P0 = 5 627 400.',
  'omsorg_illustrasjon':'Hjemmetjenestebrukere 80+ i 2050 = (SSBs ca. 9,5% * P_2050)*andel. Referansescenarioandel 2025 er 24.8 prosent, hentet fra publisert SSB nøkkelindikator. Valgfri reduksjon i prevalens er brukernes hypotese. Ingen slutning om totalt helsepersonell, tjenestetimer, utgifter eller sammenfall med aldersjustert helse.',
  'dodsfall_kritisk':'Antall døde er IKKE antall boliger frigjort; flere døde tilhører samme husholdning, mange eier ikke bolig, boliger kan være i uattraktive regioner og overdragelser kan involvere familie/utleie.',
 },
 'spesielle_forbehold':['Regional MMMM summerer til 6 195 859 i 2050, nasjonal MMM til 6 214 071; avviket 18 212 følger separate SSB-modeller (K169).', '2026 populasjon inkluderer institusjon og er ikke lik antall registrerte personer i privathusholdninger.','SSBs rapport sier 9,5 % 80+ i 2050, mens en tilhørende journalistisk artikkel sier over 10 %. Vi prioriterer hovedrapportens anslag og merker det som omtrent.','2023 HELSEMOD-scenarier og 2026 Helsepersonellplan 2040 er ulike modeller/vintager.','Tall om ønsket barnetall i spørreundersøkelser er ikke det samme som periodens SFT og kan ikke trekkes fra hverandre og kalles udekkede barneønsker.'],
 'kilder':{f'K{n}':ref.split('https://')[-1].strip() for n,org,ref in SOURCES},
 'ansvar':'Rapportutkast laget med KI-assistanse. Uavhengig reproduksjon og fagfellevurdering er ikke gjennomført.'
}
(D/'proveniens_09.json').write_text(json.dumps(PROV,ensure_ascii=False,indent=2)+'\n','utf-8')

hyp_specs=[
('Aldring og arbeidskraft','Andelen eldre vokser raskere enn arbeidsinnsatsen i omsorg','Pensjonsalder, innvandring og friskere aldring kan dempe netto press','K152 K158 K160','Kjør kohortkomponent og alders-/kjønnsspesifikk timeverkmodell med 2026-vintage','Korrigert tilgjengelig arbeidskraft vokser minst like raskt som tjenestebehovet'),
('Geografisk boligetterspørsel','Demografisk aldring fører til fallende boligetterspørsel i utvalgte distrikter','Mindre husholdninger, ferieboliger, arbeidsinnvandring og internflytting opprettholder etterspørselen','K153 K155 K156','Regionfaste husholdningsrater og nettoflytting kommune × boligtype × alder','Boligetterspørsel øker i de omtalte distriktsområdene etter kontroll'),
('Boliger etter dødsfall','Økende dødsfall øker realiserbar boligkapasitet regionalt','Ektefelle/partner bor videre, arving beholder og boligen ligger feil sted','K152 K155 K156','Registerkobling død–eierskap–husholdning–transaksjon med bosted','Andel frigjorte salgbare boliger er stabil eller faller'),
('Husholdningsstørrelse','Flere aleneboende øker boligbehov utover ren befolkningsvekst','Flergenerasjonsbolig, samboerskap, student- og arbeidsinnvandring kan dempe størrelsesfallet','K155 K153','Estimer husholdningsdannelsesrate etter alder, kjønn, kommuner, utdanning','Gjennomsnittlig husholdningsstørrelse stiger og demper behov'),
('Fertilitet og boligrisiko','Høye boligkostnader forsinker første fødsel via senere husholdningsetablering','Utdanning, samliv, seksualnormer, prevensjon og helse forklarer det meste','K154 K163 K167','Hendelsesstudie rundt pris-/kredittsjokk; kontroller partnerskap og inntekt','Ingen effekt av eksogene boligkostnadssjokk på hazard for første fødsel'),
('Urealiserte barneønsker','Et voksende gap mellom ønsket og realisert barnetall skyldes endrede rammevilkår','Varierende preferanser og survey-bias forklarer observerte gap','K163 K167','Samme individer intervjues og kobles til fødselshistorikk over 10+ år','Kohort- og panelsammenlikning viser ikke vedvarende gap'),
('Migrasjon og forsørgerbyrde','Nettoinnvandring kan redusere forsørgerbyrden første tiår','Aldring blant innvandrere og lave yrkesrater gjør effekten liten','K152 K165 K169','Dekomponer alder, arbeidsmarked, integreringsforløp og netto skatter','Effekten på timeverksjustert forsørgerbyrde er ikke positiv'),
('Komprimert sykelighet','Lavere behovsrate for 80+ demper omsorgspresset vesentlig','Overlevelse med flere kroniske lidelser kan øke tjenestetimer','K158 K157 K159','Aldersstandardiserte brukerandeler, antall timer og helsetilstand etter kohort','Lavere brukerandel kompenseres av sterk vekst i timer per bruker'),
('Produktivitet i omsorg','Økt tjenesteproduktivitet kan dekke behov uten proporsjonalt flere årsverk','Tjenestene er arbeidsintensive, og teknologi erstatter begrenset bemanning','K159 K160 K161','Kvalitetsjustert timeverk per bruker, sammenlign kontrollerte pilotkommuner','Ingen netto effekt på timeverk ved uendret kvalitet'),
('Pensjonsrespons','Lengre yrkeskarrierer øker skattebasen og demper belastning','Helseulikhet og yrkessammensetning begrenser forlenget yrkesliv','K170 K168 K162','Pensjonsreformens kohortdiskontinuiteter og aldersspesifikk yrkesdeltakelse','Ingen vedvarende økning i sysselsatte timer etter regelendringer'),
('Kommunalt gap','En del kommuner får samtidig lavere arbeidsstyrke og høyere omsorgsbehov','Tjenestesamarbeid, pendling og statlige overføringer utjevner ulikheter','K153 K159 K162','Kommunefaste panel for skattegrunnlag, omsorgsbehov, bemanning og kvalitet','Netto ressursgap forklares av annet enn aldersstruktur'),
('Boligformue intergenerasjon','Boligprisene i fraflyttingsområder demper realiserbar formue for eldre','Nye bruksformer og velferdsbehov opprettholder boligverdier','K153 K156 K07','Hedoniske boligpris- og transaksjonspaneler etter dødelighet og flytting','Boligpris- og salgslikviditet er uendret i høy-aldringsområder'),
('Fondsavhengighet og demografi','Aldringsdrevet utgiftsvekst kan overstige vekst i skattebase og fondsrom','Sterkere produksjon og lavere brukerfrekvens gjør gapet håndterbart','K162 K168 K152','Integrert modell for avgifter, pensjoner, helse og SPU med usikkerhet','Fiskalt gap forsvinner i nøkterne kontrafaktiske antakelser'),
('Institusjonelle barrierer','Manglende kommunal omstilling forsterker geografiske kostnader','Lokal tilpasning er optimal under geografiske og kvalitetskrav','K166 K159 K153','Før/etter og syntetisk kontroll for kommunesammenslåing, digitalisering og samarbeid','Ingen målbar kvalitetsjustert merkostnad med aldring/krymping'),
]
HY=[]
for i,(title,hyp,anti,keys,test,fals) in enumerate(hyp_specs,1):
 HY.append(dict(id=f'H09-{i:02d}',tittel=title,hypotese=hyp,mothypotese=anti,variabler='Alder, tid, kommune, inntekt, tjenestetimer, arbeidsdeltakelse, boligtype, familierelasjon, migrasjon',primarkilder=keys,forskningslitteratur='K161 K163 K165 K167',empirisk_test=test,falsifikasjonskriterium=fals,resultat='Ikke selvstendig kausalt estimert i denne delrapporten',evidensklasse='U',tillit='Uavklart; testdesign dokumentert',status='Primærkilder kartlagt; registerkobling/identifikasjon gjenstår',traad='09'))
save('hypoteseregister_09',HY)

claims=[
('Folketall 2026','Norge 5 627 400 personer ved inngangen til 2026','K152','A','Registrert observasjon'),
('Folketall 2050 i MMM','6 214 071 personer','K152','D','SSB betinget framskriving'),
('Folketall 2100 i MMM','6 384 547 personer','K152','D','SSB betinget framskriving'),
('Alternativ 2100 LLL','3 827 160 personer','K152','D','SSB lavbane'),
('Alternativ 2100 HHH','9 712 698 personer','K152','D','SSB høgbane'),
('Fruktbarhet 2025','1,48 mot 1,44 i 2024','K154','A','SSB observasjon'),
('Fødealder første barn','30,4 år for kvinner i 2025','K154','A','SSB observasjon'),
('Dødsfall 2025','45 040 dødsfall i 2025','K152','A','SSB registrert'),
('Dødsfall 2050 MMM','60 588 dødsfall (modell)','K152','D','Betinget framskriving'),
('Aldring 2026','284 939 personer 80+','K158','A','Registrert alder 80–89 og 90+'),
('Aldring 2040','Om lag 462 000 personer 80+','K158','D','SSB avrundet MMM'),
('Aldring 2050','Om lag 9,5 prosent 80+ av folkemengden','K165','D','Rapport avrundet'),
('Vippepunkt 2032','Flere 65+ enn 0–19 i hovedalternativet','K164','D','SSB scenario'),
('Regionvekst Akershus','19,9 prosent i 2026–2050','K153','D','SSB MMMM'),
('Regionvekst Oslo','15,9 prosent i 2026–2050','K153','D','SSB MMMM'),
('Regionfall Nordland','Minus 3,0 prosent 2026–2050','K153','D','SSB MMMM'),
('Flertall kommuner vokser','63 prosent anslås å vokse mot 2050','K166','D','SSB MMMM'),
('Husholdninger 2026','2 672 051 privathusholdninger','K155','A','SSB registrert'),
('Aleneboende 2026','1 103 955 privathusholdninger med én person','K155','A','SSB registrert'),
('Boligmasse 2026','2 762 504 registrerte boliger','K156','A','SSB registrert'),
('Boligbestandsvekst 2026','18 761 netto registrerte boliger fra 2025','K156','A','SSB bestandsendring'),
('Husholdninger versus boligmasse','90 453 enheter i differanse uten direkte tolking som ledigboliger','K155 K156','D','Egen aritmetisk beregning'),
('Omsorg årsverk 2025','163 755 årsverk','K157','A','Kommunale omsorgstjenester'),
('Omsorg utgifter 2025','184,7 mrd. kroner','K157','A','Kommunale omsorgstjenester'),
('Hjemmetjenester 80+','70 662 brukere ved utgangen av 2025','K158','A','SSB registrert'),
('Institusjon 80+','27 039 brukere ved utgangen av 2025','K158','A','SSB registrert'),
('Behov helsepersonell 2040','Modellert ubalanse 42 400 i 2040','K160','D','SSB framskriving formidlet i 2026-plan'),
('Historisk HELSEMOD 2040','Referanse 460 000 årsverk og 18 prosent i helse/omsorg','K161','D','2019 grunnlag, 2023 offentlig scenariovintage'),
('Fiskalt gap 2060','5,8 prosent av Fastlands-BNP i NB2027','K162','D','Betinget finanspolitisk referanse'),
('Barneønsker og faktisk fruktbarhet','Utvalget dokumenterer betydelig avvik i survey og realisert utvikling','K163','B','Ikke samme mål som periodens SFT'),
('Mulig boligeffekt på fertilitet','NOU peker på bolig som mulig barriere sammen med andre drivere','K163','U','Ingen egen kausal estimering'),
('Dødsfall og frigjorte boliger','Sammenhengen kan ikke utledes direkte fra nasjonalt antall døde','K152 K155 K156','U','Krever registerkobling'),
('Omflytting og boligverdier','Kommuneframskrivingene tilsier regional heterogenitet','K153','D','Ikke en boligprisprognose'),
('Frisk aldring og personell','Lavere andel i institusjon over tid endrer behovsmiks','K158','B','Andel og intensitet ikke kausal'),
('Arbeidstid og skattebase','Økt yrkesdeltakelse kan dempe budsjettpress','K170','D','Fiskal scenariorespons'),
('Husholdningsmodell 2050','Nasjonal følsomhet for antatt effektiv husholdningsstørrelse','K152 K155','D','Eget scenario, ikke SSB prognose'),
('Hjemmetjenestemodell 2050','Brukerbehov sensitivt for frekvensen og antall 80+','K157 K165','D','Eget scenario, ikke SSB prognose'),
('Langsiktige innvandringsanslag','MMM 2050 nettoinnvandring 17 071','K152','D','SSB MMM framskriving'),
('Lav/high-variant spredning','Følsomt for migrasjon, fruktbarhet og levealder','K169','D','Scenarioer er ikke sannsynlighetsintervall'),
('Barnetall og arbeidskraft i 2050','Økt fertilitet gir flere barn før voksne arbeidstakere','K168 K163','D','Livsløpsmekanisme, ikke egen strukturell kalibrering')
]
assert len(claims)==40
EV=[]
for i,(title,claim,source,cls,status) in enumerate(claims,1):
    hypo=f'H09-{min(14,1+(i-1)%14):02d}'
    EV.append(dict(id=f'E09-{i:03d}',tittel=title,traad='09',utsagn=claim,evidensklasse=cls,status=status,tillit='Høy for avleste SSB-tall' if cls=='A' else 'Betinget, ikke selvstendig kausal identifikasjon',primaerkilde=source,kilde_id=source.split()[0],hypotese=hypo,resultat=claim,mothypotese=HY[(i-1)%14]['mothypotese'],variabler=HY[(i-1)%14]['variabler'],empirisk_test=HY[(i-1)%14]['empirisk_test'],falsifikasjonskriterium=HY[(i-1)%14]['falsifikasjonskriterium'],datavintage=DATE,begrensninger='Les presis datastatus og serieproveniens; framskrivinger er betingede, ingen kausal egenanalyse',epistemisk_rolle='Beskrivende statistikk' if cls=='A' else 'Scenario eller forskningshypotese',ansvar='Norsk Økonomi, forskningstråd 09',registrert=DATE,forskningslitteratur='K163 K165 K167',kildereferanser_kontrollert=source))
save('evidensregister_09',EV)

fmt=lambda n:f'{n:,}'.replace(',',' ')
regiontable='\n'.join(f"| {r['fylke']} | {fmt(r['observert_2026'])} | {fmt(r['framskrevet_2050'])} | {r['prosent']:+.1f} % |".replace('.',',') for r in REG)
ptab='\n'.join(f"| {x['aar']} | {fmt(x['MMM'])} | {fmt(x['LLL'])} | {fmt(x['HHH'])} | {'Registrert' if x['aar']==2026 else 'Framskrevet'} |" for x in POP)
ftab='\n'.join(f"| {x['aar']} | {str(x['MMM']).replace('.',',')} | {str(x['LMM']).replace('.',',')} | {str(x['HMM']).replace('.',',')} |" for x in FERTF)
hh_table='\n'.join(f"| {x['type']} | {fmt(x['antall'])} | {x['antall']/2672051*100:.1f} % |".replace('.',',') for x in HH)
dtab='\n'.join(f"| {r['aar']} | {fmt(r['dode'])} | {r['status']} |" for r in DEATH)
htab='\n'.join(f"| {x['id']} | {x['tittel']} | {x['empirisk_test']} |" for x in HY)

report=r'''---
tittel: "09 — Demografi, arbeidskraft, boligetterspørsel og velferdsstatens bærekraft 2050–2100"
prosjekt: "Norsk Økonomi"
dato: "2026-10-13"
utgave: "1.1.0"
språk: "nb-NO"
status: "Foreløpig deskriptiv forskningsdelrapport; ikke fagfellevurdert"
---

# 09 — Demografi, arbeidskraft, boligetterspørsel og velferdsstatens bærekraft 2050–2100

**Prosjekt:** Norsk Økonomi  
**Dato og datagrense:** 13. oktober 2026  
**Status:** Kildekontrollert deskriptiv kartlegging av eksisterende forskning og offisielle framskrivinger; egne betingede følsomhetsberegninger, ingen ny registerkoblet kausalestimering.  
**Tverrtråder:** 03 Bolig og kreditt; 04 Generasjon; 05 Arbeidsmarked; 07 Ressursallokering; 08 Oljefond/finans; 10 Systemdynamikk.

## Sammendrag

**Hovedkonklusjon:** Det foreligger sterk dokumentasjon for at Norge blir vesentlig eldre og for at aldringen skjer svært ulikt mellom kommuner. Likevel er verken nasjonal boligpriskollaps eller finanspolitisk kollaps en nødvendig følge. Hovedalternativet i SSBs befolkningsframskrivinger av 12. juni 2026 innebærer at folketallet **øker** fra 5 627 400 i 2026 til 6 214 071 i 2050 og 6 384 547 i 2100, mens veksten konsentreres sterkere i eldre aldersgrupper. Lav- og høyalternativet for 2100 er henholdsvis 3 827 160 og 9 712 698; dette er **betingede scenarioer, ikke en prognosesannsynlighetsfordeling**. [K152](#k152) [K165](#k165)

Et viktig demografisk vendepunkt i hovedalternativet er 2032, da gruppen 65+ blir større enn 0–19-åringene. Antall 80+ øker fra om lag 285 000 i 2026 til om lag 462 000 i 2040 og mer enn det dobbelte av utgangsnivået innen 2050. Ved inngangen til 2050 er 80+-andelen anslått til omtrent 9,5 prosent i den nasjonale hovedrapporten. Omsorgspresset avhenger imidlertid av **funksjonsnivå, faktisk tjenestefrekvens, ressursintensitet og arbeidskraft**, ikke bare antall eldre. [K158](#k158) [K165](#k165)

2026-registeret viser 2 672 051 privathusholdninger, hvorav 1 103 955 aleneboende. Boligregisteret viser 2 762 504 boliger, både bebodde og ubebodde. Differansen **90 453** er ikke et mål på salgbare ledige boliger: registrene har forskjellige telleenheter, og boligene kan være feil geografisk plassert, ikke tilgjengelige eller ha registreringsavvik. [K155](#k155) [K156](#k156)

SSB anslår 60 588 dødsfall i 2050 mot 45 040 registrert i 2025. Dette er **ikke** 60 588 boliger frigjort for salg: flere avdøde tilhører samme husholdning, etterlevende kan bli boende, ikke alle eier bolig, og boliger kan beholdes eller flyttes over til arv/utleie. Modellen for framtidig salgbart boligtilbud må derfor arbeide på individ–husholdning–eiendom–region-nivå. [K152](#k152)

For helsepersonell anslår den offentlige Helsepersonellplanen fra juni 2026 et personellgap på **42 400 i 2040** dersom trendene fortsetter. Dette er ikke antallet omsorgsårsverk som allerede mangler i 2026, og heller ikke et tillegg som kan legges til SSBs 163 755 årsverk i kommunal omsorg i 2025. Samtidig anslår Nasjonalbudsjettet 2027 et betinget finansieringsbehov i 2060 på 5,8 prosent av Fastlands-BNP. Kausal fordeling på demografi, pensjon, helse, arbeidskraft og fondsbruk er ikke beregnet på nytt i denne delrapporten. [K157](#k157) [K160](#k160) [K162](#k162)

## 1. Problemstillinger, operasjonalisering og forskningsnivå

Undersøkelsen stiller følgende åpne spørsmål: Hvordan påvirker fødselskull, dødelighet, levealder og flytting befolkningsstrukturen regionalt? Hvor mye ny boligetterspørsel dannes i hver region når husholdningsstørrelse og boligtype endres? Hvilke boliger frigjøres faktisk ved dødsfall, flytting og nedskalering, og kan de omsettes til forventet markedsverdi? Hvordan påvirker endret aldersstruktur arbeidstilbud, pensjoner, kommunale skatteinntekter og omsorgstjenester? Hvilke mottiltak kan ha dokumenterbare effekter?

Observasjoner er **A** (beskrivende data), statistisk sammenheng **B**, kausalt identifiserte estimater **C**, og eksplisitt betingede systemmodeller **D**. Uavklarte kausalhypoteser merkes **U**. Framskrivinger er D selv når de er publisert av SSB: kvaliteten på dataene gjør ikke fremtiden til en observert hendelse. Prosjektet har ikke gjennomført egne C-studier på dette materialet.

## 2. Datagrunnlag og avgrensning

Primærgrunnlaget er SSBs nasjonale og regionale befolkningsframskrivinger publisert 12. juni 2026, registerstatistikk om husholdninger (30. september 2026), boliger (3. mars 2026), fødte (12. mars 2026) og omsorg (15. juni/21. september 2026), Helsepersonellplan 2040, NOU 2026: 2 og Nasjonalbudsjettet 2027. [K152](#k152) [K153](#k153) [K154](#k154) [K155](#k155) [K156](#k156) [K157](#k157) [K158](#k158) [K159](#k159) [K163](#k163) [K162](#k162)

Folketallet er definert som registrert bosatt ved inngangen til 2026 og framskrevet 1. januar i senere år. Husholdninger telles etter registeradresser, mens boligmasse bygger på Matrikkelen og omfatter både bebodde og ubebodde enheter. Netto boligbestandsendring er noe annet enn brutto fullførte boliger. Fødsler, dødsfall og nettoinnvandring er **årlige hendelser/strømmer**, mens folketall, husholdninger og boligmasse er **beholdninger på en dato**. Å trekke tallene fra hverandre uten felles populasjon og periodisering gir en feilslutning.

Regionalmodellens fylkestall summerer til **6 195 859 i 2050**, mens den nasjonale modellen gir **6 214 071**. Avviket på **18 212 personer** er ikke en regnefeil; SSB bruker to separate kohortkomponentmodeller, BEFREG og BEFINN, og gjør oppmerksom på at regionene ikke nødvendigvis summerer til nasjonal modell. Vi bruker derfor 6 195 859 **bare** ved summering av fylker, og 6 214 071 for nasjonale følsomhetsberegninger. [K169](#k169)

SSBs nasjonale alternativer: MMM (middels fruktbarhet, levealder og innvandring), LLL (lav nasjonal vekst) og HHH (høy). De regionale alternativene har fire komponenter, derfor hovedalternativet **MMMM**; den ekstra komponenten er innenlandsk flytting. Utsagnet «hovedalternativ» betyr ikke høy sannsynlighet for et enkelt utfall. [K169](#k169)

## 3. Framskrevet folketall 2026–2100

| År | MMM hovedalternativ | LLL lavalternativ | HHH høyalternativ | Datastatus |
|---|---:|---:|---:|---|
@@POP@@

SSBs hovedalternativ innebærer nasjonal befolkningsvekst på **10,4 prosent fra 2026 til 2050**, og deretter langt svakere vekst fram mot 2100. I lavalternativet faller befolkningen betydelig, mens høyalternativet gir sterk vekst. Alternative forutsetninger om innvandring, fruktbarhet og levealder kan derfor gi svært ulike framtidige skatte-, bolig- og tjenestegrunnlag. Tidsserien er hentet fra en og samme 2026-vintage og er publisert separat som CSV/JSON. [K152](#k152)

### 3.1 Aldring og vendepunkt

SSBs hovedalternativ gir flere 65+-åringer enn personer 0–19 i **2032**. Antallet personer 80+ var om lag 285 000 i 2026; i 2040 ventes det rundt 462 000. SSBs hovedrapport angir rundt **9,5 %** 80+ i 2050 (om lag 590 000 ved omregning mot folketallet 2050), og over 15 % rundt 2100. Den tilhørende journalistiske SSB-artikkelen bruker formuleringen «over 10 prosent i 2050»; forskjellen mellom formuleringene er derfor registrert som en **kildeintern avklaringssak**. For prosentanslaget brukes her rapport 2026/21 som definisjonskilde, ikke en falsk oppgitt presisjon. [K158](#k158) [K165](#k165) [K164](#k164)

Det er ikke bare antallet eldre som betyr noe. SSB viser at eldre oftere bor alene, at kommunenes tilgang på yrkesaktive varierer, og at noen kommuner har en aldersstruktur som allerede er vesentlig eldre enn landsgjennomsnittet. Et samlet nasjonalt forsørgelsesforhold kan skjule stor lokal variasjon. Sammenlign derfor både 65+/20–66, 80+/20–66 og **faktisk sysselsatte, justert for timeverk, deltidsandel og omsorgstid**. Aldersgrupper er ikke identiske med faktiske pensjonister eller skattebetalere.

### 3.2 Innvandring og naturlig tilvekst

SSB anslår nettoinnvandring til 20 563 i 2026, 17 071 i 2050 og om lag 15 113 i 2100 i hovedalternativet. Det forventes fødselsoverskudd fram til midten av 2040-årene, deretter fødselsunderskudd. Dermed blir migrasjon den direkte årsaken til videre nasjonal befolkningsvekst etter dette tidspunktet i hovedalternativet. Nettoinnvandring kan også påvirke den framtidige yrkesbefolkningen, men virkningen avhenger av alder ved innflytting, fullføring av utdanning, sysselsetting, botid og eventuell utvandring. [K152](#k152) [K165](#k165)

## 4. Fruktbarhet, ønsket og realisert familieetablering

Observerte SSB-tall viser at samlet fruktbarhetstall falt fra 1,73 i 2015 til 1,44 i 2024, før det økte til **1,48 i 2025**. Gjennomsnittsalderen for førstegangsfødende kvinner var 30,4 år i 2025. Dette er **periodemål**, ikke antallet barn en faktisk fødselskohort til slutt får. [K154](#k154)

| År | MMM-forutsetning | Lav fruktbarhet (LMM) | Høy fruktbarhet (HMM) |
|---|---:|---:|---:|
@@FTAB@@

Disse tallene er **modellforutsetninger fra 2026**, ikke målt utvikling i framtiden. De må ikke tegnes sammen med observerte fruktbarhetstall uten en tydelig bruddlinje og etikett. [K152](#k152)

NOU 2026: 2 dokumenterer at kvinner og menn ofte ønsker første barn tidligere enn de faktisk får det. Eldre spørreundersøkelser gjengitt i utredningen viser gjennomsnittlige **ideelle barnetall** på henholdsvis 2,36 blant kvinner og 2,09 blant menn i 2019, og rundt 2,25 blant kvinner i GGS 2020. Disse survey-tallene er **ikke direkte sammenlignbare med SFT på 1,48 i 2025**: de gjelder ulike populasjoner, ulike år, intensjoner kontra periodemål, og et ideelt antall er ikke et observerbart realisert kohortutfall. Fødselstallsutvalget peker på samliv, utdanning, arbeidsmarked, helse, normer, tidsbruk, inntekt og bolig som mulige samtidige mekanismer. [K163](#k163) [K167](#k167)

Forskningstrådene 03 og 04 gir bolig- og generasjonsmekanismer å teste, men vi kan **ikke** tilskrive det samlede fallet i fødselstall direkte til boligpriser uten longitudinelle data og identifikasjon. Vi foreslår en hendelsesstudie av boligprissjokk/kredittgrenser og fødselsrisiko, med kontroll for partnerskap, alder, inntekt, arbeidsstatus, utdanning, fertilitetsbehandling og selektiv flytting. Vurder virkninger på første, andre og tredje barn separat.

## 5. Regional befolkningsutvikling og boligetterspørsel

| Fylke | Observert 2026 | MMMM 2050 | Endring 2026–2050 |
|---|---:|---:|---:|
@@REG@@

De 15 fylkene summerer til 6 195 859 i regional MMMM, ikke 6 214 071 i nasjonal MMM. Dette er forventet modellavvik, dokumentert hos SSB. [K169](#k169)

Akershus og Oslo vokser ifølge hovedalternativet med omtrent **20 % og 16 %** fram mot 2050, mens Nordland er eneste fylke med anslått nedgang (**−3,0 %**). Hele **63 % av kommunene** er anslått å vokse, men resten kan få nedgang og samtidig sterkere aldring. Dette gir et helt annet bilde av framtidig boligetterspørsel enn en landsdekkende tese om at dødsfall fører til fallende boligverdier. Tallene sier likevel ingenting direkte om boligprisene, rentenivået eller hvilke boliger innflyttere trenger. [K153](#k153) [K166](#k166)

### 5.1 Husholdninger og boligbestand

SSB registrerte **2 672 051 privathusholdninger** i 2026:

| Husholdningstype | Antall 2026 | Andel |
|---|---:|---:|
@@HH@@

Boligregisteret viste **2 762 504 boliger**, inkludert bebodde og ubebodde enheter. Nettotilveksten i registrert boligmasse siste år var **18 761**. Differansen mellom antall registrerte boliger og antall privathusholdninger var 90 453, men denne differansen kan **ikke** tolkes som et overskudd av boliger som faktisk kan kjøpes, leies eller tas i bruk. Statistikken omfatter forskjellige objekter og kan påvirkes av studenter, institusjoner, sekundærboliger, fritidsbruk, ukjente bruksforhold og etterslep i Matrikkelen. [K155](#k155) [K156](#k156)

### 5.2 Mekanisk husholdningsfølsomhet – ikke en boligprognose

Som åpent, avgrenset regneeksempel settes 2026-husholdninger H0 = 2 672 051 og nasjonalt folketall P0 = 5 627 400. En effektiv befolkning/husholdning-rate kan da beregnes som 2,106. Ved gitt SSB-folketall i 2050 og valgt, hypotetisk framtidig effektiv rate `s` beregnes H2050 = P2050 / s. Alternativene s=1,9, 2,1 og 2,3 viser hvor sterk følsomheten er for sammensetning av husholdninger. I beregningen er **hele nasjonale folketallet** brukt, også institusjonsbefolkning. Dette kan ikke erstatte egentlige husholdningsframskrivinger, men er et transparent «hva-hvis»-regnestykke for å identifisere nøkkelusikkerheten.

Det kreves en fullført modell med husholdningsdannelsesrater per kommune, alder, kjønn, familieform, botid og leie/eie, slik at samme person aldri telles i flere husholdninger. Deretter må boligtype, lokalisering, tilgang til transport/arbeidsmarked, funksjonstilpasning og faktisk pris likviditet kobles til tilbudssiden.

### 5.3 Dødsfall og frigjorte boliger er ikke samme strøm

| År | Antall dødsfall | Datastatus |
|---|---:|---|
@@DOD@@

Det offisielle hovedalternativet anslår **60 588 dødsfall i 2050** mot **45 040 i 2025**. For å estimere netto tilgjengelig boligforsyning som følger av dødsfall må vi identifisere: (1) om avdøde eide bolig, (2) om etterlevende fortsetter husholdningen, (3) om boligen selges, leies ut, arves til eget bruk eller blir stående tom, (4) geografisk beliggenhet og boligtype, (5) parallell flytting og ny husholdningsdannelse. Samme bolig kan ikke telle som frigjort mer enn én gang ved to dødsfall i samme parhusholdning. [K152](#k152)

Boligformue kan svekkes i avfolkningsområder uten å svekkes i innflyttingsområder. Et aggregert «samlet norsk boligformue» skjuler markedets omsetningsdybde. Hypotese H09-03/H09-12 skal testes mot faktiske skjøter, dødsfall og boligpriser regionalt.

## 6. Omsorg, helsetjenester og personellbehov

I 2025 hadde kommunale omsorgstjenester **163 755 årsverk** og utgifter på **184,7 mrd. kroner**. Hjemmetjenester hadde 70 662 brukere i alderen 80+ og institusjonstjenester 27 039 i samme aldersgruppe. Tjenestene gjelder også mange yngre personer, og brukere og årsverk må ikke sammenliknes som én entydig rate. Det var 39 727 sykehjemsplasser på måletidspunktet. [K157](#k157) [K158](#k158)

SSB viser at andelen eldre som er på langtidsopphold i institusjon har falt over tid. Dette kan uttrykke friskere eldre, strengere tildeling, skifte mot hjemmetjenester eller endret registrering – og brukere med omfattende behov kan samtidig kreve mer tid per bruker. Det er derfor **for lite å multiplisere antall eldre med en fast omsorgskostnad**. En forsvarlig modell følger separate brukerandeler for 67–79, 80–89 og 90+, institusjon/hjemmetjenester, omsorgstimer, kvalitet, helsetilstand og potensielle arbeidsbesparende løsninger. [K158](#k158)

### 6.1 To forskjellige offentlige bemanningsmodeller

**Helsepersonellplan 2040 (2026)** oppgir et beregnet gap på **42 400 helsepersonell i 2040** dersom dagens trender fortsetter. Dette er et gap mellom framskrevet tilbud og etterspørsel etter helsepersonell, og gjelder langt bredere tjenester enn bare kommunal omsorg. [K159](#k159) [K160](#k160)

**Helsepersonellkommisjonens NOU 2023: 4** viste i et eldre HELSEMOD-referansealternativ 460 000 årsverk og 18 % av sysselsatte innen helse og omsorg i 2040; for 2060 var tallene 561 000 årsverk og 22 %. Dette er en **eldre vintages betingede prognosebane**, ikke det samme som gapet 42 400 i den nye planen. Tallene skal ikke adderes eller brukes som om definisjoner, datavintager og antakelser er identiske. [K161](#k161)

### 6.2 Åpent følsomhetsregneeksempel for hjemmetjenester 80+

Den nye nettsidens illustrasjon bruker SSBs omtrentlige 80+-befolkning i 2050, og lar tjenestefrekvensen være 15–35 %. Ved en hypotetisk stabil frekvens på **24,8 %** tilsier rundt 590 000 eldre omtrent **146 000 personer 80+ med hjemmetjeneste i 2050**. Dette er en *regneillustrasjon*, ikke en offisiell SSB-framskriving av antall brukere, tjenestetimer eller årsverk. Andelen vil kunne variere med alderssammensetning innen gruppen 80+, helsetilstand og prioriteringskriterier. [K157](#k157) [K165](#k165)

## 7. Arbeidskraft, produktivitet og generasjonsregnskap

Det relevante forsørgergrunnlaget er faktisk produsert arbeid og skattepliktig inntekt – ikke bare personer i alderen 20–66. En eldre befolkning kan få høyere arbeidstilbud dersom flere arbeider lenger, samtidig som helse, ulik yrkessammensetning og uførhet kan begrense muligheten. Det er derfor nødvendig å måle *timeverk* og produktivitet per yrkesaktiv kohort, ikke bare jobbandel. Finansdepartementet har tidligere vist at endrede forutsetninger om eldre yrkesdeltakelse kan gi betydelig andre resultater; utgaver med ulike demografiske forutsetninger må merkes som egne analyser. [K170](#k170)

Bedre fruktbarhet bidrar til flere arbeidstakere **etter et langt etterslep**, men øker først ressursbehovet til svangerskapsomsorg, barnehage, skole og familier. Netto budsjetteffekt for 2030–2040 kan dermed avvike fra nettoeffekten i 2060–2100. Nettoinnvandring kan gi raskere effekt hvis innflytterne er yrkesaktive og kommer i arbeid, men framtidig aldring og tjenester må inkluderes. Dette er illustrasjoner av demografisk livsløpsregnskap, ikke anslag på best egnet innvandrings- eller familiepolitikk.

Det foreslås et generasjonsregnskap med fødselskull 1945–2005, offentlig skatt/trygd/tjenester ved alder 25/30/35/40/50/60/70, arbeidstimer, boligformue og netto overføringer; resultatene skal føres både med og uten SPU-finansiering. Husholdningsgevinster ved boligbytte og redusert boligkostnad må skilles fra regnskapsmessig nasjonal velstandsgevinst. Dette arbeidet avhenger av datadeling i tråd 03, 04 og 08.

## 8. Statsfinansielle konsekvenser og samvirkende risiko

Nasjonalbudsjettet 2027 anslår et **betinget inndekningsbehov på 5,8 % av Fastlands-BNP i 2060**, sammenlignet med 6,2 % i Perspektivmeldingen 2024. Endringen er en oppdatert *modellvintage*, ikke en måling av en realisert forbedring i framtidige statsfinanser. Et demografidrevet finansieringsgap kan forsterkes av vekst i pleiebehov, lønnskostnader og pensjoner, og dempes av høyere arbeidstid, produktivitet, helsegevinster og rente-/fondsavkastning. [K162](#k162) [K168](#k168)

**Det er ikke estimert hvor stor del av 5,8 % som utelukkende skyldes aldring**. Å tilskrive hele gapet til eldrebølgen ville være metodisk uholdbart fordi referansemodellen også omfatter offentlige tjenester, skattesystem, arbeidsinnsats, fondets forventede avkastning og andre faktorer. Her kobles i stedet variablene til modell i forskningstråd 08, med ulike befolknings- og produktivitetsforutsetninger som framtidig testdesign.

## 9. Alternative forklaringer, motfunn og falsifikasjon

- **Nasjonalt boligmarked:** Befolkningen i hovedalternativet vokser – ingen offisiell støtte for automatisk nasjonal kollaps i boligetterspørsel. Lokal nedgang og lav likviditet kan likevel være betydelig.
- **Demografisk aldring:** Dette er robust på tvers av mange SSB-scenarioer. Hvor mye omsorgsbehov det skaper, er mer usikkert.
- **Lav fruktbarhet:** 2025-tallet viser oppgang fra 2024, og NOU 2026: 2 oppgir flere samtidige forklaringer. Housing-only-forklaringen er ikke bevist.
- **Omsorgsbehov:** Andelen institusjonsboende eldre har falt, men det kan være både helseeffekt og strammere kriterier. Bedret levealder innebærer ikke automatisk like mange ekstra friske år.
- **Migrasjon:** Positiv nettoinnvandring kan dempe fall i arbeidsfør befolkning, men resultater varierer med sysselsetting, integrering og framtidig utvandring.
- **Arbeidstilbud:** Økt eldre yrkesdeltakelse kan motvirke demografisk forsørgerbyrde. Likevel kan total etterspørsel etter helsepersonell vokse raskere enn tilgangen.
- **Fiskal modell:** Et finansieringsgap er et tilpasningsbehov i en betinget referansebane, ikke predikert mislighold eller konkurs.

## 10. Hypoteser, motforklaringer og testplan

Fullstendig forskningsregister: `data/hypoteseregister_09.json` og `data/evidensregister_09.json`. Alle hypotesene under er registrert som **U** til egen test har gitt et resultat. Hver post inneholder primærkilder, falsifikasjonskriterium og kunnskapshull.

| Hypotese | Tema | Foreslått empirisk test |
|---|---|---|
@@HYP@@

**P0 — data for befolkning:** Harmoniser SSB 2026-tabell 14740/14742 nasjonalt og 14746 regionalt, etter alder, kjønn og migrasjon. Fastslå om fylkesresultater aggregerer til samme nasjonale totaler i lik vintage (kontrollen er allerede utført for 2026/2050), og dokumenter revisjoner.

**P0 — bolig:** Bygg individ/husholdning/bygning-registerpanel 2005–2025 med internflytting, dødsfall, boligoverdragelse, type, faktisk tilgjengelighet, eierstatus og pris/omsetning. Beregn nye husholdninger minus netto frigjorte boliger, lokalt, ikke bare nasjonalt.

**P0 — omsorg:** Estimer alders- og kjønnsspesifikke brukerandeler og timer per mottaker 2015–2025, og alternative baner til 2060, inkludert personellreserve, sykefravær, kompetanse, kvalitet og bemanningsnormer. Sammenlign ny HELSEMOD-vintage med NOU 2023:4, uten å slå dem sammen.

**P0 — finanspolitikk:** Føl opp inntekter, pensjoner, tjenester, kommuneutgifter og arbeidsdeltakelse i fire befolknings- og produktivitetsbaner. Legg inn konsistent deflator, diskontering og GPFG-norm. Avstem komponentene til Finansdepartementets 2060-gap før egne politiske kontrafakta gjennomføres.

**P1 — fruktbarhetsmekanismen:** Hendelsesanalyse av faktisk førstefødsel etter endringer i boligpriser/kredittkrav, langsiktige barneønsker, arbeidsmarked og partnerskap. Skill effekter for første, andre og tredje fødsel.

**P1 — årsaksidentifikasjon:** Evaluer kommunale omsorgs- og arbeidsmarkedstiltak med egnet sammenligningsgruppe, før-etter-målinger, sammenlignbar datadefinisjon og følsomhetsanalyse.

## 11. Forskningsetikk, transparens og kilder

SSBs framskrivinger er **ikke løfter om framtiden**. Scenarioresultater skal ikke brukes til å beregne personlige pensjoner, skattevedtak eller verdien av bestemte boliger. Ingen personidentifiserbare individdata er lastet ned eller publisert. Personvern og forskningsetisk hjemmel må avklares før registerkobling. Rapportens forskningsgrunnlag er primært offentlig tilgjengelig aggregert statistikk og dokumenter; det er ikke gjennomført ekstern fagfellevurdering.

**KI-erklæring:** ChatGPT fra OpenAI er brukt til forskningsstrukturering, søkeassistanse, kildekompilering, utkast, beregningskontroll, kode og interaktiv publisering. Flere kategorier KI-verktøy er beskrevet på prosjektnivå; spesifikke modeller uten verifiserbar logg oppgis ikke som faktiske brukte produkter. KI er ikke primærkilde, og alle empiriske tall skal spores til de navngitte dokumentene. Prosjektansvarlig har ansvaret for videre ekstern kontroll og eventuell publisering.

**Foreslått sitering:** Norsk Økonomi (2026). *Demografi, arbeidskraft, boligetterspørsel og velferdsstatens bærekraft, 2050–2100*. Foreløpig delrapport 09, versjon 1.1.0, 13. oktober 2026. Ikke fagfellevurdert.

## Referanser i delrapport 09

@@SOURCES@@
'''
report=report.replace('@@POP@@',ptab).replace('@@REG@@',regiontable).replace('@@FTAB@@',ftab).replace('@@HH@@',hh_table).replace('@@DOD@@',dtab).replace('@@HYP@@',htab)
refs='\n'.join(f'<a id="k{n}"></a> **K{n} — {org}.** {ref}' for n,org,ref in SOURCES)
report=report.replace('@@SOURCES@@',refs)
out=R/'09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md';out.write_text(report,'utf8')
print('sources',len(SOURCES),'hypotheses',len(HY),'evidence',len(EV),'report_words',len(report.split()),'region size',len(REG),'file',out)
