#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re,sys
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
import lag_08
src=(R/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.9.0.md').read_text('utf8')
delpath=R/'08_Petroleum_oljefondet_finanspolitisk_baerekraft_v1.0.0.md'
deltext=delpath.read_text('utf8')
assert src.count('## 18. Forskningstråd 07')==1 and src.count('## 12. Forskningstråd 01')==1
assert not (R/'Norsk_Okonomi_Forskningsrapport_2026-10-13_v1.0.0.md').exists()
# Publiceringsoversikt
src=src.replace('utgave: "0.9.0', 'utgave: "1.0.0',1).replace('dato: "2026-10-12"','dato: "2026-10-13"',1).replace('datagrense: "2026-10-12"','datagrense: "2026-10-13"',1)
src=src.replace('Forskningsutgave 0.9.0 | 12. oktober 2026', 'Forskningsutgave 1.0.0 | 13. oktober 2026',1)
src=src.replace('**Datagrense:** Offentlig tilgjengelige kilder identifisert og kontrollert frem til 12. oktober 2026.','**Datagrense:** Offentlig tilgjengelige kilder identifisert og kontrollert frem til 13. oktober 2026.',1)
insert='**Nytt i v1.0.0:** Forskningstråd 08 er lagt til med Nasjonalbudsjettet 2027, kontant-/strukturregnskap, SPU-rapporter og realavkastning, oppdatert 2060-inndekningsbehov på 5,8 % av Fastlands-BNP, en forenklet, reproduserbar fondsmodell, 14 hypoteser og 32 evidensposter. Eldre 2026-budsjettanslag fra andre kapitler beholdes som historiske datavintager og korrigeres i tråd 08. Kausale effekter av fondsbruk på reformvilje og produktivitet er ikke estimert.\n'
mark='**Arbeidsspråk og publiseringsspråk:**'
assert mark in src
src=src.replace(mark,insert+mark,1)
# Nytt 8. punkt på slutten av det eldre sammendraget
needle='**Foreløpig hovedkonklusjon:**'
intro='**8. Fondsfinansiering og statsfinansiell bærekraft (Nasjonalbudsjettet 2027):** Regjeringens forslag har strukturelt oljekorrigert underskudd på 608,4 mrd. kroner, 26,6 % av statsbudsjettets utgifter og 2,7 % av fondets anslåtte inngangsverdi. Oppdaterte langsiktige beregninger viser 5,8 % av Fastlands-BNP i forventet inndekningsbehov i 2060, tidligere 6,2 % i PM24. Faktisk kontantuttak er forskjellig fra strukturelt underskudd, og den fullstendige 2027-studien finnes i § 19. [K137](#k137) [K138](#k138)\n\n'
assert needle in src
src=src.replace(needle,intro+needle,1)
# Oppdatert forskningsstatus
find='## 7. Tolv forskningstråder og status'
assert find in src
# Oppdater eksplisitte tabellrader hvis mulige; behold ellers eksisterende oppsett.

# Legg kilder K137-151 til nederst i kilderegister, før delrapportenes kapitler
refblock='\n### 11.10 Petroleum, oljefondet og offentlig finansiering (K137–K151)\n\n'
for number,org,ref in lag_08.SOURCES:
    refblock+=f'<a id="k{number}"></a> **K{number} — {org}.** {ref}\n\n'
point='\n## 12. Forskningstråd 01'
assert point in src
src=src.replace(point,'\n'+refblock+point,1)

# Tabeller med egen forenklet modell utfylt på grunnlag av faktiske Python-funksjoner.
scenario_rows=[]
for s in lag_08.SCENARIOER:
    data=lag_08.beregn_bane(s)
    by={r['aar']:r for r in data}
    overskrid=next((str(r['aar']) for r in data if r['uttak_prosent_av_inngangsfond'] is not None and r['uttak_prosent_av_inngangsfond']>3), 'Ikke før 2100')
    nullaar=next((str(r['aar']) for r in data if r['fond_ved_inngang_mrd']<=0),'Ikke før 2100')
    val=lambda v:f'{v:,.0f}'.replace(',',' ')
    scenario_rows.append(f"| {s.navn} | {val(by[2050]['fond_ved_utgang_mrd'])} | {val(by[2060]['fond_ved_utgang_mrd'])} | {val(by[2100]['fond_ved_utgang_mrd'])} | {overskrid} | {nullaar} |")
table='''\n**Beregnet scenarioresultat – fondsverdi ved utgangen av året, mrd. 2027-modellkroner. Ikke sannsynlige prognoser.**\n\n| Scenario | 2050 | 2060 | 2100 | Første år kontantuttak over 3 % av inngangsfond | Første år fond ved inngang er null |\n|---|---:|---:|---:|---|---|\n'''+ '\n'.join(scenario_rows)+'''\n\nScenarioresultatene er beregnet uten politikkrespons. Hvis fondets saldo treffer teknisk null, blir planlagt uttak **ikke** finansierbart fra SPU uten andre tiltak. Årsbaner og kode ligger i ZIP-pakken.\n\n'''
needle='### 9.3 Stresstest mot 3 %-normen'
assert needle in deltext
# Standalone delrapport inkluderer datautsnittet, og kopieres deretter til master.
deltext=deltext.replace(needle,table+needle,1)
# Appendix kildeoversikt i standalone, ikke dupliserte ID-anker.
append='\n### 15.1 Kildeliste for selvstendig delrapport\n\n'
for number,org,ref in lag_08.SOURCES:
    append+=f'- **K{number}: {org}.** {ref}\n'
deltext=deltext.rstrip()+'\n'+append+'\n'
delpath.write_text(deltext,encoding='utf8')
# Reformatter selvstendig delrapport som ett hovedkapittel i kanonisk rapport.
core=deltext.split('\n---\n',1)[1].strip()
core=re.sub(r'\A# 08 — Petroleum, oljefondet og langsiktig finanspolitisk bærekraft\s*','',core,count=1)
core=re.sub(r'^### (\d+)\.(\d+)\s',lambda m:f'#### 19.{m.group(1)}.{m.group(2)} ',core,flags=re.M)
core=re.sub(r'^## (\d+)\.\s',lambda m:f'### 19.{m.group(1)} ',core,flags=re.M)
core=core.replace('### 19.15 Kildeliste', '### 19.15 Kildeliste')
core=re.sub(r'^### 15\.1 ', '#### 19.15.1 ',core,flags=re.M)
# Oppdater leservennlig forskningsstatus og legg helt nederst.
src+='\n\n## 19. Forskningstråd 08 — Petroleum, SPU og finanspolitisk bærekraft\n\n'+core+'\n'
name='Norsk_Okonomi_Forskningsrapport_2026-10-13_v1.0.0.md'
(R/name).write_text(src,encoding='utf8')
print('Kanonisk rapport',name,'ord',len(src.split()),'delrapport ord',len(deltext.split()),'modellscenarier',len(scenario_rows))
