# gstack-tutorial-2 — 用 2 个 AI 智能体构建开源端到端 EDA 系统

[![repo self-check](https://github.com/mikelix/gstack-tutorial-2/actions/workflows/selfcheck.yml/badge.svg)](https://github.com/mikelix/gstack-tutorial-2/actions/workflows/selfcheck.yml)
[![许可：CC BY 4.0 / Apache-2.0](https://img.shields.io/badge/licence-CC%20BY%204.0%20%2F%20Apache--2.0-blue.svg)](LICENSE.md)

> **这是什么**：一份动手教程。用 **gstack** 智能体工作流 + **两个领域 AI 智能体**，
> 构建、运行并验证一条真实的开源芯片流程 —— 基于 SkyWater SKY130 开放 PDK 的
> RTL → GDS，并用验证门链把产出锁到字节级哈希。
>
> **这不是什么**：不是 Cadence 级签核课程，也不是玩具。

English version: [`README.md`](README.md)

---

## 0. 为什么要有第二份教程

[gstack-tutorial-1](https://github.com/mikelix/gstack-tutorial-1) 用一行
`hello_world.py` 教 gstack Team Mode 的评审闭环。它在自己的定位上很出色，
但它**刻意不承载任何真实产物**。

本教程保留那套骨架，只改两件事：

| | Tutorial #1 | Tutorial #2 |
|---|---|---|
| 载体 | `hello_world.py` | 真实的 RTL→GDS EDA 系统 |
| 团队 | 5 个 gstack **评审**角色 | 5 个 gstack 角色 **× 2 个领域智能体** |
| 完成判据 | 评审意见合并 | **门链全 PASS + GDS SHA 一致** |
| 环境 | 无 | 可复现的开源 EDA + 开放 PDK |
| 价值叙事 | — | 一套独立估值约 125 万人民币的系统 |

一句话的差别：**#1 里智能体评审工作；#2 里智能体做工作，并被验证门卡住。**

### 第二个差别 —— 也是更要紧的那个

在 #1 里，5 个 gstack 角色**够用**，因为产物是玩具。在 #2 里**不够用**，因为产物是硅片。

> **gstack 角色是流程专家、领域通才。** 它们没有半导体工程专业知识，也不掌握
> 半导体设计流程的运作方式。它们会接受"LVS 通过"而不知道该检查可能循环论证；
> 会重排构建步骤而静默破坏字节级确定性；会建议放宽容差以让结果变绿。
>
> **两个领域智能体掌握的正是编排层缺的那一半** —— 半导体物理与流程语义。
> 所以这不是"5 + 2"，而是一套**双钥匙机制**：流程权限归 gstack，物理权限归
> 领域智能体，**冲突时物理优先**。

完整契约：[`docs/expertise_division.zh.md`](docs/expertise_division.zh.md)
（English [`docs/expertise_division.md`](docs/expertise_division.md)）——
RACI 表、三条否决规则、升级处置流程，以及可复制的**让渡条款**。

---

## 1. 三层模型

```
  gstack 编排层           /plan-ceo-review → /spec → /plan-eng-review
  （评审与决策审计）         → /qa-only → /ship
            │
            ├──────────────► 2 个领域智能体
            │                 • AI GDS-Architect（数字：RTL→GDS、DRC/LVS）
            │                 • 资深模拟 IC 设计架构师（模拟：sizing、仿真、版图）
            │
            └──────────────► 开源 EDA + 开放 PDK + 7 道验证门链
                              Magic · Netgen · Klayout · ngspice · Xschem
                              SKY130A · Microlane P&R
```

中间层没有一个是摆设：每个智能体都有**交接契约**，它产出的每件东西都会被门卡住。

---

## 2. 为什么用 SKY130 而不是商业 PDK

作者持有受 NDA 约束的 PDK（TSMC、UMC、GlobalFoundries、ams 0.35 µm、粤芯）。
**它们一个字节都不能出现在本仓库。**

1. NDA PDK 不能公开、不能转发、不能提交进仓库。
2. 夹带闭源 PDK 的"开源教程"不是开源 —— 是带 README 的泄密。
3. SKY130 是首个以开放许可发布的代工级 PDK，**DRC/LVS/RCX 规则同样开放**，
   所以本教程的每一道门，读者都能重跑、审计、fork。
4. 没有损失：方法与工艺无关 —— 门链结构、确定性契约、智能体工作流可平移到任何
   PDK，包括那些闭源的。

> 这一节本身就是教学点：它用作者真实做过的一个决定，教会读者"什么可以开源"。

---

## 3. 完成定义（硬指标，不是愿景）

| # | 判据 | 证据 |
|---|---|---|
| 1 | 门 5 —— Magic DRC | PASS，0 violation |
| 2 | 门 6 —— Magic 提取 | PASS |
| 3 | 门 7A —— 结构级 LVS | PASS |
| 4 | 门 7B-1R2 —— Netgen 层次化 LVS | PASS —— `Circuits match uniquely.` |
| 5 | **确定性** | GDS SHA-256 跨次运行可复现 |
| 6 | **双语文档** | 英文 + 简体中文手册 |

任何一条不满足，教程就没完成。没有"基本完成"。

---

## 4. 本教程教的两条纪律

**（一）锁住产物。** 锁定工具版本 + `PYTHONHASHSEED=0` + 固定随机种子 +
冻结 GDS 时间戳 ⇒ 字节级一致的输出。门链是裁判。

**（二）不只查状态，要查数字。** 门可以全 PASS 而物理仍然是错的。教程附两个实例：

| 案例 | 预测 | 实测 |
|---|---|---|
| 四轴悬停功率（GDA） | 127.8 W | 127.4 W（0.29%） |
| CTC 捕获临界毛细数 | Ca\* = 0.043 | 0.04 ± 0.006 |

两者都经得起第一性原理交叉核验 —— 并且都**主动写明自己可被证伪的前提**
（例如桨叶效率因子独立取得，**未**用本次飞行标定）。

---

## 锁定的工具链版本（不要漂移）

| 工具 | 版本 | 提交 |
|---|---|---|
| Magic | **8.3.681** | `4432d7e` |
| Netgen | **1.5.323** | `bb8a610` |
| open_pdks / SKY130A | **1.0.572** | `54435919` |
| Microlane | — | `87079e7f6` |

版本一变，参考 SHA 即失效。要有意识地重新定基线并公布新基线；
**绝不要**通过放宽检查来"修掉"哈希不一致。

---

## 5. 仓库结构

| 路径 | 用途 |
|---|---|
| **[`TUTORIAL.md`](TUTORIAL.md)**（英文）· **[`TUTORIAL.zh.md`](TUTORIAL.zh.md)**（中文） | **逐步教程（从这里开始）** |
| [`START_HERE.md`](START_HERE.md) | 个人 / 团队两种入口 |
| [`PLAN.md`](PLAN.md) | 范围、阶段、团队拓扑、完成定义 |
| [`COLLABORATOR_GUIDE.md`](COLLABORATOR_GUIDE.md) | fork 模型、频道、评审节奏 |
| [`docs/gate_chain.md`](docs/gate_chain.md) | 逐门参考 |
| [`docs/expertise_division.zh.md`](docs/expertise_division.zh.md) | **为什么 gstack 无权决定领域问题** —— 权限契约、否决规则、让渡条款 |
| [`starter/`](starter/README.md) | **可直接运行的骨架** —— 门脚本、`db_export.py`、配置模板 |
| [`reviews/`](reviews/README.md) | **五份 gstack 评审记录范例**（CEO → spec → 工程 → QA → 发布） |
| `.github/ISSUE_TEMPLATE/weekly_progress_report.md` | 周报模板 |
| `.github/workflows/selfcheck.yml` | CI：必需文件、版本一致性、循环性守卫 |

### 交付物（三种格式）

| 格式 | 英文 | 简体中文 |
|---|---|---|
| Markdown | [`TUTORIAL.md`](TUTORIAL.md) | [`TUTORIAL.zh.md`](TUTORIAL.zh.md) |
| MS Word | [`dist/gstack-tutorial-2_EN.docx`](dist/gstack-tutorial-2_EN.docx) | [`dist/gstack-tutorial-2_ZH.docx`](dist/gstack-tutorial-2_ZH.docx) |
| PowerPoint（35 页） | [`dist/gstack-tutorial-2_EN.pptx`](dist/gstack-tutorial-2_EN.pptx) | [`dist/gstack-tutorial-2_ZH.pptx`](dist/gstack-tutorial-2_ZH.pptx) |

Markdown 是唯一事实来源，Word 与 PowerPoint 由它生成（见 `_build/`）。
改 Markdown 后重新生成 —— 不要手改二进制文件。

---

## 6. 致谢

| 项目 | 角色 |
|---|---|
| [google/skywater-pdk](https://github.com/google/skywater-pdk) | 开放许可的代工级 PDK |
| [open_pdks](https://github.com/RTimothyEdwards/open_pdks) | PDK 构建与安装框架 |
| [Magic](https://github.com/RTimothyEdwards/magic) · [Netgen](https://github.com/RTimothyEdwards/netgen) | DRC / 提取 / LVS |
| [Microlane](https://github.com/htfab/microlane) | 轻量开源布局布线 |
| [Tiny Tapeout](https://tinytapeout.com)（Matt Venn、Uri Shaked） | 低成本流片通道 |
| [Zero to ASIC Course](https://zerotoasiccourse.com) | 教同一套工具，但不用 AI 智能体 |
| [SiliWiz](https://app.siliwiz.com) | 浏览器里的硅直觉（Apache-2.0） |

**定位**：Zero to ASIC 教人用开源工具做芯片；本教程教用 **gstack + 两个领域智能体**
跑同一条流程，并用门链与哈希锁死产出。相邻层，不是竞争关系。

---

## 7. 许可

文字采用 **CC BY 4.0**，代码采用 **Apache-2.0**（见 [`LICENSE.md`](LICENSE.md)）。
本教程引用的商业产品 `e2e-ic-system` **不包含在内**，仍受其独立许可约束。
