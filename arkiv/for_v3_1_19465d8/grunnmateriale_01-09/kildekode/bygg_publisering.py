#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bygger norsk, selvstendig forskningsnettside fra kanonisk Markdown.
Kjør: python bygg_publisering.py
Avhengigheter ved ombygging: markdown-it-py og beautifulsoup4.
Selve nettsiden krever ingen avhengigheter, API eller database.
"""
from __future__ import annotations
import re, csv, json, html, unicodedata, shutil, zipfile
from pathlib import Path
from datetime import date
from bs4 import BeautifulSoup, NavigableString
from markdown_it import MarkdownIt

SCRIPT = Path(__file__).resolve()
PACKAGED = SCRIPT.parent.name == 'kildekode'
ROOT = SCRIPT.parent.parent if PACKAGED else SCRIPT.parent
TEMPLATE = SCRIPT.parent / 'mal_nettside.html'
DATE = '2026-10-13'
VERSION = 'v1.1.0'
MD = ROOT / f'Norsk_Okonomi_Forskningsrapport_{DATE}_{VERSION}.md'
# I en nedlastet publiseringspakke bygges HTML direkte i dokumentroten.
# Ved utvikling holdes publisert side isolert i nettside/ og renskes for gamle versjoner.
SITE = ROOT if PACKAGED else ROOT / 'nettside'
if not PACKAGED and SITE.exists():
    shutil.rmtree(SITE)
DATA = SITE / 'data'
DATA.mkdir(parents=True, exist_ok=True)
text = MD.read_text(encoding='utf-8')
assert text.startswith('---\n')
body = text.split('\n---\n', 1)[1].lstrip()

sources=[]
for line in body.splitlines():
    match=re.match(r'<a id="k(\d+)"></a>\s+\*\*K\d+\s+—\s+(.+?)\*\*\s*(.*)', line)
    if match:
        key=f'K{match.group(1)}'
        org=match.group(2)
        details=match.group(3)
        urls=[m.rstrip(',.') for m in re.findall(r'https?://[^\s]+',details)]
        sources.append({'id':key, 'opphav':org, 'referanse':details, 'url':urls, 'kontrollert':'2026-10-12' if int(match.group(1))<=136 else '2026-10-13'})
assert len(sources)==170, f'forventet 170 kilder, fant {len(sources)}'
smap={x['id']: x for x in sources}
(DATA/'kilder.json').write_text(json.dumps({
    'rapportversjon':'1.1.0',
    'kildedato':DATE,
    'kilder':sources,
    'ki_bruk':{
        'type':'metodeerklæring (ikke faktakilde)',
        'sted_i_rapport':'§ 10.4 og § 11.2',
        'brukt':True,
        'kjent_tjeneste':['ChatGPT (OpenAI)'],
        'funksjonskategorier':[
            'generativ KI og språkmodeller for strukturering, tekstutkast og redigering',
            'KI-assistert kildesøk, identifikasjon og sammenstilling av kilder',
            'KI-assistert analyse, beregningseksempler, programvareutvikling og visualisering'
        ],
        'begrensning':'Fullstendig logg over modellnavn, modellversjoner, øvrige tjenester og forespørsler foreligger ikke; andre spesifikke modeller er derfor ikke oppgitt.',
        'kildestatus':'KI er ikke primærkilde og tildeles ingen K-ID for empiriske påstander.',
        'ansvar':'Faglig ansvar og publiseringsansvar ligger hos prosjektansvarlig. Ingen uavhengig ekstern fagfellevurdering er gjennomført.'
    }
},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

obs=[]
def put(serie, tema, indikator, periode, gruppe, verdi, enhet, kilde, status, note=''):
    obs.append({'serie':serie,'tema':tema,'indikator':indikator,'periode':str(periode),'gruppe':gruppe,
        'verdi':str(verdi),'enhet':enhet,'kilde_id':kilde,'datastatus':status,'merknad':note})

for year, value in [(2016,7510),(2017,8488),(2018,8256),(2019,10088),(2020,10914),(2021,12340),(2022,12429),(2023,15757),(2024,19742),(2025,21268)]:
    put('fond_historikk','Statsfinanser','SPU – markedsverdi ved utgangen av året',year,'Norge',value,'mrd. NOK','K06','Regnskapsverdi','Nominell NOK; ikke inflasjonskorrigert; variasjoner inkluderer valuta og fondstilførsler')
put('fond_historikk_2026','Statsfinanser','SPU – markedsverdi ved utgangen av 1. halvår','2026-H1','Norge',22683,'mrd. NOK','K06','Halvårsobservasjon','Ikke sammenlikn som fullført år')
for country,v in [('Norge',40.2),('OECD',34.1),('Danmark',45.2),('Sverige',41.4),('Finland',42.2)]:
    put('skatt_2024','Skatt','Skatteinntekter i prosent av samlet BNP',2024,country,v,'prosent','K17','Sammenliknbar OECD-statistikk','Målt mot samlet BNP, ikke Fastlands-BNP')
put('skatt_2000','Skatt','Skatteinntekter i prosent av samlet BNP',2000,'Norge',41.8,'prosent','K17','Historisk OECD-serie')
for age,group,val in [(25,'Øverste 2 % foreldre',50),(25,'Nederste 25 % foreldre',20),(30,'Nederste 25 % foreldre',42),(30,'Nederste 25 % – Oslo/Bærum',36),(30,'Nederste 25 % – andre kommuner',46)]:
    put('boligeierskap_ung','Generasjoner','Registrert boligformue innen oppgitt alder',f'alder-{age}',group,val,'prosent','K08','Kohortanalyse','Årskull født 1988–1993, bosatt Norge 2005 og 2023')
for year,main,total,hours in [(2024,0.6,1.4,0.5),(2025,1.7,1.1,0.4)]:
    put('fastlandsvekst','Vekst','Fastlands-BNP, volumendring',year,'Norge',main,'prosent årlig','K01','Foreløpig nasjonalregnskap')
    put('totalvekst','Vekst','Samlet BNP, volumendring',year,'Norge',total,'prosent årlig','K01','Foreløpig nasjonalregnskap')
    put('timeverk_hele','Arbeid','Utførte timeverk, hele økonomien',year,'Norge',hours,'prosent årlig','K01','Foreløpig nasjonalregnskap')
put('fastland_q2','Vekst','Fastlands-BNP, sesongjustert kvartalsvekst','2026-K2','Norge',0.3,'prosent fra foregående kvartal','K01','Foreløpig','Ikke sammenlikn direkte med årlige vekstrater')
for country,val in [('Norge',49.6),('OECD',42.6)]:
    put('offutgift_2024','Offentlig sektor','Offentlige utgifter i prosent av samlet BNP',2024,country,val,'prosent','K03','OECD-sammenlikning','Denne figuren benytter total-BNP i nevner i begge observasjoner')
put('offjobber','Offentlig sektor','Andel jobbforhold i offentlig forvaltning','2025-K2','Norge',33.5,'prosent av jobbforhold','K18','SSB register','Ikke andel personer eller årsverk')
for cat, val in [('Primærbolig',8245.797),('Sekundærbolig',913.257),('All realkapital',9937.819),('Brutto finanskapital',4841.252),('Samlet bruttoformue',14779.072),('Samlet gjeld',4598.482),('Beregnet nettoformue',10180.589)]:
    put('formue_2024','Formue',cat,2024,'Husholdninger',val,'mrd. NOK','K07','SSB beregnet markedsverdi','Husholdninger med studenter er utelatt; observasjonene er beholdninger')
put('formue_bolig_andel','Formue','Primær- og sekundærbolig som andel av bruttoformue',2024,'Husholdninger',61.972,'prosent','K07','Egen beregning','(8 245 797 + 913 257)/14 779 072 * 100')
for year,val in [(2015,1.73),(2024,1.44),(2025,1.48)]:
    put('fruktbarhet','Demografi','Samlet fruktbarhetstall',year,'Norge',val,'barn per kvinne','K11','SSB statistikk','Utvalgte år; ikke komplett tidsserie')
for year,val in [(2024,54013),(2025,55401)]:
    put('fodte','Demografi','Levendefødte',year,'Norge',val,'barn','K11','SSB statistikk')
for year,val in [(2015,28.9),(2024,30.4),(2025,30.4)]:
    put('førstegangsalder','Demografi','Mors alder ved første fødsel',year,'Norge',val,'år','K11','SSB statistikk','Utvalgte år')
for year,val in [(2025,531),(2026,579)]:
    put('fondsuttak','Statsfinanser','Strukturelt oljekorrigert underskudd, anslag i RNB 2026',year,'Norge',val,'mrd. kroner i 2026-priser','K05','Budsjettanslag','Tall fra samme revisjon, ikke endelige regnskapstall')
put('fondsuttak_bn','Statsfinanser','Strukturelt underskudd som andel av trend-Fastlands-BNP',2026,'Norge',12.6,'prosent','K05','Budsjettanslag')
put('fondsuttak_andel','Statsfinanser','Strukturelt underskudd som andel av SPU-verdi ved inngang',2026,'Norge',2.7,'prosent','K05','Budsjettanslag')
put('budsjettgap','Statsfinanser','Langsiktig finanspolitisk inndekningsbehov, betinget referansebane',2060,'Norge',6.2,'prosent av Fastlands-BNP','K13','Offentlig scenario','Betinget framskriving, ikke prognose')
put('inntekts_gini','Ulikhet','Gini, ekvivalert inntekt etter skatt',2024,'Norge',0.248,'indeks','K07','SSB statistikk')
for group,val in [('Øverste 1 %',21.7),('Nederste 50 %',3.5)]:
    put('formueandel','Ulikhet','Andel samlet beregnet nettoformue',2024,group,val,'prosent','K07','SSB statistikk')
put('gründere','Bedrifter','Personer som etablerte foretak',2024,'Norge',64622,'personer','K14','Foreløpig','Ikke lik nye foretak')
put('foretak_q2','Bedrifter','Nyregistrerte foretak','2026-K2','Norge',17052,'foretak','K15','SSB foreløpig','Kvartalstall, ikke personer som etablerte foretak')
put('fou_2024','Bedrifter','Foretakssektorens egenutførte FoU',2024,'Norge',46.6,'mrd. NOK','K16','SSB FoU-telling')
# Tråd 02: nye internasjonale tidsserier, bransjetrender og kontrollmål.
# Alle verdier har dokumenterte kildekoder og definisjoner i data/proveniens_02.json.
EUpanel=json.loads((ROOT/'data'/'eurostat_produktivitet_02.json').read_text('utf-8'))
SSBperioder=json.loads((ROOT/'data'/'ssb_produktivitet_perioder_02.json').read_text('utf-8'))
TBUtabell=json.loads((ROOT/'data'/'tbu_sammenligning_02.json').read_text('utf-8'))
BNPserie=json.loads((ROOT/'data'/'ssb_bnp_vekst_02.json').read_text('utf-8'))
for r in EUpanel:
    put('eurostat_produk_02','Produktivitet','BNP per utført time, årlig realvekst','%s' % r['periode'],r['land'],r['vekst_prosent'],'prosent per år','K38','Eurostat 2026','Hele økonomien. Historisk datavintage 27. mars 2026; 2025 er enkeltår, øvrige perioder snitt.')
for r in SSBperioder:
    put('ssb_produk_02','Produktivitet',r['maal']+', '+r['naering'],r['periode'],r['naering'],r['aarlig_vekst_prosent'],'prosent per år','K36','SSB periodetabell','Ikke sammenlikn nivå eller sektorsammensetning uten harmonisering.')
for r in TBUtabell:
    put('tbu_produk_02','Produktivitet','TBU '+r['sammenligning'],r['periode'],r['gruppe'],r['vekst_prosent'],'prosent per år','K39','TBU NOU 2026:5','Handelsvektet sammenlikning; se nøyaktig definisjon og periode.')
for r in BNPserie:
    put('ssb_fastland_gdp_02','Vekst','Fastlands-BNP, årlig realvekst',r['aar'],'Norge',r['fastlands_bnp_vekst_prosent'],'prosent fra året før','K41','SSB historisk serie','BNP, ikke BNP per utført time.')
    put('ssb_total_gdp_02','Vekst','Samlet BNP, årlig realvekst',r['aar'],'Norge',r['samlet_bnp_vekst_prosent'],'prosent fra året før','K41','SSB historisk serie','BNP, ikke BNP per utført time.')

# Tråd 02, utvidelsen v0.4.1: PPP, investeringer, FoU-dekomponering og vareeksport.
TILLEGG02=json.loads((ROOT/'data'/'tilleggsindikatorer_02.json').read_text('utf-8'))
for r in TILLEGG02:
    put('utvidet_02_'+r['indikator'],'Sammenlikning 02',r['indikator'],r['periode'],r['land'],r['verdi'],r['enhet'],r['kilde_id'],r['status'],r['merknad'])
# Tråd 03: historiske SSB-serier, regionale endringer, boligbygging og generasjoner.
PRIS03=json.loads((ROOT/'data'/'boligpris_aar_03.json').read_text('utf-8'))
BYGG03=json.loads((ROOT/'data'/'boligbygging_aar_03.json').read_text('utf-8'))
REGION03=json.loads((ROOT/'data'/'boligpriser_regioner_03.json').read_text('utf-8'))
GEN03=json.loads((ROOT/'data'/'generasjoner_bolig_03.json').read_text('utf-8'))
HOVED03=json.loads((ROOT/'data'/'observasjoner_03.json').read_text('utf-8'))
for r in PRIS03:
    put('boligindeks_03','Bolig og kreditt','Prisindeks for brukte boliger',r['aar'],'Hele landet',r['prisindeks'],'2015=100','K47','Historisk SSB-observasjon',r['definisjon'])
for r in BYGG03:
    put('byggetillatelse_03','Bolig og kreditt','Igangsettingstillatelser',r['aar'],'Norge',r['igangsettingstillatelser'],'boliger','K50','SSB-byggeareal','Ferdigstillelse er en egen årlig hendelse, ikke samme boliger som tillatelse')
    put('fullfort_bolig_03','Bolig og kreditt','Fullførte boliger',r['aar'],'Norge',r['fullforte'],'boliger','K50','SSB-byggeareal','Fullført det aktuelle året')
for r in REGION03:
    put('regionbolig_03','Bolig og kreditt','Regional prisendring år/år',r['periode'],r['region'],r['aar_aar_endring_prosent'],'prosent','K49','SSB andre kvartal 2026','Endring samme kvartal året før; ikke sesongjustert kvartalsendring')
for r in GEN03:
    put('generasjoner03','Generasjoner','Registrert med boligformue innen alder',f"alder-{r['alder']}",r['gruppe'],r['andel_prosent'],'prosent','K08','SSB register','Observasjon for fødselskohorter 1988–1993; ikke en kausal effekt')
for r in HOVED03:
    put('hoved03','Bolig og kreditt',r['indikator'],r['periode'],'Norge',r['verdi'],r['enhet'],r['kilde_id'],'SSB/Finanstilsynet / egne regnestykker',r['merknad'])


# Tråd 04: deskriptiv, separat gjengitt registerserie, kohort/foreldreformue, EU-SILC og utvalgte indikatorer.
EIER04=json.loads((ROOT/'data'/'boligeierskap_alder_04.json').read_text('utf-8'))
FORELDRE04=json.loads((ROOT/'data'/'foreldreformue_bolig_04.json').read_text('utf-8'))
BYRDE04=json.loads((ROOT/'data'/'boutgiftsbelastning_04.json').read_text('utf-8'))
HOVED04=json.loads((ROOT/'data'/'hovedindikatorer_04.json').read_text('utf-8'))
KOHORT04=json.loads((ROOT/'data'/'kohortdekning_04.json').read_text('utf-8'))
for r in EIER04:
    put('boligeier_tverrsnitt_04','Generasjonsøkonomi','Har registrert boligformue ved alderen',r['aar'], f"{r['gruppe']}, {r['alder']} år",r['andel_prosent'],'prosent','K08','SSB tverrsnitt','2014/2023 er ulike befolkningsutvalg; ikke samme fødselskohort')
for r in FORELDRE04:
    put('boligeier_foreldre_04','Generasjonsøkonomi','Registrert boligformue innen alder',r['alder'],r['foreldreformue_gruppe'],r['andel_prosent'],'prosent','K08','SSB kohort','Kohorter 1988-1993, bosatt 2005 og 2023. Aldrene 31-33 omfatter bare fødte som har oppnådd alderen.')
for r in BYRDE04:
    put('boutgifter_byre_04','Generasjonsøkonomi','Svært tyngende boutgifter',r['aar'],r['aldersgruppe'],r['andel_prosent'],'prosent','K69','SSB EU-SILC','Utvalgsundersøkelse, ikke kohortstudie. Manglende år ikke interpolert.')
for r in HOVED04:
    put('indikator_04','Generasjonsøkonomi',r['indikator'],r['periode'],r['gruppe'],r['verdi'],r['enhet'],r['kilde_id'],'SSB/Finanstilsynet, transkripsjon',r['merknad'])
# KOHORT04 er kun dekningstidspunkter, ikke observerte generasjonsutfall.


# Tråd 05: atskilte statistikksystemer for registrering, etablering, vekst, venture, innovasjon og arbeid.
FORETAK05=json.loads((ROOT/'data'/'foretak_kvartal_05.json').read_text('utf-8'))
VENTURE05=json.loads((ROOT/'data'/'venture_norden_05.json').read_text('utf-8'))
ALDER05=json.loads((ROOT/'data'/'etablerere_alder_05.json').read_text('utf-8'))
VEKST05=json.loads((ROOT/'data'/'lovende_startups_05.json').read_text('utf-8'))
LEDIG05=json.loads((ROOT/'data'/'ungdomsarbeid_05.json').read_text('utf-8'))
NYUTD05=json.loads((ROOT/'data'/'nyutdannede_05.json').read_text('utf-8'))
HOVED05=json.loads((ROOT/'data'/'hovedindikatorer_05.json').read_text('utf-8'))
for r in FORETAK05:
    put('foretak_kvartal_05','Entreprenørskap','Nyregistrerte foretak',r['periode'],'Norge',r['totalt'],'registreringer','K77','SSB publisert kvartalsobservasjon','Foretak kvartal; ikke lik nyetablerte aktive foretak. Metodeendring 2026.')
for r in VENTURE05:
    put('venture_norden_05','Risikokapital','Tidligfaseinvesteringer',r['aar'],r['land'],r['mill_eur'],'millioner euro','K82','NVCA/Menon, bransjestatistikk','Foretakets hjemland, avrundet; ikke BNP-justert')
for r in ALDER05:
    put('etablerere_alder_05','Entreprenørskap','Aldersandel personlige etablerere',r['aar'],r['gruppe'],r['andel_prosent'],'prosent','K81','SSB foreløpige estimater','Personer, ikke etablerte foretak')
for r in VEKST05:
    put('lovende_startups_vekst_05','Entreprenørskap','Lovende startups i fortsatt vekst',r['aar_etter'],'Selektert oppstartskohort',r['fortsatt_vekst_prosent'],'prosent','K79','SSB forskning, omtrentlig','Ikke nasjonal niårsoverlevelse; andelen scaleup er inkludert i vekst')
    put('lovende_startups_scaleup_05','Entreprenørskap','Lovende startups blitt scaleups',r['aar_etter'],'Selektert oppstartskohort',r['blitt_scaleup_prosent'],'prosent','K79','SSB forskning, omtrentlig','Kan ikke summeres med andelen i fortsatt vekst')
for r in LEDIG05:
    put('arbeidsledighet_15_24_05','Arbeid','AKU-arbeidsledighet 15–24 år',r['aar'],'Unge i arbeidsstyrken',r['ledighet_15_24_prosent'],'prosent','K87','SSB skole, historiske AKU-verdier','Nevner er ungdom i arbeidsstyrken; ikke NEET-populasjon')
for r in NYUTD05:
    put('nyutd_sysselsetting_05','Arbeid','Sysselsetting blant nyutdannede',r['aar'],'20–34 år, nyutdannede',r['andel_sysselsatt_prosent'],'prosent','K88','SSB AKU','Annen populasjon enn andel i akademiske yrker')
    put('nyutd_akademiske_05','Arbeid','Nyutdannede med høyere utdanning i akademiske yrker',r['aar'],'Nyutdannede med høyere utdanning',r['andel_akademiske_yrker_prosent'],'prosent','K88','SSB AKU','Forskjellig nevner fra sysselsetting blant alle nyutdannede')
for r in HOVED05:
    put('hovedindikatorer_05','Entreprenørskap og arbeid',r['indikator'],r['periode'],r['gruppe'],r['verdi'],r['enhet'],r['kilde_id'],'Hovedobservasjon 05',r['merknad'])


# Tråd 06: separate populasjoner, registre og skatteforslag; aldri likestill latent gevinst med realkapitalflukt.
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

# Delrapport 07: offentlig utgiftsregnskap, COFOG, stillingsandel og metodeindikatorer.
# Årstids- og definisjonsforskjeller bevares i registeret; ingen interpolasjon.
OFF07=json.loads((ROOT/'data'/'offentlige_hovedtall_07.json').read_text('utf-8'))
COFOG07=json.loads((ROOT/'data'/'cofog_utgifter_07.json').read_text('utf-8'))
JOB07=json.loads((ROOT/'data'/'sysselsetting_offentlig_07.json').read_text('utf-8'))
HOVED07=json.loads((ROOT/'data'/'hovedindikatorer_07.json').read_text('utf-8'))
for r in OFF07:
    put('offentlige_hovedtall_07','Offentlig ressursbruk',r['indikator'],r['aar'],'Offentlig forvaltning',r['verdi_mill_kr'],'millioner kroner, løpende priser',r['kilde_id'],r['status'],'SSB offentlig forvaltning, ikke budsjettbevilgning eller kvalitetsmål')
for r in COFOG07:
    put('cofog_07','Offentlig ressursbruk',r['formaal'],r['aar'],'COFOG',r['verdi_mill_kr'],'millioner kroner, løpende priser',r['kilde_id'],r['status'],r['definisjon'])
for r in JOB07:
    put('jobbandel_offentlig_07','Arbeidsallokering','Offentlig andel av jobbforhold',r['periode'],'Offentlig forvaltning',r['offentlig_andel_jobber_prosent'],'prosent',r['kilde_id'],r['status'],'Jobbforhold, ikke sysselsatte personer eller årsverk')
for r in HOVED07:
    put('hovedindikatorer_07','Ressursbruk og tjenester',r['indikator'],r['periode'],r['gruppe'],r['verdi'],r['enhet'],r['kilde_id'],r['status'],r['merknad'])

# Forskningstråd 08: official past data, budget estimates and separately declared forecast assumptions.
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

# Studie 09 – 2026-observasjoner og tydelig merkede offisielle framskrivinger.
POP09=json.loads((ROOT/'data'/'befolkningsbaner_09.json').read_text('utf-8'))
REG09=json.loads((ROOT/'data'/'fylker_09.json').read_text('utf-8'))
HH09=json.loads((ROOT/'data'/'husholdningstyper_09.json').read_text('utf-8'))
BOL09=json.loads((ROOT/'data'/'bolig_husholdning_09.json').read_text('utf-8'))
FERT09=json.loads((ROOT/'data'/'fertilitet_09.json').read_text('utf-8'))
FERTF09=json.loads((ROOT/'data'/'fertilitetsforutsetninger_09.json').read_text('utf-8'))
DOD09=json.loads((ROOT/'data'/'dodsfall_09.json').read_text('utf-8'))
CARE09=json.loads((ROOT/'data'/'omsorgsnokkeltall_09.json').read_text('utf-8'))
ELDRE09=json.loads((ROOT/'data'/'eldre80_09.json').read_text('utf-8'))
for x in POP09:
    for alt in ('MMM','LLL','HHH'):
        put('befolkning_09','Demografi','Innbyggere etter scenario',x['aar'],alt,x[alt],'personer','K152',x['status'],'Registrert i 2026; deretter nasjonal BEFINN-vintage 2026, scenario '+alt)
for x in REG09:
    for year,k in [(2026,'observert_2026'),(2050,'framskrevet_2050')]:
        put('fylker_09','Demografi','Befolkning i fylke',year,x['fylke'],x[k],'personer','K153','Registrert' if year==2026 else 'SSB regional MMMM','Summen av 2050-fylkene 6 195 859 AVVIKER fra nasjonal MMM 6 214 071 på grunn av to forskjellige SSB-modeller (K169)')
for x in HH09:
    put('husholdninger_09','Bolig og demografi','Privathusholdninger',x['aar'],x['type'],x['antall'],'husholdninger','K155','SSB register','Ikke boligbestand eller boenheter')
for x in BOL09:
    put('bolig_09','Bolig og demografi',x['indikator'],x['aar'],'Norge',x['verdi'],x['enhet'],x['kilde_id'],x['status'],'Registrerte boliger minus privathusholdninger er ikke antall salgsklare tomme hjem')
for x in FERT09:
    put('fruktbarhet_09','Demografi','Samlet fruktbarhetstall',x['aar'],'Norge',x['fruktbarhet'],'barn per kvinne',x['kilde_id'],'SSB observert','Periodemål, ikke realisert kohortfruktbarhet')
    put('førstefødsel_09','Demografi','Alder mor ved førstefødsel',x['aar'],'Norge',x['alder_mor_foerste'],'år',x['kilde_id'],'SSB observert','Ikke mål på familiepreferanser eller kohortutfall')
for x in FERTF09:
    for alt in ('MMM','LMM','HMM'):
        put('fruktbarhetsforutsetninger_09','Demografi','Fruktbarhet, betinget SSB-forutsetning',x['aar'],alt,x[alt],'barn per kvinne','K152','SSB antakelse','Må ikke forveksles med framtidige observasjoner')
for x in DOD09:
    put('dødsfall_09','Demografi','Antall dødsfall',x['aar'],'Norge',x['dode'],'personer',x['kilde_id'],x['status'],'Antall døde er ikke antall boliger frigjort')
for x in CARE09:
    put('omsorg_09','Omsorg og arbeidskraft',x['indikator'],x['aar'],'Norge',x['verdi'],x['enhet'],x['kilde_id'],x['status'],'Gap 2040 og historisk omsorg FTE har ulike populasjoner')
for x in ELDRE09:
    put('eldre_09','Omsorg og arbeidskraft','Antall 80 år og eldre',x['aar'],'Norge',x['antall_80_pluss'],'personer',x['kilde_id'],x['status'],'2050 er EGEN avrundet beregning av 9,5 % fra rapporttekst, ikke offisielt eksakt antall')

with (DATA/'observasjoner.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(obs[0].keys()),delimiter=';')
    writer.writeheader();writer.writerows(obs)

# Delrapport 03 inneholder matematiske LaTeX-blokker i Markdown; på nettstedet
# vises en tilgjengelig, egenkontrollert menneskelesbar oppstilling uten nettavhengighet.
import html as html_module
latex_re=r'\$\$\s*\\begin\{flalign\*\}(.*?)\\end\{flalign\*\}\s*\$\$'
latex_human=[
    'Nominell prisfaktor 1993–2025 = 152,5 / 19,0 = 8,0263\nGjennomsnittlig sammensatt nominell vekstrate ≈ 6,72 % per år',
    'B = 9 159 mrd. kr (boliger)\nN = 11 958 mrd. kr (avgrenset nettoformue)\nBoligandel = 9 159 / 11 958 ≈ 76,59 %\nEtter prisfall d: N etter = 11 958 − 9 159 × d',
    'Pris ved kjøp = 5,4 mill. kr; lån = 4,86 mill. kr\nPris etter fall d = pris × (1 − d)\nEgenkapital etter fall = pris etter fall − lån\nVed 10 % fall: 0 kr; ved 20 % fall: −0,54 mill. kr',
    'Teoretisk lånetak = min(90 % av boligpris, 5 × bruttoinntekt − eksisterende gjeld)\nMinste egne midler utenfor lån = boligpris − lånetak\nFinansieringsgap = max(0, minste egne midler − egne midler − familiestøtte)'
    'Utbytteskatt + selskapsskatt: 1 − (1 − 0,22) × (1 − 0,3784) = 51,5152 %. Gjelder fullt utdelt overskudd uten skjerming.',
    'Skattepliktig aksjeverdi = 10 mill. × 0,8 = 8 mill. kr.\nFormuesskatt = (8 mill. − 1,9 mill.) × 1 % = 61 000 kr.\nBrutto utbytte uten skjerming = 61 000 / 0,6216 ≈ 98 134 kr.\nOverskudd før selskapsskatt = 98 134 / 0,78 ≈ 125 813 kr.'
]
ix=[0]
def latex_to_visible(m):
    n=ix[0];ix[0]+=1
    s=latex_human[n] if n<len(latex_human) else 'Formelen er dokumentert i Markdown-utgaven.'
    return '<div class="formel formel-flere" role="math" aria-label="Regnemodell">'+html_module.escape(s).replace('\n','<br>')+'</div>'
body=re.sub(latex_re,latex_to_visible,body,flags=re.S)
markdown=MarkdownIt('commonmark',{'html':True,'typographer':True}).enable('table').enable('strikethrough')
soup=BeautifulSoup(markdown.render(body),'html.parser')

# Bygg stabile interne lenker i hele rapporten; behold faglige K01--K22-kildeankre.
def slugify(s):
    ascii_str=''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+','-',ascii_str).strip('-')[:72]
seen=set()
for tag in soup.find_all(['h1','h2','h3','h4']):
    slug='rapport-'+slugify(tag.get_text())
    base=slug;i=2
    while slug in seen:
        slug=base+'-'+str(i);i+=1
    tag['id']=slug;seen.add(slug)

# Egne henvisningslenker som fungerer også når nettleseren ikke lenkifiserer rene URL-er.
for a in soup.find_all('a',id=re.compile(r'^k\d+$')):
    source=smap.get(a['id'].upper())
    if not source:continue
    for i,url in enumerate(source['url']):
        link=soup.new_tag('a',href=url)
        link['class']='kilde-ekstern'
        link['target']='_blank';link['rel']='noopener noreferrer'
        link.string='Åpne originalkilde' if len(source['url'])==1 else f'Åpne originalkilde {i+1}'
        a.parent.append(' ')
        a.parent.append(link)

# Formelen vises lesbart uten tredjeparts Javascript-avhengigheter.
for p in soup.find_all('p'):
    if '$$F_{t+1}' in p.get_text():
        formula=soup.new_tag('div');formula['class']='formel'; formula['role']='math'
        formula.append(BeautifulSoup('F<sub>t+1</sub> = F<sub>t</sub> · (1 + r) − U<sub>t</sub> &nbsp;&nbsp; | &nbsp;&nbsp; U<sub>t+1</sub> = U<sub>t</sub> · (1 + g)', 'html.parser'))
        p.replace_with(formula)

# Plasser brede regnskapstabeller i horisontalt rullbare containere.
for tabell in soup.find_all('table'):
    wrapper=soup.new_tag('div');wrapper['class']='tabell-rull';tabell.wrap(wrapper)

# Gjør report-tabs og kapitler navigerbare og søkbare.
chapters=[]
for h in soup.find_all('h2'):
    chapters.append({'id':h['id'],'title':h.get_text(' ',strip=True)})
article=soup.new_tag('article',id='forskningsrapport')
article['class']='rapport-tekst'
head=soup.new_tag('div');head['class']='rapport-fulloverskrift'
# Flytt alle noder fra soup over i artikkelen og pakk kapitler i sections.
children=list(soup.contents)
current=None
for child in children:
    if getattr(child,'name',None)=='h2':
        current=soup.new_tag('section',id='del-'+child.get('id',''))
        current['class']='rapport-kapittel';current['data-overskrift']=child.get_text(' ',strip=True)
        article.append(current)
    (current or article).append(child)
article_html=str(article)
article_html=article_html.replace('href="#12-forskningstrad-01-metode-forskningsarkitektur-og-evidens"','href="#rapport-12-forskningstrad-01-metode-forskningsarkitektur-og-evidens"')

# Forsøk basert på eksplisitt registrete hypoteser; søkeindeksen gjenspeiler rapportens egne formuleringer.
hypotheses=[]
for h in article.find_all('h3'):
    t=h.get_text(' ',strip=True)
    match=re.match(r'^(H\d\d)\s+—\s+(.+)',t)
    if match:
        nextnode=h.find_next_sibling('p')
        if nextnode is None: continue
        p=nextnode.get_text(' ',strip=True)
        def segment(start,end):
            m=re.search(r'\b'+re.escape(start)+r':\s*(.*?)(?=\b'+re.escape(end)+r':|$)',p)
            return m.group(1).strip() if m else ''
        hypothesis=segment('Hypotese','Motforklaring')
        against=segment('Motforklaring','Variabler og test')
        status_m=re.search(r'Status\s*(.*?)(?:\s*Falsifikasjon:|$)',p)
        st=status_m.group(1).strip(' .;') if status_m else 'Ikke ferdig testet'
        hypotheses.append({'id':match.group(1),'tittel':match.group(2), 'hypotese':hypothesis, 'motforklaring':against,'status':st,'ankerkobling':'#'+h['id']})
assert len(hypotheses)==12, f'Fant bare {len(hypotheses)} hypoteser'
for traad in ('02','03','04','05','06','07','08','09'):
    next_hypotheses=json.loads((ROOT/'data'/f'hypoteseregister_{traad}.json').read_text('utf-8'))
    for item in next_hypotheses:
        hypotheses.append({'id':item['id'],'tittel':item['tittel'],
          'hypotese':item['hypotese'],'motforklaring':item['mothypotese'],
          'status':item['status'],'ankerkobling':'#rapport-'+('18-forskningstrad-07-offentlig-ressursbruk-effektivitet-og-baumols-kostn' if traad=='07' else ('13-forskningstrad-02-norsk-okonomis-relative-utvikling-og-internasjonal-sammenligning' if traad=='02' else ('14-forskningstrad-03-bolig-kreditt-eiendomsformue-og-kapitalallokering' if traad=='03' else '15-forskningstrad-04-generasjonsokonomi-mobilitet-og-fordeling' if traad=='04' else '16-forskningstrad-05-entreprenorskap-skalering-og-unges-arbeidsmarked' if traad=='05' else '17-forskningstrad-06-skatt-eierskap-kapitalmobilitet-og-utflytting')))})
# Report 08 has a dedicated chapter; not a subchapter of taxation.
for hypo in hypotheses:
    if hypo['id'].startswith('H08-'):
        hypo['ankerkobling']='#rapport-19-forskningstrad-08-petroleum-spu-og-finanspolitisk-b-rekraft'
for hypo in hypotheses:
    if hypo['id'].startswith('H09-'):
        hypo['ankerkobling']='#rapport-20-forskningstrad-09-demografi-arbeidskraft-bolig-og-velferdsstatens-b-r'
assert len(hypotheses)==109, f'Uventet antall hypoteser: {len(hypotheses)}'


# Strukturert evidensregister vises i eget interaktivt felt.
evidence=json.loads((ROOT/'data'/'evidensregister_01.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_02.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_03.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_04.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_05.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_06.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_07.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_08.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_09.json').read_text('utf-8'))
assert len(evidence)==276, f'evidens: {len(evidence)}'

# HTML-mal lagres som kildefil ved siden av byggeskriptet.
template=TEMPLATE.read_text('utf-8')
subst={
  '@@ARTIKKEL@@':article_html,
  '@@KAPITLER@@': json.dumps(chapters,ensure_ascii=False).replace('<','\\u003c'),
  '@@HYPOTESER@@':json.dumps(hypotheses,ensure_ascii=False).replace('<','\\u003c'),
  '@@KILDER@@':json.dumps(sources,ensure_ascii=False).replace('<','\\u003c'),
  '@@OBSERVASJONER@@':json.dumps(obs,ensure_ascii=False).replace('<','\\u003c'),
  '@@ANTALLOBS@@':str(len(obs)),
  '@@ANTALLKILDER@@':str(len(sources)),
  '@@ANTALLEVIDENS@@':str(len(evidence)),
  '@@EVIDENS@@':json.dumps(evidence,ensure_ascii=False).replace('<','\\u003c'),
  '@@EU02@@':json.dumps(EUpanel,ensure_ascii=False).replace('<','\\u003c'),
  '@@BNP02@@':json.dumps(BNPserie,ensure_ascii=False).replace('<','\\u003c'),
  '@@TBU02@@':json.dumps(TBUtabell,ensure_ascii=False).replace('<','\\u003c'),
  '@@TILLEGG02@@':json.dumps(TILLEGG02,ensure_ascii=False).replace('<','\\u003c'),

  '@@PRIS03@@':json.dumps(PRIS03,ensure_ascii=False).replace('<','\u003c'),
  '@@BYGG03@@':json.dumps(BYGG03,ensure_ascii=False).replace('<','\u003c'),
  '@@REGION03@@':json.dumps(REGION03,ensure_ascii=False).replace('<','\u003c'),
  '@@GEN03@@':json.dumps(GEN03,ensure_ascii=False).replace('<','\u003c'),
  '@@EIER04@@':json.dumps(EIER04,ensure_ascii=False).replace('<','\u003c'),
  '@@FORELDRE04@@':json.dumps(FORELDRE04,ensure_ascii=False).replace('<','\u003c'),
  '@@BYRDE04@@':json.dumps(BYRDE04,ensure_ascii=False).replace('<','\u003c'),
  '@@KOHORT04@@':json.dumps(KOHORT04,ensure_ascii=False).replace('<','\u003c'),
  '@@FORETAK05@@':json.dumps(FORETAK05,ensure_ascii=False).replace('<','\\u003c'),
  '@@VENTURE05@@':json.dumps(VENTURE05,ensure_ascii=False).replace('<','\\u003c'),
  '@@ETABALDER05@@':json.dumps(ALDER05,ensure_ascii=False).replace('<','\\u003c'),
  '@@VEKST05@@':json.dumps(VEKST05,ensure_ascii=False).replace('<','\\u003c'),
  '@@LEDIG05@@':json.dumps(LEDIG05,ensure_ascii=False).replace('<','\\u003c'),
  '@@NYUTD05@@':json.dumps(NYUTD05,ensure_ascii=False).replace('<','\\u003c'),
  '@@FLYT06@@':json.dumps(FLYT06,ensure_ascii=False).replace('<', '\\u003c'),
  '@@EXIT06@@':json.dumps(EXIT06,ensure_ascii=False).replace('<', '\\u003c'),
  '@@SAT06@@':json.dumps(SAT06,ensure_ascii=False).replace('<', '\\u003c'),
  '@@NOU06@@':json.dumps(NOU06,ensure_ascii=False).replace('<', '\\u003c'),
  '@@OFF07@@':json.dumps(OFF07,ensure_ascii=False).replace('<','\u003c'),
  '@@COFOG07@@':json.dumps(COFOG07,ensure_ascii=False).replace('<','\u003c'),
  '@@JOB07@@':json.dumps(JOB07,ensure_ascii=False).replace('<','\u003c'),
  '@@HOVED07@@':json.dumps(HOVED07,ensure_ascii=False).replace('<','\u003c'),
  '@@FONDSBRUK08@@':json.dumps(FONDSBRUK08,ensure_ascii=False).replace('<','\u003c'),
  '@@PETROL08@@':json.dumps(PETROL08,ensure_ascii=False).replace('<','\u003c'),
  '@@FUND08@@':json.dumps(FUND08,ensure_ascii=False).replace('<','\u003c'),
  '@@UTTAK08@@':json.dumps(UTTAK08,ensure_ascii=False).replace('<','\u003c'),
  '@@BUDSJ08@@':json.dumps(BUDSJ08,ensure_ascii=False).replace('<','\u003c'),
  '@@HOVED08@@':json.dumps(HOVED08,ensure_ascii=False).replace('<','\u003c'),
  '@@SCEN08@@':json.dumps(SCEN08,ensure_ascii=False).replace('<','\u003c'),
  '@@POP09@@':json.dumps(POP09,ensure_ascii=False).replace('<','\u003c'),
  '@@REG09@@':json.dumps(REG09,ensure_ascii=False).replace('<','\u003c'),
  '@@HH09@@':json.dumps(HH09,ensure_ascii=False).replace('<','\u003c'),
  '@@BOL09@@':json.dumps(BOL09,ensure_ascii=False).replace('<','\u003c'),
  '@@FERT09@@':json.dumps(FERT09,ensure_ascii=False).replace('<','\u003c'),
  '@@FERTF09@@':json.dumps(FERTF09,ensure_ascii=False).replace('<','\u003c'),
  '@@DOD09@@':json.dumps(DOD09,ensure_ascii=False).replace('<','\u003c'),
  '@@CARE09@@':json.dumps(CARE09,ensure_ascii=False).replace('<','\u003c'),
  '@@ELDRE09@@':json.dumps(ELDRE09,ensure_ascii=False).replace('<','\u003c'),
}
for key,val in subst.items():
    assert key in template,key
    template=template.replace(key,val)
assert '@@' not in template, 'Uutfylt malvariabel'
(SITE/'index.html').write_text(template,encoding='utf-8')
def copy_if_different(source, target):
    if Path(source).resolve() != Path(target).resolve():
        shutil.copyfile(source,target)
for pattern in ('*_01.*','*_02.*','*_03.*','*_04.*','*_05.*','*_06.*','*_07.*','*_08.*','*_09.*'):
    for record in (ROOT/'data').glob(pattern):
        copy_if_different(record,DATA/record.name)
copy_if_different(ROOT/'data'/'proveniens_tillegg_02.json',DATA/'proveniens_tillegg_02.json')
copy_if_different(ROOT/'01_Forskningsarkitektur_metode_evidens_v0.3.0.md',SITE/'01_Forskningsarkitektur_metode_evidens_v0.3.0.md')
copy_if_different(ROOT/'02_Norges_relative_okonomiske_utvikling_v0.4.1.md',SITE/'02_Norges_relative_okonomiske_utvikling_v0.4.1.md')
copy_if_different(ROOT/'03_Bolig_kreditt_eiendomsformue_kapitalallokering_v0.5.0.md',SITE/'03_Bolig_kreditt_eiendomsformue_kapitalallokering_v0.5.0.md')
copy_if_different(ROOT/'04_Generasjonsokonomi_mobilitet_fordeling_v0.6.0.md',SITE/'04_Generasjonsokonomi_mobilitet_fordeling_v0.6.0.md')
copy_if_different(ROOT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md',SITE/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md')
copy_if_different(ROOT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md',SITE/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')
copy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',SITE/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')
copy_if_different(ROOT/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md',SITE/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md')
copy_if_different(ROOT/'09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md',SITE/'09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md')
copy_if_different(ROOT/'data'/'proveniens_04.json',DATA/'proveniens_04.json')
copy_if_different(ROOT/'data'/'proveniens_03.json',DATA/'proveniens_03.json')
copy_if_different(MD,SITE/MD.name)
copy_if_different(ROOT/'LES-MEG.md',SITE/'LES-MEG.md')

# Enkeltfiler for direkte tilgang ved siden av en opplastbar ZIP-pakke.
OUT=ROOT.parent
out_html=OUT/f'Norsk_Okonomi_Interaktiv_{DATE}_{VERSION}.html'
out_md=OUT/f'Norsk_Okonomi_Forskningsrapport_{DATE}_{VERSION}.md'
shutil.copyfile(SITE/'index.html',out_html)
shutil.copyfile(MD,out_md)
copy_if_different(ROOT/'03_Bolig_kreditt_eiendomsformue_kapitalallokering_v0.5.0.md',OUT/'03_Bolig_kreditt_eiendomsformue_kapitalallokering_v0.5.0.md')
copy_if_different(ROOT/'04_Generasjonsokonomi_mobilitet_fordeling_v0.6.0.md',OUT/'04_Generasjonsokonomi_mobilitet_fordeling_v0.6.0.md')
copy_if_different(ROOT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md',OUT/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md')
copy_if_different(ROOT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md',OUT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')
copy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',OUT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')
copy_if_different(ROOT/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md',OUT/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md')
copy_if_different(ROOT/'09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md',OUT/'09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md')
for name in ('evidensregister_09.csv','hypoteseregister_09.csv','proveniens_09.json'):
    copy_if_different(ROOT/'data'/name,OUT/name.replace('.csv','_v1.1.0.csv') if name.endswith('.csv') else OUT/name)
# Oppdater SHA-256-manifestet før publiseringsarkivet pakkes, for hver fil som skal med.
# Temporære nettlesertestbilder og rå CSV-eksporttester er ikke publiseringsinnhold.
import hashlib
def public_file(f):
    parts=f.relative_to(SITE).parts
    return f.is_file() and f.name!='MANIFEST-SHA256.txt' and '__pycache__' not in parts and not f.name.startswith(('qa_','_test_web', 'patch_'))

manifest=[]
for file in sorted(SITE.rglob('*')):
    if public_file(file):
        manifest.append(f"{hashlib.sha256(file.read_bytes()).hexdigest()}  {file.relative_to(SITE).as_posix()}")
(SITE/'MANIFEST-SHA256.txt').write_text('\n'.join(manifest)+'\n',encoding='utf-8')
zipf=OUT/f'Norsk_Okonomi_Nettside_Publisering_{DATE}_{VERSION}.zip' 
with zipfile.ZipFile(zipf,'w',zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for file in sorted(SITE.rglob('*')):
        if public_file(file) or file.name == 'MANIFEST-SHA256.txt':z.write(file,str(file.relative_to(SITE)))
    if not PACKAGED:
        z.write(SCRIPT,'kildekode/bygg_publisering.py')
        z.write(TEMPLATE,'kildekode/mal_nettside.html')
        if (ROOT/'lag_02.py').exists(): z.write(ROOT/'lag_02.py','kildekode/lag_02.py')
        if (ROOT/'ferdigstill_041.py').exists(): z.write(ROOT/'ferdigstill_041.py','kildekode/ferdigstill_041.py')
        z.write(ROOT/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.3.0.md','arkiv/Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.3.0.md')
print(f'Kilder: {len(sources)}; observasjoner: {len(obs)}; hypoteser: {len(hypotheses)}; kapitler: {len(chapters)}')
for file in [MD,out_md,out_html,zipf]:print(file,round(file.stat().st_size/1024,1),'KiB')
