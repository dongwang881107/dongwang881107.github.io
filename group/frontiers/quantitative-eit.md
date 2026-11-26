---
group_kind: frontier
date: 2026-11-25
image:
  path: /assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png
  width: 1278
  height: 675
  alt: "38 个 KIT4 水槽案例的电压重组误差分布。"
  caption: "38 个 KIT4 案例的电压重组误差 · 王冬复核"
layout: article
section: group
parent_url: /group/research/#frontiers
parent_label: 研究前沿
lang: zh-CN
title: 电阻抗成像怎样从“看得见”走向“量得准”？
description: 从刘继军团队的边界与内部参数联合反演、完整电极模型重建出发，讨论如何验证绝对电导率。
summary: 从结构先验、留出电压和独立物性测量入手，讨论怎样验证重建出的电导率。
permalink: /group/frontiers/quantitative-eit/
alternate_url: /en/group/frontiers/quantitative-eit/
---

## 看见目标之后，还要量什么？

电阻抗成像（EIT）通过边界电流和电压，反推内部的电导率分布。在水槽里，两个夹杂物的位置和轮廓可能都重建对了，其中一个的电导率仍可能偏向背景。绝对成像要进一步回答两个问题。固定区域的平均电导率离独立测量值有多远？目标变小、移向深部或电极接触变化时，这个误差是否稳定？

## 团队的两项工作分别推进了什么？

**边界误差如何传到内部？** Jinchao Pan 与刘继军在使用局部内部观测的条件下研究边界阻抗与内部电导率的同时反演，给出一定先验条件下的唯一性和正则化误差估计，并分析边界阻抗恢复误差如何影响电导率。这些结论依赖内部观测，常规 EIT 只测电极端电压时仍需另行验证。 [Pan 与 Liu，SIAM Journal on Applied Mathematics，2026](https://doi.org/10.1137/24M1687066)

**不同正则项如何改变成像？** Kai Zhu、刘继军与 Min Zhong 的预印本将自适应 Nesterov 动量用于完整电极模型，先用 KIT4 空槽测量校准背景电导率和接触阻抗，再比较 L²、L¹ 和总变差（TV）。在所测水槽案例中，L² 的结果通常更平滑、弥散，TV 的定位更连贯。下一步可在同一模体用独立测量核验目标区的电导率幅值。 [Zhu、Liu 与 Zhong，2026 年 8 月预印本，第 4 节](https://arxiv.org/abs/2608.25837v1)

外部研究提示了两项值得单独检验的偏差。Perez 等在平面电极阵列仿真中观察到，目标越小，重建电导率幅值越低。有限分辨率下目标与背景的混合可作为待检验的部分容积效应。Wang 等的实体水槽案例则表明，材料对比度反转的先验经冻结分支持续参与时，相对重建误差从无先验时的 0.077 升至 0.111。 [Perez 等，图 6–8](https://radar.brookes.ac.uk/radar/file/2b7ccb0f-6a24-41ef-be10-fa7603513389/1/perez2016three-dimensional.pdf) · [Wang 等，图 7](https://doi.org/10.1016/j.neunet.2025.107419)

## 38 个公开案例给出怎样的电压基线？

王冬在个人网站知识库补充复核了公开 KIT4 v1 的 38 个水槽案例，用相邻注流的实测电压线性预测同一案例另行记录的跳一和跳二电压。逐例相对误差的中位数分别为 **1.34%** 和 **1.30%**。这两个数描述原始读数与线性重组的差距。将它们用于判断具体先验是否错误，还要估计重复采集波动、接触与几何误差，以及两张候选图在留出观测上的可区分程度。 [KIT4 原始数据](https://zenodo.org/records/1203914) · [复核方法、逐例结果与代码]({{ '/knowledge/eit/held-out-voltage-and-wrong-priors/#results' | relative_url }})

<figure class="literature-figure">
  <img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png' | relative_url }}" width="1278" height="675" alt="38 个 KIT4 水槽案例的电压重组误差。跳一和跳二组的中位数分别为 1.34% 和 1.30%。" loading="lazy" decoding="async">
  <figcaption>相邻注流电压预测跳一、跳二组的逐例误差。数据来自王冬个人网站的补充复核。</figcaption>
</figure>

## 哪项实验可以把两个问题连起来？

可在同一实体模体上比较无图像先验、匹配先验和材料对比度反转先验，固定求解器和数据预算。用一组原始数据拟合、一组选参，锁定候选后才打开第三组电压。独立测量应与 EIT 的频率、温度匹配，并在固定实物坐标内评价目标与背景的平均电导率。改变目标尺寸、位置和接触条件后，逐项比较留出电压残差与物性误差。这样可以检验，电压筛选是否确实选出了物性更准确的图像，以及它在哪些条件下失效。 [推导与实验设计]({{ '/knowledge/eit/held-out-voltage-and-wrong-priors/#proposed-study' | relative_url }})
