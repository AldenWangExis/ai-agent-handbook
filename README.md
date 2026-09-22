<div align="right">中文 | <a href="./README_EN.md">English</a></div>

# AI Agent 核心技术白皮书

<div align="center">
  <p><strong>智以致用：从造出智能，到用好智能</strong></p>
  <p>面向企业级 Agent 构建场景，覆盖架构、构建、运行、治理、调优与实践的全生命周期指南</p>
</div>

---

## 1. 白皮书架构与写作背景

当模型从“生成内容”走向“理解目标、调用工具、操作环境并持续完成任务”，企业面对的核心问题也从“如何接入大模型”转向“如何把 Agent 变成可靠、可控、可规模化的生产力”。模型能力仍然是智能的源头，但一个能够进入真实业务流程的 Agent，还需要由 Harness、Runtime、状态存储、工具与协议、网关、安全、可观测、评估和持续优化共同支撑。

本白皮书以“智以致用”为核心命题：把可以规模化生产的认知能力，转化为能够可靠交付的任务结果。它不绑定单一模型、框架或厂商，而是尝试建立一套自洽的概念体系、架构方法与工程边界，帮助团队在快速变化的技术环境中形成可迁移的判断。

### 为什么写这本白皮书

[《2026 Agent 开发者调研报告》](./2026-agent-survey-report.md)收集了 1906 份有效问卷，受访者覆盖企业技术决策者、架构师、一线工程师与产品经理。调研反映出一个清晰趋势：企业对 Agent 的投入已形成共识，但从开发验证走向生产运行仍存在显著鸿沟。

- 已开发完成或正在开发 Agent 的受访企业合计达到 46%，真正部署到生产环节的只有 18%。
- 单 Agent、多 Agent 与 Human-in-the-Loop 将长期共存，自主度需要根据任务风险动态选择。
- 90% 的企业对上下文与记忆管理有明确需求，状态衰减、检索不准和遗忘机制缺失成为持续任务的主要障碍。
- 63% 的企业希望补齐多模型路由与自动降级能力，统一流量入口、成本治理与故障恢复成为基础设施诉求。
- 55% 的企业仍主要依赖人工抽查评估 Agent，基于运行轨迹进行自动评估的比例不足 8%。
- Coding Agent 率先规模化落地，但模型、工具与框架仍然碎片化，可迁移的工程抽象比押注单一产品更重要。

这些问题共同指向同一个结论：Agent 生产化的瓶颈不只在模型，更在模型之外的系统工程。本白皮书因此围绕 Agent 应用的完整生命周期展开：

| 生命周期 | 核心问题 | 白皮书回应 |
| --- | --- | --- |
| 架构 | 应该采用什么应用形态，授予 Agent 多大自主权？ | 定义 Agentic Application 的边界、成熟度与参考架构。 |
| 构建 | 如何把模型判断组织成可推进、可恢复、可验证的任务？ | 以 Harness 为核心，建立任务、信息与行动三类工程契约。 |
| 运行 | Agent 如何在真实环境中稳定、规模化地工作？ | 覆盖沙箱、状态存储、AI 网关、异步任务、多 Agent 协作与通信。 |
| 治理 | 如何看清行为、控制风险、管理资产并在上线前验证？ | 建立可观测、安全、资产管理和行为验证机制。 |
| 调优 | 如何把生产证据持续转化为能力提升？ | 从模型调优延伸到轨迹数据、黄金数据集、Badcase 与受控自进化。 |
| 实践 | 这些方法如何进入真实业务？ | 汇集研发、设计、运维、企业 IT、客户运营和 Agent Infra 案例。 |
| 展望 | Agentic Application 将走向哪里？ | 从应用级智能迈向 Agentic OS 与更广泛的智能协作系统。 |

## 2. 目标读者与收获

本白皮书主要面向企业级 Agent 构建与落地场景。它既适合从工程细节进入，也适合用于企业内部的技术选型、架构评审、项目立项和跨团队共识建设。

