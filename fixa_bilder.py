# Döper om inklistrade bilder (image.png, image-2.png ...) i notebooken till bild01.png, bild02.png ...
# så att varje bild får ett eget namn. Annars blir bilderna likadana i PDF-exporten.
#
# Användning (spara notebooken i VS Code först!):
#     py fixa_bilder.py                  -> fixar logistiklabb.ipynb
#     py fixa_bilder.py annan.ipynb      -> fixar en annan notebook
# Ladda sedan om notebooken från disk i VS Code (Ctrl+Shift+P -> "File: Revert File").

import json, re, sys

sys.stdout.reconfigure(encoding="utf-8")
fil = sys.argv[1] if len(sys.argv) > 1 else "logistiklabb.ipynb"
nb = json.load(open(fil, encoding="utf-8"))

# hitta högsta bildnummer som redan används
nr = 0
for cell in nb["cells"]:
    for namn in cell.get("attachments", {}):
        m = re.fullmatch(r"bild(\d+)\.\w+", namn)
        if m:
            nr = max(nr, int(m.group(1)))

# döp om alla bilder som inte redan heter bildNN, i den ordning de syns i texten
antal = 0
for cell in nb["cells"]:
    bilder = cell.get("attachments", {})
    if not bilder:
        continue
    text = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
    for gammalt in re.findall(r"attachment:([^)\s]+)", text):
        if re.fullmatch(r"bild\d+\.\w+", gammalt) or gammalt not in bilder:
            continue
        nr += 1
        nytt = f"bild{nr:02d}" + gammalt[gammalt.rfind("."):]
        bilder[nytt] = bilder.pop(gammalt)
        text = text.replace(f"![{gammalt}](attachment:{gammalt})", f"![{nytt}](attachment:{nytt})")
        text = text.replace(f"attachment:{gammalt})", f"attachment:{nytt})")
        print(f"{gammalt} -> {nytt}")
        antal += 1
    cell["source"] = text

if antal == 0:
    print("Inga bilder behövde döpas om.")
else:
    json.dump(nb, open(fil, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Klart, {antal} bilder omdöpta. Ladda om notebooken från disk i VS Code.")
