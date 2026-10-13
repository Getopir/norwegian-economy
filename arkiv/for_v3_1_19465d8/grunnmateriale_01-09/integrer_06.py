#!/usr/bin/env python3
"""Setter delrapport 06 inn i kanonisk norsk hovedrapport, med felles kilde-ID-er."""
from pathlib import Path
import re
R=Path(__file__).resolve().parent
p=R/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.7.0.md'
prior=p.read_text('utf8');sub=(R/'06_Skatt_eierskap_kapitalmobilitet_og_utflytting_v0.8.0.md').read_text('utf8')
assert 'Norsk Økonomi | Forskningsutgave 0.7.0' in prior
assert '## 12. Forskningstråd 01' in prior
sources=[]
for line in sub.splitlines():
 m=re.match(r'- \*\*K(\d+)\.\*\* (.+?) (https?://\S+)$',line)
 if m and int(m.group(1))>=93:
  key=int(m.group(1));s=m.group(2);url=m.group(3).strip()
  # Kilderegisterets lesbarhet: organisasjon/første forfatternavn først, resten i referansefelt.
  origin=re.split(r'\s+\*',s,maxsplit=1)[0].rstrip('. ')
  rest=s[len(origin):].strip(' .')
  sources.append((key,origin,rest,url))
assert len(sources)==20 and [x[0] for x in sources]==list(range(93,113)),sources
new_sources='\n\n### 11.8 Primærkilder og forskningslitteratur for forskningstråd 06\n\n'
new_sources+='Kildene nedenfor inkluderer **gjeldende rett i 2026**, formuesskatteutredninger som **ikke er lov**, SSBs registertall og forskningslitteratur. Arbeidsnotater oppgis som arbeidsnotater. Nyeste tall ble kontrollert 12. oktober 2026.\n\n'
for n,origin,rest,url in sources:
 new_sources+=f'<a id="k{n}"></a> **K{n} — {origin}.** {rest}. {url}\n\n'
prior=prior.replace('## 12. Forskningstråd 01',new_sources+'## 12. Forskningstråd 01',1)
prior=prior.replace('0.7.0 — forskningstråd 01–05: metode, økonomiske sammenligninger, bolig/kreditt, generasjonsøkonomi og entreprenørskap','0.8.0 — forskningstråd 01–06: metode, økonomiske sammenligninger, bolig/kreditt, generasjonsøkonomi, entreprenørskap og skatt/eiermobilitet')
prior=prior.replace('**Norsk Økonomi | Forskningsutgave 0.7.0 |','**Norsk Økonomi | Forskningsutgave 0.8.0 |',1)
prior=prior.replace('gir **åtte foreløpige hovedresultater**','gir **ni foreløpige hovedresultater**',1)
prior=prior.replace('**Arbeidsspråk og publiseringsspråk:** Norsk.','**Nytt i v0.8.0:** Delrapport 06 er publisert med NOU 2026: 9 sine 2021–2025-flyttedata, 2020–2024-saker om latente gevinster, norske skattesatser i 2026, alternative kausale og strukturelle studier samt Skattekommisjonens åpne provenyscenarier. Den har 12 hypoteser og 34 evidensoppføringer. Ingen selvstendig kjøring av taushetsbelagte mikrodata er hevdet utført.\n**Arbeidsspråk og publiseringsspråk:** Norsk.',1)
intro='9. **Skatt og eiermobilitet:** NOU 2026: 9 dokumenterer 141 utflyttere i et spesialutvalg på 3 565 svært formuende personer for 2021–2025. Et senere vedtak eller endring i skattesystemet er ikke forutsatt. Forskningsartikler finner skattedrevne flyttevirkninger, men er uenige om hvor store langsiktige realøkonomiske effekter dette gir. Latente skattegevinster er ikke kapitalstrømmer. [K97](#k97) [K102](#k102) [K103](#k103) [K104](#k104)\n\n'
prior=prior.replace('**Foreløpig hovedkonklusjon:**',intro+'**Foreløpig hovedkonklusjon:**',1)
prior=prior.replace('**Nøkkelord:** Fastlandsøkonomi,','**Nøkkelord:** Eiermobilitet, formuesskatt, skatt og investeringsbeslutninger, Fastlandsøkonomi,',1)
subbody=sub.split('\n---\n',1)[1].lstrip()
subbody=subbody.replace('# 06 — Skatt, eierskap, kapitalmobilitet og utflytting\n\n','',1)
subbody=re.sub(r'<a id="k(?:9[3-9]|10[0-9]|11[0-2])"></a>\s*\n','',subbody)
lines=[]
for l in subbody.splitlines():
 if l.startswith('#### '):l='#'+l
 elif l.startswith('### '):l='#'+l
 elif l.startswith('## '):l='#'+l
 lines.append(l)
prior+='\n\n## 17. Forskningstråd 06 — Skatt, eierskap, kapitalmobilitet og utflytting\n\n'+'\n'.join(lines)+'\n'
out=R/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.8.0.md';out.write_text(prior,'utf8')
print('Hovedrapport',len(prior),'tegn','nye kilde-ID',len(sources))
