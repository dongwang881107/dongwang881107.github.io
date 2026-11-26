---
group_kind: frontier
date: 2026-11-25
image:
  path: /assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png
  width: 1278
  height: 675
  alt: "Voltage recombination errors across 38 KIT4 tank cases."
  caption: "Voltage recombination errors in 38 KIT4 cases · Dong Wang’s analysis"
layout: article
section: group
parent_url: /en/group/research/#frontiers
parent_label: Research frontiers
lang: en
title: How can EIT move from seeing a target to measuring it?
description: Work from Jijun Liu’s group on joint inversion and the complete electrode model motivates tests of absolute conductivity accuracy.
summary: What structural priors, held-out voltages, and independent physical measurements can tell us about conductivity accuracy.
permalink: /en/group/frontiers/quantitative-eit/
alternate_url: /group/frontiers/quantitative-eit/
---

## What should we measure once a target is visible?

Electrical impedance tomography (EIT) estimates internal conductivity from currents and voltages at the boundary. In a saline tank, a reconstruction might correctly locate two targets and draw their outlines, yet estimate one target's conductivity too close to the background. Absolute imaging raises two further questions. How close is the mean conductivity in a fixed region to an independent measurement? How does that error change as a target gets smaller, moves deeper, or electrode contact changes?

## What questions have two studies from the group addressed?

**How do boundary errors affect the interior estimate?** Jinchao Pan and Jijun Liu study simultaneous recovery of boundary impedance and interior conductivity using local interior measurements. They establish uniqueness under stated assumptions and give regularization error estimates that account for errors propagated from the boundary impedance estimate. These results rely on interior measurements. Conventional electrode-only EIT requires a separate validation. [Pan and Liu, SIAM Journal on Applied Mathematics, 2026](https://doi.org/10.1137/24M1687066)

**How do different penalties change the image?** A preprint by Kai Zhu, Jijun Liu, and Min Zhong applies adaptive Nesterov momentum to the complete electrode model. They calibrate background conductivity and contact impedance from empty-tank KIT4 measurements, then compare L², L¹, and total variation (TV) penalties. In the tested tank configurations, L² tends to produce smoother, more diffuse images, and TV gives more spatially coherent localization. An independent measurement on the same phantom could test the accuracy of the recovered conductivity magnitude. [Zhu, Liu, and Zhong, August 2026 preprint, Section 4](https://arxiv.org/abs/2608.25837v1)

Two external studies suggest biases worth testing separately. In Perez et al.’s planar-array simulation, smaller targets gave lower conductivity estimates. Mixing between the target and the background at finite spatial resolution is one possible contributor, often described as a partial-volume effect. In one tank case from Wang et al., keeping a reversed-contrast prior active through a frozen branch increased relative reconstruction error from 0.077 in the baseline to 0.111. [Perez et al., Figures 6–8](https://radar.brookes.ac.uk/radar/file/2b7ccb0f-6a24-41ef-be10-fa7603513389/1/perez2016three-dimensional.pdf) · [Wang et al., Figure 7](https://doi.org/10.1016/j.neunet.2025.107419)

## What voltage baseline do 38 open cases provide?

As a supplementary analysis on his personal website, Dong Wang used adjacent-drive voltages to linearly predict separately recorded skip-one and skip-two voltages in 38 public KIT4 v1 tank cases. The median per-case relative errors were **1.34%** and **1.30%**, respectively. These values quantify how the original readings depart from linear recombination. To test a particular prior, we also need estimates of repeatability, contact and geometric error, and the separation between candidate voltage predictions on the held-out drives. [KIT4 source data](https://zenodo.org/records/1203914) · [Methods, case-level results, and code]({{ '/en/knowledge/eit/held-out-voltage-and-wrong-priors/#results' | relative_url }})

<figure class="literature-figure">
  <img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png' | relative_url }}" width="1278" height="675" alt="Voltage recombination errors for 38 KIT4 cases. The medians are 1.34 percent for skip-one and 1.30 percent for skip-two." loading="lazy" decoding="async">
  <figcaption>Case-level errors when adjacent-drive voltages predict the skip-one and skip-two groups. The figure comes from Dong Wang’s supplementary analysis.</figcaption>
</figure>

## Which next experiment would link voltage fit to conductivity accuracy?

Compare three reconstructions of the same physical phantom with a fixed solver and data budget. Use a baseline without an image prior, a matched prior, and a reversed-contrast prior. Fit on one block of original measurements, tune on a second, and open a third only after locking the candidates. Measure target and background conductivity independently at matched frequency and temperature, with scoring regions fixed in physical coordinates. Vary target size, position, and contact conditions. Compare held-out voltage residuals and regional conductivity errors to see when voltage-based screening selects a more accurate conductivity map. [Derivation and proposed design]({{ '/en/knowledge/eit/held-out-voltage-and-wrong-priors/#proposed-study' | relative_url }})
