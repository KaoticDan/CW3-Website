# Website security checks

Scope: KaoticDan/CW3-Website; source baseline aa4444b52b025a718b1c5bd879e7d773e1b7e27e. Production build commands and application code are unchanged.

The required status is **Website security gate**. It fails when a required job fails, skips, lacks a receipt, or reports another revision. CI alone does not enforce merges or production assignment: configure GitHub branch protection and Vercel Deployment Checks separately. Do not force-promote a deployment with a failed required check.

Checks: full-history redacted Gitleaks; four locally tested Semgrep rules; static public-output boundary (no package audit: no manifest). Scheduled scans run weekly as well as on pull requests and main pushes. No repository or deployment secrets are required.

Vendored scripts and external dependencies still require review.

A passing workflow does not certify RLS, provider settings, live authentication, headers, rate limiting, or all application security. Existing advisories remain blockers; do not omit development dependencies or add audit exceptions to turn the gate green.

Dependency metadata audit transfer to registry.npmjs.org approved by the owner on 2026-10-20 for the six package-based websites. No source or secrets are intentionally sent.

Gitleaks has reviewed, path-and-exact-line exceptions for known public identifiers or cache function expressions. No credential format or entire directory is excluded. These exceptions do not establish database authorization safety.

Gitleaks has reviewed, path-and-exact-line exceptions for known public identifiers or cache function expressions. No credential format or entire directory is excluded. These exceptions do not establish database authorization safety.
