#!/usr/bin/env python3
"""Legger tråd 05 inn i hovedrapport, og publiserer nye fagkilder som K77–K92."""
from pathlib import Path
import re
R=Path(__file__).resolve().parent
prior=(R/'Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.6.0.md').read_text('utf8')
sub=(R/'05_Entreprenorskap_skalering_innovasjon_arbeidsmarked_v0.7.0.md').read_text('utf8')
K=[
('77','Statistisk sentralbyrå (2026).','*Føretak*, statistikksiden, tabell 08076/09028/13759; oppdatert 19. august 2026. https://www.ssb.no/virksomheter-foretak-og-regnskap/virksomheter-og-foretak/statistikk/foretak'),
('78','Fjærli, E., Nygård, I. A. og Rybalka, M., SSB (2025).','*Fra oppstart til vekst: Kartlegging av norske vekstforetak 2005–2023*, Rapporter 2025/20, 12. august 2025. https://www.ssb.no/virksomheter-foretak-og-regnskap/virksomheter-og-foretak/artikler/fra-oppstart-til-vekst'),
('79','Rybalka, M., SSB (2025).','*Fra potensial til realisering – Hva skjer med lovende startups over tid?* Forskningsformidlingsartikkel, 12. august 2025. https://www.ssb.no/virksomheter-foretak-og-regnskap/virksomheter-og-foretak/artikler/fra-potensial-til-realisering-hva-skjer-med-lovende-startups-over-tid'),
('80','OECD (2026).','*OECD Economic Surveys: Norway 2026*, kapittel 4: *Resetting regulatory frameworks to revive business dynamism*, publisert 17. juni 2026. https://www.oecd.org/en/publications/oecd-economic-surveys-norway-2026_5cc02644-en/full-report/resetting-regulatory-frameworks-to-revive-business-dynamism_4501d1ee.html'),
('81','Statistisk sentralbyrå (2025).','*Etablerere i næringslivet*, foreløpige 2024-tall, tabeller 14624 og 14613, publisert 30. september 2025. https://www.ssb.no/virksomheter-foretak-og-regnskap/eierskap-og-roller/statistikk/etablerere-i-naeringslivet'),
('82','Norsk venturekapitalforening/Menon Economics (2026).','*Aktivitetsundersøkelse 2025*, nordisk tidligfase- og private-equity-statistikk, publisert 20. mai 2026; bransjefinansiert. https://nvca.no/uploads/157/NVCA-aktivitetsundersokelse-2025-FINAL.pdf'),
('83','Oslo Economics på oppdrag fra NVCA (2026).','*Kartlegging av pensjonskapitalens rolle i det norske markedet for private equity og venturekapital*, mai 2026; oppdragsfinansiert analyse. https://nvca.no/wp-content/uploads/2026/05/NVCA-rapport-om-pensjonskapital-2026-Kartlegging-av-pensjonskapital-i-norsk-PE-og-VC-2.pdf'),
('84','Langhoff, K. og Berrios, C., SSB (2026).','*Nedgang i næringslivets FoU i 2024*, publisert 21. april 2026. https://www.ssb.no/teknologi-og-innovasjon/forskning-og-innovasjon-i-naeringslivet/statistikk/forskning-og-utvikling-i-naeringslivet/artikler/nedgang-i-naeringslivets-fou-2024'),
('85','Statistisk sentralbyrå (2025).','*Innovasjon i næringslivet*, måleperiode 2022–2024, oppdatert 11. desember 2025, SSB tabell 12808. https://www.ssb.no/teknologi-og-innovasjon/informasjons-og-kommunikasjonsteknologi-ikt/statistikk/innovasjon-i-naeringslivet'),
('86','Statistisk sentralbyrå (2026).','*Hva er NEET?* Faktaside og foreløpige registertall 2025 for 15–29-åringer. https://www.ssb.no/arbeid-og-lonn/faktaside/hva-er-neet'),
('87','Statistisk sentralbyrå (2026).','*Unge som verken er i jobb eller utdanning. Hva er arbeidsledighet?* Undervisningsopplegg og historiske AKU-tall. https://www.ssb.no/ssb-skole/undervisningsopplegg/det-norske-arbeidsmarkedet/unge-som-verken-er-i-jobb-eller-utdanning.hva-er-arbeidsledighet'),
('88','Baumann, S. H., SSB (2026).','*Flere nyutdannede ser etter ny jobb*, 23. juni 2026. https://www.ssb.no/arbeid-og-lonn/sysselsetting/statistikk/arbeidskraftundersokelsen/artikler/flere-nyutdannede-ser-etter-ny-jobb'),
('89','Fjærli, E. og Rybalka, M., SSB (2026).','*Resultater av Forskningsrådets næringsrettede virksomhet i perioden 2006–2024*, Rapporter 2026/6, 18. mars 2026. https://www.ssb.no/teknologi-og-innovasjon/forskning-og-innovasjon-i-naeringslivet/artikler/resultater-av-forskningsradets-naeringsrettede-virksomhet-i-perioden-2006-2024'),
('90','Statistisk sentralbyrå (2026).','*Globale verdikjeder og outsourcing*, statistikk og metodebeskrivelse; brukt kun for definisjonsavgrensning mot utflytting. https://www.ssb.no/utenriksokonomi/utenrikshandel/statistikk/globale-verdikjeder-og-outsourcing'),
('91','Statistisk sentralbyrå (2026).','*Økonomiske analyser 2/2026 – Utsyn over året 2025*, kapittel 4 om næringsstruktur, FoU-dybde og FoU-intensitet. https://www.ssb.no/nasjonalregnskap-og-konjunkturer/okonomiske-analyser/okonomiske-analyser-2-2026-utsyn-over-aret-2025'),
('92','OECD (2025).','*Benchmarking Government Support for Venture Capital*, komparativ policyrapport. https://www.oecd.org/en/publications/benchmarking-government-support-for-venture-capital_81e53985-en.html')]
assert len(K)==16 and all('https://' in row[2] for row in K)
new_sources='\n\n### 11.7 Nye empiriske kilder for forskningstråd 05\n\n'
new_sources+='Kildene dokumenterer tidfestede mål. For K82 og K83 er bransjens finansierings- og interesseposisjon opplyst særskilt. Kravene i forskningstråd 01 til kildesporbarhet og motforklaringer gjelder også her.\n\n'
new_sources+='\n\n'.join(f'<a id="k{n}"></a> **K{n} — {org}** {info}' for n,org,info in K)+'\n\n'
assert '## 12. Forskningstråd 01' in prior
prior=prior.replace('## 12. Forskningstråd 01',new_sources+'## 12. Forskningstråd 01',1)
prior=prior.replace('**Norsk Økonomi | Forskningsutgave 0.6.0 |','**Norsk Økonomi | Forskningsutgave 0.7.0 |')
prior=prior.replace('0.6.0 — forskningstråd 01–04: metode, økonomiske sammenligninger, bolig/kreditt og generasjonsøkonomi','0.7.0 — forskningstråd 01–05: metode, økonomiske sammenligninger, bolig/kreditt, generasjonsøkonomi og entreprenørskap')
prior=prior.replace('gir **sju foreløpige hovedresultater**','gir **åtte foreløpige hovedresultater**')
intro='8. **Entreprenørskap og arbeidsmarked:** Kvartalsregistreringene er relativt høye i 2026, men OECD finner nedgang over tid i sysselsettingens andel i unge foretak og SSB registrerer at få lovende oppstartsforetak når scaleup-status. Nordisk bransjestatistikk viser lavt norsk tidligfasekapitalvolum; foretakets næring og definisjonsvalg påvirker bildet. NEET og nyutdannede må måles separat. Kausal effekt av skatter, kapitaltilførsel og boliggjeld er uavklart. [K77](#k77) [K79](#k79) [K80](#k80) [K82](#k82) [K86](#k86) [K88](#k88)\n\n'
assert '**Foreløpig hovedkonklusjon:**' in prior
prior=prior.replace('**Foreløpig hovedkonklusjon:**',intro+'**Foreløpig hovedkonklusjon:**',1)
prior=prior.replace('**Arbeidsspråk og publiseringsspråk:** Norsk.','**Nytt i v0.7.0:** Forskningstråd 05 inkluderer SSBs foretaksregistreringer 2024–2026, entreprenøralder, niårs vekstoverganger, OECDs 2026-vurdering av næringsdynamikk, nordisk tidligfasekapital, FoU og innovasjon, unge utenfor arbeid/utdanning og en eksisterende quasi-eksperimentell evaluering av FoU-støtte. Den har 12 hypoteser og 30 nye evidensposter. Et fullstendig nordisk foretakspanel og uavhengig kausalestimering gjenstår.\n**Arbeidsspråk og publiseringsspråk:** Norsk.',1)
body=sub.split('\n---\n',1)[1].lstrip()
body=body.replace('# 05 — Entreprenørskap, vekstbedrifter, innovasjon, risikokapital og unges arbeidsmarked\n\n','',1)
lines=[]
for l in body.splitlines():
 if l.startswith('### '):l='#'+l
 elif l.startswith('## '):l='#'+l
 lines.append(l)
body='\n'.join(lines)
prior+='\n\n## 16. Forskningstråd 05 — Entreprenørskap, skalering og unges arbeidsmarked\n\n'+body+'\n'
R.joinpath('Norsk_Okonomi_Forskningsrapport_2026-10-12_v0.7.0.md').write_text(prior,encoding='utf8')
print('integrert master',len(prior),'bytes sources',len(K))