| 读者 | 建议关注 | 你将获得 |
| --- | --- | --- |
| Agent / AI 应用开发者 | 构建篇、运行篇、调优篇 | 掌握 Harness、上下文、状态、工具、沙箱、轨迹与评估闭环等核心工程方法。 |
| 架构师与平台工程师 | 架构篇、运行篇、治理篇 | 建立从组件、平台责任到生命周期的完整架构视图，形成可扩展的 Agent 基础设施设计。 |
| 技术负责人和研发管理者 | 架构篇、治理篇、实践篇 | 判断应用形态、成熟度、投入边界与生产风险，支撑选型、立项和组织协同。 |
| 产品与业务负责人 | 调研报告、架构篇、实践篇 | 理解适合 Agent 的任务、人与 Agent 的责任边界，以及从试点走向核心流程的条件。 |
| 安全、质量与运维人员 | 运行篇、治理篇、调优篇 | 建立可观测、审计、安全授权、上线验证、持续评估和故障归因机制。 |
| 研究者与生态贡献者 | 全书与实践篇 | 了解企业一线问题、工程抽象和开放议题，并参与共同完善行业知识体系。 |

完整阅读后，你将能够：

- 从业务目标、任务确定性和风险出发，选择最低充分的 Agent 架构；
- 理解 Model 与 Harness 的责任边界，不把所有问题都归因于模型能力；
- 设计可持续推进、可中断恢复、可验证完成的 Agent 任务系统；
- 为 Agent 建立执行环境、状态、流量、权限、观测与成本治理底座；
- 用 Trace、Trajectory、黄金数据集和评估实验形成持续改进的数据飞轮；
- 将方法映射到研发效能、设计、运维、企业 IT、客户运营等实际场景。

## 3. 阅读导引

### 目录结构

| 篇章 | 目录 | 章节范围 | 阅读重点 |
| --- | --- | --- | --- |
| [前言](./00-preface.md) | 根目录 | — | “智以致用”的写作背景、升级原因与全书范围。 |
| [2026 Agent 开发者调研报告](./2026-agent-survey-report.md) | 根目录 | — | 企业 Agent 开发、生产化、架构选型、工具链、治理与评估现状。 |
| [架构篇](./01-architecture/) | `01-architecture/` | 第 1–2 章 | 定义对象、判断形态、选择成熟度并建立参考架构。 |
| [构建篇](./02-build/) | `02-build/` | 第 3–6 章 | 以 Harness 为核心，组织任务、信息和行动。 |
| [运行篇](./03-run/) | `03-run/` | 第 7–12 章 | 从单 Agent 稳定运行扩展到异步、多 Agent 与分布式通信。 |
| [治理篇](./04-governance/) | `04-governance/` | 第 13–16 章 | 让运行可见、行为有边界、资产可管理、上线前可验证。 |
| [调优篇](./05-optimization/) | `05-optimization/` | 第 17–24 章 | 从模型与 Agent 两条主线构建持续优化闭环。 |
| [实践篇](./06-case-study/) | `06-case-study/` | 第 25–29 章 | 企业实践、垂直场景与 Agent Infra 前沿探索。 |
| [总结与展望篇](./07-conclusion/) | `07-conclusion/` | 第 30 章 | 从 Agentic Application 走向 Agentic OS。 |
| 图片资源 | `assets/imgs/` | — | 按章节归档的正文图片。 |

### 章节导航

