# 01 — Project Vision

**Project:** playwright-python-hybrid-framework
**Phase:** Phase 0 — Project Foundation
**Step:** Step 1 — Project Vision
**Status:** Draft — pending QA Lead review
**Document Owner:** AI Assistant (advisory), reviewed and approved by QA Lead

---

## 1. Project Overview

This project is a hybrid test automation framework built with **Python**, **Playwright**, and **Pytest**, targeting the **Automation Exercise** demo e-commerce application. It is developed as a standalone, professionally engineered QA portfolio project that follows a sequential, phase-based delivery model — starting with foundational planning and QA strategy before any code is written.

## 2. Project Purpose

The purpose of this project is to design and build a maintainable, scalable automation framework that validates the functional correctness of Automation Exercise across UI and API layers, while demonstrating the full lifecycle of professional QA engineering work: planning, design, architecture, implementation, execution, defect management, CI/CD integration, and reporting.

## 3. Business / QA Objective

- Provide reliable, repeatable automated regression coverage for Automation Exercise's core user journeys.
- Reduce reliance on manual regression testing for well-understood, stable functionality.
- Produce clear, evidence-based test results (reports, logs, screenshots) that support release confidence.
- Demonstrate QA judgment in deciding what to automate, how to structure coverage, and how to report outcomes — not just script execution.

## 4. Automation Objective

- Build a hybrid automation framework combining **UI automation** and **API automation** under a single, coherent architecture.
- Support **cross-browser execution** via Playwright.
- Integrate automated execution into a **CI/CD pipeline**.
- Produce structured, human-readable **test reports** with evidence (screenshots, logs, traces where applicable).
- Keep the framework maintainable through clear separation of concerns (test logic, page interactions, data, configuration).

## 5. Portfolio Objective

This project is intended to serve as a public, professional QA/SDET portfolio artifact that demonstrates:

- End-to-end QA engineering capability, not only automation scripting.
- Test strategy and planning discipline prior to implementation.
- Framework architecture decisions made with clear rationale.
- The ability to re-engineer a solution in a second technology stack with independent, justified design choices rather than direct translation.
- CI/CD, reporting, and metrics practices expected of a senior QA/SDET role.

## 6. Application Under Test

**Application:** Automation Exercise
**Type:** Publicly available demo e-commerce web application, commonly used for QA automation practice.

Specific functional scope, page inventory, and detailed application behavior will be documented in a later phase (**Phase 1 — Application & QA Baseline**) following direct application exploration. This document does not assume or predefine functional coverage.

## 7. Technology Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| Browser Automation | Playwright (Python) |
| Test Runner / Framework | Pytest |
| Test Scope | UI automation, API automation, Hybrid E2E |
| CI/CD | To be defined in Phase 14 — CI/CD |
| Reporting | To be defined in Phase 15 — Reporting & Observability |

Tooling choices for configuration management, reporting libraries, HTTP client, and CI provider are deliberately **not finalized** in this document and will be decided during **Phase 5 — Framework Architecture** and **Phase 6 — Project Setup**, based on Python/Pytest-specific engineering judgment.

## 8. Project Scope

This project covers the design and implementation of a hybrid automation framework for Automation Exercise, including test planning, framework architecture, automated test development, CI/CD integration, reporting, and a structured comparison against the existing TypeScript implementation. It does not cover manual testing execution, performance/load testing, or security testing unless explicitly added to scope in a later phase.

## 9. In-Scope Testing

| Testing Type | Description |
|---|---|
| UI Automation | Automated browser-based validation of user-facing workflows via Playwright. |
| API Automation | Automated validation of backend/API endpoints supporting the application, where available. |
| Hybrid E2E Automation | Test scenarios combining UI and API interactions within a single workflow (e.g., API-based setup with UI-based verification, or vice versa). |
| Regression Automation | Automated re-validation of core, stable functionality to detect unintended breakage. |
| Cross-Browser Validation | Execution of applicable test suites across multiple browser engines supported by Playwright. |
| CI/CD Validation | Automated execution of the test suite within a continuous integration pipeline. |
| Reporting and Test Evidence | Generation of structured test reports and supporting evidence (logs, screenshots, traces) for each execution. |

## 10. Out-of-Scope / Future Scope

- Performance, load, and stress testing.
- Security and penetration testing.
- Accessibility (a11y) testing, unless added explicitly in a later phase.
- Mobile-native application testing.
- Visual regression testing, unless explicitly added in a later phase.
- Production monitoring or synthetic testing.

Items listed here may be reconsidered in later phases but are explicitly excluded from the current project vision.

## 11. Relationship with the Existing Playwright + TypeScript Project

An existing Playwright + TypeScript hybrid automation framework was previously built for the same application (Automation Exercise). That project serves as a **functional, QA, and automation knowledge baseline** for this Python project — not as source code to be ported.

