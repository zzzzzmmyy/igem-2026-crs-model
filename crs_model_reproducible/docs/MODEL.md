# Numerical model and reproducibility

## Scope

Well-mixed C (colicin producer), R (resistant), S (sensitive) competition with
a globally acting toxin T and shared carrying capacity K. No spatial shielding,
local neighborhoods, demographic noise, or stochastic extinction is simulated.

The retained ODE uses `g=max(0,1-(C+S+R)/K)`:

```
dC/dt = mu_C*C*g
dS/dt = mu_S*S*g - kill*T*S
dR/dt = mu_R*R*g
dT/dt = kappa*C - delta*T
```

The clipping of the logistic growth term is part of the original code. It matches
the Wiki's un-clipped expression when N <= K; it is not a new model change.
State order is **C,S,R,T**, while ratios/CSV columns use **C,R,S**.

## Default parameters

| Parameter | Value | Interpretation |
|---|---:|---|
| mu_S | 56.2/43.6, about 1.289 | Relative sensitive-strain growth |
| mu_R | 1 | Reference relative growth |
| mu_C | 39.3/43.6, about 0.901 | Relative producer growth |
| K | 1 | Normalized shared carrying capacity |
| kappa | 6 | Illustrative toxin production |
| delta | 6 | Illustrative toxin degradation |
| kill | 8 | Illustrative killing strength |
| Inoculum density | 0.01 K | Initial total normalized density |
| Passage duration | 12 | Model time units |
| Dilution | 100 | 1:100, T reset to zero |
| Extinction threshold | 1e-6 | Relative strain abundance after passage |

These are illustrative values, not fitted to this team's wet-lab measurements.
Growth rates normalized by mu_R give a model time coordinate. The existing figure
label `Time (h)` presumes the reference growth rate is assigned 1 h^-1; without
measuring that reference, 30 and 12 should be treated as model-time horizons,
not calibrated real-hour predictions. This limitation is explicit in the Wiki draft.

## Figure calculations

Figure 3-1: initial C:R:S ratios 1:1:1, 5:1:1, 0.1:1:1, 0.02:1:1; total density
0.01; duration 30; 400 time samples. Batch integration uses SciPy `solve_ivp`,
default tolerances and `max_step=0.05`. T starts at zero.

Figure 3-2: `simplex_grid(28)` samples `(28+1)*(28+2)/2 = 435` compositions,
including edges and vertices. Run 60 passages each, with `max_step=0.1`.
For each strain, record its first post-passage crossing of the relative threshold.
Three-strain persistence is the first crossing passage minus one, capped at 60.
The retained results have median persistence 0 and maximum 20 passages; 276/435
points have zero completed coexistence passages. First-loss labels: C=106, R=28,
S=301. Boundary inocula lack three strains initially and are included in these totals.

Threshold crossing is an operational numerical definition, not exact extinction.
The code continues all ODE state variables below threshold, permitting mathematical
regrowth. Multiple simultaneous first crossings are assigned by C,R,S dictionary
order, not resolved biologically. Figure 3-2 measures three-strain persistence;
it does not separately quantify R/S pairwise persistence.

Figure 3-3: 22 evenly spaced initial C fractions in [0.01,0.5], 18 potency values
in [0.5,10], 40 passages. R=S=(1-C)/2. Set `kappa=p` and `kill=p` (not p squared
on the plotted vertical axis). Delta stays at 6. The scan has 396 conditions;
observed persistence ranges from 0 to 22. Contours are 5 and 15 passages. Colors
are normalized to the observed data range, as in the original script. For a given
toxin setting, persistence need not be globally monotone in C; the candidate band
and its high-C boundary must be interpreted together.

## CSV schemas

Figure 3-1: `initial_ratio_C_R_S,time_model_units,C_fraction,R_fraction,S_fraction`.
Figure 3-2: `r_C,r_R,r_S,x,y,coexistence_passages,first_lost` (435 rows).
Figure 3-3: `r_C,r_R,r_S,potency_p,kappa,kill,coexistence_passages` (396 rows).
The reference Figure 3-3 matrix has rows in ascending potency order and columns
in ascending C-fraction order; it is model-generated regression data, not experimental data.

## Limitations relevant to interpretation

No MATLAB/SimBiology topology-only oscillation code or result is supplied in this
folder, so this package cannot reproduce that claim. No fitted calibration,
experimental validation, uncertainty analysis, formal stability proof, SBOL API,
or quantified biological-user benchmark is supplied. The 5-20% region is an
exploratory starting range, not a universal cutoff or validated optimum.