| 篇章 | 章节 | 核心内容 |
| --- | --- | --- |
| 架构篇 | [第 1 章　AI 原生应用的新阶段](<./01-architecture/第 1 章　AI 原生应用的新阶段.md>) | 应用形态演进、Agentic Application 的定义与边界、企业成熟度判断。 |
| 架构篇 | [第 2 章　Agentic Application 参考架构](<./01-architecture/第 2 章　Agentic Application 参考架构.md>) | 组件视图、平台责任与生命周期视图，以及从决策到运行和改进的架构落位。 |
| 构建篇 | [第 3 章　范式：Harness 的主流构建方式和责任边界](<./02-build/第 3 章 范式：Harness 的主流构建方式和责任边界.md>) | 高代码框架、产品化 Harness、Managed Agents、Agent 云产品与平台责任。 |
| 构建篇 | [第 4 章　任务：编排、长程推进与协作流转](<./02-build/第 4 章 任务：编排、长程推进与协作流转.md>) | Agent Loop、任务状态机、计划、阶段门禁、委派、异步续行与完成证据。 |
| 构建篇 | [第 5 章　信息：上下文、状态与可复用能力资产](<./02-build/第 5 章 信息：上下文、状态与可复用能力资产.md>) | Context Builder、压缩与卸载、Session、Task State、Workspace、Memory、Knowledge 与 Skill。 |
| 构建篇 | [第 6 章　行动：受控执行、验证反馈与交付准备](<./02-build/第 6 章 行动：受控执行、验证反馈与交付准备.md>) | Action Plane、Function Calling、MCP、A2A、环境契约、权限、HITL 与验证闭环。 |
| 运行篇 | [第 7 章　Agent 运行时与沙箱](<./03-run/第 7 章  Agent 运行时与沙箱.md>) | 沙箱、Agent Runtime、工作空间、环境生命周期与生产运行条件。 |
| 运行篇 | [第 8 章　Agent 状态存储与语义资产](<./03-run/第 8 章 Agent 状态存储与语义资产.md>) | Event Log、Checkpoint、工作区快照、Artifact、长期记忆、RAG 与业务语义。 |
| 运行篇 | [第 9 章　AI 网关与统一流量治理](<./03-run/第 9 章  AI 网关与统一流量治理.md>) | LLM、MCP、Agent 三类流量的身份、权限、预算、路由、审计与审批。 |
| 运行篇 | [第 10 章　Agent 异步任务与自动化流程](<./03-run/第 10 章  Agent 异步任务与自动化流程.md>) | 同步与异步边界、任务完成语义、定时任务、长时任务与自动化工作流。 |
| 运行篇 | [第 11 章　Multi-Agent 协作与编排](<./03-run/第 11章  Multi-Agent 协作与编排.md>) | 异构 Agent 接入、团队拓扑、任务分派、结果聚合与编排职责。 |
| 运行篇 | [第 12 章　Agent 分布式通信](<./03-run/第 12 章 Agent 分布式通信.md>) | 能力面、协作面、内构面和人机面的通信协议与消息治理。 |
| 治理篇 | [第 13 章　Agent 的可观测性](<./04-governance/第 13 章　Agent 的可观测性.md>) | 指标、日志、Trace、事件、成本归因与审计。 |
| 治理篇 | [第 14 章　Agent 安全](<./04-governance/第 14 章　Agent 安全.md>) | Prompt Injection、身份鉴权、逐次校验、高危授权与数据出域防护。 |
| 治理篇 | [第 15 章　AI 资产的发现与管理](<./04-governance/第 15 章　AI 资产的发现与管理 .md>) | Prompt、Skill、MCP 与 Agent 的注册、版本、发现、依赖和发布管理。 |
| 治理篇 | [第 16 章　Agent 行为生成与质量验证](<./04-governance/第 16 章　Agent 行为生成与质量验证.md>) | 用户模拟、环境模拟、场景配置与上线前的 Agent Simulation。 |
| 调优篇 | [第 17 章　模型调优](<./05-optimization/第 17 章　模型调优.md>) | 模型问题的归因判据、SFT、Agentic RL、模型蒸馏与上线验收。 |
| 调优篇 | [第 18 章　Agent 调优总览](<./05-optimization/第 18 章　Agent 调优总览.md>) | Agent 调优对象、方法边界与数据飞轮全景。 |
| 调优篇 | [第 19 章　Agent 轨迹数据](<./05-optimization/第 19 章　Agent 轨迹数据.md>) | 从 Trace 到 Trajectory，组织可复用的行为与决策证据。 |
| 调优篇 | [第 20 章　Agent 运行时数据处理](<./05-optimization/第 20 章　Agent 运行时数据处理.md>) | 运行数据采集、清洗、加工与声明式数据 Pipeline。 |
| 调优篇 | [第 21 章　Agent 黄金数据集](<./05-optimization/第 21 章　Agent 黄金数据集.md>) | 构建带输入、轨迹、结果与判据的高质量评估数据资产。 |
| 调优篇 | [第 22 章　Agent 优化：Badcase](<./05-optimization/第 22 章　Agent 优化：Badcase .md>) | Badcase 发现、归因、修复、回归与实验验证。 |
| 调优篇 | [第 23 章　受控自进化](<./05-optimization/第 23 章　受控自进化.md>) | 把有效经验转化为 Memory、Skill、工具和运行机制，并控制自进化风险。 |
| 调优篇 | [第 24 章　Agent 边缘运行时与全球优化](<./05-optimization/第 24 章　Agent 边缘运行时与全球优化.md>) | 边缘运行时、边缘评估、性能成本、内容分发、安全与仿真。 |
| 实践篇 | [第 25 章　研发效能](<./06-case-study/第25章 研发效能/>) | 代码审查、缺陷检测、补丁交付、研发协作与端到端交付实践。 |
| 实践篇 | [第 26 章　设计工程](<./06-case-study/第26章 设计工程/>) | Vibe Designing 与 GenUI 的设计范式和工程实践。 |
| 实践篇 | [第 27 章　运维、安全与企业 IT](<./06-case-study/第27章 运维、安全与企业IT/>) | 汽车、连锁零售和企业软件的大规模智能运维实践。 |
| 实践篇 | [第 28 章　客户、销售与运营](<./06-case-study/第28章 客户、销售与运营/>) | 长周期记忆、内容洞察、办公提效和 Data Agent 实践。 |
| 实践篇 | [第 29 章　GOAI Agent Infra 赛道：多 Agent 协同的前沿实践探索](<./06-case-study/第 29 章  GOAI Agent Infra 赛道：多 Agent 协同的前沿实践探索.md>) | 世界人工智能开源大赛优秀作品与多领域 Agent Infra 探索。 |
| 总结与展望篇 | [第 30 章　从 Agentic Application 到 Agentic OS](<./07-conclusion/第 30 章 从 Agentic Application 到 Agentic OS.md>) | 从单个应用走向可协作、可治理、可持续演进的智能系统。 |

