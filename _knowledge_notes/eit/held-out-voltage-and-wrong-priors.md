---
title: EIT 中，留出电压能识别错误先验吗？
summary: 从完整电极模型出发，结合错先验水槽实验、同源文献对照与 38 例 KIT4 电压复核，推导可检出条件并提出实体模体验证方案。
topic: 电阻抗成像（EIT）
lang: zh-CN
updated: 2026-11-21
permalink: /knowledge/eit/held-out-voltage-and-wrong-priors/
alternate_url: /en/knowledge/eit/held-out-voltage-and-wrong-priors/
---

*研究短文。以「电阻抗成像」项目知识库的错先验、实测留出和物性验收三个专题为基础。*

**摘要。** 电阻抗成像（EIT）可用结构图像缓解病态性，但结构或材料对比度写错时，反演仍可能较好地拟合边界电压。本文问的是，封存一组实测电压，能否发现这个错误并帮助选出物性更准的重建？我们从完整电极模型推导两候选的充分可分条件，交叉核对错先验水槽、合成拓扑扰动、KIT4 基准和模体物性参照，并对 KIT4 v1 的 38 例原始电压独立重算。以相邻注流的实测电压预测跳二组，病例级相对误差中位数为 **1.30%**。这个基线表明，同一理想激励空间内，原始测量仍会偏离线性重组。检出先验错误取决于候选在留出测量上的电压分离度，物性是否改善则需在同一实体案例用独立参照判断。

<nav class="literature-toc" aria-label="本文目录">
  <a href="#question">问题与难点</a><a href="#prior-work">研究现状</a><a href="#theory">数学模型</a><a href="#results">实验结果</a><a href="#cross-check">交叉验证</a><a href="#proposed-study">研究方案</a><a href="#conclusion">结论</a><a href="#references">参考文献</a>
</nav>

