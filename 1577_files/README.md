# Regnal README

Coding decisions:

- All of the TextComparator attributes and values have been removed from individual ruler files in order to make sense of what is going on. 
- All div 1, 2, 3, etc. have been changed to div
- A running list of div types:
    -  For front matter, engraved title page, illustration, preface
    - For body, history, reign
    - for back matter, index, errata
- There are marginal notes that will all need to be placed on the right side of the page
- There are pipe `|`symbols that indicate line breaks in the original text; those have been removed
- There are several types of `hi` tags throughout the text that 'mean' different things.
    - I have decided (07/25/2026) that:
        -  hi tags that appear in a marginal note should be rendered in bold
        - hi tags that refer to text in another language should be rendered in italics

To remove the TextComparator code for HTML conversion, use regular expression:

Find:

```
<p\s+xmlns(?::ns0)?="[^"]*"\s+ns0:cid="[^"]*"\s*>
```
Replace with 
```
<p>
```

