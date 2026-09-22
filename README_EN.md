<div align="right"><a href="./README.md">中文</a> | English</div>

# AI Agent Core Technology White Paper

<div align="center">
  <p><strong>Putting Intelligence to Work: From Building AI to Using It Well</strong></p>
  <p>A lifecycle guide to architecting, building, operating, governing, and improving enterprise AI agents</p>
</div>

---

## 1. Background and Structure

As models move beyond generating content to understanding goals, using tools, interacting with environments, and completing long-running tasks, the enterprise question changes. It is no longer just how to integrate a large model, but how to make agents reliable, controllable, and scalable. Model capability remains essential, but a production agent also needs a harness, runtime, state store, tool and protocol layer, gateway, security controls, observability, evaluation, and continuous improvement.

The guiding idea of this white paper is to turn broadly available cognitive capability into dependable task outcomes. Rather than committing to one model, framework, or vendor, it develops a coherent vocabulary, reference architecture, and set of engineering boundaries that teams can carry across changing technologies.

### Why this white paper

The [2026 Agent Developer Survey Report](./2026-agent-survey-report.md) collected 1,906 valid responses from enterprise technology decision-makers, architects, engineers, and product managers. Its central finding is a gap between agent development and production deployment:

- 46% of respondents had completed or were developing agents, but only 18% had deployed them in production.
- Single-agent systems, multi-agent systems, and human-in-the-loop designs are likely to coexist; autonomy should match task risk.
- 90% of enterprises reported a need for context and memory management. State degradation, inaccurate retrieval, and missing update or forgetting mechanisms hinder long-running work.
- 63% wanted better multi-model routing and automatic fallback, making a shared traffic entry point and cost controls important infrastructure concerns.
- 55% still relied mainly on manual sampling to evaluate agents, while fewer than 8% used automated evaluation based on execution trajectories.
- Coding agents have led adoption, but models, tools, and frameworks remain fragmented. Portable engineering abstractions matter more than betting on one product.

These findings suggest that production readiness is not solely a model problem. The white paper therefore follows the full agent-application lifecycle:

| Stage | Core question | What this white paper covers |
| --- | --- | --- |
| Architecture | What application form and level of autonomy fit the task? | Agentic Application boundaries, maturity, and a reference architecture. |
| Building | How can model decisions become tasks that advance, recover, and finish verifiably? | A harness built around contracts for tasks, information, and actions. |
| Runtime | How can agents work reliably and at scale in real environments? | Sandboxes, state storage, AI gateways, asynchronous work, multi-agent coordination, and communication. |
| Governance | How can teams observe behavior, control risk, manage assets, and validate before release? | Observability, security, asset management, and behavior validation. |
| Optimization | How can production evidence lead to measurable improvement? | Model tuning, trajectories, golden datasets, bad-case analysis, and controlled self-evolution. |
| Practice | How do these ideas translate into business workflows? | Cases in software engineering, design, operations, enterprise IT, customer operations, and agent infrastructure. |
| Outlook | What comes after an Agentic Application? | A path toward Agentic OS and broader intelligent collaboration. |

## 2. Audience and Takeaways

This white paper is primarily for teams building and deploying enterprise agents. It can also support technology selection, architecture reviews, project proposals, and a shared vocabulary across organizations.

| Reader | Recommended sections | What you will gain |
| --- | --- | --- |
| Agent and AI application developers | Building, Runtime, Optimization | Engineering methods for harnesses, context, state, tools, sandboxes, trajectories, and evaluation. |
| Architects and platform engineers | Architecture, Runtime, Governance | An architecture spanning components, platform responsibilities, and the application lifecycle. |
| Technology and engineering leaders | Architecture, Governance, Practice | Criteria for application form, maturity, investment boundaries, and production risk. |
| Product and business leaders | Survey, Architecture, Practice | A way to identify suitable tasks, define human-agent responsibilities, and plan the path beyond pilots. |
| Security, quality, and operations teams | Runtime, Governance, Optimization | Approaches to observation, audit, authorization, release validation, evaluation, and root-cause analysis. |
| Researchers and ecosystem contributors | Entire white paper and Practice | First-hand enterprise problems, reusable abstractions, and open questions for further work. |

By the end, you should be able to:

