"""Count place mentions per reign in the 1577 Holinshed, matching old spellings.

    from count_places import load_texts, load_places, count_names
    texts = load_texts("1577_files/regnal_files")
    counts = count_names(load_places("name_extraction/entity_names/holinshed_places.csv"), texts)
"""
import glob
import os
import re
import unicodedata

import pandas as pd
from lxml import etree

TEI = "http://www.tei-c.org/ns/1.0"
ALIASES_CSV = os.path.join(os.path.dirname(__file__), "entity_names", "place_aliases.csv")
# "Duke of Yorke", "Bishop of London": titles name people, not places
TITLES = re.compile(r"\b(?:arch)?(?:duke|duches|earle|erle|countesse|marques|bishop|abbot)s? of \w+", re.IGNORECASE)


def norm(word):
    """Spelling key for one word: Normãdye -> Normandi, VVestmynster -> Westminster."""
    word = word.replace("ã", "an").replace("õ", "on").replace("ẽ", "en").replace("ũ", "un")
    word = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode()
    key = word.lower().replace("vv", "w").replace("j", "i").replace("v", "u").replace("y", "i")
    key = re.sub(r"au(?=n)", "a", key)
    key = re.sub(r"(.)\1", r"\1", key)
    key = re.sub(r"e$", "", key)
    return key.capitalize() if word[:1].isupper() else key


def norm_text(text):
    return re.sub(r"[^\W\d_]+", lambda m: norm(m.group()), text)


def load_texts(path):
    """{reign: text}. path = folder of per-reign TEI files, or the single monarchs_reign.xml."""
    texts = {}
    if os.path.isfile(path):
        root = etree.parse(path).getroot()
        etree.strip_elements(root, f"{{{TEI}}}note", with_tail=False)
        for div in root.iterfind(f".//{{{TEI}}}div[@type='regnal_entry']"):
            texts[div.get("n")] = re.sub(r"\s+", " ", " ".join(div.itertext()).replace("ſ", "s"))
        return texts
    for f in sorted(glob.glob(os.path.join(path, "*.xml"))):
        root = etree.parse(f).getroot()
        etree.strip_elements(root, f"{{{TEI}}}note", with_tail=False)
        body = root.find(f".//{{{TEI}}}body")  # skip the TEI header
        reign = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", os.path.basename(f)[3:-4])  # HenryFirst -> Henry First
        texts[reign] = re.sub(r"\s+", " ", " ".join(body.itertext()).replace("ſ", "s"))
    return texts


def load_places(csv, min_confidence=0.75):
    df = pd.read_csv(csv)
    return df[df["confidence"] >= min_confidence].sort_values("confidence", ascending=False)


def label(name):
    """Index spelling -> display: VVestminster -> Westminster, york -> York."""
    name = name.replace("VV", "W").replace("Vv", "W")
    return name[:1].upper() + name[1:]


def count_names(df, texts, strip_titles=False, aliases=ALIASES_CSV):
    """Mentions per reign for each name in df (columns: name, spelling_variants), rows ordered by priority.

    aliases: CSV (variant,modern) naming spellings that are the same place; their rows are summed.
    """
    def spellings(name, variants):
        # A one-word variant of a multi-word name ("Henry" for "Henry Lord Percie") would match every Henry
        keep = [v.strip() for v in variants.split("|") if v.strip() and (" " not in name or " " in v.strip())]
        return "|".join([name, *keep])
    df = df.assign(spellings=[spellings(n, v) for n, v in zip(df["name"], df["spelling_variants"].fillna(""))])
    # Rows with the same spelling key become one name, labelled by the first row
    df = df.groupby(df["name"].map(norm_text).str.lower(), sort=False).agg(
        name=("name", "first"), spellings=("spellings", "|".join)
    )

    def pattern(spellings):
        keys = sorted({norm_text(s.strip()).lower() for s in spellings.split("|") if s.strip()}, key=len, reverse=True)
        # One-word names need a capital (skips "seeme", "mercy"); multi-word names ignore case
        return re.compile(r"(?<!\w)(?:" + "|".join(
            f"(?i:{re.escape(k)})" if " " in k else k[0].upper() + f"(?i:{re.escape(k[1:])})" for k in keys
        ) + r")(?!\w)")
    patterns = {label(row["name"]): pattern(row["spellings"]) for _, row in df.iterrows()}
    normed = {r: norm_text(TITLES.sub("", t) if strip_titles else t) for r, t in texts.items()}
    counts = pd.DataFrame({r: {n: len(p.findall(t)) for n, p in patterns.items()} for r, t in normed.items()})
    if aliases:  # different spellings of one place were counted on separate rows: add them up
        modern = pd.read_csv(aliases).set_index("variant")["modern"]
        counts = counts.groupby(lambda n: modern.get(n, n)).sum()
    return counts
