# Norsk Økonomi — Forskningspublikasjon og kildedokumentasjon

**Publisert utgave:** 1.1.0, 13. oktober 2026. **Språk:** Norsk bokmål.  
**Vitenskapelig status:** Første deskriptive, kildedokumenterte forskningsutgaver av delrapport 01–09. Ikke ekstern fagfellevurdering; ikke ferdig generasjonspanel for 1945–2005.  
**Formål:** Åpen, revisjonsbar forskningspublikasjon om Norges økonomi, med skille mellom observasjon, statistisk samvariasjon, kausal dokumentasjon, modellscenario og uavklarte hypoteser.

## Publiser som statisk nettside

1. Pakk ut ZIP-pakken i en mappe.
2. Last opp **hele** mappens innhold, inkludert `index.html` og `data/`, til webserverens dokumentrot, typisk `public_html` eller `www`.
3. Nettstedet fungerer uten database, API-nøkler eller serverkode; vanlige HTTP(S)-webhotell, Nginx, Apache, GitHub Pages eller tilsvarende statisk hosting er tilstrekkelig.
4. Den separate HTML-filen `Norsk_Okonomi_Interaktiv_2026-10-13_v1.1.0.html` er selvstendig og kan åpnes alene, men CSV-, JSON- og Markdown-lenkene på nettsiden virker bare dersom resten av pakkens filer følger med.
5. Ved utgivelse på et offentlig nettsted: legg inn en offentlig kontaktadresse og oppdater publikasjonens metadata/versjon ved endringer. Ikke erstatt eldre filer uten endringslogg.

## Innhold