### 实践案例导航

| 章节 | 案例 |
| --- | --- |
| 第 25 章　研发效能 | [ABACI 内核补丁定向测试与缺陷检测智能体](<./06-case-study/第25章 研发效能/ABACI 内核补丁定向测试与缺陷检测智能体 .md>) |
| 第 25 章　研发效能 | [Kitta：领域专用 Code Review Agent](<./06-case-study/第25章 研发效能/Kitta：领域专用 Code Review Agent.md>) |
| 第 25 章　研发效能 | [PatchPilot Agents：让内核补丁交付成为可编排、可验证的工程闭环](<./06-case-study/第25章 研发效能/PatchPilot Agents：让内核补丁交付成为可编排、可验证的工程闭环.md>) |
| 第 25 章　研发效能 | [从报警到自动修复，PolarDB-X 的 Loop 工程实践](<./06-case-study/第25章 研发效能/从报警到自动修复，PolarDB-X 的 Loop 工程实践.md>) |
| 第 25 章　研发效能 | [从编码提效到端到端交付，云通信的人机协作实践](<./06-case-study/第25章 研发效能/从编码提效到端到端交付，云通信的人机协作实践.md>) |
| 第 25 章　研发效能 | [从评测驱动到端到端交付：AI Agent 安全产品研发提效实践](<./06-case-study/第25章 研发效能/从评测驱动到端到端交付：AI Agent 安全产品研发提效实践.md>) |
| 第 25 章　研发效能 | [多 Agent 组成研发小队：AI 研发如何从写代码走向端到端交付](<./06-case-study/第25章 研发效能/多 Agent 组成研发小队：AI 研发如何从写代码走向端到端交付.md>) |
| 第 26 章　设计工程 | [GenUI：让 Agent 从给出答案走向交付结果](<./06-case-study/第26章 设计工程/GenUI：让 Agent 从给出答案走向交付结果.md>) |
| 第 26 章　设计工程 | [Vibe Designing：意图驱动的 AI 设计范式进化](<./06-case-study/第26章 设计工程/Vibe Designing：意图驱动的AI设计范式进化.md>) |
| 第 27 章　运维、安全与企业 IT | [吉利汽车智能运维的落地实践](<./06-case-study/第27章 运维、安全与企业IT/吉利汽车智能运维的落地实践.md>) |
| 第 27 章　运维、安全与企业 IT | [塔斯汀万店连锁的智能运维闭环实践](<./06-case-study/第27章 运维、安全与企业IT/塔斯汀万店连锁的智能运维闭环实.md>) |
| 第 27 章　运维、安全与企业 IT | [畅捷通的可观测与智能运维实践](<./06-case-study/第27章 运维、安全与企业IT/畅捷通的可观测与智能运维实践.md>) |
| 第 28 章　客户、销售与运营 | [MiniMax 构建海量长周期记忆数据底座的实践](<./06-case-study/第28章 客户、销售与运营/MiniMax 构建海量长周期记忆数据底座的实践.md>) |
| 第 28 章　客户、销售与运营 | [会计师事务所信永中和的办公提效探索](<./06-case-study/第28章 客户、销售与运营/会计师事务所信永中和的办公提效探索.md>) |
| 第 28 章　客户、销售与运营 | [哔哩哔哩构建全域内容洞察的实践](<./06-case-study/第28章 客户、销售与运营/哔哩哔哩构建全域内容洞察的实践.md>) |
| 第 28 章　客户、销售与运营 | [运营分析 Data Agent 实践](<./06-case-study/第28章 客户、销售与运营/运营分析 Data Agent 实践.md>) |

