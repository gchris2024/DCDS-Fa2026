# Holinshed Name Files

These CSV files were created from the 1577 Holinshed index, `1577 Files/Index.xml`. The process cleaned old printing features such as the long `s` and line-break markers, identified the name in each index entry, classified it, and removed entries that were topics rather than names.

## `holinshed_names.csv`

This is the detailed file. It has one row for each retained index entry. It includes:

- the extracted name and its type (`person`, `place`, `group`, or `uncertain`)
- the confidence score and the evidence used for the classification
- the index letter and page references
- both cleaned and original versions of the entry

## `holinshed_names_unique.csv`

This is the grouped file. It combines likely spelling or capitalization variants into one name. It records the number of entries, the variants that were combined, the index letters, and an example entry.

In short, `holinshed_names.csv` shows every individual index entry, while `holinshed_names_unique.csv` shows the consolidated list of distinct names.

The full methodology is documented in `method_notes.md`.
