# Obyčejná nejmenších čtverců (OLS) regresní analýza

## 1. Úvod do regresní analýzy

(... beze změn ...)

---

## 3. OLS jako alternativa experimentu

### Cíle kapitoly:

- Porovnat OLS s experimentálními metodami výzkumu.
- Diskutovat výhody a omezení OLS v kontextu kauzální inferenční analýzy.
- Identifikovat situace, ve kterých může OLS nahradit experimenty.

### Obsah kapitoly:

Experimentální metody umožňují přímé testování kauzálních vztahů prostřednictvím náhodného přiřazení jedinců do kontrolních a experimentálních skupin. V případech, kdy experiment není proveditelný z etických, praktických nebo finančních důvodů, může OLS sloužit jako alternativa pro analýzu vztahů mezi proměnnými.

Při správném nastavení a kontrole **významných proměnných** může OLS poskytnout odhady blízké těm, které by byly získány experimentální metodou. Klíčovým předpokladem je absence zkreslení způsobeného endogenitou, což lze částečně řešit zahrnutím kontrolních proměnných nebo využitím přirozených experimentů.

### Shrnutí: OLS vs. experiment

| Kritérium                            | OLS regresní analýza                                          | Experimentální metoda (RCT)                                  |
|--------------------------------------|---------------------------------------------------------------|----------------------------------------------------------------|
| Kauzalita                            | Indirektní – vyžaduje silné předpoklady                      | Přímá – založená na randomizaci                               |
| Náhodné přiřazení                    | Ne                                                            | Ano                                                           |
| Kontrola proměnných                 | Statistická (pomocí kontrolních proměnných)                  | Experimentální (manipulace a kontrola)                        |
| Možnost aplikace                    | V případech, kdy experiment není možný                       | Pokud je možné intervenovat a randomizovat                    |
| Riziko zkreslení                    | Vyšší – endogenita, omitnuté proměnné                        | Nižší – pokud je dodržena metodologie                         |
| Náklady a etika                     | Nízké, často pozorovací data                                 | Vyšší náklady, etická omezení                                 |
| Generalizovatelnost                 | Vyšší – často větší a rozmanité datasety                     | Nižší – omezeno na konkrétní experimentální populaci          |

### Poznámky:

- OLS může přiblížit výsledky experimentů, pokud jsou splněny důležité předpoklady (např. exogenita nezávislých proměnných).
- Na rozdíl od experimentů nemůže OLS vždy jednoznačně prokázat kauzalitu, ale může ji silně naznačovat.
- Techniky jako instrumentální proměnné nebo rozdíly v rozdílech (difference-in-differences) mohou posílit validitu kauzální inferenční analýzy založené na OLS.

---

