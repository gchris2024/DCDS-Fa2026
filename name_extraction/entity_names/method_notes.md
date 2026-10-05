# Name extraction from the Holinshed *Chronicles* index — method notes

## What the source is

`Index.xml` is a TEI encoding of *A Table ſeruing vnto both parts of the Chronicles of England* — the index to the 1577 Holinshed. It contains:

- 10,320 `<item>` elements, grouped into 23 `<list>` elements (A–Z, no J, U or X)
- 436 `<gap>` elements marking illegible letters or words
- `<hi rend="sup">` for superscripts (mostly the `e` of `y{e}` = *the*)
- `<pb>` page breaks; a `<head>` per section

Each item is a headword plus a gloss plus one or more references, e.g.
`Abbey of Peterburgh & Crow|land ſpoyled by King Iohn. 604.73.`

## Text normalisation

Before anything else, each entry was regularised for matching. The original spelling is preserved in the output as a separate column.

| Feature | Treatment |
|---|---|
| Long s `ſ` | → `s` |
| `\|` | Deleted — it marks a line-break in the printed column, not a hyphen (`Crow\|land` → `Crowland`) |
| `VV`, `vv` | → `W`, `w` (typographic double-v for W) |
| Ligatures `ﬁ ﬀ`, tilde vowels `ẽ õ` | Expanded (`ẽ` → `en`, `õ` → `on`) |
| `<gap>` | Replaced with `<?>` so the loss is visible rather than silently closed |
| Whitespace | Collapsed |

No attempt was made to modernise spelling in the `name` column. `Cantorburie`, `Northfolke` and `Egelredus` are left as printed, because normalising them would mean guessing at identifications the index does not make.

## Step 1 — Splitting the entry

Each entry divides into a **head** (the name and its gloss) and **references** (page and line numbers). The split point is the first numeral, with one exception: numerals preceded by *the*, *y{e}* or a royal name are regnal numbers, not references, so `Henry the .4 pag. 1129` splits after `4`, not before it. References go into their own column.

## Step 2 — Finding the name

The headword is normally the first token, but the index frequently inverts (`Bucke Iohn attainted`, `Stanley Thomas Lorde Stanley`) and frequently extends (`Bamborrough Castle`, `Ile of Wight`, `Newcastle vpon Tyne`). The name phrase therefore grows rightward from token one while the next token is:

- capitalised **and** either a known forename, a place-type word, or absent from an English dictionary; or
- a connective (`of`, `de`, `le`, `vpon`, `fitz`, `ap`, `saint`) followed by a capitalised word; or
- a place-type word in any case (`Suale riuer`, `Bosworth feeld`)

and stops at a lowercase verb, a comma, or seven tokens. Trailing prepositions are then trimmed, so `Ipswich in` becomes `Ipswich`.

## Step 3 — Corpus-internal evidence

This is the part that does the real work, and it is worth explaining at length.

A name's own entry is often too thin to classify — `Selwood. 214.80` says nothing. But every name recurs across the index in other people's entries, and *those* contexts are informative. So every capitalised token in all 10,320 entries was indexed (11,311 distinct tokens after spelling-normalisation), recording how often it appears:

| Signal | Pattern | Reads as |
|---|---|---|
| `placeword_of` | *citie of X*, *riuer of X* | place |
| `loc_prep` | *at X*, *in X*, *from X*, *neere X* | place |
| `place_head` | *X castle*, *X shire* | place |
| `title_of` | *Duke of X*, *Byshop of X* | place (territorial) |
| `place_verb` | *X besieged / brent / situate* | place |
| `forename_adj` | *Iohn X* or *X Iohn* | person |
| `title_adj` | *king X*, *sir X* | person |
| `kin` | *X his sonne*, *X hir daughter* | person |
| `bio` | *X dyeth / slayne / maryed* | person |
| `pers_verb` | *X* + any `-eth` verb | person |

The results are strikingly clean. `london`: 70 locative prepositions, 50 *citie of*, 0 personal-name adjacencies. `becket`: 66 forename adjacencies, nothing locative. `gray`: 23 forename adjacencies. Evidence is always taken from the **head token of the entry**, never the most-evidenced token in the phrase — an early version read `Sroope Archbyshoppe of Yorke` off *Yorke* and called it a place.

