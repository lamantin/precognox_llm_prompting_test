# Hogyan jutottunk el a kész megoldásig (kérdés–válasz)

## K: Mi volt a próbafeladat célja?
V: Egy terminálos (TUI) szótanuló app MVP elkészítése, ahol a tanuló szabad szöveges választ ír,
és egy „AI tanár” szemantikusan (jelentés alapján) értékeli azt, részpontszámmal és hasznos visszajelzéssel.

## K: Miért Python lett a választás?
V: Gyors MVP-fejlesztéshez ideális, tiszta architektúrát lehet vele tartani (UI / domain / storage / AI adapter),
és könnyen kezelhető a terminálos UI (Rich), valamint a HTTP integráció (requests).

## K: Miért nem OpenAI API-t használunk?
V: Mert az fizetős. Olyan alternatívát kerestünk, ami ingyenes kvótával fejlesztésre alkalmas,
és mégis OpenAI-kompatibilis API-t ad.

## K: Milyen LLM-et választottunk helyette?
V: **GitHub Marketplace Models** alól az **Azure OpenAI `o4-mini`** modellt:
https://github.com/marketplace/models/azure-openai/o4-mini

## K: Hogyan kapcsolódik a program a GitHub Models-hoz?
V: HTTP POST hívással az Azure OpenAI-kompatibilis végpontra:
`https://models.inference.ai.azure.com/chat/completions`
A hitelesítés Bearer tokennel történik (`GITHUB_TOKEN`).

## K: Hogyan biztosítjuk, hogy a TUI stabilan tudja renderelni a választ?
V: A modelltől **szigorúan JSON** választ kérünk egy rögzített sémával:
- verdict: correct|partial|incorrect
- score: 0–100
- feedback: 1–3 rövid pont
- improved_answer: rövid mintaválasz
- key_points_missing: lista
- persona_line: rövid szerep-komment (opcionális)

## K: Milyen architektúrát használ az MVP?
V: Réteges, egyszerű, tesztelhető felépítést:
- `ui/` – terminál képernyők és interakció
- `domain/` – alap modellek (Word)
- `storage/` – deck betöltése (JSON)
- `ai/` – LLM adapter (GitHub Models / o4-mini)

## K: Mit jelent a persona ebben az appban?
V: Csak a stílust/tónust változtatja (pl. neutral/funny/professor), **nem** változtathatja az értékelési kritériumokat.

## K: Mi történik, ha az AI hívás elbukik?
V: A program hibaüzenetet mutat, és a session attól még tovább működik (graceful fallback).

## K: Mi volt a fejlesztés lépésről lépésre?
V:
1) Projekt skeleton + Rich alapú terminál UI
2) Deck (JSON) és betöltés (repository)
3) Practice loop (kérdez–válasz–értékel–feedback)
4) AI adapter réteg GitHub Models (o4-mini) integrációval
5) Strukturált JSON kimenet kényszerítése + hibakezelés
6) Dokumentáció (README + ez a Q&A)

## K: Mitől “leadás-kész” ez MVP-ként?
V: Teljesíti az acceptance criteria-t: deck kezelhető helyben, terminálos gyakorlás működik,
az AI szemantikusan értékel, persona stílust ad, és hibatűrő a működés.
