# Architecture Document Template

Use this template when producing `/docs/03-architecture.md`.

---

```markdown
# Architecture: [Project Name]
> Generated: [date]
> Based on: 00-project-brief.md, 01-domain-research.md

## 1. Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | ... | ... |
| Backend | ... | ... |
| Database | ... | ... |
| Auth | ... | ... |
| Hosting | ... | ... |

## 2. System Architecture

### Component Diagram (text)
Describe components and their relationships.
Use ASCII art or describe data flow:

```
[User] → [Frontend] → [API Layer] → [Domain Logic] → [Database]
                                   ↘ [External API]
```

### Components
- **Component A**: [responsibility, inputs, outputs]
- **Component B**: [responsibility, inputs, outputs]

## 3. Data Models

### Schema

#### Table/Collection: [name]
| Field | Type | Constraints | Notes |
|-------|------|------------|-------|
| ... | ... | ... | ... |

### Relationships
[ERD description or relationship list]

## 4. API Design

### Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /api/v1/... | ... | Yes/No |
| POST | /api/v1/... | ... | Yes/No |

### Request/Response Examples
[Include concrete JSON examples]

## 5. UI/UX Wireframes (text descriptions)

### Screen 1: [Name]
- Layout: [description]
- Key elements: [list]
- User actions: [list]

### Screen 2: [Name]
[repeat]

## 6. Third-Party Dependencies

| Package | Purpose | License | Risk |
|---------|---------|---------|------|
| ... | ... | ... | Low/Med/High |

## 7. Security Considerations
- Authentication method
- Data validation approach
- Sensitive data handling

## 8. Deployment Strategy
- Environment setup
- Build process
- CI/CD (if applicable)
```

## Decision Principles

When making architecture decisions, prioritize:

1. **Simplicity** — Choose boring technology. The domain logic is complex enough.
2. **Domain fit** — Let the research document drive data model decisions.
3. **User's constraints** — Respect stated preferences (tech stack, hosting, budget).
4. **Progressive complexity** — v1 should be the simplest thing that works.