Two other counts were kept per token: how often it appears capitalised **mid-entry**, and how often lowercase. See step 5.

## Step 4 — Classification

Person and place scores accumulate from three sources, then compete.

1. **Inside the name** — a forename (+3.0), a place-type word (+3.0), a title of rank (+2.5), a title governing a place as in *Vicount of Melune* (+2.0).
2. **Corpus evidence** — the ratio of place-signals to person-signals from step 3, scaled by how much evidence exists, capped at 4 points so a name seen twice cannot outweigh direct textual evidence.
3. **Local context** — the five tokens after the name, weighted double for the first two, plus whole-entry patterns: kinship language, appointment to office (*ordeyned Byshop*), biographical events (*dyeth*, *beheaded*, *attainted*), citation as an author (*cited*, *writeth*), locative glosses (*where they inhabite*), etymological glosses (*what it signifieth in the Britishe tongue*), and location within a named region.

The higher score wins. If the margin is under 1.0 the row is marked `uncertain` rather than guessed at. Confidence is derived from the margin as a proportion of total score, plus a small bonus for evidence volume, capped at 0.97.

Two special cases: ethnonyms (*Danes*, *Britaines*, *Londoners*, *Welchmen*) are typed `group`, and cross-reference entries (`Osrec a Dane, looke Basreeg`) inherit the type of the entry they point to when that entry is well-evidenced.

## Step 5 — Filtering out non-names

About a fifth of the index consists of subject headings, not names: *Rebellion moued by Robert*, *Policie of Maximianus*, *Discipline of the Church*. Three tests, applied **after** scoring so that strong evidence can override them:

1. **The casing test.** A word that appears mid-entry in lowercase but never capitalised is a common noun. `policie` occurs lowercase 5 times, capitalised 0. `treason` 43 to 2. `kent` 0 to 84, `london` 0 to 217. This is the single most reliable discriminator, and it is derived from the document itself rather than imported.
2. **A dictionary check**, deliberately demoted to a supporting role. Webster's-derived word lists contain *cadwallader*, *hubba*, *howel*, *edgar* and *kent*, so dictionary membership alone was dropping real people; it now only counts when the casing test is also silent.
3. **A curated stoplist** of 179 abstract nouns common in this index (*parliament*, *subsidie*, *othe*, *iustes*, *sinode*, *fifteenes*), overridden when the phrase contains a forename or *of* + a genuine proper noun — so *Parliament.* is dropped but *Battel of Algeberota* is kept.

Entries whose head is a bare office with no name attached (*Ambassadours sent from Rouen*) are also dropped, while *Queene Katharin* is kept.

1,616 entries were removed this way.

## Results

| | |
|---|---|
| Entries in the index | 10,320 |
| Rows in output | 8,704 |
| Unique names after variant-grouping | 4,787 |
| person / place / group / uncertain | 5,447 / 1,518 / 727 / 1,012 |
| confidence ≥ 0.75 / 0.5–0.75 / < 0.5 | 7,265 / 427 / 1,012 |

Hand-checked against a random sample of 60 rows, roughly 90% of the confident type assignments were correct.

## Known limitations

- **Titles are genuinely ambiguous.** *Yorke*, *Northumberland* and *Chester* denote both a territory and the man who holds it, and the index uses them both ways. These lean `person` when the entry describes an action and `place` when it describes the territory, but a portion will be wrong either way.
- **Only the first name in an entry is captured.** `AAron and Iulius, martyred` yields *AAron* alone.
- **Institutions are typed `place`.** *Bury Abbay*, *Cantorbury Colledge* — defensible, but they are organisations as much as locations.
- **Spelling variants are grouped by a normalisation heuristic** (i/j, u/v, y/i, doubled letters, final -e), which will occasionally merge two distinct names or fail to merge one name.
- **`uncertain` rows are mostly terse entries** — bare cross-references and one-line stubs with no verb to read.
- The `basis_for_guess` column names the signals that fired, so any individual row can be checked against the reasoning that produced it.

## Files

- `holinshed_names.csv` — one row per index entry, with normalised and original entry text
- `holinshed_names_unique.csv` — consolidated names with spelling variants, entry counts and an example
