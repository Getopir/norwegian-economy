# Norsk Økonomi 2026

En forskningspakke om norsk økonomi, langsiktig bærekraft, kapitalallokering og generasjonsmuligheter. Materialet samler tolv delrapporter, en samlet rapport, datagrunnlag, kilde- og evidensregistre, analysekode og HTML-utgaver.

Det overordnede spørsmålet er hvordan Norge bruker den økonomiske handlefriheten fra petroleum til å bygge varig produktivitet og bred økonomisk deltakelse. Rapportene undersøker både utfordringer, motfunn og alternative forklaringer.

**Utgave:** Integrert forskningsutgave 2.0, datert 13. oktober 2026.  
**Status:** Forskningsutkast. Materialet er ikke eksternt fagfellevurdert, og full uavhengig replikasjon av data og analyser gjenstår.

## Start her

- Les [den samlede forskningsrapporten](Norsk_Okonomi_Samlet_Forskningsrapport_2026_v2.md) for helheten. Del I gjengir forskningsgrunnlaget for 01–09; del II samler tilleggene 10–12.
- Åpne [nettsiden](nettside/index.html) lokalt i en nettleser for en HTML-utgave med søk og utskrift.
- Les [vitenskapelig kvalitetssikring](VITENSKAPELIG_KVALITETSSIKRING.md) for kontrollstatus, metodebegrensninger og gjenstående forskningsoppgaver.
- Bruk [grunnmaterialet](grunnmateriale_01-09/) når du vil følge tall, kilder og beregninger tilbake til delrapportene.

## Innhold og mappestruktur

```text
.
├── README.md
├── LES_MEG.md
├── Norsk_Okonomi_Samlet_Forskningsrapport_2026_v2.md
├── VITENSKAPELIG_KVALITETSSIKRING.md
├── MANIFEST_SHA256.json
├── nettside/
│   └── index.html
├── grunnmateriale_01-09/
│   ├── delrapporter og historiske rapportversjoner
│   ├── data/          # CSV, JSON, kilder, evidens og proveniens
│   ├── kildekode/     # Publiseringskode, HTML-mal og fondsmodell
│   └── øvrige skript og tidligere HTML-utgave
├── delrapporter_10-12/
│   └── delrapporter i Markdown og HTML
└── arkiv/             # Tidligere innhold fra GitHub-repoet
```

[LES_MEG.md](LES_MEG.md) er den korte veiledningen fra forskningspakken. [arkiv/](arkiv/) bevarer de fire filene som lå i repoet før den samlede pakken ble lastet opp: en tidligere rapport, interaktiv HTML, publiserings-ZIP og README.

## De tolv delrapportene

1. [Forskningsarkitektur, metode og evidens](grunnmateriale_01-09/01_Forskningsarkitektur_metode_evidens_v0.3.0.md)
2. [Norges relative økonomiske utvikling](grunnmateriale_01-09/02_Norges_relative_okonomiske_utvikling_v0.4.1.md)
3. [Bolig, kreditt, eiendomsformue og kapitalallokering](grunnmateriale_01-09/03_Bolig_kreditt_eiendomsformue_kapitalallokering_v0.5.0.md)
4. [Generasjonsøkonomi, mobilitet og fordeling](grunnmateriale_01-09/04_Generasjonsokonomi_mobilitet_fordeling_v0.6.0.md)
5. [Entreprenørskap, skalering, innovasjon og arbeidsmarked](grunnmateriale_01-09/05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md)
6. [Skatt, eierskap, kapitalmobilitet og utflytting](grunnmateriale_01-09/06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md)
7. [Offentlig ressursbruk, effektivitet og Baumol-effekter](grunnmateriale_01-09/07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md)
8. [Petroleum, oljefondet og finanspolitisk bærekraft](grunnmateriale_01-09/08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md)
9. [Demografi, arbeidskraft, bolig og velferd mot 2050–2100](grunnmateriale_01-09/09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md)
10. [Systemdynamikk og motmodeller](delrapporter_10-12/delrapport_10_systemdynamikk_motmodeller.md), med [interaktiv HTML-utgave](delrapporter_10-12/delrapport_10_interaktiv.html)
11. [Politisk økonomi, ulikhetsmekanismer og institusjonelle insentiver](delrapporter_10-12/delrapport_11_politisk_okonomi_ulikhetsmekanismer.md)
12. [Radikale strukturreformer](delrapporter_10-12/delrapport_12_radikale_strukturreformer.md)

## Åpne nettsiden