- `index.html` — full rapporttekst med dokumenterte kilder; responsivt, interaktivt datapanel og søkbart hypoteseregister.
- `Norsk_Okonomi_Forskningsrapport_2026-10-13_v1.1.0.md` — **kanonisk rapport**, inkluderer del 01–09.
- `01_Forskningsarkitektur_metode_evidens_v0.3.0.md` — metode, påstandskontroll og evidensarkitektur.
- `02_Norges_relative_okonomiske_utvikling_v0.4.1.md` — relativ norsk verdiskaping og nordisk/europeisk sammenligning.
- `03_Bolig_kreditt_eiendomsformue_kapitalallokering_v0.5.0.md` — bolig, bankfinansiering, formue og kreditt.
- `04_Generasjonsokonomi_mobilitet_fordeling_v0.6.0.md` — generasjonsøkonomi, bolig, formue, foreldrehjelp, arbeid, levekostnader og fertilitet.
- `05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md` — nyetablering, vekstbedrifter, tidligfasekapital, innovasjon, FoU og unges arbeid, med 12 hypoteser og 30 evidensposter.
- `06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md` — 2026-skatteregler, personflytting, latent gevinst, eierlikviditet, internasjonale kausalstudier, alternative reformer og 12 hypoteser / 34 evidensposter.
- `07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md` — nasjonalregnskapet 2021–2025, COFOG-formål, offentlig jobbandel, NTP, offentlige anskaffelser, tjenestekvalitet og teori om Baumols kostnadssykdom. 14 hypoteser og 40 evidensposter. Ingen kausal originalstudie er hevdet.
- `09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md` — befolkningsframskrivinger MMM/LLL/HHH 2026–2100, regionale fylkesdata MMMM 2026–2050, fruktbarhet, husholdninger, boligmasse, dødsfall, aldring, helsepersonell og omsorg, med 14 hypoteser og 40 evidensposter. Nasjonal/regional modellforskjell er dokumentert.
- `data/befolkningsbaner_09.*`, `data/fylker_09.*`, `data/husholdningstyper_09.*`, `data/dodsfall_09.*`, `data/eldre80_09.*` — daterte SSB-data og betingede alternativer med kildekoder og tidsstatus.
- `data/hypoteseregister_09.*`, `data/evidensregister_09.*`, `data/proveniens_09.json` — register og metodeerklæring for demografistudien.
- `08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md` — petroleumsinnskudd, faktisk og strukturelt oljekorrigert underskudd, SPU-kapital, 3 %-regel, inndekningsbehov 2060, risiko og seks scenarioer til 2100; 14 hypoteser og 32 evidensposter.
- `data/fondsbruk_08.*`, `data/fondsverdi_08.*`, `data/uttaksprosent_historikk_08.*` — separate budsjetttall, markedsverdi og uttaksserier med dato og kilde. 2027 tall er forslag, og 2026-H1 ikke helt kalenderår.
- `data/petroleum_08.*`, `data/regnskapsbegreper_08.*`, `data/hovedindikatorer_08.*` — komponenter i petroleumskontantstrøm, definisjoner og primærkildedata.
- `data/scenarier_08.*`, `data/scenarieoppsummering_08.*` — seks deterministiske fremtidsbaner. Dette er modellgenererte data, ikke nasjonale observerte tidsserier, og inngår ikke i observasjonstellingen.
- `data/hypoteseregister_08.*`, `data/evidensregister_08.*`, `data/proveniens_08.json` — kildebundet forskningslogg for delrapport 08.
- `kildekode/modell_08.py`, `lag_08.py`, `integrer_08.py`, `oppdater_web_08.py` — modell, transkripsjon, rapportintegrasjon og nettsidebygger for utgave 1.0.0.
- `data/offentlige_hovedtall_07.*` — SSB offentlige inntekter, utgifter, nettoinvesteringer, årsregnskap i millioner løpende kroner.
- `data/cofog_utgifter_07.*` — 10 formålskategorier for 2021–2025; COFOG «Alminnelig offentlig tjenesteyting» er IKKE administrative kostnader isolert.
- `data/sysselsetting_offentlig_07.*` — offentlig andel av jobbforhold/månedsverk 2016–2025; ikke antall personer eller årsverk.
- `data/hovedindikatorer_07.*` — definerte observasjoner om innkjøp, BNP-andel, sykefravær, helse, NTP og budsjettscenarioer.
- `data/hypoteseregister_07.*`, `data/evidensregister_07.*`, `data/proveniens_07.json` — hypoteser, motforklaringer og maskinlesbart kildegrunnlag.
- `data/utflyttere_formuende_06.*`, `data/utflyttingsskatt_latent_06.*` — **forskjellige populasjoner** i NOU 2026: 9; latente gevinster er ikke verdier overført fra Norge.
- `data/formueskatt_sats_06.*` — vedtatte 2026-satser og formelle verdsettingsrabatter, før gjeld, bunnfradrag og særegne skattemessige verdier.
- `data/skattekommisjon_scenario_06.*` — statiske beregninger for forslag i NOU 2026: 9; **ikke lovfestede satser eller prognoser for investeringsvirkning**.
- `data/forskningsestimater_06.*` — ulike virkningsestimater fra ulike studiedesign. De kan ikke legges sammen.
- `data/hypoteseregister_06.*`, `data/evidensregister_06.*`, `data/proveniens_06.json` — etterprøvbare vurderinger og datakilde for tråd 06.
- `data/foretak_kvartal_05.*` — SSBs kvartalsregistreringer 2024–2026; 2026 med statistisk metodeendring.
- `data/venture_norden_05.*` — bransjeanslag 2025 for Norge, Danmark og Sverige; ikke BNP-justert eller fullstendig VC-univers.
- `data/lovende_startups_05.*` — SSBs **avrundede** oppstartsforløp for et selektert utvalg; ikke nasjonal scaleup-rate.
- `data/etablerere_alder_05.*`, `data/etablerere_kjonn_05.*` — foreløpige statistiske anslag om personlige etablerere.
- `data/ungdomsarbeid_05.*`, `data/nyutdannede_05.*` — AKU-verdier; NEET er en annen nevner.
- `data/hypoteseregister_05.*`, `data/evidensregister_05.*`, `data/proveniens_05.json` — reproduserbar kontroll av tråd 05.
- `data/kilder.json` — faglige referanser, kildenøkler og erklæring om KI som arbeidsverktøy.
- `data/observasjoner.csv` — 845 kildemerkede indikatorverdier fra alle ni delrapporter: historiske observasjoner, budsjettanslag, offisielle fremskrivinger og enkelte eksterne stresstestverdier (merket D) med synlig status. 444 egenmodellerte 08-scenarioverdier holdes utenfor dette registeret.
- `data/boligeierskap_alder_04.*` — SSB-tverrsnitt (2014/2023), *ikke* fulgt fødselskull.
- `data/foreldreformue_bolig_04.*` — SSB fødselskull 1988–1993, registrert boligformue innen gitt alder etter foreldres formuesgruppe. **Øvre gruppe er 99.–100. formuespersentil, altså de øverste to prosentene.**
- `data/boutgiftsbelastning_04.*` — SSB EU-SILC aldersgrupper og publiserte observasjonsår; manglende år fylles ikke kunstig ut.
- `data/hovedindikatorer_04.*` — utvalgte SSB/Finanstilsynet-indikatorer.
- `data/kohortdekning_04.*` — når kull 1945–2005 fyller 25/30/35/40; **bare kalenderår**, ikke inntektsdata eller prognoser.
- `data/hypoteseregister_04.*` — 12 hypoteser med motforklaringer og falsifikasjonskriterier.
- `data/evidensregister_04.*` — 25 evidensposter med kilde, evidensklasse og forskningsstatus.
- `data/proveniens_04.json` — transkripsjons- og tolkningsmetadata.
- `kildekode/bygg_publisering.py`, `kildekode/mal_nettside.html` — reproduserbart nettsted bygget fra rapporttekst og data.
- `opprett_data_04.py`, `opprett_registre_04.py`, `opprett_data_05.py` og `opprett_registre_05.py` — transkripsjons- og registerskript.
- `integrer_05.py`, `oppdater_web_05.py`, `integrer_06.py`, `oppdater_web_06.py` — sporbare utviklingstrinn gjennom v0.8.0; `lag_07.py` og `oppdater_web_07.py` dokumenterer transkripsjoner, analyse og nettstedstillegg til v0.9.0.
- `opprett_data_06.py` og `opprett_registre_06.py` — maskinlesbare datasett/registre for forskningstråd 06.
- `MANIFEST-SHA256.txt` — kontrollsummer for alle publiserte filer.

