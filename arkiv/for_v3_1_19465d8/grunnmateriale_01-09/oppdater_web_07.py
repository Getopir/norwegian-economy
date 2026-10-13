#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Integrerer delrapport 07 i den eksisterende, reproduserbare publiseringsbyggeren."""
from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'kildekode'/'bygg_publisering.py'
s=p.read_text('utf8')
s=s.replace("VERSION = 'v0.8.0'", "VERSION = 'v0.9.0'")
s=s.replace('assert len(sources)==112', 'assert len(sources)==136').replace('forventet 112 kilder','forventet 136 kilder')
s=s.replace("'rapportversjon':'0.8.0'","'rapportversjon':'0.9.0'")
needle="with (DATA/'observasjoner.csv').open('w',encoding='utf-8-sig',newline='') as f:"
assert needle in s
injected='''# Delrapport 07: offentlig utgiftsregnskap, COFOG, stillingsandel og metodeindikatorer.
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

'''
s=s.replace(needle,injected+needle)
s=s.replace("for traad in ('02','03','04','05','06'):","for traad in ('02','03','04','05','06','07'):")
# Ny eksplisitt trådlenke i hypoteseregister (alle andre urørt).
line="          'status':item['status'],'ankerkobling':'#rapport-'+('13-forskningstrad-02-norsk-okonomis-relative-utvikling-og-internasjonal-sammenligning' if traad=='02' else ('14-forskningstrad-03-bolig-kreditt-eiendomsformue-og-kapitalallokering' if traad=='03' else '15-forskningstrad-04-generasjonsokonomi-mobilitet-og-fordeling' if traad=='04' else '16-forskningstrad-05-entreprenorskap-skalering-og-unges-arbeidsmarked' if traad=='05' else '17-forskningstrad-06-skatt-eierskap-kapitalmobilitet-og-utflytting'))})"
assert line in s
s=s.replace(line,"          'status':item['status'],'ankerkobling':'#rapport-'+('18-forskningstrad-07-offentlig-ressursbruk-effektivitet-og-baumols-kostnadssykdom' if traad=='07' else ('13-forskningstrad-02-norsk-okonomis-relative-utvikling-og-internasjonal-sammenligning' if traad=='02' else ('14-forskningstrad-03-bolig-kreditt-eiendomsformue-og-kapitalallokering' if traad=='03' else '15-forskningstrad-04-generasjonsokonomi-mobilitet-og-fordeling' if traad=='04' else '16-forskningstrad-05-entreprenorskap-skalering-og-unges-arbeidsmarked' if traad=='05' else '17-forskningstrad-06-skatt-eierskap-kapitalmobilitet-og-utflytting')))})")
s=s.replace('assert len(hypotheses)==67','assert len(hypotheses)==81')
s=s.replace("json.loads((ROOT/'data'/'evidensregister_06.json').read_text('utf-8'))","json.loads((ROOT/'data'/'evidensregister_06.json').read_text('utf-8')) + json.loads((ROOT/'data'/'evidensregister_07.json').read_text('utf-8'))")
s=s.replace('assert len(evidence)==164','assert len(evidence)==204')
mark=next(line for line in s.splitlines() if "@@NOU06@@" in line)
assert mark in s
s=s.replace(mark,mark+'''
  '@@OFF07@@':json.dumps(OFF07,ensure_ascii=False).replace('<','\\u003c'),
  '@@COFOG07@@':json.dumps(COFOG07,ensure_ascii=False).replace('<','\\u003c'),
  '@@JOB07@@':json.dumps(JOB07,ensure_ascii=False).replace('<','\\u003c'),
  '@@HOVED07@@':json.dumps(HOVED07,ensure_ascii=False).replace('<','\\u003c'),''')
s=s.replace("' *_06.*'","' *_06.*'")
s=s.replace("(' *_01.*'","(' *_01.*'")
assert "'*_06.*'):" in s
s=s.replace("'*_06.*'):","'*_06.*','*_07.*'):")
needle="copy_if_different(ROOT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md',SITE/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')"
assert needle in s
s=s.replace(needle,needle+"\ncopy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',SITE/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')")
needle="copy_if_different(ROOT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md',OUT/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md')"
assert needle in s
s=s.replace(needle,needle+"\ncopy_if_different(ROOT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md',OUT/'07_Offentlig_ressursbruk_effektivitet_Baumol_v0.9.0.md')")
p.write_text(s,encoding='utf8')
print('Oppdatert byggesystem for 07.')