Last ned repoet som ZIP og pakk det ut, eller klon det:

```sh
git clone https://github.com/Getopir/norwegian-economy.git
cd norwegian-economy
```

Åpne deretter `nettside/index.html` i nettleseren. Den ferdige siden bruker innebygd CSS og JavaScript og krever ingen installasjon, API-nøkkel eller database. Eksterne kildesider krever nettforbindelse.

GitHub viser HTML-filens kildekode når du følger lenken i repoet. For å lese siden som en nettside må du åpne den lokalt eller publisere den på en statisk webserver. Bevar mappestrukturen ved nedlasting og publisering.

## Data, kode og sporbarhet

[data/](grunnmateriale_01-09/data/) inneholder blant annet observasjoner, kildehenvisninger, evidensregistre, hypoteseregistre, proveniens og scenarioforutsetninger i CSV og JSON. Kildematerialet viser til blant andre SSB, OECD, Norges Bank, Finansdepartementet, NBIM og Riksrevisjonen.

Kontrollrapporten oppgir 276 evidensposter for spor 01–09, med unike ID-er innen hvert spor og utfylte primærkildefelt. Dette dokumenterer registerstruktur; det bekrefter ikke alene at kildene støtter alle påstander eller at tall og årsaksforklaringer er riktige. Evidensregistrene for 10–12 er foreløpig ikke harmonisert med CSV-skjemaene for 01–09. CSV-separatoren varierer: evidensregister 06 bruker komma, mens de øvrige evidensregistrene bruker semikolon.

[kildekode/](grunnmateriale_01-09/kildekode/) inneholder blant annet:

- `modell_08.py`: en deterministisk fondstresstest med eksplisitte forutsetninger. Scenarioene har ingen estimert sannsynlighetsfordeling.
- `bygg_publisering.py` og `mal_nettside.html`: publiseringskode for den tidligere rapportutgaven 1.1.0 i grunnmaterialet. Skriptet oppgir avhengighetene `markdown-it-py` og `beautifulsoup4`; det er ikke en dokumentert bygger for den samlede utgaven 2.0.

Flere av de øvrige skriptene oppretter eller endrer data og rapportfiler. Les filstier og forutsetninger før kjøring, og bruk en separat arbeidskopi ved replikasjon.

[MANIFEST_SHA256.json](MANIFEST_SHA256.json) registrerer filstørrelser og SHA-256 for den opprinnelige forskningspakken. Manifestet omfatter ikke denne nye README-en, arkivmappen eller manifestfilen selv. Hashkontroll viser om filinnhold er bevart; den er ikke en faglig validering.

## Hvordan resultatene skal leses

Materialet skiller mellom fire dokumentasjonstyper:

- **A:** beskrivende statistikk, regnskapsinformasjon og tydelig merkede framskrivinger.
- **B:** statistisk samvariasjon eller sammenlikning.
- **C:** identifikasjonsbaserte kausale estimater, med forutsetninger som må vurderes.
- **D:** simuleringer, mekanismemodeller og betingede scenarioer.

D er en annen type dokumentasjon enn C, ikke et høyere evidensnivå. Reformforslagene skal leses som testbare forslag. Framskrivinger og scenarioer er betingede utfall, og observerte sammenhenger etablerer ikke alene årsak og virkning.

Vesentlige åpne oppgaver er harmonisering av år, prisnivå og definisjoner; replikasjon av tallserier og beregninger; et samlet evidensregister for 01–12; kausal analyse av sentrale mekanismer; sensitivitetsanalyser; og uavhengig metodegjennomgang og fagfellevurdering. Se [kvalitetssikringsdokumentet](VITENSKAPELIG_KVALITETSSIKRING.md) for prioriteringene.

## KI-bruk og faglig ansvar

Kvalitetsdokumentasjonen beskriver bruk av KI til organisering, sammenstilling, skriving, maskinell konsistenskontroll og pakking. Dette erstatter ikke uavhengig kontroll av primærkilder, kausalestimatene eller fagfellevurdering. Endelig faglig ansvar og godkjenning må ligge hos navngitte menneskelige forfattere eller fagkontrollører.

## Rettelser og videre arbeid

Ved feil eller forslag til forbedring, oppgi fil og avsnitt, hva som bør endres, og relevant primærkilde med år, enhet og definisjon. Skill mellom retting av observerte tall, metodekritikk og alternative hypoteser.

Det er foreløpig ingen egen lisensfil i repoet. Kontroller bruksrettigheter før videre distribusjon eller gjenbruk, også for underliggende kildemateriale.
