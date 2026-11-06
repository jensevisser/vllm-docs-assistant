# Python — spiekbriefje

Constructies die we in dit project gebruiken, met waar je ze tegenkomt. Groeit mee.
Fouten (`try`, `except`, `raise`) staan op een eigen spiekbriefje: [python-fouten-spiekbriefje.md](python-fouten-spiekbriefje.md).

**Inhoud**
- [Logging: iets laten zien terwijl het programma draait](#logging-iets-laten-zien-terwijl-het-programma-draait)
- [Plaatshouders in tekst: %s en %.2f](#plaatshouders-in-tekst-s-en-2f)
- [Modules en packages: code uit een ander bestand gebruiken](#modules-en-packages-code-uit-een-ander-bestand-gebruiken)
- [Parameters alleen bij naam (de ster)](#parameters-alleen-bij-naam-de-ster)
- [Een standaardwaarde als er niets is (x or y)](#een-standaardwaarde-als-er-niets-is-x-or-y)
- [Keuze op één regel (A if voorwaarde else B)](#keuze-op-één-regel-a-if-voorwaarde-else-b)
- [Wat je op de opdrachtregel typte (sys.argv)](#wat-je-op-de-opdrachtregel-typte-sysargv)
- [and / or in een voorwaarde, en kortsluiting](#and--or-in-een-voorwaarde-en-kortsluiting)
- [Een lijst of dict als standaardwaarde (valkuil)](#een-lijst-of-dict-als-standaardwaarde-valkuil)
- [Naam versus ding (wat het is-gelijkteken doet)](#naam-versus-ding-wat-het-is-gelijkteken-doet)
- [Overerving: een class bouwen op een andere class](#overerving-een-class-bouwen-op-een-andere-class)
- [Dataclass: een paar gegevens bij elkaar houden](#dataclass-een-paar-gegevens-bij-elkaar-houden)
- [Het @-teken: een decorator](#het--teken-een-decorator)
- [Twee klokken: `perf_counter` tegenover `time.time`](#twee-klokken-hoe-lang-perf_counter-tegenover-wanneer-timetime)
- [Kleine bekenden](#kleine-bekenden)
- [Docstring: beschrijving bij een functie of class](#docstring-beschrijving-bij-een-functie-of-class)

## Logging: iets laten zien terwijl het programma draait

```python
import logging
logger = logging.getLogger(__name__)      # naam = de module, bijv. src.llm_client

logger.info("gewone voortgang")           # standaard NIET zichtbaar
logger.warning("let op, maar gaat door")  # standaard wel zichtbaar
logger.info("duur=%.2fs", 0.123)          # %s / %.2f: de logger vult zelf in (geen f-string)
```

`info` ook zien? Bovenaan je script: `logging.basicConfig(level=logging.INFO)`.
In `src/` altijd logging, geen `print` (CLAUDE.md §6). De `%s`-plekken staan hieronder.
*Zie: `src/llm_client.py` regels 9, 81, 86 · rondleiding deel A en D.*

## Plaatshouders in tekst: %s en %.2f

```python
"%s"      % 3.14159     # '3.14159'   alles, net zoals print() het toont
"%.2f"    % 3.14159     # '3.14'      2 cijfers achter de komma, afgerond
"%.0f"    % 0.6         # '1'         rondt af
"%d"      % 3.9         # '3'         %d kapt af, richting nul
"%8.2f"   % 3.14159     # '    3.14'  8 posities breed; %-8.2f = linksuitgelijnd
"100%% klaar"           # '100% klaar'  %% is één echt procentteken
"%s na %.1fs" % ("ok", 2.25)   # meerdere: een tuple, in dezelfde volgorde
```

**`%.2f` rondt af, het kapt niet af.** Precies de helft gaat naar het **even** getal: `%.0f` geeft bij 0.5 → `0`, bij 1.5 → `2`, bij 2.5 → `2`. Dat voorkomt dat een reeks metingen systematisch omhoog schuift.
Let op: een getal dat op een halve lijkt, is binair vaak net iets minder. 2.675 staat opgeslagen als 2.67499999999999982236, dus `"%.2f" % 2.675` geeft `2.67`. Rond daarom alleen bij het **tonen**, en bewaar altijd de volle waarde.
`f"{x:.2f}"` volgt precies dezelfde regels.

**In logging** vul je ze niet zelf in, maar geef je de waarden als argumenten mee:

```python
logger.info("duur=%.2fs tokens=%s", 1.23456, None)   # duur=1.23s tokens=None
```

`%s` overleeft `None`; `%d` en `%.2f` geven dan een `TypeError`. Daarom staat er in `chat()` `tokens_in=%s` en niet `%d`: dat veld kan ontbreken.
Een fout in de plaatshouders stopt het programma níet: logging schrijft `--- Logging error ---` met een traceback naar stderr en draait door.
*Zie: `src/llm_client.py` regels 81–84 · `../code/voorbeelden/formatteren.py`.*

## Modules en packages: code uit een ander bestand gebruiken

```
src/__init__.py        ← leeg bestand: maakt van src/ een package
src/llm_client.py      ← een module, naam: src.llm_client
```

```python
from src.llm_client import chat   # één onderdeel uit een module
import time                       # hele module; gebruik: time.perf_counter()
```

`__name__` = naam van de module (`src.llm_client`), of `"__main__"` als je het bestand rechtstreeks start.
*Zie: rondleiding deel A.*

## Parameters alleen bij naam (de ster)

```python
def meet(kanaal, bereik=10, *, nplc=1): ...

meet(1)                  # ok: bereik=10, nplc=1
meet(1, 100, nplc=10)    # ok
meet(1, 100, 10)         # TypeError: na * alleen bij naam
```

**Parameter of argument?** De namen in de `def`-regel (`kanaal`, `bereik`, `nplc`) zijn de **parameters**. De waarden die je bij de aanroep meegeeft (`meet(1, 100, nplc=10)`) zijn de **argumenten**. Dezelfde plek, twee kanten: het aansluitpunt met het opschrift tegenover het signaal dat je erop zet.
*Zie: `chat()`, regel 34 · rondleiding deel A · `../code/voorbeelden/standaardwaarden.py`.*

## Een standaardwaarde als er niets is (x or y)

```python
options or {}     # None → {}, {"temperature": 0.2} → blijft
0 or 120          # → 120  (!) 0 telt als "niets"
```

"Niets" = `None`, `0`, `""`, `{}`, `[]`, `False`. Niet gebruiken als 0 een geldige waarde is.
*Zie: `chat()`, regels 48 en 50.*

## Keuze op één regel (A if voorwaarde else B)

```python
keuze = sys.argv[1] if len(sys.argv) > 1 else "from"
```

Lees het middenstuk eerst: is de voorwaarde waar → links, anders → rechts. Hetzelfde als:

```python
if len(sys.argv) > 1:
    keuze = sys.argv[1]
else:
    keuze = "from"
```

Alleen gebruiken als het op één regel leesbaar blijft; anders gewoon `if / else`.
*Zie: `../code/voorbeelden/raise_demo.py`, regel 30 · `../code/voorbeelden/hoe_komt_er_iets_in.py`.*

## Wat je op de opdrachtregel typte (sys.argv)

```python
import sys
print(sys.argv)
```

```
$ uv run python demo.py 1500
['demo.py', '1500']
```

`sys.argv[0]` is het bestand zelf, `sys.argv[1]` het eerste woord erachter. Altijd **tekst**, ook bij een getal: `float(sys.argv[1])` als je ermee wilt rekenen. Zonder argumenten heeft de lijst lengte 1, en geeft `sys.argv[1]` een `IndexError`. Meer dan twee knoppen → `argparse`.
*Zie: uitleg in `../code/sys-argv.md` · `../code/voorbeelden/argumenten.py` · `../code/voorbeelden/hoe_komt_er_iets_in.py`.*

## and / or in een voorwaarde, en kortsluiting

```python
if isinstance(m, dict) and "content" in m:        # goedkeuren: alles moet kloppen
if not isinstance(m, dict) or "content" not in m: # afkeuren: één reden is genoeg
```

Draai je een eis om, dan klapt `and` om naar `or`: *niet (A en B)* = *niet A of niet B*.

**Kortsluiting:** Python stopt zodra het antwoord vastligt. Bij `or` wordt rechts niet meer uitgevoerd als links `True` is; bij `and` niet als links `False` is. Zet daarom de controle die de ander mogelijk maakt links:

```python
m = None
"content" not in m          # TypeError: argument of type 'NoneType' is not iterable
```

*Zie: `chat()`, regel 70 · rondleiding deel D, sectie 3.*

## Een lijst of dict als standaardwaarde (valkuil)

```python
def f(options: dict | None = None):   # goed
    options = options or {}

def f(options: dict = {}):            # valkuil: één dict, gedeeld door alle aanroepen
```

Waarom: de `def`-regel draait één keer, en maakt de standaardwaarde dan; daarna krijgt elke aanroep datzelfde ding.

```python
def log_meting(waarde, log=[]): ...
log_meting(10.0)   # [10.0]
log_meting(9.9)    # [10.0, 9.9]   ← oude meting hangt er nog
```

Geldt voor lijst, dict en set. Getallen en teksten zijn veilig. Bekijken wat er bewaard is: `log_meting.__defaults__`.
*Zie: rondleiding deel A · `../code/voorbeelden/standaardwaarden.py`.*

## Naam versus ding (wat het is-gelijkteken doet)

Een naam is een sticker op een ding. Twee soorten "wijzigen":

```python
log = []             # sticker op een ANDER ding plakken → alleen hier merkbaar
log.append(10.0)     # op het ding ZELF schrijven → iedereen met dezelfde sticker ziet het
```

Daarom werkt `log = log or []`: een meegegeven logboek blijft, anders komt er een nieuw lijstje.
`log = []` altijd: gooit ook een bewust meegegeven logboek weg.

## Overerving: een class bouwen op een andere class

```python
class Meetinstrument:                         # ouder (basisclass)
    def __init__(self, serienummer, calibratiedatum):
        self.serienummer = serienummer
        self.calibratiedatum = calibratiedatum
    def omschrijving(self):
        return f"instrument {self.serienummer}, gecalibreerd {self.calibratiedatum}"

class Multimeter(Meetinstrument):             # kind: erft alles van Meetinstrument
    def __init__(self, serienummer, calibratiedatum, digits):
        super().__init__(serienummer, calibratiedatum)   # laat de ouder zijn deel doen
        self.digits = digits                              # eigen toevoeging
    def omschrijving(self):                               # override: vervangt die van de ouder
        return f"{self.digits}-digit multimeter, " + super().omschrijving()

dmm = Multimeter("MY12345", "2026-03-01", 6.5)
dmm.serienummer                         # "MY12345"  ← geërfd
dmm.omschrijving()                      # "6.5-digit multimeter, instrument MY12345, ..."
isinstance(dmm, Meetinstrument)         # True: een multimeter IS een meetinstrument
issubclass(Meetinstrument, Multimeter)  # False: andersom niet
```

| Begrip | Betekenis |
|---|---|
| erven | het kind krijgt alle attributen en methodes van de ouder |
| override | het kind schrijft een methode met dezelfde naam; die van het kind wint |
| `super()` | "de ouder": roep de versie van de ouder aan, bijv. in `__init__` |
| twee ouders | `class X(A, B)`: kan, maar spaarzaam gebruiken |

**Wanneer wel:** bij een "is een"-relatie: een multimeter ís een meetinstrument.
**Wanneer niet:** bij een "heeft een"-relatie: een meetopstelling *heeft* een multimeter. Geef hem er één als attribuut (`self.dmm = Multimeter(...)`), in plaats van te erven.
Bij fouten bepaalt de ouder ook wie de fout opvangt: zie [python-fouten-spiekbriefje.md](python-fouten-spiekbriefje.md).
*Zie: `../code/voorbeelden/instrument.py`.*

## Dataclass: een paar gegevens bij elkaar houden

```python
from dataclasses import dataclass

@dataclass(frozen=True)          # frozen: na het maken niet meer te wijzigen
class Meting:
    waarde: float
    eenheid: str

m = Meting(waarde=10.0003, eenheid="V")
m.waarde                          # 10.0003
m.waarde = 9.9                    # dataclasses.FrozenInstanceError
```

Python maakt zelf de `__init__` en de weergave bij `print`.
*Zie: `ChatResult`, regels 18–27 · rondleiding deel D · `../code/voorbeelden/meting_dataclass.py`.*

## Het @-teken: een decorator

```python
@dataclass
class A:
    x: int

class B:                 # precies hetzelfde resultaat
    x: int
B = dataclass(B)
```

`@f` boven een class of functie betekent: stop wat hieronder staat in `f`, en gebruik wat eruit komt. Met haakjes (`@dataclass(frozen=True)`) zijn dat de instellingen: die aanroep levert de decorator op, en die wordt toegepast.

Er komen nog: `@pytest.fixture` en `@pytest.mark.parametrize` (bouwstap 2), `@property`, `@app.get("/ask")` (FastAPI, Project 3).
*Zie: rondleiding deel D, sectie 4.*

## Twee klokken: hoe lang (`perf_counter`) tegenover wanneer (`time.time`)

```python
start = time.perf_counter()
...
duur = time.perf_counter() - start      # seconden, als float
```

| | `time.perf_counter()` | `time.time()` |
|---|---|---|
| gaf hier | `3416.564263329` | `1793816610.4274418` |
| betekent | seconden sinds een willekeurig punt (Linux: opstarten) | seconden sinds 1-1-1970 |
| monotoon | **True**: loopt altijd vooruit | **False**: kan verspringen bij een klokcorrectie |
| gebruik voor | **hoe lang** iets duurde | **wanneer** iets gebeurde |

Het losse getal van `perf_counter` zegt niets; alleen het verschil van twee aflezingen. Meet je een duur met `time.time()`, dan kan een klokcorrectie je een negatieve of te lange duur geven. Omgekeerd kun je met `perf_counter` geen datum opschrijven.
*Zie: `chat()`, regels 51 en 67 · rondleiding deel D, sectie 2.*

## Kleine bekenden

```python
data.get("message")         # None als het veld ontbreekt (data["message"] geeft KeyError)
isinstance(x, dict)         # is x een dict?
"content" not in message    # ontbreekt deze sleutel?
f"Timeout na {timeout} s"   # f-string: {..} wordt ingevuld
```

## Docstring: beschrijving bij een functie of class

```python
def chat(...):
    """Wat deze functie doet, in één zin."""
```

VSCodium toont hem als je met de muis over de naam beweegt.
