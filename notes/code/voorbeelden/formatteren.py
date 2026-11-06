"""Wat %s en %.2f doen, en hoe %.2f afrondt. Draai: uv run python notes/code/voorbeelden/formatteren.py"""

import logging

print("== 1. de plaatshouders ==")
duur = 3.14159
print("%s"      % duur)        # str(): precies wat print() ook zou tonen
print("%.2f"    % duur)        # 2 cijfers achter de komma
print("%.0f"    % duur)        # geen cijfers achter de komma
print("%f"      % duur)        # %f zonder getal: altijd 6 cijfers
print("%8.2f|"  % duur)        # 8 posities breed, rechts uitgelijnd
print("%-8.2f|" % duur)        # linksuitgelijnd
print("%d"      % duur)        # %d kapt WEL af: naar heel getal, richting nul
print("tokens=%d, duur=%.2fs, 100%% klaar" % (53, 1.2345))   # meerdere, en %% = een echt %-teken

print("\n== 2. afkappen of afronden? ==")
for waarde in [0.6, 1.4, 1.449, 1.451, -1.6]:
    print(f"  {waarde!r:>8}  ->  %.0f met %%.0f: {'%.0f' % waarde:>5}   %.2f: {'%.2f' % waarde}")

print("\n== 3. precies de helft: naar het EVEN getal ==")
for waarde in [0.5, 1.5, 2.5, 3.5, 4.5]:
    print(f"  {waarde!r:>5}  ->  %.0f  geeft  {'%.0f' % waarde}")

print("\n== 4. en de kleine lettertjes van binair ==")
for waarde in [0.125, 0.375, 2.675, 1.005]:
    print(f"  {waarde!r:>7}  ->  %.2f geeft {'%.2f' % waarde:>7}    "
          f"als 20 cijfers: {waarde:.20f}")

print("\n== 5. dezelfde regels in een f-string ==")
print(f"{duur:.2f}   {0.5:.0f}   {2.675:.2f}")

print("\n== 6. in logging: de logger vult zelf in ==")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("demo")
logger.info("duur=%.2fs, tokens=%d", 1.23456, 53)
logger.info("een fout in de plaatshouders stopt het programma NIET:")
logger.info("duur=%.2fs", "geen getal")
print("...en hier draait het gewoon door.")
