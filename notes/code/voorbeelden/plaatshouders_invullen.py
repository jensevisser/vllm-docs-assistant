"""Waar komen de waarden vandaan die in %s en %.2f terechtkomen?
Draai: uv run python notes/code/voorbeelden/plaatshouders_invullen.py
"""

import logging

print("== 1. % is een operator, net als + ==")
print("3 + 4        ->", 3 + 4)
print("'%.2f' % 3.14159 ->", "%.2f" % 3.14159)
print("links de tekst met gaten, rechts de waarde, eruit komt:", type("%.2f" % 3.14159))

print("\n== 2. de volgorde bepaalt alles ==")
print("%s is %d jaar" % ("Jense", 53))
print("%s is %d jaar" % ("Jense", 54))
print("eerste gat <- eerste waarde, tweede gat <- tweede waarde")

print("\n== 3. één waarde, of een tuple ==")
print("%s"       % "ok")            # één waarde mag los
print("%s"       % ("ok",))         # ...maar dit is hetzelfde, en veiliger
print("%s na %.1fs" % ("ok", 2.25)) # meer dan één: altijd een tuple

for tekst, waarden in [("%s %s", ("a",)), ("%s", (1, 2))]:
    try:
        print(f"  {tekst!r} met {waarden!r} ->", repr(tekst % waarden))
    except TypeError as e:
        print(f"  {tekst!r} met {waarden!r} -> TypeError: {e}")

print("\n== 4. een eigen mini-logger: wie vult er in? ==")

def mijn_log(tekst, *waarden):          # *waarden = alles wat er nog achteraan komt, als tuple
    print("  ik kreeg de tekst :", repr(tekst))
    print("  ik kreeg de waarden:", waarden)
    print("  ik vul zelf in     :", tekst % waarden)

mijn_log("duur=%.2fs tokens=%s", 1.23456, None)

print("\n== 5. en zo doet logging het echt ==")
record = logging.LogRecord(
    name="demo", level=logging.INFO, pathname="bestand.py", lineno=1,
    msg="duur=%.2fs tokens=%s", args=(1.23456, None), exc_info=None,
)
print("  record.msg  :", repr(record.msg))
print("  record.args :", record.args)
print("  getMessage():", record.getMessage())
