---
layout: article
section: group
parent_url: /group/research/#research
parent_label: 科研进展
lang: zh-CN
title: 电阻抗成像科研进展
summary: 从完整电极模型、加速反演到不规则边界有限元正演，梳理课题组现阶段的技术工作与验证范围。
permalink: /group/research/eit-technical-progress/
alternate_url: /en/group/research/eit-technical-progress/
---

## 完整电极模型与伴随灵敏度

课题组从有限尺寸电极上的总注入电流出发，建立包含电极接触阻抗的完整电极模型（CEM）。有限元正演在给定电导率、接触阻抗和电流模式时计算电极电压。报告同时推导了伴随灵敏度，用于计算电压残差对电导率变化的响应，为后续反演提供梯度。模型还将电极末端、绝缘边界和电势零平均条件纳入离散计算。〔技术报告 §1，PDF 第 1–8 页〕

## 两点梯度加速与多激励反演

反演采用带两点梯度的 Landweber 迭代，并以 Kaczmarz 方式分组利用多种电流激励。报告比较了类 L¹ 和类全变差（TV）正则化，并展示了合成数据和公开 KIT4 水槽实测电压的重建示例。现有图例可用于分析不同正则项的重建形态。速度、误差和稳定性还需要在统一参数与停机准则下补做对照，绝对电导率也需要独立物性参照。〔技术报告 §2、§5，PDF 第 9–10、17–22 页〕 · [公开 KIT4 数据](https://zenodo.org/records/1203914)

<figure class="literature-figure">
  <a href="{{ '/assets/images/group/eit-synthetic-reconstruction.png' | relative_url }}"><img src="{{ '/assets/images/group/eit-synthetic-reconstruction.png' | relative_url }}" width="1164" height="734" alt="合成电导率真值、类 L1 和类 TV 反演的四组对照。" loading="lazy" decoding="async"></a>
  <figcaption>从上到下显示合成真值、类 L¹ 和类 TV 反演。留意不同正则项下目标形态及边缘伪影。类 L¹ 与类 TV 所示参数分别为 10 和 0.1。裁自技术报告 PDF 第 19 页。</figcaption>
</figure>

## 不规则边界、电极定位与正演核验

给定离散边界坐标，先重建闭合曲线，再按弧长布置电极，并把电极端点和绝缘区标记传递到有限元网格。报告以具有解析边界的合成算例作参照，比较了 B 样条拟合与周期立方插值。56 个边界样点、16 个电极、名义网格步长 <span class="literature-math">h = 0.01</span> 时，以解析边界上名义网格步长 <span class="literature-math">h = 0.0035</span> 的计算为参照，全激励电极电压矩阵的相对误差分别为 **1.1920%** 与 **0.4551%**。同一网格步长下，直接使用解析几何的正演也与细网格参照相差约 **0.42%**，因此应结合离散误差解读两种边界方法的比较。上述数值评价的是该合成设置下的正演。〔技术报告附录 A，表 1，PDF 第 24–31 页〕

<figure class="literature-figure">
  <a href="{{ '/assets/images/group/eit-irregular-domain-mesh.png' | relative_url }}"><img src="{{ '/assets/images/group/eit-irregular-domain-mesh.png' | relative_url }}" width="1208" height="427" alt="从光滑闭合边界和电极，到多边形近似及三角网格。" loading="lazy" decoding="async"></a>
  <figcaption>56 点合成边界案例。左为闭合曲线和电极，中为带标签的多边形边界，右为 21,222 个三角形的有限元网格。图示名义步长 h = 0.02。裁自技术报告图 14，PDF 第 29 页。</figcaption>
</figure>

## 下一步如何验证

后续可在可控水槽模体中分别改变电极接触状态和物体形状，使用同批原始测量比较边界建模与重建方法。评价时同时报告封存电压残差、目标定位误差和独立测得的区域电导率，以确定误差来自几何、接触建模还是反演本身。 [研究前沿专题]({{ '/group/frontiers/quantitative-eit/' | relative_url }})

**技术来源**　Jijun Liu、Dong Wang、Min Zhong、Kai Zhu，*On the fast detection of bio-tissue conductivity from complete EIT model*，课题组技术报告。
