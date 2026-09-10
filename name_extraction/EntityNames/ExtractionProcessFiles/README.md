# Plumer Index — processing pipeline

## What Tesseract did and did not do

Tesseract did **not** produce the CSV. Every row in `Plumer_Biographies_Index.csv`
was read visually from a magnified column crop. Tesseract ran as an independent
second opinion so that disagreements between it and my reading could be flagged
and re-examined at higher magnification.

This mattered. On this 19th-century type Tesseract misread digits often enough
that its output was not usable as data. Real examples from this run:

| Entry | Tesseract | Correct |
|---|---|---|
| `Morris, Lewis, 1797` | 655 | 685 |
| `Freeman, Jonathan, 1808` (Adams row) | 4389 | 439 |
| `Anawon, 1676` | 397 | 327 |
| `Bacon, Nathaniel, 1617` | 384 | 334 |
| `Wyllis, Samuel, 1823` | 1828 | 1823 |
| `Adams, John` | "Adains" / "Adaumns" | Adams |

Where the two disagreed I re-cropped the specific row at 2–3x and read it
directly rather than trusting either source.

## Order of operations

1. **`gut5.py`** — column-splitting. Finds the gutter between the two printed
   columns on each page and writes `gutters.json`.

   This was the hard part. The naive approach fails because on many pages the
   gap between the *Vol.* and *Page.* number columns is wider than the gutter
   between the two text columns, so the split lands mid-column and silently
   truncates the page numbers. The working method profiles ink only in the
   lower table region (excluding headers), finds the two dense name blocks,
   and cuts just left of the second one. Pages 4 and 23 need different row
   windows — page 23 is mostly blank, so the default assumption breaks; see
   `ROWFRAC` in the script.

2. **`final2.py`** — writes two crop sets per page from `gutters.json`:
   - `cols/` — single upscaled column images, fed to Tesseract
   - `read/` — the same columns split top/bottom and set side by side, sized
     to ~1560px for visual reading

   Left columns for pages 10–22 were later regenerated with an extra 45px of
   right margin; page 9 had been clipping the final digit of the page numbers.

3. **The Tesseract pass** was a shell loop, not a Python script:

   ```bash
   mkdir -p ocr
   for f in cols/*.png; do
     b=$(basename "$f" .png)
     tesseract "$f" "ocr/$b" --psm 6 2>/dev/null
   done
   ```

   `--psm 6` (assume a uniform block of text) is the right mode here — the
   crops are already single columns, so Tesseract's own layout analysis only
   gets in the way. Output is in `ocr_raw/` (46 files, one per column).

4. **`check.py` / `check2.py`** — crop validation. These call Tesseract via
   `subprocess` and check what fraction of lines match the expected
   `Name, Year, Vol Page` shape. This is how the bad splits were caught:
   a left column whose lines never end in two numbers has lost its Page
   column. `check.py` was the first attempt and over-flagged on OCR noise;
   `check2.py` is the one worth reusing.

5. **`build.py`** — assembles the per-page pipe-delimited files into the final
   CSV and runs validation (volume in 1–5, year in range, page bounds,
   duplicates, alphabetical continuity across page boundaries).

## Note on the other scripts

The working directory also held about fifteen dead ends — `crop.py` through
`crop4.py`, `gaps.py`/`gaps2.py`/`gaps3.py`, `gut.py`/`gut2.py`/`gut4.py`,
`mkcrops.py`, `fix1.py`/`fix2.py`, `prof.py`. Those were successive failed
approaches to gutter detection and are not included. `gut5.py` + `final2.py`
supersede all of them.
