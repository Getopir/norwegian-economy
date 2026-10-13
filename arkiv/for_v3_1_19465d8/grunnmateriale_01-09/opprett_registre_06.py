#!/usr/bin/env python3
"""Maskinlesbart hypoteseregister og evidensjournal for delrapport 06."""
from pathlib import Path
import json,csv,re
R=Path(__file__).resolve().parent;D=R/'data'

def out(name,rows):
 with (D/(name+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 (D/(name+'.json')).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n','utf8');print(name,len(rows))
# id,tittel,hypotese,mothypotese,variabler,kilder,identifikasjon,falsifikasjon,evidensstatus
hraw=[
('01','Skattedrevet utflytting','Høyere beskatning av eiere øker flytterate i berørte skattegrupper','Mobilitet påvirkes primært av internasjonale jobb-, familie- og livsløpsfaktorer','Skatteeksponering, bosted, formue, kontrollgrupper, år','K97 K102 K103','Naturlige skattereformer, eventstudie med parallelle-trendtest, negativ kontroll','Robust flytterespons forsvinner med gode kontrollgrupper','C'),
('02','Utflytting og realinvesteringer','Når eieren flytter reduseres nye investeringer og norske jobber','Eier beholder virksomhet, kapital finansieres utenfra','Eierkobling, foretakscashflow, CAPEX, ansatte, FoU','K102 K103 K104','Matchet firmapanel rundt utflytting, test førsjokk','Ingen netto reduksjon etter seleksjonskontroll','C'),
('03','Oppstart som uteblir','Skatteregler flytter framtidige gründerprosjekter og IP ut av Norge','Tilgang til internasjonale markeder oppveier flytting og netto norsk aktivitet endres lite','Gründerhistorikk, personadresse, registrert IP, arbeidsplasser','K102 K104','Hendelsesstudier og etableringspanel 5–15 år','Ingen forskjell i nye prosjekter etter eksogent skattesjokk','U'),
('04','Likviditet og utbyttepress','Formuesskatt utløser ekstra utbytte og lavere investering i likviditetssvake foretak','Eierne har alternative likviditetskilder og skattemessige verdsettingsgrunnlag er lavt','Skattekrav, bankinnskudd, utbytte, kontantstrøm, investeringsplan','K107 K102 K98','Utnytt terskler og differensiell eierlikviditet','Ikke større utbytte- eller investeringseffekt for berørte foretak','C'),
('05','Verdsettingsrabatter og bolig','Ulike formuesverdier fører til relativ kapitalvridning fra bedrift til bolig','Boligpriser bestemmes av tilbud, renter, inntekt og andre ordninger','Portefølje, skattegrunnlag, kreditt, boligpriser, privat kapital','K93 K98 K106','Identifikasjon fra portefølje-/skattereform og lokale boligforhold','Relativ portefølje forblir uendret ved endret skatteforskjell','B'),
('06','Lokalt eierskap i vekstbedrifter','Personlig norsk eierbeskatning svekker tilførsel av lokal egenkapital','Utenlandsk kapital erstatter lokal kapital til samme eller lavere pris','Finansieringsrunder, lokalt eierskap, avkastningskrav, eierland','K98 K109 K110','Prosjektpanel rundt finansiering og regelendringer','Finansieringsgap og investeringskostnad upåvirket etter kontroll','U'),
('07','Utflyttingsskatt og innlåsing','Exitskatt begrenser flytting og låser kapital/gründere før internasjonal skalering','Exitskatt hindrer skattelekkasje uten å redusere realinvestering','Latent gevinst, faktisk flytting, etablering, investering','K95 K104','Sammenlign terskelberørte og ueksponerte med hendelsesstudie','Ingen robust endring i investering/lokalisering etter reform','U'),
('08','Betalingsutsettelse 2026','Utsettelsesordningen øker investering og overlevelse i likviditetssvake selskap','Høy rentemargin begrenser bruken og påvirker ikke investering','Utsettelse, rente, kontantstrøm, investering, overlevelse','K96','Bruk eksponeringsgrense med skatte-/firmapanel 2026–2030','Ingen forskjell i investering eller overlevelse etter differanseanalyse','U'),
('09','Skattekommisjonens design','Likere grunnlag og lavere formuesskatt gir bedre produktiv allokering','Provenytap og fordelingsvirkninger overskygger effektivitetsgevinst','Proveny, portefølje, CAPEX, Gini, arbeidstilbud','K98 K99','LOTTE-Skatt + strukturell følsomhet, reformvarianter og finansiering','Samlet nytteeffekt negativ etter full proveny-/fordelingskontroll','D'),
('10','Forutsigbarhet og kapitalkostnad','Usikre skatteregler øker kapitalkostnad og flytting av hovedkontor','Rasjonelle investorer tar høyde for varslede regler, lav reell usikkerhet','Endringsfrekvens, kapitalrenter, IP, investeringer','K98 K111','Naturlig eksperiment rundt varsler og vedtak, separate sjokk','Ingen ny kapitalkostnad etter kontroll for andre regulatoriske sjokk','U'),
('11','Dynamisk skattegrunnlag','Atferd gjør faktisk proveny vesentlig ulikt de statiske anslagene','Tilpasningen er liten og kortsiktige satsvirkninger dominerer','Skatt per pers, utflytting, skattebase, næringsinntekter','K99 K102 K103','Koble administrative skattestrømmer i langtidspanel med økonomisk motmodell','Dynamisk provenyavvik er innenfor forhåndsdefinert usikkerhetsintervall','D'),
('12','Generasjoners kapitaltilgang','Eier- og boligbeskatning bidrar til finansieringsgap for unge grunnleggere','Arv, kredittsyklus, lønn og boligtilbud forklarer gapet','Alder, husholdningsformue, bolig, startkapital, arbeidsinntekt','K98 K100 K108','Kohortanalyse med eksogene sjokk, test familiekontroll','Ingen skatteindusert forskjell i alderstilpasset etablering','U'),
]
hyp=[]
for id,title,h,a,v,k,t,f,e in hraw:
 hyp.append({'id':'H06-'+id,'tittel':title,'hypotese':h,'mothypotese':a,'variabler':v,'primarkilder':k,'empirisk_test':t,'falsifikasjonskriterium':f,'evidensklasse':e,'tillit':'Ikke selvstendig kausalt testet i dette prosjektet','status':'Litteraturgrunnlag / test utestående' if e in ('C','B') else 'Ikke testet','traad':'06'})
out('hypoteseregister_06',hyp)
# id,tittel,utsagn,klasse,kilder,hypotese,usikkerhet,alternativ,begrensning
Eraw=[
('001','Formuesskatt bunnfradrag','Enslig 2026 bunnfradrag 1,9 mill. kr','A','K93 K96','01','Høy','Skattemessig nettoformue, ikke markedsformue','Dobbelt innslagspunkt for ektefeller'),
('002','Marginal formuesskatt 2026','1,0 % i første intervall og 1,1 % over 21,5 mill. kroner','A','K93','01','Høy','Stat/kommune sammenlagt','Kun skattepliktig nettoformue'),
('003','Verdsetting aksjer','Aksjer formelt 80 % av beregnet formuesverdi','A','K93 K112','05','Høy','Ikke-børsnoterte verdsettes med andre metoder','Markedsverdi er ikke automatisk skatteverdi'),
('004','Verdsetting primærbolig','75 % rabatt i nedre verdibånd 2026','A','K93 K98','05','Høy','Høyere verdibånd har 30 % rabatt','Grense 14 mill. kroner'),
('005','Skatt på utbytte','37,84 % på aksjeutbytte/gevinster etter skjerming','A','K94 K109','04','Høy','Fritaksmetoden for selskap','Ikke alle transaksjoner er personlig utbytte'),
('006','Selskapsskatt','22 % nominell alminnelig selskapsskatt i 2026','A','K110 K109','04','Høy','Sektorunntak og skjerming','Ikke effektiv skattesats'),
('007','Skattemarginal eksempel','51,5152 % samlet selskaps- og personlig skatt ved full utdeling uten skjerming','A','K94 K110','04','Høy for aritmetikk','Alternativ uttakstidspunkt og skjerming','Mekanisk regneeksempel, ikke gjennomsnitt'),
('008','Exitskatt bunnfradrag','3 mill. kr latent gevinst og 12 års betalingsfrist for de nye reglene','A','K95','07','Høy','EØS- og tilbakeflyttingsregler varierer','Ikke skatt på selskapets kapital'),
('009','Utsettelse formuesskatt 2026','Opptil tre år ved >30 000 kroner; rente styringsrente +5 pp','A','K96','08','Høy','Løser tid, ikke nødvendigvis kostnad','Virkning utestet'),
('010','Spesialutvalg antall','3565 svært formuende definert av NOU for 2021–2025','A','K97','01','Høy','Seleksjon etter rikdom og Kapitalliste','Ikke representativt'),
('011','Utflyttere 2021','16 folkeregistrerte utflyttere i spesialutvalg','A','K97','01','Høy','Grunner for flytting ukjent','Administrative data'),
('012','Utflyttere 2022','46 folkeregistrerte utflyttere i spesialutvalg','A','K97','01','Høy','Grunner for flytting ukjent','Administrative data'),
('013','Utflyttere 2023','46 folkeregistrerte utflyttere i spesialutvalg','A','K97','01','Høy','Grunner for flytting ukjent','Administrative data'),
('014','Utflyttere 2024','16 folkeregistrerte utflyttere i spesialutvalg','A','K97','01','Høy','Grunner for flytting ukjent','Administrative data'),
('015','Utflyttere 2025','17 folkeregistrerte utflyttere i spesialutvalg','A','K97','01','Høy','Grunner for flytting ukjent','Administrative data'),
('016','Sum utflyttere','141 registrerte utflyttere 2021–2025 i NOU-utvalg','A','K97','01','Høy for sum','Ikke antall skattedrevet flytting','Femårsperiode og utvalgsdefinisjon'),
('017','Sum innflyttere','46 registrerte innflyttere 2021–2025 i NOU-utvalg','A','K97','01','Høy for sum','Ikke total innflytting blant rikeste','Utvalgsavgrensning'),
('018','Fastsatt formuesskatt før utvandring','549 mill. kroner summert på tvers av tidligere skatteår','A','K97','11','Høy for sum','Ikke nåverdi av statens inntektsbortfall','Ulike skatteår'),
('019','Utflyttingsskattesaker 2022','167 saker, latente gevinster 133,8 mrd. kr','A','K97','07','Høy for oppgitte tall','Skatt kan utsettes; aktiva kan bli i Norge','Ikke flyttet kapital'),
('020','Utflyttingsskattesaker 2023','187 saker, latente gevinster 44,284 mrd. kr','A','K97','07','Høy for oppgitte tall','Annet registreringstidspunkt enn personflytting','Ikke flyttet kapital'),
('021','SSB betalere formuesskatt','701 482 personer i 2024, 44 300 kr gjennomsnitt blant betalere','A','K101','11','Høy','Ingen kausal provenyrespons','2024 ikke 2026'),
('022','NOU 2026 prognose formuesskatt','Om lag 36 mrd. kroner i 2026 foreslått 2027-budsjett','A','K110','11','Høy for anslag','Prognose ikke endelig innbetaling','Budsjettanslag'),
('023','NOU satsalternativer','0,25–0,75 % enkel sats uten verdsettingsrabatter er foreslått ramme','A','K98','09','Høy for forslag','Uenighet om konkret sats','Ikke gjeldende lov'),
('024','NOU statisk provenyscenario','0,5 % med særskilt primærboligfradrag 7m gir -15,7 mrd. kr','D','K98','09','Modellavhengig','Oppførsel og videre finansiering kan endre resultat','Statiske provenyanslag, ikke BNP'),
('025','Ring 2026 flytterespons','Opptil rundt 100 flyttinger tilskrevet reformene','C','K102','01','Moderat, arbeidsnotat','Ulike identifikasjonsdesign/forventninger','Ekstern studie ikke replikert'),
('026','Ring 2026 investering','Ingen statistisk påvist nedgang i undersøkte firmaers investering','C','K102','02','Moderat, arbeidsnotat','Utfall på lengre sikt og nye bedrifter utelatt','Ikke bevis for null virkning'),
('027','Jakobsen mfl. flytterespons','-2 % rik skattyterbestand ved +1 pp topp formuesskatt','C','K103','01','Moderat til høy, fagfellevurdert','Heterogenitet mellom land og reformer','Ulikt årlige bruttoflyttinger'),
('028','Jakobsen mfl. aggregert effekt','-0,02 % sysselsetting,-0,07 % investering,-0,10 % verdiskaping ved +1 pp','D','K103','02','Modellavhengig','Long-run heterogenitet kan være annerledes','Aggregert estimat, ikke årsstatistikk'),
('029','Blandhol langsiktig','-1,3 % produksjon i langsiktig strukturmodell','D','K104','03','Modellavhengig','Produktivitetstap antas ved fremmed bosted','Ikke observert BNP-fall'),
('030','Iacono Bø intern migrasjon','Skattedifferanse i Bø gir lokal mobilitetsrespons','C','K105','01','Moderat','Skattekonkurranse kommune versus land','Kan ikke ekstrapoleres direkte internasjonalt'),
('031','Porteføljeallokering','Norsk skatteskapt aksjepremie påvirker porteføljer betydelig men langsomt','C','K106','05','Moderat','Porteføljeendring er ikke direkte ny norsk realinvestering','Kilde er arbeidsnotat'),
('032','Kontrafaktisk oppstartseffekt','Egen norsk kausal effekt på nyetableringer etter eierutflytting er ikke estimert','U','K102 K104','03','Åpent spørsmål','Alternativ virksomhet kan oppstå i Norge/utlandet','Ingen egen registerkjøring'),
('033','Sammenlignbarhet kapitaltap','Ingen gyldig likhet mellom sum latent gevinst og fysisk kapitalutflytting','A','K97','07','Høy definisjon','Verdier i eierskap og transaksjoner ulike størrelser','Begrepsavgrensning'),
('034','NOU 2026 kortsikt vs langsikt','Statiske skatteprovenyberegninger inkluderer ikke endelig dynamisk effekt','A','K99','11','Høy metode','Eventuelle vekstvirkninger utestet','Modellforbehold'),
]
E=[]
for ident,title,fact,klass,src,idx,conf,alt,lim in Eraw:
 E.append({'id':'E06-'+ident,'tittel':title,'traad':'06','utsagn':fact,'evidensklasse':klass,'status':('Foreløpig kildebelagt' if klass!='U' else 'Åpent – ikke gjennomført'),'tillit':conf,'primaerkilde':src,'kilde_id':src,'hypotese':'H06-'+idx,'resultat':fact,'mothypotese':alt,'variabler':'Se hypotese H06-'+idx,'empirisk_test':next(x['empirisk_test'] for x in hyp if x['id']=='H06-'+idx),'falsifikasjonskriterium':next(x['falsifikasjonskriterium'] for x in hyp if x['id']=='H06-'+idx),'datavintage':'2026-10-12','begrensninger':lim,'epistemisk_rolle':'KILDEBELAGT '+klass if klass!='U' else 'IKKE TESTET','ansvar':'Norsk Økonomi, forskningstråd 06','registrert':'2026-10-12','forskningslitteratur':'K93–K112 avhengig av tema','kildereferanser_kontrollert':src})
out('evidensregister_06',E)
assert len(hyp)==12 and len(E)==34 and set(x['hypotese'] for x in E)<=set(x['id'] for x in hyp)