- Choose the least complex agent architecture sufficient for the business goal, task uncertainty, and risk.
- Distinguish model limitations from harness and systems-engineering problems.
- Design tasks that can advance over time, recover from interruption, and finish based on verifiable evidence.
- Provide an execution environment, state, traffic management, permissions, observability, and cost controls.
- Build an improvement loop using traces, trajectories, golden datasets, and evaluation experiments.
- Apply these methods to software engineering, design, operations, enterprise IT, and customer-facing use cases.

## 3. Reading Guide

The linked chapters and case studies are currently written in Chinese; this English README is a guide to the existing content, not a translation of the entire white paper.

### Repository structure

| Part | Directory | Chapters | Focus |
| --- | --- | --- | --- |
| [Preface](./00-preface/00-preface.md) | `00-preface/` | — | Motivation, the reasons for this revision, and the scope of the book. |
| [2026 Agent Developer Survey Report](./2026-agent-survey-report.md) | Repository root | — | Enterprise development, production adoption, architecture choices, toolchains, governance, and evaluation. |
| [Architecture](./01-architecture/) | `01-architecture/` | 1–2 | Define the system, select an application form, assess maturity, and establish a reference architecture. |
| [Building](./02-build/) | `02-build/` | 3–6 | Organize tasks, information, and actions around the harness. |
| [Runtime](./03-run/) | `03-run/` | 7–12 | From reliable single-agent execution to asynchronous and distributed multi-agent systems. |
| [Governance](./04-governance/) | `04-governance/` | 13–16 | Make operations visible, behavior bounded, assets manageable, and release behavior testable. |
| [Optimization](./05-optimization/) | `05-optimization/` | 17–24 | Continuous improvement of both models and agents. |
| [Practice](./06-case-study/) | `06-case-study/` | 25–29 | Enterprise cases, domain applications, and agent-infrastructure exploration. |
| [Conclusion and Outlook](./07-conclusion/) | `07-conclusion/` | 30 | From Agentic Application to Agentic OS. |
| Image assets | `assets/imgs/` | — | Figures organized by chapter. |

### Chapter guide

