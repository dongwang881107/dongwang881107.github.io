---
layout: article
section: group
parent_url: /en/group/research/#research
parent_label: Research progress
lang: en
title: Research Progress in Electrical Impedance Tomography
summary: The complete electrode model, accelerated inversion, and finite-element forward validation on reconstructed boundaries.
permalink: /en/group/research/eit-technical-progress/
alternate_url: /group/research/eit-technical-progress/
---

## Complete electrode model and adjoint sensitivities

The complete electrode model (CEM) represents the net current on each finite electrode and accounts for electrode contact impedance. The finite-element forward solver predicts electrode voltages from the conductivity, contact impedances, and current pattern. The report derives adjoint sensitivities to compute the gradient of the voltage misfit with respect to the conductivity. The implementation also tracks electrode endpoints and insulating boundary segments and imposes a zero-mean gauge on electrode potentials. [Technical report, Section 1, PDF pp. 1–8]

## Two-point acceleration and multiple current patterns

The inverse method combines a two-point gradient Landweber iteration with Kaczmarz updates over multiple current patterns. The report compares L¹-type and total-variation penalties and shows reconstructions from simulated data and measured voltages from the open KIT4 tank dataset. The figures illustrate how penalties change reconstruction shape. Matched comparisons would be needed to quantify runtime, error, and robustness, and an independent physical reference is needed to assess absolute conductivity. [Technical report, Sections 2 and 5, PDF pp. 9–10 and 17–22] · [Public KIT4 data](https://zenodo.org/records/1203914)

<figure class="literature-figure">
  <a href="{{ '/assets/images/group/eit-synthetic-reconstruction.png' | relative_url }}"><img src="{{ '/assets/images/group/eit-synthetic-reconstruction.png' | relative_url }}" width="1164" height="734" alt="Four synthetic test cases showing the reference conductivity and the L1-type and TV-type reconstructions." loading="lazy" decoding="async"></a>
  <figcaption>Top to bottom are the synthetic reference, L¹-type reconstruction, and TV-type reconstruction. Compare target shape and artifacts near the boundary. The reported penalty parameters are 10 and 0.1 respectively. Cropped from the technical report, PDF p. 19.</figcaption>
</figure>

## Irregular boundaries, electrode placement, and forward validation

The workflow reconstructs a closed curve from discrete boundary coordinates, places electrodes by arc length, and passes electrode endpoints and insulation tags to a finite-element mesh. An experiment with a synthetic analytical boundary compares B-spline fitting and periodic cubic interpolation. With 56 boundary observations, 16 electrodes, and nominal mesh size <span class="literature-math">h = 0.01</span>, the relative errors of the electrode voltage matrix over all drives were **1.1920%** and **0.4551%**, respectively, against a reference calculated on the analytical boundary at nominal mesh size <span class="literature-math">h = 0.0035</span>. At the same nominal size, the calculation on the analytical boundary itself differed from that reference by about **0.42%**. The comparison therefore includes discretization effects and applies to forward predictions under this specific synthetic configuration. [Technical report, Appendix A, Table 1, PDF pp. 24–31]

<figure class="literature-figure">
  <a href="{{ '/assets/images/group/eit-irregular-domain-mesh.png' | relative_url }}"><img src="{{ '/assets/images/group/eit-irregular-domain-mesh.png' | relative_url }}" width="1208" height="427" alt="A smooth closed boundary and electrodes, its polygonal approximation, and the triangular mesh." loading="lazy" decoding="async"></a>
  <figcaption>The synthetic 56-point example. From left to right, the closed curve with electrodes, a tagged polygonal boundary, and the 21,222-triangle finite-element mesh at nominal h = 0.02. Cropped from the technical report, Figure 14, PDF p. 29.</figcaption>
</figure>

## What needs to be verified next?

A controlled tank experiment could vary electrode contact and target geometry separately, then compare candidate models on the same raw measurements. Reporting the residual on held-out voltages, localization error, and independently measured regional conductivity would help trace errors to geometry, contact modeling, or the inverse method. [Related research frontier]({{ '/en/group/frontiers/quantitative-eit/' | relative_url }})

**Technical source**　Jijun Liu, Dong Wang, Min Zhong, and Kai Zhu, *On the fast detection of bio-tissue conductivity from complete EIT model*, research group technical report.
