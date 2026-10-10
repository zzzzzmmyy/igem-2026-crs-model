# Attribution and provenance

The supplied original Python model and analyses came from the team's local
`建模代码_1` folder. Their human authors were not supplied in this chat. The team
must identify the actual authors/contributors in its repository and iGEM
Attributions Form rather than assigning invented names.

AI assistance in this session: English dark-background figure redesign;
portable code and folder cleanup; README, installation/export/test scaffolding;
official-rule lookup and identification of unsupported Wiki claims. AI assistance
is not experimental validation. The team should review and disclose assistance
in the manner required by the current iGEM forms/policies.

The core ODE/solver implementations, rate values, simplex sampling resolution,
passage protocol and thresholds were preserved. The cleanup did not reproduce
the topology-only model or add stochastic results to the final module.

## Background references retained from the supplied draft

These references motivate the project context and mechanisms. They do not
constitute quantitative calibration of this well-mixed implementation.

- Kerr et al. (2002), *Nature*, 418:171–174. https://doi.org/10.1038/nature00823
- Chao and Levin (1981), *PNAS*, 78:6324–6328. https://doi.org/10.1073/pnas.78.10.6324
- Weber et al. (2014), *J. R. Soc. Interface*, 11:20140172. https://doi.org/10.1098/rsif.2014.0172
- May and Leonard (1975), *SIAM J. Appl. Math.*, 29:243–253. https://doi.org/10.1137/0129022
- Reichenbach et al. (2006), *Phys. Rev. E*, 74:051907. https://doi.org/10.1103/PhysRevE.74.051907

## Dependencies and embedded figure fonts

NumPy, SciPy and Matplotlib remain under their upstream licenses; they are not
vendored. Matplotlib's DejaVu Sans is used, including its font shapes in generated
PNG output. DejaVu fonts are distributed under their own font license:
https://dejavu-fonts.github.io/License.html . Preserve the font attribution when
the team credits figure-generation assets. SVG uses font-family references and
does not initiate requests to a remote font CDN.
