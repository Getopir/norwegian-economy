#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministisk fondstresstest for Norsk Økonomi. Ingen estimert sannsynlighetsfordeling.
F(t+1) = max(0, F(t)*(1+r) + P0*(1-d)**n - U0*(1+g)**n).
F=22400 fra Nasjonalbudsjettet 2027 (beregningsteknisk estimat ved inngang).
P0=568.4 fra Nasjonalbudsjettet 2027; U0=561.7 er *kontant* underskudd.
Gjelder hypotetiske, faste modellkroner uten særskilt NOK/valutakurv-bro.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Antakelser:
    navn: str
    realavkastning: float = 0.03
    uttaksvekst: float = 0.015
    petroleumsfall: float = 0.06
    startfall: float = 0.0

STARTAAR = 2027
SLUTTAAR = 2100
STARTFOND = 22400.0
STARTPETROLEUM = 568.4
STARTUTTAK = 561.7

def beregn_bane(antakelser:Antakelser, startaar:int=STARTAAR, slutaar:int=SLUTTAAR):
    assert 2027 <= startaar <= slutaar <= 2200
    assert -0.99 < antakelser.realavkastning < 2
    assert -0.5 < antakelser.uttaksvekst < 2
    assert 0 <= antakelser.petroleumsfall <= 1
    assert 0 <= antakelser.startfall <= 0.99
    fond=STARTFOND * (1-antakelser.startfall)
    serie=[]
    # Beregn alle år fra 2027 for å sikre korrekte starttilstander ved senere vinduer.
    for year in range(STARTAAR,slutaar+1):
        n=year-STARTAAR
        pet=STARTPETROLEUM*(1-antakelser.petroleumsfall)**n
        uttak=STARTUTTAK*(1+antakelser.uttaksvekst)**n
        avk=fond*antakelser.realavkastning
        saldo=fond+avk+pet-uttak
        mangel=max(0,-saldo)
        slutt=max(0,saldo)
        post={
          'scenario':antakelser.navn,
          'aar':year,
          'fond_ved_inngang_mrd':round(fond,3),
          'realavkastning_mrd':round(avk,3),
          'petroleumstilforsel_mrd':round(pet,3),
          'kontantuttak_mrd':round(uttak,3),
          'fond_ved_utgang_mrd':round(slutt,3),
          'uttak_prosent_av_inngangsfond':round(100*uttak/fond,3) if fond>0 else None,
          'tre_prosent_av_inngangsfond_mrd':round(.03*fond,3),
          'manglende_kontanter_ved_nullgrense_mrd':round(mangel,3),
          'modelltype':'D – deterministisk hypotetisk scenario; ingen prognose'
        }
        if year>=startaar:serie.append(post)
        fond=slutt
    return serie

SCENARIOER=[
 Antakelser('A – mekanisk referanse',.03,.015,.06,0),
 Antakelser('B – lav realavkastning',.01,.015,.06,0),
 Antakelser('C – raskere vekst i uttak',.03,.03,.06,0),
 Antakelser('D – initialt fondssjokk',.03,.015,.06,.25),
 Antakelser('E – raskt fall i petroleum',.03,.015,.10,0),
 Antakelser('F – kombinert belastning',.015,.025,.10,.25),
]

if __name__=='__main__':
    for s in SCENARIOER:
        d=beregn_bane(s)
        by={x['aar']:x for x in d}
        first_too_high=next((r['aar'] for r in d if r['uttak_prosent_av_inngangsfond'] is not None and r['uttak_prosent_av_inngangsfond']>3),None)
        first_zero=next((r['aar'] for r in d if r['fond_ved_inngang_mrd']<=0),None)
        print(s.navn, 'fond utg 2060:',by[2060]['fond_ved_utgang_mrd'], 'første >3%:',first_too_high, 'nullgrense:',first_zero)
    # Eksakte aritmetiske kontroller
    r=beregn_bane(SCENARIOER[0])[0]
    assert r['fond_ved_inngang_mrd']==22400.0
    assert r['petroleumstilforsel_mrd']==568.4
    assert r['kontantuttak_mrd']==561.7
    assert r['fond_ved_utgang_mrd']==23078.7
    assert beregn_bane(Antakelser('sjokk',startfall=.25))[0]['fond_ved_inngang_mrd']==16800