## 1. 问题提出与难点
{: #question }

设盐水槽中有两个位置已知的夹杂物，一块比背景导电，另一块比背景更阻性。先验图保留两个轮廓，却把材料高低写反。用先验参与反演时，即使重建轮廓看起来正确，目标电导率和背景定量仍可能偏离真实值。这里要回答两个递进问题。第一，真正留出的电压能否区分正确和错误先验得到的候选？第二，按电压选择候选后，目标的独立物性误差是否也随之减小？

- **边界测量对位置和幅值的灵敏度不同。** 两个电导率场可以产生很近的端电压。少量额外激励只有在对目标差异敏感时才增加鉴别力。
- **电压偏差有多种来源。** 接触阻抗、边界几何、参考漂移和增益误差都能改变端电压。即使看到封存残差升高，也需要额外对照才能把原因归到先验。
- **留出必须沿原始数据链定义。** 参与归一化、接触参数估计、选择正则化强度或回退方案的测量，已经向候选提供了信息。互易读数、同一激励的换基合成以及共享参考也会造成依赖。
- **几何正确与定量正确需要不同参照。** 照片可以检查位置、轮廓和面积。区域电导率应在与 EIT 一致的频率和温度条件下独立测量，并在事先固定的物理坐标上评分。

## 2. 研究现状与证据范围
{: #prior-work }

本文是针对固定科学问题的证据综合。我们从知识库中选取有明确先验干预、观测角色或物性参照的研究，回查原文的公式、图表和数据说明。评价对象是各研究实际返回的图像或物性标量。案例来源相同的研究按同一采集谱系解释，论文之间的指标各用原定义。

**结构约束。** Kolehmainen 等用平行水平集把辅助图像的边缘方向纳入正则化，并用稀疏项允许额外边缘。Wang 等让图像先验进入坐标网络，可以只用于初始化，也可以保留冻结分支持续参与反演。两种机制都会改变哪些解容易出现，先验偏差涉及拓扑、位置、对比度和载入方式。 [2](#ref-pls) · [3](#ref-dpe)

**电压诊断。** Asfaw 和 Adler 用其余测量预测暂时排除的电极读数，以识别故障电极。Harrach 的差分 EIT 插值用电导率变化的先验上界，从未注流电极的电压推算缺失读数。在实验设计上，算法填充的读数与仪器另行记录的读数承担不同角色。 [4](#ref-asfaw) · [5](#ref-harrach)

**定量参照。** Denker 和 Masiri 的 KIT4 基准同时报告电压误差和照片分割 Dice。Hong 等在实体模体中使用独立温度探针，评价与重建输出对应的区域温度。前两者可对照拟合与几何，后者展示如何用独立传感量核查一个有物理单位的终点。 [7](#ref-denker) · [8](#ref-masiri) · [9](#ref-hong)

## 3. 数学模型与可检出条件
{: #theory }

### 3.1 从电导率到端电压

在域 Ω 内，电势 <span class="literature-math">u</span> 与正电导率 <span class="literature-math">σ</span> 满足守恒方程。第 <span class="literature-math">ℓ</span> 个电极 <span class="literature-math">E<sub>ℓ</sub></span> 的端电势为 <span class="literature-math">U<sub>ℓ</sub></span>，接触阻抗为 <span class="literature-math">z<sub>ℓ</sub></span>，净注入电流为 <span class="literature-math">I<sub>ℓ</sub></span>。令 <span class="literature-math">j<sub>n</sub> = σ∂<sub>n</sub>u</span> 为外法向通量。非电极边界无通量，净注流为零，并固定端电势的加性常数。 [1](#ref-cem)

<div class="literature-equation">
  <math display="block"><mo>∇</mo><mo>·</mo><mo stretchy="false">(</mo><mi>σ</mi><mo>∇</mo><mi>u</mi><mo stretchy="false">)</mo><mo>=</mo><mn>0</mn><mo>,</mo><mspace width="0.6em"/><mi>x</mi><mo>∈</mo><mi>Ω</mi></math>
  <math display="block"><mi>u</mi><mo>+</mo><msub><mi>z</mi><mi>ℓ</mi></msub><msub><mi>j</mi><mi>n</mi></msub><mo>=</mo><msub><mi>U</mi><mi>ℓ</mi></msub><mo>,</mo><mspace width="0.5em"/><msub><mo>∫</mo><msub><mi>E</mi><mi>ℓ</mi></msub></msub><msub><mi>j</mi><mi>n</mi></msub><mi>d</mi><mi>s</mi><mo>=</mo><msub><mi>I</mi><mi>ℓ</mi></msub></math>
  <math display="block"><msub><mo>∑</mo><mi>ℓ</mi></msub><msub><mi>I</mi><mi>ℓ</mi></msub><mo>=</mo><mn>0</mn><mo>,</mo><mspace width="0.65em"/><msub><mo>∑</mo><mi>ℓ</mi></msub><msub><mi>U</mi><mi>ℓ</mi></msub><mo>=</mo><mn>0</mn></math>
</div>

令 <span class="literature-math">η</span> 汇总几何、电极位置、接触和仪器参数，<span class="literature-math">F<sub>C</sub></span> 包含封存组 <span class="literature-math">C</span> 的注流和读出。令 e<sub>C</sub> 为测量误差，J 为对应偏导。两种解释在局部产生的无噪电压差，既受内部电导率扰动影响，也受上述参数扰动影响。

<div class="literature-equation">
  <math display="block"><msub><mi>y</mi><mi>C</mi></msub><mo>=</mo><msub><mi>F</mi><mi>C</mi></msub><mo stretchy="false">(</mo><mi>σ</mi><mo>,</mo><mi>η</mi><mo stretchy="false">)</mo><mo>+</mo><msub><mi>e</mi><mi>C</mi></msub></math>
  <math display="block"><mi>Δ</mi><msub><mi>F</mi><mi>C</mi></msub><mo>≈</mo><msub><mi>J</mi><mrow><mi>σ</mi><mo>,</mo><mi>C</mi></mrow></msub><mi>Δ</mi><mi>σ</mi><mo>+</mo><msub><mi>J</mi><mrow><mi>η</mi><mo>,</mo><mi>C</mi></mrow></msub><mi>Δ</mi><mi>η</mi></math>
</div>

这是一阶关系。若目标电导率的改变主要落在留出组的弱灵敏方向，或其电压影响可被合理的接触参数变化抵消，单个残差大小就很难确定错误的来源。

### 3.2 两个候选需要在测量上相距多远？

比较两张冻结后的候选图。设 <span class="literature-math">p<sub>1</sub></span>、<span class="literature-math">p<sub>2</sub></span> 为它们在组 <span class="literature-math">C</span> 的电压预测，<span class="literature-math">y</span> 为实际读数，<span class="literature-math">‖·‖<sub>W</sub></span> 是在相同通道上使用的加权范数，<span class="literature-math">T</span> 为参考测量和模型不确定性给出的误差上界。如果候选 1 对实测的残差至多为 <span class="literature-math">T</span>，用三角不等式得到：

<div class="literature-equation">
  <math display="block"><msub><mrow><mo>‖</mo><mi>y</mi><mo>−</mo><msub><mi>p</mi><mn>2</mn></msub><mo>‖</mo></mrow><mi>W</mi></msub><mo>≥</mo><msub><mrow><mo>‖</mo><msub><mi>p</mi><mn>1</mn></msub><mo>−</mo><msub><mi>p</mi><mn>2</mn></msub><mo>‖</mo></mrow><mi>W</mi></msub><mo>−</mo><mi>T</mi></math>
</div>

所以当 <span class="literature-math">‖p<sub>1</sub>−p<sub>2</sub>‖<sub>W</sub> &gt; 2T</span> 时，候选 2 的残差必大于 <span class="literature-math">T</span>。这是一个**有条件的充分判据**。小于这个分离程度时，结果取决于实际误差方向。实践中可用重复采集估计噪声，再用指定范围内的几何和接触扰动估计模型偏差。共享参考导致的误差相关应纳入估计。

### 3.3 多测 256 个读数，增加了多少信息？

固定电导率、接触和几何时，端电压对注流线性。对理想的实数互易模型，净零注流空间的维数为 <span class="literature-math">d = M−1</span>，其中 <span class="literature-math">M</span> 是电极数。令已参与拟合和选参的激励张成 <span class="literature-math">k</span> 维空间，且每组能完整读出端电势差。选择与该空间对齐的基后，已知的是对称响应矩阵的前 <span class="literature-math">k</span> 列及相应行。剩下的自由度只在一个 <span class="literature-math">(d−k)×(d−k)</span> 的对称块中。 [1](#ref-cem) · [6](#ref-kit4)

<div class="literature-equation">
  <math display="block"><mi>r</mi><mo stretchy="false">(</mo><mi>k</mi><mo stretchy="false">)</mo><mo>=</mo><mi>d</mi><mi>k</mi><mo>−</mo><mfrac><mrow><mi>k</mi><mo stretchy="false">(</mo><mi>k</mi><mo>−</mo><mn>1</mn><mo stretchy="false">)</mo></mrow><mn>2</mn></mfrac></math>
</div>

因此增加原始采集记录、增加理想响应坐标、提高对某种先验错误的灵敏度，是需要逐一检查的三个量。存在丢弃通道或电极故障时，应按实际激励与读出重新计算观测秩。

## 4. 实验结果
{: #results }

### 4.1 已发表结果：材料反转可以使水槽重建退化

Wang 等的 Case 5 同时包含铁环和塑料柱。图 7 中，不用外部图像先验时相对重建误差（RE）为 0.077。材料对比度反转的先验只用于初始化时仍为 0.077，冻结分支持续参与时上升到 0.111。对位的 Prior 1 下，仅初始化为 0.066，持续参与为 0.063。该误差以参考电导率的范数归一化。参考图用照片和材料赋值构建，数值来自同一个实体水槽案例。该图的可用结论是**先验内容和进入反演的方式共同影响重建**。 [3](#ref-dpe)

<figure class="literature-figure">
  <a href="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/wang2025-case5-prior-error.png' | relative_url }}"><img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/wang2025-case5-prior-error.png' | relative_url }}" width="1320" height="818" alt="图 1。真实水槽 Case 5 中，匹配先验持续嵌入时误差下降，反转对比度先验持续嵌入时误差升高。" loading="lazy" decoding="async"></a>
  <figcaption><strong>图 1。真实水槽 Case 5 中，匹配先验持续嵌入时误差下降，反转对比度先验持续嵌入时误差升高。</strong> 无外部图像先验为共同基线。根据 Wang 等正式版图 7 所标相对误差重绘。每个点对应同一案例的一种反演配置。 <a href="https://doi.org/10.1016/j.neunet.2025.107419">原文</a></figcaption>
</figure>

### 4.2 已发表结果：独立参照与错误先验要在同一案例交叉

Hong 等的实体模体每区用两支热电偶核查区域温度，文中平均绝对误差为 0.22–0.71 °C。分区误差试验另用 CT 衍生仿真。在固定模拟电压的外部热源场景里，分区平移从 0 增至 10 mm，六区域的平均绝对温差从 1.38 升至 1.80 °C。热源居中时，同样的位移下指标由 0.88 降至 0.63 °C。图 9 的预测和参考都在移动后的区域取均值，这会改变被评分的真值。对下一轮实体实验，应该把独立探针和评估区固定在实物坐标上。 [9](#ref-hong)

<figure class="literature-figure">
  <a href="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/hong2026-domain-shift-error.png' | relative_url }}"><img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/hong2026-domain-shift-error.png' | relative_url }}" width="1320" height="818" alt="图 2。CT 模拟中外部热源的六域平均温差随分区平移增大，居中热源的对应指标下降。" loading="lazy" decoding="async"></a>
  <figcaption><strong>图 2。CT 模拟中外部热源的六域平均温差随分区平移增大，居中热源的对应指标下降。</strong> 根据 Hong 等第 12 页图 9 对应实验的六个移动区域平均绝对温差重绘。横轴为分区平移，评分区域随之移动。 <a href="https://doi.org/10.1002/mp.70774">原文</a></figcaption>
</figure>

### 4.3 本文复核：KIT4 的激励秩与原始留出电压

使用 KIT4 v1 的 38 个 MAT 文件。每个文件的注流和电压阵列均为 16×79，测压模式阵列为 16×16，以 MATLAB 的 1 起算列号分组。两个划分均使用分别存储的原始电压记录，组间噪声仍可能相关。下表是三组先后并入后的净零注流秩，列数、预算和矩阵秩均由档案重新计算。 [6](#ref-kit4)

| 拟合组起点 | 拟合 | 加选参组 | 加验收组 |
| --- | ---: | ---: | ---: |
| 相邻，列 1–16 | 15 | 15 | 15 |
| 跳三，列 49–64 | 12 | 14 | 15 |
{: .literature-results }

两行的选参组为跳一（列 17–32），验收组为跳二（列 33–48）。每个组每例都有 256 个原始读数。完整读出与互易性成立时，第一行在拟合后已经覆盖 120 个理想对称响应坐标。第二行对应累计 114、119、120 个坐标，验收组至多新增一个理想坐标。这个坐标是否对错误先验足够敏感，仍需针对候选核对。

我们另做了一个纯电压基线。用相邻组的驱动矩阵 <span class="literature-math">I<sub>A</sub></span> 拟合目标组的驱动权重，权重只看电流模式。再用相邻组的电压矩阵 <span class="literature-math">V<sub>A</sub></span> 线性合成目标电压，与同一文件实测的目标 <span class="literature-math">V<sub>T</sub></span> 比较。<span class="literature-math">†</span> 表示 Moore–Penrose 伪逆，<span class="literature-math">F</span> 下标表示 Frobenius 范数。

<div class="literature-equation">
  <math display="block"><msub><mi>W</mi><mi>T</mi></msub><mo>=</mo><msubsup><mi>I</mi><mi>A</mi><mo>†</mo></msubsup><msub><mi>I</mi><mi>T</mi></msub><mo>,</mo><mspace width="0.7em"/><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>T</mi></msub><mo>=</mo><msub><mi>V</mi><mi>A</mi></msub><msub><mi>W</mi><mi>T</mi></msub></math>
  <math display="block"><msub><mi>E</mi><mi>T</mi></msub><mo>=</mo><mfrac><msub><mrow><mo>‖</mo><msub><mover accent="true"><mi>V</mi><mo>^</mo></mover><mi>T</mi></msub><mo>−</mo><msub><mi>V</mi><mi>T</mi></msub><mo>‖</mo></mrow><mi>F</mi></msub><msub><mrow><mo>‖</mo><msub><mi>V</mi><mi>T</mi></msub><mo>‖</mo></mrow><mi>F</mi></msub></mfrac></math>
</div>

跳一的病例级误差中位数为 **1.34%**（四分位区间 1.27%–1.56%），跳二为 **1.30%**（1.24%–1.56%）。这一复核衡量原始记录与线性重组的差别，使用全部 38 个档案案例作描述。误差可能包含采集及预处理偏差，不能直接把它定为错先验检出阈值。这一步没有生成电导率图，也没有对先验进行选取。 [公共输入数据](https://doi.org/10.5281/zenodo.1203914) · [复核脚本]({{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-voltage-audit.py' | relative_url }}) · [逐例数据 CSV]({{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-voltage-errors.csv' | relative_url }})

<figure class="literature-figure">
  <a href="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png' | relative_url }}"><img src="{{ '/assets/images/knowledge/eit/held-out-voltage-and-wrong-priors/kit4-held-out-voltage-error.png' | relative_url }}" width="1278" height="675" alt="图 3。以相邻注流电压预测跳一、跳二组，38 个 KIT4 案例的误差分布与中位数。" loading="lazy" decoding="async"></a>
  <figcaption><strong>图 3。以相邻注流电压预测跳一、跳二组，38 个 KIT4 案例的误差分布与中位数。</strong> 每个圆点代表一个档案案例。菱形为中位数，横线为第 25 至 75 百分位范围。数据来自本文复核。 <a href="https://doi.org/10.5281/zenodo.1203914">公开数据</a></figcaption>
</figure>

## 5. 不同文献的交叉验证
{: #cross-check }

**先验错误的后果与所用机制有关。** Kolehmainen 等模拟 Case 2 用相同电压比较 STV 无先验、正确拓扑和错误拓扑，相对电导率误差分别为 13.8%、3.3%、10.1%。错误拓扑仍可能小幅改善全局分数，同时把局部轮廓向辅助图像牵引。Wang 的实体例子改变的是材料对比度，持续嵌入使全局误差变大。这两项是不同场景下的互补证据，说明全局误差与局部先验伤害都要报告。 [2](#ref-pls) · [3](#ref-dpe)

**在同一档案上，两次分析都出现了电压与几何排序分歧。** 下面只对照 KIT4 的边界泡沫组（Set 6）。两篇报告各自的测量误差。Dice 反映重建与照片分割的几何重叠，在阻性、导电和背景三类上取平均。

| Set 6 方法 | Dice ↑ | 电压误差 ↓ |
| --- | ---: | ---: |
| Denker · GN-TV | 0.114 | 0.0004 |
| Denker · Deep D-bar | 0.408 | 0.0602 |
| Masiri · GN-TV | 0.1210 | 0.0003 |
| Masiri · Deep D-bar | 0.4332 | 0.0530 |
{: .literature-results }

两张表内部，GN-TV 的电压误差较低，照片 Dice 也较低。Denker 定义的是归一化平方残差。Masiri 表 8 的精确范数和留出条件在所核查的版本中未见说明，因此只比较各表内部排序。两项分析共享 KIT4 档案，逐例掩膜与电压列未建立一一对应。这是共享数据上的方向一致，证据强度以一次采集谱系计。 [7](#ref-denker) · [8](#ref-masiri)

**证据缺口落在同一个实体案例上。** Asfaw 与 Adler 的留出验证说明可以用电压诊断一种观测异常。Wang 直接干预错误内部先验，Hong 提供独立物理参照。对本文纳入的案例，仍需把错误内部先验、从选择中封存的真实电压和独立物性参照同时放进一个实验，才能判断选出的图像是否改善了目标物性。 [3](#ref-dpe) · [4](#ref-asfaw) · [9](#ref-hong)

## 6. 可能的突破与可检验的研究方案
{: #proposed-study }

**用候选分离度选激励，再用独立测量验收。** 从无外部图像先验、正确先验和受控错误先验得到候选，先在开发案例设定噪声、接触误差范围和筛选规则，再用拟合组得到的预测计算各候选在备选激励上的分离度。可优先选分离大、对接触和几何误差稳健的激励，对照相同数量的常规激励。对分离不足的情况保留「信息不足」结论。该设计的可证伪预测是，在相同测量预算内，面向候选差异的激励能提高对错先验的检出率，同时维持正确先验的保留率。

1. **固定模体与分组。** 同一对象成对比较无图像先验、正确先验和反转对比度先验，固定模型、求解器和数据预算。把原始注流分为拟合 A、选参 B 和终试 C。A 组生成候选，B 组只负责筛选并锁定最终返回场，C 的电压在锁定后才打开。分别改变错先验和接触扰动，检查两种因素是否能被选定的激励区分。
2. **固定终点。** 用重复测量估计电压波动，以同频独立物性测量验收固定区域的平均电导率。报告错先验误保留、正确先验误拒绝、信息不足比例、封存电压误差和固定区域物性误差。统计单位为独立模体或独立复采批次。
3. **检验物性改善。** 用 <span class="literature-math">L</span> 表示独立物性误差，<span class="literature-math">w</span> 表示错先验，<span class="literature-math">0</span> 表示无外部图像先验。令 s 表示加入观测筛选，b 表示同预算的基线。用 <span class="literature-math">Δ<sub>w</sub></span> 和 <span class="literature-math">Δ<sub>0</sub></span> 记录配对误差变化。 <span class="literature-math">Δ<sub>w</sub>&lt;0</span> 才说明错先验组的物性本身改善。<span class="literature-math">Δ<sub>w</sub>−Δ<sub>0</sub>&lt;0</span> 进一步检验收益是否针对错先验。两项同时报告。

<div class="literature-equation">
  <math display="block"><msub><mi>Δ</mi><mi>j</mi></msub><mo>=</mo><mi>L</mi><mo stretchy="false">(</mo><mi>j</mi><mo>,</mo><mi>s</mi><mo stretchy="false">)</mo><mo>−</mo><mi>L</mi><mo stretchy="false">(</mo><mi>j</mi><mo>,</mo><mi>b</mi><mo stretchy="false">)</mo><mo>,</mo><mspace width="0.5em"/><mi>j</mi><mo>∈</mo><mo>{</mo><mi>w</mi><mo>,</mo><mn>0</mn><mo>}</mo></math>
</div>

## 7. 结论
{: #conclusion }

留出电压的优势在于它直接检查冻结重建能否解释额外采集。它能否识别错误先验，取决于候选分离度、模型失配和数据链。KIT4 的复核给出了一个可重算的纯电压比较，也显示了留出记录数量与理想观测维数的差别。下一步最有区分力的实验，是在同一实体模体上同时改变内部先验、封存新电压，并独立测量目标电导率。

## 参考文献
{: #references }

1. <span id="ref-cem"></span> Somersalo E, Cheney M, Isaacson D. *Existence and uniqueness for electrode models for electric current computed tomography*. SIAM Journal on Applied Mathematics, 1992, 52(4), 1023–1040. [DOI](https://doi.org/10.1137/0152060)
2. <span id="ref-pls"></span> Kolehmainen V, Ehrhardt MJ, Arridge SR. *Incorporating structural prior information and sparsity into EIT using parallel level sets*. Inverse Problems and Imaging, 2019, 13(2), 285–307. 表 2，图 3。 [DOI](https://doi.org/10.3934/ipi.2019015)
3. <span id="ref-dpe"></span> Wang J, Deng J, Liu D. *Deep prior embedding method for Electrical Impedance Tomography*. Neural Networks, 2025, 188, 107419. 图 7。 [DOI](https://doi.org/10.1016/j.neunet.2025.107419)
4. <span id="ref-asfaw"></span> Asfaw Y, Adler A. *Automatic detection of detached and erroneous electrodes in electrical impedance tomography*. Physiological Measurement, 2005, 26(2), S175–S183. [DOI](https://doi.org/10.1088/0967-3334/26/2/017)
5. <span id="ref-harrach"></span> Harrach B. *Interpolation of missing electrode data in electrical impedance tomography*. Inverse Problems, 2015, 31(11), 115008. [DOI](https://doi.org/10.1088/0266-5611/31/11/115008)
6. <span id="ref-kit4"></span> Hauptmann A, Kolehmainen V, Mach NM, Savolainen T, Seppänen A, Siltanen S. *Open 2D Electrical Impedance Tomography data archive*. 2017. [数据说明](https://arxiv.org/abs/1704.01178) · [KIT4 v1 数据](https://doi.org/10.5281/zenodo.1203914)
7. <span id="ref-denker"></span> Denker A, Margotti F, Ning J, et al. *Deep learning based reconstruction methods for electrical impedance tomography*. Handbook of Numerical Analysis, 2025. 表 3，正式版式 (37)。 [DOI](https://doi.org/10.1016/bs.hna.2025.09.003)
8. <span id="ref-masiri"></span> Mohammadi Masiri V, Salimi Shahraki A, Abbasi M. *Cloud–edge collaborative intelligence for privacy-preserving electrical impedance tomography reconstruction with federated deep D-bar*. Journal of Cloud Computing, 2026. 表 8。 [DOI](https://doi.org/10.1186/s13677-026-01000-6)
9. <span id="ref-hong"></span> Hong J, Kim J, Lee B, et al. *Feasibility of prior-informed domain-based electrical impedance tomography for deep tissue thermometry: Phantom experiments and computed tomography-derived numerical simulations*. Medical Physics, 2026, 53(12), e70774. 表 2，图 5–7、9。 [DOI](https://doi.org/10.1002/mp.70774)
