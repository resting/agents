# Domain Research Template

Use this template when producing `/docs/01-domain-research.md`.

---

## Pre-Research Checklist

Before writing, ensure you have searched for:

1. **Wikipedia / encyclopedic sources** — for foundational overview
2. **Academic or authoritative sources** — for accuracy on mechanics
3. **Existing software implementations** — GitHub repos, commercial products
4. **Community discussions** — Reddit, forums, Stack Overflow for edge cases
5. **Tutorial/educational content** — for step-by-step breakdowns

## Document Structure

```markdown
# Domain Research: [Topic Name]
> Generated: [date] | Project: [project name]
> Sources consulted: [count]

## 1. Overview
What is [topic]? Where does it come from? Why does it matter?
Write 2-3 paragraphs that give a newcomer solid footing.

## 2. Core Concepts & Glossary

| Term | Definition | Relevance to App |
|------|-----------|-----------------|
| ... | ... | ... |

## 3. How It Works
Step-by-step mechanics. Use numbered steps.
Include formulas in plain text or LaTeX if mathematical.
Describe any decision trees or branching logic.

### 3.1 [Sub-process A]
### 3.2 [Sub-process B]
### 3.3 [Sub-process C]

## 4. Data Models

### Entities
- Entity A: [fields, types, relationships]
- Entity B: [fields, types, relationships]

### Relationships
- Entity A has-many Entity B
- Entity C belongs-to Entity A

### Sample Data
Provide a concrete example with real values.

## 5. Algorithms & Logic

### Algorithm 1: [Name]
- Input: [what goes in]
- Process: [step-by-step]
- Output: [what comes out]
- Edge cases: [what can go wrong]

### Algorithm 2: [Name]
[repeat pattern]

## 6. Existing Solutions

| Solution | Type | Strengths | Weaknesses | URL |
|----------|------|-----------|------------|-----|
| ... | ... | ... | ... | ... |

### Key Takeaways from Competitors
What can we steal (ethically)? What should we avoid?

## 7. Edge Cases & Gotchas
- Gotcha 1: [description and mitigation]
- Gotcha 2: [description and mitigation]

## 8. Implementation Considerations
- What libraries or APIs exist for this domain?
- What's the computational complexity?
- Any licensing or IP concerns?

## 9. Sources
1. [Title](URL) — [brief note on what was useful]
2. [Title](URL) — [brief note]
```

## Quality Checklist

Before finalizing the research document:

- [ ] Could a developer who knows NOTHING about this domain read this and understand it?
- [ ] Are all formulas/algorithms specific enough to implement?
- [ ] Are data models concrete enough to create database schemas?
- [ ] Have at least 5 sources been consulted?
- [ ] Are edge cases documented?
- [ ] Is competitor analysis included?
