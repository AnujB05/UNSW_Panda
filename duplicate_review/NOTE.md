# Duplicate review — manual resolution required

Nine duplicate groups had **genuinely different content** across their copies, so
per CLAUDE.md rule 3 no version was silently picked. Every version is here under
its **original name**. Resolve each group, move the winner to its target folder
(listed below), and delete the rest.

Sizes/hashes as of the 2026-08-20 scan. Nothing was moved or deleted from Downloads.

---

## 1. `a2a_temporal_attention_probes*.ipynb` → `notebooks/mechanistic/`
A2a temporal-attention probes = Experiments 37–40 (null overall).

| File | Size | Modified | md5 |
|---|---|---|---|
| `a2a_temporal_attention_probes.ipynb` | 32,554 | 2026-07-13 12:59 | 34d8c393 |
| `a2a_temporal_attention_probes (1).ipynb` | 39,332 | 2026-07-13 13:26 | ff4cecf9 |
| `a2a_temporal_attention_probes (3).ipynb` | 44,779 | 2026-07-13 14:04 | 20443409 |
| `a2a_temporal_attention_probes (2).ipynb` | 54,294 | 2026-07-13 14:48 | 6c0e818a |

⚠️ **Suffix order and mtime order disagree**: `(3)` was modified *before* `(2)`.
By mtime the newest is `(2)`; by suffix it would be `(3)`.

## 2. `g1_correlation_dimension*.ipynb` → `notebooks/rollout_topology/`
G1 — ACTIVE, currently the project's strongest positive lead. Highest-stakes group here.

| File | Size | Modified | md5 |
|---|---|---|---|
| `g1_correlation_dimension.ipynb` | 41,159 | 2026-07-19 21:24 | ddd5ce28 |
| `g1_correlation_dimension (1).ipynb` | 52,976 | 2026-07-19 21:39 | 3c03feee |
| `g1_correlation_dimension (2).ipynb` | 59,287 | 2026-07-19 22:00 | 4d0619df |

Monotonically growing within 36 minutes — most likely successive saves of one
session, so `(2)` is probably current. Not assumed.

## 3. `skew40_distance_test*.ipynb` → `notebooks/mechanistic/`

| File | Size | Modified | md5 |
|---|---|---|---|
| `skew40_distance_test.ipynb` | 72,733 | 2026-07-16 12:45 | 2f2c8083 |
| `skew40_distance_test (1).ipynb` | 86,249 | 2026-07-16 15:20 | af479067 |
| `skew40_distance_test (2).ipynb` | 91,731 | 2026-07-16 15:40 | 8dc98e53 |

## 4. `b3a_chronos_attribution*.ipynb` → `notebooks/mechanistic/`
B3a — active lead, patch-size-alignment candidate.

| File | Size | Modified | md5 |
|---|---|---|---|
| `b3a_chronos_attribution.ipynb` | 62,420 | 2026-07-17 17:12 | 6648f8b6 |
| `b3a_chronos_attribution (1).ipynb` | 66,092 | 2026-07-17 18:42 | 9a2c5130 |

## 5. `b3c_analysis_downsampled_weather*.ipynb` → `notebooks/mechanistic/`
B3c — null.

| File | Size | Modified | md5 |
|---|---|---|---|
| `b3c_analysis_downsampled_weather.ipynb` | 21,654 | 2026-07-14 21:57 | a860b617 |
| `b3c_analysis_downsampled_weather (1).ipynb` | 27,957 | 2026-07-14 22:05 | 24a3decb |

## 6. `experiments_log_new_corrected*.pdf` → `docs/meeting_notes/`
⚠️ **Most important group.** These are renderings of `experiment_log.tex`, the
project's canonical append-only record.

| File | Size | Modified | md5 |
|---|---|---|---|
| `experiments_log_new_corrected.pdf` | 619,038 | 2026-07-16 03:03 | 2efb0ad8 |
| `experiments_log_new_corrected (1).pdf` | 721,659 | 2026-07-23 02:19 | c2983bcf |
| `experiments_log_new_corrected (2).pdf` | 721,659 | 2026-08-20 16:13 | 3c3b3419 |

⚠️ `(1)` and `(2)` are **byte-identical in length but differ in hash** — a real
content edit, not a re-download. Given the log is append-only, a same-length
edit is worth understanding before discarding either.

## 7. `Experiments_log_1*.pdf` → `docs/meeting_notes/`
Earlier generation of the same log.

| File | Size | Modified | md5 |
|---|---|---|---|
| `Experiments_log_1.pdf` | 253,463 | 2026-06-17 00:02 | e1e950a7 |
| `Experiments_log_1 (1).pdf` | 317,981 | 2026-06-22 13:16 | 083cc81e |

## 8. `Claude-Continuing previous conversation*.md` → `docs/chat_transcripts/`

| File | Size | Modified | md5 |
|---|---|---|---|
| `Claude-Continuing previous conversation.md` | 144,248 | 2026-06-17 00:00 | c6f22d23 |
| `Claude-Continuing previous conversation (1).md` | 10,716 | 2026-06-17 19:24 | cfe58472 |
| `Claude-Continuing previous conversation (2).md` | 103,595 | 2026-06-18 01:18 | 67722192 |
| `Claude-Continuing previous conversation (3).md` | 394,220 | 2026-06-19 22:40 | 9118d606 |

Sizes are non-monotonic (`(1)` is 10 KB) — these look like **four different
conversations** that happened to export under the same default title, not four
saves of one. Probably all four should be kept and renamed, not de-duplicated.
`claude-project-panda/files/Claude-Continuing previous conversation (3).md` is
byte-identical to `(3)` and so is represented by the single copy here.

## 9. `Claude-Understanding nonlinear dynamical systems fundamentals*.md` → `docs/theory_reference/`

| File | Size | Modified | md5 |
|---|---|---|---|
| `…fundamentals.md` | 429,900 | 2026-06-03 03:55 | ad12740e |
| `…fundamentals (1).md` | 477,442 | 2026-06-04 03:19 | e02ab488 |
| `…fundamentals (2).md` | 662,246 | 2026-06-14 02:35 | daca1f6b |
| `…fundamentals (3).md` | 662,231 | 2026-06-19 23:00 | a07fddf6 |

⚠️ `(3)` is **15 bytes SMALLER** than `(2)` despite being 5 days newer — so `(3)`
is not simply `(2)` plus more conversation. Likely the same growing chat exported
twice with a small formatting difference, but worth a diff before discarding `(2)`.
`claude-project-panda/files/…(3).md` is byte-identical to `(3)`, represented here once.