| Part | Chapter | Main topics |
| --- | --- | --- |
| Architecture | [1. A New Stage for AI-Native Applications](<./01-architecture/第 1 章　AI 原生应用的新阶段.md>) | Application evolution, Agentic Application boundaries, and enterprise maturity. |
| Architecture | [2. Agentic Application Reference Architecture](<./01-architecture/第 2 章　Agentic Application 参考架构.md>) | Component, platform-responsibility, and lifecycle views. |
| Building | [3. Harness Construction Patterns and Responsibilities](<./02-build/第 3 章 范式：Harness 的主流构建方式和责任边界.md>) | Code-first frameworks, productized harnesses, managed agents, cloud products, and platform boundaries. |
| Building | [4. Tasks: Orchestration and Long-Horizon Collaboration](<./02-build/第 4 章 任务：编排、长程推进与协作流转.md>) | Agent loops, task state machines, planning, delegation, asynchronous continuation, and completion evidence. |
| Building | [5. Information: Context, State, and Reusable Assets](<./02-build/第 5 章 信息：上下文、状态与可复用能力资产.md>) | Context builders, compression, sessions, task state, workspaces, memory, knowledge, and skills. |
| Building | [6. Actions: Controlled Execution and Verification](<./02-build/第 6 章 行动：受控执行、验证反馈与交付准备.md>) | Action planes, Function Calling, MCP, A2A, environment contracts, permissions, and human approval. |
| Runtime | [7. Agent Runtime and Sandboxes](<./03-run/第 7 章  Agent 运行时与沙箱.md>) | Sandboxes, runtime, workspaces, environment lifecycle, and production execution. |
| Runtime | [8. Agent State Storage and Semantic Assets](<./03-run/第 8 章 Agent 状态存储与语义资产.md>) | Event logs, checkpoints, snapshots, artifacts, long-term memory, RAG, and business semantics. |
| Runtime | [9. AI Gateways and Unified Traffic Governance](<./03-run/第 9 章  AI 网关与统一流量治理.md>) | Identity, permissions, budgets, routing, audit, and approval across LLM, MCP, and agent traffic. |
| Runtime | [10. Asynchronous Agent Tasks and Automation](<./03-run/第 10 章  Agent 异步任务与自动化流程.md>) | Synchronous/asynchronous boundaries, completion semantics, scheduled work, and workflows. |
| Runtime | [11. Multi-Agent Coordination and Orchestration](<./03-run/第 11章  Multi-Agent 协作与编排.md>) | Heterogeneous agents, team topology, task assignment, result aggregation, and orchestration roles. |
| Runtime | [12. Distributed Agent Communication](<./03-run/第 12 章 Agent 分布式通信.md>) | Protocol choices and message governance across capability, collaboration, internal, and human-agent interactions. |
| Governance | [13. Agent Observability](<./04-governance/第 13 章　Agent 的可观测性.md>) | Metrics, logs, traces, events, cost attribution, and audit. |
| Governance | [14. Agent Security](<./04-governance/第 14 章　Agent 安全.md>) | Prompt injection, identity, per-action validation, high-risk authorization, and data-egress controls. |
| Governance | [15. Discovery and Management of AI Assets](<./04-governance/第 15 章　AI 资产的发现与管理 .md>) | Registration, versioning, discovery, dependencies, and releases for prompts, skills, MCP, and agents. |
| Governance | [16. Agent Behavior Generation and Quality Validation](<./04-governance/第 16 章　Agent 行为生成与质量验证.md>) | User and environment simulation, scenarios, and pre-release validation. |
| Optimization | [17. Model Tuning](<./05-optimization/第 17 章　模型调优.md>) | Root-cause criteria, SFT, agentic RL, distillation, and production acceptance. |
| Optimization | [18. Overview of Agent Optimization](<./05-optimization/第 18 章　Agent 调优总览.md>) | Optimization targets, method boundaries, and the data flywheel. |
| Optimization | [19. Agent Trajectory Data](<./05-optimization/第 19 章　Agent 轨迹数据.md>) | Turning traces into reusable behavioral and decision evidence. |
| Optimization | [20. Processing Agent Runtime Data](<./05-optimization/第 20 章　Agent 运行时数据处理.md>) | Collection, cleaning, processing, and declarative data pipelines. |
| Optimization | [21. Golden Datasets for Agents](<./05-optimization/第 21 章　Agent 黄金数据集.md>) | Evaluation assets with inputs, trajectories, outcomes, and judging criteria. |
| Optimization | [22. Improving Agents Through Bad Cases](<./05-optimization/第 22 章　Agent 优化：Badcase .md>) | Failure discovery, attribution, fixes, regression checks, and experiments. |
| Optimization | [23. Controlled Self-Evolution](<./05-optimization/第 23 章　受控自进化.md>) | Turning validated experience into memory, skills, tools, and runtime improvements. |
| Optimization | [24. Edge Runtime and Global Optimization](<./05-optimization/第 24 章　Agent 边缘运行时与全球优化.md>) | Edge runtime, evaluation, performance, cost, delivery, security, and simulation. |
| Practice | [25. Software Engineering Productivity](<./06-case-study/第25章 研发效能/>) | Code review, defect detection, patch delivery, and end-to-end engineering. |
| Practice | [26. Design Engineering](<./06-case-study/第26章 设计工程/>) | Vibe Designing and GenUI. |
| Practice | [27. Operations, Security, and Enterprise IT](<./06-case-study/第27章 运维、安全与企业IT/>) | Production operations in automotive, retail, and enterprise software. |
| Practice | [28. Customer, Sales, and Operations](<./06-case-study/第28章 客户、销售与运营/>) | Long-term memory, content insights, office productivity, and data agents. |
| Practice | [29. GOAI Agent Infra: Frontiers in Multi-Agent Collaboration](<./06-case-study/第 29 章  GOAI Agent Infra 赛道：多 Agent 协同的前沿实践探索.md>) | Open-source competition projects and agent-infrastructure exploration. |
| Conclusion and Outlook | [30. From Agentic Application to Agentic OS](<./07-conclusion/第 30 章 从 Agentic Application 到 Agentic OS.md>) | From individual applications toward collaborative, governable, evolving systems. |

### Case-study guide

