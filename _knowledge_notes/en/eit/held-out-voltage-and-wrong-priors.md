---
title: Can held-out voltages detect a wrong prior in EIT?
summary: The complete electrode model, cross-study evidence, and a reanalysis of 38 KIT4 cases motivate a physical-phantom test for screening misleading conductivity priors.
topic: Electrical Impedance Tomography (EIT)
lang: en
updated: 2026-11-21
permalink: /en/knowledge/eit/held-out-voltage-and-wrong-priors/
alternate_url: /knowledge/eit/held-out-voltage-and-wrong-priors/
---

*Research article based on the Electrical Impedance Tomography project knowledge base on prior mismatch, measurement holdout, and independent physical references.*

**Abstract.** Structural priors can stabilize electrical impedance tomography (EIT), and models can still fit boundary voltages when the shapes or material contrast in a prior are wrong. Can a set of held-out measurements reveal that error and select a more physically accurate reconstruction? We derive a sufficient condition for separating two candidates under the complete electrode model. We then compare published tank and simulation experiments, check related analyses of KIT4, and independently reanalyse the original KIT4 v1 voltages from 38 cases. Predicting skip-two voltages from adjacent-drive measurements gives a median relative error of **1.30%** per case. Even in the same ideal current space, measured records depart from their linear recombination. Detecting a wrong prior requires sufficient separation in the held-out voltages. Demonstrating a conductivity improvement requires an independent reference on the same physical case.

<nav class="literature-toc" aria-label="In this article">
  <a href="#question">Problem and challenges</a><a href="#prior-work">Prior work</a><a href="#theory">Mathematical model</a><a href="#results">Experimental results</a><a href="#cross-check">Cross-study checks</a><a href="#proposed-study">Proposed study</a><a href="#conclusion">Conclusion</a><a href="#references">References</a>
</nav>