`*.csv` er semikolondelt og UTF-8 kodet. Prosjektet legger ikke ved SSBs fortrolige mikrodata; tabellene er manuelle transkripsjoner av publiserte aggregater og må krysskontrolleres mot originalkilden ved revisjon.

## Rekonstruer nettsiden

Med Python 3.11+ og `markdown-it-py` og `beautifulsoup4` installert:

```bash
python kildekode/bygg_publisering.py
```

Kjør kommandoen fra utpakket publiseringsmappe. Byggeskriptet leser den kanoniske Markdown-rapporten og datasett i `data/`, oppdaterer `index.html` og eksporterer frittstående HTML/MD-filer til overordnet mappe. Datasett kan regenereres med `python opprett_data_06.py` og `python opprett_registre_06.py` (for tråd 06), eller tilsvarende for 05 eller tilsvarende 04-skript, men **ikke** regenerer etter at du har endret manuelt uten å kontrollere mot kilden; scriptet skriver over vedlagte transkripsjoner.

## Forskningsprinsipper og begrensninger

- **A:** Beskrivende dokumentasjon/observasjon. **B:** Statistisk sammenheng. **C:** Forskning med kausalt identifikasjonsdesign og eksplisitte forutsetninger. **D:** Betinget modellscenario, ikke «bevisstyrke D». **U:** Uavklart eller utilstrekkelig dokumentert.
- 2014 og 2023 i SSBs boligeiertverrsnitt representerer ulike populasjoner. SSBs fødselskullanalyse fra 1988–1993 måler personer som har vært registrert med boligformue innen en gitt alder. Disse **kan ikke** ukritisk kombineres.
- Aldersgrupper 25–44 og 67+ i EU-SILC er *ikke* kohorter ved samme alder. En ren sammenligning av disse beviser ikke at én generasjon er dårligere stilt historisk.
- Reglene i den interaktive låneillustrasjonen (90 prosent belåningsgrad, fem ganger inntekt) gir ingen kredittbeslutning. Stresstest, dokumentavgift, formuesrisiko og bankens skjønn er utelatt.
- Generasjonskontoer 1945–2005 ved alder 25/30/35/40 er et **forskningsmål**, ikke et ferdig estimat. Manglende historiske observasjoner skal ikke erstattes av forutsetninger uten tydelig merking.
- Alle publiserte faglige påstander må knyttes til originale referanser, og revisjoner av SSB-/Norges Bank-/OECD-statistikk skal registreres som nye datavintager.
- Flere former for KI har vært brukt til kildeorganisering, språkutvikling, dataassistanse, analyse og nettsidekode. KI er **ikke** en empirisk kilde. Detaljer står i hovedrapportens metodeerklæring og `data/kilder.json`.

