---
title: Can held-out voltages detect a wrong prior in EIT?
summary: Tank experiments, measured KIT4 voltages, and independent physical references clarify when held-out prediction can test a conductivity reconstruction.
topic: Electrical Impedance Tomography (EIT)
lang: en
updated: 2026-11-21
permalink: /en/knowledge/eit/held-out-voltage-and-wrong-priors/
alternate_url: /knowledge/eit/held-out-voltage-and-wrong-priors/
---

*A research question note based on the Electrical Impedance Tomography project’s knowledge base on prior mismatch, held-out observations, and independent physical references.*

Imagine a prior that locates two targets correctly but reverses their high and low conductivities. A reconstruction can still place both targets correctly. Could a set of measured voltages held back from the inversion reveal the conductivity error? **Held-out voltages can help when the predictions from competing reconstructions differ by more than the noise and model error under the test drives. Identifying which property is wrong also requires a reference for that property.**

## What does the existing evidence establish?

- **A wrong prior can affect reconstruction from real tank data.** In Wang et al.’s Case 5, the prior deliberately reversed the conductivity contrast. The reported relative reconstruction errors were 0.077 with no external image prior, 0.077 when the incorrect prior was used only for initialization, and 0.111 when its frozen branch remained in the inversion. The contrast shows that how the prior enters the algorithm matters. The errors use a reference image constructed from photos and assigned material values. Figure 7 tests the intervention on the prior and its reconstruction result. Screening with held-out voltages is a follow-up question. [Wang et al., Fig. 7, published PDF p. 10](https://doi.org/10.1016/j.neunet.2025.107419)
- **Held-out measurements can test observable anomalies.** Asfaw and Adler used measurements from other electrodes to predict held-out readings and compared the predictions with measurements to identify faulty electrodes. The test design can inform a wrong-prior study. In the original study, the intervention concerns electrodes. An experiment on an incorrect internal structure would need to vary that prior directly. [Asfaw and Adler’s electrode-fault study](https://doi.org/10.1088/0967-3334/26/2/017)
- **The independent reference determines what can be validated.** Hong et al. compared regional temperatures with two thermocouples per region in physical phantoms. In a separate CT-based simulation, they deliberately shifted the prescribed regions. The first experiment tests regional temperature at the probe locations. The second tests the effect of a simulated partition error. Both help design a comparison on a single physical phantom. [Hong et al.’s phantom and simulation study](https://doi.org/10.1002/mp.70774)

## What makes a held-out drive informative?

The open KIT4 archive contains measured voltages from several physical current patterns on the same tank configuration, along with photographs. Holding back complete groups of original drives makes it possible to test predictions from a frozen reconstruction. At fixed conductivity and electrode conditions, electrode voltages depend linearly on the applied currents. Under a common readout protocol, some held-out drives can lie in the span of drives used for fitting and selection. Their actual readings still test predictions on unused records. To add information about the unknown, check whether the measurements probe a new response direction and whether that direction distinguishes the candidate reconstructions. Voltages synthesized by changing the basis of the training data remain transformations of those measurements. [KIT4 data archive](https://doi.org/10.5281/zenodo.1203914) · [Data and acquisition protocol](https://arxiv.org/abs/1704.01178)

A two-candidate example makes the condition explicit. Let <span class="literature-math">p<sub>1</sub></span> and <span class="literature-math">p<sub>2</sub></span> be the predicted voltages for two fixed reconstructions on the same held-out group. If the first prediction lies within <span class="literature-math">ε</span> of the measurements and the predictions differ by more than <span class="literature-math">2ε</span>, the triangle inequality guarantees a larger residual for the second candidate. This comparison concerns those two reconstructions. Estimating <span class="literature-math">ε</span> requires accounting for measurement noise and forward-model error.

Photographs can check location and shape. To evaluate mean regional conductivity, an independent measurement of the material in the same specimen should use the same frequency, with scoring regions fixed in physical coordinates. A reconstruction can predict the held-out voltages well while conductivity remains inaccurate in a region to which those drives have little sensitivity.

## A test on a single physical phantom

1. **Control the prior.** Keep the geometry, contact conditions, frequency, and inversion budget fixed. Compare no external image prior, an accurate prior, and a controlled wrong prior. Start with one error type, such as reversing the conductivity contrast.
2. **Assign data roles before viewing results.** Fit on one group of original drives. Use a second to choose the prior weight or a fallback. Open the final group only after locking the candidate reconstructions. Record shared references, reciprocal readings, and the role of calibration parameters.
3. **Report both errors.** Report held-out voltage prediction error and mean conductivity error in fixed regions with independent material references. A larger held-out error can flag a candidate affected by a wrong prior. If the predicted voltages improve while the estimated material property moves farther from its reference, retain the case and examine drive sensitivity and forward-model mismatch.

The cases reviewed in the knowledge base establish elements of this test across separate studies. Putting deliberate prior mismatch, sealed measured voltages, and an independent property reference in one physical case would establish how much the voltage test helps screen wrong priors.
