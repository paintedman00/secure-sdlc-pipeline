# Security policy

## Scope
This repository is a teaching reference. The Flask application contains an **intentional** SQL injection in `GET /search`. It is documented and doesn't need to be reported.

Reports are welcome for anything else, in particular:
- weaknesses in the pipeline itself, such as workflow permissions, action pinning or ways to bypass a gate
- unintentional vulnerabilities in the application
- vulnerable dependencies the scanners missed

## Reporting
Use GitHub's private vulnerability reporting: **Security > Report a vulnerability** on this repository. Please don't open a public issue for an unfixed problem.

You can expect an acknowledgement within 3 working days. Fix timelines follow the severity SLAs in the [triage policy](README.md#triage-policy).
