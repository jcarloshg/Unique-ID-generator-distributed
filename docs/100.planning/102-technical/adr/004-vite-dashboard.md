# ADR-004: Vite for Web Dashboard

## Status
Accepted

## Context
We need a web-based dashboard to monitor generator health, view metrics, and manage the service. The dashboard is used by the operations team.

## Decision
We will use **Vite + React** for the web dashboard.

## Options Considered

| Option | Pros | Cons |
|--------|------|------|
| Vite + React | Fast dev server, modern tooling, team expertise | Additional build step |
| Next.js | SSR, API routes, file-based routing | Overkill for simple dashboard |
| Vue | Good documentation, simpler than React | Less team familiarity |
| Svelte | Minimal boilerplate, fast | Less ecosystem, less team familiarity |

## Decision Rationale
1. **Development speed** — Vite's hot module replacement speeds up development
2. **Modern tooling** — Standard choice for modern web apps
3. **Team expertise** — React proficiency available
4. **Performance** — Fast initial load and reactivity

## Consequences

### Positive
- Rapid UI development with hot reload
- Large ecosystem of components
- TypeScript integration for type safety
- Easy deployment as static files

### Negative
- SPA requires API backend for dynamic data
- Additional build pipeline complexity
- Separate service to deploy and monitor

## Implementation Notes
- Use **React 18** with functional components and hooks
- Use **TypeScript** for type safety
- Fetch health data from generator `/health` endpoints
- Display: instance status, uptime, IDs generated count, errors
- Use **Recharts** or **TanStack Table** for data visualization
