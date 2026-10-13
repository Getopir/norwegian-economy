#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transkriberer offentlige 2026-kilder og oppretter første dokumenterte studie i forskningstråd 07.
Manuelle observasjoner må ved ny datavintage kontrolleres mot SSB/DFØ/Riksrevisjonen.
"""
import json,csv,hashlib,datetime,math,re
from pathlib import Path
R=Path(__file__).resolve().parent;D=R/'data';D.mkdir(exist_ok=True)
STAMP='2026-10-12'
SOURCES=[
(113,'Statistisk sentralbyrå (2026)','Offentlig forvaltnings inntekter og utgifter. Tabell 14668 og 14669; oppdatert 7. september 2026. https://www.ssb.no/offentlig-sektor/offentlig-forvaltning/statistikk/offentlig-forvaltnings-inntekter-og-utgifter'),
(114,'Statistisk sentralbyrå, M. H. Skjæveland (2025)','1 av 3 jobber i offentlig forvaltning. Publisert 15. august 2025; tabell 11655. https://www.ssb.no/arbeid-og-lonn/sysselsetting/statistikk/antall-arbeidsforhold-og-lonn/artikler/1-av-3-jobber-i-offentlig-forvaltning'),
(115,'Direktoratet for forvaltning og økonomistyring (2026)','Utgifter til offentlige innkjøp. Regnskapsbasert statistikk for 2025; definisjoner og hovedrevisjon. https://www.anskaffelser.no/data-statistikk-og-analyse/utgifter-til-offentlige-innkjop'),
(116,'Riksrevisjonen (2026)','Dokument 3:15 (2025–2026): Myndighetenes arbeid med å sikre effektiv ressursbruk i offentlig sektor. Offentliggjort 10. juni 2026. https://www.riksrevisjonen.no/rapporter-mappe/no-2025-2026/myndighetenes-arbeid-med-a-sikre-effektiv-ressursbruk-i-offentlig-sektor/'),
(117,'OECD (2026)','OECD Economic Surveys: Norway 2026. OECD Publishing, Paris, 17. juni 2026. https://www.oecd.org/en/publications/oecd-economic-surveys-norway-2026_5cc02644-en.html'),
(118,'Statistisk sentralbyrå','Fylkesfordelt nasjonalregnskap – ofte stilte spørsmål. Forklarer kostnadsbasert verdsetting av offentlig produksjon. https://www.ssb.no/nasjonalregnskap-og-konjunkturer/fylkesfordelt-nasjonalregnskap-ofte-stilte-sporsm%C3%A5l/'),
(119,'Schreyer, P., OECD (2010)','Towards Measuring the Volume Output of Education and Health Services: A Handbook. OECD Statistics Working Papers 2010/02. https://doi.org/10.1787/5kmd34g1zk9x-en'),
(120,'Baumol, W. J. (1967)','Macroeconomics of Unbalanced Growth: The Anatomy of Urban Crisis. American Economic Review 57(3), 415–426; bibliografisk oversikt ved University of Bristol. https://www.bristol.ac.uk/Depts/Economics/Growth/refs/baumol.htm'),
(121,'OECD (2025)','Health at a Glance 2025: Norway. Landnotat, 13. november 2025. https://www.oecd.org/en/publications/health-at-a-glance-2025_15a55280-en/norway_3b4abde5-en.html'),
(122,'Utdanningsdirektoratet / Universitetet i Oslo (2023)','PISA 2022: Betydelig nedgang i lesing, matematikk og naturfag. 5. desember 2023. https://www.udir.no/tall-og-forskning/finn-forskning/rapporter/2023/betydelig-pisa-nedgang/'),
(123,'Samferdselsdepartementet (2024)','Meld. St. 14 (2023–2024), Nasjonal transportplan 2025–2036. Samfunnsøkonomiske analyser i planporteføljen. https://www.regjeringen.no/contentassets/aaee20cf5a9e468ea97fd51638c42407/no/pdfs/stm202320240014000dddpdfs.pdf'),
(124,'Finansdepartementet (2024)','Meld. St. 31 (2023–2024), Perspektivmeldingen 2024. Referansebaner og inndekningsbehov. https://www.regjeringen.no/no/dokumenter/meld.-st.-31-20232024/id3049290/?ch=7'),
(125,'Finansdepartementet (2025)','Meld. St. 1 (2025–2026), Nasjonalbudsjettet 2026, kapittel 3: Oppdatert langsiktig inndekningsbehov. https://www.regjeringen.no/no/dokumenter/meld.-st.-1-20252026/id3123808/?ch=3'),
(126,'NAV (2026)','Lav vekst i antall uføretrygdede i 2025. 12. februar 2026; 2025 helårsdata. https://www.nav.no/no/nav-og-samfunn/statistikk/aap-nedsatt-arbeidsevne-og-uforetrygd-statistikk/nyheter/lav-vekst-i-antall-uforetrygdede-i-2025'),
(127,'Statistisk sentralbyrå (2026)','Sykefravær, 2. kvartal 2026, sesongjusterte tabeller 12439 og 13935, oppdatert 3. september 2026. https://www.ssb.no/arbeid-og-lonn/arbeidsmiljo-sykefravaer-og-arbeidskonflikter/statistikk/sykefravaer'),
(128,'Finansdepartementet (2025)','Nasjonalbudsjettet 2026, kapittel 5.4: Effektiv offentlig ressursbruk. https://www.regjeringen.no/no/dokumenter/meld.-st.-1-20252026/id3123808/?ch=5'),
(129,'Statistisk sentralbyrå (2026)','Kommuneregnskap / KOSTRA, 2025-regnskap og definisjoner. https://www.ssb.no/offentlig-sektor/kommunale-finanser/statistikk/kommuneregnskap/'),
(130,'Direktoratet for forvaltning og økonomistyring (2025)','DFØ-notat 2025:7, Utviklingen i antall ansatte i statsforvaltningen 2023–2024, oppdatert 16. desember 2025. https://www.dfo.no/rapporter/utviklingen-i-antall-ansatte-i-statsforvaltningen-1'),
(131,'Riksrevisjonen (2025)','Dokument 1 (2025–2026), Årlig rapport til Stortinget om regnskapsrevisjon 2024. Offentliggjort 11. november 2025. https://www.riksrevisjonen.no/rapporter-mappe/no-2025-2026/arlig-rapport-til-stortinget-om-regnskapsrevisjon-2024/'),
(132,'Riksrevisjonen (2025)','Dokument 3:16 (2024–2025), Bruk av departementenes rammeavtale for konsulenttjenester på IKT-området. Offentliggjort 20. juni 2025. https://www.riksrevisjonen.no/rapporter-mappe/no-2024-2025/bruk-av-departementenes-rammeavtale-for-konsulenttjenester-pa-ikt-omradet/'),
(133,'OECD (2024)','OECD Economic Surveys: Norway 2024. Raising the Effectiveness of Public Spending. https://www.oecd.org/en/publications/oecd-economic-surveys-norway-2024_cb13475f-en/full-report/component-5.html'),
(134,'Statistisk sentralbyrå (2026)','Forsvarsutgiftene øker kraftig. 8. juni 2026; årsdata 2025 og historisk utgiftsandel av BNP. https://www.ssb.no/offentlig-sektor/offentlig-forvaltning/statistikk/offentlig-forvaltnings-inntekter-og-utgifter/artikler/forsvarsutgiftene-oker-kraftig'),
(135,'Statistisk sentralbyrå (2024)','Produktivitetsberegninger for næringer. Revidert etter hovedrevisjonen 2024; metodeforbehold for offentlig produksjon. https://www.ssb.no/nasjonalregnskap-og-konjunkturer/nasjonalregnskap/artikler/produktivitetsberegninger-for-naeringer'),
(136,'Helsedirektoratet (2026)','Nasjonalt kvalitetsindikatorsystem – årsrapport 2025. Indikatordekning og metodiske begrensninger, 30. mars 2026. https://www.helsedirektoratet.no/rapporter/nasjonalt-kvalitetsindikatorsystem-nki-arsrapport-2025/oversikt-over-nasjonale-kvalitetsindikatorer-i-2025')]
assert len(SOURCES)==24

def write_pair(stem,rows):
 (D/f'{stem}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 with (D/f'{stem}.csv').open('w',newline='',encoding='utf-8-sig') as f:
  if not rows: return
  writer=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for row in rows for k in row)),delimiter=';',extrasaction='ignore');writer.writeheader();writer.writerows(rows)

YEARS=[2021,2022,2023,2024,2025]
spend={
 'Inntekter': [2449364,3618188,3191777,3217991,3265786],
 'Løpende utgifter':[1932789,2081911,2265457,2441004,2602008],
 'Nettoinvestering i ikke-finansiell kapital':[70642,75426,83264,91290,82543],
 'Totale utgifter':[2003431,2157337,2348721,2532294,2684551],
 'Nettofinansinvestering':[445933,1460851,843056,685697,581235]}
SPEND=[{'aar':year,'indikator':key,'verdi_mill_kr':spend[key][i],'kilde_id':'K113','status':'SSB 14668 revidert 2026-09-07','nivaa':'Offentlig forvaltning, SNA/ESA'} for i,year in enumerate(YEARS) for key in spend]
write_pair('offentlige_hovedtall_07',SPEND)
COFOG={
 'Alminnelig offentlig tjenesteyting':[164512,188576,243960,274996,274613],
 'Forsvar':[72459,80934,91183,114902,171792],
 'Offentlig orden og trygghet':[44929,49396,51598,55149,59073],
 'Næringsøkonomiske formål':[246614,284344,286656,297062,313851],
 'Miljøvern':[35520,40262,42197,43416,46129],
 'Bolig og nærmiljø':[29840,35423,40113,45088,44925],
 'Helse':[320094,338567,362262,379793,391954],
 'Fritid, kultur og religion':[68988,71003,73963,76889,78883],
 'Utdanning':[207213,219688,233566,250111,254554],
 'Sosial beskyttelse':[813261,849145,923223,994887,1048776]}
EXPEND=[{'aar':year,'formaal':key,'verdi_mill_kr':COFOG[key][i],'kilde_id':'K113','status':'SSB 14669 revidert 2026-09-07','definisjon':'COFOG; generelle tjenester er ikke administrasjonskostnader'} for i,year in enumerate(YEARS) for key in COFOG]
assert abs(sum(COFOG[key][-1] for key in COFOG)-2684551)<=1
write_pair('cofog_utgifter_07',EXPEND)
EMP=[(2016,940980,1812516,34.2,32.4),(2017,954406,1838024,34.2,32.2),(2018,969214,1877981,34.0,32.2),(2019,980874,1923918,33.8,31.9),(2020,956947,1824142,34.4,33.1),(2021,997125,1845378,35.1,33.6),(2022,1015364,2022488,33.4,32.3),(2023,1033438,2052191,33.5,32.5),(2024,1048075,2064997,33.7,32.8),(2025,1052772,2089485,33.5,32.8)]
EMPLOY=[{'aar':yr,'offentlig_jobber':pub,'privat_og_offentlig_eid_jobber':pri,'offentlig_andel_jobber_prosent':shr,'offentlig_andel_maanedsverk_prosent':mon,'periode':f'{yr}K2','kilde_id':'K114','status':'Antall jobbforhold – ikke personer'} for yr,pub,pri,shr,mon in EMP]
write_pair('sysselsetting_offentlig_07',EMPLOY)
OTH=[
 {'indikator':'Offentlige innkjøp','periode':'2024','gruppe':'Offentlig forvaltning mv., SSB/DFØ','verdi':835,'enhet':'mrd. kr','kilde_id':'K115','status':'Nominell anskaffelsesstatistikk, revidert','merknad':'Bruttokjøp og investeringer; omfatter også offentlig forretningsdrift; ikke potensielt kutt'},
 {'indikator':'Offentlige innkjøp','periode':'2025','gruppe':'Offentlig forvaltning mv., SSB/DFØ','verdi':864,'enhet':'mrd. kr','kilde_id':'K115','status':'Omtrent, nominell','merknad':'Omtrent 864 milliarder; ikke utgift til administrasjon'},
 {'indikator':'Utgiftsandel samlet BNP','periode':'2024','gruppe':'Offentlig forvaltning','verdi':47.0,'enhet':'prosent','kilde_id':'K134','status':'SSB revidert','merknad':'Nevner: samlet BNP, ikke Fastlands-BNP'},
 {'indikator':'Utgiftsandel samlet BNP','periode':'2025','gruppe':'Offentlig forvaltning','verdi':48.7,'enhet':'prosent','kilde_id':'K134','status':'SSB revidert','merknad':'Nevner: samlet BNP, ikke Fastlands-BNP'},
 {'indikator':'Forsvar hovedbidrag årsvekst 2025','periode':'2025','gruppe':'COFOG forsvar','verdi':56.89,'enhet':'mrd. kr (økning fra 2024)','kilde_id':'K113 K134','status':'Egen aritmetikk fra SSB','merknad':'Ukraina-støtte forklarer mye; ikke vekst i administrasjon'},
 {'indikator':'Manglende spareinsentiver','periode':'2026-06','gruppe':'Spurte statlige virksomheter, n=144','verdi':'nesten to tredjedeler','enhet':'andel respondentvirksomheter','kilde_id':'K116','status':'Riksrevisjonens spørreundersøkelse','merknad':'Ikke to tredjedeler av ansatte eller statens budsjett'},
 {'indikator':'Uførhet 18–67','periode':'2025-12','gruppe':'Mottakere uføretrygd NAV','verdi':374900,'enhet':'personer, avrundet','kilde_id':'K126','status':'NAV desember 2025','merknad':'10,5 % av 18–67-åringer, stabil andel flere år'},
 {'indikator':'Uførhet andel','periode':'2025-12','gruppe':'18–67-åringer','verdi':10.5,'enhet':'prosent','kilde_id':'K126','status':'NAV desember 2025','merknad':'Andelen stabil fra 2020, ikke dokumentasjon på bratt økning'},
 {'indikator':'Sykefravær sesongjustert','periode':'2026K2','gruppe':'Alle næringer','verdi':6.68,'enhet':'prosent','kilde_id':'K127','status':'SSB sesongjustert','merknad':'Ikke samme størrelse som uføretrygd eller alle trygdeytelser'},
 {'indikator':'Sykefravær sesongjustert','periode':'2026K2','gruppe':'Helse- og sosialtjenester','verdi':9.61,'enhet':'prosent','kilde_id':'K127','status':'SSB sesongjustert','merknad':'Næringsgrupper, ikke organisasjonssektor; inkluderer private tjenester'},
 {'indikator':'Sykefravær sesongjustert','periode':'2026K2','gruppe':'Offentlig administrasjon og forsvar','verdi':5.68,'enhet':'prosent','kilde_id':'K127','status':'SSB sesongjustert','merknad':'Næringsgruppe, ikke hele offentlig forvaltning'},
 {'indikator':'Sykefravær sesongjustert','periode':'2026K2','gruppe':'Undervisning','verdi':6.66,'enhet':'prosent','kilde_id':'K127','status':'SSB sesongjustert','merknad':'Næringsgruppe, ikke hele offentlig forvaltning'},
 {'indikator':'Helseutgifter per innbygger PPP','periode':'2025','gruppe':'Norge','verdi':9393,'enhet':'USD kjøpekraftskorrigert','kilde_id':'K121','status':'OECD Health at a Glance 2025','merknad':'Samlede helseutgifter, offentlig og privat; ikke COFOG-utgift'},
 {'indikator':'Helseutgifter per innbygger PPP','periode':'2025','gruppe':'OECD-gjennomsnitt','verdi':5967,'enhet':'USD kjøpekraftskorrigert','kilde_id':'K121','status':'OECD Health at a Glance 2025','merknad':'Landreferanse, ulike tjenestemodeller og demografi'},
 {'indikator':'Forventet levealder','periode':'2025-rapport','gruppe':'Norge','verdi':83.1,'enhet':'år','kilde_id':'K121','status':'OECD landnotat','merknad':'Utfall påvirkes også av befolkningens levevaner og seleksjon'},
 {'indikator':'Forventet levealder','periode':'2025-rapport','gruppe':'OECD-gjennomsnitt','verdi':81.1,'enhet':'år (utledet fra oppgitt forskjell)','kilde_id':'K121','status':'Avledet beregning 83,1−2,0','merknad':'Ikke OECD direkte sitert absoluttverdi i landnotat'},
 {'indikator':'Inndekningsbehov referansebane','periode':'2060 (perspektivmeldingen 2024)','gruppe':'Norge','verdi':6.2,'enhet':'prosent Fastlands-BNP','kilde_id':'K124','status':'Betinget offentlig framskriving','merknad':'Ikke prognose for gjeld eller statsbankerott'},
 {'indikator':'Inndekningsbehov revidert referanse','periode':'2060 (Nasjonalbudsjettet 2026)','gruppe':'Norge','verdi':5.9,'enhet':'prosent Fastlands-BNP','kilde_id':'K125','status':'Betinget offentlig framskriving','merknad':'Revidert datavintage; ikke en ny observasjon for 2060'},
 {'indikator':'Prissatt netto nytte utvalgte NTP-investeringer','periode':'NTP 2025–2036','gruppe':'Store prosjekter prioritert oppstart, ekskl. Nye Veier','verdi':-125,'enhet':'mrd. kr','kilde_id':'K123','status':'NTP ex ante anslag','merknad':'Kun prissatte virkninger; ikke-prissatte nytte/kostnad inngår ikke'},
 {'indikator':'Prissatt netto nytte Nye Veier portefølje','periode':'NTP 2025–2036','gruppe':'Nye Veier-prosjekter','verdi':-17,'enhet':'mrd. kr','kilde_id':'K123','status':'NTP ex ante anslag','merknad':'Ikke prissatt total samfunnsnytte; prosjektutvalg avgjør'}]
write_pair('hovedindikatorer_07',OTH)

HYP=[
('H07-01','Administrasjonsressurser','Administrative kostnader vokser raskere enn etterspørsel og kvalitet skulle tilsi','Demografi, nye rettigheter, sikkerhetskrav og oppgaver forklarer veksten','K113 K116 K128 K129 K130','Administrative årsverk; COFOG underkoder; kommunal KOSTRA funksjoner; oppgavevolum; kvalitet','Kommune-/etatpanel med faste effekter, tjenestejustering, forskjeller mot kontroll','Ingen positiv resttrend etter kvalitet, oppgaver og geografi'),
('H07-02','Baumol-effekt på tjenestepriser','Lav relativ produktivitetsvekst i personintensive tjenester gir vedvarende relativ kostnadsvekst','Teknologi, endret behandling og kvalitetsheving dominerer kostnadsøkningen','K118 K119 K120 K135','Lønninger/timeverk, volum, kvalitet, brukertyngde, offentlig/privat sektor','Vekstregnskap sektorvis 1995–2025, kvalitetsjustert produksjon, komparativ test','Kvalitetsjustert enhetskostnad ikke forbundet med produktivitetsdifferansen'),
('H07-03','Budsjettinsentiver og kuttforslag','Manglende belønning for gevinster reduserer fremsettelse av kostnadsreduksjonstiltak','Faktiske muligheter for kutt er begrenset og informasjonskostnaden høy','K116 K128','Insentivregler, innsparingsforslag, bevilgningsendringer og resultater','Utnytt tverretatlig utprøving av gevinstretensjon og forhåndsregistrerte utfall','Ingen økning i verifiserte, kvalitetsjusterte nettogevinster'),
('H07-04','Anskaffelsespriser og samordning','Fellesanskaffelser, åpne anbud og bedre kontraktsoppfølging senker livsløpskostnader','Storskala innkjøp svekker konkurranse og fleksibilitet','K115 K116 K132','Enhetspris, kvalitet, volum, kontraktsendringer, tilbydere, livsløpskostnad','Matchet differanse-i-differanser før/etter samordnet anskaffelse','Netto gevinst forsvinner etter kvalitet og administrasjonskostnad'),
('H07-05','Digitaliseringsgevinster','Digitalisering reduserer administrative timeverk per sak når prosesser endres','Digitalisering skaper parallelle systemer og nye kontrollkostnader','K116 K128','Saksbehandlingstid, kvalitet, personell, feilretting, IKT-kostnad','Stegvis utrulling med kontrollgrupper, personvern og forvaltningskvalitet','Ingen netto tids-/kostnadsgevinst innen 36 måneder'),
('H07-06','Juridisk styring av kommuner','Flere detaljkrav øker administrasjon og reduserer lokal innovasjon','Kravene sikrer lik behandling, kvalitet og rettssikkerhet','K116 K129','Regelkrav, etterlevelseskost, klager, tilsyn, kvalitet','Naturlige endringer ved regelharmonisering; kost-nytte med tjenesteresultater','Kostnadsreduksjon oppveies fullt av dårligere kvalitet eller ingen effekt'),
('H07-07','Infrastrukturportefølje','Styrking av krav til netto nytte og etterprøving forbedrer prosjektutvalg','Ikke-prissatte virkninger og beredskap gjør lav beregnet prissatt nytte rasjonelt','K123 K133','NNB, kostnadsoverskridelser, reisetid, sikkerhet, nettverksvirkning','Kontrafaktisk porteføljesimulering og ex post utfall på realiserte prosjekter','Beregnet forbedring forsvinner ved robust verdsetting av ikke-prissatte virkninger'),
('H07-08','Helseeffektivitet','Enhetskostnader i helsesektoren overstiger de som følger av alder, sykdomsbyrde og kvalitet','Høy bemanning og kostnad gir høyere levealder, sikkerhet og tilgang','K113 K121 K136','Case mix, utfall, bemanning, ventetid, ressursbruk pr pasient','Kvalitetsjustert nordisk sykehuspanel med risikojustering','Ingen robust kostnadsforskjell ved sammenlignbare behov/utfall'),
('H07-09','Utdanning resultat og kostnad','Høy ressursbruk pr elev gir ikke proporsjonal økning i ferdigheter','Likhet, geografi, sosial integrasjon og klassestørrelse er uobserverte gevinster','K122 K133','PPP-kostnad, PISA, elevgrunnlag, fullføring, ulikhet, geografisk struktur','Multidimensjonal DEA / value-added elevdesign; kostnad per fremgang','Kostnadsrest forsvinner etter elevbakgrunn og kvalitetsmål'),
('H07-10','Arbeidslinje og sykefravær','Forebygging og målrettet arbeidstilknytning reduserer varig utenforskap med positiv netto velferd','Helsebehov og risiko for fattigdom gjør tiltak lite effektive eller skadelige','K117 K126 K127','Diagnosegruppe, funksjonsevne, tilrettelegging, tilbakefall, skatteinntekter','Stegvis innføring av frivillige tiltak; randomisering der etisk forsvarlig','Ingen vedvarende forbedring i helsejustert sysselsetting og netto budsjett'),
('H07-11','Tjenestestandard og demografi','Økende eldreandel øker ressursbehov selv uten offentlig ineffektivitet','Forebygging, teknologiforbedring og økt yrkesdeltakelse nøytraliserer deler','K124 K125 K121','Befolkningsframskriving, pleiebehov, tjenestestandard, bemanning','Alders- og sykdomsstandardisert 2030–2060 scenariomodell med følsomhetsanalyse','Stabilt/lavere ressursbehov på tvers av plausible referansebaner'),
('H07-12','Offentlig-private arbeidskraftseffekter','Uten produktivitetsgevinst reduserer sterk offentlig rekruttering privat produktivt arbeidstilbud','Offentlige tjenester øker privat sysselsetting gjennom helse, omsorg og utdanning','K114 K128 K117','Lokale lønninger, yrkesmobilitet, private investeringer og tjenestekvalitet','Regionpanel rundt eksogene tjenesteutvidelser med instrumentvariabler','Ingen negativ privat arbeidskraftseffekt eller netto verdiskapingsgevinst'),
('H07-13','Subsidier og energipriser','Generelle pris- og næringssubsidier reduserer prissignaler og omstilling','Forsyningssikkerhet, fordelingshensyn og positive eksternaliteter rettferdiggjør subsidiene','K117 K113','Prisrespons, konsum, utslipp, fordeling, subsidier, nettinvestering','Regresjonsdiskontinuitet ved kvalifiseringsgrense og reformepisode','Effektivitetstap ikke robust etter fordeling og eksternaliteter'),
('H07-14','Resultatstyring og sammenliknbarhet','Sammenlignbare input–output–outcome mål gir mer effektiv ressursbruk','Målforskyvning, gaming og rapporteringskost ødelegger nettogevinst','K116 K119 K136','Rapporteringsbyrde, kvalitetsutfall, budsjetter, saksbehandling','Forhåndsregistrert institusjonell pilot, randomisert utrulling dersom mulig','Ingen kvalitetssikret gevinst og økt kontrollbyrde')]
assert len(HYP)==14
hyp=[]
for id,title,hypothesis,alternative,src,vars,design,fals in HYP:
 hyp.append({'id':id,'tittel':title,'hypotese':hypothesis,'mothypotese':alternative,'variabler':vars,'primarkilder':src,'forskningslitteratur':('K119 K120 K133' if 'Baumol' in title else src), 'empirisk_test':design,'falsifikasjonskriterium':fals,'resultat':'Ikke selvstendig empirisk testet; dokumentert kildegrunnlag og plan','evidensklasse':'U','tillit':'Uavklart; test gjenstår','status':'Kildebelagt grunnlag; kausal test utestående','traad':'07'})
write_pair('hypoteseregister_07',hyp)

# Evidensposter: hvert felt har både hva kilden viser og hva den IKKE viser.
EVID=[
('Total offentlig utgift i 2025','Totale offentlige utgifter: 2 684,551 mrd. kr','A','K113','Ikke det samme som driftskostnader, byråkrati eller arbeidstid'),
('COFOG sosial beskyttelse 2025','1 048,776 mrd. kr, ca. 39,1 % av totalen','A','K113','Omfatter overføringer; ikke sosialadministrasjon'),
('COFOG helse 2025','391,954 mrd. kr','A','K113','Ikke identisk med OECDs helseutgiftsbegrep'),
('COFOG utdanning 2025','254,554 mrd. kr','A','K113','Ulike leveringsformer og elevsammensetning'),
('COFOG generelle tjenester 2025','274,613 mrd. kr','A','K113','Inneholder annet enn lønnet administrasjon; ikke 10,2 % ren byråkratiandel'),
('Forsvarsutgiftvekst 2025','56,890 mrd. kr høyere enn 2024; om lag 37,4 % av årlig totalutgiftsøkning','A','K113 K134','Økning vesentlig preget av Ukraina-støtte'),
('Utgiftsandel samlet BNP 2025','48,7 % av samlet BNP','A','K134','Ikke bytt nevner til Fastlands-BNP uten markering'),
('Andel offentlige jobbforhold 2025','33,5 % av jobbene i 2. kvartal 2025','A','K114','Jobbforhold er ikke antall personer, månedsverk eller årsverk'),
('Offentlig jobbandel i 2016','34,2 % av jobbforhold i 2. kvartal 2016','A','K114','Ingen monoton økning gjennom hele perioden'),
('Offentlig månedsverksandel 2025','32,8 % av månedsverk 2. kvartal 2025','A','K114','Annen nevner enn jobbforhold'),
('Offentlige anskaffelser 2025','Omtrent 864 mrd. kr','A','K115','Kjøp av realinvesteringer og tjenester; ikke nødvendigvis innsparing'),
('Riksrevisjonen spareinsentiv','Nesten to tredjedeler av statlige virksomheter oppga svake kuttinsentiver','A','K116','Survey n=144 – ikke målt prosent statsbudsjett'),
('Riksrevisjonen resultatstyring','Systematisk informasjon om ressursbruk–resultat er mangelfull','A','K116','Påstand om styringssystem, ikke beregnet tap'),
('Riksrevisjonen digitalisering','En av tre virksomheter oppga manglende rom for store effektiviseringstiltak','A','K116','Rapportert opplevd handlingsrom, ikke dokumentert realisert gevinst'),
('Riksrevisjonen rettslig styring','90 % av kommunedirektørene mente statlig juridisk styringstrykk for stort','A','K116','Holdningsmåling, ikke direkte måling av etterlevelseskostnad'),
('Riksrevisjonen regnskapskontroll','Statens regnskaper i all hovedsak riktige etter revisjon','A','K131','God regnskapsføring viser ikke om prioriteringene er optimale'),
('IKT-konsulentavtale','187 mill. kr over maksimal ramme på 600 mill. kr','A','K132','Regelbrudd og sviktende oppfølging, ikke økonomisk tap lik beløpet'),
('Statsforvaltningens personellendring','0,6 % flere ansatte 2023–2024; 0,4 % korrigert for omorganisering','A','K130','Statsforvaltningen er snevrere enn all offentlig forvaltning'),
('Helseutgift per innbygger','Norge 9 393, OECD gjennomsnitt 5 967 USD PPP','A','K121','Samlet helseutgift; ulike demografier og kvalitet'),
('Forventet levealder','Norge 83,1 år, 2,0 år over OECD-gjennomsnitt','A','K121','Indikator påvirkes av faktorer utenfor helsesystemet'),
('PISA 2022 negativ utvikling','Tilbakegang i lesing, matematikk og naturfag fra PISA 2018','A','K122','Ikke årsak fra offentlig pengebruk eller manglende effektivitet'),
('Netto prissatt nytte NTP','Utvalgte prosjekter prioritert for oppstart: −125 mrd. kr, ekskl. Nye Veier','D','K123','Ex ante prissatte virkninger; utelater ikke-prissatt beredskap etc'),
('Netto prissatt nytte Nye Veier','Utvalgte prosjekter: −17 mrd. kr','D','K123','Ikke realisert tap; ex ante delvis nytteberegning'),
('Finanspolitisk gap 2060 opprinnelig','6,2 % Fastlands-BNP i PM2024 referansebane','D','K124','Scenario ikke et forutbestemt budsjettunderskudd'),
('Finanspolitisk gap 2060 revidert','5,9 % Fastlands-BNP i Nasjonalbudsjettet 2026','D','K125','Betinget scenario, datavintage-endring'),
('Uføretrygd 2025','374 900 mottakere, 10,5 % av 18–67 år','A','K126','Andel stabil de siste årene, ikke lineær utgiftsdriver'),
('Sykefravær 2026K2','6,68 % samlet, sesongjustert','A','K127','Næringsgjennomsnitt og sesongjustering'),
('Sykefravær helse 2026K2','9,61 % sesongjustert for næringen helse og sosial','A','K127','Næringsgruppe inkluderer private virksomheter'),
('Kostnadsbasert verdsetting offentlig produksjon','SSB verdsetter ikke-markedsproduksjon fra kostnadene','A','K118 K135','Offentlig bruttoprodukt kan ikke brukes som direkte effektivitetsbevis'),
('Baumols relativkostnadsmekanisme','Differensiell produktivitetsvekst og felles lønnsmarked kan øke relative kostnader','D','K120 K119','Teoretisk mekanisme, ikke målt størrelse i Norge'),
('Helseindikatorers datamangler','Enkelte ventetids- og reinnleggelsesindikatorer var pauset av metodehensyn','A','K136','Må ikke imputere mål som ikke er publisert'),
('KOSTRA styring','Standardisert kommunalt regnskap tillater kostnadsmåling og sammenligning','A','K129','Ikke direkte utfallsbasert uten tjenestejustering'),
('Offentlig egenproduksjon versus kjøp','SSB offentlig forvaltningsstatistikk utelater offentlig eide foretak i denne sektordefinisjonen','A','K113','Eierskap er ikke det samme som institusjonell sektortilhørighet'),
('Utgiftvekst isolert dokumenterer ikke ineffektivitet','Regnskapstall alene mangler kvalitetsjustert output','U','K113 K119 K116','Påstanden kan ikke kvantifiseres uten utfallsdata'),
('Baumol-andel av offentlig kostnadsvekst','Nasjonal effektestimering ikke utført','U','K119 K120','Ingen dokumentert norsk andel i dette forskningsarbeidet'),
('Samlet konsulentbruk i Norge','Dekningsfull samlet tidsserie ikke etablert i denne delrapporten','U','K130 K132','Én avtales overskridelse er ikke et samlet kostnadsestimat'),
('Netto gevinst fra digitalisering','Ingen kausal aggregert besparelse replikert i dette prosjektet','U','K116','Styringssvikt ≠ ferdig beregnet innsparing'),
('Virkning av regulatorisk forenkling','Ingen kausal effekt på produktivitet replikert her','U','K116','Regler kan ha nytte som ikke inngår i virksomhetens kostnad'),
('Mulig ressursvridning mot offentlig sektor','Arbeidskraftseffekt på private investeringer ikke identifisert','U','K114 K128','Samtidige positive effekter fra utdanning/helse må vurderes'),
('Kontrafaktisk optimal utgiftsandel','Ingen identifisert samfunnsøkonomisk optimal offentlige utgiftsandel','U','K113 K117','Høyt nivå er ikke per definisjon sløsing')]
assert len(EVID)==40
hyp_index=[h['id'] for h in hyp]
evid=[]
for i,(title,result,grade,src,lim) in enumerate(EVID,1):
 evid.append({'id':f'E07-{i:03d}','tittel':title,'traad':'07','utsagn':result,'evidensklasse':grade,'status':('Betinget modell' if grade=='D' else 'Uavklart / ikke empirisk testet' if grade=='U' else 'Foreløpig kildebelagt'),'tillit':('Modellavhengig' if grade=='D' else 'Uavklart' if grade=='U' else 'Høy for regnskapsobservasjon; ikke årsak'),'primaerkilde':src,'kilde_id':src,'hypotese':hyp_index[min((i-1)//3,len(hyp_index)-1)],'resultat':result,'mothypotese':'Alternative definisjoner, kvalitet og demografi kan endre vurderingen','variabler':'Se forskningsplan og primærkildens definisjoner','empirisk_test':'Test angitt i register 07; ikke utført i denne utgaven','falsifikasjonskriterium':'Må verifiseres og eventuelt tilbakevises med definisjonskontroll','datavintage':'2026-10-12','begrensninger':lim,'epistemisk_rolle':'Kildebelagt beskrivelse / hypotese, ingen egen kausalestimering','ansvar':'Norsk Økonomi, forskningstråd 07','registrert':STAMP,'forskningslitteratur':'K119 K120 K133','kildereferanser_kontrollert':src})
write_pair('evidensregister_07',evid)

proven={'traad':'07','utgave':'0.9.0','registrert':STAMP,'datagrense':STAMP,'studiedesign':'målrettet kildestudie + original aritmetikk av publiserte aggregater, ikke kausal mikrostudie','kilder_nye':[f'K{n}' for n,*_ in SOURCES], 'kildesett':[{ 'kilde_id':f'K{n}','opphav':org,'referanse':detail} for n,org,detail in SOURCES],'datasett':{'offentlige_hovedtall_07':'SSB tabell 14668, 2021–2025, mill. kr','cofog_utgifter_07':'SSB tabell 14669, 2021–2025, mill. kr','sysselsetting_offentlig_07':'SSB tabell 11655, 2. kvartal 2016–2025, jobbforhold','hovedindikatorer_07':'Separat SSB, DFØ, Riksrevisjonen, OECD, NAV, NTP, blandede enheter som ikke må summeres'},'datasettkonvensjon':'Særlig 2025 totalsum og COFOG-komponentsum avviker med 1 million kroner på grunn av publisert avrunding','begrensninger':['Ingen mikrodata eller kommune-/etatpanel er estimert','Ingen internasjonal enhetlig input–output–outcome-database er publisert','Mekaniske regnestykker er ikke prediksjoner eller påvist sparepotensial','Budsjettregnskap 2025 og 2026-prognose er ulike datakilder','Generell offentlig tjenesteyting er ikke en ren byråkratikategori','Private leverandører kan drive offentlig finansierte tjenester; sektordefinisjonen er institusjonell'], 'ki_erklaering':'ChatGPT OpenAI brukt for researchassistanse, struktur, dokumentasjon og programutvikling; ingen KI-svar ført som faglig primærkilde; etterprøvbarhet krever manuell kontroll.'}
(D/'proveniens_07.json').write_text(json.dumps(proven,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

# Markdown body (kilde- og hypoteseinnhold genereres programmatisk fra samme registreringer)
md=r'''---
tittel: "07 — Offentlig ressursallokering, effektivitet og Baumols kostnadssykdom"
program: "Norsk Økonomi"
utgave: "0.9.0"
dato: "2026-10-12"
språk: "nb-NO"
status: "Foreløpig kildedokumentert deskriptiv delstudie; ikke fagfellevurdert"
---

# 07 — Offentlig ressursallokering, effektivitet og Baumols kostnadssykdom

**Norsk Økonomi | Delrapport 07 | Første empiriske undersøkelse | 12. oktober 2026**

**Problemstilling:** I hvilken grad representerer nivå og sammensetning av offentlig norsk ressursbruk en effektiv leveranse av offentlige tjenester, og hvor stor del av observerte kostnader kan tilskrives faktorer som demografi, tjenestekvalitet, geografisk struktur og Baumols kostnadssykdom, kontra ineffektive prioriteringer, administrative prosesser og manglende insentiver?

**Status og avgrensning.** Dette er en selvstendig deskriptiv datastudie og kritisk litteraturgjennomgang basert på primærstatistikk og offentlige kontroller fra 2025–2026. Den inneholder **ingen selvproduserte kausale estimater**. Kildene er hentet med målrettet søk, ikke en fullstendig systematisk bibliografisk gjennomgang. Alle regneeksempler er merket.

## 1. Sammendrag og resultater

De samlede offentlige utgiftene var **2 684,6 mrd. kroner i 2025** etter SSBs reviderte septembervintage. Beløpet omfatter betydelig omfordeling, tjenester og investeringer. Omtrent **39,1 %** ble klassifisert som sosial beskyttelse, **14,6 %** som helse og **9,5 %** som utdanning. **«Alminnelig offentlig tjenesteyting», 10,2 % av totalen, er ikke et mål på byråkratiets størrelse.** Tallene er i løpende priser og ikke inflasjonsjustert. [K113](#k113)

Det empirisk mest direkte funnet om **styringsmekanismer** kommer fra Riksrevisjonens undersøkelse i juni 2026: Nesten to tredjedeler av 144 respondentvirksomheter rapporterte svake insentiver til å foreslå kutt. Riksrevisjonen finner også svak dokumentasjon av koblingen mellom ressursbruk og resultater, utilstrekkelige mekanismer for sektorovergripende prioriteringer og gevinstrealisering ved digitalisering. Dette dokumenterer institusjonelle forbedringsbehov, men ikke et samlet tall for «sløsing». [K116](#k116)

Den deskriptive statistikken viser samtidig at offentlig forvaltnings **andel jobbforhold gikk fra 34,2 % i andre kvartal 2016 til 33,5 % i andre kvartal 2025**. Andelen har vært forholdsvis stabil; sterk vekst i offentlige utgifter er ikke ensbetydende med tilsvarende vekst i andelen ansatte. [K114](#k114)

**Hovedkonklusjon:** Offentlig norsk ressursbruk er stor og skaper viktige finansielle og arbeidskraftmessige avveininger. Institusjonelle svakheter er godt dokumentert i konkrete revisjoner. Men det er foreløpig **ikke identifisert hvor mange milliarder kroner offentlig sektor kunne spart uten reduksjon i kvalitet, tilgjengelighet, rettssikkerhet eller fordelingsmål**. Studiene må måle nettogevinster på tjenestenivå før slike tall kan publiseres.

## 2. Metode, definisjoner og forskningsetiske krav

### 2.1 Analyseopplegg

1. Avgrens offentlig *forvaltning* institusjonelt (SNA 2008 / ESA 2010) fra offentlig *eierskap* og fra privat leverte, offentlig finansierte tjenester.
2. Analyser årsregnskap etter **utgiftstype** og **formål** (COFOG). Transfereringer til husholdninger er ikke administrative driftsutgifter. Nettoinvesteringer må ikke likestilles med bruttorealinvesteringer.
3. Skille beløp i **løpende kroner**, prisjusterte beløp, årsverk, antall jobber, utførte timeverk og kvalitet/utfall.
4. Sammenlign Norge med andre land bare når finansiering, sektoravgrensning, kjøpekraft og måling av offentlig produksjon er harmonisert.
5. For resultatstudier: dokumenter «**innsatsfaktorer → tjenesteresultater → samfunnsutfall**» og samtidig konsekvenser for rettssikkerhet, tilgjengelighet og fordeling.
6. Test eksplisitt alternative forklaringer før man atribuerer en kostnadsendring til byråkrati eller ineffektivitet.

### 2.2 Viktig nasjonalregnskapsbegrensning

SSB forklarer at offentlig ikke-markedsproduksjon tradisjonelt verdsettes ved summen av lønn, innsatsvarer og kapitalslit, uten markedsbasert driftsoverskudd. Det betyr at bruttoprodukt per ansatt **ikke uten videre er et uavhengig mål på offentlig effektivitet**. OECDs håndbok om volumproduksjon av helse og utdanning drøfter metoder for kvalitets- og aktivitetsjustering og risiko for mekanisk innsatsstyrt volum. [K118](#k118) [K119](#k119) [K135](#k135)

**Målekjede:** *Input* = årsverk, finansielle utgifter, areal, materiell, energi; *output* = behandlingsforløp, rettidige vedtak, undervisningstimer, ferdigstilte tiltak; *outcome* = funksjonsevne, læring, arbeidsdeltakelse, sikkerhet og selvstendighet. En utført behandling er ikke nødvendigvis lik en varig helsegevinst.

## 3. Offentlig forvaltnings samlede utgifter, 2021–2025

SSBs septembervintage 2026 oppgir følgende observasjoner i **milliarder kroner, løpende priser**. «Totale utgifter» beregnes etter SSBs definisjoner som løpende utgifter pluss nettoinvestering i ikke-finansiell kapital; dette er ikke det samme som en sum av alle utgiftsbevilgninger på statsbudsjettets poster. [K113](#k113)

| Kalenderår | Offentlige inntekter | Løpende utgifter | Nettoinvestering i ikke-finansiell kapital | Totale utgifter |
|---|---:|---:|---:|---:|
'''
for i,year in enumerate(YEARS):
 md+=f'| {year} | {spend["Inntekter"][i]/1000:,.1f} | {spend["Løpende utgifter"][i]/1000:,.1f} | {spend["Nettoinvestering i ikke-finansiell kapital"][i]/1000:,.1f} | **{spend["Totale utgifter"][i]/1000:,.1f}** |\n'.replace(',',' ')
md+='''
Fra 2024 til 2025 økte **nominelle** totale utgifter med **152,3 mrd. kroner**, tilsvarende 6,0 %. Beløpet er ikke en beregning av realvekst, og endringen inkluderer blant annet militær støtte til Ukraina som kapitaloverføringer til utlandet. SSBs data gir en utgiftsandel av *samlet BNP* på **47,0 % i 2024** og **48,7 % i 2025**. Andelen blir betydelig høyere hvis nevneren erstattes med Fastlands-BNP; en slik endring må merkes og må ikke brukes til å hevde at to definisjoner er sammenlignbare. [K113](#k113) [K134](#k134)

## 4. Hva brukes pengene til? COFOG

| Formål | 2024, mrd. kr | 2025, mrd. kr | Andel av totalen 2025 |
|---|---:|---:|---:|
'''
for cat,series in COFOG.items():
 md+=f'| {cat} | {series[-2]/1000:,.1f} | {series[-1]/1000:,.1f} | {series[-1]/2684551*100:,.1f} % |\n'.replace(',',' ')
md+='''
*Kilde: SSB tabell 14669, siste offentlige årsdata til og med 2025. Summering av avrundede kategorier avviker med 1 mill. kr fra totalsummen.* [K113](#k113)

### 4.1 «Byråkrati» kan ikke leses rett ut av COFOG

Kategorien **alminnelig offentlig tjenesteyting** omfatter flere sentrale statlige og kommunale funksjoner og kan inkludere gjeldsforvaltning, politiske organer og andre fellesutgifter. Å omtale alle **274,6 mrd. kroner** som administrative kostnader er en definisjonsfeil. En troverdig studie av administrasjonsandelen må splitte underkoder og KOSTRA-funksjoner, trekke ut direkte tjenesteadministrasjon versus støttefunksjoner og unngå dobbelttelling av innkjøpte tjenester. [K113](#k113) [K129](#k129)

**Revisjons- og sammenligningsmerknad:** OECDs tidligere landgjennomgang oppgir en annen utgiftsandel for 2024 (49,6 % av samlet BNP) enn SSBs senere oppdaterte nasjonalregnskapsbaserte tall (47,0 %). Forskjellen må registreres som et spørsmål om datavintage, sektordefinisjon og oppdateringer; den kan ikke skjules eller løses ved å blande tallene i en graf. Denne delrapportens norske historiske serie bruker SSBs 2026-vintage, mens internasjonale OECD-sammenligninger skal bruke harmonisert OECD-vintage. [K03](#k03) [K113](#k113) [K134](#k134)

**Sosial beskyttelse** omfatter i hovedsak ytelser og sosiale formål, ikke «personell som behandler trygdesaker». Det er også metodisk ugyldig å legge COFOG-summen sammen med offentlige innkjøpsutgifter uten å kontrollere overlapp: innkjøp av tjenester er allerede en innsats i den offentlige produksjonen. [K113](#k113) [K115](#k115)

### 4.2 Forsvarsutgiftenes effekt på utgiftsveksten

Forsvarsformålet økte fra **114,9 til 171,8 mrd. kroner** fra 2024 til 2025. Det utgjorde **56,9 mrd. kroner**, omtrent **37,4 % av den samlede nominelle utgiftsøkningen** på 152,3 mrd. kroner. SSB understreker at militær støtte til Ukraina er en hovedforklaring og stort sett registreres som kapitaloverføringer til utlandet. En budsjettsammenligning som tolker hele utgiftsveksten som voksende norsk offentlig administrasjon, blir derfor feil. [K113](#k113) [K134](#k134)

## 5. Offentlig sysselsetting og arbeidskraftens alternativbruk

I andre kvartal 2025 hadde offentlig forvaltning **1 052 772 jobbforhold** og privat sektor inklusiv offentlig eide foretak **2 089 485 jobbforhold**, målt i SSBs registerstatistikk. Offentlig andel jobbforhold var **33,5 %**, mens andelen *månedsverk* var **32,8 %**. Jobbforhold er ikke antallet sysselsatte personer; én person kan ha mer enn ett jobbforhold. [K114](#k114)

| 2. kvartal | Offentlige jobbforhold | Offentlig jobbandel | Offentlig månedsverksandel |
|---|---:|---:|---:|
'''
for yr,pub,pri,share,mons in EMP:
 md+=f'| {yr} | {pub:,} | {share:.1f} % | {mons:.1f} % |\n'.replace(',',' ')
md+=r'''
Den sterke påstanden «offentlig sektor absorberer stadig mer av arbeidskraften målt som *andel jobber*» støttes ikke av akkurat denne perioden; offentlig andel er litt lavere i 2025 enn i 2016. **Alternativkostnaden ved offentlig personell** kan likevel være stor ved mangel på sykepleiere, teknikere eller lærere. Et resultat krever *marginale*, kompetansejusterte analyser av lokal lønn, mobilitet og tjenesteutfall — ikke nasjonale jobbprosenter alene. [K114](#k114)

DFØ fant **0,6 %** vekst i ansatte i snevert definert statsforvaltning fra 2023 til 2024, og **0,4 %** korrigert for omorganiseringer. Statsforvaltningen i dette datasettet er ikke all offentlig forvaltning, særlig ikke de offentlig eide helseforetakene. [K130](#k130)

## 6. Baumols kostnadssykdom — mekanisme, betingelser og måling

Baumols modell for ubalansert produktivitetsvekst beskriver en sektor med svak produktivitetsvekst som må øke lønningene omtrent i takt med sektorer med sterkere vekst for å beholde arbeidskraft. Resultatet kan være stigende **relativ pris** på arbeidsintensive tjenester selv når driften er teknisk effektiv. Modellen ble utviklet av Baumol (1967) og Baumol og Bowen (1966). Den er ikke et empirisk bevis på at norske helse-, skole- eller omsorgskostnader *faktisk* skyldes denne mekanismen. [K120](#k120)

La `g_w` være nominell lønnsvekst, `g_p` kvalitetsjustert produktivitetsvekst i tjenesten og `g_q` produktivitetsvekst i en referansesektor. I en idealisert modell med samme lønnsvekst og sammenlignbare arbeidsandeler er relativ enhetskostnad etter `t` år:

$$
\begin{flalign*}
& C_{\mathrm{rel},t}= C_{\mathrm{rel},0}\left(\frac{1+g_q}{1+g_p}\right)^t \\
& \text{Illustrasjon: }g_q=0,02,\quad g_p=0,005,\quad t=20 \\
& C_{\mathrm{rel},20}/C_{\mathrm{rel},0}=(1,02/1,005)^{20}\approx 1,345 
\end{flalign*}
$$

Dette er **ca. 34,5 % relativ kostnadsøkning over 20 år i den stiliserte modellen**, *ikke* et estimat av norsk offentlig sektors utvikling eller effektiviseringsmulighet. Ved særskilt måling må vi også inkludere kapitalkostnad, pasienttyngde, kompetansesammensetning, tjenestestandard, demografi, stordriftsforhold og endret behandlingsteknologi. [K119](#k119) [K120](#k120)

### 6.1 Hvor Baumol-hypotesen kan testes

**Omsorg:** Direkte omsorgstid kan ikke elimineres uten mulig kvalitetskostnad; nye hjelpemidler kan likevel redusere tidsbruk ved dokumentasjon, transport og enkelte løfteoppgaver. **Skole:** Klasseromstid er arbeidsintensiv, men læringsutbytte måles i faktisk ferdighetsframgang, ikke bare antall elevtimer. **Administrasjon:** Standardiserte skjemaer, datadeling og automatisering kan ha høyere produktivitetspotensial enn direkte menneskelig omsorg. Det er derfor feil å anvende én felles «Baumol-faktor» på hele offentlig sektor.

### 6.2 Forhåndsdefinert dekomponering

En empirisk tidsserieanalyse skal skille: (A) lønns- og faktorprisvekst; (B) demografisk volum; (C) endret kvalitets- og standardnivå; (D) endret bruker-/pasienttyngde; (E) målt produktivitet; og (F) uforklart residual. Residualen må ikke umiddelbart kalles sløsing, ettersom målefeil og ikke-observerte resultater kan inngå. OECD påpeker nettopp utfordringen med å måle volumproduksjon og kvalitet i helse og utdanning. [K119](#k119)

## 7. Revisjonsfunn: institusjoner, budsjettinsentiver og resultatdata

Riksrevisjonens **Dokument 3:15 (2025–2026)** er et spesielt sterkt utgangspunkt for å evaluere politikk og styring fremfor å gjette fra utgiftsnivå. Undersøkelsen offentliggjort 10. juni 2026 rapporterer:

- Nesten **to tredjedeler** av statlige virksomheter i en undersøkelse med **144 respondenter** oppga svake insentiver til å fremme innsparings- og kuttforslag.
- **Halvparten** oppgir utilstrekkelig tilrettelegging for systematiske sammenligninger med andre virksomheter.
- **En av tre** oppgir å ha utsatt eller avstått fra større effektiviseringstiltak på grunn av manglende kortsiktig handlingsrom.
- **90 % av kommunedirektørene** mener det juridiske statlige styringstrykket er for stort.
- Statens resultatinformasjon og gevinstrealisering ved digitalisering har alvorlige metodiske og organisatoriske mangler. [K116](#k116)

**Fortolkning:** Dette er til dels surveydata om virksomheters opplevelser, supplert av Riksrevisjonens dokumentgjennomgang. Det er ikke beregnet hvor mange årsverk, kroner eller tjenesteutfall som ville endret seg under en alternativ styringsmodell. Til tross for styringssvakhetene viste Riksrevisjonens separate regnskapsrevisjon av 2024 at statens regnskaper i all hovedsak var riktige. **Riktig regnskap og svak prioritering kan eksistere samtidig.** [K116](#k116) [K131](#k131)

## 8. Offentlige anskaffelser og konsulentbruk

DFØs anskaffelsesstatistikk oppgir **omtrent 864 mrd. kroner i offentlige innkjøp i 2025**, mot rundt 835 mrd. kroner i 2024. Definisjonen inkluderer kjøp av varer og tjenester og offentlige bruttoinvesteringer, og omfatter også nærmere definert offentlig forretningsdrift. Beløpet er ikke en ekstra utgift oppå hele COFOG-budsjettet. [K115](#k115)

Som rent **regneeksempel** utgjør 0,5 % av 864 mrd. kroner **4,32 mrd. kroner**. Dette beviser verken at 0,5 % er oppnåelig, at innsparingen blir varig, eller at den er netto etter implementeringskostnader, kvalitetstap og kontraktsendringer. Nettsidens simulator er merket som illustrasjon.

Riksrevisjonen dokumenterte i 2025 at departementene hadde gjort IKT-konsulentkjøp **187 mill. kroner utover maksimalverdien i en rammeavtale på 600 mill. kroner**. Dette er et konkret avtalestyringsproblem, men **overskridelsen er ikke identisk med et tilsvarende samfunnsøkonomisk tap**. En komplett studie av «konsulentsamfunnet» må samle sammenlignbar statistikk for både tjenester som er kjøpt, leveranser, intern kompetanse og kontraktsgevinster. [K132](#k132)

## 9. Helse og omsorg: kostnad versus resultat

OECDs landnotat *Health at a Glance 2025* rapporterer norske samlede helseutgifter på **9 393 USD per innbygger i kjøpekraftskorrigert valuta (PPP)**, mot **5 967 USD** som OECD-gjennomsnitt. Forventet levealder var **83,1 år** i Norge, **2,0 år over gjennomsnittet**. Høye kostnader sammen med relativt gode helseutfall utelukker både slutningen «god pengebruk bevist» og slutningen «sløsing bevist». Befolkningens øvrige helse, arbeidsmarked, aldersstruktur, geografi og tilgjengelighet må hensyntas. [K121](#k121)

Helsetjenesten må analyseres med risikojustert behandlingsresultat, forebygging, pasientsikkerhet, tilgjengelighet, reinnleggelser, case mix, bemanning og tidsbruk. Helsedirektoratets gjennomgang av indikatorene i 2025 opplyser at enkelte ventetids- og reinnleggelsesindikatorer ikke var publisert på grunn av metodiske avklaringer. Manglende kvalitetsmål skal ikke estimeres som null eller tolkes som at kvalitet er uendret. [K136](#k136)

## 10. Utdanning: ressursbruk, ferdigheter og framtidig produktivitet

PISA 2022 dokumenterte fall i norsk lesing, matematikk og naturfag fra 2018. OECDs 2024-studie finner høy norsk utdanningsressursbruk uten tilsvarende overlegen gjennomsnittsprestasjon i PISA. **Dette gir grunnlag for en effektivitetsstudie, ikke for å konkludere at skoleutgiftene har forårsaket fallet i PISA.** Elevsammensetning, nedstengninger, skjermbruk, nasjonale læreplaner, ressursfordeling og ikke-testede læringsmål er konkurrerende forklaringer. [K122](#k122) [K133](#k133)

En gyldig studie krever kostnad per elev korrigert for småskolestruktur, reiseavstander, spesialundervisning, lærertetthet og elevens sosioøkonomiske bakgrunn, samt mål for læringstilvekst og gjennomføring. Data fra KOSTRA og Udir kan være grunnlag, men kobling og resultatanalyse er ikke utført her. [K129](#k129) [K122](#k122)

## 11. Infrastruktur, energi og samfunnsøkonomisk rangering

I **Nasjonal transportplan 2025–2036** anslår regjeringen samlet netto **prissatt** nytte for store prioriterte prosjekter (eksklusive Nye Veier) til rundt **−125 mrd. kroner**; for Nye Veiers prosjekter er tallet om lag **−17 mrd. kroner**. Begge er **ex ante kost–nytte-anslag** for definerte porteføljer, og utelater etter sin natur virkninger som ikke er prissatt. Negative prissatte anslag er et begrunnet spørsmål om prioritering, ikke dokumentasjon på at prosjektene samlet er samfunnsøkonomisk ulønnsomme etter alle virkninger. [K123](#k123)

Det samme prinsippet gjelder energitiltak og strømstøtte: Prisvirkninger, forsyningssikkerhet, investering og fordeling må modelleres sammen. OECDs 2026-landrapport peker på mulige svekkede energieffektiviseringsinsentiver ved brede prisstøtteordninger, men en slik vurdering fastslår ikke at fordelingsgevinstene er verdiløse. **Regelverk og planprosesser** skal testes på faktisk tidsbruk, etterlevelseskostnader, prosjektkvalitet og juridisk sikkerhet, ikke bare antall nye forskrifter. [K117](#k117) [K116](#k116)

## 12. Arbeidslinje, sykefravær og uføretrygd

NAV rapporterte ved utgangen av 2025 om **omtrent 374 900 mottakere av uføretrygd**, tilsvarende **10,5 %** av 18–67-åringene. NAV skriver at andelen har vært nokså stabil siden 2020 og at økningen i antallet var uvanlig lav i 2025. Dette gir en nødvendig motvekt mot påstander om en eksplosiv økning i alle arbeidsmarkedsytelser. [K126](#k126)

SSB måler **6,68 % sesongjustert samlet sykefravær i andre kvartal 2026**. For *næringen* helse og sosialtjenester var andelen **9,61 %**, for undervisning **6,66 %** og for offentlig administrasjon/forsvar **5,68 %**. Næringsinndelingen er noe annet enn institusjonell offentlig forvaltning, ettersom helse- og undervisningsforetak også kan være private. Høye sykefraværstall kan være en kombinasjon av arbeidsforhold, kjønn, aldersprofil, helse og rettighetsregler. [K127](#k127)

Før et arbeidslinjetiltak kan anses effektivt, må man måle funksjonsjustert varig arbeidsdeltakelse, helse- og livskvalitet, inntekt, risiko for tilbakefall og netto offentlige inntekter/utgifter – ikke bare antall som mister en ytelse. Tiltak kan være både inkluderende og utilsiktet skadelige; nettoeffektene må være etisk og empirisk undersøkt.

## 13. Finanspolitisk holdbarhet og SPU-avhengighet

**Perspektivmeldingen 2024** viste et betinget inndekningsbehov på **6,2 % av Fastlands-BNP i 2060** gitt bestemte forutsetninger. **Nasjonalbudsjettet 2026** oppdaterte estimatet til om lag **5,9 %** under sin oppdaterte referansebane. Det er ikke to observerte underskudd, og tallene må ikke presenteres som presise prognoser eller en dato for finansielt sammenbrudd. Utgiftene er påvirket av eldreandel, tjenestestandard og forventet økonomisk vekst. [K124](#k124) [K125](#k125)

Forskningstråd 07 og 08 må kobles ved at arbeidstilbud, faktiske tjenestekostnader, produktivitetsvekst og avkastning fra SPU simuleres med konsistente forutsetninger. Et effektiviseringsscenario må regne både engangsinvestering, implementeringskostnad, resultateffekt, langsiktig drift og politisk/organisatorisk gjennomførbarhet.

## 14. Samlet evidens, motforklaringer og konklusjon

| Påstand | Foreløpig status | Hva som fortsatt mangler |
|---|---|---|
| Offentlig ressursbruk er høy | Dokumentert (A) | OECD-harmonisert formålsfordelt tidsserie og tjenestekvalitet |
| Andelen offentlige jobbforhold øker kontinuerlig | **Motsies av 2016–2025-serien** (A) | Yrkesgrupper, lokale arbeidsmarkeder, privat offentlig finansiering |
| Budsjettinsentiver og resultatdata har vesentlige svakheter | Dokumentert for undersøkt styring (A) | Estimert konsekvens for budsjetter og tjenestekvalitet |
| Offentlig sektor sløser med et bestemt antall mrd. | **Ikke dokumentert (U)** | Tjenestekostnad, kvalitet, kontrafaktisk sammenligning |
| Baumols kostnadssykdom forklarer en betydelig del av norsk kostnadsvekst | Plausibel teoretisk mekanisme (D/U) | Empirisk norsk sektorvis estimering |
| Alle dyre offentlige tjenester er ineffektive | **Ikke underbygget** | Kvalitetsjustert output og outcome |
| Offentlige investeringer er alltid lønnsomme fordi de skaper aktivitet | **Ikke underbygget** | Netto samfunnsøkonomisk nytte og alternativkostnad |

**Foreløpig konklusjon:** Det finnes sterke holdepunkter for styrings- og prioriteringsproblemer, mens de samlede budsjett- og sysselsettingstallene samtidig viser at direkte administrasjonskostnad, transfereringer, tjenester og investeringer må holdes adskilt. De viktige spørsmålene er hvilke tjenester Norge oppnår per ressursenhet, hvilke avvik som består etter justeringer, og hvilke reformer som har bedre målte nettovirkninger enn alternativene.

## 15. Registrerte hypoteser, data og falsifikasjonskriterier

De 14 hypotesene er operasjonalisert i `data/hypoteseregister_07.csv` og `data/hypoteseregister_07.json`. De følgende oppføringene er **ikke testresultater**. Hvert forskningsdesign krever forhåndsdefinert populasjon, kontroll for sentrale konfunderende faktorer, vurdering av feilkilder og et publisert replikerbart beregningsskript.

'''
for x in hyp:
 md+=f"### {x['id']} — {x['tittel']}\n\n**Hypotese:** {x['hypotese']}  \n**Motforklaring:** {x['mothypotese']}  \n**Variabler:** {x['variabler']}  \n**Primærkilder:** {x['primarkilder']}  \n**Eksisterende litteratur:** {x['forskningslitteratur']}  \n**Empirisk test:** {x['empirisk_test']}  \n**Resultat:** Ikke gjennomført i dette prosjektet.  \n**Tillit:** Uavklart; styrkes/svekkes av den planlagte testen.  \n**Falsifikasjonskriterium:** {x['falsifikasjonskriterium']}.\n\n"
md+='''## 16. Prioritert forskningsplan og krav til data

| Prioritet | Arbeidspakke | Hoveddata | Minimumsleveranse |
|---|---|---|---|
| P0 | 07-A Formålsfordelte kostnader 1978–2025 | SSB 14668/14669/14671, historiske BNP-deflatorer | Gjennomgåtte regnskap i løpende og faste priser uten tidsseriebrudd |
| P0 | 07-B Bemanning og administrasjon | SSB arbeidsforhold/timeverk, DFØ statsforvaltning, KOSTRA-funksjoner | Justert tidsserie admin-årsverk versus førstelinjeårverk |
| P0 | 07-C Baumol og offentlig produktivitet | SSB lønn, timeverk og sektorvolum, OECD kvalitet, tjenestestandard | Kvalitetsjustert faktor-/pris-/produksjonsdekomponering med intervaller |
| P0 | 07-D Resultatstyring og digitaliseringsgevinster | Riksrevisjonen/Digitaliseringsdir./DFØ, administrative saksdata | Forhåndsregistrert pilot med nettoeffekt og kontrollgruppe |
| P1 | 07-E Helseressurser | Helsedirektoratets kvalitet, SSB pleie, OECD Health | Behovs-/case-mix-justert helsepanel på tjenestenivå |
| P1 | 07-F Utdanning | Udir/PISA, KOSTRA, elevbakgrunn, elevmobilitet | Resultat per justert ressursenhet og usikkerhet |
| P1 | 07-G Anskaffelser/IKT | DFØ anskaffelser, KGV/kontrakter, statsregnskap | Prisindeks og anskaffelsesanalyser med kvalitets- og livsløpsmål |
| P1 | 07-H Infrastruktur/energi | NTP investeringsdatabaser, NVE/RME, ex post analyser | Prioriteringspanel for netto samfunnsøkonomisk nytte |
| P1 | 07-I Sykefravær/arbeidstilknytning | NAV/SSB koblede data ved tillatelse | Risikojustert varig arbeid og sosial nettoeffekt |
| P2 | 07-J Finanspolitisk integrasjon | 08 SPU, 09 demografi, 10 systemdynamikk | Sensitivitetsmodell med offentlige referansebaner og kostnadsvintage |

**Falsifikasjon på systemnivå:** Hovedfortellingen om «administrativ ekspansjon som dominerende driver» forkastes dersom regnskap og bemanning korrigert for forsvar, transfereringer, demografi og tjenesteomfang ikke viser en slik nettoandel. Hovedfortellingen om «ingen effektiviseringsmuligheter» forkastes ved troverdige piloter som viser varig kvalitetsjustert nettogevinst.

### Dataetikk og KI-erklæring

Alle aggregerte data som er gjengitt er offentlig tilgjengelige. Eventuelle koblede individdata for NAV/helse/utdanning krever lovlig tilgang, dataminimering, etisk vurdering og publisering uten reidentifiserbare celler. Flere former for kunstig intelligens har vært brukt som forskningsassistanse: ChatGPT (OpenAI) til struktur, kritisk kildesøk, tekst og programmering, med mulig bruk av andre verktøykategorier uten fullstendig modellogg. KI-systemer er **ikke** vitenskapelige primærkilder eller selvstendige fagfellevurderere. Verken eksternt review eller statistisk replikasjon av underliggende mikrodata er utført.

## 17. Kilder og maskinlesbare vedlegg

**Kilde-ID K113–K136 er globale ID-er i Norsk Økonomis kilderegister.** Ved revisjon må ny SSB-vintage registreres med dato, kilde og endringslogg. Originale artikkeltitler beholdes for identifikasjon.

'''
for num,org,detail in SOURCES: md+=f'<a id="k{num}"></a>\n\n- **K{num} — {org}.** {detail}\n\n'
md+='''**Maskinlesbare vedlegg:** `data/offentlige_hovedtall_07.csv`, `data/cofog_utgifter_07.csv`, `data/sysselsetting_offentlig_07.csv`, `data/hovedindikatorer_07.csv`, `data/evidensregister_07.csv`, `data/hypoteseregister_07.csv` og `data/proveniens_07.json`. Årlige løpende regnskap og prosentvise indikatorer ligger i forskjellige tabeller og må aldri summeres ukritisk. Alle filer er UTF-8; CSV er semikolondelt og inneholder separat kilde-ID.
'''
P=R/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md';P.write_text(md,encoding='utf8')
# Integrasjon i kanonisk hovedrapport. Kildeliste er kun én gang i kapittel 11.
prior=(R/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.8.0.md').read_text('utf8')
assert '## 12. Forskningstråd 01' in prior
srcblock='\n\n### 11.9 Offentlig ressursbruk, effektivitet og Baumol (K113–K136)\n\nKildene omfatter reviderte regnskap, uavhengig revisjon, OECDs sammenligninger og teoretisk/empirisk litteratur. De brukes som **kilder**, ikke som påstand om kausalitet eller et beregnet sparebeløp.\n\n'
for n,org,detail in SOURCES:srcblock+=f'<a id="k{n}"></a> **K{n} — {org}.** {detail}\n\n'
prior=prior.replace('## 12. Forskningstråd 01',srcblock+'## 12. Forskningstråd 01',1)
assert '**Arbeidsspråk og publiseringsspråk:** Norsk.' in prior
prior=prior.replace('**Arbeidsspråk og publiseringsspråk:** Norsk.','**Nytt i v0.9.0:** Forskningstråd 07 er kildedokumentert med offentlige utgifter og COFOG 2021–2025, jobbforhold 2016–2025, DFØ-anskaffelser, Riksrevisjonens 2026-revisjon, sektorvis sykefravær, helse- og utdanningsutfall, Baumol-modell og finanspolitiske referansebaner. Delrapporten har 14 hypoteser og 40 evidensoppføringer; ingen norsk kausal Baumol-andel eller offentlig netto ineffektivitet er tallfestet.\n**Arbeidsspråk og publiseringsspråk:** Norsk.',1)
prior=prior.replace('utgave: "0.8.0 — forskningstråd 01–06: metode, økonomiske sammenligninger, bolig/kreditt, generasjonsøkonomi, entreprenørskap og skatt/eiermobilitet"','utgave: "0.9.0 — forskningstråd 01–07: metode, økonomiske sammenligninger, bolig/kreditt, generasjonsøkonomi, entreprenørskap, skatt og offentlig ressursbruk"',1)
prior=prior.replace('**Norsk Økonomi | Forskningsutgave 0.8.0 |','**Norsk Økonomi | Forskningsutgave 0.9.0 |',1)
prior=prior.replace('gir **ni foreløpige hovedresultater**','gir **ti foreløpige hovedresultater**',1) if 'gir **ni foreløpige hovedresultater**' in prior else prior
prior=prior.replace('gir **åtte foreløpige hovedresultater**','gir **ni foreløpige hovedresultater**',1) if 'gir **åtte foreløpige hovedresultater**' in prior else prior
# Append summary before final conclusion
if '**Foreløpig hovedkonklusjon:**' in prior:
 prior=prior.replace('**Foreløpig hovedkonklusjon:**','10. **Offentlige utgifter og effektivitet:** SSBs 2025-regnskap viser 2 684,6 mrd. kroner i offentlige utgifter, men dette inkluderer trygder, tjenester og investeringer. Riksrevisjonen 2026 finner svake kuttinsentiver og mangelfulle resultatdata. Offentlig jobbandel har samtidig vært stabil eller svakt avtagende over 2016–2025. Baumols mekanisme er faglig relevant, men det foreligger ikke et norsk kausalt anslag i prosjektet på hvor mye utgiftsvekst den forklarer. [K113](#k113) [K114](#k114) [K116](#k116) [K120](#k120)\n\n**Foreløpig hovedkonklusjon:**',1)
# Use exactly one set of source anchors from main.
sub=md.split('\n## 1. Sammendrag og resultater',1)[1].split('\n## 17. Kilder og maskinlesbare vedlegg',1)[0]
sub=re.sub(r'(?m)^### (\d+\.\d+)',r'#### 18.\1',sub)
sub=re.sub(r'(?m)^## (\d+)\. ',lambda m: '### 18.'+str(int(m.group(1))+1)+' ',sub)
prior+='\n\n## 18. Forskningstråd 07 — Offentlig ressursbruk, effektivitet og Baumols kostnadssykdom\n\n*Integrert, foreløpig kildestudie. Full selvstendig delrapport 07 og kildeproveniens er lagt ved i publiseringspakken.*\n\n### 18.1 Sammendrag og resultater'+sub+'\n'
MAIN=R/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.9.0.md';MAIN.write_text(prior,encoding='utf8')
print('Kilder',len(SOURCES),'observasjoner',len(SPEND)+len(EXPEND)+len(EMPLOY)+len(OTH),'hypoteser',len(hyp),'evidens',len(evid),'rapport 07 KB',round(P.stat().st_size/1024,1))