| Reused from TypeScript Project | Not Reused from TypeScript Project |
|---|---|
| Business and application understanding | TypeScript source code |
| Requirements and functional knowledge | Folder/project structure |
| Test coverage knowledge, scenarios, and test cases | TypeScript-specific abstractions and patterns |
| Test data concepts | Playwright Test (`@playwright/test`) runner-specific patterns |
| Lessons learned and known limitations | Architecture adopted purely because it existed previously |
| Useful, technology-agnostic architectural lessons | — |

This project and the TypeScript project are **separate, independently engineered codebases** that happen to target the same application and share QA knowledge.

## 12. Python Re-engineering Philosophy

Every framework and design decision in this project will be evaluated on its own merits from a **Python + Pytest** perspective, considering Python idioms, Pytest fixture and plugin conventions, and Playwright's Python API — rather than mirroring decisions made in the TypeScript implementation. Where a TypeScript-originated pattern is not idiomatic or optimal in Python/Pytest, it will be redesigned. Architectural decisions will be documented with rationale in later phases (**Phase 5 — Framework Architecture**).

## 13. Target QA Engineering Roles

| Role | Responsibility in This Project |
|---|---|
| QA Lead | Final decision-maker; approves plans, architecture, and phase completion. |
| Senior QA / Test Engineer | Test strategy, test design, coverage decisions, defect management. |
| Automation Engineer | Framework architecture, implementation, CI/CD integration. |
| AI Assistant | Advisory support — drafts documentation, proposes designs, executes approved steps; does not make unilateral decisions on scope or direction. |

## 14. High-Level Project Success Criteria

- A working hybrid (UI + API) Playwright + Python + Pytest framework is delivered.
- Test planning and design artifacts exist prior to and independently of implementation.
- The framework executes successfully in a CI/CD pipeline.
- Test results are reported with clear, reviewable evidence.
- Framework architecture decisions are documented with rationale.
- A structured, evidence-based comparison against the TypeScript project is produced (Phase 20), without a pre-decided outcome.
- All roadmap phases are completed sequentially with QA Lead sign-off at each phase.

## 15. Key Assumptions

- Automation Exercise remains publicly accessible and stable enough to support ongoing automated testing throughout the project.
- The existing TypeScript project's business/application knowledge is accurate and can be reused as a starting reference, subject to independent verification during Phase 1.
- The QA Lead will review and approve each phase before the next phase begins.
- Detailed application functionality and requirements will be confirmed through direct exploration in Phase 1, not assumed from this document.

## 16. Key Constraints

- Sequential phase-based delivery must be followed; implementation activities are not permitted ahead of their corresponding planning phases.
- No source code, dependencies, or framework files are to be created until the roadmap reaches the relevant setup/development phases.
- Design decisions must be independently justified for Python/Pytest and must not default to replicating the TypeScript project's structure.
- This document must not predefine detailed application requirements or test scenarios; those belong to later phases.

## 17. Initial Risks

| Risk | Potential Impact | Notes |
|---|---|---|
| Availability/stability of the public Automation Exercise site | Test flakiness or execution failures unrelated to framework quality | To be monitored from Phase 1 onward |
| Unconscious carry-over of TypeScript patterns into Python design | Reduces value of the re-engineering objective | Mitigated by explicit architectural rationale in Phase 5 |
| Scope creep into out-of-scope testing types | Delays core deliverables | Managed via strict adherence to Section 9/10 scope |
| Incomplete or outdated knowledge carried from the TypeScript baseline | Gaps or inaccuracies in test coverage | Mitigated by independent application review in Phase 1 |

## 18. Project Deliverables at a High Level

- QA planning and strategy documentation (Phases 0–4).
- Documented framework architecture with rationale (Phase 5).
- A working Python + Playwright + Pytest automation framework (Phases 6–10).
- Hardened, stable test execution (Phase 11–12).
- Defect management records (Phase 13).
- CI/CD pipeline integration (Phase 14).
- Test reporting and observability setup (Phase 15).
- QA metrics and test summary reporting (Phases 16–17).
- Release readiness assessment (Phase 18).
- Final engineering review and TypeScript vs Python assessment (Phases 19–20).
- Final documentation and portfolio publication (Phases 21–24).

## 19. Governance / Working Rules

- Work proceeds strictly according to the master roadmap, one phase and step at a time.
- No step may be skipped, reordered, or combined with implementation activity without explicit QA Lead direction.
- The AI Assistant acts in an advisory and execution-support capacity; the QA Lead retains final decision authority over scope, architecture, and acceptance of each phase/step.
- Each document or deliverable is scoped to exactly what its step requires — no unrequested files, code, or dependencies are introduced.
- Assumptions made in any document must be explicitly flagged for QA Lead review rather than silently accepted as fact.

## 20. Step 1 Exit Criteria

Step 1 — Project Vision is considered complete when:

- [x] `docs/01-Project-Vision.md` has been created.
- [x] The document defines project purpose, objectives, scope, and governance without prescribing implementation details.
- [x] The relationship to the existing TypeScript project is clearly defined, distinguishing reused knowledge from reused code/structure.
- [x] No source code, dependencies, or additional documents were created.
- [ ] QA Lead has reviewed and approved this document.

Approval of this exit criterion by the QA Lead is required before proceeding to the next step in Phase 0.
