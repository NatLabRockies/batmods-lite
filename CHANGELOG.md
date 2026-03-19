# BATMODS-lite Changelog

## [Unreleased](https://github.com/NatLabRockies/batmods-lite)

### New Features
- Adding NMC811 and GraphiteSiOx material ([#22](https://github.com/NatLabRockies/batmods-lite/pull/22))
- Check bounds of intercalation fraction before calculating exchange current density ([#19](https://github.com/NatLabRockies/batmods-lite/pull/19))
- Update `materials` module with new LFP properties, from ICI ([#18](https://github.com/NatLabRockies/batmods-lite/pull/18))
- Use `CubicSpline` interpolations for LFP properties ([#15](https://github.com/NatLabRockies/batmods-lite/pull/15))
- Add degradation parameters for the electrolyte (applies to P2D only) ([#14](https://github.com/NatLabRockies/batmods-lite/pull/14))
- Add `submodels` modules with optional `Hysteresis` class, and directional `Ds` / `i0` ([#13](https://github.com/NatLabRockies/batmods-lite/pull/13))
- `Exerpiment` class interface allows for multi-step and dynamic load profiles
- Simplified `run` and `run_step` methods to work with generalized `Experiment` class
- New solver now provides additional statistics, e.g., number of function and Jacobian evaluations
- Control-specific `Solution` classes are replaced with generalized `StepSolution` and `CycleSolution`

### Optimizations
- Reduce memory usage by delaying post-processing (slicing) steps ([#17](https://github.com/NatLabRockies/batmods-lite/pull/17))
- Replaced `scikits-odes` solver with `scikit-sundae` to improve installation
- Sped up SPM by flipping cathode pointers so that bandwidth is reduced to +/- 2
- Use a generic `bandwidth` function instead of having one per model subpackage

### Bug Fixes
None.

### Breaking Changes
- Removal of `run_CC`, `run_CV`, and `run_CP` methods
- Renamed some attributes so they are no longer user-facing (`_sv0`, `_algidx`, etc.)

### Chores
- Add `Development` section/pages to the Read the Docs documentation ([#25](https://github.com/NatLabRockies/batmods-lite/pull/25))
- Improve development tools (use `ruff`, add `codecov`, host docs on RTD) ([#24](https://github.com/NatLabRockies/batmods-lite/pull/24))
- Make GitHub hyperlinks reference new org name `NREL` -> `NatLabRockies` ([#21](https://github.com/NatLabRockies/batmods-lite/pull/21))
- Rebrand NREL to NLR, and include name change for Alliance as well ([#20](https://github.com/NatLabRockies/batmods-lite/pull/20))

## [v0.0.1](https://github.com/NatLabRockies/batmods-lite/tree/v0.0.1)
This is the first release of `BATMODS-lite`. Main features/capabilities are listed below. The release is only available on GitHub. Future releases, however, will also be distributed on PyPI.

### Features
- Working SPM and P2D models
- Capability to run with current, voltage, or power demands

### Notes
- Models were verified mathematically by checking conservation equations
- Validations were completed using COMSOL equivalents
