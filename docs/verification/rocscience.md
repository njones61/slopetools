# Rocscience Slide2 Verification Corpus

The [Rocscience Slide2 verification manual](https://www.rocscience.com/help/slide2/verification-theory/verification-manuals)
publishes 111 slope stability problems drawn from the literature, each with Slide2's own factor of
safety and, in most cases, the original authors'. XSLOPE reproduces them problem by problem; the
summary table gives each problem's headline comparison and a
[match dot](index.md#how-the-match-dots-are-scored), and links to the section that builds it.

How the manual's problems reach this corpus:

- Geometry and properties come from the manual's tables and coordinate-labeled figures; a problem
  that appears only as an unlabeled figure is built from the original publication's coordinates,
  never a digitized guess.
- Roughly a third of the problems are also built in the [GeoStudio (SLOPE/W) corpus](geostudio.md);
  those rows link there rather than repeat the build.
- `benchmarks/rocscience/build_problems.py` writes the input files (problem #38 has its own builder,
  `build_vp038.py`, for the steady unsaturated seepage field behind it) and `make_figures.py` the
  figures, model inputs beside a representative solved surface.

<!-- test: file=files/rocscience/vp002.xlsx, type=circular_search, num_slices=40, fs_bishop=1.589, fs_spencer=1.585, fs_janbu=1.481, fs_mprice=1.586, benchmark=VP2 -->
<!-- test: file=files/rocscience/vp003.xlsx, type=circular_search, num_slices=40, fs_bishop=1.403, fs_spencer=1.372, fs_janbu=1.354, fs_mprice=1.371, benchmark=VP3 -->
<!-- test: file=files/rocscience/vp004.xlsx, type=circular_search, num_slices=40, fs_bishop=1.013, fs_spencer=0.989, fs_janbu=0.963, fs_mprice=0.987, benchmark=VP4 -->
<!-- test: file=files/rocscience/vp005.xlsx, type=single_circle, num_slices=60, fs_bishop=1.955, fs_spencer=1.955, fs_janbu=1.965, fs_mprice=1.955, benchmark=VP5 -->
<!-- test: file=files/rocscience/vp006.xlsx, type=single_circle, num_slices=60, fs_bishop=2.206, fs_spencer=2.290, fs_janbu=2.073, fs_mprice=2.299, benchmark=VP6 -->
<!-- test: file=files/rocscience/vp008.xlsx, type=single_noncirc, num_slices=50, fs_spencer=1.276, fs_janbu=1.294, fs_mprice=1.260, benchmark=VP8 -->
<!-- test: file=files/rocscience/vp009.xlsx, type=noncircular_search, num_slices=50, fs_spencer=0.724, fs_janbu=0.718, benchmark=VP9 -->
<!-- test: file=files/rocscience/vp010.xlsx, type=circular_search, num_slices=40, fs_bishop=1.500, fs_spencer=1.501, fs_janbu=1.457, benchmark=VP10 -->
<!-- test: file=files/rocscience/vp015.xlsx, type=circular_search, num_slices=40, fs_bishop=0.419, fs_spencer=0.422, fs_janbu=0.436, fs_mprice=0.420, benchmark=VP15 -->
<!-- test: file=files/rocscience/vp016.xlsx, type=circular_search, num_slices=40, fs_bishop=1.112, fs_spencer=1.113, fs_janbu=1.122, fs_mprice=1.111, benchmark=VP16 -->
<!-- test: file=files/rocscience/vp017.xlsx, type=circular_search, num_slices=50, fs_oms=1.274, fs_bishop=1.342, fs_spencer=1.340, benchmark=VP17 -->
<!-- test: file=files/rocscience/vp018.xlsx, type=noncircular_search, num_slices=50, fs_spencer=1.033, fs_mprice=1.024, benchmark=VP18 -->
<!-- test: file=files/rocscience/vp019.xlsx, type=circular_search, num_slices=50, fs_bishop=1.448, fs_spencer=1.429, benchmark=VP19 -->
<!-- test: file=files/rocscience/vp020.xlsx, type=circular_search, num_slices=50, fs_bishop=1.086, fs_spencer=1.091, benchmark=VP20-circ -->
<!-- test: file=files/rocscience/vp020.xlsx, type=noncircular_search, num_slices=50, fs_spencer=1.082, benchmark=VP20-noncirc -->
<!-- test: file=files/rocscience/vp023.xlsx, type=circular_search, num_slices=50, fs_oms=1.357, fs_bishop=1.130, benchmark=VP23 -->
<!-- test: file=files/rocscience/vp024.xlsx, type=circular_search, num_slices=50, fs_oms=1.435, fs_bishop=1.435, benchmark=VP24 -->
<!-- test: file=files/rocscience/vp025.xlsx, type=single_noncirc, num_slices=60, fs_spencer=1.052, benchmark=VP25 -->
<!-- test: file=files/rocscience/vp026.xlsx, type=single_noncirc, num_slices=60, right_facing=true, fs_spencer=1.043, benchmark=VP26 -->
<!-- test: file=files/rocscience/vp027.xlsx, type=single_circle, num_slices=50, fs_bishop=1.369, fs_spencer=1.375, fs_janbu=1.365, fs_mprice=1.371, fs_corps=1.388, fs_lowe=1.386, benchmark=VP27 -->
<!-- test: file=files/rocscience/vp035.xlsx, type=circular_search, num_slices=50, fs_bishop=2.529, benchmark=VP35-fs -->
<!-- test: file=files/rocscience/vp035.xlsx, type=reliability, method=bishop, circular=true, search=false, expected_beta=3.353, tolerance=0.03, benchmark=VP35-beta -->
<!-- test: file=files/rocscience/vp036.xlsx, type=circular_search, num_slices=50, fs_bishop=1.333, benchmark=VP36-fs -->
<!-- test: file=files/rocscience/vp037.xlsx, type=single_circle, num_slices=60, fs_bishop=0.764, fs_spencer=0.764, benchmark=VP37 -->
<!-- test: file=files/rocscience/vp038a.xlsx, type=single_circle, num_slices=60, suction_phi_b=Cut soil:15, fs_bishop=1.612, benchmark=VP38-h61 -->
<!-- test: file=files/rocscience/vp038b.xlsx, type=single_circle, num_slices=60, suction_phi_b=Cut soil:15, fs_bishop=1.533, benchmark=VP38-h62 -->
<!-- test: file=files/rocscience/vp038c.xlsx, type=single_circle, num_slices=60, suction_phi_b=Cut soil:15, fs_bishop=1.413, benchmark=VP38-h63 -->
<!-- test: file=files/rocscience/vp028a.xlsx, type=single_circle, num_slices=60, fs_bishop=1.129, benchmark=VP28a -->
<!-- test: file=files/rocscience/vp028a.xlsx, type=reliability, method=bishop, circular=true, search=false, expected_beta=0.768, tolerance=0.03, benchmark=VP28a-beta -->
<!-- test: file=files/rocscience/vp028a.xlsx, type=reliability_mc, method=bishop, circular=true, search=false, n_samples=10000, num_slices=40, expected_beta=0.774, tolerance=0.02, expected_pf=0.215, pf_tol=0.02, benchmark=VP28a-mc -->
<!-- test: file=files/rocscience/vp028b.xlsx, type=single_circle, num_slices=60, fs_bishop=1.158, benchmark=VP28b -->
<!-- test: file=files/rocscience/vp028b.xlsx, type=reliability, method=bishop, circular=true, search=false, expected_beta=0.787, tolerance=0.03, benchmark=VP28b-beta -->
<!-- test: file=files/rocscience/vp028b.xlsx, type=reliability_mc, method=bishop, circular=true, search=false, n_samples=10000, num_slices=40, expected_beta=0.800, tolerance=0.02, expected_pf=0.206, pf_tol=0.02, benchmark=VP28b-mc -->
<!-- test: file=files/rocscience/vp028c.xlsx, type=single_circle, num_slices=60, fs_bishop=1.177, benchmark=VP28c -->
<!-- test: file=files/rocscience/vp028c.xlsx, type=reliability, method=bishop, circular=true, search=false, expected_beta=0.798, tolerance=0.03, benchmark=VP28c-beta -->
<!-- test: file=files/rocscience/vp028c.xlsx, type=reliability_mc, method=bishop, circular=true, search=false, n_samples=10000, num_slices=40, expected_beta=0.789, tolerance=0.02, expected_pf=0.209, pf_tol=0.02, benchmark=VP28c-mc -->
<!-- test: file=files/rocscience/vp029.xlsx, type=single_circle, num_slices=60, fs_spencer=1.145, fs_mprice=1.145, benchmark=VP29-det -->
<!-- test: file=files/rocscience/vp029.xlsx, type=reliability, method=spencer, circular=true, search=false, expected_beta=0.936, tolerance=0.03, benchmark=VP29-beta -->
<!-- test: file=files/rocscience/vp030a.xlsx, type=single_circle, num_slices=60, fs_bishop=1.679, benchmark=VP30a -->
<!-- test: file=files/rocscience/vp030b.xlsx, type=single_circle, num_slices=60, fs_bishop=1.650, benchmark=VP30b -->
<!-- test: file=files/rocscience/vp032a.xlsx, type=single_circle, num_slices=60, fs_bishop=1.218, fs_spencer=1.218, benchmark=VP32a -->
<!-- test: file=files/rocscience/vp032b.xlsx, type=single_circle, num_slices=60, fs_bishop=1.216, fs_spencer=1.216, benchmark=VP32b -->
<!-- test: file=files/rocscience/vp032c.xlsx, type=single_circle, num_slices=60, fs_bishop=0.981, fs_spencer=0.981, benchmark=VP32c -->
<!-- test: file=files/rocscience/vp033.xlsx, type=single_circle, num_slices=60, composite=true, fs_bishop=1.320, benchmark=VP33 -->
<!-- test: file=files/rocscience/vp034.xlsx, type=single_noncirc, num_slices=60, fs_spencer=2.423, fs_mprice=2.384, benchmark=VP34 -->
<!-- test: file=files/rocscience/vp036.xlsx, type=reliability, method=bishop, expected_beta=2.263, tolerance=0.03, benchmark=VP36-beta -->
<!-- test: file=files/rocscience/vp039a.xlsx, type=single_circle, num_slices=60, fs_spencer=0.968, benchmark=VP39a -->
<!-- test: file=files/rocscience/vp039b.xlsx, type=single_circle, num_slices=60, fs_spencer=1.332, benchmark=VP39b -->
<!-- test: file=files/rocscience/vp039c.xlsx, type=single_circle, num_slices=60, fs_spencer=1.200, benchmark=VP39c -->
<!-- test: file=files/rocscience/vp039d.xlsx, type=single_circle, num_slices=60, fs_spencer=1.343, benchmark=VP39d -->
<!-- test: file=files/rocscience/vp040.xlsx, type=single_noncirc, num_slices=30, fs_janbu=1.003, benchmark=VP40-det -->
<!-- test: file=files/rocscience/vp040.xlsx, type=sensitivity, param=mat:Soil:pow_a, method=janbu, search=false, num_slices=30, n=3, rel_range=0.15, expected_base=1.003, expected_low=0.853, expected_high=1.154, tolerance=0.01, benchmark=VP40-sensA -->
<!-- test: file=files/rocscience/vp040.xlsx, type=sensitivity, param=mat:Soil:pow_b, method=janbu, search=false, num_slices=30, n=3, rel_range=0.15, expected_base=1.003, expected_low=0.552, expected_high=1.830, tolerance=0.01, benchmark=VP40-sensB -->
<!-- test: file=files/rocscience/vp041.xlsx, type=circular_search, num_slices=50, fs_bishop=1.668, fs_spencer=1.670, fs_janbu=1.660, benchmark=VP41 -->
<!-- test: file=files/rocscience/vp042.xlsx, type=single_circle, num_slices=60, fs_oms=1.773, fs_bishop=1.882, fs_spencer=1.926, fs_mprice=1.925, benchmark=VP42-circle -->
<!-- test: file=files/rocscience/vp042.xlsx, type=single_noncirc, num_slices=60, fs_spencer=1.882, fs_mprice=1.869, benchmark=VP42-noncirc -->
<!-- test: file=files/rocscience/vp043.xlsx, type=single_noncirc, num_slices=50, fs_spencer=1.352, fs_janbu=1.352, fs_mprice=1.352, fs_corps=1.352, fs_lowe=1.352, benchmark=VP43 -->
<!-- test: file=files/rocscience/vp044a.xlsx, type=circular_search, num_slices=40, fs_spencer=0.958, benchmark=VP44-pow -->
<!-- test: file=files/rocscience/vp044b.xlsx, type=circular_search, num_slices=40, fs_spencer=1.518, benchmark=VP44-mc -->
<!-- test: file=files/rocscience/vp044c.xlsx, type=circular_search, num_slices=40, fs_spencer=0.980, benchmark=VP44-lla -->
<!-- test: file=files/rocscience/vp045a.xlsx, type=circular_search, num_slices=50, fs_spencer=2.801, benchmark=VP45-mc -->
<!-- test: file=files/rocscience/vp045b.xlsx, type=circular_search, num_slices=50, fs_spencer=2.649, benchmark=VP45-pow -->
<!-- test: file=files/rocscience/vp047.xlsx, type=single_noncirc, num_slices=50, fs_janbu=0.899, benchmark=VP47 -->
<!-- test: file=files/rocscience/vp048.xlsx, type=single_noncirc, num_slices=50, fs_janbu=0.991, fs_spencer=0.991, benchmark=VP48 -->
<!-- test: file=files/rocscience/vp049.xlsx, type=single_noncirc, num_slices=60, fs_janbu=1.469, fs_spencer=1.439, benchmark=VP49 -->
<!-- test: file=files/rocscience/vp058.xlsx, type=single_circle, num_slices=60, fs_bishop=1.142, fs_spencer=1.140, fs_oms=1.119, benchmark=VP58 -->
<!-- test: file=files/rocscience/vp059.xlsx, type=single_noncirc, num_slices=60, fs_janbu=0.579, fs_corps=0.577, benchmark=VP59 -->
<!-- test: file=files/rocscience/vp060.xlsx, type=single_noncirc, num_slices=60, fs_spencer=1.010, fs_janbu=1.073, benchmark=VP60 -->
<!-- test: file=files/rocscience/vp050.xlsx, type=single_noncirc, num_slices=60, fs_janbu=1.448, fs_spencer=1.576, benchmark=VP50 -->
<!-- test: file=files/rocscience/vp051.xlsx, type=single_circle, num_slices=100, fs_oms=1.069, fs_bishop=1.278, fs_janbu=1.205, fs_corps=1.404, fs_lowe=1.296, fs_spencer=1.294, fs_mprice=1.304, benchmark=VP51 -->
<!-- test: file=files/rocscience/vp052a.xlsx, type=circular_search, num_slices=50, fs_spencer=1.797, fs_bishop=1.796, benchmark=VP52-dry -->
<!-- test: file=files/rocscience/vp052b.xlsx, type=circular_search, num_slices=50, fs_spencer=1.189, fs_bishop=1.176, benchmark=VP52-wet -->
<!-- test: file=files/rocscience/vp053.xlsx, type=single_noncirc, num_slices=30, fs_janbu=1.048, fs_spencer=1.048, fs_mprice=1.048, fs_lowe=1.048, benchmark=VP53 -->
<!-- test: file=files/rocscience/vp054a.xlsx, type=single_circle, num_slices=50, fs_bishop=1.100, benchmark=VP54-nopile -->
<!-- test: file=files/rocscience/vp054b.xlsx, type=single_circle, num_slices=50, fs_bishop=1.185, benchmark=VP54-pile -->
<!-- test: file=files/rocscience/vp055.xlsx, type=single_circle, num_slices=60, fs_oms=1.138, fs_bishop=1.290, fs_spencer=1.297, fs_lowe=1.321, benchmark=VP55-circle -->
<!-- test: file=files/rocscience/vp055.xlsx, type=circular_search, num_slices=50, fs_bishop=1.289, fs_spencer=1.295, benchmark=VP55-search -->
<!-- test: file=files/rocscience/vp056.xlsx, type=single_circle, num_slices=60, fs_oms=1.142, fs_bishop=1.283, fs_spencer=1.288, fs_lowe=1.307, benchmark=VP56-circle -->
<!-- test: file=files/rocscience/vp056.xlsx, type=circular_search, num_slices=50, fs_bishop=1.282, fs_spencer=1.288, benchmark=VP56-search -->
<!-- test: file=files/rocscience/vp057.xlsx, type=single_circle, composite=true, num_slices=60, fs_oms=1.086, fs_bishop=1.389, fs_spencer=1.396, fs_mprice=1.375, fs_lowe=1.387, benchmark=VP57-composite-circle -->
<!-- test: file=files/rocscience/vp057.xlsx, type=circular_search, num_slices=50, fs_bishop=1.411, fs_spencer=1.416, benchmark=VP57-circles-only -->
<!-- test: file=files/rocscience/vp057.xlsx, type=circular_search, composite=true, num_slices=50, fs_bishop=1.388, fs_spencer=1.396, benchmark=VP57-composite-search -->
<!-- test: file=files/rocscience/vp086.xlsx, type=circular_search, num_slices=50, fs_bishop=1.617, fs_spencer=1.611, benchmark=VP86 -->
<!-- test: file=files/rocscience/vp061a.xlsx, type=circular_search, num_slices=40, fs_spencer=1.466, benchmark=VP61-pow -->
<!-- test: file=files/rocscience/vp061b.xlsx, type=circular_search, num_slices=40, fs_spencer=1.367, benchmark=VP61-mc -->
<!-- test: file=files/rocscience/vp062a.xlsx, type=circular_search, num_slices=50, fs_spencer=1.001, fs_bishop=0.991, benchmark=VP62-dry -->
<!-- test: file=files/rocscience/vp062b.xlsx, type=circular_search, num_slices=50, fs_spencer=1.001, fs_bishop=0.986, benchmark=VP62-ru -->
<!-- test: file=files/rocscience/vp063.xlsx, type=noncircular_search, num_slices=50, fs_spencer=1.001, fs_janbu=0.999, benchmark=VP63 -->
<!-- test: file=files/rocscience/vp097.xlsx, type=circular_search, rapid=true, num_slices=50, fs_spencer=1.044, fs_bishop=1.042, benchmark=VP97 -->
<!-- test: file=files/rocscience/vp100.xlsx, type=circular_search, num_slices=50, fs_bishop=1.201, fs_spencer=1.206, benchmark=VP100 -->
<!-- test: file=files/rocscience/vp101.xlsx, type=circular_search, num_slices=50, fs_bishop=1.416, fs_spencer=1.422, benchmark=VP101 -->
<!-- test: file=files/rocscience/vp087.xlsx, type=single_circle, num_slices=50, fs_bishop=1.031, benchmark=VP87 -->
<!-- test: file=files/rocscience/vp088.xlsx, type=single_circle, num_slices=50, fs_spencer=1.057, benchmark=VP88 -->
<!-- test: file=files/rocscience/vp089.xlsx, type=single_circle, num_slices=50, fs_spencer=1.011, benchmark=VP89 -->
<!-- test: file=files/rocscience/vp090.xlsx, type=single_circle, num_slices=50, fs_bishop=1.012, benchmark=VP90 -->
<!-- test: file=files/rocscience/vp091.xlsx, type=single_circle, num_slices=50, fs_spencer=0.960, benchmark=VP91 -->
<!-- test: file=files/rocscience/vp092.xlsx, type=single_circle, num_slices=50, fs_bishop=1.010, benchmark=VP92 -->
<!-- test: file=files/rocscience/vp093.xlsx, type=single_circle, num_slices=50, fs_bishop=0.961, benchmark=VP93 -->
<!-- test: file=files/rocscience/vp094.xlsx, type=single_circle, num_slices=50, fs_bishop=1.020, benchmark=VP94 -->
<!-- test: file=files/rocscience/vp098.xlsx, type=circular_search, num_slices=40, rapid=true, fs_spencer=1.046, benchmark=VP98 -->
<!-- test: file=files/rocscience/vp099.xlsx, type=circular_search, num_slices=40, rapid=true, fs_spencer=1.527, benchmark=VP99 -->
<!-- test: file=files/rocscience/vp106a.xlsx, type=circular_search, num_slices=40, fs_bishop=1.143, benchmark=VP106a -->
<!-- test: file=files/rocscience/vp106b.xlsx, type=circular_search, num_slices=40, fs_bishop=1.540, benchmark=VP106b -->
<!-- test: file=files/rocscience/vp106c.xlsx, type=circular_search, num_slices=40, fs_bishop=1.451, benchmark=VP106c -->
<!-- test: file=files/rocscience/vp106d.xlsx, type=circular_search, num_slices=40, fs_bishop=1.341, benchmark=VP106d -->
<!-- test: file=files/rocscience/vp106e.xlsx, type=circular_search, num_slices=40, fs_bishop=1.260, benchmark=VP106e -->
<!-- test: file=files/rocscience/vp107a.xlsx, type=single_circle, num_slices=60, fs_bishop=1.382, fs_spencer=1.398, benchmark=VP107a -->
<!-- test: file=files/rocscience/vp107b.xlsx, type=single_circle, num_slices=60, fs_bishop=1.382, benchmark=VP107b -->
<!-- test: file=files/rocscience/vp108a.xlsx, type=single_circle, num_slices=60, fs_bishop=1.790, fs_spencer=1.797, benchmark=VP108a -->
<!-- test: file=files/rocscience/vp108b.xlsx, type=single_circle, num_slices=60, fs_bishop=1.830, fs_spencer=1.835, benchmark=VP108b -->
<!-- test: file=files/rocscience/vp109.xlsx, type=single_circle, num_slices=60, fs_bishop=1.790, fs_spencer=1.797, benchmark=VP109 -->
<!-- test: file=files/rocscience/vp096.xlsx, type=single_circle, rapid=true, num_slices=60, fs_spencer=1.434, fs_bishop=1.432, benchmark=VP96 -->
<!-- test: file=files/rocscience/vp064.xlsx, type=single_circle, num_slices=60, fs_bishop=2.489, fs_spencer=2.488, benchmark=VP64 -->
<!-- test: file=files/rocscience/vp065.xlsx, type=single_circle, num_slices=60, fs_bishop=2.725, fs_spencer=2.748, benchmark=VP65 -->
<!-- test: file=files/rocscience/vp066.xlsx, type=single_circle, num_slices=60, fs_bishop=2.254, fs_spencer=2.258, benchmark=VP66 -->
<!-- test: file=files/rocscience/vp067.xlsx, type=single_circle, num_slices=60, fs_bishop=1.320, fs_spencer=1.316, fs_janbu=1.340, benchmark=VP67 -->
<!-- test: file=files/rocscience/vp068.xlsx, type=single_circle, num_slices=60, fs_bishop=1.234, fs_mprice=1.234, benchmark=VP68 -->
<!-- test: file=files/rocscience/vp069.xlsx, type=single_circle, num_slices=60, fs_bishop=1.999, fs_spencer=2.013, fs_mprice=2.013, benchmark=VP69 -->
<!-- test: file=files/rocscience/vp075.xlsx, type=circular_search, num_slices=40, fs_bishop=1.424, fs_spencer=1.420, benchmark=VP75 -->
<!-- test: file=files/rocscience/vp075.xlsx, type=circular_search, seed=grid, num_slices=40, fs_bishop=1.424, fs_spencer=1.420, benchmark=VP75-grid -->
<!-- test: file=files/rocscience/vp076a.xlsx, type=circular_search, num_slices=40, fs_bishop=1.065, fs_spencer=1.072, benchmark=VP76-seep -->
<!-- test: file=files/rocscience/vp076b.xlsx, type=circular_search, num_slices=40, fs_bishop=1.070, fs_spencer=1.078, benchmark=VP76-piezo -->
<!-- test: file=files/rocscience/vp072a.xlsx, type=single_circle, num_slices=60, fs_oms=1.071, fs_bishop=1.339, fs_spencer=1.341, fs_mprice=1.342, benchmark=VP72-seep-tan197 -->
<!-- test: file=files/rocscience/vp072b.xlsx, type=single_circle, num_slices=60, fs_oms=1.348, fs_bishop=1.572, fs_spencer=1.563, fs_mprice=1.564, benchmark=VP72-piezo-tan197 -->
<!-- test: file=files/rocscience/vp073.xlsx, type=circular_search, num_slices=40, fs_bishop=1.766, fs_spencer=1.766, fs_janbu=1.733, benchmark=VP73 -->
<!-- test: file=files/rocscience/vp102a.xlsx, type=circular_search, num_slices=40, fs_bishop=2.452, fs_spencer=2.451, benchmark=VP102-dry -->
<!-- test: file=files/rocscience/vp102b.xlsx, type=circular_search, num_slices=40, fs_bishop=1.722, fs_spencer=1.731, benchmark=VP102-steady -->
<!-- test: file=files/rocscience/vp103a.xlsx, type=noncircular_search, num_slices=40, fs_spencer=1.221, benchmark=VP103a-deep -->
<!-- test: file=files/rocscience/vp103b.xlsx, type=noncircular_search, num_slices=40, fs_spencer=1.298, benchmark=VP103b-deep -->
<!-- test: file=files/rocscience/vp103c.xlsx, type=noncircular_search, num_slices=40, fs_spencer=1.374, benchmark=VP103c-deep -->
<!-- test: file=files/rocscience/vp103d.xlsx, type=noncircular_search, num_slices=40, fs_spencer=1.322, benchmark=VP103d-shallow -->
<!-- test: file=files/rocscience/vp103a.xlsx, type=circular_search, num_slices=40, seed=grid, tangent_depth=0;3, fs_spencer=1.299, benchmark=VP103a-deep-circ -->
<!-- test: file=files/rocscience/vp103b.xlsx, type=circular_search, num_slices=40, seed=grid, tangent_depth=0;3, fs_spencer=1.379, benchmark=VP103b-deep-circ -->
<!-- test: file=files/rocscience/vp103c.xlsx, type=circular_search, num_slices=40, seed=grid, tangent_depth=0;3, fs_spencer=1.458, benchmark=VP103c-deep-circ -->
<!-- test: file=files/rocscience/vp103a.xlsx, type=circular_search, num_slices=40, seed=grid, tangent_depth=18;30, fs_spencer=1.348, benchmark=VP103a-shallow-circ -->
<!-- test: file=files/rocscience/vp103b.xlsx, type=circular_search, num_slices=40, seed=grid, tangent_depth=18;30, fs_spencer=1.348, benchmark=VP103b-shallow-circ -->
<!-- test: file=files/rocscience/vp103c.xlsx, type=circular_search, num_slices=40, seed=grid, tangent_depth=18;30, fs_spencer=1.348, benchmark=VP103c-shallow-circ -->
<!-- test: file=files/rocscience/vp104a.xlsx, type=circular_search, num_slices=40, fs_spencer=1.372, benchmark=VP104-noseismic -->
<!-- test: file=files/rocscience/vp104b.xlsx, type=circular_search, num_slices=40, fs_spencer=0.989, benchmark=VP104-k015 -->
<!-- test: file=files/rocscience/vp104a.xlsx, type=critical_kc, method=spencer, expected_kc=0.144, k_min=0.08, k_max=0.22, kc_tol=0.01, num_slices=40, benchmark=VP104-kc -->
<!-- test: file=files/rocscience/vp082.xlsx, type=circular_search, num_slices=40, fs_bishop=1.521, fs_spencer=1.533, benchmark=VP82 -->
<!-- test: file=files/rocscience/vp083a.xlsx, type=circular_search, num_slices=40, fs_bishop=1.305, fs_spencer=1.275, benchmark=VP83-I -->
<!-- test: file=files/rocscience/vp083b.xlsx, type=circular_search, num_slices=40, fs_bishop=1.328, fs_spencer=1.326, benchmark=VP83-II -->
<!-- test: file=files/rocscience/vp084a.xlsx, type=circular_search, num_slices=40, fs_bishop=0.756, fs_spencer=0.751, benchmark=VP84-I -->
<!-- test: file=files/rocscience/vp084b.xlsx, type=circular_search, num_slices=40, fs_bishop=0.905, fs_spencer=0.897, benchmark=VP84-II -->
<!-- test: file=files/rocscience/vp084c.xlsx, type=circular_search, num_slices=40, fs_bishop=1.042, fs_spencer=1.028, benchmark=VP84-III -->
<!-- test: file=files/rocscience/vp084d.xlsx, type=circular_search, num_slices=40, fs_bishop=1.151, fs_spencer=1.131, benchmark=VP84-IV -->
<!-- test: file=files/rocscience/vp071a.xlsx, type=circular_search, num_slices=40, fs_bishop=1.132, fs_spencer=1.132, benchmark=VP71-seep -->
<!-- test: file=files/rocscience/vp071b.xlsx, type=circular_search, num_slices=40, fs_bishop=1.132, fs_spencer=1.132, benchmark=VP71-piezo -->
<!-- test: file=files/rocscience/vp070a.xlsx, type=circular_search, num_slices=40, fs_bishop=1.596, fs_spencer=1.593, benchmark=VP70-p30 -->
<!-- test: file=files/rocscience/vp070b.xlsx, type=circular_search, num_slices=40, fs_bishop=1.596, fs_spencer=1.593, benchmark=VP70-p60 -->
<!-- test: file=files/rocscience/vp074.xlsx, type=circular_search, num_slices=40, fs_bishop=1.219, fs_spencer=1.194, fs_janbu=1.161, benchmark=VP74 -->
<!-- test: file=files/rocscience/vp077a.xlsx, type=single_circle, num_slices=60, fs_oms=1.506, fs_bishop=1.652, fs_spencer=1.724, fs_mprice=1.734, benchmark=VP77-seep-circle -->
<!-- test: file=files/rocscience/vp077a.xlsx, type=circular_search, num_slices=50, fs_bishop=1.637, fs_spencer=1.700, benchmark=VP77-seep-search -->
<!-- test: file=files/rocscience/vp077b.xlsx, type=single_circle, num_slices=60, fs_oms=1.477, fs_bishop=1.591, fs_spencer=1.659, fs_mprice=1.670, benchmark=VP77-piezo-circle -->
<!-- test: file=files/rocscience/vp078.xlsx, type=circular_search, num_slices=40, fs_bishop=1.117, fs_spencer=1.131, benchmark=VP78 -->
<!-- test: file=files/rocscience/vp079.xlsx, type=circular_search, num_slices=40, fs_bishop=1.407, fs_spencer=1.397, benchmark=VP79 -->
<!-- test: file=files/rocscience/vp080a.xlsx, type=single_circle, num_slices=60, fs_bishop=2.533, fs_spencer=2.530, benchmark=VP80-t0 -->
<!-- test: file=files/rocscience/vp080b.xlsx, type=single_circle, num_slices=60, fs_bishop=1.389, fs_spencer=1.352, benchmark=VP80-t15 -->
<!-- test: file=files/rocscience/vp081.xlsx, type=circular_search, num_slices=40, fs_bishop=1.223, fs_spencer=1.204, benchmark=VP81 -->
<!-- test: file=files/rocscience/vp085a.xlsx, type=single_circle, num_slices=60, fs_bishop=1.567, fs_spencer=1.567, benchmark=VP85-active -->
<!-- test: file=files/rocscience/vp085b.xlsx, type=single_circle, num_slices=60, fs_oms=1.319, fs_bishop=1.319, benchmark=VP85-passive -->
<!-- test: file=files/rocscience/vp021a.xlsx, type=single_circle, num_slices=60, fs_oms=1.927, fs_bishop=2.075, fs_spencer=2.071, fs_mprice=2.071, benchmark=VP21-dry -->
<!-- test: file=files/rocscience/vp021b.xlsx, type=single_circle, num_slices=60, fs_oms=1.606, fs_bishop=1.759, fs_spencer=1.757, fs_mprice=1.756, benchmark=VP21-ru -->
<!-- test: file=files/rocscience/vp021c.xlsx, type=single_circle, num_slices=60, fs_oms=1.693, fs_bishop=1.829, fs_spencer=1.827, fs_mprice=1.826, benchmark=VP21-wt -->
<!-- test: file=files/rocscience/vp022a.xlsx, type=single_circle, composite=true, num_slices=60, fs_oms=1.297, fs_bishop=1.380, fs_spencer=1.379, fs_mprice=1.370, benchmark=VP22-dry -->
<!-- test: file=files/rocscience/vp022b.xlsx, type=single_circle, composite=true, num_slices=60, fs_oms=1.037, fs_bishop=1.121, fs_spencer=1.122, fs_mprice=1.112, benchmark=VP22-ru -->

<div class="corpus-summary match" markdown>

| # | Match | Problem | Results | Notes |
|---:|:-:|---|---|---|
| [1](#vp1) | 🟢 | Slope, homogenous | Spencer/M-P 0.984 vs ACADS 1.00 (−1.6%) · Bishop 0.985 vs Slide 0.987 (−0.2%) | ACADS consensus names no method |
| [2](#vp2) | 🟢 | Slope, homogenous, tension crack | Spencer 1.585 vs Slide 1.592 (−0.4%) · Bishop 1.589 vs Slide 1.596 (−0.4%) |  |
| [3](#vp3) | 🟢 | Slope, (3) materials | Spencer 1.372 vs Slide 1.375 (−0.2%) · Bishop 1.403 vs Slide 1.405 (−0.1%) |  |
| [4](#vp4) | 🟢 | Slope, (3) materials, seismic | Spencer 0.989 vs Slide 0.991 (−0.2%) · Bishop 1.013 vs Slide 1.016 (−0.3%) |  |
| [5](#vp5) | 🟢 | Dam, (4) materials | Spencer 1.955 vs Slide 1.948 (+0.4%) · Spencer 1.955 vs infinite-slope theory 1.9475 (+0.4%) |  |
| [6](#vp6) | 🟢 | Dam, (4) materials, predefined slip surface | Spencer 2.290 vs Slide 2.292 (−0.1%) · Spencer 2.290 vs ACADS 2.29 (0.0%) |  |
| [7](geostudio.md#acads-weak-layer) | 🟢 | Slope, (2) materials, weak layer | Spencer 1.258 vs Slide 1.246 (+1.0%) · M-P 1.248 vs Slide 1.275 (−2.1%) | *covered* — [SLOPE/W §2.7](geostudio.md#acads-weak-layer) (`xslope_acads_weak_layer.xlsx`), ACADS 3(a); Giam reference band 1.24–1.27 |
| [8](#vp8) | 🟢 | Slope, (2) materials, weak layer, predefined slip surface | Spencer 1.276 vs Slide 1.277 (−0.1%) · M-P 1.260 vs SLOPE/W 1.261 (−0.1%) | every method within 0.002 of Slide |
| [9](#vp9) | 🟢 | Slope, (2) materials, weak layer, water table, distributed load | Spencer 0.724 vs Slide optimized 0.707 (+2.4%) · Janbu(corr) 0.718 vs Slide 0.734 (−2.2%) | search-difficulty benchmark with a wide published band |
| [10](#vp10) | 🟢 | Slope, homogenous, pore pressure grid, ponded water | Spencer 1.501 vs Slide 1.500 (+0.1%) · Bishop 1.500 vs Slide 1.498 (+0.1%) | **built** (via FE seepage); no GeoStudio counterpart for ACADS #5 |
| [11](#vp11) | <span class="nodata">⊘</span> | Embankment, (2) materials, pore pressure grid |  | *no lock possible* — measured pressures, no flow field behind them |
| [12](#vp12) | <span class="nodata">⊘</span> | Embankment, (4) materials, tension crack, pore pressure grid |  | *no lock possible* — measured pressures, no flow field behind them |
| [13](#vp13) | <span class="nodata">⊘</span> | Embankment, (3) materials, pore pressure grid |  | *no lock possible* — measured pressures, no flow field behind them |
| [14](#vp14) | 🟢 | Slope, homogenous | Bishop 1.404 vs SLOPE/W 1.417 (−0.9%) · Bishop 1.404 vs A&T 1.451 (−3.2%) | A&T report Bishop, so Bishop governs like-for-like |
| [15](#vp15) | 🟢 | Slope, (3) materials, weak layer | Bishop 0.419 vs A&T 0.417 (+0.5%) · Bishop 0.419 vs Slide 0.420 (−0.2%) | A&T report Bishop, so Bishop governs like-for-like |
| [16](#vp16) | 🟢 | Slope, homogenous, water table | Bishop 1.112 vs Slide 1.118 (−0.5%) · Bishop 1.112 vs A&T 1.138 (−2.3%) | A&T report Bishop, so Bishop governs like-for-like |
| [17](#vp17) | 🟢 | Slope, homogenous | Bishop 1.342 vs Slide 1.344 (−0.1%) · Bishop 1.342 vs Y&U 1.348 (−0.4%) | circular search; the local non-circular search hits the same ceiling as #19/#20 |
| [18](#vp18) | 🟢 | Slope, homogenous slope, ru pore pressure | Spencer 1.033 vs Baker 1.02 (+1.3%) · Spencer 1.033 vs Slide 1.010 (+2.3%) | Slide's value is an MC-optimized non-circular search |
| [19](#vp19) | 🟢 | Slope, (4) materials | Spencer 1.429 vs Slide MC 1.398 (+2.2%) | circular search; documented non-circular search-power gap |
| [20](#vp20) | 🟢 | Slope, (4) materials, weak layer, water table | Spencer 1.091 vs Slide 1.093 (−0.2%) · Bishop 1.086 vs Slide 1.087 (−0.1%) | same search-power gap as #19 |
| [21](#vp21) | 🟢 | Slope, homogenous, ru pore pressure | dry: Spencer 2.071 vs F&K 2.073 (−0.1%) · r<sub>u</sub> = 0.25: Spencer 1.757 vs F&K 1.761 (−0.2%) · water table: Spencer 1.827 vs F&K 1.830 (−0.2%) |  |
| [22](#vp22) | 🟢 | Slope, (2) materials, weak layer, ru pore pressure | dry: Spencer 1.379 vs Slide 1.382 (−0.2%) · r<sub>u</sub> = 0.25: Spencer 1.122 vs Slide 1.124 (−0.2%) | the corpus's first composite-surface problem |
| [23](#vp23) | 🟢 | Slope, (3) materials | Ordinary 1.357 vs Low 1.36 (−0.2%) · Bishop 1.130 vs Low 1.14 (−0.9%) | the published Bishop values themselves spread 1.14–1.19 |
| [24](#vp24) | 🟢 | Slope, (3) materials | Ordinary 1.435 vs Slide 1.439 (−0.3%) · Bishop 1.435 vs Low 1.44 (−0.3%) |  |
| [25](#vp25) | 🟢 | Bearing capacity test slope, homogenous, distributed load, predefined slip surface | Spencer 1.052 vs Slide 1.051 (+0.1%) · Spencer 1.052 vs Chen & Shao 1.05 (+0.2%) | the Prandtl surface is built analytically |
| [26](#vp26) | 🟢 | Bearing capacity test prism, homogenous, distributed load, predefined slip surface | Spencer 1.043 vs bearing-capacity theory 1.0 (+4.3%) · Lowe 1.017 vs bearing-capacity theory 1.0 (+1.7%) | the closed form is the reference authority; Slide2's own Spencer 0.941 sits ~6% below it |
| [27](#vp27) | 🟢 | Slope, (2) materials, tension crack, water table (auto Hu) | Spencer 1.375 vs Slide 1.402 (−1.9%) · Spencer 1.375 vs XSTABL 1.403 (−2.0%) | a uniform offset across all six methods (digitized water table) |
| [28](#vp28) | 🟢 | Excavated slope and embankment, (3) materials and (5) materials, probabilistic analysis | Congress St.: Bishop 1.129 vs Slide 1.128 (+0.1%) · embankment, interface: Bishop 1.158 vs Slide 1.160 (−0.2%) · embankment, base: Bishop 1.177 vs Slide 1.185 (−0.7%) | **built** (3 of 10 cases) |
| [29](#vp29) | 🟢 | Submerged slope, homogenous, probabilistic analysis, water table | Spencer 1.145 vs Slide 1.157 (−1.0%) · Spencer 1.145 vs Duncan 1.17 (−2.1%) |  |
| [30](#vp30) | 🟢 | Reinforced embankment, (4) materials, tension crack, geosynthetic | circle A: Bishop 1.679 vs Slide 1.69 (−0.7%) · circle B: Bishop 1.650 vs Slide 1.66 (−0.6%) | the manual specifies Bishop for this problem |
| [31](geostudio.md#gs-2-18) | 🟢 | Reinforced embankment, (5) materials, geosynthetic | M-P 1.153 vs SLOPE/W 1.171 (−1.5%) · M-P 1.153 vs Borges & Cardoso 1.15 (+0.3%) · Bishop 1.154 vs SLOPE/W 1.170 (−1.4%) | *covered* — Borges & Cardoso Case 2, built in the GeoStudio corpus as [SLOPE/W §2.18](geostudio.md#gs-2-18) (identical embankment c'=0, φ'=35, γ=20; soft-clay layers Clay1 33, Clay2 16, Clay3 16→18.4, Clay4 18.4→55.1, matching Slide2's Table 31.2 to rounding; unanchored 200 kN/m geosynthetic at δ=33.7°). Slide2's own Circle A/B read 1.18 / 1.16 (Borges 1.19 / 1.15); the VP30 reverse-curvature blocker does not arise here. |
| [32](#vp32) | 🟢 | Reinforced embankment, (7) materials, geosynthetic | H = 7, circle A: Bishop 1.218 vs Slide 1.23 (−1.0%) · circle B: Bishop 1.216 vs Slide 1.22 (−0.3%) · H = 8.75, circle C: Bishop 0.981 vs Slide 0.98 (+0.1%) |  |
| [33](#vp33) | 🟢 | Dike, (5) materials, probabilistic analysis, water table | Bishop 1.320 vs Slide 1.305 (+1.1%) · Bishop 1.320 vs El-Ramly et al. 1.31 (+0.8%) | **built** (deterministic); composite critical surface |
| [34](#vp34) | 🟢 | Dam, (3) materials, probabilistic analysis, water table | M-P 2.384 vs Wolff & Harr 2.36 (+1.0%) | deterministic lock; the Phase I COV of 124% is outside the Taylor series' domain |
| [35](#vp35) | 🟢 | Dam, (5) materials, probabilistic analysis, reliability index | Bishop critical FS at mean strengths 2.529 vs Slide 2.551 (−0.9%) | reproduced by procedure; β spreads with the estimator at these COVs · the paper's nine fixed surfaces are reproduced at [§2.22](geostudio.md#gs-2-22) |
| [36](#vp36) | 🟢 | Slope, homogenous, probabilistic analysis, ru pore pressure, reliability index | Bishop 1.333 vs H&W 1.334 (−0.1%) · Bishop 1.333 vs Slide 1.340 (−0.5%) |  |
| [37](#vp37) | 🟢 | Slope, homogenous, distributed load, back analysis of required support force and length | Bishop 0.764 vs Slide 0.764 (0.0%) · Bishop 0.764 vs XSTABL 0.734 (+4.1%) | **built** (base slope); the support-force back-analysis and reinforced-zone length are documented, not locked |
| [38](#vp38) | 🟢 | Excavated slope, homogenous, finite element groundwater seepage analysis, matric suction | H = 61: Bishop 1.612 vs Slide 1.621 (−0.6%) · H = 62: Bishop 1.533 vs Slide 1.538 (−0.3%) · H = 63: Bishop 1.413 vs Slide 1.407 (+0.4%) |  |
| [39](#vp39) | 🟢 | Reinforced embankment, (2) materials, tension crack, geosynthetic | clay fill: Spencer 0.968 vs Slide 0.975 (−0.7%) · sand fill: Spencer 1.200 vs Slide 1.209 (−0.7%) | **built** (circular cases); noncircular cases not locked |
| [40](#vp40) | 🟢 | Slope, homogenous, sensitivity analysis | Janbu(corr) 1.003 vs Perry 0.98 (+2.3%) | the A and b sensitivity sweeps track Slide's published curves within about a percent |
| [41](#vp41) | 🟢 | Slope, homogenous, ru pore pressure | Bishop 1.668 vs Slide 1.656 (+0.7%) · Bishop 1.668 vs Charles & Soares 1.66 (+0.5%) |  |
| [42](#vp42) | 🟢 | Dam, (3) materials, water table, ponded water, tension crack | Slide's circle: Spencer 1.926 vs Slide 1.925 (+0.1%) · Baker's noncircular: Spencer 1.882 vs Baker & Leshchinsky 1.91 (−1.5%) | the reservoir is carried as an explicit hydrostatic face load |
| [43](#vp43) | 🟢 | Slope, homogenous, planar surface, RocPlane comparison | Spencer 1.352 vs RocPlane 1.351 (+0.1%) · Spencer 1.352 vs SLOPE/W 1.352 (0.0%) | the SLOPE/W model pins the crest-offset geometry |
| [44](#vp44) | 🟢 | Slope, homogenous | power curve: Spencer 0.958 vs Slide 0.960 (−0.2%) · Mohr-Coulomb: Spencer 1.518 vs Slide 1.536 (−1.2%) · LLA converged: Spencer 0.980 vs Slide 0.981 (−0.1%) |  |
| [45](#vp45) | 🟢 | Slope, homogenous | Mohr-Coulomb: Spencer 2.801 vs Slide 2.794 (+0.3%) · power curve: Spencer 2.649 vs Slide 2.662 (−0.5%) |  |
| [46](#vp46) | 🟢 | Dam, (2) materials, rapid drawdown, FE seepage, ponded water | Stage 1: 2.50 vs closed form 2.50 (0.0%) · Stage 2: Spencer 7.086 vs Slide 7.003 (+1.2%) | **partial** (stages 1–2 built; stage 3 blocked — Baker publishes the undrained strength only as a contour figure). Baker's own values: 2.41 / 6.98 / 2.18. |
| [47](#vp47) | 🟢 | Retaining wall, homogenous, planar failure, line load, shotcrete, soil nails | Janbu 0.899 vs Slide 0.890 (+1.0%) · Janbu 0.899 vs Sheahan 0.887 (+1.4%) |  |
| [48](#vp48) | 🟢 | Retaining wall, homogenous, planar failure, line load , soil nails, shotcrete | 55° plane: Janbu 0.991 vs Slide 0.989 (+0.2%) · 55° plane: Janbu 0.991 vs Sheahan 0.989 (+0.2%) | Janbu/Spencer within 0.3% of Slide on the stored plane |
| [49](#vp49) | 🟢 | Retaining wall, (2) materials, grouted tiebacks, soldier piles | Janbu(corr) 1.469 vs Slide 1.479 (−0.7%) · Janbu(corr) 1.469 vs SNAILZ 1.52 (−3.4%) |  |
| [50](#vp50) | 🟢 | Reinforced slope, (2) materials, predefined slip surface, geosynthetic | Janbu(corr) 1.448 vs SNAILZ 1.46 (−0.8%) · Janbu(corr) 1.448 vs Slide 1.417 (+2.2%) |  |
| [51](#vp51) | 🟢 | Slope, (4) materials, water table, tension crack, seismic | Spencer 1.294 vs Slide 1.293 (+0.1%) · Spencer 1.294 vs Zhu 1.293 (+0.1%) | phreatic line calibrated to the agreeing published Bishop/Spencer values |
| [52](#vp52) | 🟢 | Slope, (4) materials, water table, tension crack | dry: Spencer 1.797 vs Slide 1.804 (−0.4%) · wet: Spencer 1.189 vs Slide 1.189 (0.0%) | the shallow/noncircular surfaces need constrained searches not yet exposed |
| [53](#vp53) | 🟢 | Slope, homogenous, water table, tension crack, planar failure, RocPlane comparison | all methods 1.048 vs Slide / RocPlane / Priest 1.049 (−0.1%) | on a single plane every method coincides |
| [54](#vp54) | 🟢 | Slope, homogenous, micro piles | no pile: Bishop 1.100 vs Slide 1.102 (−0.2%) · with pile: Bishop 1.185 vs Slide 1.193 (−0.7%) |  |
| [55](#vp55) | 🟢 | Slope, homogenous, water table | Spencer 1.297 vs Slide 1.300 (−0.2%) · Bishop 1.290 vs Slide 1.293 (−0.2%) |  |
| [56](#vp56) | 🟢 | Slope, homogenous, water table, tension crack | Spencer 1.288 vs Slide 1.290 (−0.2%) · Bishop 1.283 vs Slide 1.285 (−0.2%) |  |
| [57](#vp57) | 🟢 | Slope, (2) materials, water table, tension crack, composite surfaces | composite: Spencer 1.396 vs Slide 1.400 (−0.3%) · circles-only: Spencer 1.419 vs Slide 1.422 (−0.2%) |  |
| [58](#vp58) | 🟢 | Retaining wall, (8) materials, water table, grouted tieback | Spencer 1.140 vs Slide 1.145 (−0.4%) · Spencer 1.140 vs UTEXAS4 1.14 (0.0%) |  |
| [59](#vp59) | 🟢 | Retaining wall, homogenous, water table, grouted tieback | Corps / Lowe 0.577 vs Slide 0.588 (−1.9%) | **built** (Janbu/Corps); Spencer has no solution on this surface |
| [60](#vp60) | 🟢 | Retaining wall, (2) materials, tension crack, distributed load, soil nails | Spencer 1.010 vs Slide 1.009 (+0.1%) |  |
| [61](#vp61) | 🟢 | Slope, homogenous, composite surfaces | power curve: Spencer 1.466 vs Slide 1.468 (−0.1%) · Mohr-Coulomb: Spencer 1.367 vs Slide 1.366 (+0.1%) |  |
| [62](#vp62) | 🟢 | Slope, homogenous, ru pore pressure, seismic | dry, k<sub>c</sub> = 0.432: Spencer 1.001 vs Loukidis 1.000 (+0.1%) · r<sub>u</sub> = 0.5, k<sub>c</sub> = 0.132: Spencer 1.001 vs Loukidis 1.000 (+0.1%) | FS should be 1.0 at k<sub>c</sub> |
| [63](#vp63) | 🟢 | Slope, (3) materials, seismic | Spencer 1.001 vs Loukidis 1.000 (+0.1%) · Spencer 1.001 vs Slide 0.991 (+1.0%) | noncircular search at the paper's k<sub>c</sub> = 0.155 |
| [64](#vp64) | 🟢 | Embankment, (4) materials, water table, tension crack | Spencer 2.488 vs Slide 2.445 (+1.8%) · Spencer 2.488 vs USACE 2.44 (+2.0%) |  |
| [65](#vp65) | 🟢 | Embankment, (4) materials, water table, ponded water | Bishop 2.725 vs Slide 2.716 (+0.3%) · Spencer 2.748 vs Slide 2.736 (+0.4%) |  |
| [66](#vp66) | 🟢 | Embankment, (4) materials, water table, ponded water | Spencer 2.258 vs Slide 2.307 (−2.1%) · Spencer 2.258 vs USACE 2.30 (−1.8%) |  |
| [67](#vp67) | 🟢 | Embankment, (2) materials | Spencer 1.316 vs Slide 1.328 (−0.9%) · Spencer 1.316 vs USACE 1.33 (−1.1%) |  |
| [68](#vp68) | 🟢 | Embankment, (3) materials, ponded water | Bishop 1.234 vs Slide 1.241 (−0.6%) | Spencer's base-tension guard declines this surface |
| [69](#vp69) | 🟢 | Embankment, (2) materials, water table, ponded water | Spencer 2.013 vs Slide 2.026 (−0.6%) · Bishop 1.999 vs USACE 2.01 (−0.5%) |  |
| [70](#vp70) | 🟢 | Submerged slope, homogenous, water table, ponded water | pool +30 ft: Spencer 1.593 vs Slide 1.599 (−0.4%) · pool +60 ft: Spencer 1.593 vs Slide 1.599 (−0.4%) | identical FS at both pools — the depth-independence reproduces exactly |
| [71](#vp71) | 🟢 | Slope, homogenous, finite element groundwater seepage analysis, water table | FE seepage: Spencer 1.132 vs Slide 1.141 (−0.8%) · piezometric line: Spencer 1.132 vs Slide 1.142 (−0.9%) | the two pore-pressure models agree with each other |
| [72](#vp72) | 🟢 | Embankment dam, (4) materials, finite element groundwater seepage analysis, ponded water | FE seepage, tangent 197: Spencer 1.341 vs Slide 1.312 (+2.2%) · piezometric line: Spencer 1.563 vs Slide 1.557 (+0.4%) |  |
| [73](#vp73) | 🟢 | Excavated slope, (4) materials, tension crack | Spencer 1.766 vs Slide 1.758 (+0.5%) · Spencer 1.766 vs D&W 1.76 (+0.3%) |  |
| [74](#vp74) | 🟢 | Embankment, (2) materials | Spencer 1.194 vs Slide 1.201 (−0.6%) · Spencer 1.194 vs D&W 1.19 (+0.3%) |  |
| [75](#vp75) | 🟢 | Dyke, (4) materials | free search: Bishop 1.424 vs D&W 1.45 (−1.8%) | D&W report Bishop, so Bishop governs like-for-like |
| [76](#vp76) | 🟢 | Embankment dam, homogenous, finite element groundwater seepage analysis, ponded water | FE seepage: Spencer 1.072 vs Slide 1.075 (−0.3%) · piezometric line: Spencer 1.078 vs Slide 1.100 (−2.0%) | a shallow toe surface hypersensitive to the piezometric-line elevation; the line carries Slide2's own vertices |
| [77](#vp77) | 🟢 | Dam, (2) materials, finite element groundwater seepage analysis, ponded water | FE seepage: Spencer 1.724 vs Slide 1.724 (0.0%) · piezometric line: Spencer 1.659 vs Slide 1.648 (+0.7%) |  |
| [78](#vp78) | 🟢 | Slope, homogenous | Spencer 1.131 vs Slide 1.139 (−0.7%) · Bishop 1.117 vs D&W 1.124 (−0.6%) |  |
| [79](#vp79) | 🟢 | Slope, (2) materials, infinite slope failure | Spencer 1.397 vs Slide 1.400 (−0.2%) · Spencer 1.397 vs D&W 1.40 (−0.2%) |  |
| [80](#vp80) | 🟢 | Embankment, (6) materials | tangent 0 ft: Spencer 2.530 vs Slide 2.545 (−0.6%) · tangent 15 ft: Spencer 1.352 vs Slide 1.359 (−0.5%) |  |
| [81](#vp81) | 🟢 | Embankment, (2) materials, infinite slope failure | Spencer 1.204 vs Slide 1.209 (−0.4%) · Spencer 1.204 vs D&W 1.21 (−0.5%) |  |
| [82](#vp82) | 🟢 | Embankment, (2) materials, water table | Spencer 1.533 vs Slide 1.540 (−0.5%) · Bishop 1.521 vs D&W 1.535 (−0.9%) |  |
| [83](#vp83) | 🟢 | Embankment, (2) materials | profile I: Spencer 1.275 vs Slide 1.285 (−0.8%) · profile II: Spencer 1.326 vs Slide 1.330 (−0.3%) |  |
| [84](#vp84) | 🟢 | Embankment, (2) materials | c<sub>z</sub> = 0: Spencer 0.751 vs Slide 0.756 (−0.7%) · c<sub>z</sub> = 5: Spencer 0.897 vs Slide 0.898 (−0.1%) · c<sub>z</sub> = 10: Spencer 1.028 vs Slide 1.032 (−0.4%) · c<sub>z</sub> = 15: Spencer 1.131 vs Slide 1.134 (−0.3%) |  |
| [85](#vp85) | 🟢 | Reinforced slope, homogenous, grouted tieback | passive: Bishop 1.319 vs Slide 1.324 (−0.4%) · passive: Bishop 1.319 vs D&W 1.32 (−0.1%) | the active case pairs only against Slide's GLE 1.575, which is cross-method |
| [86](#vp86) | 🟢 | Reinforced slope, homogenous, grouted tieback | Spencer 1.611 vs Slide 1.620 (−0.6%) · Spencer 1.611 vs D&W 1.61 (+0.1%) |  |
| [87](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | Bishop 1.031 vs Slide 1.040 (−0.9%) |  |
| [88](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | Spencer 1.057 vs Slide 1.043 (+1.3%) |  |
| [89](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | at T<sub>a</sub> = 11.4: Spencer 1.011 vs L&H design intent 1.0 (+1.1%) | Slide's printed result uses the baseline T<sub>a</sub> = 10, so it is not on the same basis |
| [90](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | Bishop 1.012 vs Slide 1.004 (+0.8%) |  |
| [91](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | Spencer 0.960 vs Slide 0.964 (−0.4%) | deep bearing circle |
| [92](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | at T<sub>a</sub> = 9.25: Bishop 1.010 vs L&H 1.01 (0.0%) | Slide's printed result uses the baseline T<sub>a</sub> = 10, so it is not on the same basis |
| [93](#vp87) | 🟢 | Retaining wall, (3) materials, distributed load, geotextile | at T<sub>a</sub> = 10: Bishop 0.961 vs Slide 0.958 (+0.3%) | the locked run and Slide's printed result both use T<sub>a</sub> = 10 |
| [94](#vp87) | 🟢 | Retaining wall, (3) materials, geotextile | Bishop 1.020 vs Slide 1.040 (−1.9%) |  |
| [95](#vp95) | <span class="nodata">⊘</span> | Embankment dam, homogenous, rapid drawdown, water table |  | *not supported* — Corps 2-stage, superseded by the DWW 3-stage method XSLOPE implements |
| [96](#vp96) | 🟢 | Embankment dam, homogenous, rapid drawdown, water table | Spencer 1.434 vs Slide 1.443 (−0.6%) · Spencer 1.434 vs USACE 1.44 (−0.4%) | Duncan-Wright-Wong 3-stage |
| [97](#vp97) | 🟢 | Embankment dam, homogenous, rapid drawdown, water table | Spencer 1.044 vs Slide 1.043 (+0.1%) · Spencer 1.044 vs DWW 1.05 (−0.6%) |  |
| [98](#vp98) | 🟢 | Embankment dam, (5) materials, rapid drawdown, water table | Spencer 1.046 vs Slide 1.039 (+0.7%) · Spencer 1.046 vs DWW 1.04 (+0.6%) | DWW 3-stage |
| [99](#vp99) | 🟢 | Embankment dam, (3) materials, rapid drawdown, water table | Spencer 1.527 vs Slide 1.534 (−0.5%) · Spencer 1.527 vs DWW 1.56 (−2.1%) | geometry re-pinned from the vendor GeoStudio model |
| [100](#vp100) | 🟢 | Embankment dam, homogenous, rapid drawdown, water table | Bishop 1.201 vs Morgenstern chart 1.20 (+0.1%) · Bishop 1.201 vs Slide 1.212 (−0.9%) | runs single-stage |
| [101](#vp101) | 🟢 | Embankment dam, homogenous, rapid drawdown, water table | Bishop 1.416 vs Slide 1.417 (−0.1%) · Bishop 1.416 vs Morgenstern chart 1.41 (+0.4%) |  |
| [102](#vp102) | 🟢 | Embankment dam, homogenous, rapid drawdown | dry: Spencer 2.451 vs Slide 2.455 (−0.2%) · steady state (t = 0): Spencer 1.731 vs Slide 1.745 (−0.8%) · drawdown at 100 h: Spencer 1.814 vs Slide 1.867 (−2.8%) | the 100 h frame is the widest of the 60–1500 h transient series, which runs from −2.8% to +0.2% against the Slide2 Spencer column, and sets the dot. The unsaturated band width was tested as the cause of the early-frame shortfall and is worth a small fraction of it. |
| [103](#vp103) | 🟢 | Undrained slope, multi-model optimization (MMO) | deep, P = 1.4: Spencer 1.221 vs Slide2 1.215 (+0.5%) · P = 1.5: Spencer 1.298 vs Slide2 1.290 (+0.6%) · P = 1.6: Spencer 1.374 vs Slide2 1.366 (+0.6%) · shallow: Spencer 1.322 vs Slide2 1.324 (−0.2%) | **built** (4 files, both mechanisms); the deep→shallow switch lands in Slide2's own interval |
| [104](#vp104) | 🟢 | Newmark analysis, seismic analysis, multi-modal optimization (MMO) | no seismic: Spencer 1.372 vs Slide2 uni-modal 1.360 (+0.9%) · k = 0.15: Spencer 0.989 vs Slide2 uni-modal 0.980 (+0.9%) · K<sub>y</sub> 0.144 vs Slide2 uni-modal 0.140 (+2.9%) | **built** (3 of 4 scenarios); the Newmark displacement is reproduced by a benchmark diagnostic (−0.5% at Slide2's K<sub>y</sub>), not an XSLOPE mode |
| [105](#vp105) | <span class="nodata">⊘</span> | Anisotropic surface, multi-modal optimization (MMO) |  | *blocked* — needs an orientation-dependent strength model |
| [106](#vp106) | 🟢 | Support, Ito & Matsui pile | no pile: Bishop 1.143 vs Slide 1.14 (+0.3%) · D1/D = 2: Bishop 1.540 vs Slide 1.54 (0.0%) · D1/D = 3: Bishop 1.451 vs Slide 1.43 (+1.5%) · D1/D = 4: Bishop 1.341 vs Slide 1.33 (+0.8%) · D1/D = 6: Bishop 1.260 vs Slide 1.25 (+0.8%) | **built** (5 cases); the Ito & Matsui limit pressure is auto-computed. The paper's three-dimensional finite-element results are compared separately, as a [diagnostic of the 2D pile idealization](#vp106-fem) that carries no dot |
| [107](#vp107) | 🟢 | Retaining walls, gabion walls, supports | equivalent cohesion: Spencer 1.398 vs Slide 1.386 (+0.9%) · mesh supports: Spencer 1.398 vs Slide 1.392 (+0.4%) |  |
| [108](#vp108) | 🟢 | Retaining walls, gabion walls, supports | equivalent cohesion: Bishop 1.790 vs Slide 1.787 (+0.2%) · mesh: Bishop 1.830 vs Slide 1.835 (−0.3%) | Spencer within 0.3% on both |
| [109](#vp109) | 🟢 | Retaining walls, gabion walls, weak layers | Spencer 1.797 vs Slide's joint block search 1.803 (−0.3%) · Bishop 1.790 vs Slide 1.799 (−0.5%) | the joints do not govern overall stability |
| [110](#vp110) | <span class="nodata">⊘</span> | Retaining walls, equivalent fluid pressure |  | *blocked* — vendor tutorial file, no published properties or coordinates |
| [111](#vp111) | <span class="nodata">⊘</span> | Helical anchor | Slide's problem 111 verifies its helical-anchor capacity envelope, not a slope — there is no slope and no factor of safety to lock. Helically anchored slopes are analyzed in XSLOPE by entering the governing capacity as a standard anchor force — see the [worked note](#vp111). | *no lock possible* |

</div>

---

## 🟢 VP1: Slope, homogeneous (ACADS 1(a)) {#vp1}

The headline limit-equilibrium benchmark, from the ACADS slope stability program review
(Donald & Giam 1989; Giam & Donald 1992) as documented in the
[GeoStudio SLOPE/W Verification Manual (Oct 2022)](https://files.seequent.com/PDFs/Geostudio-Slope%20Stability%20Verification%20Manual-Oct2022.pdf):
a simple homogeneous slope analyzed with a circular search against the ACADS consensus answer.

| Property | Value |
|---|---|
| Slope | 2:1, 10 m high, with a bench |
| Cohesion, $c'$ | 3.0 kPa |
| Friction angle, $\phi'$ | 19.6° |
| Unit weight, $\gamma$ | 20.0 kN/m³ |
| Pore pressure | none (total stress) |

Excel input file: [xslope_acads_simple.xlsx](../lem/files/xslope_acads_simple.xlsx)

![xslope_acads_simple: inputs and representative solution](images/xslope_acads_simple.png)

XSLOPE results for all six methods (automated critical-circle search, 50
slices, each method searched independently):

| Method | XSLOPE FOS | ACADS |
|---|---|---|
| Ordinary (OMS) | 0.942 | 1.00 (−5.8%) |
| Bishop's Simplified | 0.985 | 1.00 (−1.5%) |
| Simplified Janbu | 0.986 | 1.00 (−1.4%) |
| Corps of Engineers | 0.990 | 1.00 (−1.0%) |
| Lowe & Karafiath | 0.987 | 1.00 (−1.3%) |
| Spencer | 0.984 | 1.00 (−1.6%) |
| Morgenstern-Price | 0.984 | 1.00 (−1.6%) |

All rigorous methods fall within the ACADS accepted band; the Ordinary method reads low, its
usual conservative bias on this class of problem.

<!-- fs-table -->
**Factor of safety by method** (each method's own critical surface):

| OMS | Bishop | Janbu | Corps | Lowe | Spencer | M-P |
|---:|---:|---:|---:|---:|---:|---:|
| 0.942 | 0.985 | 0.986 | 0.990 | 0.987 | 0.984 | 0.984 |
<!-- /fs-table -->

<!-- test: file=../lem/files/xslope_acads_simple.xlsx, type=circular_search, num_slices=50, fs_oms=0.942, fs_bishop=0.985, fs_janbu=0.986, fs_corps=0.990, fs_lowe=0.987, fs_spencer=0.984, fs_mprice=0.984, benchmark=LEM-1 -->

Also [SLOPE/W §2.1](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP2: Slope, homogenous, tension crack {#vp2}

ACADS 1(b) (Giam & Donald 1989): the 1(a) slope with c'=32, phi'=10, gamma=20 and a water-filled tension crack of depth 2c/(gamma*sqrt(ka)) [Craig 1997].

**Input files:** [vp002.xlsx](files/rocscience/vp002.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | Giam |
|---|---|---|---|---|
| Bishop | 1.589 | 1.596 (−0.4%) | 1.664 (−4.5%) | 1.65 (−3.7%) |
| Janbu (corrected) | 1.481 | 1.489 (−0.5%) | — | 1.65 (−10.2%) |
| Spencer | 1.585 | 1.592 (−0.4%) | — | 1.65 (−3.9%) |
| Morgenstern-Price | 1.586 | — | 1.660 (−4.5%) | 1.65 (−3.9%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 1.592 | — | — |
| ACADS reference band | — | — | — | 1.65–1.70 |

![vp002: inputs and representative solution](images/vp002.png)

Also [SLOPE/W §2.2](geostudio.md) — the same problem in the GeoStudio corpus.


## 🟢 VP3: Slope, (3) materials {#vp3}

ACADS 1(c): a non-homogeneous three-layer slope, solved on its critical circle.

**Input files:** [vp003.xlsx](files/rocscience/vp003.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | ACADS |
|---|---|---|---|---|
| Bishop | 1.403 | 1.405 (−0.1%) | 1.414 (−0.8%) | 1.39 (+0.9%) |
| Janbu (corrected) | 1.354 | 1.357 (−0.2%) | — | 1.39 (−2.6%) |
| Spencer | 1.372 | 1.375 (−0.2%) | — | 1.39 (−1.3%) |
| Morgenstern-Price | 1.371 | — | 1.382 (−0.8%) | 1.39 (−1.4%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 1.374 | — | — |

![vp003: inputs and representative solution](images/vp003.png)

Interface coordinates are read from the labeled GeoStudio verification-manual figure. Also [SLOPE/W §2.3](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP4: Slope, (3) materials, seismic {#vp4}

ACADS 1(d): the problem #3 slope with a horizontal seismic coefficient of 0.15.

**Input files:** [vp004.xlsx](files/rocscience/vp004.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | ACADS |
|---|---|---|---|---|
| Bishop | 1.013 | 1.016 (−0.3%) | 1.02 (−0.7%) | 1.00 (+1.3%) |
| Janbu (corrected) | 0.963 | 0.965 (−0.2%) | — | 1.00 (−3.7%) |
| Spencer | 0.989 | 0.991 (−0.2%) | — | 1.00 (−1.1%) |
| Morgenstern-Price | 0.987 | — | 0.989 (−0.2%) | 1.00 (−1.3%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 0.989 | — | — |

![vp004: inputs and representative solution](images/vp004.png)

Also [SLOPE/W §2.4](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP5: Dam, (4) materials {#vp5}

ACADS 2(a) (Giam & Donald 1989): Talbingo Dam at end of construction, 4 zones, solved on its critical circular surface. The minimum is a shallow slide parallel to the (steeper) upstream face.

**Input files:** [vp005.xlsx](files/rocscience/vp005.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | Giam | Infinite-slope limit |
|---|---|---|---|---|---|
| Bishop | 1.955 | 1.948 (+0.4%) | 1.951 (+0.2%) | 1.95 (+0.3%) | 1.9475 (+0.4%) |
| Janbu (corrected) | 1.965 | 1.949 (+0.8%) | — | 1.95 (+0.8%) | 1.9475 (+0.9%) |
| Spencer | 1.955 | 1.948 (+0.4%) | — | 1.95 (+0.3%) | 1.9475 (+0.4%) |
| Morgenstern-Price | 1.955 | — | — | 1.95 (+0.3%) | 1.9475 (+0.4%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 1.948 | — | — | — |

*The critical mechanism is the infinite-slope limit tan φ′/tan β on the upstream face, which is the closed-form column above.*

![vp005: inputs and representative solution](images/vp005.png)

The section is entered as polygon material zones. Also [SLOPE/W §2.5](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP6: Dam, (4) materials, predefined slip surface {#vp6}

ACADS 2(b): Talbingo Dam on the single specified circle Xc=100.3, Yc=291.0, R=278.8 (Table 6.1).

**Input files:** [vp006.xlsx](files/rocscience/vp006.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | Giam |
|---|---|---|---|---|
| Bishop | 2.206 | 2.208 (−0.1%) | 2.207 (0.0%) | 2.29 (−3.7%) |
| Janbu (corrected) | 2.073 | 2.073 (0.0%) | — | 2.29 (−9.5%) |
| Spencer | 2.290 | 2.292 (−0.1%) | — | 2.29 (0.0%) |
| Morgenstern-Price | 2.299 | — | 2.299 (0.0%) | 2.29 (+0.4%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 2.301 | — | — |

![vp006: inputs and representative solution](images/vp006.png)

Also [SLOPE/W §2.6](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP8: Slope, (2) materials, weak layer, predefined slip surface {#vp8}

ACADS 3(b): the weak-layer slope (= LEM sample 13 / Slide #7) evaluated on the fully specified non-circular surface of Table 8.2.

**Input files:** [vp008.xlsx](files/rocscience/vp008.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | Giam |
|---|---|---|---|---|
| Janbu (corrected) | 1.294 | 1.294 (0.0%) | — | 1.34 (−3.4%) |
| Spencer | 1.276 | 1.277 (−0.1%) | — | 1.34 (−4.8%) |
| Morgenstern-Price | 1.260 | — | 1.261 (−0.1%) | 1.34 (−6.0%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 1.262 | — | — |
| SLOPE/W Bishop — not run by XSLOPE on this specified surface | — | — | 1.259 | — |

![vp008: inputs and representative solution](images/vp008.png)

Table 8.2's specified surface is a 4-point polyline. Also [SLOPE/W §2.8](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP9: Slope, (2) materials, weak layer, water table, distributed load {#vp9}

ACADS 4 (Slide #9): weak-layer slope + piezometric surface (Table 9.3) + two surcharge strips (Table 9.2: 20 kPa on the lower bench x=23-43, 20->40 kPa ramp on the crest x=70-80), solved by non-circular search. The published spread is wide — this is a search-difficulty benchmark.

**Input files:** [vp009.xlsx](files/rocscience/vp009.xlsx)

| Method | XSLOPE | Slide (block search) | Slide (optimized) | SLOPE/W | Giam |
|---|---|---|---|---|---|
| Janbu (corrected) | 0.718 | 0.734 (−2.2%) | — | — | 0.78 (−7.9%) |
| Spencer | 0.724 | 0.760 (−4.7%) | 0.707 (+2.4%) | — | 0.78 (−7.2%) |
| Bishop — not run by XSLOPE on this surface | — | — | — | 0.699 | — |
| Morgenstern-Price — not run by XSLOPE on this surface | — | — | — | 0.689 | — |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 0.720 | — | — | — |
| Slide's optimized band | — | — | 0.683–0.707 | — | — |
| ACADS: Slope 2000 (GLE — cross-method) / 20-program mean | — | — | — | — | 0.6878 / 0.808 |

![vp009: inputs and representative solution](images/vp009.png)

The weak seam is 0.6 m thick and inclined, the piezometric line has 8 points, and the geometry is read from the labeled GeoStudio figure. Also [SLOPE/W §2.9](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP10: Slope, homogenous, pore pressure grid, ponded water {#vp10}

**Input files:** [vp010.xlsx](files/rocscience/vp010.xlsx) (+ seepage sidecars)

ACADS problem #5 (Giam & Donald 1989): a slope excavated at 1:2 below initially horizontal
ground, analyzed for the long-term condition with 1 m of ponded water over the excavation floor.
Slide interpolates a pore-pressure grid digitized from the survey's flow net; XSLOPE solves the
seepage problem itself (specified head 26 on the submerged boundary, the labeled far-field water
table as head 32 on the right edge, a seepage exit face above the waterline). In a homogeneous
steady problem the head field is independent of conductivity, so those boundary conditions
determine it completely, and the solved phreatic surface matches the manual's Figure 10.2 flow
net within about 0.1 m across the section.

| Method | XSLOPE (FE seepage) | Slide (grid) | ACADS reference | ACADS survey mean |
|---|---|---|---|---|
| Bishop | 1.500 | 1.498 (+0.1%) | 1.53 (−2.0%) | 1.464 (+2.5%) |
| Spencer | 1.501 | 1.500 (+0.1%) | 1.53 (−1.9%) | 1.464 (+2.5%) |
| Janbu corrected | 1.457 | 1.457 (0.0%) | 1.53 (−4.8%) | 1.464 (−0.5%) |

![vp010: inputs and representative solution](images/vp010.png)

## ⊘ VP11: Saint-Alban test embankment — measured pore-pressure grid {#vp11}

Slide #11 is the Saint-Alban test embankment (Pilot et al. 1982), a two-material
section built on soft clay and loaded until it failed. The manual supplies its pore
pressures as a grid of values interpolated from the isobars the paper prints.

Those isobars are **construction-induced excess pore pressures** — the undrained response of
the foundation clay to the fill placed on it, recorded by piezometer as the embankment was
raised. No steady or transient flow field generates that pattern, so no flow solution can
regenerate it. XSLOPE takes water three ways — a piezometric line, an r<sub>u</sub> coefficient,
or a finite-element seepage solution — each of which describes a pressure field with a physical
model behind it, and carries no pore-pressure-grid input. There is therefore no reproducible
numeric target here and no factor of safety to lock. The same reasoning applies to
[VP12](#vp12) and [VP13](#vp13); every other water problem in this corpus is built.

## ⊘ VP12: Lanester test embankment — measured pore-pressure grid {#vp12}

Slide #12 is the Lanester test embankment: four materials, a tension crack, and the same class
of input as [VP11](#vp11) — a printed 22-point pore-pressure grid recording measured
loading-induced pressure rather than a flow field. No factor of safety is locked.

Also [SLOPE/W §2.10](geostudio.md) — the same problem in the GeoStudio corpus.

## ⊘ VP13: Cubzac-les-Ponts test embankment — measured pore-pressure grid {#vp13}

Slide #13 is the Cubzac-les-Ponts test embankment, three materials on a soft foundation, in the
same position as [VP11](#vp11) and [VP12](#vp12): the manual's pore pressures are measured
construction-induced values interpolated from the source's isobars, not a solved flow field, so
no factor of safety is locked.

## 🟢 VP14: Slope, homogeneous (Arai & Tagyo ex. 1) {#vp14}

From [Arai & Tagyo (1985)](https://doi.org/10.3208/sandf1972.25.43), *Soils
and Foundations* 25(1), and republished by Greco (1996), Malkawi et al.
(2001), and [Kim et al. (2002)](https://doi.org/10.1061/(ASCE)1090-0241(2002)128:7(546)); also
[SLOPE/W Verification Manual](https://files.seequent.com/PDFs/Geostudio-Slope%20Stability%20Verification%20Manual-Oct2022.pdf)
sec. 2.11. A homogeneous 1.5:1 slope, 20 m high, with
c = 41.65 kPa, φ = 15.0°, γ = 18.82 kN/m³ (total stress).

Excel input file: [xslope_arai_tagyo.xlsx](../lem/files/xslope_arai_tagyo.xlsx)

![xslope_arai_tagyo: inputs and representative solution](images/xslope_arai_tagyo.png)

Results for all six methods (automated critical-circle search, 50 slices):

| Method | XSLOPE FOS | SLOPE/W | Arai & Tagyo |
|---|---|---|---|
| Ordinary (OMS) | 1.344 | — | 1.451 (−7.4%) |
| Bishop's Simplified | 1.404 | 1.417 (−0.9%) | 1.451 (−3.2%) |
| Simplified Janbu | 1.411 | — | 1.451 (−2.8%) |
| Corps of Engineers | 1.476 | — | 1.451 (+1.7%) |
| Lowe & Karafiath | 1.438 | — | 1.451 (−0.9%) |
| Spencer | 1.401 | — | 1.451 (−3.4%) |
| Morgenstern-Price | 1.400 | 1.414 (−1.0%) | 1.451 (−3.5%) |

SLOPE/W publishes only Bishop and Morgenstern-Price for this problem, in its §2.11; the
remaining methods are compared against the Arai & Tagyo reference alone. The same two pairings
are tabulated at [SLOPE/W §2.11](geostudio.md#gs-2-11).

<!-- fs-table -->
**Factor of safety by method** (each method's own critical surface):

| OMS | Bishop | Janbu | Corps | Lowe | Spencer | M-P |
|---:|---:|---:|---:|---:|---:|---:|
| 1.344 | 1.404 | 1.411 | 1.476 | 1.438 | 1.401 | 1.400 |
<!-- /fs-table -->

<!-- test: file=../lem/files/xslope_arai_tagyo.xlsx, type=circular_search, num_slices=50, fs_oms=1.344, fs_bishop=1.404, fs_janbu=1.411, fs_corps=1.476, fs_lowe=1.438, fs_spencer=1.401, fs_mprice=1.400, benchmark=LEM-2b -->

Also [SLOPE/W §2.11](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP15: Slope, (3) materials, weak layer {#vp15}

Slide #15: Arai & Tagyo (1985) example 2 — three layers with a weak (c=9.8, phi=5) middle band and no water, solved by circular search. Slide2's values come from its auto-refine search.

**Input files:** [vp015.xlsx](files/rocscience/vp015.xlsx)

| Method | XSLOPE | Slide | A&T | Kim et al. (2002) |
|---|---|---|---|---|
| Bishop | 0.419 | 0.420 (−0.2%) | 0.417 (+0.5%) | — |
| Janbu (corrected) | 0.436 | 0.423 (+3.1%) | 0.430 (+1.4%) | — |
| Spencer | 0.422 | 0.409 (+3.2%) | — | 0.43 (−1.9%) |
| Morgenstern-Price | 0.420 | — | — | — |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 0.437 | — | — |

*Kim et al. state no method, so their 0.43 is a headline factor of safety and pairs with
Spencer under the fallback rule. A&T report Bishop; the A&T Janbu (corrected) entry 0.430
is the attribution this page has always carried and is not independently confirmed here.*

![vp015: inputs and representative solution](images/vp015.png)


## 🟢 VP16: Slope, homogenous, water table {#vp16}

Slide #16: Arai & Tagyo (1985) example 3 — a homogeneous slope with a water table, solved by circular search (Slide2 runs it with auto refine).

**Input files:** [vp016.xlsx](files/rocscience/vp016.xlsx)

| Method | XSLOPE | Slide | A&T | SLOPE/W |
|---|---|---|---|---|
| Bishop | 1.112 | 1.118 (−0.5%) | 1.138 (−2.3%) | 1.190 (−6.6%) |
| Janbu (corrected) | 1.122 | 1.131 (−0.8%) | — | — |
| Spencer | 1.113 | 1.118 (−0.4%) | — | — |
| Morgenstern-Price | 1.111 | — | — | — |
| Janbu (simplified) — cross-method, XSLOPE reports the f₀-corrected value | — | 1.046 | — | — |

*SLOPE/W's Bishop is the outlier of the four sources.*

![vp016: inputs and representative solution](images/vp016.png)

Also [SLOPE/W §2.12](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP17: Slope, homogenous {#vp17}

Slide #17: the Yamagami & Ueta (1988) homogeneous dry slope, solved by circular search.

**Input files:** [vp017.xlsx](files/rocscience/vp017.xlsx)

| Method | XSLOPE | Slide | Y&U |
|---|---|---|---|
| Ordinary | 1.274 | 1.278 (−0.3%) | 1.282 (−0.6%) |
| Bishop | 1.342 | 1.344 (−0.1%) | 1.348 (−0.4%) |
| Spencer | 1.340 | — | — |

*Slide, Yamagami & Ueta and Greco all report Spencer on a non-circular surface, so the
circular Spencer value has no published counterpart; XSLOPE's local non-circular search
plateaus above every published optimized surface, as at [VP19](#vp19)/[VP20](#vp20).*

![vp017: inputs and representative solution](images/vp017.png)

## 🟢 VP18: Slope, homogenous slope, ru pore pressure {#vp18}

Slide #18: Spencer (1969) / Baker (1980) homogeneous slope with ru=0.5, non-circular critical surface. The slope descends left-to-right (a right-facing case). Slide2 solves it with a random search plus Monte-Carlo optimization.

**Input files:** [vp018.xlsx](files/rocscience/vp018.xlsx)

| Method | XSLOPE | Slide (MC-optimized) | Baker | Spencer (1969) |
|---|---|---|---|---|
| Spencer | 1.033 | 1.010 (+2.3%) | 1.02 (+1.3%) | 1.08 (−4.4%) |
| Morgenstern-Price | 1.024 | — | — | — |

![vp018: inputs and representative solution](images/vp018.png)

## 🟢 VP19: Slope, (4) materials {#vp19}

Slide #19: Greco (1996) ex. 4 / Yamagami & Ueta (1988) four-layer slope, no water, non-circular critical surface. Slide2 solves it with a random search plus Monte-Carlo optimization, restricted to convex surfaces.

**Input files:** [vp019.xlsx](files/rocscience/vp019.xlsx)

| Method | XSLOPE | Slide (MC) | Greco (published band) |
|---|---|---|---|
| Bishop | 1.448 | — | — |
| Spencer | 1.429 | 1.398 (+2.2%) | 1.40–1.42 |

*Circular-search values; the local non-circular search plateaus ~1.45 (search-power gap).*

![vp019: inputs and representative solution](images/vp019.png)

Also [SLOPE/W §2.13](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP20: Slope, (4) materials, weak layer, water table {#vp20}

Slide #20: Greco (1996) ex. 5 / Chen & Shao (1988): four layers with a 0.5 m weak seam along the inclined model base, water table. Polygon-zone geometry (the base is not horizontal). Slide2 runs the problem twice — a circular toe-focus grid search, and a non-circular block search in the seam with Monte-Carlo optimization.

**Input files:** [vp020.xlsx](files/rocscience/vp020.xlsx)

*Circular (toe-focus grid)*

| Method | XSLOPE | Slide | Greco |
|---|---|---|---|
| Bishop | 1.086 | 1.087 (−0.1%) | — |
| Spencer | 1.091 | 1.093 (−0.2%) | 1.08 (+1.0%) |

*Non-circular seam block*

| Method | XSLOPE (local search) | Slide (block search + MC) | Chen & Shao (published band) | Greco (published band) |
|---|---|---|---|---|
| Spencer | 1.082 | 1.010 (+7.1%) | 1.01–1.03 | 0.973–1.1 |

![vp020: inputs and representative solution](images/vp020.png)

Also [SLOPE/W §2.14](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP21: Slope, homogeneous, r<sub>u</sub> pore pressure (Fredlund & Krahn 1977) {#vp21}

Slide #21: Fredlund & Krahn (1977)'s classic homogeneous slope — the reference
problem that [VP22](#vp22) extends with a weak seam. A single fixed circle,
center (120, 90), R = 80, in imperial units, solved for all three of F&K's
pore-pressure cases: dry, r<sub>u</sub> = 0.25, and a piezometric water table.
F&K published all four method values for every case.

**Input files:** [vp021a.xlsx](files/rocscience/vp021a.xlsx) (dry),
[vp021b.xlsx](files/rocscience/vp021b.xlsx) (r<sub>u</sub> = 0.25),
[vp021c.xlsx](files/rocscience/vp021c.xlsx) (water table)

| Method | XSLOPE (dry) | F&K (dry) | XSLOPE (r<sub>u</sub>) | F&K (r<sub>u</sub>) | Slide (r<sub>u</sub>) |
|---|---|---|---|---|---|
| Ordinary | 1.927 | 1.928 (−0.1%) | 1.606 | 1.607 (−0.1%) | 1.687 (−4.8%) |
| Bishop | 2.075 | 2.080 (−0.2%) | 1.759 | 1.766 (−0.4%) | — |
| Spencer | 2.071 | 2.073 (−0.1%) | 1.757 | 1.761 (−0.2%) | — |
| Morgenstern–Price | 2.071 | 2.076 (−0.2%) | 1.756 | 1.764 (−0.5%) | — |

Case 3 adds F&K's piezometric line — (0, 40) — (140, 20) — (180, 20), read verbatim from
the `piezos` block of the vendor RS2 "Slide2 Import" of Slide #21.

| Method | XSLOPE (water table) | F&K | Slide |
|---|---|---|---|
| Ordinary | 1.693 | 1.693 (0.0%) | 1.716 (−1.3%) |
| Bishop | 1.829 | 1.834 (−0.3%) | 1.833 (−0.2%) |
| Spencer | 1.827 | 1.830 (−0.2%) | 1.831 (−0.2%) |
| Morgenstern–Price | 1.826 | 1.832 (−0.3%) | 1.831 (−0.3%) |

*XSLOPE reproduces Fredlund & Krahn's own Ordinary-method value in both water cases where
Slide reads several points off it; the rigorous methods agree with both sources to within
0.006.*

![vp021a: inputs and representative solution](images/vp021a.png)
![vp021b: inputs and representative solution](images/vp021b.png)
![vp021c: inputs and representative solution](images/vp021c.png)

## 🟢 VP22: Slope, (2) materials, weak layer, composite surface {#vp22}

Slide #22: the Fredlund & Krahn (1977) slope of #21 with a 1-ft weak seam (c'=0, φ'=10°) between el. 16 and the impenetrable base at el. 15. This is the corpus's **composite-surface** benchmark. F&K's circle — center (120, 90), R = 80 — bottoms out at el. 10, five feet *below* the base, so it cannot be used as a circle at all: the slip surface descends on the arc until it meets the base, runs horizontally along the weak seam, and climbs back out on the arc. Here 30 of the 59 slices sit on the seam.

Two cases: dry, and r<sub>u</sub> = 0.25 in both materials.

**Input files:** [vp022a.xlsx](files/rocscience/vp022a.xlsx) (dry), [vp022b.xlsx](files/rocscience/vp022b.xlsx) (r<sub>u</sub> = 0.25)

| Method | XSLOPE (dry) | Slide (dry) | F&K (dry) | XSLOPE (r<sub>u</sub>) | Slide (r<sub>u</sub>) | F&K (r<sub>u</sub>) |
|---|---|---|---|---|---|---|
| Ordinary | 1.297 | 1.300 (−0.2%) | 1.288 (+0.7%) | 1.037 | 1.121 (−7.5%) | 1.029 (+0.8%) |
| Bishop | 1.380 | 1.382 (−0.1%) | 1.377 (+0.2%) | 1.121 | 1.124 (−0.3%) | 1.124 (−0.3%) |
| Spencer | 1.379 | 1.382 (−0.2%) | 1.373 (+0.4%) | 1.122 | 1.124 (−0.2%) | 1.118 (+0.4%) |
| Morgenstern–Price | 1.370 | 1.372 (GLE — cross-method) | 1.370 (0.0%) | 1.112 | 1.114 (GLE — cross-method) | 1.118 (−0.5%) |

*Every method agrees with Slide to within 0.004 except the Ordinary method with r<sub>u</sub>, where XSLOPE reproduces Fredlund & Krahn's own published value rather than Slide's. The published values themselves split there: the Ordinary normal force N′ = W·cosα − u·Δℓ comes from equilibrium perpendicular to the base, which on the near-horizontal seam drives it far down.*

![vp022a: inputs and representative solution](images/vp022a.png)
![vp022b: inputs and representative solution](images/vp022b.png)

## 🟢 VP23: Slope, (3) materials {#vp23}

Slide #23 / Low (1989): a stiff upper slope (c = 95 kPa, φ = 15°) standing on two
soft undrained clays, γ = 20 kN/m³ throughout — the middle layer a constant
cu = 15 kPa, and the lowest gaining strength linearly from 15 kPa at its top
(y = 4) to 30 kPa at the model base (xslope `cp` option:
Su = c + cp·(r_elev − y)). Circular search. Slide takes this problem and
[#24](#vp24) from Low's examples; the Kim column is Kim, Salgado & Lee (2002)'s
finite-element limit analysis of the same section.

**Input files:** [vp023.xlsx](files/rocscience/vp023.xlsx)

| Method | XSLOPE | Slide | Low | Kim |
|---|---|---|---|---|
| Ordinary | 1.357 | 1.370 (−0.9%) | 1.36 (−0.2%) | — |
| Bishop | 1.130 | 1.192 (−5.2%) | 1.14 (−0.9%) | 1.17 (−3.4%) |

*The Bishop spread on this deep φ = 0 problem is not a surface disagreement: the two
searches settle on the same center (XSLOPE (18.00, 16.04), Slide (18.001, 16.000)). The
outlier is Slide's own Bishop, 1.192 against the Low 1.14 its manual cites (+4.6%).*

![vp023: inputs and representative solution](images/vp023.png)

## 🟢 VP24: Slope, (3) materials {#vp24}

Slide #24 / Low (1989), the companion example to [#23](#vp23): a three-layer
undrained slope, φ = 0 and γ = 18 kN/m³ throughout, with cu = 30 kPa in the
upper layer, 20 kPa in the middle band, and 150 kPa in the stiff bottom layer.
Circular search. On a φ = 0 section the Ordinary and Bishop methods coincide,
and Low's published 1.44 is the same for both.

**Input files:** [vp024.xlsx](files/rocscience/vp024.xlsx)

| Method | XSLOPE | Slide | Low |
|---|---|---|---|
| Ordinary | 1.435 | 1.439 (−0.3%) | 1.44 (−0.3%) |
| Bishop | 1.435 | 1.439 (−0.3%) | 1.44 (−0.3%) |

*Geometry follows the RS2 vendor `.fez`: three equal 4.5 m layers (crest y = 13.5, bench
y = 7.5, slope break x = 33.5).*

![vp024: inputs and representative solution](images/vp024.png)

## 🟢 VP25: Prandtl bearing mechanism on a 60° slope (Chen & Shao 1988) {#vp25}

Slide #25 / Chen & Shao (1988): the classical plasticity problem — a weightless, frictionless 10-m slope at 60° (c = 49 kPa, γ = 10⁻⁶) loaded by the critical strip load q = 149.31 kPa over 10 m of crest, evaluated on the Prandtl slip surface (theoretical FS = 1.0). The surface is built analytically: a 45° active wedge from the load's right edge, a circular fan of radius 10/√2 centered on the load's left edge (tangent to both straight segments), and an exit through the face at Slide's printed endpoint (0.773, 1.340).

**Input files:** [vp025.xlsx](files/rocscience/vp025.xlsx)

| Method | XSLOPE | Slide | Chen & Shao | Theory |
|---|---|---|---|---|
| Spencer | 1.052 | 1.051 (+0.1%) | 1.05 (+0.2%) | 1.0 (+5.2%) |

![vp025: inputs and representative solution](images/vp025.png)

Also [SLOPE/W §2.15](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP26: Prandtl bearing mechanism on level ground {#vp26}

Slide #26: the classical Prandtl footing problem — a weightless c = 20 soil (γ = 10⁻⁶,
φ = 0) on **level ground**, loaded by a strip UDL of **102.83** over the crest. That load
is exactly the ultimate bearing capacity c·N<sub>c</sub> = 20·(2 + π) = 102.83, so the
theoretical factor of safety is **1.0** by construction. The evaluation runs on the printed
Prandtl surface (an active wedge, a logarithmic-spiral/circular fan, and a passive wedge),
extracted with its end segments extended past the ground line.

It is the corpus's canonical **level-ground bearing** problem: both ground crossings sit at
the same elevation, and because the surface is symmetric the facing is set by the load
through the `right_facing` override.

**Input files:** [vp026.xlsx](files/rocscience/vp026.xlsx)

| Method | XSLOPE | Theory | Slide2 |
|---|---|---|---|
| Spencer | **1.043** | 1.0 (+4.3%) | 0.941 (+10.8%) |

XSLOPE's methods bracket the exact theory value, with Spencer at 1.043; Slide2 reads 0.941,
−5.9% against theory. The gap is an interslice-convention difference on this degenerate
flat-ground mechanism rather than a discretization artifact: Spencer is stable from 8 to 200
slices, and densifying the analytic arc moves it *away* from Slide, toward theory. The RS2
strength-reduction rendition of the same problem (RS2-21) converges on the theory value from
the continuum side. Also [SLOPE/W §2.16](geostudio.md) — the same Prandtl problem in the
GeoStudio corpus.

## 🟢 VP27: XSTABL slope with undulating bedrock and auto-Hu pore pressures {#vp27}

Slide #27 / XSTABL v5 reference manual (Sharma 1996), via Malkawi et al. (2001): a two-material slope over undulating bedrock, a zero-strength cap layer and a water table, with soil 1 carrying distinct moist/saturated unit weights (116.4/124.2 pcf). Slide and XSTABL both apply the phreatic-inclination correction, which XSLOPE selects with the piezometric-line **Type** flag (`piezo` | `phreatic`). Evaluated on the specified circle (59.52, 219.21, R=157.68); every geometry vertex is labeled in Slide's figure and the water table was pixel-traced to ±2 ft.

**Input files:** [vp027.xlsx](files/rocscience/vp027.xlsx)

| Method | XSLOPE (phreatic Type) | Slide | XSTABL |
|---|---|---|---|
| Bishop | 1.369 | 1.396 (−1.9%) | 1.397 (−2.0%) |
| Janbu | 1.365 | 1.391 (−1.9%) | 1.392 (−1.9%) |
| Spencer | 1.375 | 1.402 (−1.9%) | 1.403 (−2.0%) |
| Morgenstern-Price | 1.371 | 1.398 (−1.9%) | 1.399 (−2.0%) |
| Corps #2 | 1.388 | 1.414 (−1.8%) | 1.416 (−2.0%) |
| Lowe & Karafiath | 1.386 | 1.411 (−1.8%) | 1.413 (−1.9%) |

*A uniform −1.9% across all six methods (−3.0% with the plain static-head `u=piezo`), consistent with a small systematic difference in the digitized water table rather than any method-level disagreement — the method-to-method spread matches Slide/XSTABL exactly. The manual's tension-crack variants (analyses 3–4) are not built.*

![vp027: inputs and representative solution](images/vp027.png)

## 🟢 VP28: Excavated slope and embankment, probabilistic analysis {#vp28}

**Input files:** [vp028a.xlsx](files/rocscience/vp028a.xlsx) (Congress St. Cut, shallow
mode) · [vp028b.xlsx](files/rocscience/vp028b.xlsx) (embankment, interface mode) ·
[vp028c.xlsx](files/rocscience/vp028c.xlsx) (embankment, deep mode)

Chowdhury & Xu (1995) evaluate probabilities of failure for two slopes: the Congress
Street Cut (Ireland 1954) — three frictionless clays under a sand cap whose strength is
excluded — and an embankment on a soft clay foundation, each with slip circles tangent to
two different layer boundaries. Slide's manual prints the critical circle (center and
radius) for every case; those circles are evaluated here as fixed surfaces with Bishop's
method, and reliability uses the Taylor-series procedure on the same surfaces.

| Case | XSLOPE FS | Slide FS | C&X FS | XSLOPE TSPM β_ln / PF | XSLOPE MC β_ln / PF | Slide RI_ln / MC PF (cross-estimator) | C&X PF (cross-estimator) |
|---|---|---|---|---|---|---|---|
| Congress St., tangent clay-2 base | 1.129 | 1.128 (+0.1%) | 1.128 (+0.1%) | 0.768 / 22.1% | 0.774 / 21.5% | 0.650 / 24.6% | 26.6% |
| Embankment, tangent interface | 1.158 | 1.160 (−0.2%) | 1.1625 (−0.4%) | 0.787 / 21.6% | 0.800 / 20.6% | 0.799 / 21.2% | 20.2% |
| Embankment, tangent foundation base | 1.177 | 1.185 (−0.7%) | 1.1479 (+2.5%) | 0.798 / 21.2% | 0.789 / 20.9% | 0.820 / 19.9% | 19.7% |

The **XSLOPE MC** column is a 10,000-sample Monte Carlo run on the same fixed circles and
the same normal input distributions the Taylor series uses, seeded so the values are
regression-locked. Given identical inputs the two estimators land on top of each other,
within ±0.015 of β_ln on all three cases.

*Input provenance.* C&X's paper states no unit weights, so the manual notes Rocscience chose the
clay unit weights to reproduce the published deterministic factor of safety. The Seequent `.gsz`
for this problem (SLOPE/W [§2.17](geostudio.md)) carries the values SLOPE/W actually used — sand
cap γ = 21, all three Congress-St. clays γ = 22, and, below clay-3 where the Slide manual is
silent, a `bed` unit at c′ = 200 / φ′ = 35° — and enters every cohesion σ as C&X's own published
per-material statistic. Two things follow: the embankment (Example 5) is fully specified there
(fill c′ = 10 / φ′ = 12° / γ = 20, foundation clay c′ = 40 / φ′ = 0 / γ = 18 over bedrock), which
is what vp028b/c carry; and the deep circle is tangent to the clay-3 base at el. −12.19, so it
rides that contact with the strong `bed` untouched.

The `.gsz` also holds SLOPE/W's own solved factors of safety and probabilities of failure for all
ten of C&X's cases, which XSLOPE reproduces on the identical imported circles with the vendor σ's.
Those runs re-exercise the mechanism the three locks above already cover, so they are read at
[SLOPE/W §2.17](geostudio.md) rather than locked again here; they also settle where the
cross-source scatter in σ_F comes from, since on SLOPE/W's searched circle the same Taylor series
lands on SLOPE/W's Monte Carlo.

![vp028a: inputs and representative solution](images/vp028a.png)
![vp028b: inputs and representative solution](images/vp028b.png)
![vp028c: inputs and representative solution](images/vp028c.png)

## 🟢 VP29: Duncan's LASH terminal — TSPM reliability vs Monte Carlo {#vp29}

**Input files:** [vp029.xlsx](files/rocscience/vp029.xlsx)

Slide #29 / Duncan (2000): the underwater trench failure at the Port of San Francisco LASH
terminal, the example the Taylor-series reliability method (TSPM) was built on and the method
XSLOPE's `reliability()` implements. San Francisco Bay Mud with depth-growing undrained strength
(su = 100 psf at el. −20 + 9.8 psf/ft), γ = 100 pcf, fully submerged below el. 0; probabilistic
inputs σ_γ = 3.3 and σ_cp = 1.2 from Slide's Table 29.2. Duncan's estimated slip surface is a pixel
trace of the drawn surface, and `reliability(search=False)` evaluates it directly.

**TSPM comparison (fixed surface, Spencer):**

| Component | XSLOPE | Duncan (2000) Table 5 | Slide (LHS Monte Carlo) |
|---|---|---|---|
| F, most likely values | 1.145 | 1.17 (−2.1%) | 1.157 (−1.0%), mean 1.166 |
| β_ln → PF | 0.936 → **17.5%** | ≈0.9 → **18%** | 1.088 → 13.96% (Monte Carlo — cross-estimator) |

*Both published sources are reproduced. The deterministic factor of safety brackets between
them on Duncan's surface, represented as a smooth least-squares arc (RMS 1.1 ft against the
pixel trace), and the probability of failure reproduces Duncan's own 18% almost exactly.
Slide's Table 29.2 renders Duncan's whole-envelope ±σ as a rate-only σ (±1.2 psf/ft), the
only form a c/cp parameterization can express, which is why Slide's Monte Carlo PF (14%)
sits below Duncan's 18%.*

*The same slope carries three published probabilities of failure — 14% (Slide MC),
18% (Duncan 2000 TSPM), 30–33% (D&W 2014 §13.5.6, on a wider 2σ-rule envelope). Two TSPM
analyses by the same author differ by more than TSPM differs from Monte Carlo, so the
σ-input choice, not the estimator, dominates probabilistic comparisons.*

![vp029: inputs and representative solution](images/vp029.png)

## 🟢 VP30: Reinforced embankment, (4) materials, tension crack, geosynthetic {#vp30}

**Input files:** [vp030a.xlsx](files/rocscience/vp030a.xlsx) (circle A) ·
[vp030b.xlsx](files/rocscience/vp030b.xlsx) (circle B)

Borges & Cardoso (2002)'s first geosynthetic-reinforced embankment on soft clay: a 2 m
symmetric embankment, 10.6 m crest, 2:3 (V/H) faces, on a 5 m saturated clay layer over a
rigid stratum, with one unanchored geosynthetic level (T = 200 kN/m, force parallel to the
sheet) at the fill base. The paper's other two embankments are also built: Case 2 as VP31,
covered by [SLOPE/W §2.18](geostudio.md#gs-2-18), and Case 3 as [VP32](#vp32).

The two sources are complementary. The manual prints the materials (Table 30.2) and the
reinforcement but leaves the geometry to an unlabeled Figure 30.1; the paper supplies the
geometry (§4.1) and, in Table 10, both published circles outright — center (1.0, 1.0),
R = 5.74 (A) and R = 5.24 (B) — along with driving and resisting moments that cross-check
the manual's to the digit. M<sub>RR</sub> = 200.00 on every circle fixes the datum: 200 kN/m
on a 1.0 m arm puts the geosynthetic at y = 0.

| Circle | XSLOPE (Bishop) | Slide2 | Borges & Cardoso |
|---|---|---|---|
| A (R = 5.74) | **1.679** | 1.69 (−0.7%) | 1.77 (−5.1%) |
| B (R = 5.24) | **1.650** | 1.66 (−0.6%) | 1.74 (−5.2%) |

Bishop is the method the manual specifies for this problem — it "best simulates the moment based
limit-equilibrium method the authors use" — and it lands within 0.7% of Slide on both circles. The
three published anchors reconcile: Borges' column is the uncracked arc integrated whole plus the
geosynthetic, Slide's and XSLOPE's are the cracked arc plus the same geosynthetic, and what
separates the two pairs is the cost of the crack.

**The tension crack is the whole problem.** Both circles have their center below the crest, so the
arc's uphill end is buried at its equator and the daylight point sits *above* it, and the arc they
bound exceeds a semicircle. Slide resolves this by auto-cracking the reverse-curvature portion.
XSLOPE never synthesizes a crack from curvature — the equivalent is an explicit `tcrack_depth`
clipping at a proper offset surface — and the depth is not tuned: the reverse-curvature portion
*is* the arc above the equator, so the crack depth is y<sub>crest</sub> − Y<sub>o</sub> = **1.0 m**,
and the arc is near-vertical where the crack cuts it, so the answer is flat over a wide range of
depths around that value. Borges' 1.77 / 1.74 come from integrating the whole arc, overhang
included; that surface doubles back 89 mm, so one x-position carries two depths and a method of
vertical slices cannot represent it at all.

**Only Bishop is locked.** For φ = 0 circles the moment-equilibrium factor of safety is the
complete-equilibrium value (Duncan, Wright & Brandon 2014, pp. 89, 96–97), which is why the manual
prescribes Bishop. Spencer is inadmissible here: base angles on the crack-shortened arc run from
+83° to −74°, so the horizontal projections of the base normals nearly cancel and the whole mass
carries only ≈68 kN/m of net horizontal driving force at F = 1 against the 200 kN/m the geosynthetic
mobilizes. Spencer can satisfy horizontal equilibrium only by hanging interslice tension at the
crack face — a root that satisfies both equations while the thrust line leaves the soil, and that
walks with the slice count instead of converging. Two controls isolate the cause: soil-only, Bishop
and Spencer agree to three decimals; and spreading the same 200 kN/m along the arc returns Spencer
beside Bishop. Complete equilibrium is satisfiable at the moment answer — Morgenstern–Price with a
half-sine interslice function converges with all base normals positive within 0.6% of Bishop.

![vp030a: inputs and representative solution](images/vp030a.png)

![vp030b: inputs and representative solution](images/vp030b.png)

**Sources:** Slide Slope Stability Verification Manual §30; Borges & Cardoso (2002),
*Geotextiles and Geomembranes* 20(6), 395–421.

## 🟢 VP32: Reinforced embankment, (7) materials, geosynthetic {#vp32}

**Input files:** [vp032a.xlsx](files/rocscience/vp032a.xlsx) (case 1, circle A) ·
[vp032b.xlsx](files/rocscience/vp032b.xlsx) (case 1, circle B) ·
[vp032c.xlsx](files/rocscience/vp032c.xlsx) (case 2, circle C)

Borges & Cardoso (2002)'s third geosynthetic-reinforced embankment: two fill stages
(a 7 m and an 8.75 m crest) of granular fill over five soft clay layers, with a
T = 200 kN/m geosynthetic at the fill base (interface friction 30.96°, force parallel
to the reinforcement). Slide2's figures for this problem carry no coordinates; the
geometry here comes from the RS2 manual's fully labeled figures for the same problem,
which print every vertex, the clay layer boundaries, and the three published circles.

| Case | XSLOPE (Bishop = Spencer) | Slide2 | Borges & Cardoso |
|---|---|---|---|
| H = 7, circle A | 1.218 | 1.23 (−1.0%) | 1.25 (−2.6%) |
| H = 7, circle B | 1.216 | 1.22 (−0.3%) | 1.19 (+2.2%) |
| H = 8.75, circle C | 0.981 | 0.98 (+0.1%) | 0.99 (−0.9%) |

![vp032a: inputs and representative solution](images/vp032a.png)

![vp032c: inputs and representative solution](images/vp032c.png)

## 🟢 VP33: Dike, (5) materials, probabilistic analysis, water table {#vp33}

**Input files:** [vp033.xlsx](files/rocscience/vp033.xlsx)

El-Ramly, Morgenstern & Cruden (2003)'s simplified probabilistic model of a Syncrude tailings
dyke: a cohesionless section (tailing sand over glacio-fluvial sands and tills, all φ = 34°) on a
presheared disturbed clay-shale with φ = 7.5° ± 2.1°. The critical mechanism rides the clay-shale,
and Slide's drawn circle (center (327.5, 394), R = 124) is tangent about nineteen meters below the
model base, so the surface is **composite** — truncated at the base and running flat inside the
weak band. This is the [composite-surface option](../lem/overview.md#composite-failure-surfaces)
exercised on a published benchmark.

|  | XSLOPE (composite) | Slide | El-Ramly et al. |
|---|---|---|---|
| Bishop, Slide's circle | 1.320 | 1.305 (+1.1%) | 1.31 (+0.8%) |

*Slide assigns three piezometric lines to different materials; XSLOPE's single line uses the
lowest everywhere — applying each of Slide's lines in turn brackets the factor of safety within
1–3%, well inside the digitizing tolerance. The clayey till's properties are not printed in the
manual, so the geometry and material zonation follow the RS2 vendor `.fez`. The published
probability of failure (1.5–1.6×10⁻³ by Monte Carlo) is reported without a lock: it rests on the
paper's spatial-averaging variance treatment, which a single slope-scale σ does not reproduce. Run
on the point-scale σ, the Taylor series and a 10,000-sample Monte Carlo agree with each other and
both sit roughly twenty times above El-Ramly et al.'s value — the variance reduction they obtain
by averaging φ along the slip surface — so the missing ingredient is a correlation-length
treatment, not the estimator.*

![vp033: inputs and representative solution](images/vp033.png)

Also [SLOPE/W §2.20](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP34: Dam, (3) materials, probabilistic analysis, water table {#vp34}

**Input files:** [vp034.xlsx](files/rocscience/vp034.xlsx)

Wolff & Harr (1987)'s reliability model of the Clarence Cannon Dam (Salt River, Missouri):
Phase I fill placed to el. 548 with a cutoff trench to rock, a Phase II shell to the crest at
el. 659, a vertical chimney drain under the crown, and a flat water table at el. 557, in polygon
zones. Geometry is digitized from the Slide model's vertex dots, which sit a few feet off the
labels in W&H's original figure and are used as-built here because the factor-of-safety targets
are Slide's; the unit weight γ = 150 pcf is Slide's published choice, tuned to reproduce W&H's
factor of safety. The analysis evaluates W&H's prescribed noncircular surface: 45° from the crest
edge through the shell and drain, along the base of the Phase I fill at el. 516, exiting the
downstream face at the waterline.

|  | XSLOPE | Slide | Wolff & Harr |
|---|---|---|---|
| Spencer | 2.423 | 2.383 (+1.7%) | — |
| Morgenstern–Price | 2.384 | 2.333 (GLE — cross-method) | 2.36 (+1.0%) |

Morgenstern–Price lands within 1% of W&H's 2.36 and 2.2% of Slide's GLE, within
the tolerance of the pixel-traced geometry.

*The probabilistic side sits outside the Taylor-series method's domain: W&H's inputs give the
Phase I fill a φ standard deviation (7.87°) larger than its mean (6.34°), so the F(φ−σ)
evaluation would use a negative friction angle and `reliability()` declines the input. The two
published probabilities themselves differ by 13× — W&H's point estimate 4.55×10⁻² against Slide's
Monte-Carlo 3.55×10⁻³ — so at a COV of 124% the sampling treatment of the φ ≥ 0 bound dwarfs the
estimator choice. `reliability_mc` carries the case past that boundary, truncating the negative φ
draws at zero as the published samplers do, and lands inside the band the three published
estimates span. It is reported rather than locked because the two published probabilities are
13× apart, so there is no single target to lock a sampled probability against; the deterministic
factor of safety is the locked benchmark.*

![vp034: inputs and representative solution](images/vp034.png)

Also [SLOPE/W §2.21](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP35: Dam, (5) materials, probabilistic analysis, reliability index {#vp35}

**Input files:** [vp035.xlsx](files/rocscience/vp035.xlsx)

Hassan & Wolff (1999)'s end-of-construction model of Cannon Dam, the benchmark for their central
finding: **the surface of minimum reliability index is not the surface of minimum factor of
safety**. Two clay fills with large strength scatter (Phase I φ = 8.5° ± 8.5°, Phase II
c = 143.6 ± 79 kPa with ρ(c,φ) = −0.55), a vertical sand-filter strip under the crest and a
spoil-covered downstream toe, in polygon-zone geometry.

Their published surfaces are search products, so the comparison reproduces the *procedure*: a
Bishop critical search at mean strengths (their surface A) and a direct minimum-β scan over
downstream circles evaluating the Taylor-series β on each fixed candidate (their surface B). The
benchmark is **downstream-slope-specific** — a global grid-seeded search finds a substantial
upstream mechanism on this dry model, and both Hassan & Wolff and Slide analyze the downstream
slope, so the seeded search is what reproduces the published problem. The c–φ correlations enter as
the standard Taylor-series cross-terms; the regression tag locks the uncorrelated β.

| Quantity | XSLOPE | Slide | Hassan & Wolff |
|---|---|---|---|
| Critical FS at means (Bishop search) | 2.529 | 2.551 (−0.9%) | 2.753 (−8.1%) |
| Minimum-β surface: β_ln | 3.353 | 4.351 (−22.9%) | 3.987 (−15.9%) |

All three programs agree on the structure: a mid-depth circle through the Phase II fill and upper
Phase I carries roughly one-third the reliability index of the factor-of-safety-critical surface,
so a design screened on the factor of safety alone would examine the wrong surface. The β
magnitudes spread with the estimator at these extreme COVs — the Taylor series evaluates strength
at φ − σ = 0° for the Phase I fill, a tail truncated-normal Monte Carlo sampling rarely reaches —
the same direction as VP36's spread at three times the COV. The paper's nine fixed surfaces are
reproduced on the SLOPE/W model's exact frame rather than this one, at
[GeoStudio §2.22](geostudio.md#gs-2-22), which also shows the paper's printed factors for surfaces
G and H to be transposed; they are not carried onto vp035.xlsx, whose digitized frame is
anisotropic enough to move the sliding weight substantially.

![vp035: inputs and representative solution](images/vp035.png)

Also [SLOPE/W §2.22](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP36: Slope, homogenous, probabilistic analysis, ru pore pressure, reliability index {#vp36}

Slide #36: Li & Lumb (1987) / Hassan & Wolff (1999) reliability benchmark: c'=18+-3.6, phi'=30+-3, gamma=18+-0.9, ru=0.2 (+-0.02, not perturbed by xslope's Taylor-series reliability - its contribution to sigma_F is small). The comparison is the deterministic Bishop factor of safety and the lognormal reliability index beta on that same surface, against Hassan & Wolff's published pair and Slide's; both are tabulated below.

**Input files:** [vp036.xlsx](files/rocscience/vp036.xlsx)

| Method | XSLOPE | H&W | Slide |
|---|---|---|---|
| Bishop | 1.333 | 1.334 (−0.1%) | 1.340 (−0.5%) |
| β_ln (reliability) | 2.263 | 2.336 (FOSM) (−3.1%) | 2.482 (Monte-Carlo) (−8.8%) |

*β estimates legitimately spread by estimation method; xslope does not perturb ru (σ = 0.02, minor).*

![vp036: inputs and representative solution](images/vp036.png)

Also [SLOPE/W §2.23](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP37: Cohesionless slope, crest surcharge, back-analysis of required support force {#vp37}

Slide #37 reproduces the "Reinforcement Example" of the XSTABL v5 reference manual (Sharma 1996 §3.8, after Koerner 1991): a 12 m high, 45° cohesionless slope (φ = 36°, γ = 20 kN/m³, c = 0, from XSTABL's Fig. 3.15) under a 40 kN/m² crest surcharge, with geometry from Slide's coordinate-labeled Fig. 37.1.

**Input files:** [vp037.xlsx](files/rocscience/vp037.xlsx) (base slope)

**Base slope (unreinforced).** On Slide's printed critical circle (center −11.410, 35.264, R 34.426; Fig. 37.3), and equally from a toe-focus, 2 m-minimum-depth search that lands on that circle unaided:

| Method | XSLOPE | Slide (Fig. 37.3) | XSTABL (F<sub>crit</sub>) |
|---|---|---|---|
| Bishop | 0.764 | 0.764 (0.0%) | 0.734 (+4.1%) |
| Spencer | 0.764 | — | — |

**Required support force (part a).** XSTABL and Slide back-analyse the horizontal support that raises the slope to FS = 1.5, reported as the maximum over all toe surfaces. Sweeping that force in XSLOPE — a reinforcement line at el 9, re-searching the critical surface at each step — gives the required design force below.

| Back-analyzed quantity for FS = 1.5 | XSLOPE | Slide | XSTABL |
|---|---|---|---|
| Required support force (part a) | ≈205 kN/m (active) / ≈305 kN/m (passive) | 351 kN/m (support-force procedure — cross-basis) | 345 kN/m (support-force procedure — cross-basis) |
| Reinforced-zone length (part b) | — *not built* | 7.6 m | 7.5 m |

The published forces come from XSTABL's support-force procedure, which sizes the force from the effective normal forces at the target factor of safety — a more conservative crediting than a limit-equilibrium reinforcement line. The regression therefore locks the base-slope factor of safety and documents the back-analysis rather than locking a force the two methods compute differently. Part b, the minimum length of an elevated-friction zone that holds FS = 1.5, needs a variable-length material zone XSLOPE does not have.

![vp037: inputs and representative solution](images/vp037.png)

## 🟢 VP38: Excavated slope, FE groundwater seepage, matric suction {#vp38}

Slide #38 reproduces Ng & Shi (1998), a 28° cut slope in Hong Kong: a homogeneous soil (24 m over a 6 m bedrock band) whose steady groundwater regime leaves the upper part of the cut **unsaturated**, so the negative pore water pressure there raises the shear strength. The stability is a conventional Bishop analysis on the FE seepage field, with the strength above the water table given by the extended (Fredlund) Mohr-Coulomb criterion:

$$\tau = c' + (\sigma_n - u_a)\tan\varphi' + (u_a - u_w)\tan\varphi^{\,b}$$

whose last term is an apparent cohesion from suction. Material (Table 38.1): $c' = 10$ kPa, $\varphi' = 38°$, $\varphi^{\,b} = 15°$, $\gamma = 16$ kN/m³.

**Input files:** [vp038a](files/rocscience/vp038a.xlsx) / [vp038b](files/rocscience/vp038b.xlsx) / [vp038c](files/rocscience/vp038c.xlsx) (right-side head $H = 61 / 62 / 63$ m), each with its `_mesh.json` / `_seep.csv` seepage sidecars.

**The seepage.** Geometry is read from the vendor RS2 mesh's external boundary, the domain closing down the right edge and along an impermeable base to the toe. XSLOPE solves the steady unsaturated field itself (`u='seep'`): total head $H$ on the right side, head 6 m on the left, the ground surface a seepage/exit face, base and far edges no-flow. Relative permeability is Ng (1998)'s measured $k$-function cast as a Gardner curve with $a = 7.479$, $n = 2.908$ and $k_s = 4.19$ m/day — measured data, not a fitted knob, and a van Genuchten cast of the same curve moves the factor of safety by < 0.005. The solved field carries bounded matric suction above the water table, unlike a deep piezometric line's unbounded hydrostatic suction, so no suction cap is required.

**The suction.** `generate_slices` reads the signed seepage pressure at each slice base; where it is negative it prices the suction into an apparent cohesion added to the resisting $c\,\Delta\ell$ term while the effective-normal term keeps $u$ clamped at 0. Below the water table the slice sees positive $u$ and no suction credit. All three cases are evaluated on Slide's printed $H = 61$ critical circle (Fig. 38.2, center (47.490, 56.311), radius 16.087) — a shallow circle entirely in the unsaturated part of the cut, where the suction credit lives. Only $H = 61$ has a figure, and the critical geometry is head-invariant to that precision.

**Results** (Bishop simplified, on Slide's printed circle, `num_slices=60`):

| $H$ (m) | XSLOPE | Slide | Ng & Shi (1998) |
|---|---|---|---|
| 61 | 1.612 | 1.621 (−0.6%) | 1.636 (−1.5%) |
| 62 | 1.533 | 1.538 (−0.3%) | 1.527 (+0.4%) |
| 63 | 1.413 | 1.407 (+0.4%) | 1.436 (−1.6%) |

XSLOPE reproduces Slide's Bishop values within 0.6% and Ng & Shi's own published Bishop values within 1.6%, and tracks the physics: the factor of safety falls as the right-side head rises. Turning the suction credit off drops all three well below the published band, confirming that the apparent cohesion, not the effective-normal pressure, carries the difference. A free search with the credit on lands not on Slide's shallow circle but on a somewhat deeper one a few percent lower, trading suction credit for a longer saturated base; locking the specified surface keeps the comparison clear of that difference.

![vp038a (H = 61 m): inputs and solution on Slide's critical circle](images/vp038a.png)

![vp038b (H = 62 m): inputs and solution](images/vp038b.png)

![vp038c (H = 63 m): inputs and solution](images/vp038c.png)

## 🟢 VP39: Reinforced embankment, (2) materials, tension crack, geosynthetic {#vp39}

**Input files:** [vp039a.xlsx](files/rocscience/vp039a.xlsx) (clay fill, unreinforced) ·
[vp039b.xlsx](files/rocscience/vp039b.xlsx) (clay, T=169) ·
[vp039c.xlsx](files/rocscience/vp039c.xlsx) (sand fill, unreinforced) ·
[vp039d.xlsx](files/rocscience/vp039d.xlsx) (sand, T=44)

Tandjiria (2002)'s required-reinforcement problem: a half-embankment (centerline at
x = 0) on soft clay, analyzed as a clay fill (c′ = 20 kPa, φ = 0, water-filled tension
crack) and as a sand fill (φ′ = 37°, dry crack). The unreinforced critical surface is
located first; the geosynthetic force at the embankment base that restores FS = 1.35
on that surface is then computed (active application, force parallel to the
reinforcement, per the source).

| Case | XSLOPE | Slide | Tandjiria (2002) |
|---|---|---|---|
| Clay fill, unreinforced (Spencer) | 0.968 | 0.975 (−0.7%) | 0.981 (−1.3%) |
| Clay fill, FS at T = 169 kN/m | 1.332 | 1.35 (−1.3%) | — |
| Clay fill, required T for FS = 1.35 | 175 kN/m | 169 (+3.6%) | 170 (+2.9%) |
| Sand fill, unreinforced (Spencer) | 1.200 | 1.209 (−0.7%) | 1.219 (−1.6%) |
| Sand fill, FS at T = 44 kN/m | 1.343 | 1.35 (−0.5%) | — |
| Sand fill, required T for FS = 1.35 | 46 kN/m | 44 (+4.5%) | 45 (+2.2%) |
| Noncircular variants (not locked) | — | 0.935 / 1.188 | — |

The regression locks the unreinforced factors of safety and the factors of safety at
Slide's published forces, each on the stored critical circle. The source's noncircular
variants (Slide's required T, 184 and 56 kN/m) are not locked: XSLOPE's noncircular search
returns seed-dependent local minima on this φ = 0 problem, and the noncircular reinforced
evaluation needs the reinforcement generalization noted for VP30.

![vp039a: inputs and representative solution](images/vp039a.png)
![vp039b: inputs and representative solution](images/vp039b.png)
![vp039c: inputs and representative solution](images/vp039c.png)
![vp039d: inputs and representative solution](images/vp039d.png)

Also [SLOPE/W §2.24](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP40: Slope, homogenous, sensitivity analysis {#vp40}

**Input files:** [vp040.xlsx](files/rocscience/vp040.xlsx)

Perry (1993, Fig. 10): a dry homogeneous slope with power-curve strength
τ = A·σ′ᵇ (A = 2, b = 0.7, γ = 20) evaluated on the specified five-segment surface —
and the corpus's first *sensitivity* benchmark: the manual sweeps A and b over ±15% of
their means and publishes the FS-vs-parameter curves. The XSLOPE sweep runs through `sensitivity()` on the fixed surface
(`search=False`, since the surface is specified), and the regression tags lock the base
case and both range endpoints for each parameter.

| Quantity | XSLOPE (Janbu) | Slide | Perry | Note |
|---|---|---|---|---|
| FS on the specified surface | 1.003 (Janbu corrected) | 0.944 (simplified — cross-method) | 0.98 (+2.3%) | Perry's value pairs with the corrected factor |
| ΔFS over the A range (±15%) — **sweep result** | −15.0% / +15.0% | −15.2% / +14.4% | ≈ ±13% | these cells are percent *changes* in FS, not factors of safety, so they are compared directly rather than ratioed: XSLOPE lands within 0.2 and 0.6 percentage points of Slide, and 2.0 pp of Perry's chart read at each end |
| ΔFS over the b range (±15%) — **sweep result** | −45.0% / +82.5% | −44.4% / +81.1% | ≈ −38% / +82% | within 0.6 and 1.4 percentage points of Slide; against Perry, 7.0 pp at the −15% end and 0.5 pp at the +15% end — Perry's endpoints are read off the published curve, as the ≈ marks |

The relative sensitivities — the quantity this problem exists to verify — agree with
Slide's Figure 40.3 within about a percent at every endpoint, and the A-sweep is exactly
linear as theory requires (on a fixed dry surface every increment of strength scales
with A). The absolute spread between the two programs is the Janbu correction-factor convention on a
power-curve soil: XSLOPE applies the c–φ correction curve, while Slide's tabulated value is
the uncorrected one.

![vp040: inputs and representative solution](images/vp040.png)

![vp040: FS vs A and b, the published sensitivity study](images/vp040_sens.png)

## 🟢 VP41: Slope, homogenous, ru pore pressure {#vp41}

Slide #41: Jiang, Baker & Yamagami (2003) homogeneous clay slope with power-curve strength tau = 1.4*(sigma')^0.8 and ru = 0.3 — exercises the v12 pow option and ru together.

**Input files:** [vp041.xlsx](files/rocscience/vp041.xlsx)

| Method | XSLOPE | Slide | Charles & Soares | Perry | Baker (band) |
|---|---|---|---|---|---|
| Bishop | 1.668 | 1.656 (+0.7%) *(path search)* | 1.66 (+0.5%) | 1.67 (−0.1%) | 1.56–1.60 |
| Janbu (corrected) | 1.660 | 1.563 (simplified — cross-method) | — | — | — |
| Spencer | 1.670 | — | — | — | — |

![vp041: inputs and representative solution](images/vp041.png)

## 🟢 VP42: Baker & Leshchinsky safety-map dam — reservoir-loaded clay-core dam {#vp42}

Slide #42 / Baker & Leshchinsky (2001): the safety-map clay-core dam — granular fill (c' = 0, φ' = 40°, γ = 21.5) around a diamond core (c' = 20, φ' = 20°, γ = 20) on a hard base (c' = 200, φ' = 45°), a half-full upstream reservoir, a phreatic dropping through the core and daylighting at the downstream toe, and a 5-m cracked crest layer modeled as a dry tension crack. Geometry is fully labeled in Slide's figure, and the section is tiled as material-zone polygons matching the SLOPE/W `.gsz` region set ([§2.25](geostudio.md#gs-2-25)). The phreatic's downstream limb is the vendor polyline both source models carry, exiting at elevation 0 on the ground surface, so there is no tailwater.

The paper states its method explicitly: pore pressures are *"evaluated using the vertical distance between the phreatic surface and the slice center,"* and the material weights are total unit weights — the effective-stress convention XSLOPE uses, which the vendor `.gsz` confirms. XSLOPE carries the reservoir as an explicit hydrostatic traction normal to the submerged face:

| Surface (Spencer) | XSLOPE | Slide | Baker & Leshchinsky (2001) |
|---|---|---|---|
| Slide's critical circle | 1.926 | 1.925 (+0.1%) | — |
| Baker's noncircular surface | 1.882 | — | 1.91 (−1.5%) |

The stored-circle result is regression-locked as **VP42-circle** (OMS 1.773, Bishop 1.882, Spencer 1.926, M-P 1.925) and Baker's surface as **VP42-noncirc** (Spencer 1.882, M-P 1.869).

**Reservoir-load statics.** For a fully submerged still-water slope the hydrostatic traction is exact: on an identical circle it reproduces the closed-form dry-buoyant-weight solution to within 0.006 in Bishop and Spencer. Folding the ponded-water column into vertical slice weight instead differs by tens of percent and can drive the base into non-physical tension, which is why the water formulation stays explicit rather than buoyant. The factor of safety on this deep, mostly submerged circle is sensitive to the phreatic surface and to the pool and the load agreeing with each other, so both are held at the shared reservoir level of el 30.

**Input files:** [vp042.xlsx](files/rocscience/vp042.xlsx)

![vp042: inputs and representative solution](images/vp042.png)

## 🟢 VP43: Slope, homogeneous — planar surface (Baker 2001) {#vp43}

Slide #43 / Baker (2001): the planar-slip-surface benchmark on a homogeneous, dry c′-φ′ slope (H = 10 m, c′ = 30 kPa, φ′ = 30°, γ = 20 kN/m³), with the factor of safety evaluated on planes through the toe as a function of where the plane daylights on the backslope. Baker's critical plane sits at X = x/H = 0.85.

The manual's figure is unlabeled and the geometry it implies controls the answer, so the geometry comes from the [SLOPE/W model for the same problem](geostudio.md#gs-2-26), which stores it exactly with the crest offset at 2.5 m. On it the critical slip plane runs from the toe (0, 0) to the daylight point (8.5, 10) at 49.6°, matching Slide's reported ≈ 49.5°, with both endpoints on the ground surface.

**Input files:** [vp043.xlsx](files/rocscience/vp043.xlsx)

| Method | XSLOPE | RocPlane | Baker (Culmann) | Slide |
|---|---|---|---|---|
| Spencer | 1.352 | 1.351 (+0.1%) | ≈ 1.35 | 1.329 (circular search — a different surface) |
| Morgenstern-Price | 1.352 | — | — | — |
| Janbu (corrected) | 1.352 | — | — | 1.329 (circular search — a different surface) |
| Corps of Engineers | 1.352 | — | — | — |
| Lowe-Karafiath | 1.352 | — | — | — |

Every method that applies to a non-circular surface reads 1.352 on the plane, agreeing to ten significant figures and matching SLOPE/W's own solve of the identical plane along with the RocPlane and Baker references. A single straight plane holds α constant on every slice, and reaching equilibrium on it leaves most of the interior boundaries in interslice tension; the four side-force methods report that state alongside the factor of safety rather than declining the surface. [SLOPE/W §2.26](geostudio.md#gs-2-26) is the same problem and reads the same way.

**Sources:** Slide Slope Stability Verification Manual §43; GeoStudio SLOPE/W Verification Manual §2.26; Baker (2001); Baker & Leshchinsky (2001).

## 🟢 VP44: Slope, homogeneous — linear vs non-linear envelope (Baker ex. 1) {#vp44}

Slide #44 / Baker (2003) example problem 1: a straight 43° slope, H = 6 m, γ = 18 kN/m³, in compacted Israeli clays, analyzed with three strength models fitted to the same triaxial data — the power curve τ = 1.107·σ′^0.86, the experimentally fitted Mohr-Coulomb envelope c′ = 11.64 kPa / φ′ = 24.7° (Baker's Table I, iteration 0, which resolves the property-table ambiguity in the Slide manual), and Baker's converged local-linear-approximation parameters c′ = 0.39 kPa / φ′ = 38.6°. The example is about extrapolating a linear envelope into the low-stress range: the Mohr-Coulomb fit says the slope is safe, the non-linear law says it is failing.

**Input files:** [vp044a.xlsx](files/rocscience/vp044a.xlsx), [vp044b.xlsx](files/rocscience/vp044b.xlsx), [vp044c.xlsx](files/rocscience/vp044c.xlsx)

| Case | Method | XSLOPE | Slide | Baker |
|---|---|---|---|---|
| (a) power curve | Spencer | 0.958 | 0.960 (−0.2%) | 0.97 (−1.2%) |
| (b) Mohr-Coulomb | Spencer | 1.518 | 1.536 (−1.2%) | 1.50 (+1.2%) |
| (c) LLA converged | Spencer | 0.980 | 0.981 (−0.1%) | 0.97 (+1.0%) |

*Baker states γ = 18 for all his examples; the Slide manual's table prints 19.5, which reconciles with neither program's results. Slide's Janbu values are simplified/uncorrected, as in [#45](#vp45).*

![vp044a: inputs and representative solution](images/vp044a.png)

![vp044b: inputs and representative solution](images/vp044b.png)

![vp044c: inputs and representative solution](images/vp044c.png)

## 🟢 VP45: Slope, homogenous {#vp45}

Slide #45 runs one 4:1 slope through two strength models. Mohr-Coulomb case:
c'=11.64, phi'=24.7, gamma=18. Power-curve case: tau = 1.107*(sigma')^0.86 (Baker's
A=0.58, n=0.86, T=0).

**Input files:** [vp045a.xlsx](files/rocscience/vp045a.xlsx), [vp045b.xlsx](files/rocscience/vp045b.xlsx)

*Mohr-Coulomb case*

| Method | XSLOPE | Slide |
|---|---|---|
| Spencer | 2.801 | 2.794 (+0.3%) |
| Janbu (simplified) — cross-method, XSLOPE reports the f₀-corrected value | — | 2.662 |

*Power-curve case*

| Method | XSLOPE | Slide |
|---|---|---|
| Spencer | 2.649 | 2.662 (−0.5%) |
| Janbu (simplified) — cross-method, XSLOPE reports the f₀-corrected value | — | 2.559 |

*Slide’s Janbu values are simplified/uncorrected; XSLOPE's carry fo and agree once scaled.*

![vp045a: inputs and representative solution](images/vp045a.png)

![vp045b: inputs and representative solution](images/vp045b.png)

## 🟢 VP46: Baker (1993) three-stage dam — stages 1-2 built {#vp46}

Slide #46 / Baker (1993): a three-loading-stage dam — end of construction with an empty reservoir, steady-state seepage with a full reservoir, and rapid drawdown. Stages 1 and 2 are built; stage 3 is not, because its undrained-strength field is printed only as a two-dimensional contour map. A small compacted-clay embankment (crest el 101, toes at x = 80 and x = 128, both el 95) sits on a deep natural-clay foundation; downstream the ground drops on a **4H:1V** face from (128, 95) to the toe bench (148, 90) and runs flat to x = 220. Geometry from Figure 46.1; materials (Table 46.1) compacted clay c′ = 6.5 kPa, φ′ = 40°, γ = 18 and natural clay c′ = 0, φ′ = 32°, γ = 18.

**Input files:** [vp046.xlsx](files/rocscience/vp046.xlsx) (stage 1, dry) / [vp046b.xlsx](files/rocscience/vp046b.xlsx) (stage 2, steady seepage, with `_mesh.json` / `_seep.csv` sidecars)

The critical mechanism is the cohesionless downstream natural-clay face, where the depth-independent infinite-slope value tan 32° / tan 14.04° = **2.50** is the manual's "Theoretical FS = 2.5". XSLOPE's circular search rides that face and lands on it:

| Method | XSLOPE | Slide | Baker | theory |
|---|---|---|---|---|
| Spencer (circular) | 2.500 | 2.534 (−1.3%) | 2.41 (+3.7%) | 2.5 (0.0%) |
| Bishop (circular) | 2.500 | — | — | — |

Slide's published Spencer 2.534 is a minimum-depth-5 m noncircular random search, which rides a slab slightly off the pure infinite-slope minimum and so reads ~1.4% high; Baker (1993) 2.41 sits ~3.6% below theory.

<!-- test: file=files/rocscience/vp046.xlsx, type=circular_search, num_slices=40, fs_spencer=2.500, fs_bishop=2.500, benchmark=VP46-dry -->

![vp046: stage 1 inputs and representative solution](images/vp046.png)

**Stage 2 — steady seepage, full reservoir.** With the reservoir full at el 100 the pore pressures come from a steady FE seepage field XSLOPE solves itself (`u='seep'`, the same route as [VP38](#vp38)): total head 100 on the submerged upstream boundary, head 0 on the base, the dry downstream ground an exit face, and the reservoir water as a distributed load on the submerged face. Baker publishes no numeric permeability, only that the two clays are equal with a 10:1 horizontal:vertical anisotropy — which is all a steady head field depends on. The one estimated field-relevant input is the natural-clay unsaturated fringe (Gardner a = 0.06, n = 2), where halving or doubling a moves FS by ≈ ±2%. The search targets the upstream slope Baker's analysis is about, which is what Slide's inherited search limits select.

| Method | XSLOPE | Slide | Baker |
|---|---|---|---|
| Spencer (circular) | 7.086 | 7.003 (+1.2%) | 6.98 (+1.5%) |
| Bishop (circular) | 7.093 | — | — |

<!-- test: file=files/rocscience/vp046b.xlsx, type=circular_search, num_slices=40, fs_spencer=7.086, fs_bishop=7.093, benchmark=VP46-steady -->

![vp046b: stage 2 inputs and representative solution](images/vp046b.png)

**Stage 3 — rapid drawdown (not built).** The undrained analysis needs the strength distribution S(x,y), which Baker prints only as the Fig. 14 contour map (20–120 kPa). That field is genuinely two-dimensional — ≈ 5–10 kPa at the reservoir bottom against ≈ 60 kPa at the same elevation under the embankment surcharge — so reducing it to the per-material one-dimensional functions XSLOPE or Slide's `.fn6` can carry is under-determined, and where the fit is anchored moves the factor of safety by far more than a lock could tolerate.

| Stage 3 (not built) | XSLOPE | Slide | Baker |
|---|---|---|---|
| Rapid drawdown | — | 2.181 | 2.18 |

Slide's value is itself a manual extraction of the same figure through the `.fn6` strength functions, which ship only with the Slide2 install.

## 🟢 VP47: Soil-nailed wall in clay (Amherst test wall) {#vp47}

Slide #47 / Sheahan & Ho (2003): 6 m vertical cut in undrained Amherst clay (cᵤ = 25 kPa, γ = 18.9 kN/m³), two nail rows at 20° declination (L = 4.9 m, tensile 118 kN, plate 86 kN, bond 15 kN/m, sₕ = 1.5 m) and the shotcrete facing weight applied as a 14.6 kN/m vertical line load at the crest. The wall failed in the field test; the published analyses sweep planar surfaces through the toe. Nails are modeled axial/passive with the FHWA-style capacity envelope (plate strength at the head, bond-strength taper at the tip).

**Input files:** [vp047.xlsx](files/rocscience/vp047.xlsx)

| Method | XSLOPE | Slide | Sheahan (trial wedge) |
|---|---|---|---|
| Janbu, critical plane (44.5°) | 0.899 | 0.890 (+1.0%) *(simplified = corrected on this plane)* | 0.887 (+1.4%) |

*Sheahan adds the nail tension unfactored; that convention (`appl=active`) gives 0.893. The tabulated 0.899 uses Slide's nail default (passive).*

![vp047: inputs and representative solution](images/vp047.png)

Also [SLOPE/W §2.27](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP48: Soil-nailed wall in sand (Clouterre test wall no. 1) {#vp48}

Slide #48 / Sheahan & Ho (2003): the CEBTP Clouterre full-scale wall — 7 m cut in Fontainebleau sand (c′ = 3 kPa, φ′ = 38°, γ = 20 kN/m³), seven nail rows at 10° declination (lengths 6/8/7.5/8/8/8/6 m from the paper's Fig. 4a, sₕ = 1.15 m), shotcrete weight as a 13.2 kN/m line load. Following Sheahan, each nail carries a constant 15 kN tension (fully anchored ends in xslope). The benchmark evaluates planar surfaces through the toe at 45–70°:

**Input files:** [vp048.xlsx](files/rocscience/vp048.xlsx)

| Plane angle | XSLOPE Janbu | XSLOPE Spencer | Slide Janbu | Sheahan |
|---|---|---|---|---|
| 55° (stored surface) | 0.991 | 0.991 | 0.989 (+0.2%) | 0.989 (+0.2%) |

*The stored surface is the 55° plane, where Slide and Sheahan agree exactly; Janbu and Spencer coincide on a single plane. Right-facing axial reinforcement against a vertical wall face — the force components, the facing detection and the Janbu correction-factor chord — is guarded by a left/right mirror consistency test.*

![vp048: inputs and representative solution](images/vp048.png)

Also [SLOPE/W §2.28](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP49: Retaining wall, grouted tiebacks, soldier piles {#vp49}

**Input files:** [vp049.xlsx](files/rocscience/vp049.xlsx)

From the Caltrans SNAILZ reference manual: a two-layer slope cut by a soldier-pile
tieback wall, evaluated on the manual's given bilinear wedge from the wall toe (Slide
prints its endpoints; the interior kink is digitized from the figure at (37.0, 33.6)).
The two tieback rows carry different bar capacities (Table 49.2, tensile = plate, bond
13,571.68 lb/ft, 8-ft spacing); the soldier pile is modeled as Slide models it — a
micro-pile at the wall face contributing 5,900 lb/ft of shear where the surface passes.

|  | XSLOPE | Slide | SNAILZ |
|---|---|---|---|
| Janbu corrected | 1.469 | 1.479 (−0.7%) | 1.52 (−3.4%) |
| Spencer | 1.439 | — | — |

*Both tiebacks are tensile-governed at the given surface (bond capacity behind the
crossing exceeds the bar capacity), so the digitized tieback lengths carry no
factor-of-safety sensitivity.*

![vp049: inputs and representative solution](images/vp049.png)

Also [SLOPE/W §2.29](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP50: Reinforced slope, (2) materials, predefined slip surface, geosynthetic {#vp50}

Slide #50 (SNAILZ reference manual): nail-reinforced wall, 14 horizontal rows with per-row length/capacity/bond strength, evaluated on the printed deep wedge (-15.813,0)-(0,-5)-(41.722,25). Plate strength equals tensile strength, so the wall end is fully anchored (lp1=0); the embedded end tapers at the bond strength (lp2 = T/bond). Active application, imperial units.

**Input files:** [vp050.xlsx](files/rocscience/vp050.xlsx)

| Method | XSLOPE | Slide | SNAILZ | SLOPE/W |
|---|---|---|---|---|
| Janbu (corrected) | 1.448 | 1.417 (+2.2%) | 1.46 (−0.8%) | 1.354 force solution, ×f₀ ≈ 1.44 (uncorrected — cross-method) |
| Spencer | 1.576 | — | — | 1.606 (M-P — cross-method) |

*Tangent orientation with the force factored by FS (Slide’s nail defaults and the SNAILZ convention); an axial, actively applied force reads substantially higher, so the reinforcement convention dominates this comparison.*

![vp050: inputs and representative solution](images/vp050.png)

Also [SLOPE/W §2.30](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP51: Slope, (4) materials, water table, tension crack, seismic {#vp51}

Slide #51 / GS 2.31: Zhu, Lee & Jiang (2003) four-layer slope, wet, k=0.1, 5 m dry tension crack, specified circle (18.058, 66.744, R=86) read from the printed info box (fig 51.2). Layer-4 properties from the GeoStudio manual (Table 85). The phreatic line is the one element read from the figure trace (anchored at (0,0)-(10,5) on the face, flat ~15.5 at the right); a ±1 m sensitivity bracket moves Bishop by less than 0.01.

**Input files:** [vp051.xlsx](files/rocscience/vp051.xlsx)

| Method | XSLOPE | Slide | Zhu | SLOPE/W |
|---|---|---|---|---|
| Ordinary | 1.069 | 1.145 (−6.6%) | 1.066 (+0.3%) | — (not published) |
| Bishop | 1.278 | 1.278 (0.0%) | 1.278 (0.0%) | 1.284 (−0.5%) |
| Janbu (corrected) | 1.205 | 1.112 (simplified — cross-method; ×f₀ ≈ 1.20) | 1.112 (simplified — cross-method) | 1.115 (uncorrected — cross-method) |
| Corps #2 | 1.404 | 1.422 (−1.3%) | 1.377 (+2.0%) | 1.368 (+2.6%) |
| Lowe-Karafiath | 1.296 | 1.288 (+0.6%) | 1.290 (+0.5%) | 1.283 (+1.0%) |
| Spencer | 1.294 | 1.293 (+0.1%) | 1.293 (+0.1%) | 1.299 (−0.4%) |
| Morgenstern-Price | 1.304 | 1.304 (GLE — cross-method) | 1.303 (GLE — cross-method) | 1.310 (−0.5%) |

*Phreatic line calibrated against the two independently agreeing Bishop/Spencer anchors (±1 m bracket).*

![vp051: inputs and representative solution](images/vp051.png)

Also [SLOPE/W §2.31](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP52: Slope, (4) materials, water table, tension crack {#vp52}

Slide #52, dry and wet (Table 52.2 water table). An unconstrained circular search lands in the
deep (surface 3) family, where Slide runs a grid search and Zhu a specified deep circle, and the
published values spread widely.

**Input files:** [vp052a.xlsx](files/rocscience/vp052a.xlsx), [vp052b.xlsx](files/rocscience/vp052b.xlsx)

*Dry — governing deep (surface 3) family*

| Method | XSLOPE | Slide | Zhu |
|---|---|---|---|
| Bishop | 1.796 | 1.804 (−0.4%) | 1.429 (+25.7%) |
| Spencer | 1.797 | 1.804 (−0.4%) | 1.836 (−2.1%) |

*Wet — governing deep (surface 3) family*

| Method | XSLOPE | Slide | Zhu |
|---|---|---|---|
| Bishop | 1.176 | 1.176 (0.0%) | 1.079 (+9.0%) |
| Spencer | 1.189 | 1.189 (0.0%) | 1.211 (−1.8%) |

*Wet Spencer and Bishop match Slide exactly; the manual itself shows a wide Slide–Zhu spread on this family.*

![vp052a: inputs and representative solution](images/vp052a.png)

![vp052b: inputs and representative solution](images/vp052b.png)

Also [SLOPE/W §2.32](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP53: Priest (1993) rigid block on a plane {#vp53}

Slide #53: Priest's (1993) rigid-block problem, cross-checked by Rocscience against both Slide and RocPlane. A homogeneous slope (c' = 20 kN/m², φ' = 30°, γ = 25 kN/m³) fails on a specified 30° plane from the toe. A 15-m crest tension crack cuts the surface at (25.981, 15) and holds 3.75 m of water (XSLOPE's `tcrack_water`, giving the ½γ<sub>w</sub>d² thrust), and the water table runs flat at el. 18.75 to above the crack, then linearly to the toe, which reproduces Priest's triangular uplift on the plane through the ordinary piezometric-line machinery.

**Input files:** [vp053.xlsx](files/rocscience/vp053.xlsx)

| Method | XSLOPE | Slide | RocPlane | Priest |
|---|---|---|---|---|
| Janbu (uncorrected = corrected) | 1.048 | 1.049 (−0.1%) | 1.049 (−0.1%) | 1.049 (−0.1%) |
| Spencer / M-P / Corps / Lowe | 1.048 | — | — | — |

*On a single plane the sliding block is statically determinate: every method returns the same 1.048, and Janbu's correction factor is exactly 1 (d/L = 0). The 0.001 gap to the three published sources is rounding.*

![vp053: inputs and representative solution](images/vp053.png)

## 🟢 VP54: Slope, homogenous, micro piles {#vp54}

Slide #54, run twice on the printed critical circle: unreinforced, and with the micro-pile row
added.

**Input files:** [vp054a.xlsx](files/rocscience/vp054a.xlsx), [vp054b.xlsx](files/rocscience/vp054b.xlsx)

*No pile*

| Method | XSLOPE | Slide | Yamagami | SLOPE/W |
|---|---|---|---|---|
| Bishop | 1.100 | 1.102 (−0.2%) | 1.10 (0.0%) | 1.102 (−0.2%) |

*With micro-pile row*

| Method | XSLOPE | Slide | Yamagami | SLOPE/W |
|---|---|---|---|---|
| Bishop | 1.185 | 1.193 (−0.7%) | 1.20 (−1.3%) | 1.223 (−3.1%) |

*Slide adds the pile shear un-factored (= XSLOPE's active application); a free search settles on a circle that exits upslope of the pile and misses it, so the tags pin the printed circle.*

![vp054a: inputs and representative solution](images/vp054a.png)

![vp054b: inputs and representative solution](images/vp054b.png)

Also [SLOPE/W §2.34](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP55: Pockoski & Duncan test slope 1 {#vp55}

Slide #55: Pockoski & Duncan (2000) test slope 1 — a homogeneous sandy clay slope (c' = 300 psf, φ' = 30°, γ = 120 pcf), 2:1 face, 50 ft high, with the water table at ground on the lower plateau rising to 10 ft below the crest. P&D used this trio of slopes to compare eight programs; Slide ran an 80×80 grid at tolerance 10⁻⁴. XSLOPE's seed is Slide's printed critical circle (center (24.103, 195.256), R = 100.266), whose endpoints XSLOPE reproduces to 0.01 ft.

**Input files:** [vp055.xlsx](files/rocscience/vp055.xlsx)

| Method | XSLOPE | Slide | Other published codes | Note |
|---|---|---|---|---|
| Bishop | 1.290 *(search 1.289)* | 1.293 (−0.2%) | 1.29 (0.0%) | UTEXAS4, SLOPE/W, XSTABL and RSS all publish 1.29 |
| Spencer | 1.297 *(search 1.295)* | 1.300 (−0.2%) | 1.30 (−0.2%) | UTEXAS4 and SLOPE/W both publish 1.30 |
| Lowe–Karafiath | 1.321 | 1.318 (+0.2%) | 1.32 (+0.1%) | UTEXAS4 |

*The water table between its two pinned ends (at ground on the plateau, 10 ft below the crest) is a figure trace; the 0.003 three-method agreement on Slide's own circle validates it.*

![vp055: inputs and representative solution](images/vp055.png)

## 🟢 VP56: Pockoski & Duncan test slope 2 {#vp56}

Slide #56: P&D test slope 2 — the slope of #55 with a **dry 5.5-ft tension crack**. The crack depth comes straight from Slide's info box: the critical surface's right endpoint sits at el. 144.5 while its slope intercept is 150.0. Seed = Slide's printed critical (center (24.662, 197.656), R = 100.790).

**Input files:** [vp056.xlsx](files/rocscience/vp056.xlsx)

| Method | XSLOPE | Slide | Other published codes | Note |
|---|---|---|---|---|
| Bishop | 1.283 *(search 1.282)* | 1.285 (−0.2%) | 1.28 (+0.2%) | UTEXAS4 and SLOPE/W both publish 1.28 |
| Spencer | 1.288 *(search 1.288)* | 1.290 (−0.2%) | 1.29 (−0.2%) | UTEXAS4 and SLOPE/W both publish 1.29 |
| Lowe–Karafiath | 1.307 | 1.304 (+0.2%) | 1.31 (−0.2%) | UTEXAS4 |

![vp056: inputs and representative solution](images/vp056.png)

## 🟢 VP57: Pockoski & Duncan test slope 3 — composite vs. circles-only {#vp57}

Slide #57: Pockoski & Duncan (2000) test slope 3 — sandy clay (c' = 300 psf, φ' = 35°, γ = 130 pcf) over a 5-ft highly plastic clay seam (c' = 0, φ' = 25°) on the model base at el. 85, water table at ground on the lower plateau rising to 10 ft below the crest, dry 6-ft tension crack. The manual runs the problem twice, with and without composite surfaces, which makes it an A/B test of XSLOPE's `composite` option against the clamped default: Slide's printed composite critical bottoms below the base, so the surface truncates and rides the weak seam, while its circles-only critical is tangent to the base, exactly what a clamped search must settle for.

**Input files:** [vp057.xlsx](files/rocscience/vp057.xlsx)

| Method | XSLOPE composite | Slide composite | XSTABL (composite) | SLOPE/W (composite) | XSLOPE circles-only | Slide circles-only |
|---|---|---|---|---|---|---|
| Bishop | 1.389 | 1.392 (−0.2%) | — | — | 1.415 *(search 1.411)* | 1.417 (−0.1%) |
| Spencer | 1.396 | 1.400 (−0.3%) | — | — | 1.419 *(search 1.416)* | 1.422 (−0.2%) |
| Lowe–Karafiath | 1.387 | 1.385 (+0.1%) | — | — | 1.422 | 1.414 (+0.6%) |
| Ordinary | 1.086 | 1.257 (−13.6%) | — | 0.85 (+27.8%) | — | — |

*Bishop, Spencer and Lowe agree with Slide to 0.008 in both modes, and `circular_search(composite=True)` finds the truncated critical unaided (1.388 / 1.396). The Ordinary method is an outlier by design: the published OMS values span 0.85 (SLOPE/W) to 1.257 (Slide) on the composite surface, the pore-pressure pathology documented at [VP22](#vp22), and XSLOPE's 1.086 sits inside that spread.*

![vp057: inputs and representative solution](images/vp057.png)

## 🟢 VP58: Tied-back wall in layered soil {#vp58}

**Input files:** [vp058.xlsx](files/rocscience/vp058.xlsx)

Pockoski & Duncan (2000)'s fourth test slope, from their eight-program comparison of
reinforced-slope analysis: a 44-ft tied-back excavation wall in eight horizontal layers, water
table at grade in front of the wall and el. 102.5 behind it, with three identical tieback rows at
20° (88 ft, 40-ft bond, bond-governed at 40,000 lb/ft of wall). Evaluated on Slide's printed
critical circle, tangent to the glaciomarine contact.

| Method | XSLOPE | Slide | UTEXAS4 | SLOPE/W | WINSTABL |
|---|---|---|---|---|---|
| Bishop simplified | 1.142 | 1.147 (−0.4%) | 1.14 (+0.2%) | 1.14 (+0.2%) | 1.16 (−1.6%) |
| Spencer | 1.140 | 1.145 (−0.4%) | 1.14 (0.0%) | 1.14 (0.0%) | 1.20 (−5.0%) |
| Ordinary | 1.119 | 1.129 (−0.9%) | — | 1.12 (−0.1%) | — |

![vp058: inputs and representative solution](images/vp058.png)

## 🟢 VP59: Tieback wall in sand, drawdown water table {#vp59}

**Input files:** [vp059.xlsx](files/rocscience/vp059.xlsx)

Pockoski & Duncan (2000)'s fifth test slope: a single-row tieback wall in homogeneous sand
(c′ = 0, φ′ = 30°) with a water table drawn down to the wall face, under-designed on purpose so
that every published factor of safety is below 1. The critical surface is prescribed from Slide's
printout, running from the wall toe to the upper ground, and the water table enters with the
phreatic-inclination correction Slide and XSTABL apply on steeply inclined water tables.

| Method | XSLOPE | Slide | UTEXAS4 | SLOPE/W | WINSTABL |
|---|---|---|---|---|---|
| Corps / Lowe-Karafiath | 0.577 | 0.588 (−1.9%) | 0.76 (−24.1%) | — | — |
| Janbu (corrected) | 0.579 | 0.583 (simplified — cross-method) | 0.64 (simplified) | 0.61 (simplified) | 0.76 (simplified) |
| Bishop simplified | — | 0.582 | 0.56 | 0.60 | 0.74 |
| Spencer | — | 0.596 | 0.65 | 0.59 | — |
| Ordinary | — | 0.859 | — | — | — |

*This problem was built to stress reinforced-slope codes and it shows: the published Bishop
values alone span 0.56–0.74. Spencer finds no solution on this surface: its force and moment
residuals stay bounded away from zero over the whole admissible range of F and θ, so the single
constant interslice inclination admits no equilibrium here. Bishop and the Ordinary
method do not apply to a non-circular polyline, so the force-equilibrium family carries the lock.
The four sources publish Janbu simplified where XSLOPE reports the f₀-corrected value, so that row
is a cross-method bearing.*

![vp059: inputs and representative solution](images/vp059.png)

## 🟢 VP60: Soil-nailed wall with tension crack and surcharges {#vp60}

**Input files:** [vp060.xlsx](files/rocscience/vp060.xlsx)

Pockoski & Duncan (2000)'s seventh test slope: a 25-ft soil-nailed wall in undrained sandy clay
(c = 800 psf, φ = 0) carrying a 250-psf crest surcharge plus a 500-psf strip over the first 7.3 ft,
with a dry 7-ft tension crack and five passive nail rows at 15° (25,918 lb tensile at 5-ft spacing,
bond 1,508 lb/ft). Evaluated on Slide's printed critical circle, truncated by the crack at its
printed endpoint; at that geometry the top nail row passes above the truncated surface and does not
participate.

| Method | XSLOPE | Slide | UTEXAS4 | SLOPE/W | WINSTABL |
|---|---|---|---|---|---|
| Spencer | 1.010 | 1.009 (+0.1%) | 1.02 (−1.0%) | 1.02 (−1.0%) | 0.99 (+2.0%) |
| Janbu (corrected) | 1.073 | 1.041 (simplified — cross-method) | 1.08 (simplified) | 1.07 (simplified) | 1.10 (simplified) |

The nailed-wall codes and the limit-equilibrium codes disagree more with each other than the
limit-equilibrium codes do among themselves:

| Nailed-wall code, on its own mechanism | Published |
|---|---|
| GOLD-NAIL | 0.91 |
| SNAIL (wedge) | 0.84 |

![vp060: inputs and representative solution](images/vp060.png)

## 🟢 VP61: London clay, linear vs non-linear envelope (Baker ex. 3) {#vp61}

Slide #61 / Baker (2003) example problem 3: the same 43°, H = 6 m slope as [#44](#vp44), with strength functions fitted to Perry's CD triaxial data on London clay — (a) power curve τ = 3.39344·(σ′+0.152)^0.6 (Baker A = 0.535, n = 0.60, T = 0.0015) and (b) the fitted Mohr-Coulomb envelope c′ = 6.0 kPa, φ′ = 32°. Unlike the compacted-clay data of #44, this data set includes measurements at very low normal stress, so the two envelopes give similar factors of safety.

**Input files:** [vp061a.xlsx](files/rocscience/vp061a.xlsx), [vp061b.xlsx](files/rocscience/vp061b.xlsx)

| Case | Method | XSLOPE | Slide | Baker |
|---|---|---|---|---|
| (a) power curve | Spencer | 1.466 | 1.468 (−0.1%) | 1.48 (−0.9%) |
| (b) Mohr-Coulomb | Spencer | 1.367 | 1.366 (+0.1%) | 1.35 (+1.3%) |
| (a) power curve | Janbu simplified — cross-method | — | 1.348 | — |
| (b) Mohr-Coulomb | Janbu simplified — cross-method | — | 1.291 | — |

![vp061a: inputs and representative solution](images/vp061a.png)

![vp061b: inputs and representative solution](images/vp061b.png)

## 🟢 VP62: Slope, homogenous, ru pore pressure, seismic {#vp62}

Slide #62, dry at kc = 0.432 and at ru = 0.5 with kc = 0.132. Slide solves both with a circular
search, Loukidis with a log-spiral mechanism.

**Input files:** [vp062a.xlsx](files/rocscience/vp062a.xlsx), [vp062b.xlsx](files/rocscience/vp062b.xlsx)

*Dry, kc = 0.432*

| Method | XSLOPE | Slide | SLOPE/W | Loukidis |
|---|---|---|---|---|
| Bishop | 0.991 | 0.991 (0.0%) | 0.993 (−0.2%) | — |
| Spencer | 1.001 | 1.001 (0.0%) | 1.001 (0.0%) | 1.000 (+0.1%) |

*ru = 0.5, kc = 0.132*

| Method | XSLOPE | Slide | SLOPE/W | Loukidis |
|---|---|---|---|---|
| Bishop | 0.986 | 0.987 (−0.1%) | 0.988 (−0.2%) | — |
| Spencer | 1.001 | 1.001 (0.0%) | 1.001 (0.0%) | 1.000 (+0.1%) |

![vp062a: inputs and representative solution](images/vp062a.png)

![vp062b: inputs and representative solution](images/vp062b.png)

Also [SLOPE/W §2.38](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP63: Slope, (3) materials, seismic — critical seismic coefficient {#vp63}

**Input files:** [vp063.xlsx](files/rocscience/vp063.xlsx)

Loukidis, Bandini & Salgado (2003)'s second example: a three-layer dry slope (a weak φ = 15°
middle layer between a light c = 4 kPa cap and a strong φ = 45° base) loaded pseudo-statically at
the paper's critical seismic coefficient kc = 0.155, at which the factor of safety is exactly 1.
Loukidis analyzed a log-spiral mechanism and Slide a path search with Monte-Carlo optimization;
XSLOPE runs its noncircular search from a seed through the layer-2/3 daylight point the manual
identifies as a point on the critical surface.

|  | XSLOPE | Slide | Loukidis et al. |
|---|---|---|---|
| Spencer, noncircular search | 1.001 | 0.991 (+1.0%) | 1.000 (log-spiral, by definition of kc) |

The critical surface enters at the daylight point (35.8, 27.9) and exits on the crest at
x ≈ 121. The mechanism is genuinely noncircular: a circular search on the same model reads
several percent high. Geometry is calibrated from the Slide figure's vertex dots; Slide's
bench is 12 m wide where the paper's figure annotates 8 m, and Slide's model is the
factor-of-safety target here.

![vp063: inputs and representative solution](images/vp063.png)

## 🟢 VP64: USACE end-of-construction dam (EM 1110-2-1902 Fig. 4-1) {#vp64}

Slide #64 / USACE EM 1110-2-1902 (2003) Figure 4-1: the manual's Spencer hand-verification dam at end-of-construction — a symmetric 50-ft embankment at 4H:1V (undrained c=1000 psf, φ=5°) over a 10-ft sand blanket, foundation clay (c=3000, φ=0) and rock, with an embankment core trench through the sand, groundwater at the sand top, and a 7-ft crest tension crack. Evaluated on the specified circle (center (102,163), tangent to el. 0).

**Input files:** [vp064.xlsx](files/rocscience/vp064.xlsx)

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Spencer | 2.488 | 2.445 (+1.8%) | 2.44 (+2.0%) |
| Bishop | 2.489 | 2.447 (+1.7%) | — |

*Neither figure labels its vertices; the crest half-width (17 ft) and toes (±217) were pinned by reconciling USACE's printed slice table, and the residual is within that geometric uncertainty.*

![vp064: inputs and representative solution](images/vp064.png)

## 🟢 VP65: USACE dam, upstream low pool (EM 1110-2-1902 Fig. 4-2) {#vp65}

Slide #65: the [#64](#vp64) dam under steady low-pool conditions — drained strengths (embankment c = 100 psf, φ = 25°; sand 0/35; clay 0/28; rock 0/45, moist/saturated unit-weight splits), pool at el. 20 with the pond load on the submerged upstream face, no tension crack. Evaluated on USACE's printed circle (center (−102, 163), R = 173, tangent to the clay top). This dam is ponded on the upstream face only, and the piezometric line stops short of the downstream face at x = 117.778 as RS2's import of the model does. The printed circle daylights near x = 27, so the truncation does not touch the limit-equilibrium result; it matters to the [SSRM build](rs2.md#p4-vp65), which carries the field everywhere.

**Input files:** [vp065.xlsx](files/rocscience/vp065.xlsx)

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Bishop | 2.725 | 2.716 (+0.3%) | 2.71 (+0.6%) |
| Spencer | 2.748 | 2.736 (+0.4%) | — |

![vp065: inputs and representative solution](images/vp065.png)

## 🟢 VP66: USACE dam, chart-check properties (EM 1110-2-1902 Fig. 4-3) {#vp66}

Slide #66: the [#64](#vp64)/[#65](#vp65) dam family with the manual's chart-check property set (single unit weights: embankment c = 200 psf, φ = 25°, γ = 115; sand 0/35/130; clay 0/27/115), pool at el. 20, evaluated on Slide's printed circle (center (−135, 169), tangent to the sand top). Slide's printed slip endpoints show its model uses a slightly flatter face than its siblings, which is reproduced here. Unlike [#65](#vp65) this dam is ponded on **both** faces — the figure hatches ponded water upstream and downstream alike, and RS2's import carries hydrostatic tractions on both — so the file carries both ponds under a full-width piezometric line at el. 20. The printed circle is upstream, so the downstream pond does not enter the limit-equilibrium result; it is what lets the same file drive the [SSRM build](rs2.md#p4-vp66).

**Input files:** [vp066.xlsx](files/rocscience/vp066.xlsx)

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Spencer | 2.258 | 2.307 (−2.1%) | 2.30 (−1.8%) |
| Bishop | 2.254 | 2.307 (−2.3%) | — |

*The three Slide sibling models #64/#65/#66 carry three slightly different digitizations of the same USACE dam, so each is matched against its own printed evidence.*

![vp066: inputs and representative solution](images/vp066.png)

## 🟢 VP67: USACE end-of-construction embankment (example F-5) {#vp67}

Slide #67 / USACE EM 1110-2-1902 (2003) example F-5: a non-homogeneous embankment (c = 1780 psf, φ = 5°, γ = 135 pcf) on a 100-ft undrained fine-grained foundation (c = 1600 psf, φ = 2°, γ = 127 pcf), analyzed at end of construction. Slide's figure labels every vertex; the circle is centered 259 ft above and 101 ft right of the toe and passes through the toe (R = 278.0).

**Input files:** [vp067.xlsx](files/rocscience/vp067.xlsx)

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Spencer | 1.316 | 1.328 (−0.9%) | 1.33 (−1.1%) |
| Bishop | 1.320 | 1.332 (−0.9%) | — |
| Janbu (corrected) | 1.340 | 1.345 (−0.4%) | — |

![vp067: inputs and representative solution](images/vp067.png)

## 🟢 VP68: USACE φ=0 slope with ponded water (example E-10) {#vp68}

Slide #68 / USACE EM 1110-2-1902 example E-10: an undrained three-layer slope (c = 600/400/500 psf, γ = 120/100/105 pcf, all φ = 0) with 8 ft of water ponded against it (pool el. 0), fully labeled figure. The specified circle sits 8.4 ft right and 36 ft above the toe and is tangent to the base of soil 3 (center (48.4, 28), R = 48).

**Input files:** [vp068.xlsx](files/rocscience/vp068.xlsx)

| Method | XSLOPE | Slide | USACE (E-10 chart) |
|---|---|---|---|
| Bishop | 1.234 | 1.241 (−0.6%) | 1.33 (−7.2%) |
| Morgenstern-Price | 1.234 | 1.244 (GLE — cross-method) | — |

*Slide notes the same offset against the USACE chart solution. Spencer's base-tension guard declines this surface (base tension at the φ=0 crest slices); the root it declines is the 1.234 Bishop and Morgenstern-Price return, so M-P carries the complete-equilibrium comparison.*

![vp068: inputs and representative solution](images/vp068.png)

## 🟢 VP69: Steady-seepage dam with a piezometric line (USACE example F-6) {#vp69}

Slide #69 / USACE EM 1110-2-1902 example F-6: a 112-ft embankment (c' = 0, φ' = 34°, γ = 130 pcf) on a granular foundation (c' = 0, φ' = 35°, γ = 125 pcf) under steady seepage. Pore pressures come from the piezometric line, which leaves the pool surface at el. 100, drops to the chimney drain, follows it to the tailwater at el. 22.5 and runs out flat to the downstream face; USACE takes u as the vertical distance to that line, so the `phreatic` flag is off. The tailwater ponds the toe from x = 337.4 rightward. Specified circle: center (269, 248), R = 280, bottoming out on USACE's el. −32 stratum line.

**Input files:** [vp069.xlsx](files/rocscience/vp069.xlsx)

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Bishop | 1.999 | 2.011 (−0.6%) | 2.01 (−0.5%) |
| Spencer | 2.013 | 2.026 (−0.6%) | — |
| Morgenstern-Price | 2.013 | 2.027 (GLE — cross-method) | — |

*Slide's Figure 69.1 carries axis ticks and vertex markers, so the section was recovered exactly: ground (0,100)–(38.4,100)–(60.8,112)–(81,112)–(194.9,73.7)–(400,0)–(450,0). The rip-rap, chimney drain and drainage blanket take the embankment properties, as USACE does, and the circle misses all three. The uniform −0.6% offset is the residual of the piezometric-line kink, which the figure locates only to about a foot.*

![vp069: inputs and representative solution](images/vp069.png)

## 🟢 VP70: Submerged slope, two pool depths (D&W Fig. 6.27) {#vp70}

Slide #70 / Duncan & Wright (2005) Fig. 6.27: a fully submerged homogeneous slope (c = 100 psf, φ = 20°, γ = 128 pcf; (0,15)–(30,15)–(105,45)–(140,45)) analyzed with the pool 30 ft and then 60 ft above the crest, to show that the factor of safety is independent of submergence depth because the extra water weight and the extra pore pressure cancel. Pond loads over the whole submerged surface; free circular search.

**Input files:** [vp070a.xlsx](files/rocscience/vp070a.xlsx), [vp070b.xlsx](files/rocscience/vp070b.xlsx)

| Case | Method | XSLOPE | Slide | D&W |
|---|---|---|---|---|
| pool +30 ft | Bishop / Spencer | 1.596 / 1.593 | 1.603 / 1.599 (−0.4% / −0.4%) | 1.60 (−0.3% / −0.4%) |
| pool +60 ft | Bishop / Spencer | 1.596 / 1.593 | 1.603 / 1.599 (−0.4% / −0.4%) | 1.60 (−0.3% / −0.4%) |

*xslope reproduces the depth-independence exactly (identical FS at both pools) — a direct check on the consistency of the pond-load and pore-pressure treatments.*

![vp070a: inputs and representative solution](images/vp070a.png)
![vp070b: inputs and representative solution](images/vp070b.png)

## 🟢 VP71: FE seepage vs. piezometric line, same slope (D&W Figs. 6.37–6.38) {#vp71}

Slide #71 / Duncan & Wright (2005) Figs. 6.37 and 6.38: a homogeneous 2H:1V slope (c' = 200 psf, φ' = 20°, γ = 125 pcf; ground (0,40)–(120,40)–(200,80)–(440,80) over a base at el. 0) with water standing at el. 40 on the toe side and el. 75 behind the crest. The point of the example is that the same slope is solved two ways — pore pressures from a finite-element seepage analysis, and pore pressures from a piezometric line — and the two must agree.

Case 1 runs XSLOPE's own FE seepage solver (specified heads of 40 and 75 on the two vertical boundaries, the ground surface an exit face) and feeds the nodal pore pressures to the search through `u = 'seep'`; case 2 uses the piezometric line read off Slide's Figure 71.2. Free circular search in both.

**Input files:** [vp071a.xlsx](files/rocscience/vp071a.xlsx) (FE seepage), [vp071b.xlsx](files/rocscience/vp071b.xlsx) (piezometric line)

| Case | Method | XSLOPE | Slide | D&W |
|---|---|---|---|---|
| FE seepage | Bishop / Spencer | 1.132 / 1.132 | 1.141 / 1.141 (−0.8% / −0.8%) | 1.138 (−0.5% / −0.5%) |
| Piezometric line | Bishop / Spencer | 1.132 / 1.132 | 1.142 / 1.142 (−0.9% / −0.9%) | 1.141 (−0.8% / −0.8%) |

*The two pore-pressure models land within 0.0006 of each other, the same near-identity Slide reports (1.141 vs 1.142): the corpus's end-to-end check that a phreatic surface computed from scratch reproduces the one Duncan & Wright drew.*

![vp071a: inputs and representative solution](images/vp071a.png)
![vp071b: inputs and representative solution](images/vp071b.png)

## 🟢 VP72: Dam on a layered foundation — underseepage and artesian uplift (D&W Fig. 6.39) {#vp72}

Slide #72 / Duncan & Wright (2005) Figs. 6.39–6.40: a symmetric embankment dam (3:1 shell faces, 90 ft high, narrow 0.5H:1V clay core) on a **layered foundation** — 30 ft of clay over 15 ft of much more permeable sand — with pond at el. 302 and tailwater at the downstream ground. Elevations, slopes and properties come from D&W's figure, x-coordinates from vertex extraction of Slide's Figure 72.1. The example exists for the underseepage: flow through the sand pushes upward beneath the downstream shell, which a single piezometric line cannot represent, and D&W's FS with FE pore pressures is 14–19% lower than with the piezo line. One modeling detail matters enormously — Slide's boundary-condition markers show no-flow vertical edges, so the heads sit on the ground surface only and all underseepage is forced up through the clay. Giving the sand a fixed-head exit at the model edge instead guts the artesian pressures and reads ~13% high; with the correct conditions XSLOPE's field puts u at the toe 40% above hydrostatic, and 65% at 5 ft depth.

Pore pressures are modeled both ways, as in the manual: FE seepage from XSLOPE's own solver, and
Slide's piezometric line vertex-extracted from Figure 72.2. This dam is also
[LEM sample problem 8](../lem/samples.md#8-earth-dam), built independently from the book; the
corpus file follows Slide's slightly different crest and core-top dimensions rather than the
book's, since Slide's published numbers are the benchmark here.

**Input files:** [vp072a.xlsx](files/rocscience/vp072a.xlsx) (FE seepage), [vp072b.xlsx](files/rocscience/vp072b.xlsx) (piezometric line)

| Case | Method | XSLOPE (tangent 197) | Slide | D&W |
|---|---|---|---|---|
| FE seepage | Bishop | 1.339 | 1.312 (+2.1%) | 1.37 (−2.3%) |
| FE seepage | Spencer | 1.341 | 1.312 (+2.2%) | 1.37 (−2.1%) |
| Piezometric line | Bishop | 1.572 | 1.563 (+0.6%) | 1.57 (+0.1%) |
| Piezometric line | Spencer | 1.563 | 1.557 (+0.4%) | 1.57 (−0.4%) |

*The tagged benchmarks are the circles tangent to el. 197, the bottom of the foundation clay — D&W's own reported case, well-posed and reproducible. The global critical is deliberately not tagged: it is a shallow toe slough driven by the artesian exit gradient, so its factor of safety depends on the minimum admissible surface size, and Slide does not print its critical surface.*

![vp072a: inputs and representative solution](images/vp072a.png)

The piezometric-line case for comparison (Slide's line from Figure 72.2, with its tangent-197 critical):

![vp072b: inputs and representative solution](images/vp072b.png)

## 🟢 VP73: The Bradwell excavated slope (Skempton & LaRochelle 1965) {#vp73}

Slide #73 / Duncan & Wright (2005): the excavated slope for reactor 1 at Bradwell — one of the classic case histories of short-term failure in stiff-fissured clay. The lower excavation is cut at ½:1 in London Clay; the overlying Marsh Clay and the clay fill (spoil, placed back on the Marsh Clay) are both at 1:1. The fill is cracked to its full depth (11.4 ft).

London Clay is stratified into six sublayers, each with an undrained strength that grows linearly with depth, S<sub>u</sub> = c<sub>z</sub> + (y<sub>z</sub> − y)·Δc<sub>z</sub>. That is precisely XSLOPE's `cp` option, so the six rows of Slide's Table 73.2 map straight onto six materials — with the two upper units (clay fill, Marsh Clay) that makes eight. Free circular search.

**Input files:** [vp073.xlsx](files/rocscience/vp073.xlsx)

| Method | XSLOPE | Slide | D&W |
|---|---|---|---|
| Bishop | 1.766 | 1.762 (+0.2%) | 1.76 (+0.3%) |
| Spencer | 1.766 | 1.758 (+0.5%) | 1.76 (+0.3%) |
| Janbu (corrected) | 1.733 | 1.736 (−0.2%) | 1.74 (−0.4%) |

*Every method within 0.5% — the tightest agreement of the Duncan & Wright group, and a good check that the stratified `cp` profile and the full-depth tension crack compose correctly.*

![vp073: inputs and representative solution](images/vp073.png)

## 🟢 VP74: Sand embankment on saturated clay (D&W Fig. 7.12) {#vp74}

Slide #74 / Duncan & Wright (2005) Fig. 7.12: a 100-ft cohesionless embankment (c=0, φ=40°, γ=140 pcf) on a 50-ft saturated clay foundation (c=2500 psf, φ=0); fully labeled figure, imperial units, dry. Free circular search.

**Input files:** [vp074.xlsx](files/rocscience/vp074.xlsx)

| Method | XSLOPE (search) | Slide | D&W |
|---|---|---|---|
| Bishop | 1.219 | 1.228 (−0.7%) | 1.22 (−0.1%) |
| Spencer | 1.194 | 1.201 (−0.6%) | 1.19 (+0.3%) |
| Janbu (corrected) | 1.161 | 1.174 (−1.1%) *(Slide's simplified value is 1.079 — cross-method)* | 1.07 (simplified — cross-method) |

![vp074: inputs and representative solution](images/vp074.png)

## 🟢 VP75: The James Bay dyke (D&W Fig. 7.16) {#vp75}

Slide #75 / Duncan & Wright (2005) Fig. 7.16: one of the planned James Bay dykes — a granular fill embankment with a wide berm (ground (−17,31)–(40,31)–(58,25)–(114,25)–(132,19)–(168,19), metric) resting on three soft clay units: a 4 m crust (c = 41 kN/m²), 8 m of marine clay (34.5) and 7 m of lacustrine clay (31.2), all φ = 0. Fill c' = 0, φ' = 30°. Free circular search.

**Input files:** [vp075.xlsx](files/rocscience/vp075.xlsx)

| Method | XSLOPE (search) | D&W | Slide (own circle) |
|---|---|---|---|
| Bishop | 1.424 | 1.45 (−1.8%) | 1.468 |
| Spencer | 1.420 | — | 1.464 |

*The critical surface is a deep circle tangent to the base of the lacustrine clay, cutting all three foundation units. This problem is the corpus's local-minimum showcase: from a single mid-depth seed the 9-point descent settles onto a base-tangent local minimum that exits through the berm — converged, plausible-looking, and well above the true minimum with no warning — so the input file carries three seeds spanning shallow to deep. [Grid seeding](../lem/search.md#grid-seeding-global-search) (`seed='grid'`) removes the trap entirely: with the circles sheet ignored it finds Spencer 1.420 on its own, and that is regression-locked alongside the seeded search.*

![vp075: inputs and representative solution](images/vp075.png)

Also [SLOPE/W §2.44](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP76: Homogeneous dam, FE seepage vs. piezometric line (D&W Fig. 7.19) {#vp76}

Slide #76 / Duncan & Wright (2005) Fig. 7.19: a homogeneous earth embankment (c' = 100 psf, φ' = 30°, γ = 100 pcf) on an impermeable foundation, ground (0,0)–(100,40)–(120,48)–(135,48)–(255,0), with the pool at el. 40 covering the entire upstream face. As in VP71, pore pressures are modeled two ways — an FE seepage analysis and a piezometric line — and the critical circle is found by free search.

**Input files:** [vp076a.xlsx](files/rocscience/vp076a.xlsx) (FE seepage), [vp076b.xlsx](files/rocscience/vp076b.xlsx) (piezometric line)

| Case | Method | XSLOPE | Slide | D&W |
|---|---|---|---|---|
| FE seepage | Bishop / Spencer | 1.065 / 1.072 | 1.068 / 1.075 (−0.3% / −0.3%) | 1.19 & 1.08 (chart) — a published band, not one value |
| Piezometric line | Bishop / Spencer | 1.070 / 1.078 | 1.090 / 1.100 (−1.8% / −2.0%) | 1.16 (−7.8% / −7.1%) |

*The FE case lands within 0.6% of Slide, and XSLOPE's computed phreatic surface tracks the line Slide digitized from Duncan & Wright to better than a foot everywhere. The piezometric case carries Slide2's own nine vertices, read from its model rather than traced off the figure, including a break just below the waterline that a raster reading misses. That matters because the problem is ill-conditioned: the critical circle is a shallow toe surface where the water table is nearly at the ground, effective stresses are small, and dropping the line by half a foot raises Bishop by 6%, while on the exact vertices both methods land within 2% of Slide.*

![vp076a: inputs and representative solution](images/vp076a.png)
![vp076b: inputs and representative solution](images/vp076b.png)

## 🟢 VP77: Thick-core dam, FE seepage vs. piezometric line (D&W Fig. 7.24) {#vp77}

Slide #77 / Duncan & Wright (2005) Fig. 7.24: a symmetric earth dam with a thick clay core on an impervious foundation, pond at el. 315. Geometry comes from D&W's coordinate-labeled figure — shell faces 2.75:1 to an 80-ft crest at el. 338, the core a trapezoid with 1.5:1 faces and a 50-ft top at el. 328. Core c' = 0, φ' = 20°, γ = 120 pcf, k = 10⁻⁵ ft/min; shell c' = 0, φ' = 38°, γ = 140 pcf, k = 10⁻³, a 100:1 contrast. Both zones are cohesionless, so the benchmark targets the deep circle tangent to the base at el. 127, where both of Slide's printed criticals bottom out.

Like VP71 and VP76, pore pressures are modeled two ways: XSLOPE's own FE seepage (head 315 on the submerged upstream face, exit face downstream, no-flow base), whose phreatic surface drops from 312 to 231 across the core and runs near-flat at el. ~134 through the downstream shell as D&W's Fig. 7.38 does; and Slide's piezometric line, extracted from Figure 77.2 by axis-tick-calibrated vertex detection, whose detected vertices land on the core's 1.5:1 face at (572, 312) and the downstream face at (1182, 148).

**Input files:** [vp077a.xlsx](files/rocscience/vp077a.xlsx) (FE seepage), [vp077b.xlsx](files/rocscience/vp077b.xlsx) (piezometric line)

| Method | XSLOPE FE seepage | Slide FE seepage | XSLOPE piezo line | Slide piezo line |
|---|---|---|---|---|
| Bishop | 1.652 *(search 1.637)* | 1.658 (−0.4%) | 1.591 *(search 1.566)* | 1.584 (+0.4%) |
| Spencer | 1.724 *(search 1.700)* | 1.724 (0.0%) | 1.659 | 1.648 (+0.7%) |
| Morgenstern–Price | 1.734 | — | 1.670 | — |
| Ordinary | 1.506 | — | 1.477 | — |

*Values on Slide's printed circles; the free-search values in parentheses are slightly deeper circles of the same family. D&W's four-program Spencer spread for the FE case is 1.67–1.72, and XSLOPE's 1.724 sits at its top edge, equal to Slide's own manual value. One numerical note from the seepage run: the unsaturated front width must scale with the dam (h0 = −5 ft ≈ one element, the sharpest the mesh resolves; the VP76-style −1 ft is sub-grid here and the fixed-point iteration never converges).*

![vp077a: inputs and representative solution](images/vp077a.png)
![vp077b: inputs and representative solution](images/vp077b.png)

## 🟢 VP78: Pure cohesive slope on a foundation (D&W Fig. 14.3) {#vp78}

Slide #78 / Duncan & Wright (2005) Fig. 14.3: c = 1000 psf, φ = 0, γ = 100 pcf; a 50-ft slope at 1V:0.8H over a 30-ft foundation ((0,30)–(90,30)–(130,80)–(240,80), base at y = 0, all vertices labeled in Slide's figure). For φ = 0 the critical circle is the deep, base-tangent one, which the free search finds directly.

**Input files:** [vp078.xlsx](files/rocscience/vp078.xlsx)

| Method | XSLOPE (search) | Slide (base-tangent) | Slide (toe circle — a different surface) | D&W |
|---|---|---|---|---|
| Bishop | 1.117 | 1.141 (−2.1%) | 1.126 | 1.124 (−0.6%) |
| Spencer | 1.131 | 1.139 (−0.7%) | 1.200 | — |

*xslope's free search reaches slightly below Slide's tangent-line-constrained minimum. Slide's toe-circle rows repeat identically for the 46.5-ft and 60-ft foundation variants, so only the 30-ft model is built.*

![vp078: inputs and representative solution](images/vp078.png)

## 🟢 VP79: Cohesionless embankment on a φ=0 foundation (D&W Fig. 14.4) {#vp79}

Slide #79 / Duncan & Wright (2005) Fig. 14.4: a c=0, φ=30°, γ=120 pcf embankment (15 ft high at ~21.5°) over a 20-ft φ=0 foundation with c=450 psf; geometry fully labeled in Slide's figure ((0,20)–(40,20)–(78,35)–(130,35), base y=0). The critical mechanism is the deep circle tangent to the base; the shallow infinite-slope mechanism does not govern.

**Input files:** [vp079.xlsx](files/rocscience/vp079.xlsx)

| Method | XSLOPE (search) | Slide | D&W |
|---|---|---|---|
| Bishop | 1.407 | 1.412 (−0.4%) | 1.40 (+0.5%) |
| Spencer | 1.397 | 1.400 (−0.2%) | — |

![vp079: inputs and representative solution](images/vp079.png)

## 🟢 VP80: Embankment on a stratified foundation (D&W Fig. 14.5) {#vp80}

Slide #80 / Duncan & Wright (2005) Fig. 14.5: an embankment (c=1 psf, φ=35°, γ=120 pcf) over five alternating φ=0 clay and c≈0 sand layers (fully labeled figure, imperial units). Two circles from the published center (142, 147): tangent to the foundation top (R=87) and tangent to the 15-ft-depth line (R=102) — the deeper circle drops FS from ~2.5 to ~1.35 as it engages the 500-psf clay.

**Input files:** [vp080a.xlsx](files/rocscience/vp080a.xlsx), [vp080b.xlsx](files/rocscience/vp080b.xlsx)

| Case | Method | XSLOPE | Slide | D&W |
|---|---|---|---|---|
| tangent 0 ft | Bishop / Spencer | 2.533 / 2.530 | 2.549 / 2.545 (−0.6% / −0.6%) | 2.56 (−1.1% / −1.2%) |
| tangent 15 ft | Bishop / Spencer | 1.389 / 1.352 | 1.398 / 1.359 (−0.6% / −0.5%) | 1.35 (+2.9% / +0.1%) |

![vp080a: inputs and representative solution](images/vp080a.png)

![vp080b: inputs and representative solution](images/vp080b.png)

## 🟢 VP81: Embankment on a φ=0 foundation (D&W Fig. 14.7) {#vp81}

Slide #81 / Duncan & Wright (2005) Fig. 14.7: a c=0, φ=30°, γ=124 pcf embankment (19 ft at ~26.6°) over a 15-ft φ=0 foundation with c=500 psf, γ=98 pcf; geometry fully labeled in Slide's figure ((0,15)–(35,15)–(73,34)–(128,34), base y=0). The deep base-tangent circle governs.

**Input files:** [vp081.xlsx](files/rocscience/vp081.xlsx)

| Method | XSLOPE (search) | Slide | D&W |
|---|---|---|---|
| Bishop | 1.223 | 1.230 (−0.6%) | 1.21 (+1.1%) |
| Spencer | 1.204 | 1.209 (−0.4%) | — |

![vp081: inputs and representative solution](images/vp081.png)

## 🟢 VP82: Embankment with a water table (D&W Fig. 14.20-a) {#vp82}

Slide #82 / Duncan & Wright (2005) Fig. 14.20-a: an embankment (c' = 600 psf, φ' = 25°, γ = 125 pcf; ground (0,60)–(60,60)–(140,20)–(200,20)) on a cohesionless foundation (c' = 0, φ' = 30°, γ = 132 pcf), with a piezometric line running (0,40)–(100,30)–(140,20)–(200,20). Free circular search.

**Input files:** [vp082.xlsx](files/rocscience/vp082.xlsx)

| Method | XSLOPE | Slide | D&W |
|---|---|---|---|
| Bishop | 1.521 | 1.533 (−0.8%) | 1.535 (−0.9%) |
| Spencer | 1.533 | 1.540 (−0.5%) | — |

![vp082: inputs and representative solution](images/vp082.png)

## 🟢 VP83: Embankment wall on an undrained foundation (D&W Fig. 14.20-b) {#vp83}

Slide #83 / Duncan & Wright (2005) Fig. 14.20-b: an embankment (c' = 0, φ' = 36°, γ = 123 pcf; ground (0,40)–(55,40)–(75,30)–(140,30)) on a 30-ft undrained foundation (φ = 0, γ = 97 pcf) down to a base at el. 0. Two foundation strength profiles are tested: profile I increases with depth, c<sub>u</sub> = 200 + 15·z psf, and profile II is constant at 300 psf. Free circular search.

Profile I uses XSLOPE's `cp` strength option, which is exactly this form — an undrained strength `c` at a reference elevation `r_elev`, growing at rate `cp` per foot below it.

**Input files:** [vp083a.xlsx](files/rocscience/vp083a.xlsx) (profile I), [vp083b.xlsx](files/rocscience/vp083b.xlsx) (profile II)

| Case | Method | XSLOPE | Slide | D&W |
|---|---|---|---|---|
| I: c<sub>u</sub> = 200 + 15·z | Bishop / Spencer | 1.305 / 1.275 | 1.313 / 1.285 (−0.6% / −0.8%) | 1.300 (+0.4% / −1.9%) |
| II: c<sub>u</sub> = 300 | Bishop / Spencer | 1.328 / 1.326 | 1.335 / 1.330 (−0.5% / −0.3%) | 1.312 (+1.2% / +1.1%) |

*With the constant profile the critical circle runs all the way down to the base of the foundation, as Slide notes; the free search finds it without being told to.*

![vp083a: inputs and representative solution](images/vp083a.png)
![vp083b: inputs and representative solution](images/vp083b.png)

## 🟢 VP84: Embankment on a foundation with four strength gradients (D&W Fig. 15.9) {#vp84}

Slide #84 / Duncan & Wright (2005) Fig. 15.9: an embankment (c' = 0, φ' = 35°, γ = 125 pcf; ground (0,20)–(40,20)–(90,40)–(140,40)) on a 20-ft undrained foundation (φ = 0, γ = 100 pcf) whose strength is c<sub>u</sub> = 300 + c<sub>z</sub>·z. The same slope is run with four strength gradients, c<sub>z</sub> = 0, 5, 10 and 15 psf/ft — a systematic sweep of the `cp` option.

**Input files:** [vp084a.xlsx](files/rocscience/vp084a.xlsx), [vp084b.xlsx](files/rocscience/vp084b.xlsx), [vp084c.xlsx](files/rocscience/vp084c.xlsx), [vp084d.xlsx](files/rocscience/vp084d.xlsx)

| Profile | c<sub>z</sub> (psf/ft) | XSLOPE Bishop / Spencer | Slide | D&W |
|---|---|---|---|---|
| I | 0 | 0.756 / 0.751 | 0.761 / 0.756 (−0.7% / −0.7%) | 0.75 (+0.8% / +0.1%) |
| II | 5 | 0.905 / 0.897 | 0.909 / 0.898 (−0.4% / −0.1%) | 0.90 (+0.6% / −0.3%) |
| III | 10 | 1.042 / 1.028 | 1.045 / 1.032 (−0.3% / −0.4%) | 1.03 (+1.2% / −0.2%) |
| IV | 15 | 1.151 / 1.131 | 1.154 / 1.134 (−0.3% / −0.3%) | 1.13 (+1.9% / +0.1%) |

*Four gradients on one geometry: the whole family tracks Slide within 0.7% and D&W within 1%, and with VP83 exercises the depth-varying undrained strength option from constant to 15 psf/ft.*

![vp084a: inputs and representative solution](images/vp084a.png)
![vp084b: inputs and representative solution](images/vp084b.png)
![vp084c: inputs and representative solution](images/vp084c.png)
![vp084d: inputs and representative solution](images/vp084d.png)

## 🟢 VP85: Reinforced slope, homogenous, grouted tieback {#vp85}

Slide #85 case 1 applies the tieback as active support, case 2 as passive; each is
evaluated on the circle Slide prints for it.

**Input files:** [vp085a.xlsx](files/rocscience/vp085a.xlsx), [vp085b.xlsx](files/rocscience/vp085b.xlsx)

*Active support, on Slide’s printed GLE circle*

| Method | XSLOPE | Slide | D&W |
|---|---|---|---|
| Bishop | 1.567 | 1.575 (GLE on the same circle — cross-method) | 1.51 (+3.8%) |
| Spencer | 1.567 | 1.575 (GLE on the same circle — cross-method) | — |
| Bishop, on Slide's own searched circle | — | 1.531 (a different surface) | — |
| Slide's own spread across all its methods | — | 1.42–2.05 | — |

*Passive support, on Slide’s printed Bishop circle*

| Method | XSLOPE | Slide (Bishop, same circle) | D&W |
|---|---|---|---|
| Ordinary | 1.319 | 1.324 (Bishop — cross-method) | 1.32 (−0.1%) |
| Bishop | 1.319 | 1.324 (−0.4%) | 1.32 (−0.1%) |

*The concentrated support force strains the interslice assumptions, which is why Slide’s own
methods scatter so widely here and why the per-circle comparison is the meaningful one.*

![vp085a: inputs and representative solution](images/vp085a.png)

![vp085b: inputs and representative solution](images/vp085b.png)

The problem is Duncan & Wright (2005) Fig. 6.34; the tieback carries 9,000 lb/ft, applied horizontally at mid-height of the slope.

## 🟢 VP86: Reinforced slope, homogenous, grouted tieback {#vp86}

Slide #86: Duncan & Wright (2005) Fig. 7.28 / STABGM reinforced fill on a strong rock foundation: 5 geogrids (800 lb/ft, 20 ft long, every 4 ft), solved by Slide2 with a circular search.

**Input files:** [vp086.xlsx](files/rocscience/vp086.xlsx)

| Method | XSLOPE | Slide | D&W |
|---|---|---|---|
| Bishop | 1.617 | 1.629 (−0.7%) | 1.61 (+0.4%) |
| Spencer | 1.611 | 1.620 (−0.6%) | 1.61 (+0.1%) |
| Slide2 GLE — cross-method, no XSLOPE counterpart | — | 1.622 | — |

![vp086: inputs and representative solution](images/vp086.png)

## 🟢 VP87–VP94: Geosynthetic multitiered MSE walls (Leshchinsky & Han 2004) {#vp87}

**Input files:** [vp087.xlsx](files/rocscience/vp087.xlsx) · [vp088.xlsx](files/rocscience/vp088.xlsx) ·
[vp089.xlsx](files/rocscience/vp089.xlsx) · [vp090.xlsx](files/rocscience/vp090.xlsx) ·
[vp091.xlsx](files/rocscience/vp091.xlsx) · [vp092.xlsx](files/rocscience/vp092.xlsx) ·
[vp093.xlsx](files/rocscience/vp093.xlsx) · [vp094.xlsx](files/rocscience/vp094.xlsx)

Slide #87–#94 reproduce the parametric study in [Leshchinsky & Han (2004)](https://doi.org/10.1061/(ASCE)1090-0241(2004)130:12(1225)): a three-tier segmental MSE wall — three 3-m tiers offset 1.2 m, 0.3-m block columns (c = 2.5 kPa, φ = 34°), reinforced and retained fill c = 0 / φ = 34°, foundation c = 10 kPa / φ = 34° 6 m deep, γ = 18 kN/m³ throughout — with geotextile layers every 0.6 m, L = 6.3 m, at the tensile strength Ta the paper required for FS = 1.0 in each variation. Pullout resistance is 80% of the fill strength and the geotextile force is applied horizontally (`dir=axial`, `appl=passive`, Slide's convention). Each problem's Slide-printed critical circle is stored in its file, so the tags evaluate a deterministic surface.

Two quirks in the manual: Slide's VP89/92/93 results were computed with the baseline Ta = 10
supports even though their support tables print the paper's per-case required strengths, so on
those rows Slide's value and the locked run are not on the same basis; and VP91's printed circle
exits exactly tangent to the crest and needs a hair of extra radius to intersect.

| # | Case | Method (Slide's figure) | XSLOPE | Slide | L&H FLAC continuum | L&H Bishop (design target, 1.00 by construction) |
|---|---|---|---|---|---|---|
| 87 | Baseline (Ta=10) | Bishop | 1.031 | 1.040 (−0.9%) | 0.99 | 1.00 |
| 88 | Fill φ=25 (Ta=22) | Spencer | 1.057 | 1.043 (+1.3%) | 0.99 | 1.00 |
| 89 | L=4.2 m (Ta=11.4) | Spencer | 1.011 | 0.971 *(used Ta=10 — cross-basis)* | 0.98 | 1.00 |
| 90 | Two types (7.5/11.0) | Bishop | 1.012 | 1.004 (+0.8%) | 1.01 | 1.00 |
| 91 | Foundation c=0, φ=18 | Spencer | 0.960 | 0.964 (−0.4%) | 0.86 (bearing mechanism) | 1.00 |
| 92 | Water hw=3 m (Ta=9.25) | Bishop | 1.010 | 1.037 *(used Ta=10 — cross-basis)* | 1.01 | 1.00 |
| 93 | Surcharge q=20 (Ta=10) | Bishop | 0.961 | 0.958 (+0.3%) | 1.02 | 1.00 |
| 94 | Five 1.8-m tiers (Ta=10.1) | Bishop | 1.020 | 1.040 (−1.9%) | — | 1.00 |

*VP92 models the paper's hw as pore pressure in the foundation soil only (a drained MSE fill), plus the 3-m pond standing against the lower tier; treating the fill as saturated instead reconciles with neither program. XSLOPE's free circular search finds slightly more critical circles than Slide's grid on several of these.*

![vp087: inputs and representative solution](images/vp087.png)

![vp088: inputs and representative solution](images/vp088.png)

![vp089: inputs and representative solution](images/vp089.png)

![vp090: inputs and representative solution](images/vp090.png)

![vp091: inputs and representative solution](images/vp091.png)

![vp092: inputs and representative solution](images/vp092.png)

![vp093: inputs and representative solution](images/vp093.png)

![vp094: inputs and representative solution](images/vp094.png)

In VP90 the upper 8 geotextile layers carry Ta = 7.5 and the lower 7 carry Ta = 11.0; VP93's Ta = 10 is also the value stored in the RS2 vendor `.fez`.

## ⊘ VP95: USACE Appendix G dam, Corps 2-stage drawdown method {#vp95}

Slide #95 runs the USACE EM 1110-2-1902 (1970) Appendix G example — the same dam that
[VP96](#vp96) builds — through the **Corps of Engineers 2-stage** rapid-drawdown
procedure and its R-envelope.

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Corps of Engineers 2-stage drawdown | — *not implemented* | 1.347 | 1.35 |

XSLOPE implements the Duncan, Wright & Wong (1990) **3-stage** procedure that superseded the
2-stage method — the one the later edition of the same manual carries, and the one every drawdown
problem in this corpus is solved with. It is verified on this very dam in [VP96](#vp96) and on six
further drawdown problems in VP97–VP102, so the omission is a deliberate scope exclusion rather
than a gap.

## 🟢 VP96: Embankment dam, homogenous, rapid drawdown, water table {#vp96}

Slide #96 / USACE EM 1110-2-1902 (2003) Appendix G example: 3:1 then 2.5:1 embankment face, max pool el. 103 drawn down to 24, specified circle (169.5, 210, R=210). Material: c'=0, phi'=30, gamma=135 pcf with the Kc=1 envelope d=1379 psf, psi=18.2 deg (Figure G-5). Solved with the Duncan-Wright-Wong 3-stage procedure. (Slide's #95 runs the same model with the older Corps 2-stage method — see [VP95](#vp95).)

**Input files:** [vp096.xlsx](files/rocscience/vp096.xlsx)

| Method | XSLOPE | Slide | USACE |
|---|---|---|---|
| Bishop | 1.432 | 1.443 (−0.8%) | 1.44 (−0.6%) |
| Spencer | 1.434 | 1.443 (−0.6%) | 1.44 (−0.4%) |

![vp096: inputs and representative solution](images/vp096.png)

Also [SLOPE/W §2.41](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP97: Embankment dam, homogenous, rapid drawdown, water table {#vp97}

Slide #97: Pilarcitos Dam (Duncan, Wright & Wong 1990). Homogeneous earthfill, gamma=135 pcf, c'=0, phi'=45; R-envelope cR=60 psf, phiR=23. Kc=1 envelope via D&W (2014) eqs 9.6-9.7: d = cR cos(phiR) cos(phi') / (1-sin(phiR)) = 64.1 psf, psi = 24.4 deg (the same equations reproduce the USACE App G values 1379/18.2 exactly). Drawdown 72 -> 37 ft.

**Input files:** [vp097.xlsx](files/rocscience/vp097.xlsx)

| Method | XSLOPE | Slide | DWW |
|---|---|---|---|
| Bishop | 1.042 | 1.043 (−0.1%) | 1.05 (−0.8%) |
| Spencer | 1.044 | 1.043 (+0.1%) | 1.05 (−0.6%) |
| Corps 2-stage — not implemented, superseded by the DWW 3-stage procedure | — | 0.823 | 0.82 |

*The dam that actually failed in drawdown sits right at FS ≈ 1.*

![vp097: inputs and representative solution](images/vp097.png)

Also [SLOPE/W §2.43](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP98: Walter Bouldin Dam rapid drawdown (Duncan, Wright & Wong 1990) {#vp98}

Slide #98: the Walter Bouldin Dam failure case — a rolled earthfill dam that failed during a 32-ft drawdown in 1975, pool 47 ft → 15 ft. Its five zones are rebuilt from Slide's coordinate-labeled Figure 98.1 with the interior boundaries traced from its color zones; the Kc = 1 undrained envelopes come from the paper's own Table 2, with riprap and gravel drained.

**Input files:** [vp098.xlsx](files/rocscience/vp098.xlsx)

| Method | XSLOPE | Slide | DWW |
|---|---|---|---|
| DWW 3-stage (Spencer, circular search) | 1.046 | 1.039 (+0.7%) | 1.04 (+0.6%) |
| Corps 2-stage — not implemented | — | 0.931 | — |
| Lowe & Karafiath staged — not implemented | — | 1.075 | — |

*The critical circle ((52,21)→(157,60)) falls where the dam actually slid.*

![vp098: inputs and representative solution](images/vp098.png)

Also [SLOPE/W §2.40](geostudio.md) — the same problem in the GeoStudio corpus.

## 🟢 VP99: Pumped-storage project dam rapid drawdown (DWW 1990) {#vp99}

Slide #99: the paper's hypothetical pumped-storage dam — silty clay core and random zone (c′=0, φ′=36°, Kc=1 envelope 2250 psf/20°), free-draining rockfill shells (φ′=37°), drawdown 285 ft → 120 ft (paper El 545 → 380). The core and random zone carry identical strengths, so only the rockfill/clay boundary affects the result.

The geometry is **re-pinned from the vendor GeoStudio model** of the same DWW problem ([SLOPE/W §2.42](geostudio.md)), read with `xslope.geostudio.read_gsz`, because Slide's Figure 99.1 is unlabeled and a trace of it gives a dam ≈19 ft short in crest-to-base height. The `.gsz` point table fixes the section exactly: translated by y−260 to keep the 285/120 pool levels, it puts the base at −10, the crest at 290, and the three upstream benches at el. 60/120/190. The two vendors' figures genuinely differ, and GeoStudio's is the one that matches the published factor of safety.

**Input files:** [vp099.xlsx](files/rocscience/vp099.xlsx)

| Method | XSLOPE | Slide | SLOPE/W | DWW |
|---|---|---|---|---|
| DWW 3-stage (Spencer, circular search) | 1.527 | 1.534 (−0.5%) | 1.550 (−1.5%) | 1.56 (−2.1%) |

*With the vendor geometry XSLOPE lands within 0.5% of Slide (1.527 vs 1.534) and inside the published band.*

![vp099: inputs and representative solution](images/vp099.png)

## 🟢 VP100: Embankment dam, homogenous, rapid drawdown, water table {#vp100}

Slide #100: complete drawdown (100 -> 0), B-bar = 1: the residual pore pressure is hydrostatic below the slope surface, i.e. piezo = ground, no external pond.

**Input files:** [vp100.xlsx](files/rocscience/vp100.xlsx)

*Complete drawdown (100 → 0)*

| Method | XSLOPE | Morgenstern chart | Slide |
|---|---|---|---|
| Bishop | 1.201 | 1.20 (+0.1%) | 1.212 (B-bar) (−0.9%) |
| Spencer | 1.206 | — | — |

![vp100: inputs and representative solution](images/vp100.png)

## 🟢 VP101: Embankment dam, homogenous, rapid drawdown, water table {#vp101}

Slide #101: partial drawdown (100 -> 50), B-bar = 1: piezo follows the ground where the face is above the pool and stays at 50 below it, with the remaining pond loading the submerged face.

**Input files:** [vp101.xlsx](files/rocscience/vp101.xlsx)

*Partial drawdown (100 → 50)*

| Method | XSLOPE | Slide | Morgenstern chart |
|---|---|---|---|
| Bishop | 1.416 | 1.417 (−0.1%) | 1.41 (+0.4%) |
| Spencer | 1.422 | — | — |

![vp101: inputs and representative solution](images/vp101.png)

## 🟢 VP102: Earth dam before rapid drawdown (Huang & Jia 2008) {#vp102}

Slide #102 / Huang & Jia (2008): a homogeneous earth dam (c' = 13.8 kPa, φ' = 37°, γ = 18.2 kN/m³; ground (0,7.3)–(33.5,7.3)–(86.66,24.39)–(99.75,28.6)–(107.05,28.6)–(157.9,7.3)–(191.4,7.3)) whose reservoir at el. 24.39 is drawn down instantaneously to the tailwater at el. 7.3, with factors of safety reported at 60–1500 h. This entry reproduces the two end members Slide reports separately — the dry dam and the initial steady seepage condition the drawdown starts from — and the transient curve between them, from XSLOPE's own uncoupled [transient seepage solve](../seep/transient.md). The section follows the manual's *result* figures rather than its Figure 102.1 labels, which are rounded to the nearest meter; the distinction is worth about 3% of the factor of safety, because the rounded labels describe a dam 0.7 m taller with a steeper downstream face where the critical mechanism sits.

**Input files:** [vp102a.xlsx](files/rocscience/vp102a.xlsx) (dry), [vp102b.xlsx](files/rocscience/vp102b.xlsx) (initial steady seepage), [vp102t_60/100/300/600/1500.xlsx](files/rocscience/vp102t_1500.xlsx) (drawdown snapshots)

**End members.**

| Case | Method | XSLOPE | Slide | Huang & Jia |
|---|---|---|---|---|
| Dry | Bishop / Spencer | 2.452 / 2.451 | 2.455 (−0.1% / −0.2%) | 2.43 (+0.9% / +0.9%) |
| Steady state (t = 0) | Bishop / Spencer | 1.722 / 1.731 | 1.745 (−1.3% / −0.8%) | 1.70 (+1.3% / +1.8%) |

*Both critical surfaces are shallow wedges on the downstream face, the face whose slope the rounded labels change. Both sit about 1–2% above Huang & Jia's own values.*

**Transient drawdown series (φ<sup>b</sup> = 0°).** After the reservoir drops the phreatic surface falls and the pore pressures dissipate, so the factor of safety rises monotonically: the governing minimum is the initial steady state above, and this series verifies the dissipation curve rather than a new critical minimum. One uncoupled transient solve (initial condition the steady full-pool field, isotropic *k* = 6×10⁻⁵ m/s, *S*<sub>s</sub> = 0.0196 /m, *S*<sub>y</sub> = 0.4) writes one *u* = 'seep' snapshot per save time, and the Spencer search runs on each. The vendor material selects RS2's built-in "Simple" conductivity and water-content functions, which XSLOPE does not implement, so the Gardner pair *a* = 0.1, *n* = 3 is substituted — the one input here not transcribed from the vendor's own model.

| Stage | XSLOPE Spencer | Slide2 Spencer |
|---|---|---|
| 60 h | 1.761 | 1.804 (−2.4%) |
| 100 h | 1.814 | 1.867 (−2.8%) |
| 300 h | 2.045 | 2.092 (−2.2%) |
| 600 h | 2.238 | 2.242 (−0.2%) |
| 1500 h | 2.378 | 2.373 (+0.2%) |

*The curve is reproduced end to end and every station sits within 3% of the Slide2 Spencer column. The early half runs low and the late half converges onto Slide2, a shortfall that closes as the dam drains — a drainage-rate difference rather than a flow-field error, since a wrong field would not vanish at the end of the series. Its direction matches the substituted retention curve, which holds water more tightly in the unsaturated zone and so drains this dam a little more slowly; priced against the section's own sensitivity to the phreatic surface, the worst station is about 0.4 m of head. Widening the unsaturated band was tested as the cause and is not it. The RS2 strength-reduction counterpart is [P4-VP102](rs2.md#p4-vp102), which rides the same flow solve.*

![vp102a: inputs and representative solution](images/vp102a.png)
![vp102b: inputs and representative solution](images/vp102b.png)
![VP102 transient rapid-drawdown: factor of safety vs time, XSLOPE Spencer vs Slide2 Table 102.3](images/vp102t_curve.png){width=800px}

<!-- test: file=files/rocscience/vp102t_60.xlsx, type=circular_search, num_slices=40, fs_spencer=1.761, benchmark=VP102-t-60 -->
<!-- test: file=files/rocscience/vp102t_100.xlsx, type=circular_search, num_slices=40, fs_spencer=1.814, benchmark=VP102-t-100 -->
<!-- test: file=files/rocscience/vp102t_300.xlsx, type=circular_search, num_slices=40, fs_spencer=2.045, benchmark=VP102-t-300 -->
<!-- test: file=files/rocscience/vp102t_600.xlsx, type=circular_search, num_slices=40, fs_spencer=2.238, benchmark=VP102-t-600 -->
<!-- test: file=files/rocscience/vp102t_1500.xlsx, type=circular_search, num_slices=40, fs_spencer=2.378, benchmark=VP102-t-1500 -->

## 🟢 VP103: Two-layer undrained slope — deep vs shallow mechanism {#vp103}

Slide #103 reproduces the headline case of [Guo & Griffiths (2020)](https://doi.org/10.1139/cgj-2019-0642):
an undrained embankment of strength c<sub>u1</sub> on an undrained foundation of strength
c<sub>u2</sub>, over a firm base. The paper's subject is *which mechanism governs*. A **deep**
mechanism cuts through the embankment and swings down through the foundation, so its factor of
safety rises with c<sub>u2</sub>; a **shallow** one stays inside the embankment, riding the layer
interface, and does not depend on c<sub>u2</sub> at all. As the foundation is made stronger the
deep branch climbs past the flat shallow branch, at the paper's
P<sub>crit</sub> = (c<sub>u2</sub>/c<sub>u1</sub>)<sub>crit</sub>.

**Geometry** (paper Figure 1a at H = 18 m, cot β = 2.0, D = 2.0): ground (0, 36)-(36, 36)-(72, 18)-(90, 18),
layer interface horizontal at el 18, firm base at el 0. **Materials** (manual Figure 103.2):
c<sub>u1</sub> = 60 kPa and c<sub>u2</sub> = 84 / 90 / 96 kPa — strength ratios P = 1.4 / 1.5 / 1.6 —
with γ = 20 kN/m³ in both layers and no water.

**Isolating the two modes.** Slide2 separates the minima with a multi-modal Particle Swarm search,
XSLOPE with a `tangent_depth` window (the [RS2-61](rs2.md#rs2-61) precedent) — one in the
foundation, one in the embankment — refining each with the non-circular search. Slide2 ran Particle
Swarm with Surface Altering optimization, so its surfaces are not circles and the comparison is only
fair against optimized surfaces.

**Input files:** [vp103a.xlsx](files/rocscience/vp103a.xlsx) (P = 1.4) ·
[vp103b.xlsx](files/rocscience/vp103b.xlsx) (P = 1.5) ·
[vp103c.xlsx](files/rocscience/vp103c.xlsx) (P = 1.6) ·
[vp103d.xlsx](files/rocscience/vp103d.xlsx) (P = 1.6, seeded on the shallow mode)

| Strength ratio P | Mode | XSLOPE Spencer, optimized | XSLOPE Spencer, circles only | Slide2 (PS + SA) |
|---|---|---|---|---|
| 1.4 | deep | **1.221** | 1.299 | 1.215 (+0.5%); its uni-modal search reads 1.216 |
| 1.5 | deep | **1.298** | 1.379 | 1.290 (+0.6%) |
| 1.6 | deep | 1.374 | 1.458 | 1.366 (+0.6%) |
| 1.4 | shallow | 1.322 | 1.348 | *not reported* |
| 1.5 | shallow | 1.322 | 1.348 | 1.324 (−0.2%) |
| 1.6 | shallow | **1.322** | 1.348 | **1.315** (+0.5%) |

*(Bold marks the governing mechanism at that strength ratio. The shallow row is one solved file,
vp103d: the mechanism never enters the foundation, so its factor of safety is identical at all three
ratios.)*

Every optimized value sits within 0.6% of Slide2, and always high, as a coordinate-descent
refinement from a single seed does against a swarm. The circles-only column runs about 7% above
Slide2 on the deep mechanism but only 2% high on the shallow one, because the deep surface wants to
cut steeply through the weak embankment and then run long and flat through the strong foundation,
and no single circle does both. Guo & Griffiths make the same observation about their own
limit-equilibrium comparison — the method of slices "requires the critical mechanism to be circular,
while the FEM places no restriction on its shape."

**The transition.** With optimized surfaces the deep branch is critical at P = 1.4 and P = 1.5 and
has been overtaken by P = 1.6, so the switch falls between 1.5 and 1.6 — the interval the manual
reports, and one grid step above the paper's finite-element P<sub>crit</sub> = 1.5. Restricted to
circles the crossing moves *down*, to between 1.4 and 1.5: the surface family changes not just the
factor of safety but which mechanism is predicted to govern. Apart from its P<sub>crit</sub> table
the paper publishes factors of safety as charts, so the locks are measured against the Slide2 values
printed in the manual's §103.2 result figures.

![vp103a: P = 1.4 inputs and the deep mechanism (governing)](images/vp103a.png)

![vp103c: P = 1.6 inputs and the deep mechanism (no longer governing)](images/vp103c.png)

![vp103d: P = 1.6 inputs and the shallow mechanism (governing)](images/vp103d.png)

## 🟢 VP104: Seismic slope with Newmark and multi-modal optimization {#vp104}

Slide #104 is built on Slide2's own *Tutorial 28 — Seismic Analysis with the Newmark Method*, so
the verification manual prints no geometry of its own. The model is a 10 m, 2:1 slope in three
layers over a horizontal base (soil 1: c = 0, φ = 38°; soil 2: c = 5.3 kPa, φ = 23°; soil 3:
c = 7.2 kPa, φ = 20°; all γ = 19.5 kN/m³), dry, with no external loads. The manual runs four
scenarios twice, once with multi-modal Particle Swarm plus Surface Altering optimization and once
with the ordinary uni-modal search, and prints both columns in Table 104.1. The two published
columns agree to about 0.1%, and the uni-modal column is what an ordinary circular search targets,
so three of the four scenarios reproduce directly.

**Input files:** [vp104a.xlsx](files/rocscience/vp104a.xlsx) (no seismic) ·
[vp104b.xlsx](files/rocscience/vp104b.xlsx) (k = 0.15)

| Scenario | XSLOPE (Spencer) | Slide2 uni-modal | Slide2 MMO |
|---|---|---|---|
| No seismic | 1.372 | 1.360 (+0.9%) | 1.359 (+1.0%) |
| Seismic coefficient k = 0.15 | 0.989 | 0.980 (+0.9%) | 0.978 (+1.1%) |
| Critical acceleration | K<sub>y</sub> = 0.144 | K<sub>y</sub> = 0.140 (+2.9%) | K<sub>y</sub> = 0.139 (+3.6%) |
| Newmark displacement | — *diagnostic, below* | 5.081 cm | 5.042 cm |

*All three built scenarios run about +0.9% high, in the same direction and by the same amount:
Slide2's Surface Altering optimization refines the surface away from a circle and so finds a
slightly lower minimum than a circular search can, and the critical acceleration follows from
that. The critical-acceleration row is a `critical_kc` lock, not a factor of safety.*

**The fourth scenario — permanent Newmark displacement — is reproduced as a diagnostic.**
The seismic record it needs is not printed in the verification manual but ships with the product:
the tutorial model the problem is built on (`Tutorial 28 Seismic.slmd`) stores the whole time
history inside its *Newmark Displacement* scenario — 5862 samples at dt = 0.005 s spanning 0 to
29.305 s, labeled *Mammoth Lakes-1 1980: CVK-090*. `benchmarks/rocscience/newmark_vp104.py`
carries that record and integrates it with the textbook rigid-block scheme: while the driving
acceleration exceeds the yield acceleration K<sub>y</sub> the block accelerates relative to the
ground at (a − K<sub>y</sub>)·g, one-way, and the relative velocity is integrated to a permanent
displacement.

| K<sub>y</sub> | Rigid-block integration | Slide2 published |
|---|---|---|
| 0.139 — Slide2 MMO | 5.015 cm | 5.042 cm (−0.5%) |
| 0.140 — Slide2 uni-modal | 4.906 cm | 5.081 cm (−3.4%) |
| 0.144 — XSLOPE `critical_kc` | 4.496 cm | — |

The published pair is **non-monotone in K<sub>y</sub>** — the larger yield acceleration is printed
with the larger displacement — which no single integration of one record can produce, since
displacement falls as K<sub>y</sub> rises. The two columns are two different critical surfaces whose
K<sub>y</sub> is printed rounded to three decimals, and inverting each published displacement back
through the integration shows that only the multi-modal row's value is consistent with its printed
K<sub>y</sub>, and it agrees to −0.5%. Displacement is also far more sensitive to the yield
acceleration than the factor of safety is: XSLOPE's K<sub>y</sub> runs +2.9% high because a circular
search cannot follow Slide2's surface-altering optimization, and carried through the same
integration that 2.9% removes about 11% of the displacement. That amplification is why the yield
acceleration, not the displacement, is the quantity worth locking.

**Scope.** XSLOPE's seismic modeling is pseudo-static: a seismic coefficient in the
limit-equilibrium solve, plus the `critical_kc` search for the k at which the searched minimum
factor of safety reaches 1. Displacement integration is not an analysis mode — the script above
takes a yield acceleration as an input and reads no XSLOPE model — so that row carries no lock.

![vp104a: no-seismic inputs and Spencer critical surface](images/vp104a.png)

![vp104b: k = 0.15 inputs and Spencer critical surface](images/vp104b.png)

## ⊘ VP105: Anisotropic strength surface {#vp105}

Slide #105 gives its material an **anisotropic strength function** — shear strength
that depends on the orientation of the slip surface relative to a fabric direction —
and searches it with multi-modal optimization.

XSLOPE has no orientation-dependent strength model: every material's strength is a function of
position and normal stress, and nothing in the slice formulation reads the direction the base of
the slice runs, so there is no input that expresses this problem and no factor of safety to lock.
It is a strength-model gate, not a search gate — [VP103](#vp103) separates two competing minima
with `tangent_depth` windows and [VP104](#vp104) reproduces Slide2's multi-modal table from an
ordinary circular search. The same gap blocks [GeoStudio §2.47](geostudio.md).

## 🟢 VP106: Support, Ito & Matsui pile {#vp106}

**Input files:** [vp106a.xlsx](files/rocscience/vp106a.xlsx) (no pile) ·
[vp106b](files/rocscience/vp106b.xlsx) / [c](files/rocscience/vp106c.xlsx) /
[d](files/rocscience/vp106d.xlsx) / [e](files/rocscience/vp106e.xlsx)
(D1/D = 2, 3, 4, 6)

Cai & Ugai (2000)'s pile-reinforced slope: a 10-m, 1V:1.5H dry cohesive-frictional slope
(γ = 20, c′ = 10, φ′ = 20) with a row of 0.8-m steel-tube piles at mid-slope, embedded to
bedrock, at center-to-center spacings of 2–6 diameters. The pile's stabilizing force is
the Ito & Matsui (1975) theoretical limit pressure, which XSLOPE computes automatically
from the pile diameter and spacing (the per-pile force is divided by the spacing to give
the per-meter-width value). The reaction is applied in the passive sense — added to the
resisting moment and divided by the factor of safety — which is how Slide applies it.

| Case | XSLOPE (Bishop search) | Slide | Cai & Ugai |
|---|---|---|---|
| No pile | 1.143 | 1.14 (+0.3%) | 1.13 (+1.2%) |
| D1/D = 2 | 1.540 | 1.54 (0.0%) | 1.54 (0.0%) |
| D1/D = 3 | 1.451 | 1.43 (+1.5%) | 1.37 (+5.9%) |
| D1/D = 4 | 1.341 | 1.33 (+0.8%) | 1.31 (+2.4%) |
| D1/D = 6 | 1.260 | 1.25 (+0.8%) | 1.25 (+0.8%) |

At the closest spacing (D1/D = 2) all three programs agree exactly: the pile force is
large enough that the critical surface avoids the pile entirely. At D1/D = 3 the published
values themselves spread — Slide sits 4.4% above the paper, a search-method difference the
manual acknowledges — and XSLOPE lands 1.5% above Slide but 5.9% above Cai & Ugai's own
value, the widest gap among this section's references. Every other case agrees with
Slide within 0.8% and with the originating paper within 2.4%.

![vp106a: inputs and representative solution](images/vp106a.png)
![vp106b: inputs and representative solution](images/vp106b.png)
![vp106c: inputs and representative solution](images/vp106c.png)
![vp106d: inputs and representative solution](images/vp106d.png)
![vp106e: inputs and representative solution](images/vp106e.png)

## VP106 — finite-element variant: the 2D pile idealization measured {#vp106-fem}

**Input files:** [vp106a_fem.xlsx](files/rocscience/vp106a_fem.xlsx) (no pile) ·
[vp106c_fem.xlsx](files/rocscience/vp106c_fem.xlsx) (D1/D = 3, free head) ·
[vp106c_fem_fix.xlsx](files/rocscience/vp106c_fem_fix.xlsx) (D1/D = 3, unrotated head — rotation held, translation free)

Cai & Ugai analyzed this slope twice; the limit-equilibrium side is [VP106](#vp106) above, and the
other is a **three-dimensional** shear-strength-reduction finite-element model that meshes the
individual piles and the soil between them, with interfaces that can slip. These three files run
that side through XSLOPE's SSRM at the paper's default D1/D = 3, on the same section and soil, with
the pile as a plane-strain beam: E = 6×10⁷ kPa on the 0.8 m section, so I = 0.0201 m⁴ and
A = 0.5027 m², both divided by the 2.4 m spacing; soil E = 2×10⁵ kPa, ν = 0.25. The Ito & Matsui
limit pressure the limit-equilibrium files carry is deliberately absent: in a finite-element
analysis the pile carries what the soil pushes onto it.

**This is a diagnostic, not a verification, and it carries no match dot.** The two models are not
the same model, and the differences below measure what separates them.

| Case | XSLOPE SSRM (2D beam) | Cai & Ugai 3D FE |
|---|---|---|
| No pile | 1.136 | 1.14 (−0.4%) |
| Pile, free head | 1.578 | 1.36 (+16.0%) |
| Pile, unrotated head | 1.587 | 1.45 (+9.4%) |
| Pile, hinged head — not built | — | 1.54 |
| Pile, fully fixed head — not built | — | 1.55 |

Without a pile the two agree to −0.4%: the same section, soil and strength-reduction procedure,
with nothing three-dimensional in either model. That row is what makes the other two readable. With
the pile in place the two-dimensional model reads high, by +16.0% with a free head and +9.4% with
the head unrotated, which is the direction the idealization predicts: in three dimensions the soil
at three diameters' spacing arches onto the piles, some of it moves between them, and it can slip
along each pile's surface, while in a plane-strain smear the row is a continuous sheet at one-third
the stiffness that everything above has to push through. The two locked rows differ by the head
condition and nothing else, and they land a bisection step apart where the three-dimensional pair
is separated by an order of magnitude more: restraining the head governs how the soil arches
around individual piles, and a plane-strain sheet already carries load along its whole length.
Holding the tip as well leaves the unrotated-head factor of safety unchanged, because the tip sits
on the model's own base.

The limit-equilibrium path at [VP106](#vp106) lands nearer the three-dimensional answer than the
finite-element path does, and still above it, so neither two-dimensional route recovers the
three-dimensional credit. What recommends the limit-equilibrium path is the Ito & Matsui limit pressure behind it, a theory *of*
the three-dimensional mechanism rather than a two-dimensional stand-in for it.

**Scope.** The plane-strain beam is an exact representation of a member that really is continuous
out of plane, and it is verified as one against a sheet pile wall in
[GeoStudio's SIGMA/W benchmark](geostudio.md#sigmaw-wall). For a discrete pile row the validated
route is limit equilibrium with the Ito & Matsui limit pressure — [VP106](#vp106) across four
spacings, and [VP54](#vp54). See
[Pile Elements in FEM](../fem/piles.md#applicability-continuous-walls-and-discrete-pile-rows).

**Sources:** Cai & Ugai (2000), the three-dimensional shear-strength-reduction results.

<!-- test: file=files/rocscience/vp106a_fem.xlsx, type=fem_ssrm, expected_fs=1.136, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=0.85, f_max=1.45, max_iter=16000, benchmark=VP106-FEM-nopile -->
<!-- test: file=files/rocscience/vp106c_fem.xlsx, type=fem_ssrm, expected_fs=1.578, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=1.0, f_max=1.8, max_iter=16000, benchmark=VP106-FEM-free -->
<!-- test: file=files/rocscience/vp106c_fem_fix.xlsx, type=fem_ssrm, expected_fs=1.587, element_type=tri6, target_size=0.9, tolerance=0.01, f_min=1.0, f_max=1.9, max_iter=16000, benchmark=VP106-FEM-fixed -->

## 🟢 VP107: Retaining walls, gabion walls, supports {#vp107}

**Input files:** [vp107a.xlsx](files/rocscience/vp107a.xlsx) (equivalent cohesion) ·
[vp107b.xlsx](files/rocscience/vp107b.xlsx) (mesh method)

Cao et al. (2016)'s case study of a Vancouver gabion-wall failure: a 6 m battered wall
of 1 m gabions (courses 4–3–3–2–2–1 wide) retaining a 30° backfill with a 12 kN/m²
crest surcharge and a water table rising into the retained slope. Slide models the
steel mesh two ways — an equivalent gabion cohesion (c = 100 kPa, from Grodecki 2017)
or explicit geosynthetic supports at every course interface (T = 71 kN/m, tangent,
active, anchored both ends) — and reports overall (external) stability only. Both
variants are evaluated on Slide's drawn critical circle, which passes about a meter
beneath the wall base.

| Variant | XSLOPE Bishop | Slide Bishop | XSLOPE Spencer | Slide Spencer |
|---|---|---|---|---|
| Equivalent cohesion | 1.382 | 1.373 (+0.7%) | 1.398 | 1.386 (+0.9%) |
| Mesh (geosynthetic supports) | 1.382 | 1.378 (+0.3%) | 1.398 | 1.392 (+0.4%) |
| Slide's unfiltered Cuckoo minima, wall-face surfaces | — | 1.032 / 1.034 | — | — |

XSLOPE's unconstrained grid search finds the same deep basin, within 0.5% of
Slide's limit-filtered search. The governing surface passes under the wall, so it
never crosses the mesh supports and the two representations coincide exactly on it —
the manual's own conclusion. (The mesh-variant file exercises the geosynthetic input
path; reinforcement mechanics are locked by VP87–VP94.) The last table row is Slide's own non-circular Cuckoo search on small surfaces at the wall
face, below the second limit set the manual applies to exclude them; those are not locked.

![vp107a: inputs and representative solution](images/vp107a.png)
![vp107b: inputs and representative solution](images/vp107b.png)

## 🟢 VP108: Stepped gabion wall, steps facing outwards {#vp108}

**Input files:** [vp108a.xlsx](files/rocscience/vp108a.xlsx) (equivalent cohesion) ·
[vp108b.xlsx](files/rocscience/vp108b.xlsx) (mesh method)

A 4 m gabion wall of 1 m cubes (courses 4–3–2–1, staircase exposed on the outward
face, back face straight and partly embedded) on a sloping soil-1 over soil-2
profile, dry. As in VP107, Slide represents the steel mesh either as an equivalent
gabion cohesion (c = 59.7 kPa, Grodecki 2017 with f_t = 100 kN/m) or as explicit
geosynthetic supports (T = 100 kN/m) at the course interfaces. Both variants are
evaluated on Slide's drawn critical circles, which enter the crest behind the wall
and pass just beneath its base. The labeled points (16.453, 5.178) and
(18.573, 5.89) pin where the soil-1/soil-2 interface meets the wall base and
re-emerges one course up the back face — the bottom course's back is embedded in
soil 2.

| Variant | XSLOPE Bishop | Slide Bishop | XSLOPE Spencer | Slide Spencer |
|---|---|---|---|---|
| Equivalent cohesion | 1.790 | 1.787 (+0.2%) | 1.797 | 1.791 (+0.3%) |
| Mesh (geosynthetic supports) | 1.830 | 1.835 (−0.3%) | 1.835 | 1.839 (−0.2%) |
| Slide's unfiltered Cuckoo minima, wall-face surfaces | — | 1.512 / 1.522 | — | — |

XSLOPE's unconstrained grid search finds the same basin below Slide's
limit-filtered grid search. The governing circles do not cross the mesh supports
(the two variants differ only through their slightly different critical circles), so
the mesh file's tag guards the geosynthetic input path rather than reinforcement
mechanics — VP87–VP94 lock those. The last table row is Slide's own unfiltered Cuckoo minima on small
wall-face surfaces, excluded by the manual's own limit set.

![vp108a: inputs and representative solution](images/vp108a.png)
![vp108b: inputs and representative solution](images/vp108b.png)

## 🟢 VP109: Gabion wall with weak joint layers {#vp109}

**Input files:** [vp109.xlsx](files/rocscience/vp109.xlsx)

The VP108 wall with thin weak layers between the gabion courses representing
potential joint or shear failure through the wall: friction 90% of the gabion fill
(φ = 37.8°) and cohesion from the 20.4 kN/m joint tensile strength across the 1 m
gabion width (c = 20.4 kPa), modeled here as 6 cm bands carved from the wall at the
three course interfaces. Slide runs a block search along the layers with endpoint
limits that exclude small wall-hugging surfaces.

|  | XSLOPE (Fig 108.3 circle) | Slide (block search along joints) |
|---|---|---|
| Bishop | 1.790 | 1.799 (−0.5%) |
| Spencer | 1.797 | 1.803 (−0.3%) |
| Unfiltered block minimum at the wall face | — | 1.516 |

The joint layers do not govern overall stability: Slide's constrained block search
lands within 0.7% of the plain VP108 deep circle, which passes beneath wall and
bands alike, and XSLOPE's unconstrained circular search on the weak-layer model agrees. The last table row is the unfiltered block minimum Slide's figure reports for a small
surface at the wall face, excluded by its limit set and not locked here.

![vp109: inputs and representative solution](images/vp109.png)

## ⊘ VP110: Equivalent fluid pressure wall support {#vp110}

Slide #110 verifies its **equivalent fluid pressure (EFP)** support type by showing
that it gives the same answer as the distributed load it stands for: the wall modeled
as an EFP support and the wall modeled as an explicit triangular pressure on the face
return the same factor of safety.

| Model (Slide's own equivalence check) | XSLOPE | Slide2 (Spencer) |
|---|---|---|
| EFP support | — *nothing to rebuild* | 2.566 |
| Explicit triangular face pressure | — *nothing to rebuild* | 2.566 |

The manual prints neither soil properties nor coordinates for the model — it is Slide's own
tutorial file — so there is nothing independent to rebuild and nothing to lock. The equivalence it
demonstrates is exactly how XSLOPE models such a wall: the restraint is entered as a triangular
distributed load over the face through `dloads`, so there is no separate support type because the
distributed load *is* the model.

## ⊘ VP111: Helical anchor — capacity note (no lock) {#vp111}

Slide's problem 111 verifies its helical-anchor **capacity envelope**, not a slope analysis: for
an anchor with three 0.2-m helices (1-m spacing, 0.1-m shaft), shaft tensile capacity 85 kN and
head capacity 80 kN, the manual tabulates the available force as a function of where a slip surface
crosses the anchor — the minimum of plate pullout behind the surface, stripping ahead of it, and
shaft tension, each from the Perko (2009) plate-bearing formulas. There is no slope and no factor
of safety to verify against.

**Analyzing helically anchored slopes in XSLOPE:** compute the governing capacity at the expected
slip-surface crossing — from the supplier's rating, an installation-torque correlation, or the
Perko formulas — divide by the out-of-plane spacing, and enter the result as the tension capacity
of a standard anchor line at the anchor's geometry. That is the same value Slide's internal model
would apply; only the plate-bearing bookkeeping is external.
