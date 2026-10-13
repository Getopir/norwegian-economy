#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Registrerer kontrollert publiserte aggregater og egne scenarier for forskningsområde 08.
OBSERVASJON = offentlig tall med datavintage; MODELL = hypotetisk beregning.
"""
from pathlib import Path
import sys, csv, json, hashlib
R=Path(__file__).resolve().parent
D=R/'data';D.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'kildekode'))
from modell_08 import SCENARIOER, STARTFOND, STARTPETROLEUM, STARTUTTAK, beregn_bane
STAMP='2026-10-13'; VERSION='1.0.0'
SOURCES=[
(137,'Finansdepartementet (2026)','Meld. St. 1 (2026–2027): Nasjonalbudsjettet 2027, kapittel 3, tabeller 3.1, 3.6, 3.8 og 3.9 og langsiktige baner. Publisert 7. oktober 2026. https://www.regjeringen.no/no/dokumenter/meld.-st.-1-20262027/id3175768/?ch=3'),
(138,'Finansdepartementet (2026)','Nøkkeltall i Nasjonalbudsjettet 2027. Publisert 7. oktober 2026. https://www.regjeringen.no/no/aktuelt/nokkeltall-i-nasjonalbudsjettet-2027/id3174610/'),
(139,'Finansdepartementet (2026)','Statsbudsjettet 2027: Statens inntekter og utgifter, inkludert oljekorrigert underskudd. Publisert 7. oktober 2026. https://www.regjeringen.no/no/statsbudsjett/2027/statsbudsjettet-2027-statens-inntekter-og-utgifter/id3173250/'),
(140,'Norges Bank Investment Management (2026)','Halvårsrapport 2026, publisert 12. august 2026; markedsverdi, avkastning og valutaeffekter per 30. juni 2026. https://www.nbim.no/no/nyheter-og-innsikt/rapporter/2026/halvarsrapport-2026/nettrapport-halvarsrapport-2026/'),
(141,'Norges Bank Investment Management (2026)','Årsrapport 2025: verdivurdering, nominelle bidrag, avkastning og netto realavkastning 1998–2025. https://www.nbim.no/en/news-and-insights/reports/2025/annual-report-2025/web-report-annual-report-2025'),
(142,'Norskpetroleum.no / Finansdepartementet (2026)','Statens inntekter fra petroleumsvirksomhet. 2026- og 2027-anslag, oppdatert 7. oktober 2026. https://www.norskpetroleum.no/okonomi/statens-inntekter/'),
(143,'Finansdepartementet (2024)','Meld. St. 31 (2023–2024): Perspektivmeldingen 2024; inndekningsbehovet 2060 og demografiske mekanismer. https://www.regjeringen.no/no/dokumenter/meld.-st.-31-20232024/id3049290/?ch=7'),
(144,'Finansdepartementet (2024/2026)','Bruk av fondsmidler i årene fremover; handlingsregelen og forutsetninger om 3 % forventet realavkastning. https://www.regjeringen.no/no/tema/okonomi-og-budsjett/norsk_okonomi/bruk-av-oljepenger-/bruk-av-fondsmidler-i-arene-framover/id450470/'),
(145,'Det internasjonale pengefondet – IMF (2026)','Norway: Staff Concluding Statement of the 2026 Article IV Mission. Publisert 3. september 2026. https://www.imf.org/en/news/articles/2026/09/03/mcs090326-norway-staff-concluding-statement-of-the-2026-article-iv-mission'),
(146,'Norges Bank Investment Management (2026)','Stress Testing 2025: hypotetiske scenarier for fondstap på 20–37 %. https://www.nbim.no/contentassets/c7d3b015300d48a1ac0136f069b9bed7/gpfg_stresstesting-2025.pdf'),
(147,'Finansdepartementet (2026)','Datagrunnlag for fig. 3.3: historisk uttaksprosent 2001–2026 og rettesnor 4/3 %. Regjeringens publiserte tabellgrunnlag. https://www.regjeringen.no/contentassets/f0bee855059446a0bec37bed12b6b830/kap-3_2026-filer/sheet004.htm'),
(148,'Finansdepartementet (2017)','Meld. St. 26 (2016–2017), Forvaltningen av Statens pensjonsfond i 2016. Forventet realavkastning og endring fra 4 til 3 %. https://www.regjeringen.no/no/dokumenter/meld.-st.-26-20162017/id2545354/?ch=1'),
(149,'Corden, W. M. og Neary, J. P. (1982)','Booming Sector and De-Industrialisation in a Small Open Economy. The Economic Journal 92(368), 825–848. https://doi.org/10.2307/2232670'),
(150,'Hartwick, J. M. (1977)','Intergenerational Equity and the Investing of Rents from Exhaustible Resources. American Economic Review 67(5), 972–974. https://ideas.repec.org/a/aea/aecrev/v67y1977i5p972-74.html'),
(151,'Finansdepartementet (2026)','Prop. 1 S (2026–2027), kapittel 3, seksjon om Statens pensjonsfond og faktisk overføring mellom budsjett og fond. https://www.regjeringen.no/no/dokumenter/prop.-1-s-20262027/id3175738/?ch=3'),
]
assert len(SOURCES)==15 and [s[0] for s in SOURCES]==list(range(137,152))

def write_pair(stem,rows):
    (D/f'{stem}.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if rows:
        fields=list(dict.fromkeys(k for row in rows for k in row.keys()))
        with (D/f'{stem}.csv').open('w',encoding='utf-8-sig',newline='') as fh:
            w=csv.DictWriter(fh,fieldnames=fields,delimiter=';',extrasaction='ignore');w.writeheader();w.writerows(rows)

budget=[]
for y,stru,main,spend,spu in [(2025,507.4,11.6,24.5,2.6),(2026,583.4,12.7,26.5,2.7),(2027,608.4,12.6,26.6,2.7)]:
    budget.append({'aar':y,'strukturelt_underskudd_lopende_mrd':stru,'andel_trend_fastlands_bnp_prosent':main,'andel_statsbudsjettets_utgifter_prosent':spend,'andel_fondsverdi_prosent':spu,'kilde_id':'K137','budsjettvintage':'2026-10-07 – Nasjonalbudsjettet 2027','observasjonsstatus': '2027 regjeringens forslag' if y==2027 else 'tidligere år revidert i Nasjonalbudsjettet 2027','merknad':'Strukturell, konjunkturjustert indikator; ikke faktisk kontantoverføring'})
write_pair('fondsbruk_08',budget)
pet=[]
for y,components in [(2026,{'Skatt på petroleum':378.0,'Miljø- og arealavgift':11.1,'Netto SDØE':256.1,'Equinor-utbytte':25.4,'Sum petroleum netto':670.6}),(2027,{'Skatt på petroleum':346.6,'Miljø- og arealavgift':12.3,'Netto SDØE':184.8,'Equinor-utbytte':24.7,'Sum petroleum netto':568.4})]:
    for k,v in components.items():
        pet.append({'aar':y,'komponent':k,'milliarder_kroner_lopende':v,'kilde_id':'K142','status':'Nasjonalbudsjettet 2027-anslag', 'merknad':'Summens underposter avrundet; bruk publisert sum fremfor å utlede fra delkomponenter.'})
write_pair('petroleum_08',pet)

fiscal_cash=[]
for y,typ,v,k,desc in [
 (2026,'Oljekorrigert kontantunderskudd',454.8,'K137','2026-vintage per Nasjonalbudsjettet 2027; engangseffekt fra skattetrekkskonto'),
 (2026,'Strukturelt oljekorrigert underskudd',583.4,'K137','Konjunktur- og bokføringseffekt justert'),
 (2027,'Oljekorrigert kontantunderskudd',561.7,'K139','Budsjettert kontantoverføring fra SPU'),
 (2027,'Strukturelt oljekorrigert underskudd',608.4,'K137','Finanspolitisk styringsmål, ikke lik kontantoverføring'),
 (2027,'Statens inntekter uten petroleum',1725.,'K139','Statens budsjetterte inntekter uten petroleum'),
 (2027,'Statens utgifter uten petroleum',2287.,'K139','Statens budsjetterte utgifter uten petroleum'),
 (2027,'Statens samlede inntekter',2328.,'K139','Inkludert petroleum, budsjettføring'),
 (2027,'Statens samlede utgifter',2322.,'K139','Inkludert petroleum, budsjettføring'),
 (2027,'SPU beregningsteknisk kapital ved inngang',22400.,'K138','Anslag, ikke markedsobservasjon'),
 (2027,'Realisert netto petroleumsstrøm fra staten, anslag',568.4,'K142','Budsjettanslag'),
]: fiscal_cash.append({'aar':y,'indikator':typ,'milliarder_kroner_lopende':v,'kilde_id':k,'status':desc})
write_pair('regnskapsbegreper_08',fiscal_cash)

fund=[]
for year,v in [(2016,7510),(2017,8488),(2018,8256),(2019,10088),(2020,10914),(2021,12340),(2022,12429),(2023,15757),(2024,19742),(2025,21268)]:
  fund.append({'periode':str(year),'aar':year,'fond_mrd_nok':v,'kilde_id':'K141' if year>=2021 else 'K06','status':'Faktisk markedsverdi ved utgangen av året','merknad':'Løpende NOK; inkluderer valuta, avkastning og netto kapitaltilførsel'})
fund.append({'periode':'2026-H1','aar':2026,'fond_mrd_nok':22683,'kilde_id':'K140','status':'Faktisk markedsverdi per 30. juni 2026','merknad':'Halvårsobservasjon, ikke 2026 årsverdi'})
write_pair('fondsverdi_08',fund)

historical=[3.9,4.8,5.5,4.6,4.2,3.0,2.4,2.6,3.8,3.7,3.0,3.4,3.3,3.0,2.7,2.7,2.9,2.4,2.8,3.6,3.1,2.6,2.9,2.6,2.6,2.7]
assert len(historical)==26
withdraw=[{'aar':2001+n,'uttaksprosent':v,'forventet_realavkastning_prosent':4 if 2001+n<=2017 else 3,'kilde_id':'K147','status':'Offentlig publisert historisk figurserie per 2026; eldre anslagsvintage','merknad':'Budsjettindikator, ikke årlig realisert avkastning'} for n,v in enumerate(historical)]
withdraw.append({'aar':2027,'uttaksprosent':2.7,'forventet_realavkastning_prosent':3,'kilde_id':'K137','status':'Anslag fra regjeringens budsjettforslag for 2027','merknad':'2027 fra NB27; for 2001–2026 fra publisert finansdepartementstabell 2026'})
write_pair('uttaksprosent_historikk_08',withdraw)

ind=[
 ('Fond realavkastning, annualisert 1998–2025',2025,4.34,'prosent','K141','Regnskapsrapport, historisk annualisert; ingen framtidsgaranti'),
 ('Fond realavkastning, annualisert 1998–H1 2026','2026-H1',4.51,'prosent','K140','Regnskap, historisk annualisert'),
 ('Fond avkastning, 2025 i valutakurv',2025,15.11,'prosent','K141','Historisk kalenderår'),
 ('Fond avkastning, 2026 første halvår i valutakurv','2026-H1',9.44,'prosent','K140','Historisk halvår'),
 ('Kronekursbidrag til fondets verdi 2025',2025,-1155,'mrd. NOK','K141','Regnskapseffekt fra valutakurser'),
 ('Kronekursbidrag til fondets verdi 2026 H1','2026-H1',-427,'mrd. NOK','K140','Regnskapseffekt fra valutakurser'),
 ('Fondsverdi mot Fastlands-BNP, 2029',2029,4.9,'multiplikator','K137','Betinget statlig framskriving'),
 ('Fondsverdi mot Fastlands-BNP, 2060',2060,4.5,'multiplikator','K137','Betinget statlig framskriving'),
 ('Strukturelt underskudd som % av trend-Fastlands-BNP, 2001',2001,2.0,'prosent','K137','Historisk finanspolitisk mål'),
 ('Inndekningsbehov i 2060, Perspektivmeldingen 2024','2060-vintage-2024',6.2,'prosent Fastlands-BNP','K143','Betinget framskriving, ikke realisert tall'),
 ('Inndekningsbehov i 2060, Nasjonalbudsjettet 2026','2060-vintage-2025',5.9,'prosent Fastlands-BNP','K125','Betinget framskriving, ikke realisert tall'),
 ('Inndekningsbehov i 2060, Nasjonalbudsjettet 2027','2060-vintage-2026',5.8,'prosent Fastlands-BNP','K137','Betinget framskriving, ikke realisert tall'),
 ('Endring offentlig inntekt 2027–2060',2060,-2.2,'prosentpoeng Fastlands-BNP','K137','Betinget framskriving'),
 ('Endring offentlig utgift 2027–2060',2060,3.6,'prosentpoeng Fastlands-BNP','K137','Betinget framskriving'),
 ('Hypotetisk stresstest: ekstremvær',2025,-20,'prosent fond','K146','D — hypotetisk stressmodell; ingen prognose'),
 ('Hypotetisk stresstest: regional gjeldskrise',2025,-32,'prosent fond','K146','D — hypotetisk stressmodell; ingen prognose'),
 ('Hypotetisk stresstest: AI-korreksjon',2025,-35,'prosent fond','K146','D — hypotetisk stressmodell; ingen prognose'),
 ('Hypotetisk stresstest: fragmentert verden',2025,-37,'prosent fond','K146','D — hypotetisk stressmodell; ingen prognose'),
]
ind=[{'indikator':a,'periode':str(b),'verdi':c,'enhet':d,'kilde_id':e,'status':f,'merknad':f} for a,b,c,d,e,f in ind]
write_pair('hovedindikatorer_08',ind)

hyp_defs=[
('Fondsbruk versus skattebase','Økt strukturelt underskudd har systematisk erstattet manglende vekst i fastlandsskattebasen','Oppspart formue brukes planmessig, mens fastlandsskattebasen utvikler seg normalt','Strukturelt underskudd, skatter, timeverk, BNP og fondsverdi','K137 K138 K01','Deskriptiv dekomponering og kontroll for produktivitets-/sysselsettingsvekst 2001–2027','Historisk fondsbruk øker uten systematisk svakere vekst i fastlandsskattebasen'),
('Vedvarende lav realavkastning','Realavkastning under 3 % i lange perioder reduserer varig finanspolitisk rom','Utgifts-/uttakstilpasning og fortsatt petroleum begrenser tap','Porteføljerisiko, avkastning, fondskapital, varige utgifter','K137 K140 K146','Stokastisk stresstest koblet til ulike finanspolitiske reaksjonsregler','Normalårskorrigert uttaksandel forblir bærekraftig på tvers av de undersøkte avkastningsregimene'),
('Lavere kontantstrøm fra petroleum','Nettotilførselen til SPU avtar raskere enn budsjettert innfasing','Oljepris, investering, teknologi og skatteprofil kompenserer','Volum, pris, skatt, SDØE, nettopetroleum og innskudd','K142 K137','Backtest av priser/volum/utgifter 1971–2027 og prognosevintage','Netto petroleumskontantstrøm vokser relativt til kontantuttak gjennom robust tidsvindu'),
('Markedsgevinst og varige forpliktelser','Stigende fondskurser etterfølges av mer vedvarende offentlig ressursbruk','Handlingsregelen glatter svingninger og setter motsykliske rammer','SPU avkastning, finanspolitisk impuls, varige bevilgninger','K137 K145','Eventstudie over markedsbevegelser kontrollert for vekst og politiske skift','Ingen robust varig budsjetteffekt utover beregnet realavkastning'),
('Politisk omstillingspress','Stor SPU-reserve øker sannsynligheten for å utsette ulønnsomme ordninger','Likvid buffer muliggjør gode reformer og risikodemping','Kuttforslag, budsjettbindinger, evaluering, politisk horisont','K145 K137 K116','Saksnivå og ex post evaluering med kontrollcase og beslutningsspor','Ingen systematisk forsinket omprioritering der finansielt handlingsrom er størst'),
('Ressursdrevet realappresiering','Petroleum og fondsfinansiert etterspørsel svekker deler av konkurranseutsatt sektor','Global strukturendring, oljeleverandørnæring og kvalitet forklarer forhold','Realvalutakurs, lønn, eksportmarkedsandel, industriinvestering','K149 K39 K36','Sektorpanelet 02 med handelseksponering, konjunktur og verdenssjokk','Negativ virkning forsvinner etter relevant kontroll'),
('Aldring og skattebasen','Aldersrelatert utgiftsvekst overstiger bærekraftig økning i skattegrunnlag','Økt yrkesdeltakelse, migrasjon og teknologi reduserer gap','Forsørgerkvote, helseutgifter, pensjon, sysselsetting','K137 K143','Replikasjon av 2060-baner med kobling til kohortregnskap 09','Robuste baner med alders- og behovsjustering viser fravær av finansieringsgap'),
('Buffer under treprosentregelen','Lavere normalårsuttak skaper nødvendig finanspolitisk buffer','Høyere uttak kan likevel gi høyere sosial nettoverdi','Uttaksandel, finanspolitisk impuls, volatilitet, samfunnsnytte','K137 K144','Regimeanalyse med tapsfunksjon og uttaks-/bufferalternativer','Motsyklisk buffer gir ingen robust velferds-/risikofordel'),
('Valutaverdsettelse','NOK-verdi kan maskere risiko for reell norsk budsjettkjøpekraft','Kronefleksibilitet gir støtdemping av nasjonaløkonomien','NOK, valutakurv, reell valuta, importpriser og finanspolitisk uttak','K140 K141','Regnskapsbro og scenarioer med og uten valutaeffekt','Økt NOK-verdi følges konsistent av lik økning i internasjonal og norsk kjøpekraft'),
('Forsvar og pensjonsbindinger','Store fremtidige forpliktelser kan redusere investering og fleksibilitet','Beredskap/helse gir varige inntekter og resiliens','Bindinger, årlige tiltak, samfunnsøkonomisk nytte, skatt','K137 K143','Budsjettforpliktelser eks post vs alternativkapitalbruk','Ingen redusert netto handlingsfrihet etter kvalitets- og risikoverdi'),
('Energiomstilling og inntekt','Internasjonal etterspørselsendring trekker petroleumsinntekter under referansebanen','Etterspørsel, teknologi, energisikkerhet og pris gir motløp','Produksjon, ressurser, kostnader, olje- og gasspris','K142 K137','Sammenlign scenariofamilier mot observerte og historiske anslag','Netto kontantstrøm holder seg vedvarende på eller over referansebanen'),
('Produktivitetsreform mot uttaksnorm','Styrket fastlandsproduktivitet har større varig nettoeffekt enn moderate regelendringer i SPU-uttak','Kortsiktig velferd og risiko kan tilsi annerledes portefølje','Produktivitet, skattebase, uttaksregel, dissontering, investeringsnivå','K145 K137 K03','Flersektor-modell med varige skattebaser og følsomhet','Fondsregel alene har større robuste netto gevinster gitt like kostnader og risiko'),
('Intergenerasjonell rettferdighet','Dagens fondsbruk gir asymmetrisk fordeling av nasjonalformue og forpliktelser','Dagens tjenestefinansiering og offentlige investeringer gir også fremtidige goder','Offentlig nettoformue, skatt, utdanning, pensjon og fødselskull','K150 K137 K143','Generasjonsregnskap 04/09 med både transfereringer og kapitaltjenester','Netto nåverdi av offentlige fordelinger viser ikke systematisk senere generasjonstap'),
('Fondsillusion i beslutninger','Høy SPU-verdi kan føre til systematisk overvurdering av varig finansiering','Transparens, fondsstyring og makroekspertise motvirker feilen','Forventninger, underskuddsbegrep, beslutninger og medietekster','K137 K145','Forhåndsregistrert survey og tekstanalyse over tid','Ingen systematisk feiltolkning ved randomisert informasjonsdesign'),
]
hypotheses=[]
for i,(title,hyp,mot,vars,kilder,test,fals) in enumerate(hyp_defs,1):
    hypotheses.append({'id':f'H08-{i:02}','tittel':title,'hypotese':hyp,'mothypotese':mot,'variabler':vars,'primarkilder':kilder,'forskningslitteratur':kilder,'empirisk_test':test,'falsifikasjonskriterium':fals,'resultat':'Ikke selvstendig kausalt estimert i denne delrapporten','evidensklasse':'U','tillit':'Uavklart: kilde-/modellgrunnlag etablert','status':'Forskningsdesign registrert; kausal test gjenstår','traad':'08'})
assert len(hypotheses)==14
write_pair('hypoteseregister_08',hypotheses)

scenarios=[];scenario_summaries=[]
for s in SCENARIOER:
    full=beregn_bane(s)
    scenarios.extend(full)
    by={x['aar']:x for x in full}
    cross=next((row['aar'] for row in full if row['uttak_prosent_av_inngangsfond'] is not None and row['uttak_prosent_av_inngangsfond']>3),None)
    zero=next((row['aar'] for row in full if row['fond_ved_inngang_mrd']==0),None)
    scenario_summaries.append({'scenario':s.navn,'realavkastning_prosent':100*s.realavkastning,'vekst_i_kontantuttak_prosent':100*s.uttaksvekst,'nedgang_petroleum_prosent':100*s.petroleumsfall,'initialt_fall_i_fond_prosent':100*s.startfall,'fond_etter_2050_mrd':by[2050]['fond_ved_utgang_mrd'],'fond_etter_2060_mrd':by[2060]['fond_ved_utgang_mrd'],'fond_etter_2070_mrd':by[2070]['fond_ved_utgang_mrd'],'fond_etter_2100_mrd':by[2100]['fond_ved_utgang_mrd'],'forste_aar_uttak_over_3_prosent':cross,'forste_aar_teknisk_nullsaldo':zero,'type':'D — matematisk scenario, ikke prognose'})
write_pair('scenarier_08',scenarios)
write_pair('scenarieoppsummering_08',scenario_summaries)

# Evidensposter er klassifisert slik at utestede påstander ikke fremstår som observerte funn.
claims=[
 ('Budsjettforslag 2027 strukturelt underskudd','608,4 mrd. kr; 12,6 % trend-Fastlands-BNP','K137','A','Avrundet og konjunkturjustert; ikke kontantoverføring'),
 ('Andel statsbudsjettets utgifter','26,6 % i 2027-budsjettforslag','K137','A','Nevner er statsbudsjettets utgifter; ikke offentlig forvaltning samlet'),
 ('Uttaksandel fondskapital','2,7 % av anslått kapital ved 2027-inngangen','K138','A','Beregningsteknisk nevner, ikke faktisk markedsobservasjon'),
 ('2027 petroleum netto','568,4 mrd. kr forventet','K142','A','Budsjettanslag, sensitivt for energi-/valutapris'),
 ('Faktisk kontantunderskudd 2027','561,7 mrd. kr anslått','K139','A','Budsjettvedtak kan endres, ikke lik strukturelt mål'),
 ('Strukturelt versus kontant 2026','583,4 mot 454,8 mrd. kr','K137','A','Skattetrekkskonto gir spesielt tidsforskjøvet skatteinnbetaling'),
 ('Fondsverdi 30.06.2026','22 683 mrd. kr','K140','A','Halvårsregnskap; 2026 ikke fullført'),
 ('Fondsverdi 31.12.2025','21 268 mrd. kr','K141','A','Regnskapsverdi, ikke oppsummert kjøpekraft'),
 ('Fondsavkastning 2025','15,11 % i valutakurv','K141','A','Historisk nominell avkastning, ikke real forventning'),
 ('Fondsavkastning første halvår 2026','9,44 % i valutakurv','K140','A','Halvårsobservasjon, ikke helår'),
 ('Valutaeffekt fond 2025','−1 155 mrd. kr i NOK-verdi','K141','A','Verdsettelseseffekt, ikke tap i internasjonal valutakurv'),
 ('Valutaeffekt fond H1 2026','−427 mrd. kr i NOK-verdi','K140','A','Verdsettelseseffekt'),
 ('Historisk realavkastning 1998–2025','4,34 % annualisert netto','K141','A','Historisk, ikke fremover garantert'),
 ('Forventet realavkastning handlingsregel','3 % etter omlegging fra 4 %','K144','A','Rettesnor, ikke sikker årlig betaling'),
 ('Fond-/Fastlands-BNP i 2029','4,9 ganger i betinget framskriving','K137','D','Projeksjon, ikke observert'),
 ('Fond-/Fastlands-BNP i 2060','4,5 ganger i betinget framskriving','K137','D','Projeksjon, ikke observert'),
 ('Inndekningsbehov 2060 i PM24','6,2 % av Fastlands-BNP','K143','D','Betinget scenario fra 2024-vintage'),
 ('Inndekningsbehov 2060 i NB26','5,9 % av Fastlands-BNP','K125','D','Betinget scenario fra 2025-vintage'),
 ('Inndekningsbehov 2060 i NB27','5,8 % av Fastlands-BNP','K137','D','Betinget scenario fra 2026-vintage'),
 ('Endret statsutgiftsandel 2027–2060','+3,6 prosentpoeng Fastlands-BNP','K137','D','Betinget statlig beregning'),
 ('Endret offentlig inntektsandel 2027–2060','−2,2 prosentpoeng Fastlands-BNP','K137','D','Betinget statlig beregning'),
 ('SPU-historikk budsjett','2001 ca. 2 % trend-Fastlands-BNP, 2027 12,6 %','K137','A','Sammenligning av budgettindikator over 26 år, ikke kausal analyse'),
 ('SPU stresseksempel verdifall','20–37 % hypotetiske scenarier fra NBIM','K146','D','Ingen sannsynlighetsvurdering'),
 ('Oljeprisfølsomhet','10 kr høyere oljepris gir 11,8 mrd. mer i 2027–2028 samlet','K137','D','Gassprisen forutsettes å endres tilsvarende prosentvis'),
 ('Scenario A modellfond 2060','37 500,84 mrd. kr ved utgangen av 2060 i faste modellkroner','K138','D','Forenklet egen modell, ikke offisiell prognose'),
 ('Scenario B modellfond 2060','13 009,89 mrd. kr ved utgangen av 2060 i faste modellkroner','K138','D','Forenklet egen modell, ikke offisiell prognose'),
 ('Scenario D porteføljesjokk','25 % initialt tap, øvrige antakelser holdt uendret','K146','D','Hypotetisk ikke-lineær risikomodell uten politikkrespons'),
 ('Fondets størrelse utsetter skattereform','Uavklart kausal mekanisme','K145','U','Ingen kausal estimat i denne rapporten'),
 ('Oljefondet svekker generasjonsmobilitet','Uavklart total nettovirkning','K150','U','Krever kohortregnskap og kontrafaktiske analyser'),
 ('Oljefondet gjør offentlige utgifter varig finansierbare','Ikke dokumentert som ubegrenset finansiering','K137','U','Utgift og inntekt må modelleres samlet'),
 ('Hollandsk syke forklarer industrisvakhet','Konkurrerende årsaksforklaringer','K149','U','Sektorpanelet og identifikasjon gjenstår'),
 ('Prisdrevet petroleumssjokk og realfond','Ikke identifisert norsk årsakseffekt på sektornivå','K142','U','Eksport, priser og reell valutakurs må identifiseres'),
]
assert len(claims)==32
evidence=[]
for i,(title,result,source,cls,limit) in enumerate(claims,1):
    hypothesis=f'H08-{min(i,14):02}'
    evidence.append({'id':f'E08-{i:03}','tittel':title,'traad':'08','utsagn':result,'evidensklasse':cls,'status':('Kildebelagt budsjett/portefølje' if cls=='A' else 'Betinget modellscenario, ikke prognose' if cls=='D' else 'Kausalt uavklart'),'tillit':'Høy for korrekt transkripsjon, ingen kausal slutning' if cls=='A' else 'Avhenger av forutsetninger; ikke estimert sannsynlighet' if cls=='D' else 'Uavklart','primaerkilde':source,'kilde_id':source,'hypotese':hypothesis,'resultat':result,'mothypotese':'Alternative regnskapsdefinisjoner, risikofordeling og realøkonomisk tilpasning','variabler':'Fondsverdi; petroleum; uttak; skattebase; befolkning; avkastning','empirisk_test':'Se hypoteseregister 08; bare tilgjengelige aggregerte kilder og modell er gjennomført','falsifikasjonskriterium':'Utled påstanden mot original definisjon eller konstruer validert kontrafaktisk design','datavintage':STAMP,'begrensninger':limit,'epistemisk_rolle':'Beskrivelse eller modell; ingen egen kausalestimering','ansvar':'Norsk Økonomi, forskningstråd 08','registrert':STAMP,'forskningslitteratur':'K145 K149 K150','kildereferanser_kontrollert':source})
write_pair('evidensregister_08',evidence)

provenance={
 'traad':'08','utgave':VERSION,'datagrense':STAMP,
 'kildeoversikt':[{'id':f'K{n}','referanse':t,'url':t.split('https://')[-1] if False else t[t.index('https://'):]} for n,_,t in SOURCES],
 'observasjonsstatus':'Budsjettforslag 2027. 2025–2026 oppdatert 2027-vintage. Historiske SPU-tall fra NBIM 2025. Kontantunderskudd 2026 påvirket av innbetalingstidspunkt.',
 'dataklasser':{'A':'offentlig beskrivende statistikk og regnskap','B':'statistisk assosiasjon','C':'kausal identifikasjon – ingen nye C i denne delrapporten','D':'betinget modell eller offentlig framskriving','U':'uavklart'},
 'egne_modeller':'Uten empirisk usikkerhetsfordeling; konstant realavkastning, reell uttaksvekst og avtagende petroleum i modellkroner; ingen politikk- eller skattefeedback.',
 'startfond_2027_mrd':STARTFOND,'petroleum_2027_mrd':STARTPETROLEUM,'faktisk_fondsuttak_2027_mrd':STARTUTTAK,
 'strukturelt_underskudd_2027_mrd':608.4,
 'scenario_etterprovbarhet':'kildekode/modell_08.py, data/scenarier_08.json, data/scenarier_08.csv',
 'kildekart':{'fondsbruk_08':'K137','petroleum_08':'K142','regnskapsbegreper_08':'K137 K139 K151','fondsverdi_08':'K141 K140 K06','uttaksprosent_historikk_08':'K147 K137','hovedindikatorer_08':'K137 K140 K141 K143 K146'},
 'modellbegrensninger':['r er konstant realavkastning; ikke prognose','Deler av petroleumscashflow er nominell budsjettvintage, i scenariet holdes første år realt konstant','Uttak er faktisk kontantunderskudd og ikke strukturelt underskudd','Ingen valutakurs, statsbudsjett, skatter, demografi eller investeringsvirkninger','Ingen etisk/personvernrisiko fra aggregerte kilder'],
 'KI_erklæring':'KI brukt til kildesøk, organisering, tekstutkast, programmering og beregningskontroll; ingen KI-systemer er empirisk kilde.'
}
(D/'proveniens_08.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Forskning 08: kilder',len(SOURCES),'hypoteser',len(hypotheses),'evidens',len(evidence),'scenarioår',len(scenarios),'observerte faktabaser',sum(map(len,[budget,pet,fiscal_cash,fund,withdraw,ind])))
