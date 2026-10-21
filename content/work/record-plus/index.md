---
title: Record Plus Investigation Platform
description: "Case study: turning document analysis, business rules, and data-science output into investigator-facing workflows."
eyebrow: Case study / 03
heading: 'Turning complex analysis into <em>usable investigation workflows.</em>'
meta:
  - Healthcare fraud investigation
  - ASP.NET · Blazor · JavaScript
  - 2025–present
weight: 30
tags:
  - Healthcare
  - Blazor
  - ASP.NET
  - AI
aliases:
  - /work/record-plus.html
intro:
  - "From an early split-screen prototype to a production platform with approximately eleven major feature areas—all while the product’s requirements were still taking shape."
  - "Record Plus is a web-based platform for investigators reviewing healthcare claims, medical records, and related evidence. It brings document review, data analysis, business rules, and AI-assisted insights into a central workspace."
cardTitle: 'Record Plus Investigation Platform'
cardBlurb: "Turning document analysis, business rules, and data-science output into investigator-facing workflows."
---

{{< case-section eyebrow="The challenge" >}}
## Data is only valuable when people can act on it.

The platform started as a limited interface: a PDF document alongside a single information tab. As the product grew, the team needed to turn outputs from document processing and data-science services into workflows investigators could understand, navigate, and trust.

The work was exploratory. Requirements often began as concepts rather than complete specifications, so the engineering role included identifying unanswered questions, refining intended behavior with stakeholders, and translating the result into testable, maintainable functionality.
{{< /case-section >}}

{{< case-section eyebrow="My role" >}}
## Engineering, technical analysis, and product refinement.

I worked across the front end and back end: clarifying feature ideas, implementing Blazor and JavaScript behavior, integrating APIs and data services, translating business rules into application logic, supporting QA, resolving defects, and preparing features for release.

That combination mattered because individual tabs were substantial products in their own right. A feature could involve a new investigator workflow, several data sources, document interaction, export behavior, and careful coordination with existing functionality.
{{< /case-section >}}

{{< case-section eyebrow="Document analysis" >}}
## Make document intelligence interactive.

Data-science services identify meaningful regions in medical and claim documents, such as provider information and other structured sections. I integrated those API results into the investigation interface and built controls that allow users to choose which detected sections are visible as PDF layers.

This shifted document analysis from a static backend result into an active investigative tool: users could focus on relevant evidence without losing the context of the underlying record.
{{< /case-section >}}

{{< case-section eyebrow="Architecture" >}}
## Give a fast-growing product safer boundaries.

As feature count increased, tightly coupled interactions made it easier for one change to disturb an unrelated tab or document behavior. I reorganized the JavaScript-heavy portions of the page into functional modules and introduced a publish-subscribe event bus.

- Modules publish state changes instead of directly manipulating one another
- Features subscribe only to the events they need
- Reduced direct dependencies and regression risk
- Created a clearer extension pattern as the product continued to grow

{{< pullquote >}}A prototype can survive on direct connections. A product needs boundaries that make the next change safer.{{< /pullquote >}}
{{< /case-section >}}

{{< case-section eyebrow="Claim Assist and comparison" >}}
## Build complex workflows from incomplete inputs.

I implemented significant parts of Claim Assist, an experience that lets investigators search for a claim and generate a multi-section analysis that can include organization-defined business rules, medical literature, medication information, side effects, and related claim or document analysis.

I also worked on document-comparison functionality that helps investigators identify copied content between records, highlight relevant areas, review findings side by side, and export results. In both areas, the key engineering work was converting stakeholder intent into clear logic without destabilizing the rest of the application.
{{< /case-section >}}

{{< case-section eyebrow="AI-assisted development" >}}
## Use AI tools without outsourcing judgment.

In a sensitive healthcare environment, I used approved AI-assisted development tools within the organization’s established workflow. They helped me explore implementation patterns in unfamiliar JavaScript-heavy areas, while I retained responsibility for architecture, security, review, validation, testing, and maintainability.

That discipline was essential: no protected healthcare data was exposed, and every resulting implementation still had to be understood and owned by the engineer responsible for it.
{{< /case-section >}}

{{< case-section eyebrow="Impact" >}}
## From prototype to a production investigation platform.

- Expanded from an early split-screen prototype to approximately eleven major feature areas
- Made data-science and AI outputs usable within investigator workflows
- Centralized document review, claim analysis, comparison, business rules, and related evidence
- Established architectural patterns that support safer future feature development
- Helped move exploratory product ideas through QA and formal release

{{< pullquote >}}The strongest engineering contribution was not just building features. It was helping define the product those features needed to become.{{< /pullquote >}}
{{< /case-section >}}