| Chapter | Case study |
| --- | --- |
| 25. Software engineering | [ABACI: Targeted Testing and Defect Detection for Kernel Patches](<./06-case-study/第25章 研发效能/ABACI 内核补丁定向测试与缺陷检测智能体 .md>) |
| 25. Software engineering | [Kitta: A Domain-Specific Code Review Agent](<./06-case-study/第25章 研发效能/Kitta：领域专用 Code Review Agent.md>) |
| 25. Software engineering | [PatchPilot Agents: Orchestrated, Verifiable Kernel Patch Delivery](<./06-case-study/第25章 研发效能/PatchPilot Agents：让内核补丁交付成为可编排、可验证的工程闭环.md>) |
| 25. Software engineering | [From Alerts to Automatic Repair: PolarDB-X Loop Engineering](<./06-case-study/第25章 研发效能/从报警到自动修复，PolarDB-X 的 Loop 工程实践.md>) |
| 25. Software engineering | [From Coding Productivity to End-to-End Delivery: Human-Agent Collaboration in Cloud Communications](<./06-case-study/第25章 研发效能/从编码提效到端到端交付，云通信的人机协作实践.md>) |
| 25. Software engineering | [Evaluation-Driven Delivery: AI Agent Security Product Development](<./06-case-study/第25章 研发效能/从评测驱动到端到端交付：AI Agent 安全产品研发提效实践.md>) |
| 25. Software engineering | [A Multi-Agent Engineering Team: From Writing Code to End-to-End Delivery](<./06-case-study/第25章 研发效能/多 Agent 组成研发小队：AI 研发如何从写代码走向端到端交付.md>) |
| 26. Design engineering | [GenUI: From Answers to Deliverables](<./06-case-study/第26章 设计工程/GenUI：让 Agent 从给出答案走向交付结果.md>) |
| 26. Design engineering | [Vibe Designing: An Intent-Driven AI Design Paradigm](<./06-case-study/第26章 设计工程/Vibe Designing：意图驱动的AI设计范式进化.md>) |
| 27. Operations and IT | [Geely's Intelligent Operations Practice](<./06-case-study/第27章 运维、安全与企业IT/吉利汽车智能运维的落地实践.md>) |
| 27. Operations and IT | [Tastien's Intelligent Operations Loop Across 10,000 Stores](<./06-case-study/第27章 运维、安全与企业IT/塔斯汀万店连锁的智能运维闭环实.md>) |
| 27. Operations and IT | [ChangJieTong's Observability and Intelligent Operations](<./06-case-study/第27章 运维、安全与企业IT/畅捷通的可观测与智能运维实践.md>) |
| 28. Customer and operations | [MiniMax's Long-Horizon Memory Data Foundation](<./06-case-study/第28章 客户、销售与运营/MiniMax 构建海量长周期记忆数据底座的实践.md>) |
| 28. Customer and operations | [Office Productivity at ShineWing, an Accounting Firm](<./06-case-study/第28章 客户、销售与运营/会计师事务所信永中和的办公提效探索.md>) |
| 28. Customer and operations | [Bilibili's Cross-Platform Content Insights](<./06-case-study/第28章 客户、销售与运营/哔哩哔哩构建全域内容洞察的实践.md>) |
| 28. Customer and operations | [Data Agent for Operational Analytics](<./06-case-study/第28章 客户、销售与运营/运营分析 Data Agent 实践.md>) |

### Suggested reading paths

- **New to enterprise agents:** Survey → Chapters 1–2 → Chapters 3–6 → Chapters 13–16.
- **Moving an agent into production:** Chapters 7–9 → Chapters 13–14 → Chapters 18–23.
- **Building a multi-agent system:** Chapters 4–6 → Chapters 10–12 → Chapters 13 and 16.
- **Responsible for evaluation and optimization:** Chapter 13 → Chapters 18–23 → relevant case studies.
- **Responsible for selection or project approval:** Survey → Chapters 1–3 → Practice → Chapter 30.

## 4. Roadmap

This white paper is an open, evolving project rather than a document frozen after its first release. Planned work includes:

- **More enterprise cases:** Add first-hand examples from engineering, operations, customer service, data, security, finance, and industry-specific workflows, including trade-offs and failure modes.
- **Hands-on cloud experiences:** Create reproducible online exercises for sandboxes, runtimes, AI gateways, state storage, observability, and evaluation.
- **Deeper governance coverage:** Track enterprise needs in identity, prompt-injection defense, data egress, audit, asset registration, versioning, and pre-release simulation.
- **Stronger evaluation methods:** Expand coverage of task success rates, trajectory evaluation, LLM-as-Judge, golden datasets, bad-case regression, online experiments, and quality–cost trade-offs.
- **Ongoing technical updates:** Revisit conclusions as models, harnesses, protocols, runtimes, multi-agent systems, and Agentic OS evolve.
- **Community collaboration:** Improve content guidelines, case templates, terminology, review processes, and release practices.

### Contributing

Developers, architects, researchers, enterprise teams, and product practitioners are welcome to contribute. You can open an Issue to report an error or suggest a topic; submit a Pull Request to improve a chapter, figure, or reference; share a sanitized case study or postmortem; or contribute reproducible code, cloud exercises, datasets, and experiments.

Please respect authorship and permission boundaries. Remove or obtain authorization for enterprise data, customer information, internal-system details, and security-sensitive material before contributing.

## 5. Contributors

Thanks to everyone who has helped with architecture, writing, case studies, and review. 

### Alibaba Agent Expert Team

All current white-paper authors belong to the Alibaba Agent Expert Team. Names are retained as recorded in the Chinese author roster; where a GitHub ID is provided, the name links to the corresponding GitHub avatar URL.

| Contribution area | Team members |
| --- | --- |
| Architecture | [王晨(望宸)](https://github.com/max-wc), [沈林(静罗)](https://github.com/2011shenlin) |
| Building | [刘军(陆龟)](https://github.com/chickenlj), [泮圣伟(十眠)](https://github.com/panxiaojun233) |
| Runtime | [赵庆杰(卢令)](https://github.com/jackzhao8886), [李诗波(承吉)](https://github.com/ifree99), [林清山(隆基)](https://github.com/hill007299), [黄晓萌(学仁)](https://github.com/HuangXiaomeng), [张添翼(澄潭)](https://github.com/johnlanni), [赵源筱(如漫)](https://github.com/endlessseeker), [孙校(洵沐)](https://github.com/sunxia0), [宋震(凡玺)](https://github.com/skyrealman), [胡庆达(执壹)](https://github.com/hqd2009), [柳遵飞(翼严)](https://github.com/shiyiyue1102), [朱桐(濯光)](https://github.com/Sunrisea), [余华峰](https://github.com/maplefeng-a), [罗鑫(子葵)](https://github.com/luoxiner), [孔可青(青瑭)](https://github.com/kkqqqqqq) |
| Governance | [肖长军(穹谷)](https://github.com/xcaspar), [周洋(中亭)](https://github.com/aspnetdb), [张磊(玄裕)](https://github.com/MrZhangL), [王方(方羞)](https://github.com/fangxiu-wf), [张海彬(古琦)](https://github.com/NameHaibinZhang), [程书意(舒义)](https://github.com/chengshuyi), [刘子明(牧思)](https://github.com/123liuziming), [饶子昊(铖朴)](https://github.com/steverao), [任懿(云邺)](https://github.com/boo0m), [杨永(渭龙)](https://github.com/Chalres-yang), [王硕(蓝知)](https://github.com/MagicBlueCH), [马昕(灵闻)](https://github.com/maxin0324), [刘宇轩(浴血)](https://github.com/uestc-lyx), [杨翊(席翁)](https://github.com/KomachiSion) |
| Optimization | [张寒萌(若梨)](https://github.com/ColdMe), [李盛荣(舒伯)](https://github.com/Lsrsaga), [王亚宁(栀露)](https://github.com/Wyn123321), [孙坚运(文渠)](https://github.com/simonjoylet), [马云雷](https://github.com/mayunlei), [王桢(士宁)](https://github.com/neverafraid1), [郑前祎](https://github.com/zqyi), [刘航(望夕)](https://github.com/liuhang51574-art), [陈新(骏维)](https://github.com/chenx0116-bit) |
| Practice | 杨涛(昀至), 朱颜(竞竞), 余艾琳(芋一), 胡峻(老糊) |
| Conclusion and Outlook | 林演(林生) |

### External Contributors

Community contributions are welcome through Issues and Pull Requests; accepted contributors will be acknowledged here.

---

If this white paper helps you understand, build, or govern agents, please share it, discuss it, and help improve it.
