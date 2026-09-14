# -*- coding: utf-8 -*-
"""Chinese deck: gstack 教程 No. 2"""
import os
import sys
sys.path.insert(0, r'D:\ipason\EDA\gstack-tutorial-2\_build')
from deck import *  # noqa
from deck import NAVY, NAVY2, ACCENT, ACCENT2, WHITE, LIGHT, GREY, DARK

DIAGRAM = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', 'docs', 'two-key-authority.png')

FOOT = "gstack 教程 No. 2  ·  在 WorkBuddy 上构建 AI 智能体驱动的端到端 EDA 系统"


def build_zh(prs):
    n = [0]

    def num(s, dark=False):
        n[0] += 1
        footer(s, FOOT, dark)
        pagenum(s, n[0], dark)

    # 1
    num(slide_title(
        prs,
        "gstack 教程 No. 2",
        "在 WorkBuddy 上构建 AI 智能体驱动的\n端到端 EDA 系统",
        ["面向研究生与青年工程师的逐步实操教程",
         "基于 SkyWater SKY130 开放 PDK 的 RTL → GDS，用四道门链与字节级哈希验证"],
        "版本 1.0 · 2026 年 9 月 · 文字 CC BY 4.0 · 代码 Apache-2.0"), dark=True)

    # 2
    num(slide_bullets(
        prs,
        "你要构建什么 —— 以及必须证明什么",
        ["在 SkyWater SKY130 开放 PDK 上构建一条开源的 RTL → GDS 流程",
         "用 5 个 gstack 编排角色 + 2 个领域 AI 智能体驱动它",
         "用四道验证门与可复现的 SHA-256 证明它成立",
         "交付双语文档，以及一份不软化的局限陈述"],
        note="你不需要商业 EDA 授权、NDA，也不需要流片预算。"))

    # 3
    num(slide_table(
        prs,
        "为什么要有第二份教程？",
        ["", "教程 #1", "教程 #2"],
        [["载体", "hello_world.py", "真实的 RT→GDS EDA 系统"],
         ["团队", "5 个 gstack 评审角色", "5 个 gstack 角色 × 2 个领域智能体"],
         ["完成判据", "评审意见合并", "门链全 PASS + GDS SHA 一致"],
         ["环境", "无", "可复现的开源 EDA + 开放 PDK"],
         ["价值叙事", "—", "一套估值约 125 万元人民币的系统"]],
        col_widths=[1.4, 2.8, 4.2], first_bold=True,
        note="教程 #1 刻意不承载真实产物。在你真正需要产物之前，那都是正确的选择。"))

    # 4
    num(slide_layers(
        prs,
        "三层模型",
        [("第 1 层\ngstack 编排",
          ["/plan-ceo-review → /spec → /plan-eng-review → /qa-only → /ship",
           "每个角色都有停止点，于是决策被审计，而不是被静默吞掉。"], NAVY),
         ("第 2 层\n两个领域智能体",
          ["AI GDS-Architect —— 数字：RTL→GDS、DRC、LVS、确定性",
           "资深模拟 IC 设计架构师 —— 模拟：sizing、仿真、版图意图",
           "各有交接契约：收到什么、产出什么、由谁判定。"], ACCENT),
         ("第 3 层\n开源 EDA + PDK + 门链",
          ["Magic 8.3.681 · Netgen 1.5.323 · KLayout · ngspice · Xschem",
           "SKY130A（open_pdks 1.0.572）· Microlane 布局布线",
           "门 5 DRC → 门 6 提取 → 门 7A LVS → 门 7B-1R2 LVS"], NAVY2)],
        note="一个产出的文件没有任何门去检验的智能体，是在写作业，不是在做工程。"))

    # 5
    num(slide_table(
        prs,
        "五个 gstack 角色",
        ["命令", "角色", "职责", "停止条件"],
        [["/plan-ceo-review", "AI CEO", "挑战范围、定位、野心", "范围站得住"],
         ["/spec", "AI PM", "拆解成可派发的任务项", "待办清单具体可执行"],
         ["/plan-eng-review", "AI 工程师", "锁定架构、数据流、执行顺序", "计划可施工"],
         ["/qa-only", "AI QC", "测试并报告 —— 但不修改", "报告已归档"],
         ["/ship", "AI DevOps", "定版、打包、写文档、发布", "发布已打标签"]],
        col_widths=[1.8, 1.2, 3.4, 1.9], first_bold=True,
        note="价值不在于 AI 有多聪明，而在于每个角色都有停止点。"))

    # 6
    num(slide_table(
        prs,
        "两个领域智能体",
        ["智能体", "负责", "产出", "由谁判定"],
        [["AI GDS-Architect",
          "数字后端：布局布线、DRC、提取、LVS、流出版图",
          "GDS、提取网表、门日志",
          "门 5、6、7A、7B-1R2"],
         ["资深模拟 IC 设计架构师",
          "模拟前端：拓扑、sizing、仿真、版图意图",
          "已 sizing 的电路图、仿真结果、版图约束",
          "ngspice 仿真、DRC（7B-2 在路线图上）"]],
        col_widths=[1.9, 3.2, 2.5, 1.9], first_bold=True, size=11.5,
        note="数字智能体走主线，模拟智能体在第 9 部分接入。"))

    # 6b 能力缺口
    num(slide_table(
        prs,
        "能力缺口 —— 为什么 5 个角色不够",
        ["gstack 角色会很自然地……", "……但它不知道"],
        [["接受“LVS 通过”", "朴素的 LVS 可能是循环论证，什么也证明不了"],
         ["接受“DRC 干净”", "实际跑了哪几类规则、又豁免了什么"],
         ["为了整洁重排构建顺序", "流式写出顺序会改变 GDS 字节流，破坏确定性"],
         ["建议“放宽检查就能变绿”", "放宽签核检查是唯一不可饶恕的动作"],
         ["把现有产物直接打包", "没有可复现哈希的 GDS 不叫发布版"],
         ["起草对外文案", "一个写错的物理数字会毁掉全部可信度"]],
        col_widths=[5.6, 5.6], first_bold=True, size=11.5,
        kicker="与教程 #1 的第二个、也是更要紧的差别",
        note="gstack 角色天生是流程专家、领域通才 —— 正因如此它们才是好的编排者。"))

    # 6c 双钥匙
    num(slide_quote(
        prs,
        "流程权限归 gstack。\n物理权限归领域智能体。\n冲突时物理优先。",
        "不是“5 + 2”，而是一套双钥匙机制 —— 5 个决定流程，2 个决定物理。",
        "双钥匙机制"))

    # 6d 权限契约
    num(slide_table(
        prs,
        "权限契约 —— 谁有权决定什么",
        ["决策事项", "gstack", "领域智能体", "人类"],
        [["范围、阶段划分、任务拆解", "决定", "被咨询", "批准"],
         ["选哪个 PDK / 标准单元库", "无权", "决定", "批准"],
         ["什么算“门通过”", "执行", "决定", "—"],
         ["DRC 违例能否豁免", "无权", "决定", "签字"],
         ["LVS 失配如何解读", "报告", "决定", "—"],
         ["发布内容与版本号", "决定", "被咨询", "批准"],
         ["任何含物理数字的表述", "无权", "决定", "—"]],
        col_widths=[4.4, 2.3, 2.7, 1.8], first_bold=True, size=11.5,
        note="先读“无权”那几行。那才是整张表的重点。"))

    # 6d2 双钥匙权限图
    num(slide_image(
        prs,
        "双钥匙权限模型 —— 一图流",
        DIAGRAM,
        kicker="第 0 部分 · 谁有权决定什么",
        note="gstack 持流程权，两个领域智能体持物理权；二者共同喂给门链，冲突时物理权获胜。"))

    # 6e 三条否决规则
    num(slide_bullets(
        prs,
        "三条否决规则",
        ["领域否决优先于流程便利 —— 不安全的步骤就不做，计划怎么写都不算",
         "门的结果不是事实，直到领域智能体读过日志 —— 而不只是状态行",
         "绝不为让构建通过而放宽检查 —— 领域智能体必须书面说明错的到底是哪一方"],
        kicker="权限契约",
        note="“PASS” 只是一个字符串。日志才是证据。"))

    # 6f 让渡条款
    num(slide_code(
        prs,
        "让渡条款 —— 粘贴进每一个 gstack 提示词",
        ["需征询领域智能体。在你敲定任何涉及 DRC、LVS、提取、确定性或",
         "PDK 规则的表述之前，先将该具体论断交给领域智能体（数字方向",
         "交给 AI GDS-Architect，模拟方向交给资深模拟 IC 设计架构师），",
         "并逐字引用其答复。",
         "",
         "若领域智能体与你的结论冲突，以领域智能体为准。不要自行裁决 ——",
         "把两方陈述并列提交给人类裁决。"],
        lang_note="成本只有一个段落，却是“听起来对”与“确实对”的分界线。",
        note="智能体凭什么可信：非循环 LVS、确定性 GDS，以及从李雅普诺夫指数（2002）到认证诊断芯片（2023）的 22 年证据链。"))

    # 7
    num(slide_bullets(
        prs,
        "为什么用 SKY130，而不是商业 PDK",
        ["NDA PDK 不能公开、不能转发、不能提交进仓库",
         "夹带闭源 PDK 的“开源教程”不是开源 —— 是带 README 的泄密",
         "SKY130 是首个以开放许可发布的代工级 PDK，DRC/LVS/RCX 规则同样开放",
         "没有损失：方法与工艺无关，可平移到任何 PDK"],
        note="这一节本身就是教学点：它用作者真实做过的一个决定，教会读者什么可以开源。"))

    # 8
    num(slide_table(
        prs,
        "课程地图",
        ["部分", "做什么", "时间"],
        [["0", "心智模型：三层、五角色、两智能体", "30 分钟"],
         ["1", "安装 WorkBuddy、gstack 与两个领域智能体", "45 分钟"],
         ["2", "安装开源 EDA 工具链（三条路径）", "30 分钟 – 4 小时"],
         ["3", "阶段 1 —— AI CEO 定范围", "45 分钟"],
         ["4", "阶段 2 —— AI PM 拆解工作", "45 分钟"],
         ["5", "阶段 3 —— AI 工程师跑通 RTL → GDS", "3–5 小时"],
         ["6", "阶段 4 —— AI QC 验证并证明确定性", "2–3 小时"],
         ["7", "阶段 5 —— AI DevOps 发布", "1–2 小时"],
         ["8", "本教程真正教的两条纪律", "30 分钟"],
         ["9", "接入模拟智能体", "2–4 小时"],
         ["10–12", "故障排查、考核、接下来做什么", "自定进度"]],
        col_widths=[0.9, 6.6, 1.6], first_bold=True, size=12,
        note="首次完整走完约 10–14 小时。每个部分结尾都有必须通过才往下走的检查点。"))

    # 9
    num(slide_checklist(
        prs,
        "第 0 部分 —— 检查点",
        ["你能说出 5 条 gstack 命令及各自的停止点",
         "你能用一句话讲清教程 #1 与 #2 的差别",
         "你能解释为什么 NDA PDK 不能出现在本仓库",
         "你能举出一项 gstack 角色无权决定的事项，并说出该由谁决定",
         "让渡条款已复制到随手可粘贴的地方"],
        note="五条全绿才往下走。可迁移的是心智模型，不是命令。"))

    # 10
    num(slide_steps(
        prs,
        "第 1 部分 —— 安装宿主与两个智能体",
        ["下载腾讯 WorkBuddy，安装、登录，用最简提示验证技能系统在线",
         "安装 gstack 技能套件；确认 @skill:gstack 能正确路由",
         "创建 ~/.workbuddy/skills/e2e-ic-system/agents/ 目录",
         "保存 ai_gds_architect.md 与 analog_ic_architect.md（最小简介见 1.3 节）",
         "重启 WorkBuddy 并确认：「列出你能看到的智能体」"],
        note="智能体规格与宿主无关 —— Claude Code 与 OpenAI Codex 用法相同。"))

    # 11
    num(slide_table(
        prs,
        "第 2 部分 —— 三条安装路径",
        ["路径", "平台", "时间", "状态"],
        [["A —— 一键安装器（install_eda.bat）", "Windows 11", "1–3 小时（需编译）", "beta"],
         ["B —— 手动逐步安装", "任意", "2–4 小时", "文档完整"],
         ["C —— TinyTapeout 虚拟机镜像（推荐）", "Win / macOS / Linux", "约 30 分钟", "上游维护"]],
        col_widths=[4.2, 2.2, 2.0, 2.2], first_bold=True, size=11.5,
        note="从未装过开源 EDA 工具链，就走选项 C。不要把第一天耗在编译上。"))

    # 12
    num(slide_table(
        prs,
        "锁定版本 —— 不要漂移",
        ["组件", "版本", "Commit", "来源"],
        [["Magic", "8.3.681", "4432d7e", "RTimothyEdwards/magic"],
         ["Netgen", "1.5.323", "bb8a610", "RTimothyEdwards/netgen"],
         ["open_pdks / SKY130A", "1.0.572", "54435919", "RTimothyEdwards/open_pdks"],
         ["Microlane", "—", "87079e7f6", "htfab/microlane"]],
        col_widths=[2.6, 1.7, 1.7, 4.3], first_bold=True,
        note="版本漂移是 SHA 莫名不一致的头号原因。"))

    # 13
    num(slide_code(
        prs,
        "先验证，再往下走",
        ["magic   -dnull -noconsole --version",
         "netgen  -batch -nogui",
         "cat $PDK_ROOT/sky130A/.config/nodeinfo.json",
         "ls $PDK_ROOT/sky130A/libs.tech",
         "",
         "# 预期：",
         "#   node sky130A · 130 nm · open_pdks 1.0.572（54435919）",
         "#   magic 8.3.681（4432d7e）· 11 个标准单元库",
         "#   sky130_fd_sc_hd：446 个单元"],
        lang_note="四条都有响应，就可以进入阶段 1。",
        note="开放 PDK 自带 DRC、LVS 与 RCX 规则档 —— PEX 的缺口在我们自己的流程侧，不在 PDK。"))

    # 14
    num(slide_bullets(
        prs,
        "阶段 1 —— AI CEO 定范围",
        ["执行 /plan-ceo-review，粘贴你的范围陈述",
         "明确追问：时间不够先砍哪一块？我哪条主张最弱？",
         "一份好的评审给你四样东西 —— 风险排序、砍项清单、一条挑战、一个未决问题",
         "把结论写进 reviews/01-ceo-review.md"],
        kicker="阶段 1 · /plan-ceo-review · 45 分钟",
        note="如果评审没有提出任何你目前答不上来的问题，说明这份评审太浅。"))

    # 15
    num(slide_table(
        prs,
        "阶段 2 —— 工作拆解",
        ["编号", "任务项", "责任方", "由谁判定"],
        [["W1", "工具链安装 + VERSIONS.lock", "DevOps", "检查点 2"],
         ["W2", "智能体安装 + 交接契约", "DevOps", "检查点 1"],
         ["W3", "config.env + 隔离启动器", "工程师", "启动器能跑"],
         ["W4", "布局布线至 GDS", "AI GDS-Architect", "门 5、6"],
         ["W5", "非循环参考源导出", "AI GDS-Architect", "产物非 GDS 派生"],
         ["W6", "LVS 对（7A、7B-1R2）", "AI GDS-Architect", "门 7A、7B-1R2"],
         ["W7", "确定性证明（重跑比对 SHA）", "QC", "SHA 一致"],
         ["W8", "模拟 sizing + 仿真（选修轨）", "资深模拟 IC 设计架构师", "ngspice 仿真"],
         ["W9", "双语文档 + 发布包", "DevOps", "完成定义"]],
        col_widths=[0.8, 4.4, 2.6, 2.7], first_bold=True, size=11.5,
        note="每个任务项都要点名判定它的门。没有门，就不算完成。"))

    # 16
    num(slide_bullets(
        prs,
        "阶段 3 —— AI 工程师跑通 RTL → GDS",
        ["先跑 /plan-eng-review：锁定数据流、产物命名、每道门的位置",
         "问出新人从不问的问题：门失败时运行目录怎么处理？",
         "派发 AI GDS-Architect 时，必须包含四条强制报告项",
         "使用隔离启动器 —— Windows 上绝不要用裸 shell"],
        kicker="阶段 3 · /plan-eng-review · 3–5 小时",
        note="四条强制报告项：产物及路径 · 门状态 · GDS 的 sha256 · 没有检查什么。"))

    # 17
    num(slide_flow(
        prs,
        "非循环规则 —— 本教程的智识核心",
        [(0.62, 2.20, 2.6, 0.95, "布局布线数据库\n（活的）", NAVY, True),
         (4.05, 1.75, 3.3, 0.72, "db_source_export.py\n（流出之前）", ACCENT, True),
         (4.05, 2.90, 3.3, 0.72, "GDS → Magic 提取", NAVY2, True),
         (8.20, 1.75, 3.3, 0.72, "参考源", ACCENT, False),
         (8.20, 2.90, 3.3, 0.72, "版图网表", NAVY2, False),
         (4.05, 4.15, 7.45, 0.80, "Netgen 层次化 LVS  →  门 7B-1R2", NAVY, True),
         (0.62, 5.30, 12.1, 0.62,
          "GDS 网表自比永远通过；同一起源的两条独立派生，才有诊断力。",
          LIGHT, False)],
        note="去耦电容的电源/地必须取自权威 PDK CDL/SPICE，而不是版图。"))

    # 18
    num(slide_table(
        prs,
        "四道门",
        ["门", "检查什么", "工具", "通过判据"],
        [["5 —— DRC", "几何是否违反代工规则", "Magic 8.3.681", "0 violation（豁免须列出）"],
         ["6 —— 提取", "版图 → 网表", "Magic 8.3.681", "完成；警告逐一枚举"],
         ["7A —— 结构级 LVS", "布局布线网表 vs 门级网表", "Microlane 比较器", "结构匹配"],
         ["7B-1R2 —— 层次化 LVS", "提取网表 vs P&R 数据库派生源", "Netgen 1.5.323", "Circuits match uniquely."]],
        col_widths=[2.2, 3.3, 2.2, 3.4], first_bold=True, size=11.5,
        note="没有产物的门，等于没有跑。"))

    # 18b
    num(slide_table(
        prs,
        "退出码契约 —— VOID 有独立码",
        ["码", "含义", "你该做什么"],
        [["0", "所有门 PASS", "记录 SHA，继续"],
         ["1", "某门 FAILED", "冻结运行目录，读日志，修根因"],
         ["2", "某门返回 VOID", "检查什么都没证明 —— 重新派生参考源再跑"],
         ["3", "环境错误", "配置错、工具缺失，或复用了 RUN_DIR"]],
        col_widths=[0.9, 4.0, 6.3], first_bold=True, size=12,
        note="若 VOID 与 PASS 共用一个码，扫一眼的人、或只断言“非零即错”的 CI，就可能把它当成通过。"))

    # 19
    num(slide_bullets(
        prs,
        "阶段 4 —— AI QC 验证，并证明确定性",
        ["组织纪律：跑门的人不能认证自己的门",
         "跑 /qa-only —— 它只报告，不改",
         "在干净的 shell 里完整跑两遍，比对 GDS 的 sha256",
         "全部记入 VERSIONS.lock；发布两个基准（Windows 链、虚拟机链）"],
        kicker="阶段 4 · /qa-only · 2–3 小时",
        note="不要用放松检查去“修好”不一致 —— 去查原因。"))

    # 20
    num(slide_two_col(
        prs,
        "阶段 5 —— AI DevOps 发布",
        "发布里必须有什么",
        ["VERSIONS.lock —— 可复现性",
         "四道门的日志",
         "GDS + 参考 SHA",
         "README（英）+ README（中）",
         "已知局限章节",
         "许可：文字 CC BY 4.0，代码 Apache-2.0"],
        "四文件规则",
        ["一个概念变更 = 4 个文件 × 4 次校验",
         "门脚本 · 英文文档 · 中文文档 · 评审记录",
         "每一项都要复核",
         "在开头就为它排预算",
         "不要在最后一天才发现"],
        kicker="阶段 5 · /ship · 1–2 小时",
        note="从教程 #1 原样搬过来，因为它仍然成立。"))

    # 21
    num(slide_bullets(
        prs,
        "纪律一 —— 锁住产物",
        ["锁定工具版本 + PYTHONHASHSEED=0 + 固定随机种子 + 冻结 GDS 时间戳",
         "⇒ 字节级一致的输出 ⇒ 一个你可以公开发布的哈希",
         "AI 智能体几分钟就能产出“看起来对”的东西",
         "在“看起来对”与“工程”之间，唯一的屏障是一个无法被辩倒的裁判"],
        kicker="本教程真正教的两条纪律",
        note="哈希就是这样的裁判。"))

    # 22
    num(slide_table(
        prs,
        "纪律二 —— 不只查状态，要查数字",
        ["案例", "预测", "实测", "误差"],
        [["四轴悬停功率（GDA）", "127.8 W", "127.4 W", "0.29%"],
         ["CTC 捕获临界毛细数 Ca*", "0.043", "0.04 ± 0.006", "落在实验带内"]],
        col_widths=[4.6, 2.0, 2.4, 2.3], first_bold=True, size=12.5,
        note="两者都经得起第一性原理交叉核验 —— 并且都主动写明自己可被证伪的前提。"))

    # 23
    num(slide_quote(
        prs,
        "「FM = 0.39，独立取自桨叶数据 —— 未用本次飞行标定。」",
        "主动交代“在哪个前提下我的数字会错”，正是把主张变成证据的那个动作。",
        "最关键的一句话"))

    # 24
    num(slide_bullets(
        prs,
        "第 9 部分 —— 接入模拟智能体",
        ["资深模拟 IC 设计架构师负责：电路图、sizing、仿真、工艺角、版图意图",
         "工具链：Xschem → ngspice → Magic",
         "始终要求它点名最可能出错的那一个假设",
         "诚实状态：它的门尚未实现 —— 由仿真与人工评审判定"],
        kicker="第 9 部分 · 2–4 小时",
        note="从一个李雅普诺夫指数到一台获证诊断设备，走了 22 年。领域在变，纪律没变。"))

    # 24b 模拟工作流
    num(slide_table(
        prs,
        "模拟智能体执行的工作流",
        ["阶段组", "序号", "回答的问题"],
        [["指标与物理", "1–3", "传感器建模、噪声 / 动态范围预算、PDK 器件数据"],
         ["架构", "4–6", "拓扑对比、g_m/I_D 初步 sizing、手工计算"],
         ["标称与行为级", "7–9", "标称 SPICE、噪声贡献、行为级仿真"],
         ["统计", "10–12", "PVT、蒙特卡洛 / 失配、设计中心化"],
         ["版图", "13–15", "floorplan、关键器件、渐进式 PEX"],
         ["后版图", "16–18", "噪声 / 稳定性 / PVT、高良率分析、可靠性 / EMIR"],
         ["硅片", "19–20", "AMS 验证、流片、表征、模型相关性"]],
        kicker="第 9 部分 · 给研究生",
        note="先学顺序再学工具 —— 顺序本身就是 expertise。完整 20 行表见 TUTORIAL.zh.md §9.5。"))

    # 24c 方法论
    num(slide_code(
        prs,
        "方法论，一行说完",
        "Specs → Physics → Architecture → Optimization → Statistics → Layout → Silicon\n\n不是：  画电路图 → SPICE → 画版图",
        kicker="第 9 部分 · 核心哲学",
        note="每个箭头都是一扇门：说出是什么产物穿过了它，否则把该阶段记为 VOID —— 没有可对照产物的阶段没有通过，它只是跑过。"))

    # 24d AI 四层级
    num(slide_table(
        prs,
        "AI 该待在哪 —— 四个层级",
        ["层级", "AI 做什么", "由谁验证", "2026 年现状"],
        [["1 工程助手", "推导公式、写脚本、生成测试台、分析日志、画 trade-off", "工程师逐条读它产出的一切", "今天就非常好用"],
         ["2 设计空间优化器", "在你设的约束内选 W、L、I_D、C、R", "仿真器 —— 唯一的裁判", "约束设得对就非常好用"],
         ["3 版图助手", "布局、布线、约束捕获、寄生优化", "DRC / LVS 门 + 版图感知检查", "进展快 —— Synopsys：AI 模拟版图流程，DRC 干净，迭代更少"],
         ["4 自主智能体", "端到端编排 EDA 任务", "基于物理的引擎，持续验证", "涌现中 —— Siemens：“自验证”智能体；LLM 永远不单独裁定"]],
        kicker="第 9 部分 · AI 的正确角色",
        note="本教程的双钥匙契约就是用开源工具搭出的第 4 层：LLM 永远不裁定正确性 —— 物理引擎裁定。"))

    # 25
    num(slide_table(
        prs,
        "故障排查 —— 高频六项",
        ["症状", "可能原因", "处置"],
        [["magic: command not found", "不在 PATH / Cygwin 未隔离启动", "用启动器；检查 config.env"],
         ["SHA 两次运行不一致", "版本漂移、时间戳未冻结", "复核 VERSIONS.lock；PYTHONHASHSEED=0"],
         ["虚拟机上 SHA 不同", "PDK 构建与工具修订不同", "预期结果 —— 发布第二个基准"],
         ["Netgen 报 setup 文件错", "在 source 脚本里用了 6 参数形式", "改用 4 参数 Tcl 形式"],
         ["路径被破坏", "MSYS 路径转换", "env -i + MSYS2_ARG_CONV_EXCL='*'"],
         ["LVS 通过得太轻松", "循环比对（GDS 比 GDS）", "参考源必须来自布局布线数据库"]],
        col_widths=[3.4, 4.1, 4.6], first_bold=True, size=11))

    # 26
    num(slide_table(
        prs,
        "考核 —— 评分标准",
        ["判据", "权重"],
        [["四道门均 PASS 且带产物", "30%"],
         ["SHA 可复现且已记录", "20%"],
         ["局限陈述诚实且具体", "20%"],
         ["演示了纪律二 —— 某数字手工重算", "20%"],
         ["双语输出或文档清晰", "10%"]],
        col_widths=[8.5, 2.0], first_bold=True, size=13,
        note="实验题：复现 · 故意破坏 · 循环 LVS · 物理 vs 状态 · 智能体问责。"))

    # 27
    num(slide_bullets(
        prs,
        "接下来",
        ["PEX / RCX 与门 7B-2 —— 规则档已随 PDK 提供",
         "用 ngspice 做后仿真；经 OpenLane/OpenSTA 做完整 STA（需 Docker）",
         "经 TinyTapeout shuttle 流片，100 美元起",
         "给模拟智能体装上真正的门链 —— 工作量大，价值高"],
        note="致谢：google/skywater-pdk · open_pdks · Magic · Netgen · Microlane · Tiny Tapeout · Zero to ASIC · SiliWiz"))

    # 27b
    num(slide_two_col(
        prs,
        "仓库里附带什么",
        "可运行骨架 —— starter/",
        ["run_all.sh 串起四道门 + 循环性守卫 + 指纹",
         "run_drc.tcl · run_extract.tcl · run_lvs.tcl",
         "db_export.py —— 流片前参考源导出",
         "config.env.example · versions.lock.template · designs/"],
        "审计轨迹 —— reviews/",
        ["01 CEO —— 范围、砍项清单、问题上抛而非硬答",
         "02 spec —— W1–W9、关键路径、三条上抛",
         "03 工程 —— 循环 LVS 被判 VOID 后修复",
         "04 QA —— 附八行“未被检查”表",
         "05 发布 —— 清单、双语一致、许可、四文件审计"],
        note="CI（.github/workflows/selfcheck.yml）：版本锁跨文档漂移、或循环性守卫消失，即失败。"))

    # 28
    num(slide_quote(
        prs,
        "#1 里智能体评审工作。\n#2 里智能体做工作 ——\n并被验证门卡住。",
        "四道门全通过、SHA 可复现，才算学完。",
        "一句话的差别"), dark=True)


if __name__ == '__main__':
    build(r'D:\ipason\EDA\gstack-tutorial-2\dist\gstack-tutorial-2_ZH.pptx', build_zh)
