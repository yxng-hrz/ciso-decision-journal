# Enterprise Risk Mapping

## 1. Scope
This risk mapping covers information security, business continuity,
regulatory compliance, and reputational risks.

## 2. Critical Assets
| Asset | Description | Impact |
|-----|------------|--------|
| Customer Data | Personal & business data | Critical |
| SaaS Platform | Core revenue service | Critical |
| Cloud Infrastructure | Compute, storage, IAM | High |
| Brand Reputation | Customer trust | High |
| Key Staff | DevOps & senior engineers | Medium |

## 3. Threat Landscape
- Ransomware
- Credential compromise
- Third-party breaches
- Human error
- Cloud provider outage

## 4. Risk Scenarios
### R1 – Ransomware on production
- Likelihood: Medium
- Impact: Very High
- Inherent Risk: Critical

### R2 – Data breach via compromised account
- Likelihood: High
- Impact: High
- Inherent Risk: Critical

### R3 – Prolonged service outage
- Likelihood: Medium
- Impact: High
- Inherent Risk: High

### R4 – GDPR non-compliance
- Likelihood: Medium
- Impact: Medium/High
- Inherent Risk: High

## 5. Risk Treatment
| Risk | Strategy | Controls | Residual Risk |
|----|---------|---------|---------------|
| R1 | Reduce | Offline backups, DRP | Medium |
| R2 | Reduce | MFA, RBAC, training | Medium |
| R3 | Reduce | Redundancy, SLA | Low |
| R4 | Reduce | Audits, policies | Low |

## 6. Executive Conclusion
Critical risks are identified, owned, and actively managed.
Residual risks are accepted knowingly by management.