## Særlige feiltolkninger i forskningstråd 05

- Kvartalsvise foretaksregistreringer er ikke netto jobbskaping eller overlevelse. Metodeendring fra 2026 gjør direkte sammenligninger mindre robuste.
- Vekst- og scaleup-andelene etter 3/6/9 år gjelder et selektert utvalg SSB-definerte «lovende startups», ikke alle norske foretak. Andel scaleup **inngår i** vekstandelen og må ikke summeres med den.
- Andel unge ledige i AKU (15–24) har arbeidsstyrken som nevner; NEET-registeret omfatter personer 15–29 og måler utenforskap fra både jobb og utdanning.
- NVCA/Menon er bransjestatistikk. Det er ingen identifisert kausal sammenheng fra kapitaltilførsel, skattenivå eller utdanningsresultat til antallet arbeidsplasser i denne utgaven.

## Særlige feiltolkninger i forskningstråd 06

- De 141 registrerte utflytterne 2021–2025 gjelder et *særskilt utvalg* på 3 565 personer i en NOU-tabell, ikke alle rike, og gir ingen kausal skatteandel.
- Fastsatt latent gevinst i en utflyttingsskattesak er ikke den samme som faktisk kapital ut av landet, skatt innbetalt eller aktivitet som slutter å finne sted i Norge.
- Skattekommisjonens foreslåtte formuesskattesatser og tilhørende statiske provenyendringer er **forslag**, ikke vedtatt gjeldende rett.
- Å kombinere formuesskatt, selskapsbeskatning og utbytteskatt i én illustrasjon krever eksplisitte antakelser om eierforhold, skjerming, skattemessig verdi, gjeld, likviditet og om midlene allerede er skattlagt i selskapet.
- Rings kortsiktige resultater, Jakobsen og medforfatteres nordiske estimater og Blandhols modellframskrivinger er *ikke* estimater av ett og samme utfall. Ulike resultater er beholdt separat.

## Særlige feiltolkninger i forskningstråd 07

