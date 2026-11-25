> 🚧 **Status: active development.** It works for the author; interfaces may change.

# Turkish Model Catalog

A source-backed catalog of **190 Turkish-relevant language-model, speech (ASR/TTS), NLP, dataset and benchmark entries**, with one research card per entry (what the developer claims, how it was trained, how to try it, independent evidence, open questions, source links), plus a single offline HTML page to browse it. The page and data are in Turkish.

How this differs from [jev-teknik-arastirma](https://github.com/KemalG-u/jev-teknik-arastirma): that repository is a single write-up on one provider's decision API; this one is a broad catalog of Turkish-relevant models, datasets and benchmarks, with one research card per entry.

Türkçe sürüm: [README.tr.md](README.tr.md)

> **Snapshot: data collected October 2026; licenses and benchmark claims not re-verified.**
> Nothing here was downloaded, run or benchmarked by the author. A card records what a source says and how far that claim could be checked, not a quality ranking.

## Why this exists

Turkish model information is scattered across Hugging Face cards, blog posts, papers and vendor pages, and the same name often covers several different releases. This project collects them in one place, separates models from products, datasets and tools, and keeps every claim attached to its source so you can see what is evidence and what is marketing.

## What is in the repository

| Path | What |
|---|---|
| `sayfalar/TURKCE-MODEL-LABORATUVARI.html` | The generated, self-contained catalog page (open it in a browser; no network needed) |
| `sayfalar/turkce-model-laboratuvari.template.html` | Page template with placeholders for the data |
| `arastirma/katalog.json` | The original 190-entry catalog (name, URL, developer, license note, date, old notes) |
| `arastirma/tam-tarama/*-sonuc.json` | Research cards in eight batches (`*-girdi.json` are the batch inputs) |
| `arastirma/eleme-kararlari.json` | Entries removed from the active view (abandoned or withdrawn) and replacements, each with evidence URLs |
| `arastirma/depo-kimlikleri.json`, `metin-ilk-tur.json`, `ses-ilk-tur.json` | Repository revisions and first-pass notes used by the page generator |
| `arastirma/*.py`, `*.js`, `*.cjs` | Generation and validation scripts |

Card status counts in this snapshot: 44 documented, 88 limited, 5 identity/access unresolved, 53 non-model sources (datasets, tools, papers, products). These are research states, not performance scores. The old A-D labels inside the original catalog notes are narrow task-fit labels from the author's earlier use case, not a general quality ranking.

## Quick start

Browse: open `sayfalar/TURKCE-MODEL-LABORATUVARI.html` in a browser.

Regenerate and validate the page (Python 3, Node.js for the syntax check):

```bash
python arastirma/sayfa-uret.py      # rebuilds sayfalar/TURKCE-MODEL-LABORATUVARI.html from the JSON
python arastirma/sayfa-dogrula.py   # counts, links, original-catalog equality, JS syntax check
```

In this snapshot the regenerated page is byte-identical to the shipped one, and `sayfa-dogrula.py` passes.

To work from the author's original catalog HTML instead of `katalog.json`, set `MODEL_CATALOG_HTML` to its path (it must contain a `<script id="veri" type="application/json">` block); the validator then also checks its SHA-256.

## Requirements

Python 3 (standard library only for the commands above) and Node.js (for `sayfa-dogrula.py`'s syntax check). No third-party packages.

## Limits and unverified claims

- **Snapshot, not live.** Data was collected in October 2026. Licenses, release dates, benchmark numbers and availability may have changed; none were re-verified for this release.
- **Cards are not benchmarks.** No model was downloaded or run. "Documented" means the sources were readable and consistent, not that the model is good.
- **Raw source extracts are not included.** The cached third-party page texts and per-record fetch dossiers used while researching were removed from this repository (third-party content, possible personal data such as contact addresses and forum usernames). `kaynak-topla.py`, `kaynak-ek.py`, `destek-kaynaklari.py`, `destek-kartlari.py` and `eleme-uygula.py` need those fetched files and the network; they are kept as documentation of the method and will not run as-is from this repository. The batch inputs reference the removed folders with relative paths.
- **The page was only machine-checked.** The data checks and JavaScript syntax pass; a visual and interaction check in a real browser was not completed (the earlier check was blocked by `file://` browser policy).
- Some catalog notes (the original `gerekce` field) mention the author's former task labels such as "YEREL-LM"; they are kept verbatim because the validator compares the catalog to the original.
- The catalog text is Turkish; entry names, URLs and model identifiers are as published by their authors.

## License

- Data and text compiled by the author (catalog, cards, selection decisions, page text): [CC BY 4.0](LICENSE-DATA).
- Code (scripts and the page template/generator): [Apache-2.0](LICENSE).
- Information about third-party models, datasets and papers is summarized from, and linked to, the sources listed on each card; those works keep their own licenses and terms. See [THIRD-PARTY.md](THIRD-PARTY.md).

## Contributing

Corrections with a source link are welcome as issues. See [SECURITY.md](SECURITY.md) for security reports.