### 推荐阅读路径

- **第一次系统了解企业 Agent**：调研报告 → 第 1–2 章 → 第 3–6 章 → 第 13–16 章。
- **正在把 Agent 接入生产**：第 7–9 章 → 第 13–14 章 → 第 18–23 章。
- **正在建设多 Agent 系统**：第 4–6 章 → 第 10–12 章 → 第 13、16 章。
- **负责评估与持续优化**：第 13 章 → 第 18–23 章 → 对应领域实践案例。
- **负责选型或项目立项**：调研报告 → 第 1–3 章 → 实践篇 → 第 30 章。

## 4. 下一步规划

白皮书将以开放项目的方式持续维护，而不是在首次发布后封存。接下来的重点包括：

- **扩展企业实践案例**：增加更多来自研发、运营、客服、数据、安全、财务和行业场景的一线案例，补充成功路径、架构取舍与真实失败模式。
- **增加云资源线上体验**：围绕沙箱、Runtime、AI 网关、状态存储、可观测和评估等关键能力，设计可复现的云上体验流程，让读者从阅读进一步走向动手验证。
- **持续完善治理内容**：跟进身份权限、Prompt Injection 防护、数据出域、审计、资产注册、版本治理和上线前仿真等企业核心议题。
- **持续完善评估体系**：补充任务成功率、轨迹评估、LLM-as-Judge、黄金数据集、Badcase 回归、线上实验和成本质量权衡等方法与案例。
- **跟进技术演进**：持续吸收模型、Harness、协议、Runtime、多 Agent 和 Agentic OS 的新进展，并及时修正已经不再适用的判断。
- **建设社区协作机制**：逐步完善内容规范、案例模板、术语表、校对流程和版本发布方式，降低高质量贡献的门槛。

### 欢迎贡献

欢迎开发者、架构师、研究者、企业技术团队和产品实践者参与共建。你可以：

- 提交 Issue，指出事实错误、概念歧义、链接失效或需要补充的主题；
- 提交 Pull Request，完善章节、修正内容、优化图表或补充参考资料；
- 分享经过脱敏的企业实践、故障复盘、评估方法与架构取舍；
- 提供可复现的代码、云资源体验流程、数据集或实验方案；
- 参与术语统一、技术审校、案例评审和内容翻译。