- Samlede offentlige utgifter på 2 684,6 milliarder kroner i 2025 er ikke et anslag på «offentlig sløsing» eller offentlig administrasjon. Omtrent 1 049 milliarder er sosial beskyttelse (COFOG), som i stor grad er overføringer.
- Forsvarsformålets vekst i 2025 var stor og inkluderte militær støtte til Ukraina. Dette forklarer en vesentlig del av regnskapsveksten og må skilles fra løpende administrasjon.
- Offentlige anskaffelser på om lag 864 mrd. kroner i 2025 overlapper allerede COFOG- og utgiftstallene; de kan ikke legges til som en ekstra offentlig utgift.
- Jobbandel offentlig forvaltning var 33,5 % i 2025-K2 mot 34,2 % i 2016-K2. Jobbforhold, utførte månedsverk og personer er ulike nevnere.
- Baumols mekanisme om høyere relative enhetskostnader i arbeidsintensive tjenester er teori; den interaktive kalkulatoren er en **stylisert sensitivitetsmodell** og ikke estimert norsk årsakssammenheng.
- BNP-nevner og datavintage: OECDs tidligere beregning for 2024 (49,6 %) er ikke identisk med SSBs reviderte 2026-vintage for 2024 (47,0 %). Tidsserie- og landstudier må harmoniseres før inferens.
- Netto prissatt nytte i NTP er et forhåndsanslag for valgte prosjekter; ikke-prissatte verdier, prosjektutvalg og realiserte utfall må håndteres før evaluering.
- Riksrevisjonens revisjonsresultater dokumenterer konkrete styringsproblemer, men gjør ikke om utgiftsregnskapet til et kvantifisert «sparepotensial».

## Særlige feiltolkninger i forskningstråd 08

- **608,4 mrd. kroner i 2027** er budsjettforslagets *strukturelle* oljekorrigerte underskudd, ikke faktisk planlagt overføring. **561,7 mrd. kroner** er budsjettert kontantunderskudd, og **568,4 mrd. kroner** er netto petroleumskontantstrøm til fondet. Ikke summer tallene som utgifter.
- Fondsverdi **22 683 mrd.** 30. juni 2026 er en observert halvårsverdi; **22 400 mrd.** ved inngangen til 2027 er et beregningsteknisk anslag i statsbudsjettet.
- Finansdepartementets langsiktige inndekningsbehov **5,8 % av Fastlands-BNP i 2060** er en betinget framskriving fra Nasjonalbudsjettet 2027, ikke en konkursprognose.
- De seks scenarioene 2027–2100 er **matematiske sensitivitetsregnestykker**. De bruker kontantuttak, petroleumstilførsel og tenkt realavkastning, men ikke fullstendig økonomi-/budsjettmodell, valutaprosess eller sannsynlighetsfordelinger. Ingen fremtidsbane er rangert som sannsynlig.
- En fondsverdi som vokser i milliarder modellkroner gir ikke automatisk finanspolitisk bærekraft. Utgiftspress, arbeidsmarked, skattebase, tjenestekvalitet og aldersstruktur analyseres i andre forskningstråder.

## Kildekritikk og forskningsstatus

Denne publikasjonen er **ikke** et dokumentert, nasjonalt registerpanel som sammenligner alle norske fødselskull fra 1945 til 2005 ved samme alder, og inneholder ikke nye kausalt identifiserte estimater om generasjonseffekter. Videre arbeid forutsetter forskeradgang til registerdata eller ytterligere harmoniserte historiske aggregerte kilder. Det skal etableres en særskilt, ekstern kvalitetssikring før forskningsprogrammet omtales som avsluttet.

**Opphavsrett:** Refererte databaser og publikasjoner tilhører opprinnelige rettighetshavere. Ikke anta at denne publiseringspakken gir rett til å republisere rådata som ikke er lagt ved. Nettsiden bruker ingen tredjepartssporing eller fjernstyrt annonse-/analysebibliotek.

## Kvalitetsavgrensning for delrapport 09

SSBs nasjonale BEFINN (MMM) gir 6 214 071 innbyggere i 2050, mens regional BEFREG (MMMM) summerer til 6 195 859. Forskjellen 18 212 skyldes ulike demografiske modeller og er dokumentert av SSB; ingen fylkesjustering er gjort. Husholdnings- og omsorgsregneeksemplene er deterministiske illustrasjoner uten kalibrert atferdsrespons. Fødsler og dødsfall er ikke lik boligtransaksjoner; publiserte mikrodata er ikke brukt.
