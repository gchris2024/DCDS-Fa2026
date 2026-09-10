# DCDS Factoidal Prosopography

Preliminary work for Fall 2026.

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

## Repository File Tree

```text
.
|-- 1577 Files/             # Primary 1577 Holinshed XML files and regnal records
|   |-- RegnalFiles/
|   |   |-- HenryFirst.xml
|   |   |-- HenrySecond.xml
|   |   |-- KingStephen.xml
|   |   |-- WilliamConqueror.xml
|   |   `-- WilliamRufus.xml
|   |-- 1577_working.xml
|   |-- Description_Britain.xml
|   |-- Errata.xml
|   |-- History_Ireland.xml
|   |-- History_Scotland.xml
|   |-- Index.xml
|   |-- README.md
|   `-- Regnal_Years.xml
|-- 1587 files/             # 1587 edition source XML
|   `-- 1587 copy.xml
|-- file_drawer/            # Junk drawer
|   |-- Holinshed - Disambiguated Person Names.csv
|   |-- holinshed_disambiguated.csv
|   `-- holinshed_nameList.csv
|-- name_extraction/        # Name extraction scripts, GUI launcher, results, and notes
|   |-- EntityNames/
|   |   |-- holinshed_names.csv
|   |   |-- holinshed_names_unique.csv
|   |   `-- method_notes.md
|   |-- gui_launcher/
|   |   |-- extract_names_gui.py
|   |   |-- README.md
|   |   |-- run_extract_names_gui.bat
|   |   |-- run_extract_names_gui.command
|   |   `-- run_extract_names_gui.sh
|   |-- output/
|   |   |-- holinshed_elizabeth_excerpt_analysis_s_name_contexts.csv
|   |   |-- Holinshed_vol1_book1_name_contexts.csv
|   |   |-- Holinshed_vol3_book3_name_contexts.csv
|   |   |-- multiple_names_contexts.csv
|   |   `-- name_contexts.csv
|   `-- extract_names.py
|-- .gitignore
|-- Holinshed Proposal.md
|-- monarchs_reign.xml
|-- README.md
|-- requirements.txt
`-- run.sh
```