贡献内容应尊重原创与授权边界；涉及企业数据、客户信息、内部系统和安全细节时，请先完成必要的脱敏与许可确认。

## 5. 贡献者

感谢所有参与架构设计、章节写作、案例整理与内容审校的贡献者。以下名单整理自[作者文档](./作者.md)。

### 阿里巴巴 Agent 专家团队

当前白皮书作者均为阿里巴巴 Agent 专家团队成员。

| 贡献领域 | 团队成员 |
| --- | --- |
| 架构篇 | [王晨(望宸)](https://github.com/max-wc.png)、[沈林(静罗)](https://github.com/2011shenlin.png) |
| 构建篇 | [刘军(陆龟)](https://github.com/chickenlj.png)、[泮圣伟(十眠)](https://github.com/panxiaojun233.png) |
| 运行篇 | [赵庆杰(卢令)](https://github.com/jackzhao8886.png)、[李诗波(承吉)](https://github.com/ifree99.png)、[林清山(隆基)](https://github.com/hill007299.png)、[黄晓萌(学仁)](https://github.com/HuangXiaomeng.png)、[张添翼(澄潭)](https://github.com/johnlanni.png)、[赵源筱(如漫)](https://github.com/endlessseeker.png)、[孙校(洵沐)](https://github.com/sunxia0.png)、[宋震(凡玺)](https://github.com/skyrealman.png)、[胡庆达(执壹)](https://github.com/hqd2009.png)、[柳遵飞(翼严)](https://github.com/shiyiyue1102.png)、[朱桐(濯光)](https://github.com/Sunrisea.png)、[余华峰](https://github.com/maplefeng-a.png)、[罗鑫(子葵)](https://github.com/luoxiner.png)、[孔可青(青瑭)](https://github.com/kkqqqqqq.png) |
| 治理篇 | [肖长军(穹谷)](https://github.com/xcaspar.png)、[周洋(中亭)](https://github.com/aspnetdb.png)、[张磊(玄裕)](https://github.com/MrZhangL.png)、[王方(方羞)](https://github.com/fangxiu-wf.png)、[张海彬(古琦)](https://github.com/NameHaibinZhang.png)、[程书意(舒义)](https://github.com/chengshuyi.png)、[刘子明(牧思)](https://github.com/123liuziming.png)、[饶子昊(铖朴)](https://github.com/steverao.png)、[任懿(云邺)](https://github.com/boo0m.png)、[杨永(渭龙)](https://github.com/Chalres-yang.png)、[王硕(蓝知)](https://github.com/MagicBlueCH.png)、[马昕(灵闻)](https://github.com/maxin0324.png)、[刘宇轩(浴血)](https://github.com/uestc-lyx.png)、[杨翊(席翁)](https://github.com/KomachiSion.png) |
| 调优篇 | [张寒萌(若梨)](https://github.com/ColdMe.png)、[李盛荣(舒伯)](https://github.com/Lsrsaga.png)、[王亚宁(栀露)](https://github.com/Wyn123321.png)、[孙坚运(文渠)](https://github.com/simonjoylet.png)、[马云雷](https://github.com/mayunlei.png)、[王桢(士宁)](https://github.com/neverafraid1.png)、[郑前祎](https://github.com/zqyi.png)、[刘航(望夕)](https://github.com/liuhang51574-art.png)、[陈新(骏维)](https://github.com/chenx0116-bit.png) |
| 实践篇 | 杨涛(昀至)、朱颜(竞竞)、余艾琳(芋一)、胡峻(老糊) |
| 总结与展望篇 | 林演(林生) |

### 外部贡献者

当前暂无外部贡献者，项目持续开放社区贡献。欢迎开发者、架构师、研究者、企业技术团队和产品实践者通过 Issue 或 Pull Request 参与内容共建；贡献被采纳后，贡献者信息将补充到本模块。

---

如果这份白皮书帮助你更好地理解、构建或治理 Agent，欢迎分享、讨论并参与共建。