## 1. Research problem and challenges
{: #question }

Suppose a saline tank contains two inclusions at known locations. One is more conductive than the background and the other more resistive. An auxiliary image preserves their boundaries but reverses their material contrast. Using it in the inversion could place the targets correctly while biasing their estimated conductivity and the background. This raises two questions. Can genuinely held-out voltages separate the candidate fields produced by the correct and wrong priors? If they can, does selecting among those fields also reduce error against an independent physical reference?

- **The observations depend differently on shape and conductivity.** Two fields can produce nearly identical electrode voltages. Extra drives help when they are sensitive to the specific difference under study.
- **Different error mechanisms can change the same voltages.** Contact impedance, boundary shape, reference drift, and gain errors can increase a test residual. Attributing that increase to a prior takes additional controls.
- **A holdout has to be defined before processing and selection.** Data used to normalize, estimate contact, tune the penalty, or select a fallback have already informed the candidate. Reciprocal entries, changed current bases, and shared reference measurements can introduce dependence.
- **Geometry and conductivity require distinct measurements.** A photograph can check location, boundary, and area. Mean regional conductivity calls for an independent measurement at matched frequency and temperature, with scoring regions fixed in physical coordinates.

## 2. Prior work and scope of the evidence
{: #prior-work }

This is a focused synthesis of evidence from the project knowledge base. We selected studies that document an intervention on a prior, the role of voltage observations, or a physical reference. We checked the relevant equations, figures, tables, and dataset documentation. We evaluated the image or physical quantity each study actually returns. Studies that reuse one acquisition archive share its provenance, and we retained the original definitions of their metrics.

**Structural regularization.** Kolehmainen et al. use parallel level sets to bring auxiliary edge directions into the penalty while allowing additional edges through sparsity. Wang et al. incorporate an image prior into a coordinate network, either as initialization or through a frozen branch that remains active throughout the inversion. Each mechanism changes which fields are easier to reconstruct. Relevant mismatches include topology, location, material contrast, and how the prior is imposed. [2](#ref-pls) · [3](#ref-dpe)

**Electrical checks.** Asfaw and Adler predict withheld electrode readings from remaining measurements to detect faulty electrodes. Harrach’s interpolation estimates missing driven-electrode data in difference EIT using an a priori bound on conductivity change. Interpolated values and new instrument readings play different roles in a test. [4](#ref-asfaw) · [5](#ref-harrach)

**Physical references.** The Denker and Masiri KIT4 comparisons both report voltage discrepancy and photo-based Dice. Hong et al. use independent temperature probes in physical phantoms to check the same regional quantity that their method estimates. The KIT4 studies compare electrical and geometric scores. The thermometry study illustrates a physical reference in the units of an estimated quantity. [7](#ref-denker) · [8](#ref-masiri) · [9](#ref-hong)

## 3. Mathematical model and detectability
{: #theory }

### 3.1 From conductivity to electrode voltage

The potential <span class="literature-math">u</span> and positive conductivity <span class="literature-math">σ</span> satisfy conservation in the domain Ω. For electrode <span class="literature-math">E<sub>ℓ</sub></span>, write <span class="literature-math">U<sub>ℓ</sub></span> for electrode potential, <span class="literature-math">z<sub>ℓ</sub></span> for contact impedance, and <span class="literature-math">I<sub>ℓ</sub></span> for the associated applied current. Let <span class="literature-math">j<sub>n</sub> = σ∂<sub>n</sub>u</span> be the outward flux. The remaining boundary has zero flux. The currents sum to zero, and a voltage gauge fixes the additive constant. [1](#ref-cem)

<div class="literature-equation">
  <math display="block"><mo>∇</mo><mo>·</mo><mo stretchy="false">(</mo><mi>σ</mi><mo>∇</mo><mi>u</mi><mo stretchy="false">)</mo><mo>=</mo><mn>0</mn><mo>,</mo><mspace width="0.6em"/><mi>x</mi><mo>∈</mo><mi>Ω</mi></math>
  <math display="block"><mi>u</mi><mo>+</mo><msub><mi>z</mi><mi>ℓ</mi></msub><msub><mi>j</mi><mi>n</mi></msub><mo>=</mo><msub><mi>U</mi><mi>ℓ</mi></msub><mo>,</mo><mspace width="0.5em"/><msub><mo>∫</mo><msub><mi>E</mi><mi>ℓ</mi></msub></msub><msub><mi>j</mi><mi>n</mi></msub><mi>d</mi><mi>s</mi><mo>=</mo><msub><mi>I</mi><mi>ℓ</mi></msub></math>
  <math display="block"><msub><mo>∑</mo><mi>ℓ</mi></msub><msub><mi>I</mi><mi>ℓ</mi></msub><mo>=</mo><mn>0</mn><mo>,</mo><mspace width="0.65em"/><msub><mo>∑</mo><mi>ℓ</mi></msub><msub><mi>U</mi><mi>ℓ</mi></msub><mo>=</mo><mn>0</mn></math>
</div>

Collect geometry, electrode positions, contacts, and instrument parameters in <span class="literature-math">η</span>. Let <span class="literature-math">F<sub>C</sub></span> represent the forward map for the sealed group <span class="literature-math">C</span>, including its drives and readout. Let e<sub>C</sub> denote measurement error and J the relevant derivative. The local noiseless voltage change depends on both conductivity and these other parameters.

<div class="literature-equation">
  <math display="block"><msub><mi>y</mi><mi>C</mi></msub><mo>=</mo><msub><mi>F</mi><mi>C</mi></msub><mo stretchy="false">(</mo><mi>σ</mi><mo>,</mo><mi>η</mi><mo stretchy="false">)</mo><mo>+</mo><msub><mi>e</mi><mi>C</mi></msub></math>
  <math display="block"><mi>Δ</mi><msub><mi>F</mi><mi>C</mi></msub><mo>≈</mo><msub><mi>J</mi><mrow><mi>σ</mi><mo>,</mo><mi>C</mi></mrow></msub><mi>Δ</mi><mi>σ</mi><mo>+</mo><msub><mi>J</mi><mrow><mi>η</mi><mo>,</mo><mi>C</mi></mrow></msub><mi>Δ</mi><mi>η</mi></math>
</div>

This is a first-order relation. If a target perturbation is weakly visible on the test drives, or a plausible change in contact cancels its voltage effect, one residual magnitude cannot resolve the source.

### 3.2 How far apart must two predictions be?

Take two locked candidate reconstructions with test predictions <span class="literature-math">p<sub>1</sub></span> and <span class="literature-math">p<sub>2</sub></span>. Let <span class="literature-math">y</span> denote the readings, <span class="literature-math">‖·‖<sub>W</sub></span> a weighted norm on those same channels, and <span class="literature-math">T</span> an error bound informed by measurement and forward-model uncertainty. If the first prediction lies within <span class="literature-math">T</span> of the observed voltages, the triangle inequality gives:

<div class="literature-equation">
  <math display="block"><msub><mrow><mo>‖</mo><mi>y</mi><mo>−</mo><msub><mi>p</mi><mn>2</mn></msub><mo>‖</mo></mrow><mi>W</mi></msub><mo>≥</mo><msub><mrow><mo>‖</mo><msub><mi>p</mi><mn>1</mn></msub><mo>−</mo><msub><mi>p</mi><mn>2</mn></msub><mo>‖</mo></mrow><mi>W</mi></msub><mo>−</mo><mi>T</mi></math>
</div>

A gap <span class="literature-math">‖p<sub>1</sub>−p<sub>2</sub>‖<sub>W</sub> &gt; 2T</span> then gives a second residual greater than <span class="literature-math">T</span>. This is a **conditional sufficient test**. With a smaller gap, the direction of the actual error matters. Repeated measurements can inform the noise estimate, and controlled geometric and contact changes can inform the model-error bound. A common reference can induce correlated errors.

### 3.3 Do 256 withheld readings add 256 new constraints?

At fixed conductivity, contact, and geometry, electrode voltages are linear in applied current. For an ideal real reciprocal response with <span class="literature-math">M</span> electrodes, the balanced-current space has dimension <span class="literature-math">d = M−1</span>. Suppose the fitting and selection drives span a <span class="literature-math">k</span>-dimensional subspace and the electrode potential differences are fully read out. In a basis aligned with the subspace, those data determine the first <span class="literature-math">k</span> columns of the symmetric response and, by symmetry, the corresponding rows. Only a symmetric block of size <span class="literature-math">(d−k)×(d−k)</span> remains undetermined. [1](#ref-cem) · [6](#ref-kit4)

<div class="literature-equation">
  <math display="block"><mi>r</mi><mo stretchy="false">(</mo><mi>k</mi><mo stretchy="false">)</mo><mo>=</mo><mi>d</mi><mi>k</mi><mo>−</mo><mfrac><mrow><mi>k</mi><mo stretchy="false">(</mo><mi>k</mi><mo>−</mo><mn>1</mn><mo stretchy="false">)</mo></mrow><mn>2</mn></mfrac></math>
</div>

It follows that adding recorded readings, adding independent coordinates of the ideal response, and increasing sensitivity to a particular prior error are separate goals. Missing readout channels or faulty electrodes require computing the rank for the actual drives and measurements.

## 4. Experimental results
{: #results }

### 4.1 Published tank results on reversed material contrast

Wang et al.’s Case 5 contains an iron ring and a plastic cylinder. The reported relative reconstruction error (RE) in Figure 7 is 0.077 with no external image prior. It stays at 0.077 when the reversed-contrast prior is used only for initialization and rises to 0.111 when the frozen prior branch remains in use. For the aligned Prior 1, the two values are 0.066 and 0.063. These errors use the paper’s photographic and assigned-material reference image for one physical tank case. The experiment shows that **both the content of the prior and how it enters the inversion matter**. [3](#ref-dpe)

<figure class="literature-figure">
  <a href="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/wang2025-case5-prior-error.png' | relative_url }}"><img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/wang2025-case5-prior-error.png' | relative_url }}" width="1320" height="818" alt="Figure 1. In the real Case 5 tank, persistent embedding lowers error for a matched prior and raises it for a reversed-contrast prior." loading="lazy" decoding="async"></a>
  <figcaption><strong>Figure 1. In the real Case 5 tank, persistent embedding lowers error for a matched prior and raises it for a reversed-contrast prior.</strong> Both comparisons share the no-image-prior baseline. Redrawn from the relative reconstruction errors printed in Wang et al., Fig. 7. Each point is one configuration on the same case. <a href="https://doi.org/10.1016/j.neunet.2025.107419">Source</a></figcaption>
</figure>

### 4.2 Published evidence on independent references and partition error

Hong et al. checked regional temperature with two thermocouples per region in physical phantoms, reporting mean absolute errors of 0.22–0.71 °C. They perturbed the partitions in a separate CT-derived simulation. With an external heat source, shifting the regions from 0 to 10 mm increased the six-region mean absolute temperature error from 1.38 to 1.80 °C. With a central heat source, the same shift changed the score from 0.88 to 0.63 °C. The estimates and reference temperatures in Figure 9 were averaged over the translated regions, so the target being scored also changed. A physical follow-up should keep the external probes and scoring regions fixed. [9](#ref-hong)

<figure class="literature-figure">
  <a href="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/hong2026-domain-shift-error.png' | relative_url }}"><img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/hong2026-domain-shift-error.png' | relative_url }}" width="1320" height="818" alt="Figure 2. As simulated regions shift, the six-region mean absolute temperature error rises for external heating and falls for central heating." loading="lazy" decoding="async"></a>
  <figcaption><strong>Figure 2. As simulated regions shift, the six-region mean absolute temperature error rises for external heating and falls for central heating.</strong> Redrawn from the numerical results on p. 12 associated with Hong et al., Fig. 9. The six regions used for scoring move with the partition. <a href="https://doi.org/10.1002/mp.70774">Source</a></figcaption>
</figure>

### 4.3 Reanalysis of KIT4 drive ranks and withheld voltages

We used the 38 MAT cases from KIT4 v1. Each case has 16×79 drive and voltage arrays and a 16×16 measurement-pattern matrix. The groups below use the archive’s one-based column numbers. Both layouts use raw, separately stored voltage records. Their noise may still be correlated. We recomputed the cumulative balanced-current ranks from the archive. [6](#ref-kit4)

| Fitting block | Fit | + Select | + Test |
| --- | ---: | ---: | ---: |
| Adjacent, cols. 1–16 | 15 | 15 | 15 |
| Skip-three, cols. 49–64 | 12 | 14 | 15 |
{: .literature-results }

Both layouts use skip-one (columns 17–32) for selection and skip-two (columns 33–48) for testing, with 256 raw readings per group and case. Under complete readout and reciprocity, the first layout already spans all 120 coordinates of the ideal symmetric response after fitting. The second gives 114, 119, and 120 coordinates in succession. The test block contributes one new ideal coordinate under those assumptions. Whether it is sensitive to a specific prior error needs to be checked against the actual candidates.

We also computed a voltage-only baseline. Fit the target-drive weights using the adjacent-drive current matrix <span class="literature-math">I<sub>A</sub></span> and the target currents, without using target voltages. Combine the measured adjacent voltages <span class="literature-math">V<sub>A</sub></span> with those weights. Compare the result with measured target voltages <span class="literature-math">V<sub>T</sub></span> from the same file. The dagger denotes the Moore–Penrose pseudoinverse, and the subscript F denotes the Frobenius norm.

<div class="literature-equation">
  <math display="block"><msub><mi>W</mi><mi>T</mi></msub><mo>=</mo><msubsup><mi>I</mi><mi>A</mi><mo>†</mo></msubsup><msub><mi>I</mi><mi>T</mi></msub><mo>,</mo><mspace width="0.7em"/><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>T</mi></msub><mo>=</mo><msub><mi>V</mi><mi>A</mi></msub><msub><mi>W</mi><mi>T</mi></msub></math>
  <math display="block"><msub><mi>E</mi><mi>T</mi></msub><mo>=</mo><mfrac><msub><mrow><mo>‖</mo><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>T</mi></msub><mo>−</mo><msub><mi>V</mi><mi>T</mi></msub><mo>‖</mo></mrow><mi>F</mi></msub><msub><mrow><mo>‖</mo><msub><mi>V</mi><mi>T</mi></msub><mo>‖</mo></mrow><mi>F</mi></msub></mfrac></math>
</div>

Median per-case relative error is **1.34%** for skip-one (interquartile range 1.27%–1.56%) and **1.30%** for skip-two (1.24%–1.56%). This is a descriptive check over all 38 archived cases, measuring the gap between the original readings and their linear prediction. Acquisition and preprocessing effects may contribute to that gap, so it cannot directly set a threshold for prior error. This analysis uses no conductivity reconstruction or prior selection. [Public input archive](https://doi.org/10.5281/zenodo.1203914) · [Audit script]({{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-voltage-audit.py' | relative_url }}) · [Case-level CSV]({{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-voltage-errors.csv' | relative_url }})

<figure class="literature-figure">
  <a href="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png' | relative_url }}"><img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png' | relative_url }}" width="1278" height="675" alt="Figure 3. Relative errors for predicting skip-one and skip-two voltages from adjacent measurements across 38 KIT4 cases." loading="lazy" decoding="async"></a>
  <figcaption><strong>Figure 3. Relative errors for predicting skip-one and skip-two voltages from adjacent measurements across 38 KIT4 cases.</strong> Each dot is an archive case. Diamonds mark medians and horizontal lines span the 25th–75th percentiles. Values come from the reanalysis in this article. <a href="https://doi.org/10.5281/zenodo.1203914">Public archive</a></figcaption>
</figure>

## 5. Cross-study checks
{: #cross-check }

**The effects depend on the type of mismatch and how the prior enters the inversion.** In Kolehmainen et al.’s simulated Case 2, the STV relative conductivity errors are 13.8% with no auxiliary prior, 3.3% with the correct topology, and 10.1% with the wrong topology. The wrong topology can improve the global score while pulling parts of the boundary toward the auxiliary image. In Wang’s tank example, the error is in material contrast, and persistent embedding worsens the global score. Together these studies motivate reporting both whole-image error and local harm from a prior. [2](#ref-pls) · [3](#ref-dpe)

**Two analyses of one archive agree on a ranking reversal.** The following comparison concerns the KIT4 boundary-foam group (Set 6). Each paper supplies its own measurement-error metric. Dice averages the geometric overlaps for resistive, conductive, and background regions against photo-derived segmentation.

| Set 6 method | Dice ↑ | Voltage error ↓ |
| --- | ---: | ---: |
| Denker · GN-TV | 0.114 | 0.0004 |
| Denker · Deep D-bar | 0.408 | 0.0602 |
| Masiri · GN-TV | 0.1210 | 0.0003 |
| Masiri · Deep D-bar | 0.4332 | 0.0530 |
{: .literature-results }

Within both tables, GN-TV has lower voltage discrepancy and lower photo Dice. Denker defines the normalized squared residual. The exact norm and holdout conditions for Masiri’s Table 8 were unresolved in the version reviewed, so comparisons are within each table. Both analyses use the KIT4 archive. Case-level mask and voltage-column identities remain unresolved across the two implementations. The direction agrees across reanalyses of one acquisition lineage. [7](#ref-denker) · [8](#ref-masiri)

**The decisive comparison belongs in one physical case.** Asfaw and Adler show that held-out voltages can support one kind of electrical diagnosis. Wang intervenes directly on an incorrect internal prior, and Hong supplies independent physical references. The reviewed cases motivate an experiment combining the wrong internal prior, genuine readings kept out of selection, and an independent property measurement on the same phantom. That combination can test whether a selected reconstruction improves the target conductivity. [3](#ref-dpe) · [4](#ref-asfaw) · [9](#ref-hong)

## 6. Proposed experiment and potential advance
{: #proposed-study }

**Choose drives for candidate separation, then test with independent measurements.** Generate candidates with no external image prior, an accurate prior, and a controlled wrong prior. Use development cases to set the noise and contact ranges and lock the decision rule. Use predictions from the fitting stage to rank available drives by their ability to separate candidates under those conditions. Compare with a conventional protocol on the same number of measurements. Reserve an “insufficient information” decision for poorly separated cases. The falsifiable prediction is that candidate-directed drives improve detection of wrong priors at a matched measurement budget while retaining correct priors.

1. **Fix the phantom, solver, and data roles.** Use the same physical case, geometry, forward model, and inversion budget across prior settings. Start by reversing conductivity contrast. Generate candidates from drive block A. Use B to select and lock the returned field. Then open C for final testing. Vary contact and prior mismatch separately to test whether the chosen drives can distinguish these effects.
2. **Fix the endpoints independently.** Use repeats to estimate electrical variability. Independently measure same-frequency material conductivity and evaluate means in fixed regions. Report wrong-prior retention, rejection of correct priors, abstention, held-out voltage error, and regional conductivity error. Use independent phantoms or sessions as sampling units.
3. **Test material recovery as well as detection.** Let <span class="literature-math">L</span> denote independent property error. Use <span class="literature-math">w</span> for wrong prior and <span class="literature-math">0</span> for no external image prior. Use s for voltage screening and b for the matched baseline. Let <span class="literature-math">Δ<sub>w</sub></span> and <span class="literature-math">Δ<sub>0</sub></span> denote paired changes in error with voltage screening versus the baseline in each group. A negative <span class="literature-math">Δ<sub>w</sub></span> shows improvement in the wrong-prior group. A negative <span class="literature-math">Δ<sub>w</sub>−Δ<sub>0</sub></span> would also support a benefit specific to prior mismatch. Report both contrasts.

<div class="literature-equation">
  <math display="block"><msub><mi>Δ</mi><mi>j</mi></msub><mo>=</mo><mi>L</mi><mo stretchy="false">(</mo><mi>j</mi><mo>,</mo><mi>s</mi><mo stretchy="false">)</mo><mo>−</mo><mi>L</mi><mo stretchy="false">(</mo><mi>j</mi><mo>,</mo><mi>b</mi><mo stretchy="false">)</mo><mo>,</mo><mspace width="0.5em"/><mi>j</mi><mo>∈</mo><mo>{</mo><mi>w</mi><mo>,</mo><mn>0</mn><mo>}</mo></math>
</div>

## 7. Conclusion
{: #conclusion }

Held-out voltages directly test whether a locked reconstruction explains unused measurements. Their ability to reveal a wrong prior depends on response separation, model mismatch, and the measurement chain. The KIT4 reanalysis provides a reproducible voltage-only baseline and shows how the number of held-out readings can differ from the gain in ideal response dimension. A decisive follow-up would change the internal prior, seal newly measured voltages, and independently measure target conductivity on the same physical phantom.

## References
{: #references }

1. <span id="ref-cem"></span> Somersalo E, Cheney M, Isaacson D. *Existence and uniqueness for electrode models for electric current computed tomography*. SIAM Journal on Applied Mathematics, 1992, 52(4), 1023–1040. [DOI](https://doi.org/10.1137/0152060)
2. <span id="ref-pls"></span> Kolehmainen V, Ehrhardt MJ, Arridge SR. *Incorporating structural prior information and sparsity into EIT using parallel level sets*. Inverse Problems and Imaging, 2019, 13(2), 285–307. Table 2 and Fig. 3. [DOI](https://doi.org/10.3934/ipi.2019015)
3. <span id="ref-dpe"></span> Wang J, Deng J, Liu D. *Deep prior embedding method for Electrical Impedance Tomography*. Neural Networks, 2025, 188, 107419. Fig. 7. [DOI](https://doi.org/10.1016/j.neunet.2025.107419)
4. <span id="ref-asfaw"></span> Asfaw Y, Adler A. *Automatic detection of detached and erroneous electrodes in electrical impedance tomography*. Physiological Measurement, 2005, 26(2), S175–S183. [DOI](https://doi.org/10.1088/0967-3334/26/2/017)
5. <span id="ref-harrach"></span> Harrach B. *Interpolation of missing electrode data in electrical impedance tomography*. Inverse Problems, 2015, 31(11), 115008. [DOI](https://doi.org/10.1088/0266-5611/31/11/115008)
6. <span id="ref-kit4"></span> Hauptmann A, Kolehmainen V, Mach NM, Savolainen T, Seppänen A, Siltanen S. *Open 2D Electrical Impedance Tomography data archive*. 2017. [Data description](https://arxiv.org/abs/1704.01178) · [KIT4 v1 archive](https://doi.org/10.5281/zenodo.1203914)
7. <span id="ref-denker"></span> Denker A, Margotti F, Ning J, et al. *Deep learning based reconstruction methods for electrical impedance tomography*. Handbook of Numerical Analysis, 2025. Table 3 and published Eq. (37). [DOI](https://doi.org/10.1016/bs.hna.2025.09.003)
8. <span id="ref-masiri"></span> Mohammadi Masiri V, Salimi Shahraki A, Abbasi M. *Cloud–edge collaborative intelligence for privacy-preserving electrical impedance tomography reconstruction with federated deep D-bar*. Journal of Cloud Computing, 2026. Table 8. [DOI](https://doi.org/10.1186/s13677-026-01000-6)
9. <span id="ref-hong"></span> Hong J, Kim J, Lee B, et al. *Feasibility of prior-informed domain-based electrical impedance tomography for deep tissue thermometry: Phantom experiments and computed tomography-derived numerical simulations*. Medical Physics, 2026, 53(12), e70774. Table 2 and Figs. 5–7 and 9. [DOI](https://doi.org/10.1002/mp.70774)
