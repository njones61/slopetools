# Rocscience RS2 (SSRM) Corpus

The [RS2 Slope Stability Verification Manual](https://www.rocscience.com/help/rs2/verification-theory/verification-manuals)
(Rocscience) publishes 68 slope stability problems in Parts I–III, and a separate, later
Part 4 manual (© 2021) re-verifies 52 Slide2 verification problems by shear strength
reduction. Most rows below verify XSLOPE's FEM/**SSRM** solver against RS2's own SSR column,
which is what the manuals exist to publish; a few verify a published limit-equilibrium
quantity instead and name the column they reproduce. The four summary tables give each
problem's headline comparison, a [match dot](index.md#how-the-match-dots-are-scored) and a
link to the section that builds it. The long-standing SSRM anchors (Griffiths & Lane 1999 and
the feature samples) are on the [SSRM benchmarks page](ssrm.md), and full bibliographic
details for the author-year citations here are on the shared [References](references.md) page.

## Methodology

How the RS2 manuals' problems reach this corpus:

- Geometry and properties come from the manuals' coordinate-labeled figures and the vendor
  `.fez` models; a problem also built in the [Slide2 corpus](rocscience.md) uses that same
  input file.
- Rocscience publishes two RS2 models for many problems, a native rebuild (Parts I–III) and a
  Slide2 import (Part IV), which can differ in their constraints. A row is scored against the
  model its corpus file was built from; the other model's number is labeled as such.
- Elastic constants, tensile caps, the at-rest initial stress (`k0 = 1`) and the flow rule
  (ψ = 0) follow the vendor model; a strength-reduction constraint it states (an SSR search
  polygon, an elastic twin) is carried in the file. Where the published mechanism is deeper
  than the unconstrained one, the row reports both, the deep value under the
  [`min_slip_depth` filter](../fem/overview.md#surficial-skin-failures-and-the-minimum-slip-depth-filter).
- A few rows are verified by limit equilibrium because their published target is an LEM
  quantity: a critical seismic coefficient ([#68](#rs2-68)), an LEM-versus-SRM column
  ([#61](#rs2-61)), a multi-method table or limit-analysis bound ([#51](#p4-vp51),
  [#60](#rs2-60)). Each such row names the column it reproduces.
- `benchmarks/rocscience/build_rs2.py` writes the input files and `make_rs2_figures.py` the
  figures.

## Status

Status terms in the tables below — *covered*, *blocked*, *no lock possible* and the rest —
follow the [shared definitions](index.md#status-terms), and appear in a row's Results or Notes
text rather than in a column of their own. Where a problem cannot be reproduced the row says
why rather than leaving a blank; everything else is built and locked at its tagged mesh.

### Part I (1–34)

<div class="corpus-summary match" markdown>

| # | Match | Problem | Results | Notes |
|---:|:-:|---|---|---|
| [1](#rs2-1) | 🟢 | Simple slope stability assessment | SSRM 0.986 vs RS2 SSRM 0.99 (−0.4%) | |
| [2](#rs2-2) | 🟢 | Non-homogeneous slope | SSRM 1.347 vs RS2 SSRM 1.36 (−1.0%) | |
| [3](#rs2-3) | 🟢 | Non-homogeneous slope with seismic load (0.15g) | SSRM 0.958 vs RS2 SSRM 0.97 (−1.2%) | |
| [4](#rs2-4) | 🟢 | Dry Talbingo dam | Unconstrained: SSRM 1.672 vs closed form tan45/tan30.9 = 1.669 (+0.2%) · SSR Exclusion Area: SSRM 1.894 vs RS2 Part IV VP5 SSR 1.9 (−0.3%) | Two mechanisms, both locked; Part I's own 1.88 is the native model's unconstrained number. |
| [5](#rs2-5) | 🟢 | Water table with weak seam | SSRM 1.280 vs RS2 SSRM 1.26 (+1.6%) | |
| [6](#rs2-6) | 🟢 | Slope with load and pore pressure by water table (ACADS 4) | SSRM 0.777 vs ACADS referee 0.78 (−0.4%) | **built** (caveat) — +12.6% above RS2's own SSRM 0.69, and above Slide2's MC-optimized LEM. |
| [7](#rs2-7) | 🟢 | Pore pressure by digitized total head grid (ACADS 5) | SSRM 1.483 vs RS2 SSRM 1.48 (+0.2%) | Runs on the FE-seepage model built for Slide2 VP10. |
| [8](#rs2-8) | <span class="nodata">⊘</span> | Saint-Alban test embankment | | *no lock possible* — the grid encodes measured construction-induced pressures; RS2 SSRM 0.96 vs Pilot 1.04 recorded. |
| [9](#rs2-9) | 🟢 | Cubzac-les-Ponts test embankment | SSRM 1.320 vs RS2 SSRM 1.31 (+0.8%) | Pore pressures synthesized from the manual's printed 44-point table and the vendor model's water-table line, 95 points in all; the vendor's elastic face layer carried as `elastic_materials`. Pilot 1.24. |
| [10](#rs2-10) | 🟢 | Simple slope II (Arai & Tagyo ex. 1) | SSRM 1.411 vs RS2 SSRM 1.40 (+0.8%) | |
| [11](#rs2-11) | 🟢 | Layered slope (Arai & Tagyo ex. 2) | SSRM 0.406 vs RS2 SSRM 0.41 (−1.0%) | Scored against the Part IV VP15 model this file is built from; RS2's two models are input-identical and differ only in the SRF tensile setting, and the native twin's factor is 0.39. RS2's own SSRM is the only valid pairing — the 0.39–0.43 cross-bearing is stitched from two other programs' searches, which the conventions exclude. |
| [12](#rs2-12) | 🟢 | Simple slope + water table (Arai & Tagyo ex. 3) | SSRM 1.098 vs RS2 SSRM 1.09 (+0.7%) | |
| [13](#rs2-13) | 🟢 | Simple slope III (Yamagami & Ueta) | SSRM 1.332 vs RS2 SSRM 1.33 (+0.2%) | |
| [14](#rs2-14) | 🔴 | Simple slope, pore pressure by r<sub>u</sub> | SSRM 0.916 vs RS2 SSRM 0.98 (−6.5%) | **built** (caveat) — the factor never becomes mesh-independent; the tag pins 2.0 m as a regression lock. |
| [15](#rs2-15) | 🟢 | Layered slope II (Greco ex. 4 / Yamagami & Ueta) | SSRM 1.372 vs RS2 SSRM 1.38 (−0.6%) | Scored against the Part IV VP19 model this file is built from. |
| [16](#rs2-16) | 🟢 | Layered slope and water table with weak seam (Greco ex. 5 / Chen & Shao) | SSRM 0.978 inside Greco 0.973–1.1 · vs RS2 SSRM 1.02 (−4.1%) | Greco's own published range is the source author's and governs. Nearly mesh-invariant (0.959 at 2.2 m). |
| [17](#rs2-17) | 🟢 | Slope with three pore pressure conditions (Fredlund & Krahn) | Dry: SSRM 1.987 vs RS2 SSRM 1.98 (+0.4%) · r<sub>u</sub> = 0.25: SSRM 1.692 vs RS2 SSRM 1.68 (+0.7%) | **built** (dry + r<sub>u</sub>); the water-table case is not built. |
| [18](#rs2-18) | 🟡 | Three pore pressure conditions and a weak seam (Fredlund & Krahn) | Dry: SSRM 1.323 vs RS2 SSRM 1.26 (+5.0%) · r<sub>u</sub> = 0.25: SSRM 1.042 vs RS2 SSRM 0.99 (+5.3%) | **built** (dry + r<sub>u</sub>). Both files are the Slide2 VP22 model, so the Part IV values are the pairing. RS2 solved this problem twice, unconstrained both times, and its two answers differ by ~6%; its native rebuild publishes 1.34 / 1.05, which XSLOPE sits −1.3% and −0.8% from. |
| [19](#rs2-19) | 🟢 | Undrained layered slope (Low 1989) | SSRM 1.477 vs Low 1.44 (+2.6%) · vs RS2 SSRM 1.41 (+4.8%) | **built** (caveat) — Low's own factor governs; quoted at the tagged mesh, and the two SSRM values straddle the LEM. |
| [20](#rs2-20) | 🟢 | Slope with vertical load (Prandtl's wedge) | SSRM 1.003 vs RS2 SSRM 1.01 (−0.7%) | Prandtl theory 1.0 is a reference authority in its own right here. |
| [21](#rs2-21) | 🟢 | Bearing capacity test prism (Prandtl II) | SSRM 1.003 vs RS2 SSRM 1.01 (−0.7%) | Converging on Prandtl theory 1.0. One trial is undecided at the iteration ceiling. |
| [22](#rs2-22) | 🟢 | Layered slope with undulating bedrock | SSRM 1.534 vs RS2 SSRM 1.52 (+0.9%) | **built** (SSRM variant), on the vendor's boundary-load cap, carried at the vendor's own vertical load direction. |
| [23](#rs2-23) | 🟢 | Underwater slope with linearly varying cohesion | Under RS2's own elastic partition: SSRM 1.112 vs RS2 SSRM 1.12 (−0.7%) | **built** — the vendor model states the "can't fail" region element by element (a full-depth vertical band, not the text's "above el. −20 and right of the bench"), and the corpus carries it. Partition removed, the same model reads 0.215. |
| [24](#rs2-24) | <span class="nodata">⊘</span> | Layered slope with geosynthetic reinforcement | | *blocked* — the vendor models join embankment to foundation across a frictional slip interface along the geotextile, an element type XSLOPE does not have, so these rows are not attempted. The construction is read from the vendor models. RS2 SSRM 1.15 / 0.95 published. |
| [25](#rs2-25) | 🔴 | Syncrude tailings dyke (El-Ramly et al. 2003) | SSRM 1.202 vs RS2 SSRM 1.29 (−6.8%) | **built** (caveat) — refinement widens the gap rather than closing it: 1.174 at a 2.5 m mesh against the 1.202 locked at 5 m. |
| [26](#rs2-26) | 🟢 | Clarence Cannon dam (Wolff & Harr 1987) | SSRM 2.294 vs RS2 SSRM 2.29 (+0.2%) | |
| [27](#rs2-27) | 🟢 | Homogeneous slope, pore pressure by r<sub>u</sub> | SSRM 1.342 vs RS2 SSRM 1.31 (+2.4%) | **built** — regression lock at the 1.0 m mesh, flat from there down. |
| [28](#rs2-28) | 🟢 | Excavated slope, FE groundwater and matric suction (Ng & Shi 1998) | H = 61: SSRM 1.669 vs RS2 SSR 1.64 (+1.8%) · H = 62: SSRM 1.544 vs RS2 SSR 1.55 (−0.4%) · H = 63: SSRM 1.406 vs RS2 SSR 1.41 (−0.3%) | **built** (three heads). The corpus derives from the native `#028` variant, whose material partition holds 63% of the domain elastic, so the Part I §28 values govern. |
| [29](#rs2-29) | 🟢 | Geosynthetic-reinforced embankment on soft soil (Tandjiria 2002) | Sand: SSRM 1.219 vs RS2 SSRM 1.22 (−0.1%) · Clay: SSRM 0.997 vs RS2 SSR 0.99 (+0.7%) | **built** (both cases). The sand model runs unconstrained, as both vendor twins did; the clay model states its tension crack as geometry (crest cut at 2c/γ plus the removed weight as surcharge) and is transcribed that way. |
| [30](#rs2-30) | 🟡 | Homogeneous slope, power-curve strength (Perry 1993) | SSRM 1.023 vs RS2 SSR 0.97 (+5.5%) | Run under the vendor model's own three SSR exclusion areas, carried in the file as "SSR elastic" overlays. Unconstrained the file reads 0.898, on the native rebuild's own 0.91. |
| [31](#rs2-31) | 🟢 | M-C vs power curve (Baker 2003 ex. 1) | M-C: SSRM 1.529 vs RS2 SSRM 1.53 (−0.1%) · M-C local-linear: SSRM 0.969 vs RS2 SSRM 0.98 (−1.1%) · power curve: SSRM 0.973 vs Baker 0.97 (+0.3%) · GHB fit: SSRM 1.115 vs RS2 SSRM 1.11 (+0.5%) | **built** (four cases); the power curve is scored against the authorities sharing its strength model, since RS2's own table labels its 1.11 "SRF (Generalized Hoek-Brown)". |
| [32](#rs2-32) | 🟢 | M-C vs power curve II (Baker 2003 ex. 2) | M-C: SSRM 2.790 vs RS2 SSRM 2.83 (−1.4%) · power curve: SSRM 2.637 vs RS2 SSRM 2.63 (+0.3%) | **built** (both halves). RS2 solves the power-curve half on two different strength models; the pairing is its own power-curve model (Part IV VP45, 2.63). The native `#032-powercurve` model is a fitted Generalized Hoek-Brown envelope, and its 2.74 is a different strength model's answer. |
| [33](#rs2-33) | 🟢 | Homogeneous slope with tension crack and water table (P&D test slope 2) | SSRM 1.269 vs RS2 SSRM 1.28 (−0.9%) | **built** (caveat) — the dry tension crack has no FEM representation. |
| [34](#rs2-34) | 🟢 | M-C vs power curve III (Baker 2003 ex. 3, London clay) | M-C: SSRM 1.373 vs RS2 SSRM 1.38 (−0.5%) · power curve: SSRM 1.497 vs RS2 SSRM 1.47 (+1.8%) | **built** (both halves). |

</div>

### Part II (35–58)

<div class="corpus-summary match" markdown>

| # | Match | Problem | Results | Notes |
|---:|:-:|---|---|---|
| [35](#p4-vp70) | 🟢 | Submerged slope (D&W Fig 6.27) | SSRM 1.594 vs D&W referee 1.60 (−0.4%) | *covered* by the Part IV build [P4-VP70](#p4-vp70) on the Slide2 [VP70](rocscience.md#vp70) file; Part II's RS2 SSRM 1.64 and Part IV's 1.58 bracket it. |
| [36](#rs2-36) | 🟢 | Seepage analysis, homogeneous slope (D&W Fig 6.37) | FE seepage: SSRM 1.111 vs RS2 SSRM 1.12 (−0.8%) · piezo approximation: SSRM 1.111 vs RS2 SSRM 1.12 (−0.8%) | **built** (both cases). |
| [37](#rs2-37) | <span class="nodata">⊘</span> | Embankment with layered foundation (D&W Fig 6.39) | | *reported, no lock* — the two programs find different mechanisms: RS2's is the artesian downstream-toe slide, XSLOPE's a deeper surface. |
| [38](#rs2-38) | 🟢 | Cohesionless embankment on saturated clay foundation (D&W Fig 7.12) | SSRM 1.190 vs RS2 SSRM 1.17 (+1.7%) | Part 2's own SSRM is 1.21; RS2 re-ran the problem between the two manuals. |
| [39](#rs2-39) | <span class="nodata">⊘</span> | Homogeneous embankment dam, FE seepage (D&W Fig 7.19) | | *deferred* with the other FE-seepage cases — the third member of the [RS2-41/43](#rs2-39) family; the LEM build is Slide2 [VP76](rocscience.md#vp76). |
| [40](#rs2-40) | 🟡 | Dam with impermeable foundation (D&W Fig 7.24) | Piezometric, filter off: SSRM 1.160 vs closed form 1.190 (−2.5%) · Piezometric, `min_slip_depth` = 30 ft: SSRM 1.521 vs RS2 SSRM 1.53 (−0.6%) · FE seepage: SSRM 1.590 vs RS2 SSRM 1.52 (+4.6%) | **built** (both seepage cases). The piezometric case carries two mechanisms, both locked; the deep one settles from a 50 ft cutoff up, and it follows the element size as the skin does, so both are regression locks at the tagged mesh. The FE-seepage case is the widest of the three and sets the dot. |
| [41](#rs2-39) | 🟢 | Earth embankment, infinite-slope mechanism (D&W Fig 14.4) | SSRM 1.431 vs D&W referee 1.44 (−0.6%) | **built** (caveat) — the unconstrained skin is the mechanism, and it lands inside RS2's own 1.43–1.47 band. |
| [42](#rs2-42) | 🟢 | James dike | SSRM 1.214 vs RS2 SSRM 1.19 (+2.0%) | Scored against the Part IV VP75 model this file is built from; the input-identical native twin, which differs only in its SRF tensile setting and a coarser mesh, publishes 1.26. |
| [43](#rs2-39) | 🟢 | Earth embankment, infinite-slope mechanism (D&W Fig 14.7) | SSRM 1.209 vs RS2 Part IV VP81 case 1 SSR 1.23 (−1.7%) | **built** (caveat) — run under the vendor model's own SSR Exclusion Area; unconstrained the c = 0 skin localizes at 1.116. |
| [44](#rs2-44) | 🟢 | Seepage analysis for an earth embankment (D&W Fig 14.20-a) | SSRM 1.490 vs RS2 SSRM 1.51 (−1.3%) | |
| [45](#rs2-45) | 🟢 | Varying undrained shear strength profiles (D&W Fig 14.20-b) | vp083a: SSRM 1.314 vs RS2 SSRM 1.32 (−0.5%) · vp083b: SSRM 1.314 vs RS2 SSRM 1.32 (−0.5%) | **built** (caveat). |
| [46](#rs2-46) | 🟢 | Varying undrained strength profiles II (D&W Fig 15.9, c<sub>u</sub> = 300 + c<sub>z</sub>·z) | a: SSRM 0.787 vs RS2 SSRM 0.78 (+0.9%) · b: SSRM 0.929 vs RS2 SSRM 0.93 (−0.1%) · c: SSRM 1.057 vs RS2 SSRM 1.05 (+0.7%) · d: SSRM 1.145 vs RS2 SSRM 1.15 (−0.4%) | |
| [47](#rs2-47) | 🟢 | Purely cohesive slope, varying thickness (D&W Fig 14.3) | 30 ft: SSRM 1.061 vs RS2 SSRM 1.06 (+0.1%) · 46.5 ft: SSRM 1.045 vs RS2 SSRM 1.06 (−1.4%) · 60 ft: SSRM 1.045 vs RS2 SSRM 1.07 (−2.3%) | **built** (all 3 thicknesses); scored against the Part IV VP78 case-(a) models these files are built from. |
| [48](#rs2-48) | <span class="nodata">⊘</span> | Multi-tiered geotextile wall, baseline (Leshchinsky & Han 2004) | | *blocked* — RS2 splits the mesh along the geotextile layers and joins the halves with frictional slip interfaces, an element type XSLOPE does not have, so the SSR row is not attempted. RS2 SSR 1.05 published; Leshchinsky & Han's FDM referee 0.99, their Bishop 1.00. |
| [49](#rs2-49) | <span class="nodata">⊘</span> | Geotextile wall, fill-quality variant | SSRM 0.881 | **built**, locked at the section's mesh — steady under a refinement step, but RS2's factor comes from the split-interface wall [RS2-48](#rs2-48) describes, so there is nothing to score it against. |
| [50](#rs2-50) | <span class="nodata">⊘</span> | Geotextile wall, 4.2 m reinforcement variant | | *reported, no lock* — the c = 0 fill localization makes the value follow the mesh, and RS2's factor comes from the split-interface wall [RS2-48](#rs2-48) describes. |
| [51](#rs2-51-wall) | <span class="nodata">⊘</span> | Geotextile wall, dual reinforcement type | SSRM 0.998 | **built**, locked at the section's mesh — as [RS2-49](#rs2-49): steady under refinement, with no comparable vendor factor to score against. |
| [52](#rs2-52) | <span class="nodata">⊘</span> | Geotextile wall, weak-foundation variant |  | *reported, no lock* — bearing failure on the c = 0 / φ = 18° foundation, on the LEM file's 30 m section and on the vendor's own 24 m section alike, recorded beside RS2's own SSR 0.84 and the L&H FLAC referee 0.86. Those come from the split-interface wall [RS2-48](#rs2-48) describes, so they are not scored against XSLOPE's bonded continuum, and neither reading is locked. |
| [53](#rs2-53) | <span class="nodata">⊘</span> | Geotextile wall, water variant | | *reported, no lock* — brackets, but the c = 0 fill localization makes the value follow the mesh, so no comparison is derived. |
| [54](#rs2-54) | <span class="nodata">⊘</span> | Geotextile wall, crest-surcharge variant | | *reported, no lock* — the most refinement-sensitive member of the family. |
| [55](#rs2-55) | <span class="nodata">⊘</span> | Geotextile wall, tier-count variant | | *reported, no lock* — brackets, but the c = 0 fill localization makes the value follow the mesh, so no comparison is derived. |
| [56](#rs2-56) | 🟢 | Homogeneous slope vs Z-Soil, PLAXIS, GEO FEM (Pruska 2003, H = 7 m, 5 cases) | Case 2 (weakest): SSRM 0.664 vs RS2 SSRM 0.67 (−0.9%) · Case 5 (strongest): SSRM 2.096 vs RS2 SSRM 2.14 (−2.1%) | The two locks bracket the family; case 5 is the wider of them and sets the dot. Published columns for all five cases in [the Pruska section](#pruska). |
| [57](#rs2-57) | 🟢 | Pruska H = 10.5 m, 6 cases | Case 1 (weakest): SSRM 0.439 vs RS2 SSRM 0.44 (−0.2%) · Case 6 (strongest): SSRM 1.401 vs RS2 SSRM 1.42 (−1.3%) | The two locks bracket the family; case 6 is the wider of them and sets the dot. Published columns for all six cases in [the Pruska section](#pruska). |
| [58](#rs2-58) | 🟢 | Pruska H = 14 m, 6 cases | Case 1: SSRM 0.339 vs RS2 SSRM 0.33 (+2.7%) · Case 5: SSRM 0.714 vs RS2 SSRM 0.72 (−0.8%) · Case 6: SSRM 1.066 vs RS2 SSRM 1.06 (+0.6%) | **built** (6 of 6) — the three locks within ±2.7%; case 1 is the widest and sets the dot. |

</div>

### Part III (59–68)

<div class="corpus-summary match" markdown>

| # | Match | Problem | Results | Notes |
|---:|:-:|---|---|---|
| [59](#rs2-59) | 🟢 | Three-layered soil slope | SSRM 1.553 vs RS2 SSRM 1.57 (−1.1%) | Görög & Török (2007) Budapest landslide; the critical mechanism is non-circular, so a circular search misfinds a deeper surface and this is an SSRM problem. |
| [60](#rs2-60) | 🟢 | Generalized Hoek–Brown, homogeneous slope | β = 15°: Spencer 1.009 vs Slide2 1.011 (−0.2%) · β = 30°: Spencer 0.989 vs Slide2 0.992 (−0.3%) · β = 45°: Spencer 1.035 vs Slide2 1.035 (0.0%) | **built** (LEM), three slope angles at GSI = 70 with the vendor σ<sub>ci</sub>. SSRM is not locked on this problem. |
| [61](#rs2-61) | 🟢 | Local and global minima, homogeneous slope | Case 1: Spencer 1.338 vs Slide2 1.336 (+0.1%) · Case 3: Spencer 1.437 vs Slide2 1.443 (−0.4%) · Case 2: constrained SSRM 1.398 vs RS2 SSRM 1.36 (+2.8%) | **built** (cases 1, 3, 2) — one geometry, four search regions; case 2 uses RS2's own Search-Area polygon. Case 4 blocked. |
| [62](#rs2-62) | 🟡 | Three-layered slope with a soft band | SSRM 0.781 vs RS2 SSR 0.81 (−3.6%) | **built** (Analysis III) — the decisive input is the vendor per-material tensile strength reduced with the SRF; without it the FE equilibrates at F ≥ 1.3. |
| [63](#rs2-63) | 🟢 | Homogeneous slope assessment | Spencer 1.398 vs Slide2 1.380 (+1.3%) · SSRM 1.409 vs RS2 SSRM 1.38 (+2.1%) | Cheng et al. (2007), 11 m homogeneous slope. |
| [64](#rs2-64) | 🔴 | Three homogeneous landslides | C1: SSRM 5.189 vs RS2 SSR 5.14 (+1.0%) · C3: SSRM 4.807 vs RS2 SSR 4.69 (+2.5%) · C5: SSRM 5.620 vs RS2 SSR 5.47 (+2.7%) · C7: SSRM 1.639 vs RS2 SSR 1.70 (−3.6%) · C11: SSRM 1.403 vs RS2 SSR 1.46 (−3.9%) · C12: SSRM 1.147 vs RS2 SSR 1.22 (−6.0%) · C2: SSRM 6.564 vs RS2 SSR 6.10 (+7.6%) · C4: SSRM 5.461 vs RS2 SSR 4.95 (+10.3%) | **partial** (8 of 12 locked; C6 and C8–C10 blocked). Teoman et al. (2004) Ankara clay E90 highway, each case pinned by RS2 to a digitized proposed slip surface. C4 sets the dot; on it and C2 the Teoman and Slide2 Bishop columns (5.32 / 5.32 and 6.67 / 6.64) sit beside XSLOPE, but they are cross-method and cannot carry the comparison. |
| [65](#rs2-65) | 🟢 | Tailings dam | SSRM 1.306 vs RS2 SSRM 1.29 (+1.2%) | Tzenkov (2008) Padina dam, 8 materials on a 225 × 77 m section, locked at the vendor's own mesh density. The reference FEM 1.41 and the LEM columns are cross-bearings that do not govern. |
| [66](#rs2-66) | 🟢 | Embankment basal stability | Face skin, worst leg (h₁ = 4, 6 and 8 m): SSRM 1.031 vs closed form 1.050 (−1.8%) · thinnest and thickest bands (h₁ = 2 and 10 m): SSRM 1.044 vs 1.050 (−0.6%) | **built** — two mechanisms, both locked across all five soft-layer thicknesses; the deep run uses `min_slip_depth` = 4 m, and every file meshes its soft band at 1.05 m. The dot is the face skin's, against a closed form that does not depend on the flow rule, and the worst of the five legs sets it: none is wider, and the two extreme thicknesses are the narrowest. The deep family (1.169 at h₁ = 2 and 4 m, 1.031 at 6 and 10 m) is recorded beside RS2's SSR column rather than scored against it: every published strength-reduction solution of this problem runs associated flow, ψ = φ, where XSLOPE runs ψ = 0. |
| [67](#rs2-67) | 🟢 | Earth dam under steady & transient unsaturated seepage | Case 1 (dry): SSRM 2.502 vs RS2 SSR 2.48 (+0.9%) · Case 2 (steady): SSRM 1.695 vs RS2 SSR 1.70 (−0.3%) · Case 3 (90 h, downstream): SSRM 1.820 vs RS2 SSR 1.83 (−0.5%) · Case 3 (90 h, upstream): SSRM 2.008 vs RS2 SSR 2.04 (−1.6%) · Case 4 (1500 h, downstream): SSRM 2.320 vs RS2 SSR 2.34 (−0.9%) · Case 4 (1500 h, upstream): SSRM 2.742 vs RS2 SSR 2.76 (−0.7%) | **built** (6 of 6 locked). Three run on RS2's own imported drawdown pore-pressure fields; three reconstruct the flow by an own steady solve from the vendor's boundary conditions. |
| [68](#rs2-68) | 🔴 | Seismically loaded slopes | Case 1 Spencer: k꜀ 0.132 vs Loukidis Spencer 0.131 (+0.8%) · Case 2 Spencer: k꜀ 0.433 vs Loukidis Spencer 0.431 (+0.5%) · Case 3 Bishop: k꜀ 0.169 vs Slide2 Bishop 0.155 (+9.0%) · Case 3 Spencer: k꜀ 0.167 vs Loukidis Spencer 0.155 (+7.7%) | The target is a **critical seismic coefficient** k꜀, not a factor of safety, reached by a `critical_kc` bisection. Case 3 sets the dot on its Bishop leg. Loukidis publishes a Spencer k꜀ but no Bishop k꜀ for this example — the RS2 manual columns it the other way round — so Slide2 is the Bishop authority. Every input class verifies against the vendor `#068_03` model; RS2's own SSRM k꜀ 0.161 is a strength-reduction number and stays a cross-bearing. |

</div>

### Part IV — RS2 *Slope Stability Verification Manual, Pt 4* (catalog)

<div class="corpus-summary match" markdown>

| # | Match | Problem | Results | Notes |
|---:|:-:|---|---|---|
| [1](#rs2-1) | 🟢 | Slope, homogeneous (ACADS 1a) | SSRM 0.986 vs RS2 SSRM 0.99 (−0.4%) | Piggyback on [RS2-1](#rs2-1). Part IV publishes RS2 SSRM 0.98; ref 1.00 [Giam]. |
| [2](#p4-vp2) | 🟢 | Slope, homogeneous, tension crack (ACADS 1b) | SSRM 1.644 vs RS2 SSRM 1.63 (+0.9%) | Own SSRM build carrying the vendor's T = 0 crack zone; ref 1.65 [Giam]. |
| [3](#rs2-2) | 🟢 | Slope, 3 materials (ACADS 1c) | SSRM 1.347 vs RS2 SSRM 1.36 (−1.0%) | Piggyback on [RS2-2](#rs2-2). Part IV publishes RS2 SSRM 1.34; ref 1.39. |
| [4](#rs2-3) | 🟢 | Slope, 3 materials, seismic (ACADS 1d) | SSRM 0.958 vs RS2 SSRM 0.97 (−1.2%) | Piggyback on [RS2-3](#rs2-3). Part IV publishes RS2 SSRM 0.95; ref 1.00. |
| [5](#rs2-4) | 🟢 | Dam, 4 materials (ACADS 2a) | Unconstrained: SSRM 1.672 vs closed form 1.669 (+0.2%) · SSR Exclusion Area: SSRM 1.894 vs RS2 SSRM 1.9 (−0.3%) | Locked twice on [RS2-4](#rs2-4), the second under this manual's own SSR Exclusion Area. Slide2 1.948, ref 1.95 [Giam]. |
| [6](#p4-vp6) | 🟢 | Dam, 4 materials, predefined surface (ACADS 2b) | SSRM 2.188 vs RS2 SSRM 2.15 (+1.8%) | Own SSRM build, constrained to RS2's 37-vertex Search Area from `#006.fez`, which holds the mechanism on ACADS 2(b)'s upstream circle. |
| [7](#rs2-5) | 🟢 | Slope, 2 materials, weak layer (ACADS 3a) | SSRM 1.280 vs RS2 SSRM 1.26 (+1.6%) | Piggyback on [RS2-5](#rs2-5). Part IV publishes RS2 SSRM 1.24; ref 1.24–1.27. |
| [9](#rs2-6) | 🟢 | Weak layer, water table, load (ACADS 4) | SSRM 0.777 vs ACADS referee 0.78 (−0.4%) | Piggyback on [RS2-6](#rs2-6). Part IV publishes RS2 SSRM 0.76. |
| [10](#rs2-7) | 🟢 | Homogeneous, pore-pressure grid, ponded (ACADS 5) | SSRM 1.483 vs RS2 SSRM 1.48 (+0.2%) | Piggyback on [RS2-7](#rs2-7). Part IV publishes RS2 SSRM 1.46; ref 1.53. |
| [14](#rs2-10) | 🟢 | Slope, homogeneous (Arai & Tagyo 1) | SSRM 1.411 vs RS2 SSRM 1.40 (+0.8%) | Piggyback on [RS2-10](#rs2-10). Part IV publishes RS2 SSRM 1.37–1.39. |
| [15](#rs2-11) | 🟢 | Slope, 3 materials, weak layer (Arai & Tagyo 2) | SSRM 0.406 vs RS2 SSRM 0.41 (−1.0%) | Piggyback on [RS2-11](#rs2-11). Parts I–III publish RS2 SSRM 0.39 on the input-identical native twin; Kim/Greco 0.39–0.44. |
| [16](#rs2-12) | 🟢 | Slope, homogeneous, water table (Arai & Tagyo 3) | SSRM 1.098 vs RS2 SSRM 1.09 (+0.7%) | Piggyback on [RS2-12](#rs2-12). |
| [17](#rs2-13) | 🟢 | Slope, homogeneous (Yamagami & Ueta) | SSRM 1.332 vs RS2 SSRM 1.33 (+0.2%) | Piggyback on [RS2-13](#rs2-13). Part IV publishes RS2 SSRM 1.32. |
| [19](#rs2-15) | 🟢 | Slope, 4 materials (Greco ex. 4) | SSRM 1.372 vs RS2 SSRM 1.38 (−0.6%) | Piggyback on [RS2-15](#rs2-15); Greco/Spencer 1.40–1.42. |
| [21](#rs2-17) | 🟢 | Homogeneous, r<sub>u</sub> (Fredlund & Krahn) | Dry: SSRM 1.987 vs RS2 SSRM 1.98 (+0.4%) · r<sub>u</sub> = 0.25: SSRM 1.692 vs RS2 SSRM 1.68 (+0.7%) | Piggyback on [RS2-17](#rs2-17). Part IV publishes RS2 SSRM 1.98 / 1.68 / 1.77. |
| [22](#rs2-18) | 🟡 | Weak layer, r<sub>u</sub> (Fredlund & Krahn) | Dry: SSRM 1.323 vs RS2 SSRM 1.26 (+5.0%) · r<sub>u</sub> = 0.25: SSRM 1.042 vs RS2 SSRM 0.99 (+5.3%) | Piggyback on [RS2-18](#rs2-18). Part IV publishes 1.26 / 0.99 / 1.15 against the native model's 1.34 / 1.05 / 1.13 — the vendor's own scatter, both unconstrained. |
| [24](#rs2-19) | 🟢 | Slope, 3 materials (Low 1989) | SSRM 1.477 vs Low 1.44 (+2.6%) · vs RS2 SSRM 1.41 (+4.8%) | Piggyback on [RS2-19](#rs2-19); Low's own factor governs, as on that row. Part IV publishes RS2 SSRM 1.42. |
| [25](#rs2-20) | 🟢 | Bearing-capacity slope (Prandtl / Chen & Shao) | SSRM 1.003 vs RS2 SSRM 1.01 (−0.7%) | Piggyback on [RS2-20](#rs2-20); Chen & Shao 1.05. |
| [26](#rs2-21) | 🟢 | Bearing-capacity prism (Prandtl II) | SSRM 1.003 vs RS2 SSRM 1.01 (−0.7%) | Piggyback on [RS2-21](#rs2-21). Part IV publishes RS2 SSRM 1.00; theory 1.0. |
| [32](#rs2-24) | <span class="nodata">⊘</span> | Reinforced embankment, 7 materials (Borges 2002) | | *blocked* with [RS2-24](#rs2-24), whose models these are: the slip interface along the geotextile has no XSLOPE counterpart, so the SSR rows are not attempted. Part IV publishes RS2 SSRM 1.24 / 1.21 / 0.98; Borges 1.25 / 1.19 / 0.99. The limit-equilibrium build of the same problem is Slide2 [VP32](rocscience.md#vp32). |
| [38](#rs2-28) | 🟢 | Excavated slope, FE seepage, suction (Ng & Shi 1998) | H = 61: SSRM 1.669 vs RS2 SSR 1.64 (+1.8%) · H = 62: SSRM 1.544 vs RS2 SSR 1.55 (−0.4%) · H = 63: SSRM 1.406 vs RS2 SSR 1.41 (−0.3%) | Piggyback on [RS2-28](#rs2-28), which is built from the native `#028` models; the Part I §28 values govern. |
| [39](#rs2-29) | 🟢 | Reinforced embankment, geosynthetic (Tandjiria 2002) | Sand: SSRM 1.219 vs RS2 SSRM 1.22 (−0.1%) · Clay: SSRM 0.997 vs RS2 SSR 0.99 (+0.7%) | Piggyback on [RS2-29](#rs2-29), both cases; the clay lock pairs with RS2's own Part I model. Part IV publishes RS2 SSRM 0.97 / 1.42 / 1.22 / 1.39. |
| [40](#rs2-30) | 🟡 | Homogeneous, power curve, sensitivity (Perry 1993) | SSRM 1.023 vs RS2 SSR 0.97 (+5.5%) | Piggyback on [RS2-30](#rs2-30); run under the vendor's own three exclusion areas, carried in the file. Perry 0.98. |
| [41](#p4-vp41) | 🟢 | Homogeneous, power curve, r<sub>u</sub> (Jiang/Baker 2003) | SSRM 1.656 vs RS2 SSRM 1.64 (+1.0%) | Own SSRM build; Bishop 1.66 / Janbu 1.60–1.67. |
| [42](rocscience.md#vp42) | <span class="nodata">⊘</span> | Dam, safety-map example (Baker & Leshchinsky 2001) |  | *reported, no lock* — SSRM 1.653 against RS2 SSRM 1.84, the c = 0 granular-shell localization [RS2-40](#rs2-40) documents; the LEM side reproduces the reference cluster on all three surfaces (Spencer 1.926 / 1.882 / 1.939 vs 1.925 / 1.91 / 1.934). B&L 1.91. |
| [44](#rs2-31) | 🟢 | Homogeneous, M-C vs power curve (Baker 2003 ex. 1) | M-C: SSRM 1.529 vs RS2 SSRM 1.53 (−0.1%) · M-C local-linear: SSRM 0.969 vs RS2 SSRM 0.98 (−1.1%) · power curve: SSRM 0.973 vs Baker 0.97 (+0.3%) · GHB fit: SSRM 1.115 vs RS2 SSRM 1.11 (+0.5%) | Piggyback on [RS2-31](#rs2-31), four cases. Part IV publishes RS2 SSRM 0.96 / 1.5 / 0.93. |
| [45](#rs2-32) | 🟢 | Homogeneous, M-C vs power curve (Baker 2003 ex. 2) | M-C: SSRM 2.790 vs RS2 SSRM 2.83 (−1.4%) · power curve: SSRM 2.637 vs RS2 SSRM 2.63 (+0.3%) | Piggyback on [RS2-32](#rs2-32). Part IV publishes RS2 SSRM 2.65 / 2.78 / 2.63; 2.63 is its power-curve model and governs that half. Parts I–III's 2.74 comes from a Generalized Hoek-Brown fit of the same envelope. |
| [51](#p4-vp51) | 🟢 | 4 materials, water table, TC, seismic, 12-method (Zhu 2003) | Spencer 1.300 vs Slide2 1.293 (+0.5%) | Own Part IV build, LEM (partial) — [details](#p4-vp51). RS2 SSRM 1.22; Slide2 GLE 1.304. |
| [56](#rs2-33) | 🟢 | Homogeneous, water table, TC (Pockoski & Duncan slope 2) | SSRM 1.269 vs RS2 SSRM 1.28 (−0.9%) | Piggyback on [RS2-33](#rs2-33). Part IV publishes RS2 SSRM 1.26; an eight-program LEM table spans 1.02–1.32. |
| [57](#p4-vp57) | 🟢 | Layered, TC (Pockoski & Duncan slope 3) | SSRM 1.323 vs RS2 SSRM 1.32 (+0.2%) | Own SSRM build carrying the vendor's T = 0 crack zone; the eight-program LEM table sits near 1.40. |
| [60](#p4-vp60) | 🟢 | Soil-nailed wall (Pockoski & Duncan slope 7) | SSRM 1.009 vs RS2 SSRM 0.98 (+3.0%) | Own SSRM build with five passive nail rows rooted in the vertical wall face, just under XSLOPE's own Spencer 1.010. GOLD-NAIL 0.91 / UTEXAS4 1.02. |
| [61](#rs2-34) | 🟢 | Homogeneous, composite surfaces (Baker 2003 ex. 3) | M-C: SSRM 1.373 vs RS2 SSRM 1.38 (−0.5%) · power curve: SSRM 1.497 vs RS2 SSRM 1.47 (+1.8%) | Piggyback on [RS2-34](#rs2-34). Part IV publishes RS2 SSRM 1.34 / 1.45; Baker 1.35 / 1.48. |
| [62](#rs2-68) | 🟢 | Homogeneous, r<sub>u</sub>, seismic k꜀ (Loukidis 2003 ex. 1) | Spencer: k꜀ 0.132 vs Loukidis Spencer 0.131 (+0.8%) | Piggyback on [RS2-68](#rs2-68), Case 1. RS2 SSRM 0.96. |
| [63](#rs2-68) | 🔴 | 3 materials, seismic k꜀ (Loukidis 2003 ex. 2) | Bishop: k꜀ 0.169 vs Slide2 Bishop 0.155 (+9.0%) · Spencer: k꜀ 0.167 vs Loukidis Spencer 0.155 (+7.7%) | Piggyback on [RS2-68](#rs2-68), Case 3. The paper's Table 3 publishes Spencer 0.155 and no Bishop value for this example, so Slide2 is the Bishop authority. RS2's own SSRM k꜀ is 0.161, a cross-bearing here; Part IV's 0.99 is the SSR factor of safety RS2 reports at the paper's fixed k = 0.155, not a k꜀. |
| [64](#p4-vp64) | 🟢 | Embankment, 3 layers, water table, TC (USACE 2003 Fig 4-1) | SSRM 2.394 vs RS2 SSRM 2.37 (+1.0%) | Own SSRM build; Spencer 2.44 [USACE]. The vendor's 65-vertex SSR corridor is documented, not carried — it is thinner than the corpus mesh. |
| [65](#p4-vp65) | <span class="nodata">⊘</span> | Embankment, water table, ponded (USACE 2003 Fig 4-2) |  | *reported, no lock* — own SSRM build, unconstrained, at 1.909 on an upstream mechanism; RS2's 2.60 is constrained to the published circle by an SSR corridor the corpus mesh cannot resolve, so the two are not a pairing. Ref 2.71. |
| [66](#p4-vp66) | 🟢 | Embankment, water table, ponded (USACE 2003 Fig 4-3) | SSRM 2.172 vs RS2 SSRM 2.22 (−2.2%) | Own SSRM build, ponded on both faces as the vendor model is. USACE 2.30. |
| [67](#p4-vp67) | 🟢 | Embankment, 2 materials, end of construction (USACE 2003 F-5) | SSR Exclusion Area: SSRM 1.303 vs RS2 SSRM 1.33 (−2.0%) | Own SSRM build; unconstrained it finds the true global minimum at 1.076. Ref 1.33. |
| [68](#p4-vp68) | 🟢 | Slope, homogeneous, φ = 0 (USACE 2003 E-10) | SSR Search Area: SSRM 1.203 vs RS2 SSRM 1.17 (+2.8%) | Own SSRM build, two answers: every published number describes one *specified* circle, and RS2's SSR is constrained to it by the 30-vertex Search Area in `#068.fez`. Unconstrained, 1.016 on a weaker mechanism. Slide2 1.241, ref 1.33 [USACE]. |
| [69](#p4-vp69) | 🟢 | Embankment, 2 materials, steady seepage (USACE 2003 F-6) | SSR Search Area: SSRM 1.944 vs RS2 SSRM 1.94 (+0.2%) | **built** (caveat) — RS2's published factor is constrained by the 38-vertex Search Area in `#069.fez`, which the tag carries verbatim. Both zones are c = 0, so the factor drifts with refinement (2.019 / 1.969 / 1.944 / 1.931 at 8 / 6.5 / 5 / 4 ft); the tag pins the 5 ft mesh. Unconstrained, 1.508. USACE 2.01, Slide2 Spencer 2.026. |
| [70](#p4-vp70) | 🟢 | Submerged homogeneous slope (Duncan & Wright Fig 6.27) | SSRM 1.594 vs RS2 SSRM 1.58 (+0.9%) | Own SSRM build; Spencer 1.60, ref 1.60. |
| [71](#rs2-36) | 🟢 | Homogeneous, FE seepage (Duncan & Wright Fig 6.37) | FE seepage: SSRM 1.111 vs RS2 SSRM 1.12 (−0.8%) · piezo approximation: SSRM 1.111 vs RS2 SSRM 1.12 (−0.8%) | Piggyback on [RS2-36](#rs2-36); Spencer 1.13 / 1.14. |
| [72](#rs2-37) | <span class="nodata">⊘</span> | Embankment dam, 4 materials, FE seepage (D&W Fig 6.39) |  | *reported, no lock* — the two programs find different mechanisms. RS2 SSRM 1.00–1.49 vs Spencer 1.16–1.63. |
| [74](#rs2-38) | 🟢 | Cohesionless embankment on clay (D&W Fig 7.12) | SSRM 1.190 vs RS2 SSRM 1.17 (+1.7%) | Piggyback on [RS2-38](#rs2-38); Spencer 1.20. |
| [75](#rs2-42) | 🟢 | James Bay dyke, 4 materials (D&W Fig 7.16) | SSRM 1.214 vs RS2 SSRM 1.19 (+2.0%) | Piggyback on [RS2-42](#rs2-42). Parts I–III publish RS2 SSRM 1.26 on the input-identical native twin; circular 1.45 / non-circular 1.17. |
| [76](#rs2-39) | <span class="nodata">⊘</span> | Homogeneous embankment dam, FE seepage (D&W Fig 7.19) |  | *deferred* — the SSRM sibling of [RS2-41/43](#rs2-39); the LEM build is Slide2 [VP76](rocscience.md#vp76). RS2 SSRM 0.97 / 0.98 vs Slide2 Spencer 1.08 / 1.10, D&W 1.08–1.19. Part 4 does not cover Slide2 VP77, the dam of [RS2-40](#rs2-40). |
| [78](#rs2-47) | 🟢 | Purely cohesive slope, thickness variants (D&W Fig 14.3) | 30 ft: SSRM 1.061 vs RS2 SSRM 1.06 (+0.1%) · 46.5 ft: SSRM 1.045 vs RS2 SSRM 1.06 (−1.4%) · 60 ft: SSRM 1.045 vs RS2 SSRM 1.07 (−2.3%) | Piggyback on [RS2-47](#rs2-47), all three thicknesses on the case-(a) models; D&W 1.12–1.14. |
| [79](#rs2-39) | 🟢 | Earth embankment, infinite-slope failure (D&W Fig 14.4) | SSRM 1.431 vs D&W referee 1.44 (−0.6%) | Piggyback on [RS2-41](#rs2-39); the deep run reads 1.419. Part IV publishes RS2 SSRM 1.41 / 1.45; ref 1.40 / 1.44. |
| [81](#rs2-39) | 🟢 | Earth embankment, infinite-slope failure (D&W Fig 14.7) | SSRM 1.209 vs RS2 SSRM 1.23 (−1.7%) | Piggyback on [RS2-43](#rs2-39), under the vendor model's own SSR Exclusion Area. Part IV case 2 publishes 1.15; ref 1.21 / 1.15. |
| [82](#rs2-44) | 🟢 | Earth embankment, water table (D&W Fig 14.20-a) | SSRM 1.490 vs RS2 SSRM 1.51 (−1.3%) | Piggyback on [RS2-44](#rs2-44). Part IV publishes RS2 SSRM 1.50; Spencer 1.54. |
| [83](#rs2-45) | 🟢 | Embankment wall (D&W Fig 14.20-b) | vp083a: SSRM 1.314 vs RS2 SSRM 1.32 (−0.5%) · vp083b: SSRM 1.314 vs RS2 SSRM 1.32 (−0.5%) | Piggyback on [RS2-45](#rs2-45). Part IV publishes RS2 SSRM 1.29 / 1.30; Spencer 1.28 / 1.33. |
| [102](#p4-vp102) | 🔴 | Homogeneous earth dam, rapid drawdown (Huang & Jia) | Dry: SSRM 2.455 vs RS2 SSRM 2.43 (+1.0%) · drawdown φ<sup>b</sup> = 0°, worst frame (60 h): SSRM 1.713 vs RS2 SSR 1.77 (−3.2%) · φ<sup>b</sup> = 37°, worst frame (1500 h): SSRM 2.687 vs RS2 SSR 2.48 (+8.3%) | **built** (dry + transient) — own SSRM build plus the 60–1500 h drawdown curve from XSLOPE's own transient seepage solve. The φ<sup>b</sup> = 37° late frame sets the dot: the credit is uncapped on both sides — every `#102_3_*` model sets φ<sup>b</sup> = 37° with a zero air-entry value and the material suction cutoff off — and it grows with the drainage, buying about twice the factor of safety that separates the vendor's own two columns. The same uncapped machinery is within 1.8% on [RS2-28](#rs2-28), so the gap sits in the size of the suction field rather than the strength model. The φ<sup>b</sup> = 0° baseline is within 3.2% at every frame. The vendor SSR Search Area is carried in the files and is inert: the dry case returns the same 2.455. Spencer 2.455, ref 2.43. |

</div>

Of the 52 problems cataloged, 37 piggyback on the RS2-N section that carries the comparison.
The other fifteen have a build section of their own: fourteen below — the twelve-method Zhu
comparison ([VP51](#p4-vp51)), built by limit equilibrium, and thirteen strength-reduction builds
on a shared Slide2 file ([VP2](#p4-vp2), [VP6](#p4-vp6), [VP41](#p4-vp41), [VP57](#p4-vp57),
[VP60](#p4-vp60), [VP64](#p4-vp64), [VP65/VP66](#p4-vp65), [VP67](#p4-vp67), [VP68](#p4-vp68),
[VP69](#p4-vp69), [VP70](#p4-vp70) and [VP102](#p4-vp102)) — and the safety-map dam on the Slide2
page ([VP42](rocscience.md#vp42)). VP70's Parts I–III counterpart is problem 35, which the same
build covers.

---

## Problem details

### RS2-1: Simple slope stability assessment {#rs2-1}

Slide2 counterpart: [VP1](rocscience.md#vp1) (ACADS 1a).

**Input files:** [xslope_acads_simple.xlsx](../lem/files/xslope_acads_simple.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | ACADS referee |
|---|---|---|---|---|
| SSRM | 0.986 | 0.99 (−0.4%) | Bishop 0.987 | 1.00 (−1.4%) |

<!-- test: file=../lem/files/xslope_acads_simple.xlsx, type=fem_ssrm, expected_fs=0.986, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-1 -->

![RS2-1: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-1.png)

### RS2-2: Non-homogeneous slope {#rs2-2}

Slide2 counterpart: [VP3](rocscience.md#vp3).

**Input files:** [vp003.xlsx](files/rocscience/vp003.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | ACADS referee |
|---|---|---|---|---|
| SSRM | 1.347 | 1.36 (−1.0%) | Spencer 1.375 | 1.39 (−3.1%) |

<!-- test: file=files/rocscience/vp003.xlsx, type=fem_ssrm, expected_fs=1.347, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=1.0, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-2 -->

![RS2-2: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-2.png)

### RS2-3: Non-homogeneous slope with seismic load (0.15g) {#rs2-3}

Slide2 counterpart: [VP4](rocscience.md#vp4).

**Input files:** [vp004.xlsx](files/rocscience/vp004.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | ACADS referee |
|---|---|---|---|---|
| SSRM | 0.958 | 0.97 (−1.2%) | Spencer 0.991 | 1.00 (−4.2%) |

k is entered negative per the FEM sign convention — this is a left-facing slope, so the
pseudo-static force acts in −x, while the LEM takes the magnitude and directs it from the
failure surface.

<!-- test: file=files/rocscience/vp004.xlsx, type=fem_ssrm, expected_fs=0.958, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-3 -->

![RS2-3: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-3.png)

### RS2-4: Dry Talbingo dam {#rs2-4}

Slide2 counterpart: [VP5](rocscience.md#vp5).

**Input files:** [vp005.xlsx](files/rocscience/vp005.xlsx)

| Case | XSLOPE SSRM | Published |
|---|---|---|
| Unconstrained (true global minimum) | 1.672 | closed form tan 45° / tan 30.9° = **1.669** (+0.2%) |
| RS2's own model: SSR Exclusion Area | 1.894 | RS2 SSRM **1.9** (−0.3%, Part 4 VP5, the model this file's zone comes from) |

**Two mechanisms.** Every zone of this dam is cohesionless except the clay core, so the classical
answer for a face is the surface-parallel slide FS = tan φ / tan β, independent of depth, and the
steepest face governs. XSLOPE's unfiltered SSRM finds exactly that on the steeper **downstream
bench**, the shear strain a thin surface band along the two steepest bench segments (30.9° and
30.8°) inside the c = 0 downstream Rockfill. RS2 reports a **crest / inclined-core** band instead,
in both of its published models. Part 4's Figure 5.3 is annotated "SSR Exclusion Area" across the
whole downstream benched shell, and `slope stability #005.fez` carries that ring verbatim, so
material inside it is not reduced and the bench skin is out of the competition by construction;
the constrained row reproduces that model and lands on the mechanism the figure draws.

Part 1's 1.88 is a *different* model's number and is not that comparison's partner. It came from
the RS2-native `#004` model, which carries **no constraint polygon at all** — an unconstrained run
that nonetheless reports the crest/core band — so the unconstrained row is anchored on the closed
form instead. The two vendor numbers landing within 1.1% of each other is a consequence of RS2
finding the same band either way, not evidence that the exclusion area is inert. Slide2's 1.948
and the ACADS referee 1.95 are limit-equilibrium answers on the gentler **upstream** face, where
every LEM method collapses to tan φ / tan β, and [RS2 Part IV VP6](#p4-vp6) is a third station on
the same dam: confining reduction to RS2's upstream SSR *Search* Area holds the mechanism on
ACADS 2(b)'s specified circle.

**Mesh.** Both rows are locked at the 6.5 m tri6 mesh, 3 166 elements against the vendor model's
2 204, so XSLOPE's mesh is the finer of the two, and both mechanisms drift mildly downward under
refinement. Everything else matches the vendor `.fea` field by field: geometry, the four zones'
strengths, E = 50 000 kPa, ν = 0.4, and the per-material tensile caps 0 / 0 / 0 / 85 kPa held
static under reduction (`tensilestrength_SRF: 0`).

<!-- test: file=files/rocscience/vp005.xlsx, type=mesh_elements, element_type=tri6, target_size=6.5, expected_elements=3166, benchmark=RS2-4-mesh -->
<!-- test: file=files/rocscience/vp005.xlsx, type=fem_ssrm, expected_fs=1.672, element_type=tri6, target_size=6.5, tolerance=0.01, f_min=1.5, f_max=2.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-4 -->
<!-- test: file=files/rocscience/vp005.xlsx, type=fem_ssrm, expected_fs=1.894, element_type=tri6, target_size=6.5, tolerance=0.02, f_min=1.5, f_max=2.3, max_iter=16000, tension_srf=false, k0=1, ssr_zone=0;0;315.5;162;319.5;162;321.6;162;327.6;162;386.9;130.6;386.9;0, benchmark=RS2-4-zone -->

**Unconstrained — the downstream bench skin (vp005)**

![RS2-4: the dry Talbingo dam solved unconstrained, SSRM 1.672 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the strain a thin surface band on the steepest downstream bench segments](images/RS2-4.png)

**Under Part 4's SSR Exclusion Area — the crest / core band (vp005)**

![RS2-4 with the downstream shell held at full strength by Part 4's SSR Exclusion Area, SSRM 1.894 against Part 4's SSR 1.9 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the mechanism at the top of the inclined clay core, fanning down its upstream flank](images/RS2-4-zone.png)

### RS2-5: Water table with weak seam {#rs2-5}

Slide2 counterpart: **VP7** (inventory-only on the LEM page — no detail section to link).

**Input files:** [xslope_acads_weak_layer.xlsx](../lem/files/xslope_acads_weak_layer.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | ACADS referee |
|---|---|---|---|---|
| SSRM | 1.280 | 1.26 (+1.6%) | Spencer 1.258 | 1.24–1.27 (+0.8%) |

The geometry and both material strengths reproduce the RS2 verification `.fez` for this
problem exactly. Its groundwater setup, however, differs: the library `.fez` supplied for
Problem 5 carries no water table (a dry variant, pore pressure zero at every node), whereas
the manual's problem statement — "Water Table with Weak Seam" — and this reconstruction both
place the phreatic surface at the base of the weak seam (y = 26.5). Because that seam is
purely frictional (c = 0, φ = 10°), the water table is what drives the factor down to the
published 1.26; XSLOPE's wet reconstruction reproduces that value (1.280), so the file is
kept as the faithful build of the published problem.

<!-- test: file=../lem/files/xslope_acads_weak_layer.xlsx, type=fem_ssrm, expected_fs=1.280, element_type=tri6, target_size=2.0, tolerance=0.01, f_min=0.9, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-5 -->

![RS2-5: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-5.png)

### RS2-6: Slope with load and pore pressure by water table (ACADS 4) {#rs2-6}

Slide2 counterpart: [VP9](rocscience.md#vp9). Built with a caveat.

**Input files:** [vp009.xlsx](files/rocscience/vp009.xlsx)

| Method | XSLOPE | ACADS referee | RS2 SSRM | ACADS survey mean | Slide2 LEM | XSLOPE LEM |
|---|---|---|---|---|---|---|
| SSRM | 0.777 | 0.78 (−0.4%) | 0.69 (+12.6%) | 0.808 | 0.68–0.71 (MC-optimized) | 0.724 |

XSLOPE's SSRM lands on the ACADS referee value but sits +12.6% above RS2's SSRM, and above
Slide2's LEM as well — the published values for this thin-weak-seam problem are widely spread,
as they are at [#16](#rs2-16).

<!-- test: file=files/rocscience/vp009.xlsx, type=fem_ssrm, expected_fs=0.777, element_type=tri6, target_size=1.3, tolerance=0.02, f_min=0.3, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-6 -->

![RS2-6: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-6.png)

### RS2-7: Pore pressure by digitized total head grid (ACADS 5) {#rs2-7}

Slide2 counterpart: [VP10](rocscience.md#vp10).

**Input files:** [vp010.xlsx](files/rocscience/vp010.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | Giam |
|---|---|---|---|---|
| SSRM | 1.483 | 1.48 (+0.2%) | 1.498–1.501 | 1.53 (−3.1%) |

The SSRM runs on the FE-seepage model XSLOPE built for Slide2 [VP10](rocscience.md#vp10) (the
grid is a stand-in for the flow solution; sidecars are tri6 so the SSRM plasticity is not
volumetrically locked).

<!-- test: file=files/rocscience/vp010.xlsx, type=fem_ssrm, expected_fs=1.483, tolerance=0.01, f_min=1.0, f_max=2.2, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-7 -->

![RS2-7: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-7.png)

### RS2-8: Saint-Alban test embankment {#rs2-8}

Slide2 counterpart: [VP11](rocscience.md#vp11).

| Method | XSLOPE | RS2 SSRM | Pilot |
|---|---|---|---|
| SSRM | *no lock possible* | 0.96 | 1.04 recorded |

The grid encodes measured construction-induced pressures (see the Slide2 corpus VP11 row) rather
than a computed flow field, and the manual states it as equal-pressure lines drawn on the geometry
figure rather than as a coordinate table, so there is nothing here XSLOPE can reproduce as a lock.
Its companion [RS2-9](#rs2-9) prints its grid as a table and is built.

### RS2-9: Cubzac-les-Ponts test embankment {#rs2-9}

Slide2 counterpart: [VP13](rocscience.md#vp13).

**Input files:** [rs2_9.xlsx](files/rocscience/rs2_9.xlsx) — with the
`rs2_9_mesh.json` / `rs2_9_seep.csv` sidecars beside it, which carry the mesh and its nodal pore
pressures.

A 4.5 m embankment (c' = 0, φ' = 35°, γ = 21.2 kN/m³) on 9 m of soft clay — 3 m of upper clay
(c' = 10 kPa, φ' = 24°, γ = 15.5 kN/m³) over 6 m of lower clay (10 kPa, 28.4°, 15.5) — built and
loaded to failure in 1974. Two features of the problem set it apart from the rest of the corpus,
and the file carries both explicitly.

**The pore pressures are measured, not computed.** They are construction-induced pressures under
an embankment taken to failure, with no flow field behind them. The manual prints them as a
44-point table — four equal-pressure contours crossed at thirteen stations — and draws the water
table at el 8, where u = 0 across the full width; the vendor model carries that line as 51 further
grid points, 95 in all. The manual also names the interpolation it used, a thin plate spline, so
the file's pore-pressure sidecar is that spline through the same 95 points, evaluated on the file's
own mesh and clamped at u ≥ 0. It reproduces all 44 printed points exactly, and every node it takes
negative lies at or above el 8, where the section is unsaturated and RS2 reads no pore pressure
either. The `u = 'seep'` sidecar is **synthesized from published data** rather than solved by
XSLOPE or imported from a vendor field, and the builder records where every number came from.

**The face is held elastic.** From the manual: "Verification is for a deep failure so support of
the face is required since the factor of safety against embankment face failure is 1.11. This is
accomplished by using a thin layer of elastic (infinite strength) material on the face of the
embankment." The vendor model pins that layer down exactly — the quad (25.5, 9) – (19, 13.5) –
(20, 13.5) – (26.5, 9), 4.5 m², 0.9% of the domain — so it is transcribed as its own material and
run through the tag's `elastic_materials`, as [RS2-23](#rs2-23) carries its own.

| Method | XSLOPE | RS2 SSRM | Pilot |
|---|---|---|---|
| SSRM (1.0 m mesh) | 1.320 | 1.31 (+0.8%) | Bishop 1.24 recorded |

ψ = 0. The tensile caps are the vendor model's — T = 0 on the embankment, 10 kPa on both clays —
held static through the reduction (`tensilestrength_SRF = 0`), and E = 50 000 kPa / ν = 0.4
throughout is the vendor model's own.

<!-- test: file=files/rocscience/rs2_9.xlsx, type=fem_ssrm, expected_fs=1.320, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.8, f_max=2.2, max_iter=16000, tension_srf=false, k0=1, elastic_materials=Embankment (elastic face skin), benchmark=RS2-9 -->

![RS2-9: Cubzac-les-Ponts test embankment, SSRM 1.320 vs RS2 SSR 1.31 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-9.png)

### RS2-10: Simple slope II (Arai & Tagyo ex. 1) {#rs2-10}

Slide2 counterpart: [VP14](rocscience.md#vp14) (Arai & Tagyo 1).

**Input files:** [xslope_arai_tagyo.xlsx](../lem/files/xslope_arai_tagyo.xlsx)

| Method | XSLOPE | RS2 SSRM | XSLOPE LEM | Slide2 LEM |
|---|---|---|---|---|
| SSRM | 1.411 | 1.40 (+0.8%) | Bishop 1.404 / Spencer 1.401 | 1.409 / 1.406 |

<!-- test: file=../lem/files/xslope_arai_tagyo.xlsx, type=fem_ssrm, expected_fs=1.411, element_type=tri6, target_size=2.2, tolerance=0.02, f_min=1.2, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-10 -->

![RS2-10: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-10.png)

### RS2-11: Layered slope (Arai & Tagyo ex. 2) {#rs2-11}

Slide2 counterpart: [VP15](rocscience.md#vp15).

**Input files:** [vp015.xlsx](files/rocscience/vp015.xlsx)

| Method | XSLOPE | RS2 SSRM | Greco/Kim pattern search | XSLOPE LEM |
|---|---|---|---|---|
| SSRM | 0.406 | 0.41 (−1.0%) | 0.39–0.43 | 0.419–0.422 |

*Scored against Part IV VP15's RS2 SSRM 0.41, the value published for the model vp015.xlsx is
built from. RS2 ran this deck twice on input-identical models that differ only in how the strength
reduction treats tension — the native `#011` run reduces tensile strength brittly (residual
T = 0), the Part IV `#015` import holds it perfectly plastic (T<sub>r</sub> = T), which is what
XSLOPE's FEM does — and publishes 0.39 for the native one, so XSLOPE sits inside the vendor's own
spread on identical inputs. The 0.39–0.43 column is a band stitched from Greco's and Kim's
separate pattern searches, which the page's conventions exclude, and Arai & Tagyo's own factor is
a Bishop value.*

<!-- test: file=files/rocscience/vp015.xlsx, type=fem_ssrm, expected_fs=0.406, element_type=tri6, target_size=1.9, tolerance=0.02, f_min=0.25, f_max=0.65, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-11 -->

![RS2-11: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-11.png)

### RS2-12: Simple slope + water table (Arai & Tagyo ex. 3) {#rs2-12}

Slide2 counterpart: [VP16](rocscience.md#vp16).

**Input files:** [vp016.xlsx](files/rocscience/vp016.xlsx)

| Method | XSLOPE | RS2 SSRM | XSLOPE LEM |
|---|---|---|---|
| SSRM | 1.098 | 1.09 (+0.7%) | Bishop 1.112 / Spencer 1.113 |

The FEM piezo pore pressure uses the vertical-distance convention, consistent with the LEM
slicer and the published analyses.

<!-- test: file=files/rocscience/vp016.xlsx, type=fem_ssrm, expected_fs=1.098, element_type=tri6, target_size=1.3, tolerance=0.02, f_min=0.9, f_max=1.45, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-12 -->

![RS2-12: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-12.png)

### RS2-13: Simple slope III (Yamagami & Ueta) {#rs2-13}

Slide2 counterpart: [VP17](rocscience.md#vp17).

**Input files:** [vp017.xlsx](files/rocscience/vp017.xlsx)

| Method | XSLOPE | RS2 SSRM | Greco Spencer | XSLOPE LEM | Yamagami & Ueta |
|---|---|---|---|---|---|
| SSRM | 1.332 | 1.33 (+0.2%) | 1.33 | Bishop 1.342 / Spencer 1.340 | 1.348 / 1.339 |

<!-- test: file=files/rocscience/vp017.xlsx, type=fem_ssrm, expected_fs=1.332, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=1.1, f_max=1.65, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-13 -->

![RS2-13: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-13.png)

### RS2-14: Simple slope, pore pressure by r<sub>u</sub> {#rs2-14}

Slide2 counterpart: [VP18](rocscience.md#vp18) (this problem is Slide2 VP18, not VP21). Built
with a caveat.

**Input files:** [vp018.xlsx](files/rocscience/vp018.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 Spencer | Baker | XSLOPE LEM |
|---|---|---|---|---|---|
| SSRM (regression lock at the 2.0 m mesh) | 0.916 | 0.98 (−6.5%) | 1.01 | 1.02 | Spencer 1.033 |

The SSRM factor on *this* model does not become mesh-independent: 0.972 → 0.916 → 0.859 → 0.859
as the target size goes 2.8 → 2.0 → 1.4 → 1.0 m, the last two rungs landing in one cell of the
strength-reduction bracket rather than on a demonstrated plateau. The tag pins 2.0 m as a
regression lock, chosen mid-sweep rather than at either end. The drift belongs to the
pore-pressure state rather than to the geometry: with r<sub>u</sub> = 0.5 half the overburden is
canceled, leaving so little effective confinement that the shear band keeps localizing as the
elements shrink, and a tension cutoff changes nothing. The same loading makes [#27](#rs2-27)
mesh-sensitive at the milder r<sub>u</sub> = 0.2, where it settles instead of drifting.

<!-- test: file=files/rocscience/vp018.xlsx, type=fem_ssrm, expected_fs=0.972, element_type=tri6, target_size=2.8, tolerance=0.02, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-14-m2.8 -->
<!-- test: file=files/rocscience/vp018.xlsx, type=fem_ssrm, expected_fs=0.859, element_type=tri6, target_size=1.4, tolerance=0.02, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-14-m1.4 -->
<!-- test: file=files/rocscience/vp018.xlsx, type=fem_ssrm, expected_fs=0.859, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-14-m1.0 -->
<!-- test: file=files/rocscience/vp018.xlsx, type=fem_ssrm, expected_fs=0.916, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-14 -->

![RS2-14: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-14.png)

### RS2-15: Layered slope II (Greco ex. 4 / Yamagami & Ueta) {#rs2-15}

Slide2 counterpart: [VP19](rocscience.md#vp19).

**Input files:** [vp019.xlsx](files/rocscience/vp019.xlsx)

| Method | XSLOPE | RS2 SSRM (Part IV VP19) | Slide2 Spencer | Greco |
|---|---|---|---|---|
| SSRM | 1.372 | 1.38 (−0.6%) | 1.398 | 1.40–1.42 |

This file is the Slide2 VP19 model, so its pairing is Part IV VP19's SSR **1.38** (−0.6%). RS2's
Part IV model constrains that run — its `.fez` carries a four-vertex SSR Search Area, the manual
noting it "was used to define the slope limits in RS2" — where the corpus run is unconstrained;
the two agree anyway, and RS2's own native rebuild (Part I problem 15, unconstrained) publishes
1.39 on the same slope, so nothing on this problem turns on the constraint.

<!-- test: file=files/rocscience/vp019.xlsx, type=fem_ssrm, expected_fs=1.372, element_type=tri6, target_size=4.33, tolerance=0.02, f_min=1.1, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-15 -->

![RS2-15: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-15.png)

### RS2-16: Layered slope and water table with weak seam (Greco ex. 5 / Chen & Shao) {#rs2-16}

Slide2 counterpart: [VP20](rocscience.md#vp20).

**Input files:** [vp020.xlsx](files/rocscience/vp020.xlsx)

| Method | XSLOPE | Governing | RS2 SSRM | Slide2 Spencer | XSLOPE LEM |
|---|---|---|---|---|---|
| SSRM | 0.978 | Greco 0.973–1.1 (inside) | 1.02 (−4.1%) | 1.093 circular / 1.007 noncircular | 1.086–1.091 |

*Greco's own published range is the source author's factor and governs; RS2's SSRM is the
same-method vendor pairing at −4.1%. Nearly mesh-invariant: 0.978 at 4.0 and 3.0 m, easing to
0.959 at 2.2 m. The LEM locks
run on the same file.*

The model's base is an *inclined* polygon boundary. Displacements are fixed along the whole
bottom polyline (see [#22](#rs2-22)) rather than only at the nodes of the single lowest
elevation; supported at one corner alone, a body on an inclined base reaches equilibrium at
no F at all.

<!-- test: file=files/rocscience/vp020.xlsx, type=fem_ssrm, expected_fs=0.978, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-16-m4.0 -->
<!-- test: file=files/rocscience/vp020.xlsx, type=fem_ssrm, expected_fs=0.959, element_type=tri6, target_size=2.2, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-16-m2.2 -->
<!-- test: file=files/rocscience/vp020.xlsx, type=fem_ssrm, expected_fs=0.978, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-16 -->

![RS2-16: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-16.png)

### RS2-17: Slope with three pore pressure conditions (Fredlund & Krahn) {#rs2-17}

Slide2 counterpart: [VP21](rocscience.md#vp21).
Built for the dry and r<sub>u</sub> cases.

**Input files:** [vp021a.xlsx](files/rocscience/vp021a.xlsx),
[vp021b.xlsx](files/rocscience/vp021b.xlsx)

| Method | XSLOPE | RS2 SSRM (Part IV VP21) | Slide2 | Fredlund & Krahn |
|---|---|---|---|---|
| SSRM (vp021a, dry) | 1.987 | 1.98 (+0.4%) | M-P 2.075 | 2.076 |
| SSRM (vp021b, r<sub>u</sub> = 0.25) | 1.692 | 1.68 (+0.7%) | 1.760–1.763 | 1.761–1.766 |

Both files are the Slide2 VP21 model, so the pairing is Part IV VP21's SSR column. Neither that
model nor RS2's own native rebuild carries an SSR polygon on any case. The water-table case
(VP21 case 3) is not built.

<!-- test: file=files/rocscience/vp021a.xlsx, type=fem_ssrm, expected_fs=1.987, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.6, f_max=2.5, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-17 -->
<!-- test: file=files/rocscience/vp021b.xlsx, type=fem_ssrm, expected_fs=1.692, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.2, f_max=2.2, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-17b -->

**Dry case (vp021a)**

![RS2-17: dry case (vp021a) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-17.png)

**r<sub>u</sub> = 0.25 case (vp021b)**

![RS2-17b: r<sub>u</sub> = 0.25 case (vp021b) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-17b.png)

### RS2-18: Three pore pressure conditions and a weak seam (Fredlund & Krahn) {#rs2-18}

Slide2 counterpart: [VP22](rocscience.md#vp22). Built for the dry and r<sub>u</sub> cases.

**Input files:** [vp022a.xlsx](files/rocscience/vp022a.xlsx),
[vp022b.xlsx](files/rocscience/vp022b.xlsx)

| Method | XSLOPE | RS2 SSRM (native) | RS2 SSRM (Part IV) | Slide2 | Fredlund & Krahn |
|---|---|---|---|---|---|
| SSRM (vp022a, dry) | 1.323 | 1.34 | 1.26 (+5.0%) | Bishop 1.382 | — |
| SSRM (vp022b, r<sub>u</sub> = 0.25) | 1.042 | 1.05 | 0.99 (+5.3%) | 1.124 | 1.124 |

*Both files are the Slide2 VP22 model, so the Part IV column is the pairing. The native column is
the same vendor's second solution of the same problem, −1.3% and −0.8% from XSLOPE.*

This one returns the *same* factor at 3.0 m and 2.0 m — the mechanism is pinned by the weak
seam, a geometric feature, so it cannot migrate with refinement. The contrast with
[#14](#rs2-14) is the point: there, nothing pins the band. The water-table case is not built.

**RS2 solved this problem twice, and both runs are unconstrained.** The Part IV `.fez` files for
cases 1 and 2 carry no SSR polygon (only the unbuilt case 3, water table, does), and the native
rebuild is unconstrained as well over identical geometry, which makes the native column an
informative second reading rather than a second pairing. The two vendor answers are about 6%
apart on cases 1 and 2 — wider than the distance from either of them to XSLOPE — and the dot
follows the Part IV pairing, so this row is scored at the wider of the two.

<!-- test: file=files/rocscience/vp022a.xlsx, type=fem_ssrm, expected_fs=1.323, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=1.0, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-18-m2.0 -->
<!-- test: file=files/rocscience/vp022a.xlsx, type=fem_ssrm, expected_fs=1.323, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.0, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-18 -->
<!-- test: file=files/rocscience/vp022b.xlsx, type=fem_ssrm, expected_fs=1.042, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.8, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-18b -->

**Dry case (vp022a)**

![RS2-18: dry case (vp022a) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-18.png)

**r<sub>u</sub> = 0.25 case (vp022b)**

![RS2-18b: r<sub>u</sub> = 0.25 case (vp022b) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-18b.png)

### RS2-19: Undrained layered slope (Low 1989) {#rs2-19}

Slide2 counterpart: [VP24](rocscience.md#vp24) (this problem is Slide2 VP24). Built with a
caveat.

**Input files:** [vp024.xlsx](files/rocscience/vp024.xlsx)

| Method | XSLOPE | Governing | RS2 SSRM | Slide2 LEM |
|---|---|---|---|---|
| SSRM | 1.477 at the tagged mesh | Low 1.44 (+2.6%) | 1.41 (+4.8%) | 1.439 |

*Low's own factor is the source author's and governs; RS2's SSRM is the same-method vendor
pairing at +4.8%, and the two SSRM values straddle the LEM.*

The geometry follows the RS2 vendor `.fez`: three equal 4.5 m layers (crest y = 13.5, slope
break x = 33.5), which makes the weak Middle layer (c = 20) a full 4.5 m thick.

<!-- test: file=files/rocscience/vp024.xlsx, type=fem_ssrm, expected_fs=1.477, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=1.1, f_max=1.8, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-19 -->

![RS2-19: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-19.png)

### RS2-20: Slope with vertical load (Prandtl's wedge) {#rs2-20}

Slide2 counterpart: [VP25](rocscience.md#vp25).

**Input files:** [vp025.xlsx](files/rocscience/vp025.xlsx)

| Method | XSLOPE | RS2 SSRM (Part IV VP25) | Prandtl theory | Slide2 Spencer |
|---|---|---|---|---|
| SSRM | 1.003 | 1.01 (−0.7%) | 1.0 (+0.3%) | 1.051 on the specified surface |

The file is the Slide2 VP25 model, so its pairing is Part IV VP25's SSR **1.01** (−0.7%). That
vendor run was constrained — `#025.fez` carries a ten-vertex SSR Exclusion Area, which the manual
says was used "to ensure the predetermined Slide2 geometry" — where the corpus run is
unconstrained; on this problem the mechanism is the Prandtl wedge either way, and RS2's own
unconstrained native rebuild (Part I problem 20) publishes 1.0, the closed form's own value.

<!-- test: file=files/rocscience/vp025.xlsx, type=fem_ssrm, expected_fs=1.003, element_type=tri6, target_size=0.8, tolerance=0.01, f_min=0.5, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-20 -->

![RS2-20: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-20.png)

### RS2-21: Bearing capacity test prism (Prandtl II) {#rs2-21}

Slide2 counterpart: [VP26](rocscience.md#vp26).

**Input files:** [vp026.xlsx](files/rocscience/vp026.xlsx)

| Method | XSLOPE | RS2 SSRM | Prandtl theory | Slide2 Spencer |
|---|---|---|---|---|
| SSRM | 1.003 | 1.01 (−0.7%) | 1.0 (+0.3%) | 0.941 on the specified surface |

*The SSRM converges on the theory value from above.*

<!-- test: file=files/rocscience/vp026.xlsx, type=fem_ssrm, expected_fs=1.003, element_type=tri6, target_size=0.8, tolerance=0.01, f_min=0.5, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-21 -->

![RS2-21: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-21.png)

### RS2-22: Layered slope with undulating bedrock {#rs2-22}

Slide2 counterpart: [VP27](rocscience.md#vp27). Built on an SSRM variant.

**Input files:** [vp027_fem.xlsx](files/rocscience/vp027_fem.xlsx)

| Method | XSLOPE | Published |
|---|---|---|
| SSRM | 1.534 | RS2 SSRM 1.52 (+0.9%) |

*Measured on the vendor's own model formulation.*

Two features of the FEM matter on this model. Displacements are fixed along the whole bottom
*polyline* of the domain rather than only the nodes at the lowest elevation, which an
undulating bedrock base requires (as at [#16](#rs2-16)); and the FEM applies the
phreatic-inclination (Hu) correction this problem specifies, matching the LEM's
Type=phreatic path.

The SSRM runs on [vp027_fem.xlsx](files/rocscience/vp027_fem.xlsx), which reconstructs the RS2
vendor `.fez`. The published model caps the crest with a **zero-strength** layer (c = 0, φ = 0), a
limit-equilibrium device with no continuum equivalent, so the vendor does not mesh that cap as a
material at all: it applies the cap's dead weight as two boundary distributed loads on a
single-material continuum at a constant γ = 124.2 pcf. This reconstruction adopts that formulation
in every respect — loads, magnitudes, extents, unit weight, the vendor's 9-vertex Hu-corrected
water table, and the load **direction**.

**The load direction matters here.** The vendor declares both crest loads `type: "vertical"`:
dead weight, with no horizontal component. XSLOPE's default is to apply a distributed load
perpendicular to the loaded surface, which is right for water pressure and wrong for a surcharge;
the `dloads` sheet's [Direction](../usage/input_template.md#worksheet-dloads) option selects
between the two, and this file sets both blocks to `vertical`. The loaded crest runs
(101, 88) → (200, 99), an inclination of 6.34°, so the surface-normal reading would add a
horizontal thrust of tan 6.34° = 11.1% of the surcharge, directed into the hill and against the
sliding direction — i.e. stabilizing, and enough to lift the factor above the vendor's own value.

vp027's LEM locks stand on the as-published [vp027.xlsx](files/rocscience/vp027.xlsx), which carries no
distributed loads at all and is unaffected.

<!-- test: file=files/rocscience/vp027_fem.xlsx, type=fem_ssrm, expected_fs=1.534, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.2, f_max=1.9, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-22 -->

![RS2-22: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-22.png)

### RS2-23: Underwater slope with linearly varying cohesion {#rs2-23}

Slide2 counterpart: [VP29](rocscience.md#vp29). Duncan's (2000) LASH terminal slope at the
Port of San Francisco: San Francisco Bay Mud, S<sub>u</sub> = 100 psf at el. −20 growing
9.8 psf/ft with depth, γ = 100 pcf, fully submerged below el. 0.

**Input files:** [vp029_split.xlsx](files/rocscience/vp029_split.xlsx) — the
[VP29](rocscience.md#vp29) model with RS2's own strength-reduction constraint carried as a
material partition.

**Where RS2's "can't fail" region is.** The published text places the elastic region "above
elevation −20 and to the right of the bench". The vendor model places it elsewhere: in
`slope stability #023` the Mohr-Coulomb elements (471 of 969) union to a seven-vertex polygon
that is a **full-depth vertical band** between two clean cuts at x = 70.755 and x = 350.168, the
same two x values the file carries as internal material boundary lines. The corpus file
reproduces that band, which covers 48.8% of the domain by area against the vendor's own 48.9%
element-area fraction; the two pieces outside it carry identical soil properties and are held
elastic at solve time. Both materials take the vendor's elastic pair (ν = 0.4, E = 10⁶ psf) and
the band carries `rock1`'s cap T = 100 psf.

| Case | XSLOPE SSRM | RS2 SSRM | LEM anchor ([VP29](rocscience.md#vp29)) |
|---|---|---|---|
| Under RS2's own partition (vp029_split) | **1.112** | 1.12 (−0.7%) | Spencer 1.145 on Duncan's surface |
| Same model, partition removed | 0.215 | — | — |

The second row is what makes the first a comparison rather than a coincidence. Remove the
partition from the same model and the reduction goes straight to the shallow skin above
el. −20; nothing else changes between the two, so the constrained factor is a measurement of the
vendor's constraint acting on this slope's mechanics.

<!-- test: file=files/rocscience/vp029_split.xlsx, type=fem_ssrm, expected_fs=0.215, element_type=tri6, target_size=6.0, tolerance=0.02, f_min=0.1, f_max=1.5, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-23-nopartition -->
<!-- test: file=files/rocscience/vp029_split.xlsx, type=fem_ssrm, expected_fs=1.112, element_type=tri6, target_size=6.0, tolerance=0.02, f_min=0.8, f_max=1.5, max_iter=16000, tension_srf=false, k0=1, elastic_materials=Bay Mud (elastic outer 1);Bay Mud (elastic outer 2), benchmark=RS2-23 -->

![RS2-23: LASH terminal underwater slope (Duncan 2000) under RS2's own elastic partition, SSRM 1.112 vs RS2 SSRM 1.12 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-23.png)

### RS2-24: Layered slope with geosynthetic reinforcement {#rs2-24}

Slide2 counterpart: [VP32](rocscience.md#vp32).

The problem is a 7 m and an 8.75 m embankment of two cohesionless fills on five soft clay layers,
with a single geosynthetic sheet at the fill base (Borges & Cardoso 2002).

| Published | RS2 SSR (Part I, 7 m / 8.75 m) | RS2 SSR (Part IV, three cases) |
|---|---|---|
| Borges & Cardoso 2002 | 1.15 / 0.95 | 1.24 / 1.21 / 0.98 |

**The SSR rows are not attempted.** RS2 does not mesh the section as one body. Its `#024` models
split the solid mesh along the geotextile into two, 39 coincident node pairs joined by frictional slip
joints (c = 0, φ = 30.96°), with the geotextile itself as tension-only beam elements
(EA = 200 000 kN/m, Ft = 200 kN/m) running along the split — so the load path between embankment
and foundation passes through a sliding interface. XSLOPE meshes a bonded continuum and has no
interface element, so that sliding joint has no XSLOPE counterpart, and no XSLOPE run stands
opposite the published factors. All five vendor models are built this way — the two native `#024`
models and the three `#032` Slide2 imports.

The limit-equilibrium side of this problem is built and locked as Slide2
[VP32](rocscience.md#vp32) — Bishop and Spencer on the three published circles, where the
geosynthetic enters as a force rather than through an interface.

### RS2-25: Syncrude tailings dyke (El-Ramly et al. 2003) {#rs2-25}

Slide2 counterpart: [VP33](rocscience.md#vp33). Built with a caveat.

**Input files:** [vp033.xlsx](files/rocscience/vp033.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 | El-Ramly | XSLOPE LEM |
|---|---|---|---|---|---|
| SSRM | 1.202 | 1.29 (−6.8%) | Bishop 1.305 | 1.31 | 1.320 on Slide's circle |

Geometry, material zonation, unit weights and elastic constants follow the RS2 vendor `.fez`
(`slope stability #025.fez`): the 15-vertex external boundary, the four internal material
interfaces, the diagonal Pgc/Kca wedge cut, and ν = 0.4 with E = 50 000 kPa on every zone. The
vendor file gives Clayey till (Pgc) φ = 7.5°, equal to the clay-shale.

**Refinement does not close the deficit; it widens it.** The Glacio-fluvial sand band is only
3.3 m thick, thinner than one element at the tagged 5 m size, so resolution is the natural place to
look for a −6.8% deficit. It is not there: at a 2.5 m target size the model meshes to 5 239
elements against the tagged mesh's 1 457 and the strength reduction reads **1.174**, further below
RS2's 1.29 rather than nearer it, with finer meshes continuing in the same direction. Nor is the
tagged mesh coarse against the vendor's own, which solves this dyke at 3 527 nodes and 1 698
quadratic triangles against the tag's 3 080 and 1 457.

**The corpus file carries one piezometric line where the vendor model carries two.** This is the
problem RS2 titles *"…with Multiple Phreatic Surfaces"*: its `.fea` assigns one piezometric line to
the Tailing sand and a second, 0.7–3.6 m lower, to the four zones beneath. The corpus file applies
the lower line throughout, so 577 m² of the Tailing sand that the vendor has saturated is dry here
and the pore pressure along the tailings-sand base runs about 20% low. That is a real difference
from the vendor model and it is the caveat on this row, but it is the *more* favorable of the two
readings, since less pore pressure makes a slope read stronger, so it cannot be what puts XSLOPE
below the vendor.

This dyke belongs with the small group of models on this page whose SSRM falls further below the
limit-equilibrium cluster on the same inputs than the usual strength-reduction margin, which is a
property of the solver rather than of this file: its geometry, strengths, unit weights and elastic
constants all match the vendor model field by field. The value is locked at the tagged mesh as a
regression anchor and the deficit is reported.

<!-- test: file=files/rocscience/vp033.xlsx, type=mesh_elements, element_type=tri6, target_size=5.0, expected_elements=1457, expected_nodes=3080, benchmark=RS2-25-mesh -->
<!-- test: file=files/rocscience/vp033.xlsx, type=mesh_elements, element_type=tri6, target_size=2.5, expected_elements=5239, benchmark=RS2-25-mesh-fine -->
<!-- test: file=files/rocscience/vp033.xlsx, type=fem_ssrm, expected_fs=1.174, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=0.9, f_max=1.8, max_iter=16000, k0=1, benchmark=RS2-25-m2.5 -->
<!-- test: file=files/rocscience/vp033.xlsx, type=fem_ssrm, expected_fs=1.202, element_type=tri6, target_size=5.0, tolerance=0.02, f_min=0.9, f_max=1.8, max_iter=16000, k0=1, benchmark=RS2-25 -->

![RS2-25: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-25.png)

### RS2-26: Clarence Cannon dam (Wolff & Harr 1987) {#rs2-26}

Slide2 counterpart: [VP34](rocscience.md#vp34).

**Input files:** [vp034.xlsx](files/rocscience/vp034.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 | Wolff & Harr | XSLOPE LEM |
|---|---|---|---|---|---|
| SSRM | 2.294 | 2.29 (+0.2%) | GLE 2.333 / Spencer 2.383 | 2.36 | M-P 2.384 |

This file reconstructs Slide2's VP34 model of the dam: polygon zones with the chimney drain, four
in all — Phase I and Phase II fill, a sand drain and a foundation sand. The RS2 vendor `.fez`
models the same dam with a more detailed six-zone section, adding a layered higher-strength
foundation, a distinct L-shaped filter drain and a downstream Spoil Fill wedge. Those extra zones
all sit **below or outside the governing mechanism** — the critical surface runs 45° through the
Phase II shell, horizontal along the Phase I base at el. 516, and exits at the downstream
waterline — so they are not reproduced here, and the file stays faithful to the Slide2 VP34 model
it is locked against.

The model's piezometric line stands above the downstream ground, so the section carries a pond
on the downstream face. Its weight is derived from the piezometric surface and applied as a
traction, which is what makes the piezometric line a sound full-field pore pressure here.

<!-- test: file=files/rocscience/vp034.xlsx, type=fem_ssrm, expected_fs=2.294, element_type=tri6, target_size=15.0, tolerance=0.02, f_min=1.7, f_max=3.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-26 -->

![RS2-26: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-26.png)

### RS2-27: Homogeneous slope, pore pressure by r<sub>u</sub> {#rs2-27}

Slide2 counterpart: [VP36](rocscience.md#vp36) (Li & Lumb 1987 / Hassan & Wolff 1999). Built;
the r<sub>u</sub> mesh-sensitivity documented on [RS2-14](#rs2-14) is mild enough here to settle.

**Input files:** [vp036.xlsx](files/rocscience/vp036.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 | Hassan & Wolff |
|---|---|---|---|---|
| SSRM (regression lock at the 1.0 m mesh) | 1.342 | 1.31 (+2.4%) | Bishop 1.339 | 1.334 (deterministic) |

This homogeneous 2:1 slope (c' = 18 kPa, φ' = 30°, γ = 18 kN/m³, r<sub>u</sub> = 0.2) is the
deterministic core of the [VP36](rocscience.md#vp36) reliability benchmark. Its r<sub>u</sub>
loading is the same mechanism that makes [RS2-14](#rs2-14) mesh-dependent — r<sub>u</sub> cancels
part of the confinement, and unregularized Mohr-Coulomb has no length scale to arrest a localizing
band — but the milder r<sub>u</sub> = 0.2 here settles rather than drifts: 1.373 / 1.342 / 1.342 at
1.5 / 1.0 / 0.7 m target sizes, flat from the tagged 1.0 m mesh down.

<!-- test: file=files/rocscience/vp036.xlsx, type=fem_ssrm, expected_fs=1.373, element_type=tri6, target_size=1.5, tolerance=0.02, f_min=1.1, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-27-m1.5 -->
<!-- test: file=files/rocscience/vp036.xlsx, type=fem_ssrm, expected_fs=1.342, element_type=tri6, target_size=0.7, tolerance=0.02, f_min=1.1, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-27-m0.7 -->
<!-- test: file=files/rocscience/vp036.xlsx, type=fem_ssrm, expected_fs=1.342, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=1.1, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-27 -->

![RS2-27: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-27.png)

### RS2-28: Excavated slope with FE groundwater and matric suction (Ng & Shi 1998) {#rs2-28}

Slide2 counterpart: [VP38](rocscience.md#vp38). A 28° Hong Kong cut (24 m soil over 6 m
bedrock); a steady unsaturated FE groundwater analysis at three far-field heads (H = 61 /
62 / 63 m) supplies both the positive and the negative (matric-suction) pore pressures, and
the SSRM reduces strength to failure. Material (manual Table 1): c′ = 10 kPa, φ′ = 38°,
φ_b = 15°, γ = 16 kN/m³.

**Input files:** [rs2_28a.xlsx](files/rocscience/rs2_28a.xlsx) /
[b](files/rocscience/rs2_28b.xlsx) / [c](files/rocscience/rs2_28c.xlsx) — geometry from the vendor
`.fea` external boundary, with XSLOPE's own steady unsaturated Gardner seepage supplying u because
the vendor result file is empty. The domain is split into a Mohr-Coulomb corridor near the cut and
an elastic outer zone, reproducing the vendor's own material partition; both materials carry its
elastic pair (ν = 0.4, E = 50 000 kPa), and the corridor carries `rock1`'s tensile cap T = 10 kPa,
held static through the reduction as the vendor model does.

**Which vendor model these files are built from.** This problem exists in the archive four ways
over the identical domain: RS2's native `#028_01/02/03`, one per far-field head, and both a native
and an imported copy of `#038-1/-2/-3`. The corpus files are built from the native `#028_0N`
boundary and its material partition, which holds **63%** of the domain elastic and draws no SSR
polygon at all — the partition itself is the constraint, where the `#038-*` variants hold 53% and
draw a polygon as well. So this row is scored against the Part I §28 values below.

| H | XSLOPE SSRM | RS2 (SSR) | Slide2 | [Ng & Shi (1998)](https://doi.org/10.1016/S0266-352X(97)00036-0) |
|---|---|---|---|---|
| 61 m | **1.669** | 1.64 (+1.8%) | 1.616 (+3.3%) | 1.636 (+2.0%) |
| 62 m | **1.544** | 1.55 (−0.4%) | 1.535 (+0.6%) | 1.527 (+1.1%) |
| 63 m | **1.406** | 1.41 (−0.3%) | 1.399 (+0.5%) | 1.436 (−2.1%) |

*Published values are from the RS2 *Slope Stability Verification Manual, Part 1*, §28
(Table 2). The manual's §38-derived cross-reference elsewhere quoting "1.56 / 1.46 / 1.32"
does not match this table.*

**The left edge is a boundary, not a slope.** The model is truncated far behind the cut, and the
vendor treats that face as a support: every node fixed in both directions, with a constant total
head of 6 m prescribed along the same line. It is drawn 0.13 m off vertical over its 30.7 m height,
so a literal transcription meshes it traction-free under up to +172 kPa of pore pressure, which
carries an effective *tension* beyond the Mohr-Coulomb apex at any strength-reduction factor and
equilibrates at no strength at all. The corpus files draw the edge exactly vertical, which is what
the vendor's restraint means physically.

**How suction is credited, and what caps it.** The manual's Table 1 gives Ng & Shi's modified
Mohr-Coulomb criterion, τ = c′ + (σ_n − u_a) tan φ′ + (u_a − u_w) tan φ_b with φ_b = 15°, and the
corridor material carries that angle. `rock1`'s tensile cap T = 10 kPa sits below its own
c′/tan φ′ apex of 12.8 kPa, and the suction credit raises that apex further wherever the soil is
unsaturated, so the cap is an active limit here rather than a formality; it is transcribed from
the vendor model and the locks are taken with it.

<!-- test: file=files/rocscience/rs2_28a.xlsx, type=fem_ssrm, expected_fs=1.669, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-28a -->

![RS2-28a: H = 61 m, SSRM 1.669 vs RS2 SSR 1.64 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-28a.png)

<!-- test: file=files/rocscience/rs2_28b.xlsx, type=fem_ssrm, expected_fs=1.544, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-28b -->

![RS2-28b: H = 62 m, SSRM 1.544 vs RS2 SSR 1.55 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-28b.png)

<!-- test: file=files/rocscience/rs2_28c.xlsx, type=fem_ssrm, expected_fs=1.406, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-28c -->

![RS2-28c: H = 63 m, SSRM 1.406 vs RS2 SSR 1.41 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-28c.png)

### RS2-29: Geosynthetic-reinforced embankment on soft soil (Tandjiria 2002) {#rs2-29}

Slide2 counterpart: [VP39](rocscience.md#vp39). The manual's §29/§30 headings are swapped.
Built for both published cases — the sand embankment first, then RS2's own clay model.

**Input files:** [vp039c.xlsx](files/rocscience/vp039c.xlsx) (sand) /
[rs2_29clay.xlsx](files/rocscience/rs2_29clay.xlsx) (clay)

| Method | XSLOPE | RS2 SSRM (Part IV VP39 case 3) | RS2 SSRM (native #29) | Slide2 Spencer | Tandjiria |
|---|---|---|---|---|---|
| SSRM (sand case, vp039c, unconstrained) | 1.219 | 1.22 (−0.1%) | 1.25 | 1.209 | 1.219 |

**Which vendor model this file is, and why it runs unconstrained.** vp039c is the Slide2 VP39
**case 3** model — sand fill, *no reinforcement* — so its pairing is Part IV VP39 case 3's SSR
**1.22**. That vendor model carries no SSR polygon — its `SSR_polygonal_zones` block is empty —
and neither does RS2's own native
rebuild of the same case, so the corpus run is unconstrained too and the three answers agree
within 2.5%. The exclusion area in this problem's `.fez` family belongs to a *different* case, the
reinforced sand embankment of case 4, and constrains that model rather than this one.

Unconstrained, the reduction localizes on a shallow compound surface through the c = 0 fill face
and the soft-clay toe, the above-tolerance band sitting at about 0.4 m median depth on the 6 m
embankment.

<!-- test: file=files/rocscience/vp039c.xlsx, type=fem_ssrm, expected_fs=1.219, element_type=tri6, target_size=0.7, tolerance=0.02, f_min=0.9, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-29 -->

![RS2-29: sand case (vp039c), unconstrained SSRM 1.219 vs RS2 Part IV VP39 case 3 SSR 1.22 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-29.png)

#### The clay case: RS2's tension crack is geometry

RS2 models the *unreinforced clay* embankment as a separate file
(`slope stability #029_clay`, published SSR **0.99**), and that model states the tension crack
**geometrically** rather than constitutively. The crest is cut 2.06 m down from the 9.0 m
embankment crest, exactly the theoretical crack depth 2c/γ = 2 × 20 / 19.4 = 2.06 m, and the
removed wedge's weight is put straight back on the cut surface as a vertical surcharge,
γ z = 39.964 kPa: uniform where the wedge was a full-thickness slab (x = 0–10) and tapering to
nothing where it thinned out against the 30° face (x = 13.568). Both materials are
Mohr-Coulomb c = 20 kPa, φ = 0, γ = 19.4 kN/m³, E = 50 000 kPa, ν = 0.4, each capped at
T = 20 kPa, and there is no water anywhere in the model.

`rs2_29clay.xlsx` transcribes that model on the vendor's own external boundary. Its toe sits at
x = 20.3923, which makes the face exactly 30°, where the Slide2 figure the vp039 family is
built from rounds the toe to x = 20; on the otherwise identical model that rounding is worth
+1.9% (0.978 → 0.997), so the two geometries are kept apart rather than shared.

| Method | XSLOPE | RS2 SSR (Part I #29, clay) | RS2 SSR (Part IV VP39 case 1) |
|---|---|---|---|
| SSRM (clay case, rs2_29clay) | 0.997 | 0.99 (+0.7%) | 0.97 |

Part I's 0.99 governs — it is the published factor for the model this file transcribes. Part
IV's VP39 case 1 is a *different* model of the same problem: it leaves the crest uncut and
splits the top 2 m off as its own zero-tension material zone instead.

**The brittle cap is not what decides it.** The vendor drops each material's tensile strength
from T = 20 to 0 the moment it fails in tension, a path XSLOPE's constant cap cannot follow. With
the crack already cut out of the geometry there is no crest tension left for the cap to govern,
and the model reads the same at the peak cap and at the residual.

<!-- test: file=files/rocscience/rs2_29clay.xlsx, type=fem_ssrm, expected_fs=0.997, element_type=tri6, target_size=0.7, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-29-clay -->

![RS2-29-clay: RS2's own clay model (rs2_29clay), SSRM 0.997 vs RS2 Part I SSR 0.99 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-29-clay.png)

### RS2-30: Homogeneous slope, power-curve strength (Perry 1993) {#rs2-30}

Slide2 counterpart: [VP40](rocscience.md#vp40). Swapped heading (see [#29](#rs2-29)).

**Input files:** [vp040.xlsx](files/rocscience/vp040.xlsx)

| Method | XSLOPE | RS2 SSR (Part IV VP40, constrained) | RS2 SSR (native #030, unconstrained) | Slide2 Janbu | Perry |
|---|---|---|---|---|---|
| SSRM, under the vendor model's own SSR exclusion areas | 1.023 | 0.97 (+5.5%) | 0.91 | 0.944 | 0.98 (+4.4%) |

The FEM linearizes the reduced envelope at the current stress per iteration.

**Which vendor model this file is.** Both RS2 models of this slope share the geometry exactly, so
the **strength model** decides it: `vp040.xlsx` carries Perry's power curve τ = A σ'<sup>b</sup>
with A = 2, b = 0.7, which is what the Slide2-import model `#040` carries, where RS2's native
rebuild `#030` carries a *Generalized Hoek-Brown* envelope fitted to the same data — the same
substitution its table labels explicitly at [#31](#rs2-31). The file is therefore the Part IV VP40
model, and its pairing is that model's published SSR **0.97**.

**The vendor's constraint is carried in the file.** `#040` draws three SSR exclusion areas — one
of them wholly interior, so the reducible region is a polygon with a hole along Perry's specified
failure surface — and the materials inside them are linear elastic, the same partition in strength
terms (50.65% of the domain by the vendor's own materials, 50.4% by the polygons), the two readings
agreeing to a quarter of a percent. The published 0.97 was produced with that constraint in place,
so `vp040.xlsx` carries all three rings as v20 polygon-sheet overlay rows under the **"SSR
elastic"** sentinel (Mat ID −3): the vendor gives these regions a material that cannot yield at
all, and on a sub-unity model a full-strength hold would not bracket the solve. Constrained that
way the reduction is pushed off the shallow band and the SSRM lands at **1.023**, +5.5% on the
published 0.97 — a like-for-like comparison the same-method pairing does not account for. RS2's own
native `#030` rebuild carries no constraint of any kind, and the column above records it.

<!-- test: file=files/rocscience/vp040.xlsx, type=fem_ssrm, expected_fs=1.023, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=0.5, f_max=1.5, max_iter=16000, k0=1, benchmark=RS2-30 -->

![RS2-30: constrained SSRM 1.023 vs RS2 Part IV VP40 SSR 0.97 — FEM inputs with the vendor's three SSR exclusion areas drawn as dashed "SSR elastic" outlines, mesh, max shear strain and displacement vectors at the critical SRF. The strain band runs along the lower edge of the held wedge, on Perry's specified surface](images/RS2-30.png)

### RS2-31: M-C vs power curve (Baker 2003 ex. 1) {#rs2-31}

Slide2 counterpart: [VP44](rocscience.md#vp44). Built, four cases.

**Input files:** [vp044a.xlsx](files/rocscience/vp044a.xlsx),
[vp044b.xlsx](files/rocscience/vp044b.xlsx),
[vp044c.xlsx](files/rocscience/vp044c.xlsx),
[vp044d.xlsx](files/rocscience/vp044d.xlsx)

| Case | XSLOPE SSRM | Governing published | Slide2 |
|---|---|---|---|
| vp044b — M-C, c′ = 11.64 kPa, φ′ = 24.7° | 1.529 | RS2 SSRM **1.53** (−0.1%) | — |
| vp044c — M-C, local-linear c′ = 0.39 kPa, φ′ = 38.6° | 0.969 | RS2 SSRM **0.98** (−1.1%) | — |
| vp044a — Baker's power curve, τ = 1.107·σ<sub>n</sub><sup>0.86</sup> | 0.973 | **Baker 0.97** (+0.3%) | Janbu 0.921 / Spencer 0.960 |
| vp044d — RS2's Generalized Hoek-Brown fit of that curve | 1.115 | RS2 SSRM **1.11** (+0.5%) | — |

**The power-curve problem is solved with two different strength models, and RS2 says so in
print.** Its Part 1 results table labels the row itself — "Power Curve | SRF (Generalized
Hoek-Brown) | 1.11" — and the vendor model matches: `slope stability #031-powecurve.fea` carries a
Generalized Hoek-Brown fit to Baker's curve, where the Slide2-import twin keeps the literal law
that vp044a carries. So the two vendor files confirm which *criterion* each program applies.

**Why the substitution matters on this slope.** The two envelopes cross at σ<sub>n</sub> ≈ 40 kPa,
and below it the fit is the stronger of the two — by 14% at 12.5 kPa, by 25% at 5 kPa and by 43% at
1 kPa. This 6 m slope never gets near the crossover: the effective normal stresses on its critical
surface run about 0.6–12.5 kPa (Slide2 publishes a maximum of 11.51 kPa for the same case), so the
fit hands the whole failure surface materially more strength than Baker's law does. That is why
RS2's 1.11 sits 15.6% above Slide2's own Spencer on an identical slope, and why the difference is a
strength-model difference rather than a solver one — the fit was made for a stress range this
slope does not reach.

**vp044d closes the comparison.** Carrying RS2's own envelope through XSLOPE's `hb` material
option, the SSRM returns **1.115** against RS2's 1.11 (+0.5%). Its four Hoek-Brown inputs —
σ<sub>ci</sub> = 113.132 kPa, GSI = 5, m<sub>i</sub> = 50, D = 0 — are **back-derived** from the
vendor's m<sub>b</sub> / s / a rather than published, reproducing all three to six significant
figures. The envelope's own tensile strength is nil, consistent with the power curve's T = 0, so
the file carries no cap.

<!-- test: file=files/rocscience/vp044b.xlsx, type=fem_ssrm, expected_fs=1.529, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=1.1, f_max=2.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-31a -->
<!-- test: file=files/rocscience/vp044c.xlsx, type=fem_ssrm, expected_fs=0.969, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=0.6, f_max=1.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-31b -->
<!-- test: file=files/rocscience/vp044a.xlsx, type=fem_ssrm, expected_fs=0.973, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=0.5, f_max=1.6, max_iter=16000, k0=1, benchmark=RS2-31c -->
<!-- test: file=files/rocscience/vp044d.xlsx, type=fem_ssrm, expected_fs=1.115, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=0.7, f_max=1.6, max_iter=16000, k0=1, benchmark=RS2-31d -->

**Mohr-Coulomb case (vp044b)**

![RS2-31a: Mohr-Coulomb case (vp044b, SSRM 1.529) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-31a.png)

**Mohr-Coulomb case (vp044c)**

![RS2-31b: Mohr-Coulomb case (vp044c, SSRM 0.969) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-31b.png)

**Power-curve case (vp044a)**

![RS2-31c: power-curve case (vp044a, SSRM 0.973) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-31c.png)

**RS2's Generalized Hoek-Brown fit of the same curve (vp044d)**

![RS2-31d: RS2's Generalized Hoek-Brown rendering of the power-curve case (vp044d, SSRM 1.115) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-31d.png)

### RS2-32: M-C vs power curve II (Baker 2003 ex. 2) {#rs2-32}

Slide2 counterpart: [VP45](rocscience.md#vp45). Built, both halves. The RS2 manual's problem 32
heading names a different problem from the one its body presents: the body is Baker's example 2,
the linear-versus-power-curve envelope pair reproduced here, the same off-by-one heading slip the
manual carries at §29/§30 and §33.

**Input files:** [vp045a.xlsx](files/rocscience/vp045a.xlsx),
[vp045b.xlsx](files/rocscience/vp045b.xlsx)

| Method | XSLOPE | RS2 SSRM (Part IV VP45) | RS2 SSRM (native #32, GHB fit) | Slide2 Spencer |
|---|---|---|---|---|
| SSRM (vp045a, M-C) | 2.790 | 2.83 (−1.4%) | — | — |
| SSRM (vp045b, power curve) | 2.637 | 2.63 (+0.3%) | 2.74 | 2.662 |

RS2 solves the power-curve half twice, on two different strength models. Part IV's VP45 model
carries the literal power law as a native `PowerCurve` plasticity material — the same strength
model vp045b carries — so that is the pairing this half is scored against. The Parts I–III native
model `#032-powercurve` instead re-expresses the same envelope as a fitted **Generalized
Hoek-Brown** material, and its published factor is that fit's answer rather than the power
curve's. Converting the fit back to shear–normal space (Balmer transform) shows it running a few
percent stronger than the literal curve over the slope's working-stress range, which is why it
sits above both power-curve answers.

<!-- test: file=files/rocscience/vp045a.xlsx, type=fem_ssrm, expected_fs=2.790, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=2.3, f_max=3.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-32 -->
<!-- test: file=files/rocscience/vp045b.xlsx, type=fem_ssrm, expected_fs=2.637, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=1.8, f_max=3.6, max_iter=16000, k0=1, benchmark=RS2-32b -->

**Mohr-Coulomb case (vp045a)**

![RS2-32: Mohr-Coulomb case (vp045a, SSRM 2.790) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-32.png)

**Power-curve case (vp045b)**

![RS2-32b: power-curve case (vp045b, SSRM 2.637) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-32b.png)

### RS2-33: Homogeneous slope with tension crack and water table (P&D test slope 2) {#rs2-33}

Slide2 counterpart: [VP56](rocscience.md#vp56). Swapped heading. Built with a caveat.

**Input files:** [vp056.xlsx](files/rocscience/vp056.xlsx)

| Method | XSLOPE | RS2 SSRM | Eight-program LEM table |
|---|---|---|---|
| SSRM | 1.269 | 1.28 (−0.9%) | 1.03–1.32 |

The model's dry tension crack has no FEM representation, worth ~2–3% here.

<!-- test: file=files/rocscience/vp056.xlsx, type=fem_ssrm, expected_fs=1.269, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.9, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-33 -->

![RS2-33: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-33.png)

### RS2-34: M-C vs power curve III (Baker 2003 ex. 3, London clay) {#rs2-34}

Slide2 counterpart: [VP61](rocscience.md#vp61). Built, both halves.

**Input files:** [vp061a.xlsx](files/rocscience/vp061a.xlsx),
[vp061b.xlsx](files/rocscience/vp061b.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 Spencer | Baker |
|---|---|---|---|---|
| SSRM (vp061b, M-C) | 1.373 | 1.38 (−0.5%) | — | — |
| SSRM (vp061a, power curve) | 1.497 | 1.47 (+1.8%) | 1.47 | 1.48 |

<!-- test: file=files/rocscience/vp061b.xlsx, type=fem_ssrm, expected_fs=1.373, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=1.0, f_max=1.9, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-34 -->
<!-- test: file=files/rocscience/vp061a.xlsx, type=fem_ssrm, expected_fs=1.497, element_type=tri6, target_size=0.5, tolerance=0.02, f_min=1.0, f_max=2.2, max_iter=16000, k0=1, benchmark=RS2-34b -->

**Mohr-Coulomb case (vp061b)**

![RS2-34: Mohr-Coulomb case (vp061b, SSRM 1.373) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-34.png)

**Power-curve case (vp061a)**

![RS2-34b: power-curve case (vp061a, SSRM 1.497) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-34b.png)

### RS2-36: Seepage analysis, homogeneous slope (D&W Fig 6.37) {#rs2-36}

Slide2 counterpart: [VP71](rocscience.md#vp71) (= Slide2 VP71, not
[VP70](rocscience.md#vp70)). Built, both cases.

**Input files:** [vp071a.xlsx](files/rocscience/vp071a.xlsx),
[vp071b.xlsx](files/rocscience/vp071b.xlsx)

| Method | XSLOPE | RS2 SSRM | Referee | XSLOPE LEM |
|---|---|---|---|---|
| SSRM (vp071a, FE seepage) | 1.111 | 1.12 (−0.8%) | 1.138 (−2.4%) | 1.132 |
| SSRM (vp071b, piezo approximation) | 1.111 | 1.12 (−0.8%) | 1.141 (−2.6%) | 1.132 |

The seep case runs on tri6 sidecars.

<!-- test: file=files/rocscience/vp071a.xlsx, type=fem_ssrm, expected_fs=1.111, tolerance=0.01, f_min=0.7, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-36a -->
<!-- test: file=files/rocscience/vp071b.xlsx, type=fem_ssrm, expected_fs=1.111, element_type=tri6, target_size=4.4, tolerance=0.01, f_min=0.7, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-36b -->

**FE-seepage case (vp071a)**

![RS2-36a: FE-seepage case (vp071a) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-36a.png)

**Piezometric-line case (vp071b)**

![RS2-36b: piezometric-line case (vp071b) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-36b.png)

### RS2-37: Embankment with layered foundation (D&W Fig 6.39) {#rs2-37}

Slide2 counterpart: [VP72](rocscience.md#vp72). Reported, no lock.

| Published | RS2 SSRM (table) | RS2 SSRM (convergence graph) | Slide2 | Referee |
|---|---|---|---|---|
| D&W Fig 6.39 | 0.95 | 1.1 | 1.15 / 1.16 | 1.11 |

The two programs are not finding the same mechanism — RS2's is the artesian downstream-toe slide,
where XSLOPE's strength reduction localizes on a deeper surface — so nothing here is locked and no
difference is derived. Reproducing the toe mechanism needs
toe-refined meshing — noted with the artesian-toe discussion in the Slide2
[VP72](rocscience.md#vp72) section. The vendor's own SSR polygon on this problem is a
mechanism-selection corridor of the [VP64](#p4-vp64) kind — a ~12.5 m band traced along the slip
surface it wants, 0.7% of the domain — and it is documented rather than carried: it is thinner
than this model's mesh, so transcribing it would rasterize to a band too ragged to form a
mechanism, and a finer mesh would be required first.

### RS2-38: Cohesionless embankment on saturated clay foundation (D&W Fig 7.12) {#rs2-38}

Slide2 counterpart: [VP74](rocscience.md#vp74) (Duncan & Wright 2005, Fig 7.12).

**Input files:** [vp074.xlsx](files/rocscience/vp074.xlsx)

A cohesionless sand embankment (c = 0, φ = 40°, γ = 140 pcf) on a saturated clay foundation
(c = 2500 psf, φ = 0, γ = 140 pcf). The critical surface is the deep foundation mechanism through the
undrained clay. The FEM elastic constants are the vendor model's own, E = 1×10⁶ psf and ν = 0.4 on
both materials.

| Method | XSLOPE | RS2 SSRM (Part 4) | RS2 SSRM (Part 2) | Slide2 Spencer | D&W referee | XSLOPE LEM |
|---|---|---|---|---|---|---|
| SSRM (7.0 m mesh) | 1.190 | 1.17 (+1.7%) | 1.21 | 1.20 circular / 1.18 non-circular | 1.22 (Bishop) / 1.19 (Spencer) | Bishop/Spencer/Janbu 1.219 / 1.194 / 1.161 |

RS2 re-ran this problem between its two manuals, and XSLOPE sits between the two published
factors. ψ = 0; locked at the 7.0 m mesh on this 700-ft-wide section.

<!-- test: file=files/rocscience/vp074.xlsx, type=fem_ssrm, expected_fs=1.190, element_type=tri6, target_size=7.0, tolerance=0.02, f_min=0.9, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-38 -->

![RS2-38: cohesionless embankment on saturated clay (D&W Fig 7.12), SSRM 1.190 vs RS2 SSRM 1.17 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-38.png)

### RS2-39/41/43: Earth embankment, infinite-slope mechanism (Duncan & Wright) {#rs2-39}

RS2 Parts I–III problems 41 (Slide2 [VP79](rocscience.md#vp79), D&W Fig 14.4) and 43 (Slide2
[VP81](rocscience.md#vp81), D&W Fig 14.7) are cohesionless embankments (c = 0, φ = 30°) on an
undrained φ = 0 foundation, each analyzed for a **very shallow infinite-slope skin** in the
embankment and a **deep** surface RS2 forces by holding the foundation linear-elastic. Problem 39
(VP76, D&W Fig 7.19) is the FE-seepage member of the family and is deferred with the other
FE-seepage cases. The skin is the natural unconstrained SSRM mechanism, and VP81's vendor model
additionally carries an SSR Exclusion Area, which its lock reproduces.

**Input files:** [vp079.xlsx](files/rocscience/vp079.xlsx) (RS2-41, Fig 14.4) ·
[vp081.xlsx](files/rocscience/vp081.xlsx) (RS2-43, Fig 14.7)

| Case | XSLOPE SSRM | Governing published | RS2 SSRM | Slide2 Bishop/Spencer |
|---|---|---|---|---|
| VP79 infinite slope (unconstrained) | 1.431 | D&W referee 1.44 (−0.6%) | 1.47 (−2.7%) | 1.44 |
| VP81 under the vendor model's SSR Exclusion Area | 1.209 | RS2 SSRM 1.23 (−1.7%) — Part IV VP81 case 1, deep | 1.23 (−1.7%) | 1.15–1.16 (infinite) |

On **VP79** the unconstrained SSRM finds the infinite-slope skin, −0.6% from the Duncan & Wright
referee and inside the RS2 1.43–1.47 band. **VP81 carries a constraint its own vendor model
states**: `slope stability #081_-_duncan_page220_figure_14-7_deep.fez` writes an
`SSR_polygonal_zones` block flagged as an *exclusion* area, holding a small block of the section —
2.7% of the domain — at full strength while everything else is reduced. Carried as its complement
(`ssr_zone` has one sense, *reduce inside*, so an exclusion enters as the ten-vertex ring covering
the rest), the SSRM reads **1.209**, −1.7% on that model's own published value: the `_deep` file is
**Part IV VP81 case 1**, whose SSR is **1.23**. The 1.19 published for this problem is a
*different* model's number — RS2's native rebuild at Part II problem 43, and its **shallow**
infinite-slope case at that. That native shallow model is one of the archive's
constraint-by-material cases: it holds 57.7% of the domain elastic with no polygon at all, which is
how RS2 kept its slip surface out of the foundation. Unconstrained, the corpus file localizes the
c = 0 cohesionless skin on the fine tri6 mesh with no length scale to arrest it (the behavior
[RS2-40](#rs2-40) documents), and holding the foundation elastic does not separate a deep
mechanism from it. Locked at the 1.5 m mesh. ψ = 0; E = 1×10⁶ psf and ν = 0.4, the vendor model's
own constants.

<!-- test: file=files/rocscience/vp079.xlsx, type=fem_ssrm, expected_fs=1.431, element_type=tri6, target_size=1.5, tolerance=0.02, f_min=1.1, f_max=1.9, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-41 -->
<!-- test: file=files/rocscience/vp081.xlsx, type=fem_ssrm, expected_fs=1.209, element_type=tri6, target_size=1.5, tolerance=0.02, f_min=0.9, f_max=1.5, max_iter=16000, tension_srf=false, ssr_zone=128;34;128;15;128;0;0;0;0;15;35;15;39.1558;15;71.1539;29.9985;73;34;128;34, k0=1, benchmark=RS2-43 -->

**VP79 (RS2-41, D&W Fig 14.4)**

![RS2-41: cohesionless embankment infinite-slope mechanism (D&W Fig 14.4), SSRM 1.431 vs D&W 1.44 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-41.png)

**VP81 (RS2-43, D&W Fig 14.7)**

![RS2-43: cohesionless embankment infinite-slope mechanism (D&W Fig 14.7), SSRM 1.209 vs RS2 Part IV VP81 case 1 SSR 1.23 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-43.png)

### RS2-40: Dam with impermeable foundation (D&W Fig 7.24) {#rs2-40}

Slide2 counterpart: [VP77](rocscience.md#vp77). RS2 runs the dam twice, once with a
finite-element seepage field and once with a drawn piezometric line, and publishes an SSR for
each; both are built here.

**Input files:** [vp077b.xlsx](files/rocscience/vp077b.xlsx) (piezometric),
[vp077a.xlsx](files/rocscience/vp077a.xlsx) (finite-element seepage)

| Case | XSLOPE SSRM | Published |
|---|---|---|
| Piezometric, filter off (true global minimum) | 1.160 | saturated seepage-parallel infinite slope **1.190** (−2.5%) |
| Piezometric, `min_slip_depth` = 30 ft (deep) | 1.521 | RS2 SSRM **1.53** (−0.6%) |
| Finite-element seepage | 1.590 | RS2 SSRM **1.52** (+4.6%) |

**Two mechanisms.** As on the dry Talbingo dam ([RS2-4](#rs2-4)), the cohesionless downstream
shell can fail as a surface-parallel skin rather than a deep rotation, and here the piezometric
line daylights on that face near the toe, so the skin is *saturated*: its closed form is the
seepage-parallel infinite slope, (140 − 62.4)/140 × tan 38° / tan 20° = **1.190**. With the depth
filter off the SSRM finds exactly that mechanism, the shear strain concentrating 1–8 ft below the
downstream 2.75:1 face between the piezometric daylight and the toe. The FEM reads 1.160, 2.5%
below the idealized value because the finite, partially saturated toe geometry softens it, and a
shell-φ sweep tracks the anchor law at a *constant* ratio across φ = 30–42°.

RS2 reports the other one, and its manual draws it: a surface that starts at the crest, cuts down
through the clay core, reaches the foundation contact at el 127 and continues as a basal shear
band under the downstream shell out to the toe. Excluding anything shallower than 30 ft with
[`min_slip_depth`](../fem/overview.md#surficial-skin-failures-and-the-minimum-slip-depth-filter)
returns exactly that band, at **1.521**, −0.6% on RS2's 1.53. Neither figure nor text on RS2's side
carries an SSR annotation for this problem, so its 1.53 is an unconstrained strength reduction that
simply localizes on the deeper surface, and the depth filter is how XSLOPE asks the same
question.

| `min_slip_depth` (ft) | off | 15 | 20 | 30 | 50 | 80 |
|---|---|---|---|---|---|---|
| XSLOPE SSRM | 1.160 | 1.246 | 1.418 | **1.521** | 1.555 | 1.555 |

The 50 and 80 ft values are identical to seven decimals — the plateau test the filter's
documentation prescribes — so the deep-seated answer is the 1.555 they agree on, +1.6% on RS2's
1.53. The 30 ft cutoff the tag pins is the first one clear of the skin and reads 1.521; the
reading is still rising at that cutoff and settles from 50 ft up.

**Mesh, and what the deep lock is.** A deep mechanism's factor follows the element size until the
zone that carries it is resolved, and this dam's still does: the same filtered run gives 1.521 at
the tagged 12.4 ft mesh (2 223 tri6) and 1.487 at the 8 ft mesh (5 220 tri6). The skin drifts under
refinement as well, so both rows are **regression locks at the tagged mesh**.

**What the vendor model states.** RS2 models this dam natively rather than by import — the
Slide2-import set runs #076 straight to #078 — as `#040_01` for the finite-element seepage case and
`#040_02` for the piezometric one. Both give the shell and the core a tensile strength of zero,
held static through the strength reduction, and both fills being cohesionless that cap stands where
the Mohr-Coulomb apex already does, so the run is the same whichever way the tension-SRF flag is
set. The initial stress is the page's K0 = 1 field and the flow rule is ψ = 0.

**The finite-element seepage case.** [vp077a.xlsx](files/rocscience/vp077a.xlsx) is the same file
the limit-equilibrium side of the problem is locked on ([VP77](rocscience.md#vp77)). Its row here
runs the route the case names: mesh the dam at the tagged 12.4 ft in tri6, solve the model's own
boundary set on that mesh — specified head 315 on the submerged upstream face, the downstream face
an exit face, the foundation impervious — and reduce the strengths on that same mesh and that same
field. It brackets **1.590**, +4.6% on RS2's 1.52 for its Case 1. Unlike the piezometric case there
is no shallow skin to exclude: excluding everything shallower than 30 ft returns **1.607**, one cell
of the row's own bracket above the unconstrained minimum, so the mechanism the filter leaves is the
mechanism the unconstrained run already finds. With the phreatic surface solved on the mesh rather
than drawn across it, the downstream face does not carry the saturated skin the piezometric case
localizes on.

<!-- test: file=files/rocscience/vp077b.xlsx, type=mesh_elements, element_type=tri6, target_size=12.4, expected_elements=2223, benchmark=RS2-40-mesh -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=mesh_elements, element_type=tri6, target_size=8.0, expected_elements=5220, benchmark=RS2-40-mesh-fine -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.160, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, k0=1, benchmark=RS2-40 -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.487, element_type=tri6, target_size=8.0, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=30, k0=1, benchmark=RS2-40-deep-m8 -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.246, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=15, k0=1, benchmark=RS2-40-d15 -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.418, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=20, k0=1, benchmark=RS2-40-d20 -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.555, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=50, k0=1, benchmark=RS2-40-d50 -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.555, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=80, k0=1, benchmark=RS2-40-d80 -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=fem_ssrm, expected_fs=1.521, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=30, k0=1, benchmark=RS2-40-deep -->
<!-- test: file=files/rocscience/vp077a.xlsx, type=fem_ssrm, expected_fs=1.590, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, k0=1, seep=steady, benchmark=RS2-40-seep -->
<!-- test: file=files/rocscience/vp077a.xlsx, type=fem_ssrm, expected_fs=1.607, element_type=tri6, target_size=12.4, tolerance=0.02, f_min=1.1, f_max=2.2, max_iter=16000, min_slip_depth=30, k0=1, seep=steady, benchmark=RS2-40-seep-d30 -->

**Filter off — the saturated downstream face skin (vp077b)**

![RS2-40: piezometric case (vp077b) solved with the depth filter off, SSRM 1.160 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the strain in a shallow band under the downstream face between the piezometric daylight and the toe](images/RS2-40.png)

**`min_slip_depth` = 30 ft — the basal band RS2 draws (vp077b)**

![RS2-40 with anything shallower than 30 ft excluded, SSRM 1.521 against RS2 SSRM 1.53 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the surface cutting down through the clay core and running out along the foundation contact under the downstream shell](images/RS2-40-deep.png)

**Finite-element seepage, unconstrained (vp077a)**

![RS2-40 solved on a finite-element seepage field, SSRM 1.590 against RS2 SSRM 1.52 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the band cutting down from the crest through the clay core and running out along the foundation contact under the downstream shell with no depth filter applied](images/RS2-40-seep.png)

### RS2-42: James dike {#rs2-42}

Slide2 counterpart: [VP75](rocscience.md#vp75).

**Input files:** [vp075.xlsx](files/rocscience/vp075.xlsx)

| Method | XSLOPE | RS2 SSRM (Part IV VP75) | RS2 SSRM (native #42) | Slide2 noncircular LEM | D&W non-circular |
|---|---|---|---|---|---|
| SSRM | 1.214 | 1.19 (+2.0%) | 1.26 | 1.11–1.16 | 1.17 |

*Scored against Part IV VP75's RS2 SSRM, the value published for the model vp075.xlsx is
transcribed from. As on [RS2-11](#rs2-11), RS2 ran this deck twice on input-identical decks that
differ only in the SRF tensile setting: the native `#042` model reduces tensile strength brittly
on a 1080-element mesh, the Part IV import holds tension perfectly plastic on 3031 elements, which
matches both XSLOPE's tensile behavior and its mesh density.*

<!-- test: file=files/rocscience/vp075.xlsx, type=fem_ssrm, expected_fs=1.214, element_type=tri6, target_size=1.85, tolerance=0.02, f_min=0.8, f_max=1.8, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-42 -->

![RS2-42: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-42.png)

### RS2-44: Seepage analysis for an earth embankment (D&W Fig 14.20-a) {#rs2-44}

Slide2 counterpart: [VP82](rocscience.md#vp82) (= Slide2 VP82, not
[VP76](rocscience.md#vp76) — §39's body carries VP76).

**Input files:** [vp082.xlsx](files/rocscience/vp082.xlsx)

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | Referee |
|---|---|---|---|---|
| SSRM | 1.490 | 1.51 (−1.3%) | 1.532 / 1.541 | 1.528–1.542 (−2.5%) |

<!-- test: file=files/rocscience/vp082.xlsx, type=fem_ssrm, expected_fs=1.490, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=1.0, f_max=2.1, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-44 -->

![RS2-44: FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-44.png)

### RS2-45: Varying undrained shear strength profiles (D&W Fig 14.20-b) {#rs2-45}

Slide2 counterpart: [VP83](rocscience.md#vp83). Built with a caveat.

**Input files:** [vp083a.xlsx](files/rocscience/vp083a.xlsx),
[vp083b.xlsx](files/rocscience/vp083b.xlsx)

| Method | XSLOPE | RS2 SSRM | D&W referee |
|---|---|---|---|
| SSRM (vp083a) | 1.314 | 1.32 (−0.5%) | 1.28–1.33 (inside) |
| SSRM (vp083b) | 1.314 | 1.32 (−0.5%) | 1.28–1.33 (inside) |

Both cases land inside the referee band under the per-node criterion. [RS2-19](#rs2-19),
the other φ = 0 foundation problem, reads +4.8% against RS2's own SSRM and keeps its caveat.

<!-- test: file=files/rocscience/vp083a.xlsx, type=fem_ssrm, expected_fs=1.314, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.9, f_max=1.9, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-45a -->
<!-- test: file=files/rocscience/vp083b.xlsx, type=fem_ssrm, expected_fs=1.314, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.9, f_max=1.9, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-45b -->

**Case a (vp083a)**

![RS2-45a: vp083a (SSRM 1.314) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-45a.png)

**Case b (vp083b)**

![RS2-45b: vp083b (SSRM 1.314) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-45b.png)

### RS2-46: Varying undrained strength profiles II (D&W Fig 15.9, c<sub>u</sub> = 300 + c<sub>z</sub>·z) {#rs2-46}

Slide2 counterpart: [VP84](rocscience.md#vp84).

**Input files:** [vp084a–d](files/rocscience/vp084a.xlsx)

| Method | XSLOPE | RS2 SSRM | Duncan & Wright |
|---|---|---|---|
| SSRM (vp084a) | 0.787 | 0.78 (+0.9%) | 0.75 (+4.9%) |
| SSRM (vp084b) | 0.929 | 0.93 (−0.1%) | 0.90 (+3.2%) |
| SSRM (vp084c) | 1.057 | 1.05 (+0.7%) | 1.03 (+2.6%) |
| SSRM (vp084d) | 1.145 | 1.15 (−0.4%) | 1.13 (+1.3%) |

*XSLOPE sits +1.3 to +4.9% above the Duncan & Wright column, the φ = 0 pattern.*

<!-- test: file=files/rocscience/vp084a.xlsx, type=fem_ssrm, expected_fs=0.787, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.4, f_max=1.3, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-46a -->
<!-- test: file=files/rocscience/vp084b.xlsx, type=fem_ssrm, expected_fs=0.929, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.5, f_max=1.4, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-46b -->
<!-- test: file=files/rocscience/vp084c.xlsx, type=fem_ssrm, expected_fs=1.057, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.6, f_max=1.5, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-46c -->
<!-- test: file=files/rocscience/vp084d.xlsx, type=fem_ssrm, expected_fs=1.145, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.7, f_max=1.7, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-46d -->

**Case a (vp084a)**

![RS2-46a: vp084a (SSRM 0.787) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-46a.png)

**Case b (vp084b)**

![RS2-46b: vp084b (SSRM 0.929) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-46b.png)

**Case c (vp084c)**

![RS2-46c: vp084c (SSRM 1.057) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-46c.png)

**Case d (vp084d)**

![RS2-46d: vp084d (SSRM 1.145) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-46d.png)

### RS2-47: Purely cohesive slope, varying thickness (D&W Fig 14.3) {#rs2-47}

Slide2 counterpart: [VP78](rocscience.md#vp78). All three foundation-thickness variants built.

**Input files:** [vp078.xlsx](files/rocscience/vp078.xlsx) (30 ft) ·
[vp078b.xlsx](files/rocscience/vp078b.xlsx) (46.5 ft) ·
[vp078c.xlsx](files/rocscience/vp078c.xlsx) (60 ft)

A pure-cohesive slope (c = 1000 psf, φ = 0, γ = 100 pcf), 50-ft face at 1:0.8, over a firm-based
foundation of varying thickness. D&W Fig 14.3 plots FS against that thickness; RS2 re-runs the
30 / 46.5 / 60 ft cases by strength reduction. The three geometries are RS2's own external boundary
read verbatim from the vendor `.fez` (`#047_01/02/03`): the firm base stays at y = 0 and the
foundation *surface* is raised, so the base sits progressively deeper below the toe.

| Method | XSLOPE | RS2 SSRM (Part IV VP78 case a) | D&W referee |
|---|---|---|---|
| SSRM (30-ft foundation, vp078) | 1.061 | 1.06 (+0.1%) | 1.124–1.135 (−5.6%, toe circle) / 1.139–1.141 (base tangent) |
| SSRM (46.5-ft foundation, vp078b) | 1.045 | 1.06 (−1.4%) | — |
| SSRM (60-ft foundation, vp078c) | 1.045 | 1.07 (−2.3%) | — |

**Which vendor models these are.** Each corpus file reproduces the external boundary of the
Part IV **case-(a)** model for its thickness — the toe-failure case — vertex for vertex
(0/240/80 · 0/240/96.5 · −10/270/110). The native `#047_01/02/03` twins draw the same boundaries,
but the case-(b) tangent-failure models do not, so the case-(a) lineage is the one the files
match, and the table above pairs against its published values.

XSLOPE tracks RS2's slight decrease-then-plateau with depth, and on the 30-ft case sits *between*
the two published anchors. The RS2 manual's VP78 write-up says of these models that "to force RS2
to iterate for SRF associated with a failure surface passing through the toe of the slope, a SSR
Exclusion Area was used" (the technique reproduced for [RS2-P4-VP67](#p4-vp67)), and the case-(a)
`.fez` files do carry it: a four-vertex exclusion rectangle holding 19.0 / 22.4 / 23.5% of the
domain. The corpus runs are unconstrained and land on the constrained values anyway. Each is
regression-locked at its XSLOPE value (4.0 m tri6 mesh).

<!-- test: file=files/rocscience/vp078.xlsx, type=fem_ssrm, expected_fs=1.061, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.6, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-47 -->
<!-- test: file=files/rocscience/vp078b.xlsx, type=fem_ssrm, expected_fs=1.045, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.6, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-47b -->
<!-- test: file=files/rocscience/vp078c.xlsx, type=fem_ssrm, expected_fs=1.045, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=0.6, f_max=1.6, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-47c -->

![RS2-47: 30-ft case (vp078) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-47.png)

![RS2-47b: 46.5-ft foundation (vp078b), SSRM 1.045 vs RS2 SSRM 1.06 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-47b.png)

![RS2-47c: 60-ft foundation (vp078c), SSRM 1.045 vs RS2 SSRM 1.07 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-47c.png)

### RS2-48–55: Multi-tiered geotextile walls (Leshchinsky & Han 2004) {#rs2-48}

Slide2 counterparts: [VP87](rocscience.md#vp87)–VP94 (one-for-one, verified; only VP87 has a
detail section on the LEM page). The baseline's SSR row is not attempted; of the seven parametric
variants, two are locked at the section's mesh and five are reported without locks. None of the
eight is scored against a published factor, for the reason given below.

The wall is three 3 m tiers of reinforced granular fill behind 0.3 m facing-block columns, each
tier carrying geotextile layers at an allowable strength T<sub>a</sub> (Leshchinsky & Han 2004).
RS2's numbers are from Part 2 of its verification manual, problem 48, which imports this Slide2
model.

| Published (baseline wall) | RS2 SSR | RS2 LEM (Bishop / Spencer / GLE) | L&H FDM referee | L&H Bishop | Slide2 Bishop |
|---|---|---|---|---|---|
| Leshchinsky & Han 2004 | 1.05 | 1.02 / 1.03 / 1.03 | 0.99 | 1.00 | 1.040 |

**The SSR row is not attempted.** RS2 does not mesh the wall as one body: its `#048` model splits
the solid mesh along the geotextile layers, 195 coincident node pairs joined by frictional slip
joints with tension-only beam elements running along the split, so the load path between the
reinforced fill and its sheets passes through sliding interfaces. XSLOPE meshes a bonded continuum
and has no interface element, so those joints have no counterpart and no XSLOPE run stands opposite
RS2's factor. The limit-equilibrium side of the same wall is built and locked
([VP87](rocscience.md#vp87): Bishop 1.031 vs Slide2 1.040), where the sheets enter as forces.

`#049` through `#055` carry the same split mesh and the same joints as `#048`; what changes case
by case is the sheet. So every RS2 SSR value in the variant sections below comes from the
split-interface wall and XSLOPE's runs from a bonded continuum: they are recorded side by side,
never scored against each other.

**Input files:** [vp087.xlsx](files/rocscience/vp087.xlsx) (baseline) through
[vp094.xlsx](files/rocscience/vp094.xlsx). Geotextile modeled as an FEM truss with the vendor
`.fez` stiffness EA = 6300 kN/m (cbeam1). Every file carries the vendor's tensile caps — T = 0 on
the reinforced granular fill, 10 on the foundation soil, 2.5 on the blocks, and T = 0 on the c = 0
foundation of the weak-foundation variant — together with its E = 50,000 kPa and ν = 0.4 on all
three materials. The caps are static through the strength reduction, which is the setting the
vendor models carry. On a c = 0 fill a cap of zero stands where the Mohr-Coulomb apex c/tan φ
already does, so what the fill's cap changes is nothing and what the transcription changes is the
blocks' cap and the elastic pair. Every row runs the isotropic at-rest stress state the
SSRM rows on this page use. A fill that admits no tension decides which convergence criterion can
bracket the wall: it settles into a stationary state at elastic displacement scale, which a pure
non-convergence criterion would read as collapse, where the default hybrid criterion requires
displacement evidence before calling a trial failed. On the water variant (vp092) the reinforced fill is
modeled free-draining, pore pressure on the foundation only, following Leshchinsky & Han and
Slide2's own model, which the LEM side of the file is locked against.

Each variant carries its own published set, from the same manual pages as the baseline's:

| Variant (RS2 problem) | RS2 SSR | RS2 LEM Bishop / Spencer / GLE | L&H FDM referee |
|---|---|---|---|
| 49 — fill quality | 1.08 | 0.98 / 0.97 / 0.97 | 0.99 |
| 50 — reinforcement length | 0.93 | 0.93 / 0.92 / 0.91 | 0.98 |
| 51 — reinforcement type | 1.00 | 0.92 / 0.91 / 0.91 | 1.01 |
| 52 — foundation strength | 0.84 | — / 0.96 / 0.98 | 0.86 |
| 53 — water | 1.03 | 0.92 / 1.00 / 1.13 | 1.01 |
| 54 — surcharge | 0.92 | 0.87 / 0.91 / 0.91 | 1.02 |
| 55 — tier number | 1.04 | 0.92 / 0.94 / 0.94 | 1.00 |

Every SSR in that column comes from the split-interface wall, and the referee column from
Leshchinsky & Han's own model of it, so the runs below are recorded beside them and scored against
neither.

Across the seven parametric variants (vp088–vp094 — fill quality, reinforcement length and type,
foundation soil, water, surcharge, tier count) the strength reduction brackets a factor on the
corpus mesh in every case. On these wished-in-place walls the geotextile bars are not mobilized to
their pull-out capacity at the incipient failure state, so the pull-out envelope is not what sets
those factors.

Neither the element order, the facing nor the tension model is what those factors follow. RS2
meshes these walls with `lst_element`, the same 6-node quadratic triangle XSLOPE uses; its `Blocks`
material is ordinary Mohr-Coulomb with `Apply_SSR` on rather than a linear-elastic "can't-fail"
zone, so the facing is not holding the mechanism up; and the vendor's Rankine cutoff T = c is
carried on every material, where on the c = 0 fill it stands at the Mohr-Coulomb apex, so that fill
admits no tension whichever way the cutoff is read. What remains is a **shear localization
through the c = 0 reinforced granular
fill**: a cohesionless mass has no intrinsic length scale, so the failing band can collapse onto
the element size and the factor follow the mesh instead of settling. Five of the seven variants do
that — the reinforcement-length, weak-foundation, water, surcharge and tier-count cases all move
under a step of refinement to a 0.7 m mesh — and they are reported without locks. The fill-quality
and reinforcement-type variants hold their factor across that step, inside the bracket tolerance
the family runs at, and each carries a regression lock at the section's 1.0 m mesh. What no row in
the family carries is a comparison: RS2 publishes its own factors from the split-interface wall
either way. The baseline carries the same mesh sensitivity in milder form.

#### The seven parametric variants, one by one

Each variant is its own problem in the RS2 manual, so each is listed separately in the summary
table above and anchored here. All seven share the baseline's model, mesh and reinforcement
treatment; what follows is only what distinguishes each one and where it ended up.

#### RS2-49: Geotextile wall, fill quality (vp088) {#rs2-49}

The reinforced fill's strength is reduced relative to the baseline. The strength reduction brackets
**SSRM 0.881**, and a step of refinement to a 0.7 m mesh returns the same factor, so the variant is
locked as a regression at the section's mesh. RS2's own factor for this wall comes from the
split-interface model, so no comparison is derived from it.

<!-- test: file=files/rocscience/vp088.xlsx, type=fem_ssrm, expected_fs=0.881, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.5, f_max=3.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-49 -->

![RS2-49: reduced-strength fill (vp088, φ = 25°, Ta = 22 kN/m) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. The mechanism stays inside the reinforced mass, as on the baseline](images/RS2-49.png)

#### RS2-50: Geotextile wall, 4.2 m reinforcement (vp089) {#rs2-50}

The geotextile layers are shortened. The strength reduction brackets a factor on the corpus mesh,
but a step of refinement moves it — the localization the family shares — so the variant is reported
without a lock.

![RS2-50: shortened 4.2 m geotextile layers (vp089, Ta = 11.4 kN/m) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. Shortening the sheets pulls the mechanism back into the reinforced mass behind their ends](images/RS2-50.png)

#### RS2-51: Geotextile wall, dual reinforcement type (vp090) {#rs2-51-wall}

Two geotextile grades in one wall. It brackets **SSRM 0.998**, and a step of refinement to a 0.7 m
mesh moves it by one cell of the bracket the row runs at — inside the row's tolerance, and well
below the spread the mesh-following variants show — so it is locked as a regression at the section's
mesh.

<!-- test: file=files/rocscience/vp090.xlsx, type=fem_ssrm, expected_fs=0.998, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.5, f_max=3.0, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-51-wall -->

![RS2-51: two geotextile grades in one wall (vp090, Ta = 11.0 kN/m on the lower seven layers, 7.5 kN/m above) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. The geometry is the baseline's; the two grades differ in tensile capacity and anchorage length, not in layout](images/RS2-51-wall.png)

#### RS2-52: Geotextile wall, weak foundation (vp091) {#rs2-52}

The foundation is c = 0, φ = 18°, and the wall fails in bearing rather than through the reinforced
mass — the lowest factor in the family. Its published values are in the family table above, and
what the three codes agree on is the mechanism: Leshchinsky & Han's FLAC drops on this case as
XSLOPE's SSRM does, into the foundation.

**Two sections.** vp091 is the only file in this family whose foundation runs from x = −6 rather
than x = 0: the extra 36 m² exists so that Slide's printed critical circle, which daylights at
x = −1.6, can be seated for the LEM comparison. RS2's own #052 and the seven sibling corpus files
are all the 24 m section, and it is built here too
([vp091_fem.xlsx](files/rocscience/vp091_fem.xlsx)). A bearing mechanism is sensitive to the run of
ground in front of the toe, so the two sections could have been expected to differ widely; at the
section's mesh they bracket the same factor. Neither is locked: this variant is one of the five
whose factor follows the mesh, and RS2's own factor comes from the split-interface wall.

![RS2-52: cohesionless foundation (vp091, c = 0, φ = 18°), recorded beside RS2's own SSR 0.84 and Leshchinsky & Han's FLAC referee 0.86 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. The strain band leaves the reinforced mass and runs down through the foundation to daylight beyond the toe: the bearing mechanism both codes find on this variant](images/RS2-52.png)

#### RS2-53: Geotextile wall, water (vp092) {#rs2-53}

A pond against the wall. The reinforced granular fill is modeled free-draining, pore pressure on
the foundation only, following Leshchinsky & Han and Slide2's own model rather than the vendor's
whole-mesh alternative. It brackets the highest factor in the family, but the same c = 0 fill
localization makes the value follow the mesh, so the variant is reported without a lock.

![RS2-53: pond against the wall (vp092, piezometric line at y = 9 with a 3 m pond on the lower tier, Ta = 9.25 kN/m) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. The reinforced fill is modeled free-draining, so pore pressure acts on the foundation only and the pond enters as a distributed load on the lower tier](images/RS2-53.png)

#### RS2-54: Geotextile wall, crest surcharge (vp093) {#rs2-54}

A surcharge on the wall crest. It brackets on the corpus mesh and moves under refinement with the
water and tier-count variants, so it is reported without a lock.

![RS2-54: 20 kPa surcharge on the uppermost tier (vp093, Ta = 10.0 kN/m) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. The surcharge drives the band through the upper tiers of the reinforced mass](images/RS2-54.png)

#### RS2-55: Geotextile wall, tier count (vp094) {#rs2-55}

The number of wall tiers is varied. It brackets, and as on the water and surcharge variants the
value follows the mesh, so it is reported without a lock.

![RS2-55: five 1.8 m tiers offset 0.6 m (vp094, Ta = 10.1 kN/m) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF. Spreading the same 9 m of height over five tiers instead of three leaves the mechanism where the baseline puts it](images/RS2-55.png)

### RS2 Part IV VP51: Four-material slope, water table, tension crack, seismic — 12-method comparison (Zhu et al. 2003) {#p4-vp51}

**Input files:** [rs2_51.xlsx](files/rocscience/rs2_51.xlsx) — Part 4 Verification Problem #51.

> Zhu, D.Y., Lee, C.F. & Jiang, H.D. (2003). "A generalised framework of limit equilibrium
> methods for slope stability analysis." *Géotechnique* 53(4), 377–395. *(RS2/Slide2 Slope
> Stability Verification Manual, Part 4, Problem #51.)*

A four-layer 1V:2H slope (toe (0,0) → crest (60,30)) whose strata dip parallel to the face:
Layer 1 (top, c = 20, φ = 32°, γ = 18.2), Layer 2 (c = 25, φ = 30°, γ = 18.0), Layer 3 (the
weak band, c = 40, **φ = 18°**, γ = 18.5) and Layer 4 (bottom, c = 40, φ = 28°, γ = 18.8). Pore
pressure comes from a 9-point piezometric surface connected to every material; a horizontal
seismic coefficient **k = 0.1** is applied; and a **dry tension crack** of the Rankine active
depth *h*<sub>c</sub> = 2c/(γ√K<sub>a</sub>) ≈ 3.97 m sits in the top layer. The published task
is the factor of safety on a **given circular surface** with 100 slices, tolerance 0.001, over
twelve LEM methods. This is an LEM problem; the RS2 SSRM value of 1.22 in the catalog is an
independent finite-element mechanism, not the LEM target reproduced here.

**Partial — reconstructed surface.** The vendor `.fez` is an RS2 SSRM model that carries **no LEM
slip surface**, and the given circle and tension-crack depth are figure-only. The circle here —
center (32, 36), tangent at y = 1.0 (R = 35), daylighting from the lower face to the back plateau —
was recovered by inversion against the rigorous methods; geometry, materials, the piezo line and
k = 0.1 are transcribed from `slope stability #051.fez`. On this surface, at 100 slices:

| Method | XSLOPE | Slide2 | Zhu | Note |
|---|---|---|---|---|
| Ordinary (OMS) | 1.092 | 1.145 (−4.6%) | 1.066 (+2.4%) | lands inside the Slide2–Zhu spread |
| Bishop simplified | 1.316 | 1.278 (+3.0%) | 1.278 (+3.0%) |  |
| Janbu simplified | 1.196\* | 1.112 | 1.112 | \*XSLOPE reports Janbu **corrected** (f₀ ≈ 1.08); 1.196/1.08 ≈ **1.11** ✓, so the columns are not like-for-like |
| Corps of Engineers | 1.400 | 1.422 (−1.5%) | 1.377 (+1.7%) | inside the Slide2–Zhu spread |
| Lowe & Karafiath | 1.244 | 1.288 (−3.4%) | 1.290 (−3.6%) |  |
| **Spencer** | **1.300** | **1.293** (**+0.5%**) | **1.293** (**+0.5%**) |  |
| GLE / Morgenstern–Price | 1.282 | 1.304 | 1.303 (−1.6%) | half-sine interslice function; Slide2's column is GLE, which this page's conventions treat as a different method from XSLOPE's M-P, so it stays bare like the Janbu row |

Spencer — the headline LEM value the RS2 manual's Table 51.2 quotes — reproduces to +0.5%, and
Janbu once the corrected-vs-simplified convention is undone matches to within 0.5%; OMS and Corps
both land between the Slide2 and Zhu columns. Bishop (+3.0%), Lowe (−3.4%) and M-P (−1.6%) carry
the residual of fitting a figure-only circle plus method-implementation differences (XSLOPE's M-P
uses a half-sine interslice function and lands just below Spencer, where Zhu's GLE lands just
above). An unconstrained circular search does **not** reproduce this problem — it dives into a
spurious deep mechanism daylighting on the flats through the φ = 18° weak band, so the
verification is locked as a single fixed circle, not a search.

<!-- test: file=files/rocscience/rs2_51.xlsx, type=single_circle, num_slices=100, fs_oms=1.092, fs_bishop=1.316, fs_janbu=1.196, fs_corps=1.400, fs_lowe=1.244, fs_spencer=1.300, fs_mprice=1.282, benchmark=RS2-P4-VP51 -->

![RS2 Part IV VP51: four-material slope with water table, tension crack and seismic k = 0.1 (Zhu et al. 2003) — inputs (left) and the given-circle Spencer solution FS = 1.30 (right)](images/rs2_51.png)

### RS2-56: Homogeneous slope vs Z-Soil, PLAXIS, GEO FEM (Pruska 2003, H = 7 m, 5 cases) {#rs2-56}

New corpus files (no Slide2 counterpart). Built: all five cases.

**Input files:** [rs2_56c1.xlsx](files/rocscience/rs2_56c1.xlsx) ·
[rs2_56a.xlsx](files/rocscience/rs2_56a.xlsx) (case 2) ·
[rs2_56c3.xlsx](files/rocscience/rs2_56c3.xlsx) ·
[rs2_56c4.xlsx](files/rocscience/rs2_56c4.xlsx) ·
[rs2_56b.xlsx](files/rocscience/rs2_56b.xlsx) (case 5)

| Method | XSLOPE | Published |
|---|---|---|
| SSRM (rs2_56a — case 2, weakest; lock) | 0.664 | RS2 SSRM 0.67 (−0.9%) |
| SSRM (rs2_56b — case 5, strongest; lock) | 2.096 | RS2 SSRM 2.14 (−2.1%) |

*The two locks bracket the family, the weakest case and the strongest, and case 5 is the wider of the two, so it sets the dot. The published columns for all five cases — RS2, Z-Soil, PLAXIS, GEO FEM and Slide2 — are in [the Pruska cross-bearing section](#pruska).*

<!-- test: file=files/rocscience/rs2_56a.xlsx, type=fem_ssrm, expected_fs=0.664, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=0.32, f_max=1.12, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-56a -->
<!-- test: file=files/rocscience/rs2_56b.xlsx, type=fem_ssrm, expected_fs=2.096, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=1.79, f_max=2.59, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-56b -->

**Case 2 — weakest of the five (rs2_56a)**

![RS2-56a: case 2, (γ, c, φ) = (18, 5, 10), the weakest of the five (SSRM 0.664) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-56a.png)

**Case 5 — strongest of the five (rs2_56b)**

![RS2-56b: case 5, (γ, c, φ) = (24, 20, 30), the strongest of the five (SSRM 2.096) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-56b.png)

### RS2-57: Pruska H = 10.5 m, 6 cases {#rs2-57}

New corpus files. Built: all six cases.

**Input files:** [rs2_57a.xlsx](files/rocscience/rs2_57a.xlsx) (case 1) ·
[rs2_57c2.xlsx](files/rocscience/rs2_57c2.xlsx) ·
[rs2_57c3.xlsx](files/rocscience/rs2_57c3.xlsx) ·
[rs2_57c4.xlsx](files/rocscience/rs2_57c4.xlsx) ·
[rs2_57c5.xlsx](files/rocscience/rs2_57c5.xlsx) ·
[rs2_57b.xlsx](files/rocscience/rs2_57b.xlsx) (case 6)

| Method | XSLOPE | Published |
|---|---|---|
| SSRM (rs2_57a — case 1, weakest; lock) | 0.439 | RS2 SSRM 0.44 (−0.2%) |
| SSRM (rs2_57b — case 6, strongest; lock) | 1.401 | RS2 SSRM 1.42 (−1.3%) |

*The two locks bracket the family, the weakest case and the strongest, and case 6 is the wider of the two, so it sets the dot. The published columns for all six cases — RS2, Z-Soil, PLAXIS, GEO FEM and Slide2 — are in [the Pruska cross-bearing section](#pruska).*

<!-- test: file=files/rocscience/rs2_57a.xlsx, type=fem_ssrm, expected_fs=0.439, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=0.1, f_max=0.89, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-57a -->
<!-- test: file=files/rocscience/rs2_57b.xlsx, type=fem_ssrm, expected_fs=1.401, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=1.07, f_max=1.87, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-57b -->

**Case 1 — weakest of the six (rs2_57a)**

![RS2-57a: case 1, (γ, c, φ) = (18, 5, 10), the weakest of the six (SSRM 0.439) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-57a.png)

**Case 6 — strongest of the six (rs2_57b)**

![RS2-57b: case 6, (γ, c, φ) = (24, 20, 30), the strongest of the six (SSRM 1.401) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-57b.png)

### RS2-58: Pruska H = 14 m, 6 cases {#rs2-58}

New corpus files. Built: all six cases.

**Input files:** [rs2_58a.xlsx](files/rocscience/rs2_58a.xlsx) (case 1) ·
[rs2_58c2.xlsx](files/rocscience/rs2_58c2.xlsx) ·
[rs2_58c3.xlsx](files/rocscience/rs2_58c3.xlsx) ·
[rs2_58c4.xlsx](files/rocscience/rs2_58c4.xlsx) ·
[rs2_58c5.xlsx](files/rocscience/rs2_58c5.xlsx) ·
[rs2_58b.xlsx](files/rocscience/rs2_58b.xlsx) (case 6)

| Method | XSLOPE | Published |
|---|---|---|
| SSRM (rs2_58a — case 1, weakest; lock) | 0.339 | RS2 SSRM 0.33 (+2.7%) |
| SSRM (rs2_58c5 — case 5, c = 5, φ = 30; lock) | 0.714 | RS2 SSRM 0.72 (−0.8%) |
| SSRM (rs2_58b — case 6, strongest; lock) | 1.066 | RS2 SSRM 1.06 (+0.6%) |

*The three locks land within ±2.7% of RS2's M-C, case 1 being the widest, so it sets the dot.
Case 5 — the steepest, most cohesionless material (c = 5, φ = 30 on the 54.5° face) on the tallest
slope — is the third lock, and it sits inside the tight published cluster [the Pruska
cross-bearing section](#pruska) tabulates.*

<!-- test: file=files/rocscience/rs2_58a.xlsx, type=fem_ssrm, expected_fs=0.339, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=0.1, f_max=0.78, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-58a -->
<!-- test: file=files/rocscience/rs2_58c5.xlsx, type=fem_ssrm, expected_fs=0.714, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=0.27, f_max=1.07, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-58c5 -->
<!-- test: file=files/rocscience/rs2_58b.xlsx, type=fem_ssrm, expected_fs=1.066, element_type=tri6, target_size=0.8, tolerance=0.02, f_min=0.71, f_max=1.51, max_iter=16000, tension_srf=false, k0=1, benchmark=RS2-58b -->

**Case 1 — weakest of the six (rs2_58a)**

![RS2-58a: case 1, (γ, c, φ) = (18, 5, 10), the weakest of the six (SSRM 0.339) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-58a.png)

**Case 5 — the steep cohesionless face (rs2_58c5)**

![RS2-58c5: case 5, (γ, c, φ) = (18, 5, 30), the steepest cohesionless face in the study (SSRM 0.714) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-58c5.png)

**Case 6 — strongest of the six (rs2_58b)**

![RS2-58b: case 6, (γ, c, φ) = (24, 20, 30), the strongest of the six (SSRM 1.066) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-58b.png)

---

## The Pruska cross-bearing (#56–58) {#pruska}

Pruska (2003) analyzed three homogeneous slopes (H = 7, 10.5, and 14 m over an 8-m
foundation) with five or six material sets each in four SSRM programs, and RS2 reproduces the
study. Its published columns are tabulated here; every case is a committed corpus file, and the
seven XSLOPE locks — the weakest and strongest case of each family, plus the steepest
cohesionless case of the tallest slope — are at [#56](#rs2-56), [#57](#rs2-57) and
[#58](#rs2-58) above.
(The study's Drucker-Prager columns are not comparable; XSLOPE, like Slide2, analyzes
Mohr-Coulomb only.)

**Elastic constants and tensile caps come from the shipped models, not the printed tables.**
Each section's Table 1 gives ν per case but prints E once, as a merged cell spanning every
row — "5,000". The models RS2 solved these SSR values with carry two pairs, keyed to the
material family: (ν, E) = (0.30, 5 000) for the γ = 24 / c = 20 cases and (0.35, 10 000) for
the γ = 18 / c = 5 cases. Every case also carries a real tensile cap, T = c, well inside the
uncapped Mohr-Coulomb apex (20 against 34.6 kPa on #56 case 5; 5 against 8.66 kPa on #58 case 5).
Both are transcribed from the models.

**H = 7 m (#56):** cases (γ, c, φ) = (24,20,10), (18,5,10), (24,20,20), (18,5,20), (24,20,30)

| Case | RS2 | Z-Soil | PLAXIS | GEO FEM | Slide2 LEM |
|---|---|---|---|---|---|
| 1 | 1.22 | 1.21 | 1.22 | 1.31 | 1.22 |
| 2 | 0.67 | 0.71 | 0.68 | 0.73 | 0.66 |
| 3 | 1.68 | 1.64 | 1.65 | 1.71 | 1.64 |
| 4 | 1.05 | 0.95 | 0.99 | 1.17 | 1.02 |
| 5 | 2.14 | 1.98 | 2.09 | 2.19 | 2.08 |

**H = 10.5 m (#57):** cases 1–6 = (18,5,10), (24,20,10), (18,5,20), (24,20,20), (18,5,30), (24,20,30)

| Case | RS2 | Z-Soil | PLAXIS | GEO FEM | Slide2 LEM |
|---|---|---|---|---|---|
| 1 | 0.44 | 0.46 | 0.44 | 0.48 | 0.44 |
| 2 | 0.79 | 0.83 | 0.85 | 0.91 | 0.80 |
| 3 | 0.69 | 0.71 | 0.71 | 0.73 | 0.69 |
| 4 | 1.11 | 1.14 | 1.17 | 1.18 | 1.10 |
| 5 | 0.96 | 0.98 | 0.97 | 1.03 | 0.95 |
| 6 | 1.42 | 1.52 | 1.45 | 1.54 | 1.40 |

**H = 14 m (#58):** same six material cases as #57

| Case | RS2 | Z-Soil | PLAXIS | GEO FEM | Slide2 LEM |
|---|---|---|---|---|---|
| 1 | 0.33 | 0.34 | 0.35 | 0.35 | 0.34 |
| 2 | 0.59 | 0.61 | 0.59 | 0.63 | 0.60 |
| 3 | 0.52 | 0.54 | 0.53 | 0.59 | 0.53 |
| 4 | 0.83 | 0.84 | 0.82 | 0.86 | 0.84 |
| 5 | 0.72 | 0.75 | 0.74 | 0.73 | 0.73 |
| 6 | 1.06 | 1.07 | 1.06 | 1.10 | 1.08 |

The four programs disagree among themselves more than XSLOPE's locks differ from RS2: GEO FEM
reads 23.2% above Z-Soil on #56 case 4 and 11.3% above PLAXIS on #58 case 3. RS2's own column is
quoted to two decimals throughout, so on the weakest material of the tallest face — #58 case 1,
which sets that row's dot — one count in the last place is worth 3.0%.

### RS2-59: Stability of a three-layered soil slope (Görög & Török 2007) {#rs2-59}

**Input files:** [rs2_59.xlsx](files/rocscience/rs2_59.xlsx)

The Budapest (Rózsadomb) landslide, after

> [Görög, P. & Török, Á. (2007)](https://doi.org/10.5194/nhess-7-417-2007). *Slope stability assessment of weathered clay by using
> field data and computer modelling: a case study from Budapest.* Natural Hazards 45
> (as presented in the RS2 Slope Stability Verification Manual, Part III, Problem 59,
> "Stability of a Three-Layered Soil Slope", pp. 200–201).

A ~415 m wide × ~75 m tall real-coordinate hillslope in three layers: a YellowClay/Debris
cover (c = 50, φ = 15°, γ = 19), a thin weak **waste lens** (c = 1, φ = 5°, γ = 14) and a
strong GreyClay base (c = 250, φ = 30°, γ = 22). The waste lens is a wedge confined to the
left ~136 m — ~12.6 m thick at the toe face, tapering to zero at x = 136 — that daylights on
the toe. The critical mechanism is a **non-circular** translational slip riding the top of
the lens, which is what makes this an SSRM (not a circular-search) problem: an unconstrained
circular search misfinds the deeper competing surface (FS ≈ 1.9), whereas the SSRM localizes
the shear band through the c = 1 / φ = 5 lens on its own. Dry — no water table, tension crack,
seismic or loads. Elastic constants are the published Case-1 values (E = 50 000 kPa, ν = 0.4;
the vendor `.fez` reader does not parse E/ν); ψ = 0 (the Griffiths convention this corpus uses).

| Case | XSLOPE | RS2 SSRM | PLAXIS | Slide2 |
|---|---|---|---|---|
| Case 1 (published moduli), 3 m mesh | 1.553 | 1.57 (−1.1%) | 1.6 (−2.9%) | 1.567 |
| Case 2 (varying moduli) | — | 1.56 | 1.6 | 1.567 |

The published problem also runs a **Case 2** with varying moduli (GreyClay 20 000, YellowClay/
Debris 18 000, Waste 2 000 kPa). Since SSRM FS is insensitive to the elastic constants (an E-only
change), Case 2 is not a separate XSLOPE case and the row above carries the vendor columns only.

XSLOPE's SSRM lands on the Slide2 / RS2 SSRM cluster and just below PLAXIS. It is locked as a
**regression** anchor at the 3 m mesh, a full solve on the ~415 m section, rather than advertised
as converged.

<!-- test: file=files/rocscience/rs2_59.xlsx, type=fem_ssrm, expected_fs=1.553, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.3, f_max=1.9, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-59 -->

![RS2-59: Budapest three-layered soil slope (Görög & Török 2007), critical slip riding a thin weak waste lens (c = 1, φ = 5), SSRM 1.553 at the 3 m mesh — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-59.png)

### RS2-60: Generalized Hoek-Brown, homogeneous slope (Li et al. 2008) {#rs2-60}

**Input files:** [rs2_60a.xlsx](files/rocscience/rs2_60a.xlsx) (β = 15°) ·
[rs2_60b.xlsx](files/rocscience/rs2_60b.xlsx) (β = 30°) ·
[rs2_60c.xlsx](files/rocscience/rs2_60c.xlsx) (β = 45°)

A homogeneous rock slope at three angles, after

> [Li, A.J., Merifield, R.S., & Lyamin, A.V. (2008)](https://doi.org/10.1016/j.ijrmms.2007.08.010). "Stability charts for rock slopes based
> on the Hoek-Brown failure criterion." *International Journal of Rock Mechanics and Mining
> Sciences* 45(5), 689–700.

GSI = 70, $m_i$ = 15, $D$ = 0, γ = 23 kN/m³, ν = 0.3, $H$ = 1 m. This is the companion to the
[Hammah benchmark](#hoek-brown) at the opposite end of the criterion: GSI = 70 is a strong,
lightly-jointed rock mass, a = 0.501, essentially the classical exponent, where Hammah's GSI = 5
is a badly broken one at a = 0.619.

**The problem is normalized, and that is the trap.** Li's charts work in the dimensionless ratio
σci/(γH), and every case here sits at a *critical* ratio, so F ≈ 1 by construction. With
$H$ = 1 m, γH is just 23 kPa, and a critical ratio below one puts σci in the **sub-kPa to few-kPa
range** — a 1 m slope in 0.6 kPa rock is the same problem as a 100 m slope in 60 kPa rock.
Entering σci in MPa, as Hoek-Brown convention invites, overstates the strength a thousandfold and
the slope becomes trivially stable.

**Where σci comes from.** The manual never prints it, so each case takes σci straight from the
RS2 vendor model (the material's Generalized Hoek-Brown σci field in the `.fez`). That choice
matters because the vendor files and Li's Table 1 do not fully agree:

| case | β | published σci (vendor `.fez`) | ratio implied by the published σci | Li (2008) Table 1 ratio | agree? |
|---|---:|---:|---:|---:|:--:|
| a | 15° | 0.598 kPa | 0.026 | 0.026 | yes |
| b | 30° | 1.61 kPa | 0.070 | 0.075 | no |
| c | 45° | 4.37 kPa | 0.190 | 0.176 | no |

Only case a's published ratio reproduces the vendor σci. Using Li's ratios for b and c would give
1.725 kPa and 4.048 kPa instead of the vendor's 1.61 kPa and 4.37 kPa. XSLOPE uses the **vendor**
values, so the reconstruction is faithful to the RS2 model that actually produced the
published results rather than to a chart the model does not match.

**Factors of safety:**

| case | XSLOPE Bishop | XSLOPE Spencer | Slide2 Spencer | Li (limit analysis) |
|---|---|---|---|---|
| a (β = 15°) | 1.009 | 1.009 | 1.011 (−0.2%) | 1.0 (+0.9%) |
| b (β = 30°) | 0.987 | 0.989 | 0.992 (−0.3%) | 1.0 (−1.1%) |
| c (β = 45°) | 1.030 | 1.035 | 1.035 (0.0%) | 1.0 (+3.5%) |

*All three Spencer factors reproduce Slide2's own Spencer values almost exactly
(1.009 / 0.989 / 1.035 vs 1.011 / 0.992 / 1.035), confirming the Hoek-Brown implementation at
high GSI. Every case lands within 3.5% of unity, as a critical ratio should. SSRM is not
locked on this problem.*

**One more paper erratum, on case a.** Li's Table 1 labels its last block β = 10°, but the body
text and the charts say 15° (Fig. 5 is β = 15°; no β = 10° chart exists) — a typographical
error. RS2 read it as 15° too: its Slide2 value for case a (1.011) reproduces Li's own F for
that row.

<!-- test: file=files/rocscience/rs2_60a.xlsx, type=circular_search, method=spencer, expected_fs=1.009, num_slices=40, benchmark=RS2-60a -->
<!-- test: file=files/rocscience/rs2_60b.xlsx, type=circular_search, method=spencer, expected_fs=0.989, num_slices=40, benchmark=RS2-60b -->
<!-- test: file=files/rocscience/rs2_60c.xlsx, type=circular_search, method=spencer, expected_fs=1.035, num_slices=40, benchmark=RS2-60c -->

### RS2-61: Local and global minima, homogeneous slope (Cheng et al. 2007) {#rs2-61}

**Input files:** [rs2_61a.xlsx](files/rocscience/rs2_61a.xlsx) (one geometry; cases 1 & 3 locked
by circular LEM, case 2 locked by constrained SSRM, case 4 blocked)

A homogeneous benched slope, after

> [Cheng, Y.M., Lansivaara, T., & Wei, W.B. (2007)](https://doi.org/10.1016/j.compgeo.2006.10.011). "Two-dimensional slope stability analysis
> by limit equilibrium and strength reduction methods." *Computers and Geotechnics* 34, 137–150.

c = 5 kPa, φ = 30°, γ = 20 kN/m³. The problem exists to show how a search settles onto
*different* minima: case 1 is the unconstrained global minimum, while cases 2–4 fence an RS2
Polygon Search Area onto successive **local** minima. All four cases share the one geometry
([rs2_61a.xlsx](files/rocscience/rs2_61a.xlsx)); only the search region changes. Published:

| Case | Surface (RS2 fig.) | XSLOPE Spencer (LEM) | XSLOPE SSRM (SSR-zone) | XSLOPE Bishop | Slide2 | Cheng (ref) | RS2 SSR | Governing |
|---|---|---|---|---|---|---|---|---|
| 1 | mid-lower face (global) | **1.338** (locked) | — | 1.342 | 1.336 (+0.1%) | 1.327 (+0.8%) | 1.35 | Slide2 |
| 2 | deep toe-to-crest (Fig. 4) | *blocked* | **1.398** (locked) | — | 1.385 | 1.375 | 1.36 (+2.8%) | RS2 SSR |
| 3 | upper face, crest→bench (Fig. 5) | **1.437** (locked) | — | — | 1.443 (−0.4%) | 1.415 (+1.6%) | 1.42 | Slide2 |
| 4 | shallow near-crest (Fig. 6) | *blocked* | *blocked* | — | 1.397 | 1.40 | 1.42 | RS2 SSR |

**Case 1 (global).** Seeding the circular search with a toe-to-crest circle refines onto the
global minimum, a mid-lower-face circle daylighting between x ≈ 19 and 27, on which Spencer and
Bishop agree and both land on the Slide2 and Cheng values.

**Case 3 (upper-face local minimum).** `circular_search` takes optional search-window limits
(`center_box` / `entry_range` / `exit_range` / `tangent_depth`), the LEM analog of RS2's SSR
Polygon Search Area. Confining the Spencer search to the upper-face window read from **Fig. 5** —
entry on the crest bench (x ≈ 42–54), exit at the first bench (x ≈ 23–32), tangent bottoming at the
bench elevation (y ≈ 16–22) — redirects it off the global minimum and onto the distinct upper-face
one, where Spencer lands on the published Slide2 and Cheng values. The bounds come from the
figure's mechanism rather than from tuning to the number, and the same result holds across loosened
variants of the window.

**Cases 2 and 4 — LEM route (blocked).** RS2's Case-2 (deep toe-to-crest) and Case-4 (shallow
near-crest) minima come from a *strength-reduction* search pinned by a polygon area; they are
**not local minima of the circular LEM problem** on this geometry. A Spencer search confined to
Fig. 4's toe-to-crest window pins against the window edge, the deep family draining toward the
global with no interior minimum, and one confined to Fig. 6's near-crest window returns a higher
factor still, a shallow c = 5 circle on the 32° upper face being genuinely stronger. Neither
reproduces the published Cheng/Slide2 columns, so the LEM route to those columns is blocked; the
FEM route below reaches them.

**Cases 2 and 4 — FEM route, against RS2's SSR column.** `solve_ssrm` accepts an `ssr_zone`
polygon (RS2's "SSR Search Area"): strength reduction applies only to elements whose centroid lies
inside it, and everything outside is held at full strength. The polygon is **RS2's own**, read
verbatim from the native `slope stability #061_02.fez` / `#061_04.fez`, and RS2-61 carries no
material partition, so it is the whole constraint. Confining the SSRM to Fig. 4's deep toe-to-crest
zone reproduces Case 2: **SSRM 1.398 vs RS2 SSRM 1.36 (+2.8%)**, inside the corpus's usual
SSRM-vs-published band (cf. [RS2-63](#rs2-63) +2.1%), locked at the 1.0 m tri6 mesh. Case 4's
near-crest zone confines the mechanism to the correct shallow surface, but the confined mechanism
in c = 5 / φ = 30 is stiffer in XSLOPE's SSRM than in RS2's, and further above RS2's value than
Case 2 is on the same geometry, so Case 4 is reported rather than locked.

<!-- test: file=files/rocscience/rs2_61a.xlsx, type=circular_search, method=spencer, expected_fs=1.338, num_slices=40, benchmark=RS2-61a -->
<!-- test: file=files/rocscience/rs2_61a.xlsx, type=circular_search, method=spencer, expected_fs=1.437, num_slices=40, entry_range=42;54, exit_range=23;32, tangent_depth=16;22, benchmark=RS2-61-case3 -->
<!-- test: file=files/rocscience/rs2_61a.xlsx, type=fem_ssrm, expected_fs=1.398, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=1.0, f_max=2.0, max_iter=16000, ssr_zone=8.516;12.255;8.686;6.779;21.55;8.975;28.407;13.412;31.455;18.522;32.3046;20.2236;28.228;21.032;26.57;17.894;22.043;13.995;8.516;12.255, tension_srf=true, k0=1, benchmark=RS2-61-case2 -->

**Case 2 — deep toe-to-crest, constrained SSRM (rs2_61a)**

![RS2-61: local and global minima (Cheng et al. 2007), Case 2 (deep toe-to-crest), constrained SSRM 1.398 vs RS2 SSRM 1.36 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the mechanism confined to RS2's SSR-Search-Area polygon read verbatim from the vendor model](images/RS2-61-case2.png)

### RS2-62: Three-layered slope with a soft band (Cheng et al. 2007) {#rs2-62}

**Input files:** [rs2_62a.xlsx](files/rocscience/rs2_62a.xlsx) (Analysis I, 28 m) ·
[b](files/rocscience/rs2_62b.xlsx) (II, 20 m) · [c](files/rocscience/rs2_62c.xlsx) (III, 12 m)

A three-layer slope carrying a thin **soft band** (Soil 2: c = 0, φ = 25°) that dips through it
between a stronger cap (Soil 1: c = 20, φ = 35°) and base (Soil 3: c = 10, φ = 35°); γ = 19,
E = 14 MPa, ν = 0.3 throughout. From the same Cheng, Lansivaara & Wei (2007) paper as
[RS2-61](#rs2-61)/[63](#rs2-63). Three geometries narrow the band's daylight width (Analysis
I / II / III = 28 / 20 / 12 m domains), and each was run at two dilation angles — Case 1 (ψ = 0)
and Case 2 (ψ = φ, associated). **This is a hard, code-divergent benchmark by design**: for the
same ψ = 0 input, Plaxis and RS2 return ≈ 0.8–0.9 while Flac3D returns 1.03–1.64.

| Analysis | XSLOPE SSRM (ψ = 0) | RS2 SSR | Plaxis | Flac3D | Status |
|---|---|---|---|---|---|
| I (28 m) | ≈ 1.0 (coarse mesh) | 0.88 | 0.86 | 1.64 | not locked |
| II (20 m) | ≈ 1.0 (coarse mesh) | 0.89 | 0.85 | 1.30 | not locked |
| III (12 m) | **0.781** | 0.81 (−3.6%) | 0.82 (−4.8%) | 1.03 (−24.2%) | locked |

Case 2 (ψ = φ, associated flow) is **out of scope by construction** — XSLOPE's SSRM is
non-associated only (ψ = 0, the Griffiths convention). Its published values are recorded for
completeness and no dot rests on them:

| Analysis | RS2 SSR | Plaxis | Flac3D |
|---|---|---|---|
| I (28 m) | 0.98 | 0.97 | 1.61 |
| II (20 m) | 0.98 | 0.97 | 1.28 |
| III (12 m) | 0.93 | 0.94 | 1.03 |

**Band thickness (≈ 0.4 m) sets the mechanism.** The SSRM reproduces the Plaxis/RS2 ψ = 0
cluster only when the mesh resolves the soft band, so feature-aware refinement
(`refine_factor=3, refine_features=thin_zones`) drives ≥ 3 elements across it. Below that the
band is invisible to the solver and the slope reads as far too stable. Analyses I and II show the
same under-resolution (≈ 1.0), and band-only refinement does not fix them because their
wider-domain mechanism runs through the far field, so only the compact Analysis III geometry is
locked; it is the representative case for the family.

**The decisive input on this problem is tensile strength.** The vendor `.fez` assigns each
material an explicit tensile cap (`t_cut` = 20 / 0 / 10 kPa, equal to its cohesion) and reduces it
with the SRF (`tensilestrength_SRF: 1`). Without those caps, Mohr-Coulomb gives the cap soil an
implicit tensile strength of c/tan φ ≈ 28 kPa, which holds the steep entry cut at the crest shut,
and the FE then *genuinely* equilibrates far past the vendors' answer. With the vendor caps
carried into the model and reduced with the SRF, the band mechanism mobilizes as limit equilibrium
predicts, and the bisection returns **0.781** — 3.6% conservative of RS2 and 4.8% of Plaxis. The
geometry and strengths match the vendor model vertex for vertex.

**The vendor's own refinement region is not transcribed.** `#062_05`'s `disc regions:` block
declares an interior refinement rectangle over the band at 0.084 m against a 0.687 m boundary
discretization. The corpus mesh instead reaches the band through `refine_features=thin_zones`,
which leaves it finer than the vendor's in the band itself and coarser in the cap above it, where
this problem's tensile entry cut forms. That is a real difference from the vendor model, and it is
the caveat on the −3.6% rather than an explanation of it.

<!-- test: file=files/rocscience/rs2_62c.xlsx, type=fem_ssrm, expected_fs=0.781, element_type=tri6, target_size=0.45, tolerance=0.02, f_min=0.5, f_max=1.3, max_iter=40000, refine_factor=3, refine_features=thin_zones, tension_srf=true, k0=1, benchmark=RS2-62c -->

**Analysis III — 12 m domain, ψ = 0 (rs2_62c)**

![RS2-62: three-layered slope with a soft band (Cheng et al. 2007), Analysis III (12 m domain, ψ = 0, vendor tensile strengths, SSRM 0.781) — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the mechanism riding the soft band](images/RS2-62c.png)

### RS2-63: Slope stability assessment of a homogeneous slope (Cheng et al. 2007) {#rs2-63}

**Input files:** [rs2_63.xlsx](files/rocscience/rs2_63.xlsx)

An 11 m homogeneous slope, from the same Cheng, Lansivaara & Wei (2007) paper as
[RS2-61](#rs2-61). c = 10 kPa, φ = 30°, γ = 20 kN/m³ — a single, well-defined mechanism, so
LEM and SSRM agree:

| Method | XSLOPE | Governing published | XSLOPE Bishop | Cheng et al. |
|---|---|---|---|---|
| Spencer | 1.398 | Slide2 1.380 (+1.3%) | 1.401 | 1.383 (+1.1%) |
| SSRM | 1.409 | RS2 SSRM 1.38 (+2.1%) | — | — |

Both XSLOPE values run just above the published cluster — a consistent, small offset rather than a
method disagreement.

<!-- test: file=files/rocscience/rs2_63.xlsx, type=circular_search, method=spencer, expected_fs=1.398, num_slices=40, benchmark=RS2-63-lem -->
<!-- test: file=files/rocscience/rs2_63.xlsx, type=fem_ssrm, expected_fs=1.409, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.8, f_max=2.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-63 -->

![RS2-63: homogeneous slope (Cheng et al. 2007), SSRM 1.409 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-63.png)

### RS2-64: Slope stability assessment of three homogeneous landslides (Teoman et al. 2004) {#rs2-64}

**Input files:** locked — [a](files/rocscience/rs2_64a.xlsx) (C1) ·
[c](files/rocscience/rs2_64c.xlsx) (C3) · [e](files/rocscience/rs2_64e.xlsx) (C5) ·
[b](files/rocscience/rs2_64b.xlsx) (C2) · [d](files/rocscience/rs2_64d.xlsx) (C4) ·
[g](files/rocscience/rs2_64g.xlsx) (C7) · [k](files/rocscience/rs2_64k.xlsx) (C11) ·
[l_split](files/rocscience/rs2_64l_split.xlsx) (C12). Built but blocked — f (C6), h/i/j/l, and
[h_split](files/rocscience/rs2_64h_split.xlsx) (C8). C8 and C12 are rebuilt as the vendor material
partition for the `elastic_materials` run option.

Three road-cut landslides in Ankara clay along the E90 highway, after

> [Teoman, M.B., Topal, T. & Isik, N.S. (2004)](https://doi.org/10.1007/s00254-003-0954-3). "Assessment of slope stability in Ankara clay: a case
> study along E90 highway." *(RS2 Slope Stability Verification Manual, Part III, Problem 64, pp. 219–227.)*

Each of the three slopes is modeled in its **Original** (pre-slide) and **Failed** (post-slide,
with a scarp) profile, under a **short-term** (total-stress, dry) and a **long-term** (fully
saturated plus a 0.03 g horizontal pseudo-static coefficient) scenario — **12 single-material
Mohr-Coulomb cases** in all, whose strengths, elastic constants and tensile caps are read straight
from the vendor `.fez`. The manual reports three FS columns: RS2 SSRM, the Teoman reference
(Bishop), and Slide2 Bishop.

The decisive detail is **how RS2 obtained its SSR column**: *"The RS2 SSR Search Area option was
used to obtain the factor of safety for each of the proposed slip surfaces."* RS2 pinned each
strength-reduction run to a narrow band hugging a digitized *proposed* slip surface (manual
Fig. 4), and the native `.fez` states that band two ways at once — an explicit
`SSR_polygonal_zones` Search-Area polygon, and a material partition that places the Mohr-Coulomb
material only in a corridor along the proposed surface while the rest of the domain is
linear-elastic and cannot yield under any strength-reduction factor. The two nearly coincide: the
search polygon is 6.9 to 39.2% larger than the Mohr-Coulomb corridor in every one of the twelve
cases, so RS2's reducible region is strictly their intersection, and the strip between them is soil
the mechanism does not use on any case but C4.

Each corpus file carries the vendor's search polygon through `solve_ssrm`'s `ssr_zone`, read
verbatim from the `.fez`. One approximation remains: `ssr_zone` holds the outside-corridor elements
at **full Mohr-Coulomb strength**, whereas the vendor makes them **elastic**. That is immaterial
where the base slope is stable at full strength, but where it is **sub-unity** a failing skin
outside the corridor cannot be suppressed and the constrained solve reports the slope unstable, so
the two sub-unity cases (C8, C12) are rebuilt as the explicit **material partition** RS2 uses,
through `solve_ssrm`'s `elastic_materials` run option on the vendor's own per-element footprint.

The three **short-term Original** slopes have simple convex profiles whose unconstrained global
minimum coincides with the pinned surface, so they lock unconstrained; the two **long-term
Original** slopes (C7, C11) and the two scarped **short-term Failed** slopes (C2, C4) lock inside
each case's own SSR polygon, and C12 on the vendor material partition. All eight verify against
RS2's own SSR column, the same method under two names and the only pairing on this row that can
carry a difference. The four cases that lock against nothing — C6 and C8–C10 — are built and
measured but are not tabulated, because a value the suite does not regenerate cannot be held to
the row beside it:

| Case | Geometry | XSLOPE SSRM | RS2 SSR | Teoman ref* | Slide2 | Lock verifies vs | Status |
|---|---|---|---|---|---|---|---|
| C1 | Slope 1 ST Original | **5.189** | 5.14 (+1.0%) | 5.25 | 5.24 | RS2 SSRM (+1.0%) | *locked* |
| C3 | Slope 2 ST Original | **4.807** | 4.69 (+2.5%) | 4.87 | 4.89 | RS2 SSRM (+2.5%) | *locked* |
| C5 | Slope 3 ST Original | **5.620** | 5.47 (+2.7%) | 5.44 | 5.45 | RS2 SSRM (+2.7%) | *locked* |
| C7 | Slope 1 LT Original | **1.639** | 1.70 (−3.6%) | 1.79 | 1.68 | RS2 SSRM (−3.6%), & Slide2 1.68 | *locked* |
| C11 | Slope 3 LT Original | **1.403** | 1.46 (−3.9%) | 1.51 | 1.51 | RS2 SSRM (−3.9%) | *locked* |
| C2 | Slope 1 ST Failed | **6.564** | 6.10 (+7.6%) | 6.67 | 6.64 | RS2 SSRM (+7.6%) | *locked* |
| C4 | Slope 2 ST Failed | **5.461** | 4.95 (+10.3%) | 5.32 | 5.32 | RS2 SSRM (+10.3%) — **sets the dot** | *locked* |
| C12 | Slope 3 LT Failed | **1.147** (elastic split) | 1.22 (−6.0%) | 1.13 | 1.15 | RS2 SSRM (−6.0%) | *locked* |

*\*Ref = Teoman et al. (SLOPE/W v.4 Bishop); Slide2 = Slide2 5.0 Bishop. Each percentage is
against the authority named beside it in the "Lock verifies vs" column.*

**The five Original locks** (C1/C3/C5 unconstrained, C7/C11 constrained) sit +1.0 to +2.7% and
−3.6 to −3.9% from RS2's SSRM, the positive offset matching the usual SSRM-vs-published gap
(cf. [RS2-63](#rs2-63), +2.1%). They are locked at the 1.0 m tri6 mesh.

**C2 and C4 are the row's widest same-method differences, at +7.6% and +10.3%.** On these two
scarped short-term Failed geometries RS2's *own* SSR column sits **below its own Bishop columns**
(C2 6.10 vs 6.67 / 6.64, −8.5%; C4 4.95 vs 5.32 / 5.32, −7.0%), whereas on the Originals RS2's
SSRM and Bishop agree. XSLOPE's constrained SSRM sits with the Bishop cluster instead, so Teoman,
Slide2 and XSLOPE triangulate against each other while RS2's strength-reduction column stands apart
from all three; C12 is the same situation with the sign reversed. That agreement is a
**cross-bearing**, not a pairing: Bishop is a limit-equilibrium method and this row's quantity is a
strength-reduction factor, so it is reported as context and cannot carry the comparison. Against
the only same-method authority the problem publishes, C4 sets this row's dot.

Part of the separation is the vendor's tensile caps, which every lock above carries and which a
strength-reduction analysis feels where a Bishop analysis on a pinned circular surface essentially
does not. That does not account for the whole gap, and the residual divergence is **unexplained**:
it is not a truncated strength-reduction sweep — each vendor `.fea` runs an automatic SRF search
whose reported values lie far above the `final_SRF` field, a vestigial default — and nothing
further in the files evidences a cause.

**C6 stays blocked on its corridor.** C6 is the narrowest scarped geometry — its `#064_06` corridor
is ≈ 8 m wide against ≈ 15 m for C4, at identical strengths — and the tight corridor forces a
stiffer mechanism than any published surface, so it locks against nothing.

The 0.03 g pseudo-static coefficient acts in the destabilizing direction on every long-term case
(RS2 `bx = +0.03`, downslope for these left-high slopes). Teoman's and Slide2's Bishop values are
taken on a digitized proposed surface the paper does not publish, and an unconstrained circular
search does not reach them: it tracks them on the smooth short-term originals but finds a lower
minimum than the pinned surface elsewhere, and confining the search to the crest-to-toe mechanism
the figures draw removes those skins without closing the gap.

<!-- test: file=files/rocscience/rs2_64a.xlsx, type=fem_ssrm, expected_fs=5.189, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=4.0, f_max=7.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-64a -->
<!-- test: file=files/rocscience/rs2_64c.xlsx, type=fem_ssrm, expected_fs=4.807, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=3.5, f_max=6.5, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-64c -->
<!-- test: file=files/rocscience/rs2_64e.xlsx, type=fem_ssrm, expected_fs=5.620, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=4.0, f_max=7.5, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-64e -->
<!-- test: file=files/rocscience/rs2_64b.xlsx, type=fem_ssrm, expected_fs=6.564, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=5.5, f_max=8.0, max_iter=16000, ssr_zone=8.586;8.21;5.834;6.959;6.985;3.006;10.538;-0.747;16.793;-1.748;22.947;-1.097;24.499;1.555;22.797;3.006;20.445;1.305;17.043;1.005;11.939;1.805;9.54718;4.7567;9.637;7.109, tension_srf=true, k0=1, benchmark=RS2-64b -->
<!-- test: file=files/rocscience/rs2_64d.xlsx, type=fem_ssrm, expected_fs=5.461, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=4.5, f_max=6.5, max_iter=16000, ssr_zone=4.467;6.136;3.297;3.758;6.455;0.717;11.056;-1.272;17.645;-1.272;18.737;0.795;17.489;1.691;15.345;0.561;10.003;1.418;5.949;4.031;4.467;6.136, tension_srf=true, k0=1, benchmark=RS2-64d -->
<!-- test: file=files/rocscience/rs2_64g.xlsx, type=fem_ssrm, expected_fs=1.639, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=1.0, f_max=2.5, max_iter=16000, ssr_zone=6.726;7.086;5.442;5.549;6.703;3.353;8.58;0.973;12.299;-1.186;15.538;-1.726;19.497;-1.846;22.991;0.615;19.668;1.926;17.788;0.352;12.322;1.445;9.131;3.675;6.726;7.086, tension_srf=true, k0=1, benchmark=RS2-64g -->
<!-- test: file=files/rocscience/rs2_64k.xlsx, type=fem_ssrm, expected_fs=1.403, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.9, f_max=2.2, max_iter=16000, ssr_zone=3.413;5.74;2.387;4.091;3.413;2.113;5.538;0.391;9.604;-1.404;12.242;-1.404;14.0932;-0.511713;14.0932;1.014;11.839;1.014;10.593;0.465;8.175;1.454;5.831;2.699;4.45466;4.16031;3.413;5.74, tension_srf=true, k0=1, benchmark=RS2-64k -->
<!-- test: file=files/rocscience/rs2_64l_split.xlsx, type=fem_ssrm, expected_fs=1.147, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=0.8, f_max=2.0, max_iter=16000, elastic_materials=rock2a;rock2b, tension_srf=true, k0=1, benchmark=RS2-64l-split -->

**Case 1 — Slope 1 short-term Original (rs2_64a)**

![RS2-64: Ankara E90 landslides (Teoman et al. 2004), Case 1 (Slope 1 short-term Original), SSRM 5.189 vs RS2 SSRM 5.14 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the deep rotational mechanism coinciding with RS2's pinned Search-Area surface](images/RS2-64a.png)

**Case 2 — Slope 1 short-term Failed (rs2_64b)**

![RS2-64: Ankara E90 landslides (Teoman et al. 2004), Case 2 (Slope 1 short-term Failed), constrained SSRM 6.564 vs RS2 SSRM 6.10 (+7.6%); RS2's own SSRM sits 8–9% below its Bishop columns 6.67/6.64, which XSLOPE lands on, and the vendor tensile caps move XSLOPE part of the way toward RS2 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the mechanism confined to RS2's SSR-Search-Area polygon read verbatim from the vendor model](images/RS2-64b.png)

**Case 4 — Slope 2 short-term Failed (rs2_64d)**

![RS2-64: Ankara E90 landslides (Teoman et al. 2004), Case 4 (Slope 2 short-term Failed), constrained SSRM 5.461 vs RS2 SSRM 4.95 (+10.3%); RS2's own SSRM sits ~7% below its Bishop columns 5.32/5.32, which XSLOPE lands on, and the vendor tensile caps move XSLOPE part of the way toward RS2 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the mechanism confined to RS2's SSR-Search-Area polygon read verbatim from the vendor model](images/RS2-64d.png)

**Case 7 — Slope 1 long-term Original (rs2_64g)**

![RS2-64: Ankara E90 landslides (Teoman et al. 2004), Case 7 (Slope 1 long-term Original), constrained SSRM 1.639 vs RS2 SSRM 1.70 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the mechanism confined to RS2's SSR-Search-Area polygon read verbatim from the vendor model](images/RS2-64g.png)

**Case 11 — Slope 3 long-term Original (rs2_64k)**

![RS2-64: Ankara E90 landslides (Teoman et al. 2004), Case 11 (Slope 3 long-term Original), constrained SSRM 1.403 vs RS2 SSRM 1.46 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the mechanism confined to RS2's SSR-Search-Area polygon read verbatim from the vendor model](images/RS2-64k.png)

**Case 12 — Slope 3 long-term Failed, vendor material partition (rs2_64l_split)**

![RS2-64: Ankara E90 landslides (Teoman et al. 2004), Case 12 (Slope 3 long-term Failed), constrained SSRM 1.147 vs RS2 SSRM 1.22 — FEM inputs, mesh, maximum shear strain and displacement vectors at the critical SRF, the mechanism confined to the vendor's Mohr-Coulomb corridor with the surrounding zones held linear-elastic](images/RS2-64l-split.png)

### RS2-65: Slope stability assessment of a tailings dam (Tzenkov 2008) {#rs2-65}

**Input files:** [rs2_65.xlsx](files/rocscience/rs2_65.xlsx)

The Padina tailings dam, after

> Tzenkov, A. (2008). *(as cited in the RS2 Slope Stability Verification Manual, Part III,
> Problem 65, "Slope Stability Assessment of a Tailings Dam", Table 1, pp. 230–231).*

A 225 m wide × 77 m tall cross-section of an **eight-material** tailings dam with a
**phreatic surface**. Twelve zones tile the domain with no gaps or overlaps (union area =
domain area = 13 262 m²): a Marl base, Marly-Clay and Alluvial-Clay bands, a Counterfill
body, the Tailings core (c = 0, φ = 34.8°) and the Rockfill/Fill embankment shells. Pore
pressure is applied from a single 14-point phreatic surface connected to every material
(static groundwater — the vendor `.fez` carries no FE seepage solution to read). Strength
parameters are Table 1 = the `.fez`; the elastic constants E, ν are Table 1 (the `.fez`
imports E = 0, so they must be supplied for the FE build); ψ = 0 (the Griffiths convention
this corpus uses).

| Method | XSLOPE | RS2 SSRM | Slide2 LEM | Reference LEM | Reference FEM |
|---|---|---|---|---|---|
| SSRM (2.2 m mesh, the vendor's own density) | 1.306 | 1.29 (+1.2%) | 1.41 circular / 1.33 non-circular | 1.39 | 1.41 (−7.4%) |

**The lock is taken at RS2's own discretization.** Every physical input on this eight-material
section transcribes verbatim, and the mesh is one of the inputs the `.fez` specifies: RS2 solves
5 224 six-node triangles on 10 687 nodes, where a 3 m target size gives 3 798 on 7 803 nodes. The lock is
therefore taken at the vendor's own ~2.2 m size, where the SSRM reads **1.306**, +1.2% from RS2's
1.29 and inside the published 1.29–1.41 band.

**The factor does not descend steadily toward that value.** Across the refinement range it reads
**1.344 / 1.344 / 1.294** at 8 / 5 / 3 m and then returns to the 1.306 locked at 2.2 m, so the
finest mesh is not the lowest and the lock is a regression anchor at a stated discretization
rather than a refinement limit.

<!-- test: file=files/rocscience/rs2_65.xlsx, type=mesh_elements, element_type=tri6, target_size=3.0, expected_elements=3798, expected_nodes=7803, benchmark=RS2-65-mesh -->
<!-- test: file=files/rocscience/rs2_65.xlsx, type=fem_ssrm, expected_fs=1.344, element_type=tri6, target_size=8.0, tolerance=0.02, f_min=1.1, f_max=1.5, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-65-m8 -->
<!-- test: file=files/rocscience/rs2_65.xlsx, type=fem_ssrm, expected_fs=1.344, element_type=tri6, target_size=5.0, tolerance=0.02, f_min=1.1, f_max=1.5, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-65-m5 -->
<!-- test: file=files/rocscience/rs2_65.xlsx, type=fem_ssrm, expected_fs=1.294, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.1, f_max=1.5, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-65-m3 -->
<!-- test: file=files/rocscience/rs2_65.xlsx, type=fem_ssrm, expected_fs=1.306, element_type=tri6, target_size=2.2, tolerance=0.02, f_min=1.1, f_max=1.5, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-65 -->

![RS2-65: Padina tailings dam (Tzenkov 2008), 8 materials + phreatic surface, SSRM 1.306 at the vendor's own 2.2 m mesh — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-65.png)

### RS2-66: Embankment basal stability (Nakamura et al. 2008) {#rs2-66}

**Input files:** [rs2_66a.xlsx](files/rocscience/rs2_66a.xlsx) (h₁ = 2 m) ·
[b](files/rocscience/rs2_66b.xlsx) (4 m) · [c](files/rocscience/rs2_66c.xlsx) (6 m) ·
[d](files/rocscience/rs2_66d.xlsx) (8 m) · [e](files/rocscience/rs2_66e.xlsx) (10 m)

A 10 m high embankment on soft ground, after

> [Nakamura, A., Cai, F., & Ugai, K. (2008)](https://doi.org/10.1201/9780203885284-c107). "Embankment basal stability analysis using shear
> strength reduction finite element method." *(as cited in the RS2 Slope Stability Verification
> Manual, Part III, Problem 66).*

A cohesionless fill (c = 0, φ = 35°, 1.5:1 side slopes, 20 m crest, 10 m high) is placed on a
**soft** upper foundation stratum (φ = 0, c = 35 kPa) of thickness h₁ over a firm 10 m bearing
stratum (φ = 0, c = 100 kPa); γ = 18.82 kN/m³ throughout, with the vendor model's own elastic
constants and its flat 50 kPa tensile cap on all three materials. The soft-layer thickness h₁ is
the varied parameter (2, 4, 6, 8, 10 m), and every file declares a mesh refinement polygon over its
soft stratum at one size, 1.05 m.

**Two mechanisms.** One is the **deep basal squeeze** through the soft φ = 0 band — the mechanism
the manual's shear-strain figures show, the one its SSR column reports, and the one h₁ governs.
The other is a **surficial skin on the c = 0 embankment face**: the 1.5H:1V faces are purely
frictional, so a surface-parallel slide has the depth-independent closed form
FS = tan 35° / tan 33.69° = **1.050**, the same value at every h₁, the corpus's recurring c = 0
mechanism met on [RS2-4](#rs2-4), [RS2-40](#rs2-40), [VP81](#rs2-39) and VP69.

The skin is the shallower of the two and it is what an unfiltered SSRM reports: across the family
the filter-off value is **1.031** at three of the five thicknesses, −1.8% on the closed-form 1.050,
and **1.044** at the thinnest and the thickest band — nearly one number rather than a trend in h₁,
exactly as a depth-independent mechanism should behave. Setting `min_slip_depth` = 4 m — below the
fill skin, above the basal band — excludes the skin and returns the deep mechanism, which is far
stronger than the skin under the two thinnest bands and comes down to the skin's own level across
the three thicker ones.
Both are locked:

| h₁ (m) | XSLOPE SSRM, filter off (face skin) | XSLOPE SSRM, `min_slip_depth` = 4 m (deep) | RS2 SSR | Slide2 Spencer | Nakamura LEM | Nakamura FEM |
|---|---|---|---|---|---|---|
| 2 | 1.044 | 1.169 | 1.13 | 1.05 | 1.21 | 1.24 |
| 4 | 1.031 | 1.169 | 1.19 | 1.16 | 1.22 | 1.16 |
| 6 | 1.031 | 1.031 | 1.13 | 1.10 | 1.22 | 1.16 |
| 8 | 1.031 | 1.056 | 1.08 | 1.13 | 1.10 | 1.10 |
| 10 | 1.044 | 1.031 | 1.05 | 1.05 | 1.08 | 1.08 |

**Which mechanism each published column reports.** RS2's SSR column is the deep mechanism
throughout: the filtered XSLOPE row reads above it at the thinnest band and below it at the other
four thicknesses, the widest of the four being the 6 m band. Those differences are recorded beside
the published values, not scored against them, because every published strength-reduction solution
of this problem runs associated flow (ψ = φ) where XSLOPE runs ψ = 0 — a modeling difference the
manual's own problem statement declares, confined to the granular fill since both φ = 0 clays are
dilationless either way. This row's dot is therefore the face skin's, whose closed form carries no
flow rule at all. The Slide2 Spencer column is **not one mechanism**: at h₁ = 2 m and h₁ = 10 m it
reports 1.05, the face-skin closed form to three significant figures, and at h₁ = 4 / 6 / 8 m it
reports the deeper surface, so the two XSLOPE columns above are what keeps the comparison like for
like.

**Mesh.** Both mechanisms run through material with no length scale of its own — the c = 0 fill on
the face, the φ = 0 clay under it — so both follow the element size. At the model's 3 m global size
the soft band would carry about one element row, so the family's 1.05 m refinement polygon over
that band is what resolves it, at one size across all five thicknesses so the rows stay comparable
with each other. Everything else — the boundary fixity, the isotropic K = 1 field stress and the
vendor's flat 50 kPa tensile cap — is transcribed from the vendor model.

<!-- test: file=files/rocscience/rs2_66a.xlsx, type=fem_ssrm, expected_fs=1.044, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-66a -->
<!-- test: file=files/rocscience/rs2_66b.xlsx, type=fem_ssrm, expected_fs=1.031, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-66b -->
<!-- test: file=files/rocscience/rs2_66c.xlsx, type=fem_ssrm, expected_fs=1.031, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-66c -->
<!-- test: file=files/rocscience/rs2_66d.xlsx, type=fem_ssrm, expected_fs=1.031, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-66d -->
<!-- test: file=files/rocscience/rs2_66e.xlsx, type=fem_ssrm, expected_fs=1.044, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-66e -->

<!-- test: file=files/rocscience/rs2_66a.xlsx, type=fem_ssrm, expected_fs=1.169, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, min_slip_depth=4, k0=1, benchmark=RS2-66a-deep -->
<!-- test: file=files/rocscience/rs2_66b.xlsx, type=fem_ssrm, expected_fs=1.169, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, min_slip_depth=4, k0=1, benchmark=RS2-66b-deep -->
<!-- test: file=files/rocscience/rs2_66c.xlsx, type=fem_ssrm, expected_fs=1.031, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, min_slip_depth=4, k0=1, benchmark=RS2-66c-deep -->
<!-- test: file=files/rocscience/rs2_66d.xlsx, type=fem_ssrm, expected_fs=1.056, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, min_slip_depth=4, k0=1, benchmark=RS2-66d-deep -->
<!-- test: file=files/rocscience/rs2_66e.xlsx, type=fem_ssrm, expected_fs=1.031, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=0.8, f_max=1.6, max_iter=16000, tension_srf=true, min_slip_depth=4, k0=1, benchmark=RS2-66e-deep -->

The first two figures below are the filter-off runs: at h₁ = 2 m the strain concentrates in the
face skin, while at h₁ = 10 m the soft layer is thick enough that the deep squeeze has weakened
to the skin's own level and the contours fill it. The third is the filtered run on the same
model and mesh, showing what the 4 m cutoff selects instead. The intermediate thicknesses are not
drawn separately: filter off, the skin is the same depth-independent mechanism at every h₁, and
filtered, they are the same basal squeeze through a thicker band.

**Thinnest soft band — h₁ = 2 m (rs2_66a)**

![RS2-66a: embankment basal stability (Nakamura et al. 2008), thinnest soft band (h₁ = 2 m), filter off, SSRM 1.044 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the strain concentrated in the face skin](images/RS2-66a.png)

**Thickest soft band — h₁ = 10 m (rs2_66e)**

![RS2-66e: the same embankment with the thickest soft band (h₁ = 10 m), filter off, SSRM 1.044 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the two mechanisms nearly meeting (1.044 filter off against 1.031 filtered) and the contours filling the soft layer](images/RS2-66e.png)

**Thinnest soft band, deep mechanism — h₁ = 2 m, `min_slip_depth` = 4 m (rs2_66a)**

![RS2-66a with the 4 m depth filter: the deep basal mechanism, SSRM 1.169 against RS2 SSR 1.13 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the strain filling the fill body and concentrating at both toes where it meets the soft φ = 0 band, and the embankment spreading outward on both sides instead of one face sliding](images/RS2-66a-deep.png)

### RS2-67: Earth dam under steady & transient unsaturated seepage (Huang & Jia 2009) {#rs2-67}

**Input files:** [rs2_67a.xlsx](files/rocscience/rs2_67a.xlsx) (Case 1, dry) ·
[rs2_67b.xlsx](files/rocscience/rs2_67b.xlsx) (Case 2, steady — own-flow) ·
[rs2_67c.xlsx](files/rocscience/rs2_67c.xlsx) (Case 3, 90 h downstream) ·
[rs2_67d.xlsx](files/rocscience/rs2_67d.xlsx) (Case 3, 90 h upstream) ·
[rs2_67e.xlsx](files/rocscience/rs2_67e.xlsx) (Case 4, 1500 h downstream — own-flow) ·
[rs2_67f.xlsx](files/rocscience/rs2_67f.xlsx) (Case 4, 1500 h upstream — own-flow)

A homogeneous earth dam evaluated at successive seepage states, after

> [Huang, M., & Jia, C-Q. (2009)](https://doi.org/10.1016/j.compgeo.2008.03.006). "Strength reduction FEM in stability analysis of soil slopes
> subjected to transient unsaturated seepage." *Computers and Geotechnics* 36(1–2), 93–101.
> *(as cited in the RS2 Slope Stability Verification Manual, Part III, Problem 67).*

The dam is a single Mohr-Coulomb material (c = 13.8 kPa, φ = 37°, γ = 18.2 kN/m³, E = 10⁵ kPa,
ν = 0.3), 21.3 m tall above the benches on a 191.4 m base, with a 1V:3.1H upstream face and a
1V:2.4H downstream face over toe benches both at el 7.30 m and a 7.30 m crest at el 28.60 — the
dimensions printed on the manual's Figure 1. The manual runs six SSRM stages: **Case 1** dry; **Case 2** with
a steady downstream free surface; **Case 3** the downstream and upstream faces 90 h after a rapid
drawdown; **Case 4** the same faces at 1500 h. The two sub-analyses per drawdown time share one
snapshot pore-pressure field — they differ only in which face the SSR search targets (the upstream
run confines strength reduction to RS2's upstream Search Area, so the mechanism is the upstream
slope rather than the weaker downstream one).

**Which geometry.** The vendor ships this dam twice. The authored section — benches both at
el 7.30 m, crest el 28.60, crest width 7.30 m, base 191.4 m, every dimension printed on the
manual's own Figure 1 — is the one in the dry, steady and 1500 h files. The two 90 h files carry a
slightly rotated re-import of the same dam (benches 6.663 / 6.86 m, crest 28.162, left edge not
quite vertical), 4.2% lighter by section area, and they keep it, because their pore pressures
**are** the vendor's own 90 h mesh and the geometry has to agree with the field it carries. The
choice is not cosmetic: on the authored section the tailwater el 7.30 m sits exactly **on** the
downstream bench, so the downstream pool has zero depth — which is why the steady and 1500 h vendor
files carry no downstream load at all — and the upstream driving head is (24.4 − 7.3) = 17.10 m
rather than the 17.74 m the re-imported bench elevation would give.

**How the stages are built.** The dry case and both 90 h faces are imported directly: RS2's
*computed* `.fea` carries the solved pore-pressure field as a per-node block, and that field goes
through XSLOPE's external-pore-pressure path (`u='seep'`), so the SSRM runs on RS2's own mesh with
RS2's own snapshot pore pressures and the comparison isolates the strength-reduction mechanics.
Each snapshot field is, to machine precision, hydrostatic below a 14-point phreatic surface, so
RS2 represents each transient state as a water-table position rather than a spatially complex
field.

The steady (Case 2) and 1500 h (Case 4) computed files carry no recoverable solved field, so both
are **reconstructed from the vendor groundwater BC block** — and both turn out to be *steady*
problems. Case 2, at full pool, retains its BC block (upstream reservoir total head 24.4 m,
downstream tailwater 7.3 m, downstream seepage face), so XSLOPE solves its own steady unconfined
seepage, with the reservoir also entering as an external hydrostatic normal load on the wetted
upstream boundary; without that face load the upstream toe has no confining water pressure and
fails immediately. **Case 4 is the decisive read of the vendor model:** its groundwater `.slw` is a
single steady stage with every specified-head node drawn fully down to the tailwater, so RS2
renders the "1500 h" stage as the **fully-drained steady state** at the drawn-down pool rather than
a literal-time snapshot, and XSLOPE reconstructs it as Case 2 with the pool lowered and no face
load on either side.

**Own transient-flow cross-check.** XSLOPE's uncoupled transient solver is exercised directly on
this dam: starting from the steady full pool (el 24.4), the reservoir is stepped to the tailwater
(el 7.3) at *t* = 0 and the dam drains with RS2's own hydraulics. At 90 h the computed phreatic
surface overlays RS2's own imported 90 h field to a mean 0.01 m on the upstream face, parting only
in the thin crest and core. With RS2's slow conductivity the same run is still far from drained at
1500 h, which is why RS2 renders Case 4 by the drained steady limit rather than the literal-time
solution.

![RS2-67 90 h phreatic surface: own transient flow vs RS2 imported field](images/rs2_67_fielddiff.png)

| Stage | XSLOPE SSRM | RS2 SSR | Slide2 (Bishop / Janbu / Spencer / GLE) | ref LEM | ref FEM | status |
|---|---|---|---|---|---|---|
| Case 1 — dry | **2.502** | 2.48 (+0.9%) | 2.45 / 2.32 / 2.44 / 2.42 | 2.43 | 2.50 (+0.1%) | **built** |
| Case 2 — steady, downstream | **1.695** | 1.70 (−0.3%) | 1.64 / 1.55 / 1.73 / 1.71 | 1.70 | 1.78 (−4.8%) | **built** — own flow field |
| Case 3 — 90 h, downstream | **1.820** | 1.83 (−0.5%) | 1.77 / 1.68 / 1.88 / 1.85 | 1.92 | 2.08 (−12.5%) | **built** |
| Case 3 — 90 h, upstream | **2.008** | 2.04 (−1.6%) | 1.99 / 1.89 / 2.07 / 2.06 | 2.03 | — | **built** |
| Case 4 — 1500 h, downstream | **2.320** | 2.34 (−0.9%) | 2.22 / 2.09 / 2.35 / 2.31 | 2.38 | 2.42 (−4.1%) | **built** — own flow field |
| Case 4 — 1500 h, upstream | **2.742** | 2.76 (−0.7%) | 2.66 / 2.52 / 2.79 / 2.76 | 2.80 | — | **built** — own flow field |

All six stages land within 1.6% of RS2's own SSR column, and five of the six within 1%.

Cases 2 and 4 land inside the Slide2 LEM method spread as well as on RS2's SSR column, so
reconstructing the field from the vendor's boundary conditions costs about a percent, not several.
The unsaturated curve was never a candidate for the residual — with RS2's built-in permeability
model reproduced as a tabulated curve the Case-2 head field is nearly SWCC-invariant, and Case 4 is
a zero-flow equilibrium at the drawn-down pool, so its field is conductivity-independent outright.

FS rises monotonically as the dam drains, so the governing minimum across the drawdown sequence is
the steady full pool (Case 2); Cases 3 and 4 verify the safer rising states.

<!-- test: file=files/rocscience/rs2_67a.xlsx, type=fem_ssrm, expected_fs=2.502, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=1.5, f_max=3.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-67a -->
<!-- test: file=files/rocscience/rs2_67c.xlsx, type=fem_ssrm, expected_fs=1.820, tolerance=0.02, f_min=1.0, f_max=3.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-67c -->
<!-- test: file=files/rocscience/rs2_67d.xlsx, type=fem_ssrm, expected_fs=2.008, tolerance=0.02, f_min=1.0, f_max=3.0, max_iter=16000, ssr_zone=-6.95691;-29.8799;102.318;-29.8799;102.318;66.9821;-6.95691;66.9821, tension_srf=true, k0=1, benchmark=RS2-67d -->
<!-- test: file=files/rocscience/rs2_67b.xlsx, type=fem_ssrm, expected_fs=1.695, tolerance=0.02, f_min=1.0, f_max=3.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-67b -->
<!-- test: file=files/rocscience/rs2_67e.xlsx, type=fem_ssrm, expected_fs=2.320, tolerance=0.02, f_min=1.0, f_max=3.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-67e -->
<!-- test: file=files/rocscience/rs2_67f.xlsx, type=fem_ssrm, expected_fs=2.742, tolerance=0.02, f_min=1.0, f_max=3.0, max_iter=16000, ssr_zone=-5.89862;-33.6746;102.478;-33.6746;102.478;70.3747;-5.89862;70.3747, tension_srf=true, k0=1, benchmark=RS2-67f -->

Two of the six stages are drawn, one for each mechanism the row carries. The unconstrained
stages differ only in the pore-pressure field they run on, and the two upstream stages differ
only in the drawdown time, so the remaining four repeat one of these two pictures.

**Case 2 — steady full pool, own flow field (rs2_67b)**

![RS2-67 Case 2: the dam at full pool on XSLOPE's own steady seepage solve, SSRM 1.695 against RS2 SSR 1.70 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the unconstrained mechanism on the downstream face, which governs the drawdown sequence](images/RS2-67b.png)

**Case 3 — 90 h after drawdown, upstream Search Area (rs2_67d)**

![RS2-67 Case 3 upstream: RS2's own imported 90 h drawdown field with strength reduction confined to the vendor's upstream Search Area, SSRM 2.008 against RS2 SSR 2.04 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the mechanism on the upstream face instead of the weaker downstream one](images/RS2-67d.png)

### RS2-68: Stability of seismically loaded slopes (Loukidis et al. 2003) {#rs2-68}

**Input files:** [rs2_68a.xlsx](files/rocscience/rs2_68a.xlsx) (Case 1, r<sub>u</sub> = 0.5) ·
[b](files/rocscience/rs2_68b.xlsx) (Case 2, dry) · [c](files/rocscience/rs2_68c.xlsx) (Case 3, 3-layer)

The one problem on this page whose target is **not a factor of safety** but a
**critical seismic coefficient** k꜀, after

> [Loukidis, D., Bandini, P., & Salgado, R. (2003)](https://doi.org/10.1680/geot.2003.53.5.463). "Stability of seismically loaded slopes
> using limit analysis." *Géotechnique*, 53(5), 463–479. *(RS2 Slope Stability Verification
> Manual, Part III, Problem 68.)*

k꜀ is the horizontal pseudo-static coefficient at which the slope is **just stable** — the k
for which the searched minimum FS = 1. Three cases share a 25 m, 1V:3H homogeneous slope
(c = 25 kPa, φ = 30°, γ = 20 kN/m³) except where noted: **Case 1** adds a pore-pressure ratio
r<sub>u</sub> = 0.5; **Case 2** is dry; **Case 3** replaces the homogeneous body with three
dipping rock bands on a benched profile — an upper wedge (c = 4, φ = 30, γ = 17), a
weak-friction middle band (c = 25, **φ = 15**, γ = 19) that the mechanism rides, and a strong
base (c = 15, φ = 45, γ = 19).

This is one of the [limit-equilibrium rows](#methodology) on this page: the harness searches the
**LEM** minimum to FS = 1, so the comparison is against the manual's LEM columns and the reference
limit-analysis bounds, with RS2's own SSRM k꜀ quoted as a cross-bearing. No SSRM value on this row
is locked; the strength-reduction leg is measured on Case 3 and reported under
[the SSRM cross-check](#rs2-68-ssrm) below.

XSLOPE reproduces k꜀ with a `critical_kc` harness: FS falls monotonically as k rises, so k꜀ is a
single crossing, located by bisecting k on a near-critical circle and confirming with a full search
at that k.

**Governing comparisons** — one authority per column, like-for-like on method:

| Case | Method | XSLOPE k꜀ | Slide2 | Loukidis (same method) |
|---|---|---|---|---|
| 1 (r<sub>u</sub> = 0.5) | Bishop | 0.127 | 0.118 (+7.6%) | 0.127 (0.0%) |
| 1 (r<sub>u</sub> = 0.5) | Spencer | 0.132 | 0.132 (0.0%) | 0.131 (+0.8%) |
| 2 (dry) | Bishop | 0.426 | 0.425 (+0.2%) | 0.426 (0.0%) |
| 2 (dry) | Spencer | 0.433 | 0.431 (+0.5%) | 0.431 (+0.5%) |
| 3 (3-layer) | Bishop | 0.169 | 0.155 (+9.0%) | — |
| 3 (3-layer) | Spencer | 0.167 | 0.151 (+10.6%) | 0.155 (+7.7%) |

The governing authority is Loukidis's own same-method k꜀ where the paper publishes one: cases 1
and 2 in both methods, and case 3 in **Spencer**, whose Table 3 for that example lists Spencer's
method and publishes **no Bishop value at all**. (The RS2 manual's own §68 Case 3 table places
that value in a *Reference Bishop* column and leaves its *Reference Spencer* column blank, which
reverses the source.) So case 3's Bishop column has one authority, Slide2's, and its Spencer column
has the paper's. The largest governing difference on the row is the +9.0% Bishop leg, and it sets
the dot.

**Cross-bearings** — these are *context*, not governing pairings, and no dot rests on them:

| Case | Loukidis FEM | Loukidis log-spiral | Loukidis limit analysis UB / LB | RS2 SSRM |
|---|---|---|---|---|
| 1 (r<sub>u</sub> = 0.5) | 0.132 | 0.132 | 0.145 / 0.126 | 0.125 |
| 2 (dry) | 0.433 | 0.432 | 0.454 / 0.423 | 0.413 |
| 3 (3-layer) | 0.161 | — | 0.172 / 0.148 | 0.161 |

The homogeneous cases land squarely on the reference: Case 1 Spencer and Case 2 in both methods
match the Slide2 and reference LEM columns to a thousandth or two, and Case 1 Bishop sits exactly
on the reference Bishop — it is Slide2's own Bishop that is the low outlier there. Their critical
mechanism is a **deep, large-radius** arc, consistent with the published failure-surface figures.

**Case 3 runs high**, +9.0% against Slide2's Bishop and +7.7% against the paper's Spencer, and no
single cause accounts for the gap. The governing surface rides the thin φ = 15° band, and Slide2
reaches its Spencer k꜀ with a Monte-Carlo-optimized non-circular path, so surface shape is a
plausible part of the Spencer leg. It does not carry the Bishop leg: Bishop's method is circular
by construction and Slide2 reaches its own value with a circular surface, so XSLOPE's circular
search is finding a different circle rather than being unable to represent the mechanism. The
XSLOPE values do fall inside the reference bracket and beside RS2's own SSRM, but those are
cross-method readings and do not soften the same-method result.

**The inputs are not the difference.** Every input class was checked against the vendor model
`slope stability #068_03.fez` this row is built from: the three zone polygons reproduce its own
meshed material regions to within 0.004 m² of area on 10 288.75 m² of section, the strengths and
unit weights match its material records exactly, and there is no groundwater on either side. The
pseudo-static force matches too — the vendor writes a uniform body force b<sub>x</sub> = −k per
element, which is k·W acting through each element's centroid, the same line of action as XSLOPE's
seismic moment arm — and cases 1 and 2 exercise that arm on deep, large-radius surfaces and land
within 0.8%. The residual is a difference in the located LEM minimum, not in the model it is
located on.

#### The SSRM cross-check on Case 3 — measured, not locked {#rs2-68-ssrm}

Part IV states this problem the other way round from Part III: instead of searching for k꜀, it
fixes k at Loukidis's own coefficient and reports the factor of safety there.

| Published at k = 0.155 g | RS2 SSR | Slide2 (Spencer / GLE) | Loukidis Spencer |
|---|---|---|---|
| RS2 Part IV Table 68.2 | 0.99 | 0.994 | 1.000 |

That is a strength-reduction target XSLOPE can pair with like for like, on the same `rs2_68c`
file, with `k_seismic` = 0.155 g driving toward the face — the sign the vendor model writes as a
uniform body force b<sub>x</sub> = −k. But the factor never stops moving under mesh refinement. It
falls at every step of a target-size sweep from 4.0 m down to 1.5 m — a seven-fold increase in
element count, from 1 593 to 10 803 tri6 — and it is still falling on the finest mesh, crossing
RS2's own SSR on the way down.
There is no length scale for the series to converge to: the mechanism rides a thin φ = 15° band,
and unregularized Mohr-Coulomb fixes no thickness for that band, so each refinement resolves it
thinner and the slope weaker. Locking any mesh of that sweep would let the mesh choice decide the
row's dot, so no strength-reduction value on this problem is locked, and the SSRM route to a
critical seismic coefficient inherits the same drift. The vendor's tensile caps are carried in the
measurement.

**The search is not what separates them.** Held at the published coefficient, the shipped seed and
an automatic 300-circle grid-and-tangent sweep find the same surface, and the broader search finds
a *worse* one; neither reaches FS = 1 there, so the +9.0% is not a search that stopped early. The
circular-versus-non-circular reading is not available either: Bishop is circular by construction
and both Bishop authorities reach their value with circular surfaces. The residual is a difference
in the located minimum rather than in the line of action or the surface, and it is unexplained.
The locks on this row are **k꜀ locks, not factors of safety**, recorded as regression anchors at
the values XSLOPE's circular search returns.

<!-- test: file=files/rocscience/rs2_68a.xlsx, type=critical_kc, method=bishop, expected_kc=0.127, k_min=0.08, k_max=0.18, kc_tol=0.01, num_slices=40, benchmark=RS2-68a-bishop -->
<!-- test: file=files/rocscience/rs2_68a.xlsx, type=critical_kc, method=spencer, expected_kc=0.132, k_min=0.08, k_max=0.18, kc_tol=0.01, num_slices=40, benchmark=RS2-68a-spencer -->
<!-- test: file=files/rocscience/rs2_68b.xlsx, type=critical_kc, method=bishop, expected_kc=0.426, k_min=0.38, k_max=0.48, kc_tol=0.01, num_slices=40, benchmark=RS2-68b-bishop -->
<!-- test: file=files/rocscience/rs2_68b.xlsx, type=critical_kc, method=spencer, expected_kc=0.433, k_min=0.38, k_max=0.48, kc_tol=0.01, num_slices=40, benchmark=RS2-68b-spencer -->
<!-- test: file=files/rocscience/rs2_68c.xlsx, type=mesh_elements, element_type=tri6, target_size=4.0, expected_elements=1593, benchmark=RS2-68-mesh-coarse -->
<!-- test: file=files/rocscience/rs2_68c.xlsx, type=mesh_elements, element_type=tri6, target_size=1.5, expected_elements=10803, benchmark=RS2-68-mesh-fine -->
<!-- test: file=files/rocscience/rs2_68c.xlsx, type=critical_kc, method=bishop, expected_kc=0.169, k_min=0.11, k_max=0.20, kc_tol=0.01, num_slices=40, benchmark=RS2-68c-bishop -->
<!-- test: file=files/rocscience/rs2_68c.xlsx, type=critical_kc, method=spencer, expected_kc=0.167, k_min=0.11, k_max=0.20, kc_tol=0.01, num_slices=40, benchmark=RS2-68c-spencer -->

**Case 2 — dry homogeneous slope (rs2_68b)**

![RS2-68: seismically loaded slopes (Loukidis et al. 2003), Case 2 dry homogeneous — inputs with the pseudo-static arrow at k꜀ = 0.433 (left) and the Spencer critical seismic surface, a broad arc dipping below the toe, FS = 1.00 (right)](images/rs2_68b.png)

**Case 3 — three-layer, band-riding slope (rs2_68c)**

![RS2-68 Case 3 three-layer — inputs (left) and the Spencer critical surface at k꜀ = 0.167 riding the weak φ = 15° middle band, FS = 1.00 (right)](images/rs2_68c.png)

## Part IV SSRM builds on shared Slide2 geometry {#part-iv-ssrm}

RS2's Part IV catalog above re-verifies its Slide2 problems by shear-strength reduction. Where
a Part IV problem shares its geometry with a built Slide2/LEM lock, the same corpus file also
carries its **own** SSRM run against RS2's published SSRM, since an LEM lock does not stand in
for the SSRM comparison. These sections carry those SSRM builds on the shared files.

### RS2 Part IV VP2: Homogeneous slope with tension crack (ACADS 1b) {#p4-vp2}

Slide2/LEM counterpart: [VP2](rocscience.md#vp2) (Giam & Donald 1989, ACADS 1(b)). RS2 Part IV
re-runs this slope by shear-strength reduction (Table 2.2), so the shared file also carries a
real SSRM lock, not just the LEM cross-reference.

**Input files:** [vp002.xlsx](files/rocscience/vp002.xlsx)

A single-material slope: c' = 32 kPa, φ' = 10°, γ = 20 kN/m³. The LEM version
[VP2](rocscience.md#vp2) carries a water-filled tension crack (depth 2c/(γ√Ka), per Craig)
that trims the resisting soil. RS2's own SSRM does *not* leave the crack out, and it does not
model it by truncation either: its vendor `.fez` represents it physically, as a near-surface
material zone parallel to the ground surface carrying a **tensile-strength cutoff T = 0**,
over a deep substrate with T = 32 kPa. The file carries both, so each solver sees the crack
the way its own model states it — the LEM reads `tcrack_depth`, the FEM reads the zone. Both
caps are reduced along with c' and tan φ' through the strength reduction, matching the
vendor's `tensilestrength_SRF = 1`.

The zone's base is laid at the file's own crack depth, 3.814 m, against the vendor's 3.87 m; the
sliver band between the two lines is thinner than the slicer resolves, so one elevation serves
both solvers. A T = 0 crest zone opens in tension more readily than the body around it and pulls
the SRF down. ([RS2-29](#rs2-29)'s clay model reaches the same end by geometry instead, cutting
the crest away and replacing its weight with a surcharge.) ψ = 0; E and ν are the vendor model's
own elastics (E = 50 000 kPa, ν = 0.4), inert for the factor of safety.

| Method | XSLOPE | RS2 SSRM | Giam & Donald reference | Slide2 Spencer |
|---|---|---|---|---|
| SSRM (1 m mesh) | 1.644 | 1.63 (+0.9%) | 1.65 (−0.4%) | 1.592 |

The value is **mesh-converged**: 1.669 / 1.644 / 1.644 / 1.644 at 3 / 1.5 / 1.0 / 0.7 m target
sizes, flat from 1.5 m down — at 3 m the zone is about one element thick and the cutoff barely
engages. Locked at the 1.0 m mesh.

<!-- test: file=files/rocscience/vp002.xlsx, type=fem_ssrm, expected_fs=1.669, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP2-m3.0 -->
<!-- test: file=files/rocscience/vp002.xlsx, type=fem_ssrm, expected_fs=1.644, element_type=tri6, target_size=1.5, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP2-m1.5 -->
<!-- test: file=files/rocscience/vp002.xlsx, type=fem_ssrm, expected_fs=1.644, element_type=tri6, target_size=0.7, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP2-m0.7 -->
<!-- test: file=files/rocscience/vp002.xlsx, type=fem_ssrm, expected_fs=1.644, element_type=tri6, target_size=1.0, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP2 -->

![RS2 Part IV VP2: ACADS 1(b) homogeneous slope (Giam & Donald 1989), SSRM 1.644 with the vendor's T = 0 crack zone vs RS2 SSRM 1.63 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP2.png)

### RS2 Part IV VP6: Talbingo dam, specified upstream circle (ACADS 2b) {#p4-vp6}

Slide2/LEM counterpart: [VP6](rocscience.md#vp6) (ACADS 2(b), Giam & Donald 1989). This is the
**same four-zone Talbingo dam** as [RS2-4](#rs2-4) (ACADS 2(a)); the two problems differ only in
which mechanism is sought. RS2-4's **unconstrained** SSRM finds the true global minimum — the
steeper 30.9° downstream bench (**1.672**, a surface-parallel infinite-slope slide). ACADS 2(b)
instead asks for the factor on a **single specified upstream circle**, and RS2 obtains its
published SSRM of **2.15** by confining strength reduction to an **SSR Search Area** hugging that
upstream face.

**Input files:** [vp006.xlsx](files/rocscience/vp006.xlsx) — the same dam as
[vp005.xlsx](files/rocscience/vp005.xlsx), carrying the ACADS 2(b) specified circle.

The constraint polygon is **RS2's own**, a 37-vertex ring over the upstream face and core read
verbatim from `slope stability #006.fez`. `solve_ssrm`'s `ssr_zone` confines strength reduction to
elements inside it and holds the downstream shell and deep interior at full strength, redirecting
the mechanism off the downstream infinite-slope minimum and onto the upstream circle through the
cohesive core. The vendor `.fez` additionally makes its abutment and foundation blocks
linear-elastic, which `ssr_zone` approximates by holding those elements at full Mohr-Coulomb
strength — the same approximation stated for [RS2-61](#rs2-61)/[RS2-64](#rs2-64). ψ = 0.

| Method | XSLOPE | RS2 SSRM | Slide2 (specified upstream circle) | Giam & Donald reference |
|---|---|---|---|---|
| SSRM, unconstrained (→ [RS2-4](#rs2-4)) | 1.672 | — (downstream bench, true global min) | — | — |
| SSRM, SSR Search Area (upstream circle) | 2.188 | 2.15 (+1.8%) | Bishop 2.208 / Spencer 2.292 / GLE 2.301 | 2.29 (−4.5%) |

The upstream-face confinement lifts the factor from the unconstrained 1.672 on the downstream
bench to the upstream-circle 2.188, reproducing RS2's ACADS 2(b) answer, so the split between the
two is a **mechanism choice, not a discrepancy**. Locked at the RS2-4 mesh (6.5 m tri6); this
mechanism sits close enough to its critical factor that different valid numerical configurations
land a bisection step or two apart, and the lock records the configuration the package ships. The
2(a) problem's own constraint is different again — an SSR *Exclusion* Area over the downstream
shell rather than a search area over the upstream face — and [RS2-4](#rs2-4) locks that
configuration separately.

<!-- test: file=files/rocscience/vp006.xlsx, type=fem_ssrm, expected_fs=2.188, element_type=tri6, target_size=6.5, tolerance=0.02, f_min=1.8, f_max=2.5, max_iter=16000, ssr_zone=337.693;156.655;332.733;149.028;321.296;131.643;301.471;106.786;282.104;86.9617;253.282;65.612;218.97;44.5673;191.673;33.2825;160.106;24.1326;129.302;18.6427;106.884;16.5077;82.3323;16.5077;59.6101;20.1677;46.2384;23.742;43.4453;27.1826;26.5181;18.6427;29.4837;15.139;45.1228;9.79785;62.5076;7.05289;90.1096;5.22292;107.647;5.22292;124.269;5.22292;147.754;7.66288;167.883;10.8653;189.996;16.9652;206.923;22.7602;226.464;30.2593;250.08;42.5849;274.937;59.2071;299.184;79.9468;312.146;94.4341;328.442;115.178;340.663;132.406;348.593;150.686;350.477;154.416;339.88;160.039;337.693;156.655, tension_srf=true, k0=1, benchmark=RS2-P4-VP6 -->

![RS2 Part IV VP6: ACADS 2(b) Talbingo dam (Giam & Donald 1989), constrained SSRM 2.188 vs RS2 SSRM 2.15 — the mechanism confined to RS2's upstream SSR-Search-Area polygon read verbatim from the vendor model; FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP6.png)

### RS2 Part IV VP41: Homogeneous slope, power curve + r<sub>u</sub> (Jiang, Baker & Yamagami 2003) {#p4-vp41}

Slide2/LEM counterpart: [VP41](rocscience.md#vp41). RS2 Part IV (Table 41.2) re-runs this slope by
shear-strength reduction, exercising the FEM's **power-curve strength and r<sub>u</sub> pore pressure
together**.

**Input files:** [vp041.xlsx](files/rocscience/vp041.xlsx)

A homogeneous slope whose strength follows the power curve τ = 1.4·(σ')<sup>0.8</sup> (A = 1.4,
B = 0.8, γ = 20 kN/m³), with r<sub>u</sub> = 0.3. The non-linear envelope is locked separately on RS2-30/31/32/34 and the r<sub>u</sub> option on
RS2-14/17b/18b; this problem exercises the two together.

| Method | XSLOPE | RS2 SSRM | Slide2 | Charles & Soares | Baker | Perry | XSLOPE LEM |
|---|---|---|---|---|---|---|---|
| SSRM (1.5 m mesh) | 1.656 | 1.64 (+1.0%) | Spencer 1.666 / GLE 1.653 | Bishop 1.66 | Janbu 1.60 | rigorous Janbu 1.67 | Bishop 1.668 / Spencer 1.670 |

XSLOPE's SSRM lands at **1.656**, +1.0% above RS2's SSRM 1.64 and inside the published LEM cluster.
It is mesh-stable between the 2.5 m and 1.5 m target sizes. Locked at the 1.5 m mesh. ψ = 0; E and
ν are the file's inert elastics (E = 8 000 kPa, ν = 0.45, assigned by soil type — the vendor
model publishes none for a power-curve material).

<!-- test: file=files/rocscience/vp041.xlsx, type=fem_ssrm, expected_fs=1.656, element_type=tri6, target_size=1.5, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, k0=1, benchmark=RS2-P4-VP41 -->

![RS2 Part IV VP41: Jiang/Baker power-curve slope with r<sub>u</sub> = 0.3, SSRM 1.656 vs RS2 SSRM 1.64 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP41.png)

### RS2 Part IV VP57: Layered slope with weak seam, water table (Pockoski & Duncan slope 3) {#p4-vp57}

Slide2/LEM counterpart: [VP57](rocscience.md#vp57). RS2 Part IV (Table 57.2) re-runs this layered
slope by shear-strength reduction.

**Input files:** [vp057.xlsx](files/rocscience/vp057.xlsx)

Sandy clay (c = 300 psf, φ = 35°, γ = 130 pcf) over a highly plastic clay seam (c = 0, φ = 25°), with
a water table and a dry tension crack. The critical mechanism rides the weak c = 0 seam. The FEM
elastic constants are the vendor model's own, E = 1×10⁶ psf and ν = 0.4 on every material.

The tension crack is stated twice, once for each solver. The LEM reads `tcrack_depth` and truncates
the surface; the FEM reads the **crack zone** the vendor model carries in its place — a twin of the
sandy clay with a **tensile-strength cutoff T = 0**, filling the wedge between the ground surface and
the crack line (0, 100)–(125, 144)–(200, 144), 6 ft deep under the crest and tapering to nothing at
the base of the slope. Both are transcribed, so each solver sees the crack the way its own model
states it.

| Method | XSLOPE | RS2 SSRM | Slide2 Spencer | SLOPE/W | XSTABL | XSLOPE LEM |
|---|---|---|---|---|---|---|
| SSRM (3.0 m mesh) | 1.323 | 1.32 (+0.2%) | 1.40 composite / 1.42 not-composite | 1.40 | 1.41 | Bishop/Spencer 1.389 / 1.396 composite |

XSLOPE's SSRM lands at **1.323**, +0.2% on RS2's own SSRM 1.32 — the reduction rides the weak c = 0
seam, the same mechanism by which RS2's SSRM itself sits below the composite LEM cluster (~1.40).
Unlike [VP2](#p4-vp2), the crest cutoff itself does nothing here: the mechanism is a deep slide
along the c = 0 seam and never opens the crest in tension. The zone is carried for fidelity to the
vendor model rather than because it moves the answer. Locked at 3.0 m. ψ = 0.

<!-- test: file=files/rocscience/vp057.xlsx, type=fem_ssrm, expected_fs=1.323, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.0, f_max=1.7, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP57 -->

![RS2 Part IV VP57: layered slope with weak seam (P&D slope 3), SSRM 1.323 vs RS2 SSRM 1.32 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP57.png)

### RS2 Part IV VP60: Soil-nailed wall (Pockoski & Duncan slope 7) {#p4-vp60}

Slide2/LEM counterpart: [VP60](rocscience.md#vp60). RS2 Part IV re-runs this nailed wall by
shear-strength reduction.

**Input files:** [vp060.xlsx](files/rocscience/vp060.xlsx)

A near-vertical wall in undrained sandy clay (c = 800 psf, φ = 0, γ = 120 pcf) retained by five
passive soil-nail rows (15° declination, heads on the wall face at El. 23 / 18 / 13 / 8 / 3),
with a dry 7-ft tension crack and overlapping crest surcharges (250 psf full-width + 500 psf over
the first 7.3 ft). The nails carry an FEM axial rigidity (EA ≈ 2000·T_max, the grouted-nail
convention); the soil elastic constants are the vendor model's own, E = 1×10⁶ psf and ν = 0.4.

| Method | XSLOPE | RS2 SSRM | Slide2 | UTEXAS4 | GOLD-NAIL |
|---|---|---|---|---|---|
| SSRM (2.0 ft mesh) | 1.009 | 0.98 (+3.0%) | Spencer 1.009 / Janbu 1.041 | 1.02 / 1.08 | 0.91 |

*The Slide2 values are on Slide's printed circle; the published spread is 0.91–1.02.*

The inclined nails root **on the vertical wall face**, so the soil surface is split along each nail
line (an OCC boolean-fragment build) and the nail nodes are shared with the 2D mesh by
construction; embedded and edge-recovered, such wall-rooted lines stay non-conforming. With the
nails conforming, XSLOPE's SSRM lands at **1.009**, squarely inside the published 0.91–1.02 spread.
For undrained φ = 0 clay the nail bond is adhesion-governed, so the fixed-ramp pull-out is
faithful, and the conforming mesh equilibrates at a uniform size without feature refinement. ψ = 0.

**The vendor model holds a third of the domain elastic, and this run does not.**
`#060-slope7` states its strength-reduction constraint as a linear-elastic twin rather than a
polygon: a duplicate of the firm-soil foundation carrying *"Plasticity Specifications: None"*
over 33.9% of the domain by area, which cannot yield at any strength-reduction factor. RS2's
published 0.98 was produced with it; the corpus run above is unconstrained. The two agree to
+3.0% anyway, but the comparison is not constrained-against-constrained the way
[P4-VP67](#p4-vp67) and [P4-VP69](#p4-vp69) are, and the partition is the reason this row's
agreement carries a caveat.

**The vendor's tension zone is recorded rather than carried.** Slide's tension crack for this
problem is an inclined line, and `#060-slope7.fez` states it as geometry: a twin of the sandy clay
with a **tensile-strength cutoff T = 0** filling everything above a boundary that leaves the wall
face at el 22.5 and runs 40 ft down at the nails' own 15° declination before running flat to the
right edge. That zone is 23% of the domain and covers the whole upper retained mass, and
transcribing it as a second material drops the factor well below RS2's own SSR. RS2 publishes 0.98
*with* the zone in place, so what separates the two is the treatment of a zero tensile cutoff on a
φ = 0 clay rather than the geometry. The zone is therefore recorded here rather than carried, and
the crack stays stated the LEM way, through `tcrack_depth`.

<!-- test: file=files/rocscience/vp060.xlsx, type=fem_ssrm, expected_fs=1.009, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=0.7, f_max=1.3, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP60 -->

![RS2 Part IV VP60: soil-nailed wall (P&D slope 7), SSRM 1.009 vs RS2 SSRM 0.98 — FEM inputs, mesh with the wall-rooted nails conforming into the 2D mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP60.png)

### RS2 Part IV VP64: USACE end-of-construction dam (Fig 4-1) {#p4-vp64}

Slide2/LEM counterpart: [VP64](rocscience.md#vp64) (USACE EM 1110-2-1902 Fig 4-1). RS2 Part IV
publishes an SSRM of **2.37** (Table 64.2; Slide2 Spencer 2.445).

**Input files:** [vp064.xlsx](files/rocscience/vp064.xlsx)

The dam is a symmetric 50-ft embankment (c = 1000 psf, φ = 5°) over a 10-ft sand blanket
(c = 0, φ = 35°), foundation clay (c = 3000, φ = 0°) and rock, with an embankment core trench
cutting through the sand to the clay.

| Method | XSLOPE | RS2 SSRM | Slide2 Spencer | USACE Spencer | XSLOPE LEM Spencer |
|---|---|---|---|---|---|
| SSRM (6 ft mesh) | 2.394 | 2.37 (+1.0%) | 2.445 | 2.44 | 2.488 |

The core trench pinches the sand blanket to zero thickness, splitting it into an upstream and a
downstream wedge, so the blanket is laid as two explicit polygons rather than as a stacked profile
line: polygon extraction from a stacked profile keeps only the upstream wedge and leaves a ~10-ft
void under the downstream shell that collapses under gravity at any strength. With the domain
tiling as a closed continuum the SSRM converges to **2.394**, +1.0% on RS2's SSRM 2.37. The
geometry follows USACE's 4H:1V Fig 4-1 and the source's moist/saturated unit weights, not the
steeper single-bulk Slide2-Import conversion of the same problem.

**The vendor zone here is a mechanism-selection corridor, and it is documented rather than
carried.** `#064.fez` holds a 65-vertex SSR *search area* that is not a region but a ~6 ft ribbon
traced along Slide2's Spencer critical circle, from the crest down to the downstream toe — 96.2% of
the domain is outside it and held at full strength. It is RS2's way of reproducing a specified
Slide2 slip surface by strength reduction, the idiom the manual states in prose on VP6, VP19 and
VP25. Because the ring is drawn *around* the mechanism, the constrained and unconstrained answers
coincide by construction, which is why the unconstrained lock reproduces the constrained published
value. The corridor is not transcribed because it is thinner than the corpus mesh: at
target_size = 6.0 ft it is about one element across, so as an `ssr_zone` it rasterizes to a ragged
one-element chain that cannot form a mechanism at all. Carrying it would require refining to four
or more elements across the band, so the corridor is recorded here and the unconstrained lock
stands.

**So is the crest tension zone.** `#064.fez` fills the crest block — x ±16, el 43–50 against its own
crest — with a twin of the embankment carrying a **tensile-strength cutoff T = 0**, which is how RS2
imports Slide's 7-ft crest crack. This file states the same 7 ft of crack through `tcrack_depth`
instead, so the crack is carried as geometry rather than as a second material.

<!-- test: file=files/rocscience/vp064.xlsx, type=fem_ssrm, expected_fs=2.394, element_type=tri6, target_size=6.0, tolerance=0.02, f_min=2.0, f_max=2.8, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP64 -->

![RS2 Part IV VP64: USACE Fig 4-1 end-of-construction dam, SSRM 2.394 vs RS2 SSRM 2.37 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP64.png)

### RS2 Part IV VP65 / VP66: USACE upstream-pool dams (Fig 4-2, Fig 4-3) {#p4-vp65}

<a id="p4-vp66"></a>

Slide2/LEM counterparts: [VP65](rocscience.md#vp65) and [VP66](rocscience.md#vp66). Two dams of one
family — the [VP64](#p4-vp64) embankment under a pool at el. 20 — so they are treated together. Own
SSRM builds on the shared Slide2 files.

**Input files:** [vp065.xlsx](files/rocscience/vp065.xlsx) · [vp066.xlsx](files/rocscience/vp066.xlsx)

| Case | XSLOPE SSRM | RS2 SSR | USACE |
|---|---|---|---|
| VP66 (Fig 4-3), ponded both faces | **2.172** | 2.22 (−2.2%) | 2.30 |
| VP65 (Fig 4-2), ponded upstream only | *reported, not locked* | 2.60 | 2.71 |

**The two dams are watered differently, and the source says so twice each.** VP66 stands in water on
both faces: Figure 66.1 draws the inverted-triangle water symbol and the ponded-water hatch upstream
and downstream alike, and its piezometric line runs the full width of the section at el. 20. RS2's
Slide2-import model `#066` states the same pair — a piezometric line spanning the full width at
el. 20, and water tractions in *two* groups, the second beginning exactly where el. 20 meets the
downstream face. VP65 stands in water on the upstream face only: Figure 65.1 hatches ponded water
upstream and nowhere else, and `#065` states that pair too — a piezometric line stopping short of
the downstream face, water tractions on the upstream face alone, and a solved nodal pore-pressure
field that is hydrostatic to el. 20 under the line and **exactly zero beyond it, at every
elevation**. Each corpus file carries its own model's pair, and beyond a piezometric line's own
extent XSLOPE assigns no pore pressure in the FEM, as in the LEM. The two have to be declared
together: where standing water is present its weight is part of the total stress the pore pressure
is subtracted from — under a pond σ′ = γ′z, positive at every depth — so a piezometric surface is a
sound full-field pore pressure for a finite element model exactly when the pond that sustains it is
carried as a load. Neither problem's published slip circle reaches the
downstream face, so the limit-equilibrium factors on [VP65](rocscience.md#vp65) and
[VP66](rocscience.md#vp66) are the same under either treatment.

**VP66 locks; VP65 is reported against a constrained vendor factor.** With the downstream pond its
model carries, VP66's SSRM is **2.172** against RS2's SSR 2.22, inside the band the corpus locks
within. VP65 equilibrates under gravity and brackets a complete strength reduction well below
RS2's 2.60. The water is not what separates them: VP65's own model states its truncated
piezometric line and its upstream-only pond together, and the file carries both.

What separates them is which mechanism each factor describes. XSLOPE's SSRM here is
**unconstrained**, and it fails the *upstream* slope, shear concentrating in the base of the
upstream embankment just above the published circle, which bottoms at el. −10 under the crest.
RS2's 2.60 is obtained inside the SSR corridor described below, traced along that same published
circle. An unconstrained factor against a zone-constrained one is not a pairing, so the row is
reported rather than locked.

Both vendor models carry that corridor, a mechanism-selection ribbon of the [VP64](#p4-vp64) kind —
6.6 ft wide on VP65 and 9.2 ft on VP66, each traced along the problem's published upstream circle.
Neither is transcribed. Both are thinner than the corpus mesh, and `#065` draws its corridor on a
section of its own — crest el. 45, toes at ±200, against the el. 50 / ±217 section Figure 65.1
labels — so it does not land on the corpus geometry at all. The factors above are therefore
unconstrained runs: on VP66 that still lands within 2.2% of the vendor's constrained value, and on
VP65 it does not.

<!-- test: file=files/rocscience/vp066.xlsx, type=fem_ssrm, expected_fs=2.172, element_type=tri6, target_size=6.0, tolerance=0.02, f_min=1.7, f_max=3.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP66 -->

![RS2 Part IV VP66: USACE Fig 4-3 dam ponded on both faces, SSRM 2.172 vs RS2 SSRM 2.22 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP66.png)

![RS2 Part IV VP65: USACE Fig 4-2 dam ponded on the upstream face only, the unconstrained strength reduction failing the upstream slope where RS2's zone-constrained SSRM 2.60 describes the published circle — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP65.png)

### RS2 Part IV VP69: USACE steady-seepage embankment (example F-6) {#p4-vp69}

Slide2/LEM counterpart: [VP69](rocscience.md#vp69) (USACE EM 1110-2-1902 example F-6). Own SSRM
build, with two answers: the model's own global minimum and the vendor's constrained one.

**Input files:** [vp069.xlsx](files/rocscience/vp069.xlsx)

A 112 ft embankment (c′ = 0, φ′ = 34°, γ = 130 pcf) on a granular foundation (c′ = 0, φ′ = 35°,
γ = 125 pcf) under steady seepage, with the pool at el. 100 and the tailwater ponding the toe at
el. 22.5. E and ν are the vendor model's own, E = 1×10⁶ psf and ν = 0.4 on both materials, and
both carry its tensile cap T = 0 — inert on a c = 0 material, whose Mohr-Coulomb apex is already
at zero.

| Case | XSLOPE SSRM | RS2 SSR | USACE | Slide2 Spencer |
|---|---|---|---|---|
| SSRM, under RS2's own SSR Search Area (5 ft mesh) | **1.944** | 1.94 (+0.2%) | 2.01 | 2.026 |

**Where RS2's constraint is.** `slope stability #069.fez` states it twice: an
`SSR_polygonal_zones` ring flagged as a Search Area, 38 vertices running from the crest down
through the foundation to the toe and back, and a material partition that leaves only 1 030 of its
9 626 elements Mohr-Coulomb over that same corridor. Both mean *reduce strength only along the deep
surface*, and the tag carries the polygon verbatim.

The corridor is a band rather than a region, so it has to be checked against the mesh before it
can be carried, and it rasterizes faithfully: across the 8 / 6.5 / 5 / 4 ft sweep the elements
whose centroids fall inside it are 10.4 to 10.7% of the mesh against the vendor's own 10.7%
Mohr-Coulomb element fraction, and the polygon's area is within 1.8% of the vendor's footprint.
This is not the one-element-ribbon case that [VP64](#p4-vp64) and [RS2-37](#rs2-37) record but do
not carry.

**The constrained factor is mesh-sensitive.** Across that same sweep it reads 2.019 / 1.969 /
1.944 / 1.931, and since the mask is faithful at every one of those meshes the drift is the c = 0
band continuing to localize, the behavior [RS2-14](#rs2-14) and [RS2-40](#rs2-40) document. The tag
pins the 5 ft mesh, the coarsest at which the band spans two elements across its thinnest section,
as a regression lock rather than a converged value.

**Unconstrained, and why a depth filter is the wrong instrument here.** Both zones are c = 0, so
with every element reduced the mechanism is a shallow cohesionless face skin, the pattern
[RS2-40](#rs2-40) documents. The `min_slip_depth` filter lifts the factor here too but does not
settle on one — this 112 ft embankment has no cutoff plateau of the kind RS2-40's 211 ft dam has —
and a depth-filtered *unconstrained* run is in any case not the experiment RS2 ran. Where the
vendor model states the constraint outright, carrying it is the closer reproduction.

<!-- test: file=files/rocscience/vp069.xlsx, type=fem_ssrm, expected_fs=2.019, element_type=tri6, target_size=8.0, tolerance=0.02, f_min=1.6, f_max=2.4, max_iter=16000, tension_srf=true, k0=1, ssr_zone=33.597;107.325;24.959;104.224;24.959;99.5;29.831;86.063;54.416;49.74;70.805;30.25;117.538;-4.523;144.115;-21.134;189.962;-35.53;242.817;-43.261;274.99;-43.261;309.124;-35.806;331.749;-30.967;357.775;-22.859;378.551;-15.274;395.712;-7.552;408.011;0.18;408.011;3.031;397.188;4.415;394.659;1.915;378.932;-6.122;363.678;-11.366;342.512;-18.23;324.016;-22.997;289.408;-27.383;261.664;-28.622;242.89;-27.381;222.062;-24.152;195;-16.402;165.067;-7.522;139.718;6.525;121.957;15.244;104.035;28.322;89.666;40.593;71.905;57.385;56.889;71.916;44.296;89.677;36.646;102.583, benchmark=RS2-P4-VP69-m8 -->
<!-- test: file=files/rocscience/vp069.xlsx, type=fem_ssrm, expected_fs=1.969, element_type=tri6, target_size=6.5, tolerance=0.02, f_min=1.6, f_max=2.4, max_iter=16000, tension_srf=true, k0=1, ssr_zone=33.597;107.325;24.959;104.224;24.959;99.5;29.831;86.063;54.416;49.74;70.805;30.25;117.538;-4.523;144.115;-21.134;189.962;-35.53;242.817;-43.261;274.99;-43.261;309.124;-35.806;331.749;-30.967;357.775;-22.859;378.551;-15.274;395.712;-7.552;408.011;0.18;408.011;3.031;397.188;4.415;394.659;1.915;378.932;-6.122;363.678;-11.366;342.512;-18.23;324.016;-22.997;289.408;-27.383;261.664;-28.622;242.89;-27.381;222.062;-24.152;195;-16.402;165.067;-7.522;139.718;6.525;121.957;15.244;104.035;28.322;89.666;40.593;71.905;57.385;56.889;71.916;44.296;89.677;36.646;102.583, benchmark=RS2-P4-VP69-m6.5 -->
<!-- test: file=files/rocscience/vp069.xlsx, type=fem_ssrm, expected_fs=1.931, element_type=tri6, target_size=4.0, tolerance=0.02, f_min=1.6, f_max=2.4, max_iter=16000, tension_srf=true, k0=1, ssr_zone=33.597;107.325;24.959;104.224;24.959;99.5;29.831;86.063;54.416;49.74;70.805;30.25;117.538;-4.523;144.115;-21.134;189.962;-35.53;242.817;-43.261;274.99;-43.261;309.124;-35.806;331.749;-30.967;357.775;-22.859;378.551;-15.274;395.712;-7.552;408.011;0.18;408.011;3.031;397.188;4.415;394.659;1.915;378.932;-6.122;363.678;-11.366;342.512;-18.23;324.016;-22.997;289.408;-27.383;261.664;-28.622;242.89;-27.381;222.062;-24.152;195;-16.402;165.067;-7.522;139.718;6.525;121.957;15.244;104.035;28.322;89.666;40.593;71.905;57.385;56.889;71.916;44.296;89.677;36.646;102.583, benchmark=RS2-P4-VP69-m4 -->
<!-- test: file=files/rocscience/vp069.xlsx, type=fem_ssrm, expected_fs=1.944, element_type=tri6, target_size=5.0, tolerance=0.02, f_min=1.6, f_max=2.4, max_iter=16000, tension_srf=true, k0=1, ssr_zone=33.597;107.325;24.959;104.224;24.959;99.5;29.831;86.063;54.416;49.74;70.805;30.25;117.538;-4.523;144.115;-21.134;189.962;-35.53;242.817;-43.261;274.99;-43.261;309.124;-35.806;331.749;-30.967;357.775;-22.859;378.551;-15.274;395.712;-7.552;408.011;0.18;408.011;3.031;397.188;4.415;394.659;1.915;378.932;-6.122;363.678;-11.366;342.512;-18.23;324.016;-22.997;289.408;-27.383;261.664;-28.622;242.89;-27.381;222.062;-24.152;195;-16.402;165.067;-7.522;139.718;6.525;121.957;15.244;104.035;28.322;89.666;40.593;71.905;57.385;56.889;71.916;44.296;89.677;36.646;102.583, benchmark=RS2-P4-VP69 -->

![RS2 Part IV VP69: USACE F-6 steady-seepage embankment under RS2's own 38-vertex SSR Search Area, SSRM 1.944 vs RS2 SSR 1.94 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP69.png)

### RS2 Part IV VP67: USACE end-of-construction embankment (example F-5) {#p4-vp67}

Slide2/LEM counterpart: [VP67](rocscience.md#vp67) (USACE EM 1110-2-1902 example F-5). This
problem has two distinct answers, and both are reproduced: the **unconstrained** critical SRF
(a deep foundation mechanism) and the **toe-circle** SRF that RS2 forces with an SSR Exclusion
Area to obtain its published SSRM of **1.33**.

**Input files:** [vp067.xlsx](files/rocscience/vp067.xlsx) (unconstrained) ·
[vp067c.xlsx](files/rocscience/vp067c.xlsx) (SSR exclusion below El. 81)

A 91-ft embankment (c = 1780 psf, φ = 5°, γ = 135 pcf) on a 100-ft soft, undrained foundation
(c = 1600 psf, φ = 2°, γ = 127 pcf) over a rigid base, at end of construction. ψ = 0; E and ν are
the vendor model's own, E = 1×10⁶ psf and ν = 0.4 on all three materials.

| Method | XSLOPE | RS2 SSRM | Slide2 Spencer | USACE |
|---|---|---|---|---|
| SSRM, unconstrained (8 ft mesh) | 1.076 | — (true global minimum) | — | — |
| SSRM, SSR exclusion below El. 81 (8 ft mesh) | 1.303 | 1.33 (−2.0%) | 1.328 | 1.33 |

*The Slide2 and USACE columns on the constrained row are on the specified toe circle.*

**Unconstrained minimum (1.076).** With every zone reduced, the SSRM finds a deep translational
mechanism riding the foundation/bedrock contact through the soft φ = 2° clay — daylighting near
the upstream toe, sliding along the base, and rising through the downstream face. It is
bedrock-contact-pinned and essentially mesh-independent between the 8 and 4 ft target sizes, and
XSLOPE's own unconstrained LEM circular search finds the same deep family, so the two solvers
agree on the true global minimum. This is the mechanism a single USACE specified circle — centered
259 ft above the toe (R = 278), bottoming only ~19 ft into the foundation — does not probe.

**Toe-circle SRF (1.303) vs RS2's 1.33.** RS2's published 1.33 is likewise not the unconstrained
minimum: it is obtained by barring strength reduction in the foundation below the lowest point of
the specified circle (≈ El. 81), an **SSR Exclusion Area** that forces the mechanism up onto the
toe circle. Reproducing that constraint — vp067c splits the foundation at El. 81 into identical
upper and lower zones and excludes the lower one — XSLOPE's SSRM gives **1.303**, and the critical
shear band moves up into the embankment and shallow foundation, the toe-circle family.

<!-- test: file=files/rocscience/vp067.xlsx, type=fem_ssrm, expected_fs=1.076, element_type=tri6, target_size=8.0, tolerance=0.02, f_min=0.9, f_max=1.8, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP67 -->
<!-- test: file=files/rocscience/vp067c.xlsx, type=fem_ssrm, expected_fs=1.303, element_type=tri6, target_size=8.0, tolerance=0.02, f_min=1.2, f_max=1.5, max_iter=16000, ssr_exclude=Foundation lower, tension_srf=true, k0=1, benchmark=RS2-P4-VP67c -->

**Unconstrained critical SRF (vp067)**

![RS2 Part IV VP67: USACE F-5 embankment on soft foundation (end of construction), unconstrained SSRM 1.076 riding the foundation/bedrock contact vs the specified-circle SSRM 1.33 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP67.png)

**SSR Exclusion Area below El. 81 (vp067c)**

![RS2 Part IV VP67c: the same embankment with an SSR Exclusion Area below El. 81, SSRM 1.303 on the toe-circle family matching RS2's constrained SSRM 1.33 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP67c.png)

### RS2 Part IV VP68: Undrained φ = 0 three-layer slope, ponded (USACE E-10) {#p4-vp68}

Slide2/LEM counterpart: [VP68](rocscience.md#vp68) (USACE EM 1110-2-1902 example E-10). RS2 Part IV
(Table 68.2) re-runs this undrained slope by shear-strength reduction. Built, with two locked
answers — the model's own global minimum and the vendor's constrained one.

**Input files:** [vp068.xlsx](files/rocscience/vp068.xlsx)

An undrained three-layer slope (c = 600 / 400 / 500 psf, all φ = 0, γ = 120 / 100 / 105 pcf) with 8 ft
of water ponded against it (pool el 0). φ = 0 so strength reduction acts on cohesion alone; the
elastic constants are the vendor model's own, E = 1×10⁶ psf and ν = 0.4 on all three layers, as are
the tensile caps (600 / 400 / 500 psf, reduced with the SRF). This is a **total-stress** problem:
every layer is undrained, so the pool acts as a load and nothing else, and the file carries no
piezometric line — matching the vendor model, whose solved nodal pore pressure is zero everywhere.
ψ = 0.

| Case | XSLOPE SSRM (2.0 ft mesh) | RS2 SSRM | Slide2 | USACE E-10 chart |
|---|---|---|---|---|
| Unconstrained (global minimum) | 1.016 | — | — | — |
| RS2's SSR Search Area | 1.203 | **1.17** (+2.8%) | Bishop 1.241 / GLE 1.244 | 1.33 (−9.5%) |

*The Slide2 and USACE columns on the constrained row are both on the specified circle.*

**Every published number for this problem is an answer about one specified circle.** RS2's 1.17,
Slide2's 1.241 and USACE's 1.33 all describe the toe circle centered at (48.4, 28) with R = 48,
tangent to the base, and RS2's strength reduction is *constrained* to it: `#068.fez` writes a
30-vertex **SSR Search Area** whose first 23 vertices trace that circle and
whose remaining seven close the ring along the base and up both edges, so the region enclosed is
the material *below* the circle, 30% of the domain, and reduction never touches the mass above it.
Carried verbatim onto the tag as an `ssr_zone`, it moves XSLOPE from 1.016 to **1.203** and moves
the mechanism onto the base-tangent surface RS2's figure draws.

**Unconstrained, the slope has a weaker mechanism, and two independent methods find it.** With no
search area the reduction localizes a band along the base of the *weakest* layer, emerging at the
toe — not a surficial skin, since φ = 0 everywhere leaves no cohesionless face to slide — and a
free grid-seeded circular search lands on the same feature independently, its critical Bishop
circle tangent to the Soil 2 / Soil 3 contact at el −8.0. So the unconstrained minimum is real and
sits well below the specified circle; it is locked as the model's own global minimum, alongside the
constrained row that answers RS2's question.

**Mesh.** The unconstrained branch drifts down with refinement, 1.016 → 0.997 between the tagged
2.0 ft mesh (1 499 tri6) and a 1.2 ft mesh (4 132 tri6), and the constrained branch does not
survive that refinement at all: the search area's held-at-full-strength surroundings leave the
confined mechanism with no equilibrium at any strength-reduction factor, the sub-unity limit of the
`ssr_zone` approximation described on [RS2-64](#rs2-64). The constrained row is therefore locked at
the tagged mesh. The rest of the model matches the vendor `.fea` field by field: geometry to the
vertex, the three strengths, the unit weights recovered from its solid properties, the elastic
pair, the caps, the tension-SRF flag, and the three ponded-water load segments.

<!-- test: file=files/rocscience/vp068.xlsx, type=mesh_elements, element_type=tri6, target_size=2.0, expected_elements=1499, benchmark=RS2-P4-VP68-mesh -->
<!-- test: file=files/rocscience/vp068.xlsx, type=mesh_elements, element_type=tri6, target_size=1.2, expected_elements=4132, benchmark=RS2-P4-VP68-mesh-fine -->
<!-- test: file=files/rocscience/vp068.xlsx, type=fem_ssrm, expected_fs=0.997, element_type=tri6, target_size=1.2, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP68-m1.2 -->
<!-- test: file=files/rocscience/vp068.xlsx, type=fem_ssrm, expected_fs=1.016, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP68 -->
<!-- test: file=files/rocscience/vp068.xlsx, type=fem_ssrm, expected_fs=1.203, element_type=tri6, target_size=2.0, tolerance=0.02, f_min=0.8, f_max=1.4, max_iter=16000, tension_srf=true, ssr_zone=92.8636;16;92.1089;13.5678;89.5431;7.89038;87.3049;3.11374;85.0122;-0.270854;82.4464;-3.19143;79.635;-6.76709;76.8782;-9.03258;71.9651;-12.2534;67.6798;-14.6281;60.8833;-16.839;56.5707;-17.6578;52.0124;-18.504;48.7097;-18.8588;45.9256;-18.8588;41.804;-18.4221;37.9281;-17.6851;34.8438;-16.839;30.4766;-15.3377;26.7917;-13.5909;22.3426;-10.9978;19.7496;-9.27823;18.1938;-8;18.1938;-7.12192;16.365;-7.12192;16.365;-20;95.5679;-20;96.3634;16;96.4959;18.5104;93.1817;18.1127, k0=1, benchmark=RS2-P4-VP68-zone -->

**Unconstrained — the model's own global minimum (vp068)**

![RS2 Part IV VP68: undrained φ = 0 three-layer slope with ponded water (USACE E-10), unconstrained SSRM 1.016 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the band running along the base of the weakest layer and emerging at the toe](images/RS2-P4-VP68.png)

**RS2's own SSR Search Area — the specified circle (vp068)**

![RS2 Part IV VP68 with reduction confined to the vendor's 30-vertex SSR Search Area, SSRM 1.203 against RS2 SSRM 1.17 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the mechanism moved down onto the base-tangent circle the search area draws](images/RS2-P4-VP68-zone.png)

### RS2 Part IV VP70: Submerged homogeneous slope (Duncan & Wright Fig 6.27) {#p4-vp70}

Slide2/LEM counterpart: [VP70](rocscience.md#vp70). RS2 Part IV (Table 70.2/70.3) re-runs this
submerged slope by shear-strength reduction. The point of the problem is that the factor of safety is
independent of pool depth (30 ft vs 60 ft above the crest); RS2 reports SSRM 1.58 for both. This build
also covers **RS2 Part II §35** ("Submerged slope"), which is the identical Duncan & Wright Fig 6.27
model (native `.fez` #035: c′ = 100 psf, φ = 20°, γ = 128 pcf), which RS2 publishes separately, so
the two RS2 manuals bracket XSLOPE's value around the D&W referee — both columns are in the table
below.

**Input files:** [vp070a.xlsx](files/rocscience/vp070a.xlsx) (pool 30 ft above crest)

A homogeneous slope (c = 100 psf, φ = 20°, γ = 128 pcf) fully submerged under a pool 30 ft above the
crest, with the pond pressure applied over the whole submerged surface and pore pressures from the
piezometric line. The FEM elastic constants are the vendor model's own, E = 1×10⁶ psf and ν = 0.4.

| Method | XSLOPE | RS2 SSRM (Part IV VP70) | RS2 SSRM (Part II §35, native) | D&W referee | Slide2 | XSLOPE LEM |
|---|---|---|---|---|---|---|
| SSRM (3.0 m mesh) | 1.594 | 1.58 (+0.9%) | 1.64 (−2.8%) | 1.60 (−0.4%) | Bishop 1.603 / Spencer 1.599 | Bishop 1.596 / Spencer 1.593 |

*The XSLOPE LEM values are identical at both pool depths.*

The pond-load and pore-pressure treatments balance over the submerged surface, the same
consistency check the [VP70](rocscience.md#vp70) LEM lock makes. Mesh-stable, and locked at the
3.0 m mesh. ψ = 0.

<!-- test: file=files/rocscience/vp070a.xlsx, type=fem_ssrm, expected_fs=1.594, element_type=tri6, target_size=3.0, tolerance=0.02, f_min=1.2, f_max=2.0, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP70 -->

![RS2 Part IV VP70: submerged slope (D&W Fig 6.27), SSRM 1.594 vs RS2 SSRM 1.58 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP70.png)

### RS2 Part IV VP102: Homogeneous earth dam, dry (Huang & Jia 2008) {#p4-vp102}

Slide2/LEM counterpart: [VP102](rocscience.md#vp102). RS2 Part IV reports an SSRM for the dry dam
(Table 102.2) and for the *transient* rapid-drawdown series — Table 102.3 for φ<sup>b</sup> = 0° and
Table 102.4 for φ<sup>b</sup> = 37° — at 60–1500 h. XSLOPE reproduces all three from its own uncoupled
transient seepage solve (the same flow solve that feeds the Slide2-LEM curve in
[VP102](rocscience.md#vp102)).

**Input files:** [vp102a.xlsx](files/rocscience/vp102a.xlsx) (dry) ·
[vp102t_60](files/rocscience/vp102t_60.xlsx) / [100](files/rocscience/vp102t_100.xlsx) / [300](files/rocscience/vp102t_300.xlsx) / [600](files/rocscience/vp102t_600.xlsx) / [1500.xlsx](files/rocscience/vp102t_1500.xlsx) (drawdown snapshots)

A homogeneous earth dam (c' = 13.8 kPa, φ' = 37°, γ = 18.2 kN/m³). The elastic pair comes from the
shipped `.fez`, E = 50 000 kPa and ν = 0.4, where both manuals *print* E = 1×10⁵ kPa and ν = 0.3 —
one of the places where the vendor's printed table and its own model disagree, and one that a
strength-reduction factor is insensitive to. ψ = 0 throughout.

**The vendor's SSR Search Area is carried in the files.** Every published VP102 SSR value — the
dry factor and both drawdown columns — was produced with a constraint: each vendor `.fez` writes an
`SSR_polygonal_zones` block holding a five-vertex *search area*, an axis-aligned rectangle over the
**downstream half** of the section from the crest's downstream break outward, spanning the full
height. Reduction applies only inside it, so 47% of the domain is reduced and the upstream 53% is
held at full strength. The corpus files carry that rectangle verbatim as a v20 polygon-sheet
overlay row (sentinel Mat ID −1, "SSR reduce"), read from `#102_1` for the dry file and from the
`#102_2_*` drawdown models for the snapshots. It is a fidelity transcription, not a correction: the
critical mechanism on this dam is a downstream-face wedge and already lies inside the rectangle, so
the constraint is inert here — the dry case returns the same value to every printed digit with the
zone carried as without it — and with it carried, neither side of the comparison is constrained
differently from the other.

RS2 itself enforces the rectangle differently, by splitting the mesh along it and giving the
outside region a material that cannot yield at all, where the corpus overlay holds the outside at
*full* strength. The two are the same constraint on this dam, whose mechanism is nowhere near the
boundary between them, and the overlay is what every locked value below is taken under.

**Dry case.**

| Method | XSLOPE | RS2 SSRM | Huang & Jia FEM | Slide2 Spencer | XSLOPE LEM |
|---|---|---|---|---|---|
| SSRM (2.5 m mesh) | 2.455 | 2.43 (+1.0%) | 2.43 (+1.0%) | 2.455 | Bishop 2.452 / Spencer 2.451 |

The critical mechanism is a shallow downstream-face wedge, mildly mesh-sensitive between the 2.5
and 1.5 m target sizes. Locked at 2.5 m.

<!-- test: file=files/rocscience/vp102a.xlsx, type=fem_ssrm, expected_fs=2.455, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.9, f_max=2.8, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP102 -->

![RS2 Part IV VP102: dry homogeneous earth dam (Huang & Jia 2008), SSRM 2.455 vs RS2 SSRM 2.43 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF](images/RS2-P4-VP102.png)

**Transient drawdown SSRM.** After the reservoir drops from el. 24 to el. 7 at *t* = 0, the dam
drains and the strength-reduction factor rises monotonically, so the governing minimum is the
initial steady state. Each snapshot's *u* = 'seep' field comes from the single transient seepage
solve described under [VP102](rocscience.md#vp102), meshed as tri6 so the SSRM runs on the
snapshot's own quadratic mesh. Case 2 takes φ<sup>b</sup> = 0°, the clamped baseline in which
suction credits no strength; Case 3 sets φ<sup>b</sup> = 37° through the run's `suction_phi_b`
option, so matric suction above the phreatic surface adds apparent cohesion s·tan φ<sup>b</sup>.

| Stage | Case 2 XSLOPE (φ<sup>b</sup> = 0°) | Case 2 RS2 SSR | Case 3 XSLOPE (φ<sup>b</sup> = 37°) | Case 3 RS2 SSR |
|---|---|---|---|---|
| 60 h | 1.713 | 1.77 (−3.2%) | 1.779 | 1.82 (−2.3%) |
| 300 h | 1.998 | 2.06 (−3.0%) | 2.162 | 2.14 (+1.0%) |
| 1500 h | 2.304 | 2.29 (+0.6%) | 2.687 | 2.48 (+8.3%) |

*Case 2 runs 3.0–3.2% below the RS2 SSR drawdown column over the first 300 h and crosses it by
1500 h (+0.6%). That is the same shape the Slide2-LEM curve shows on the same flow solve, from the
same cause: the substituted Gardner retention curve holds water in the unsaturated zone more tightly
than RS2's built-in "Silt" pair, so XSLOPE's dissipation front runs slightly *behind* the vendor's
early on. The dry case, which has no water in it at all, sits +1.0% instead.*

*Case 3 adds the φ<sup>b</sup> = 37° suction credit, and it grows with the drainage: +1.0% at 300 h
and +8.3% above the RS2 SSR value by 1500 h, the frame with the most suction to credit. The
vendor's basis for that column is what the corpus carries: every `#102_3_*` model sets
φ<sup>b</sup> = 37° on the dam material with an air-entry value of zero, against
φ<sup>b</sup> = 0° on the paired `#102_2_*` twins, with the material suction cutoff switched off,
so the credit is uncapped on both sides.*

*What the 8.3% measures is the size of the suction field, not the strength model. At 1500 h
XSLOPE's field puts 46% of the mesh in suction and reaches 204 kPa, an apparent cohesion of up to
154 kPa against c′ = 13.8 kPa, and the factor of safety it buys is about twice what separates the
vendor's own two columns. The same extended Mohr-Coulomb machinery is exercised uncapped under the
identical vendor settings by [RS2-28](#rs2-28), at φ<sup>b</sup> = 15° on a steady unsaturated
field, and lands within 2.1% of RS2's SSR at all three heads with no positive bias, so the
difference here rides in on the same substituted Gardner curve that sets the Case 2 shape.*

<!-- test: file=files/rocscience/vp102t_60.xlsx, type=fem_ssrm, expected_fs=1.713, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.5, f_max=2.9, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP102-t-60-c2 -->
<!-- test: file=files/rocscience/vp102t_300.xlsx, type=fem_ssrm, expected_fs=1.998, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.5, f_max=2.9, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP102-t-300-c2 -->
<!-- test: file=files/rocscience/vp102t_1500.xlsx, type=fem_ssrm, expected_fs=2.304, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.5, f_max=2.9, max_iter=16000, tension_srf=true, k0=1, benchmark=RS2-P4-VP102-t-1500-c2 -->
<!-- test: file=files/rocscience/vp102t_60.xlsx, type=fem_ssrm, expected_fs=1.779, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.5, f_max=2.9, max_iter=16000, suction_phi_b=Material 1:37, tension_srf=true, k0=1, benchmark=RS2-P4-VP102-t-60-c3 -->
<!-- test: file=files/rocscience/vp102t_300.xlsx, type=fem_ssrm, expected_fs=2.162, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.5, f_max=2.9, max_iter=16000, suction_phi_b=Material 1:37, tension_srf=true, k0=1, benchmark=RS2-P4-VP102-t-300-c3 -->
<!-- test: file=files/rocscience/vp102t_1500.xlsx, type=fem_ssrm, expected_fs=2.687, element_type=tri6, target_size=2.5, tolerance=0.02, f_min=1.5, f_max=2.9, max_iter=16000, suction_phi_b=Material 1:37, tension_srf=true, k0=1, benchmark=RS2-P4-VP102-t-1500-c3 -->

One frame of each case is drawn: the mechanism is the same downstream-face wedge at every frame
of a monotone sequence, so the remaining four repeat one of these two pictures.

**Case 2 — 300 h after drawdown, φ<sup>b</sup> = 0° (vp102t_300)**

![RS2 Part IV VP102 Case 2 at 300 h, the φ<sup>b</sup> = 0° baseline, SSRM 1.998 against RS2 SSR 2.06 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the downstream-face wedge on the draining transient field](images/RS2-P4-VP102-t-300-c2.png)

**Case 3 — 1500 h after drawdown, φ<sup>b</sup> = 37° (vp102t_1500)**

![RS2 Part IV VP102 Case 3 at 1500 h, with the φ<sup>b</sup> = 37° suction credit, SSRM 2.687 against RS2 SSR 2.48 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the frame with the most suction to credit and the widest difference on the row](images/RS2-P4-VP102-t-1500-c3.png)

## Hoek-Brown verification (Hammah et al. 2005) {#hoek-brown}

The `hb` strength option is verified end-to-end — LEM *and* SSRM — against Example 1 of the
Rocscience method paper that introduced Hoek-Brown shear-strength reduction. It is the
low-GSI counterpart to [RS2-60](#rs2-60) above, which exercises the same criterion at
GSI = 70:

> Hammah, R.E., Yacoub, T.E., Corkum, B., & Curran, J.H. (2005). "The shear strength
> reduction method for the generalized Hoek-Brown criterion." *Proc. 40th U.S. Symposium
> on Rock Mechanics (ARMA/USRMS)*, Anchorage, Paper 05-810.

A 10 m high homogeneous rock slope at 45° in a very weak rock mass: $\sigma_{ci}$ = 30 MPa,
GSI = 5, $m_i$ = 2, $D$ = 0, $\gamma$ = 25 kN/m³, $E$ = 5000 MPa, $\nu$ = 0.3. This is a
demanding test of the criterion rather than of the geometry — at GSI = 5 the envelope is
strongly curved, and the exponent $a$ = 0.619 is far from the $a$ = 0.5 special case.

**Derived constants.** m<sub>b</sub> and a reproduce the paper's Table 1 to its printed digits;
s differs by 4.2%, the paper's 2.5 × 10⁻⁵ being a rounded print of exp(−95/9):

| | XSLOPE | Hammah et al. |
|---|---|---|
| $m_b$ | 0.0672 | 0.067 |
| $s$ | 2.605e-5 | 2.5e-5 |
| $a$ | 0.61921 | 0.619 |

**Factors of safety:**

| Method | XSLOPE | Hammah et al. |
|---|---|---|
| Bishop simplified | 1.150 | 1.153 (−0.3%) |
| Spencer | 1.152 | 1.152 (0.0%) |
| Janbu corrected | 1.144 | — |
| Morgenstern-Price | 1.148 | — |
| SSRM | 1.166 | 1.15 (+1.4%) |

*Hammah et al. report the same SSRM 1.15 for the generalized Hoek-Brown criterion and for its
equivalent Mohr-Coulomb form.*

The paper dimensions only the slope itself (10 m high, 10 m run) and leaves the foundation
depth and lateral extents unstated. The answer does not depend on them: foundation depths of
2, 4, 6 and 10 m all return Bishop 1.150 / Spencer 1.152, because the critical mechanism
exits at the toe. The SSRM approaches the published value from above as the mesh refines, and is
quoted here at the tagged 0.9 m mesh.

Corps of Engineers and Lowe & Karafiath both converge on this slope. They are the two methods that
struggle on *strong* rock masses, where the instantaneous friction angle at low confinement
exceeds ~55°; at GSI = 5 the envelope is weak enough that they are well behaved. See the note in
the [LEM overview](../lem/overview.md#hoek-brown-strength).

<!-- test: file=files/rocscience/hammah_hb1.xlsx, type=circular_search, num_slices=40, fs_bishop=1.150, fs_spencer=1.152, fs_janbu=1.144, fs_mprice=1.148, benchmark=HB-lem -->
<!-- test: file=files/rocscience/hammah_hb1.xlsx, type=fem_ssrm, expected_fs=1.166, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=0.8, f_max=1.6, max_iter=16000, k0=1, benchmark=HB-ssrm -->

![Hoek-Brown SSRM (Hammah et al. 2005 example 1): a 10 m, 45° slope in a GSI = 5 rock mass, SSRM 1.166 against the paper's 1.15 — FEM inputs, mesh, max shear strain and displacement vectors at the critical SRF, the band exiting at the toe](images/HB-ssrm.png)
