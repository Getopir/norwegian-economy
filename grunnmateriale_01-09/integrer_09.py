#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
import re,json,sys
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R))
from lag_09 import SOURCES
src=(R/'Norsk_Okonomi_Forskningsrapport_2026-10-13_v1.0.0.md').read_text('utf8')
deltext=(R/'09_Demografi_arbeidskraft_bolig_velferd_2050_2100_v1.1.0.md').read_text('utf8')
assert src.count('## 19. Forskningstråd 08')==1
assert src.count('<a id="k151"></a>')==1
src=src.replace('utgave: "1.0.0', 'utgave: "1.1.0',1)
src=src.replace('Forskningsutgave 1.0.0 | 13. oktober 2026','Forskningsutgave 1.1.0 | 13. oktober 2026',1)
insert='**Nytt i v1.1.0:** Forskningstråd 09 om befolkning, aldring, arbeidskraft, husholdninger, boligmarked, omsorg og kommunal/statlig bærekraft: SSBs juni 2026-nasjonale MMM/LLL/HHH-framskrivinger og regionale MMMM-framskrivinger, 14 registrerte hypoteser, 40 evidensposter, 19 nye primær-/litteraturkilder samt egne scenarioer for husholdningsdannelse og hjemmetjenestebruk. Nasjonal og regional folketallsmodell har ulik nasjonalsum i 2050; forskjellen på 18 212 personer er beholdt og forklart. Ingen boligsalgsprognose eller kausal estimering av fruktbarhet.\n'.replace('\u0001','')
mark='**Arbeidsspråk og publiseringsspråk:**'
assert mark in src
src=src.replace(mark,insert+mark,1)
needle='**Foreløpig hovedkonklusjon:**'
intro='**9. Demografi og regional bærekraft (SSB 2026):** Nasjonalt MMM-scenario innebærer 6 214 071 innbyggere i 2050, opp fra 5 627 400 i 2026, men med sterk aldring og regionale forskjeller. Regionmodellens fylkesverdier summerer separat til 6 195 859 personer. Ingen nasjonal boligpriskollaps kan utledes av dette, og økende dødsfall er ikke identisk med frigjorte boliger. Nasjonalbudsjettet 2027 og Helsepersonellplan 2040 viser betinget finanspolitisk og arbeidskraftmessig risiko. Studiedesign og kilder finnes i §20. [K152](#k152) [K153](#k153) [K160](#k160) [K169](#k169)\n\n'
assert needle in src
src=src.replace(needle,intro+needle,1)
refblock='\n### 11.11 Demografi, befolkning, bolig, omsorg og skattebase (K152–K170)\n\n'
for num,org,ref in SOURCES:
 refblock+=f'<a id="k{num}"></a> **K{num} — {org}.** {ref}\n\n'
marker='\n## 12. Forskningstråd 01'
assert marker in src
src=src.replace(marker,'\n'+refblock+marker,1)
core=deltext.split('\n---\n',1)[1].strip()
core=re.sub(r'^# 09 — .*?\n','',core,count=1)
core=core.split('\n## Referanser i delrapport 09')[0].strip()
core=re.sub(r'^### (\d+)\.(\d+)\s+',lambda m:f'#### 20.{m.group(1)}.{m.group(2)} ',core,flags=re.M)
core=re.sub(r'^## (\d+)\.\s+',lambda m:f'### 20.{m.group(1)} ',core,flags=re.M)
src+='\n\n## 20. Forskningstråd 09 — Demografi, arbeidskraft, bolig og velferdsstatens bærekraft\n\n'+core+'\n\n**Kildeliste for delrapport 09:** [K152](#k152)–[K170](#k170) i hovedrapportens § 11.11.\n'
assert len(re.findall(r'<a id="k\d+"></a>',src))==170
name='Norsk_Okonomi_Forskningsrapport_2026-10-13_v1.1.0.md'
(R/name).write_text(src,encoding='utf8')
print('Integrert',name,'ord',len(src.split()),'kilder',len(re.findall(r'<a id="k\d+"></a>',src)))
