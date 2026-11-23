# DCDS Factoidal Prosopography

Preliminary work for Fall 2026 on the 1577 edition of Holinshed's *Chronicles*.

The repository holds three things: TEI transcriptions of the 1577 text split by
reign, authority lists of people and places extracted from the 1577 index, and
notebooks that count those names across the reigns to find where the chronicle
concentrates its attention.

## Setup

### Create and activate a virtual environment

```bash
python3 -m venv .venv
```

Activate the environment using the command for your shell:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows
source .venv/Scripts/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## The data

### TEI source (`1577_files/`)

`1577_working.xml` is the full working transcription; `Description_Britain.xml`,
`History_Britain.xml`, `History_Scotland.xml`, `History_Ireland.xml`,
`Index.xml` and `Errata.xml` are its major divisions.

Two per-reign views of the English history now exist:

- `regnal_files/` — one file per monarch, `01_WilliamConqueror.xml` through
  `23_Elizabeth.xml`, each with a `<div type="reign">` for that reign
- `monarchs_reign.xml` — all 23 reigns in a single file as
  `<div type="regnal_entry">` elements. Most of the analysis reads this.

### Authority lists (`name_extraction/entity_names/`)

All of these derive from the 1577 index (`1577_files/Index.xml`), which was
cleaned of long `s`, line-break pipes, ligatures and tilde vowels before the
headword of each entry was identified and classified. The method is written up
in `method_notes.md` and `holinshed_names_explanation.md`.

| File | Rows | Contents |
|---|---|---|
| `holinshed_names.csv` | ~8,700 | one row per retained index entry, with type (`person`/`place`/`group`/`uncertain`), confidence, basis for the guess, page refs, cleaned and original entry |
| `holinshed_names_unique.csv` | ~4,800 | the same names consolidated, with spelling variants merged |
| `holinshed_people.csv` | ~2,400 | person names with spelling variants |
| `holinshed_places.csv` | ~950 | place names with spelling variants and confidence |
| `place_aliases.csv` | 41 | old spelling → modern place (`Roan` → `Rouen`, `Caleis` → `Calais`) |


## Repository File Tree

```text
.
|-- 1577_files/                       # 1577 Holinshed TEI source
|   |-- regnal_files/                 # one file per reign, in regnal order
|   |   |-- 01_WilliamConqueror.xml
|   |   |-- 02_WilliamRufus.xml
|   |   |-- 03_HenryFirst.xml
|   |   |-- 04_Stephen.xml
|   |   |-- 05_HenrySecond.xml
|   |   |-- 06_RichardFirst.xml
|   |   |-- 07_John.xml
|   |   |-- 08_HenryThird.xml
|   |   |-- 09_EdwardFirst.xml
|   |   |-- 10_EdwardSecond.xml
|   |   |-- 11_EdwardThird.xml
|   |   |-- 12_RichardSecond.xml
|   |   |-- 13_HenryFourth.xml
|   |   |-- 14_HenryFifth.xml
|   |   |-- 15_HenrySixth.xml
|   |   |-- 16_EdwardFourth.xml
|   |   |-- 17_EdwardFifth.xml
|   |   |-- 18_RichardThird.xml
|   |   |-- 19_HenrySeventh.xml
|   |   |-- 20_HenryEighth.xml
|   |   |-- 21_EdwardSixth.xml
|   |   |-- 22_Mary.xml
|   |   `-- 23_Elizabeth.xml
|   |-- 1577_working.xml              # full working transcription
|   |-- Description_Britain.xml
|   |-- Errata.xml
|   |-- History_Britain.xml
|   |-- History_Ireland.xml
|   |-- History_Scotland.xml
|   |-- Index.xml                     # source of the name authority lists
|   |-- monarchs_reign.xml            # all 23 reigns as regnal_entry divs
|   `-- README.md                     # TEI encoding decisions
|-- name_extraction/
|   |-- entity_names/
|   |   |-- ExtractionProcessFiles/   # index OCR + column-splitting pipeline
|   |   |   |-- build.py
|   |   |   |-- check2.py
|   |   |   |-- final2.py
|   |   |   |-- gut5.py
|   |   |   |-- ocr_all.txt
|   |   |   |-- ocr_raw.zip
|   |   |   `-- README.md
|   |   |-- holinshed_names.csv       # one row per index entry
|   |   |-- holinshed_names_unique.csv
|   |   |-- holinshed_people.csv
|   |   |-- holinshed_places.csv
|   |   |-- place_aliases.csv         # old spelling -> modern place
|   |   |-- holinshed_names_explanation.md
|   |   `-- method_notes.md           # extraction methodology
|   |-- gui_launcher/
|   |   |-- extract_names_gui.py
|   |   |-- run_extract_names_gui.bat
|   |   |-- run_extract_names_gui.command
|   |   |-- run_extract_names_gui.sh
|   |   `-- README.md
|   |-- output/                       # extracted name contexts
|   |   |-- Holinshed_vol1_book1_name_contexts.csv
|   |   |-- Holinshed_vol3_book3_name_contexts.csv
|   |   |-- holinshed_elizabeth_excerpt_analysis_s_name_contexts.csv
|   |   |-- multiple_names_contexts.csv
|   |   `-- name_contexts.csv
|   |-- count_places.py               # shared normalization + counting
|   `-- extract_names.py
|-- notebooks/
|   |-- places_1577.ipynb             # places across reigns + hot spots
|   |-- places_per_reign.ipynb        # per-reign top places + spike ranking
|   |-- places_by_regnal.ipynb        # deprecated
|   |-- spikes_edward_scotland.ipynb  # Scotland spike in Edward I
|   `-- top_place_by_monarch.ipynb
|-- .gitignore
|-- Holinshed Proposal.md
|-- README.md
|-- requirements.txt
`-- run.sh                            # launches the name-extraction GUI
```
