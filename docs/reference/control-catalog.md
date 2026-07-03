# CMMC Level 2 Control Requirements Catalog

> **Scope:** Tier 1 (IL4) CMMC Level 2 for NV011 and NV012.
> **Source of truth:** NIST SP 800-171 Rev. 2 (110 controls), CMMC 2.0 scoring (32 CFR Part 170), and NIST SP 800-171A assessment objectives.
> **Control text:** Verbatim from NIST SP 800-171 Rev. 2 PDF, extracted July 2026.
> **SPRS weights:** Official values from 32 CFR § 170.24(c)(2)(ii).
> **Generated:** 2026-07-02

## Scoring and POA&M Rules

| Score | CMMC Status | Meaning |
|-------|-------------|---------|
| 110 | Final Level 2 (Self) | All controls MET; valid 3 years |
| 88–109 | Conditional Level 2 (Self) | 80%+ with only POA&M-eligible gaps; 180-day closeout |
| <88 | No status | Not eligible for CUI contract award |

### Weight distribution

| Point value | Count | Meaning |
|-------------|-------|---------|
| 5 points | 42 | Significant exploitation or CUI exfiltration risk if not implemented |
| 3 points | 14 | Specific and confined effect on network/data security if not implemented |
| 1 point | 52 | Limited or indirect effect if not implemented |
| 3 or 5 points | 2 | Variable based on implementation (see below) |

### Variable-weight controls

- **IA.L2-3.5.3 (MFA):** 5 points if not implemented for any users; 3 points if implemented only for remote and privileged users.
- **SC.L2-3.13.11 (FIPS-validated cryptography):** 5 points if encryption is not employed; 3 points if encryption is employed but not FIPS-validated.

### POA&M restrictions

Only 1-point controls may be placed on a POA&M. The following six 1-point controls are **excluded** from POA&M eligibility per 32 CFR § 170.21(a)(2)(iii):

- AC.L2-3.1.20 – Verify and control/limit connections to and use of external systems
- AC.L2-3.1.22 – Control CUI posted or processed on publicly accessible systems
- CA.L2-3.12.4 – Develop, document, and periodically update system security plans
- PE.L2-3.10.3 – Escort visitors and monitor visitor activity
- PE.L2-3.10.4 – Maintain audit logs of physical access
- PE.L2-3.10.5 – Control and manage physical access devices

All 3-point and 5-point controls must be MET at assessment. A current System Security Plan (CA.L2-3.12.4) is required for the assessment to proceed.

## Control Catalog

### Access Control (AC)

**AC.L2-3.1.1** — 3.1.1 — *5 points*

> Limit system access to authorized users, processes acting on behalf of authorized users, and devices (including other systems).

- **NIST SP 800-53 mapping:** AC-2, AC-3, AC-17
- **CIS Controls v8:** CIS 3, 5, 6
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.2** — 3.1.2 — *5 points*

> Limit system access to the types of transactions and functions that authorized users are permitted to execute.

- **NIST SP 800-53 mapping:** AC-3
- **CIS Controls v8:** CIS 3, 6
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.3** — 3.1.3 — *1 point*

> Control the flow of CUI in accordance with approved authorizations.

- **NIST SP 800-53 mapping:** AC-4
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** Yes

**AC.L2-3.1.4** — 3.1.4 — *1 point*

> Separate the duties of individuals to reduce the risk of malevolent activity without collusion.

- **NIST SP 800-53 mapping:** AC-5
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** Yes

**AC.L2-3.1.5** — 3.1.5 — *3 points*

> Employ the principle of least privilege, including for specific security functions and privileged accounts.

- **NIST SP 800-53 mapping:** AC-6
- **CIS Controls v8:** CIS 4, 6
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.6** — 3.1.6 — *1 point*

> Use non-privileged accounts or roles when accessing nonsecurity functions.

- **NIST SP 800-53 mapping:** AC-6(2)
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** Yes

**AC.L2-3.1.7** — 3.1.7 — *1 point*

> Prevent non-privileged users from executing privileged functions and capture the execution of such functions in audit logs.

- **NIST SP 800-53 mapping:** AC-6(9), AC-6(10)
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** Yes

**AC.L2-3.1.8** — 3.1.8 — *1 point*

> Limit unsuccessful logon attempts.

- **NIST SP 800-53 mapping:** AC-7
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**AC.L2-3.1.9** — 3.1.9 — *1 point*

> Provide privacy and security notices consistent with applicable CUI rules.

- **NIST SP 800-53 mapping:** AC-8
- **POA&M eligibility:** Yes

**AC.L2-3.1.10** — 3.1.10 — *1 point*

> Use session lock with pattern-hiding displays to prevent access and viewing of data after a period of inactivity.

- **NIST SP 800-53 mapping:** AC-11, AC-11(1)
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** Yes

**AC.L2-3.1.11** — 3.1.11 — *1 point*

> Terminate (automatically) a user session after a defined condition.

- **NIST SP 800-53 mapping:** AC-12
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** Yes

**AC.L2-3.1.12** — 3.1.12 — *5 points*

> Monitor and control remote access sessions.

- **NIST SP 800-53 mapping:** AC-17(1), AC-17(2)
- **CIS Controls v8:** CIS 12, 13
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.13** — 3.1.13 — *5 points*

> Employ cryptographic mechanisms to protect the confidentiality of remote access sessions.

- **NIST SP 800-53 mapping:** AC-17(2)
- **CIS Controls v8:** CIS 13
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.14** — 3.1.14 — *1 point*

> Route remote access via managed access control points.

- **NIST SP 800-53 mapping:** AC-17(3)
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** Yes

**AC.L2-3.1.15** — 3.1.15 — *1 point*

> Authorize remote execution of privileged commands and remote access to security-relevant information.

- **NIST SP 800-53 mapping:** AC-17(4)
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** Yes

**AC.L2-3.1.16** — 3.1.16 — *5 points*

> Authorize wireless access prior to allowing such connections.

- **NIST SP 800-53 mapping:** AC-18
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.17** — 3.1.17 — *5 points*

> Protect wireless access using authentication and encryption.

- **NIST SP 800-53 mapping:** AC-18(1)
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.18** — 3.1.18 — *5 points*

> Control connection of mobile devices.

- **NIST SP 800-53 mapping:** AC-19
- **CIS Controls v8:** CIS 1
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.19** — 3.1.19 — *3 points*

> Encrypt CUI on mobile devices and mobile computing platforms.

- **NIST SP 800-53 mapping:** AC-19(5)
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**AC.L2-3.1.20** — 3.1.20 — *1 point*

> Verify and control/limit connections to and use of external systems.

- **NIST SP 800-53 mapping:** AC-20, AC-20(1)
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** No (1-point excluded per 32 CFR 170.21(a)(2)(iii))

**AC.L2-3.1.21** — 3.1.21 — *1 point*

> Limit use of portable storage devices on external systems.

- **NIST SP 800-53 mapping:** AC-20(2)
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** Yes

**AC.L2-3.1.22** — 3.1.22 — *1 point*

> Control CUI posted or processed on publicly accessible systems.

- **NIST SP 800-53 mapping:** AC-22
- **POA&M eligibility:** No (1-point excluded per 32 CFR 170.21(a)(2)(iii))

### Awareness and Training (AT)

**AT.L2-3.2.1** — 3.2.1 — *5 points*

> Ensure that managers, systems administrators, and users of organizational systems are made aware of the security risks associated with their activities and of the applicable policies, standards, and procedures related to the security of those systems.

- **NIST SP 800-53 mapping:** AT-2
- **CIS Controls v8:** CIS 14
- **POA&M eligibility:** No (3- or 5-point)

**AT.L2-3.2.2** — 3.2.2 — *5 points*

> Ensure that personnel are trained to carry out their assigned information security-related duties and responsibilities.

- **NIST SP 800-53 mapping:** AT-3
- **CIS Controls v8:** CIS 14
- **POA&M eligibility:** No (3- or 5-point)

**AT.L2-3.2.3** — 3.2.3 — *1 point*

> Provide security awareness training on recognizing and reporting potential indicators of insider threat.

- **NIST SP 800-53 mapping:** AT-2(2)
- **CIS Controls v8:** CIS 14
- **POA&M eligibility:** Yes

### Audit and Accountability (AU)

**AU.L2-3.3.1** — 3.3.1 — *5 points*

> Create and retain system audit logs and records to the extent needed to enable the monitoring, analysis, investigation, and reporting of unlawful or unauthorized system activity.

- **NIST SP 800-53 mapping:** AU-2, AU-3, AU-3(1), AU-6
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** No (3- or 5-point)

**AU.L2-3.3.2** — 3.3.2 — *3 points*

> Ensure that the actions of individual system users can be uniquely traced to those users, so they can be held accountable for their actions.

- **NIST SP 800-53 mapping:** AU-2, AU-3, AU-6
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** No (3- or 5-point)

**AU.L2-3.3.3** — 3.3.3 — *1 point*

> Review and update logged events.

- **NIST SP 800-53 mapping:** AU-2(3)
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** Yes

**AU.L2-3.3.4** — 3.3.4 — *1 point*

> Alert in the event of an audit logging process failure.

- **NIST SP 800-53 mapping:** AU-5
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** Yes

**AU.L2-3.3.5** — 3.3.5 — *5 points*

> Correlate audit record review, analysis, and reporting processes for investigation and response to indications of unlawful, unauthorized, suspicious, or unusual activity.

- **NIST SP 800-53 mapping:** AU-6(1), AU-6(3)
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** No (3- or 5-point)

**AU.L2-3.3.6** — 3.3.6 — *1 point*

> Provide audit record reduction and report generation to support on-demand analysis and reporting.

- **NIST SP 800-53 mapping:** AU-7
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** Yes

**AU.L2-3.3.7** — 3.3.7 — *1 point*

> Provide a system capability that compares and synchronizes internal system clocks with an authoritative source to generate time stamps for audit records.

- **NIST SP 800-53 mapping:** AU-8
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** Yes

**AU.L2-3.3.8** — 3.3.8 — *1 point*

> Protect audit information and audit logging tools from unauthorized access, modification, and deletion.

- **NIST SP 800-53 mapping:** AU-9
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** Yes

**AU.L2-3.3.9** — 3.3.9 — *1 point*

> Limit management of audit logging functionality to a subset of privileged users.

- **NIST SP 800-53 mapping:** AU-9(4)
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** Yes

### Configuration Management (CM)

**CM.L2-3.4.1** — 3.4.1 — *5 points*

> Establish and maintain baseline configurations and inventories of organizational systems (including hardware, software, firmware, and documentation) throughout the respective system development life cycles.

- **NIST SP 800-53 mapping:** CM-2, CM-6, CM-8, CM-8(1)
- **CIS Controls v8:** CIS 1, 2, 4
- **POA&M eligibility:** No (3- or 5-point)

**CM.L2-3.4.2** — 3.4.2 — *5 points*

> Establish and enforce security configuration settings for information technology products employed in organizational systems.

- **NIST SP 800-53 mapping:** CM-6
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** No (3- or 5-point)

**CM.L2-3.4.3** — 3.4.3 — *1 point*

> Track, review, approve or disapprove, and log changes to organizational systems.

- **NIST SP 800-53 mapping:** CM-3
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** Yes

**CM.L2-3.4.4** — 3.4.4 — *1 point*

> Analyze the security impact of changes prior to implementation.

- **NIST SP 800-53 mapping:** CM-4
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** Yes

**CM.L2-3.4.5** — 3.4.5 — *5 points*

> Define, document, approve, and enforce physical and logical access restrictions associated with changes to organizational systems.

- **NIST SP 800-53 mapping:** CM-5
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** No (3- or 5-point)

**CM.L2-3.4.6** — 3.4.6 — *5 points*

> Employ the principle of least functionality by configuring organizational systems to provide only essential capabilities.

- **NIST SP 800-53 mapping:** CM-7
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** No (3- or 5-point)

**CM.L2-3.4.7** — 3.4.7 — *5 points*

> Restrict, disable, or prevent the use of nonessential programs, functions, ports, protocols, and services.

- **NIST SP 800-53 mapping:** CM-7(1)
- **CIS Controls v8:** CIS 4, 16
- **POA&M eligibility:** No (3- or 5-point)

**CM.L2-3.4.8** — 3.4.8 — *5 points*

> Apply deny-by-exception (blacklisting) policy to prevent the use of unauthorized software or deny-all, permit-by-exception (whitelisting) policy to allow the execution of authorized software.

- **NIST SP 800-53 mapping:** CM-7(4), CM-7(5)
- **CIS Controls v8:** CIS 2
- **POA&M eligibility:** No (3- or 5-point)

**CM.L2-3.4.9** — 3.4.9 — *1 point*

> Control and monitor user-installed software.

- **NIST SP 800-53 mapping:** CM-11
- **CIS Controls v8:** CIS 2
- **POA&M eligibility:** Yes

### Identification and Authentication (IA)

**IA.L2-3.5.1** — 3.5.1 — *5 points*

> Identify system users, processes acting on behalf of users, and devices.

- **NIST SP 800-53 mapping:** IA-2, IA-5
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** No (3- or 5-point)

**IA.L2-3.5.2** — 3.5.2 — *5 points*

> Authenticate (or verify) the identities of users, processes, or devices, as a prerequisite to allowing access to organizational systems.

- **NIST SP 800-53 mapping:** IA-2, IA-5
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** No (3- or 5-point)

**IA.L2-3.5.3** — 3.5.3 — *5 points* Variable: 5 points if not implemented for any users; 3 points if only remote/privileged users.

> Use multifactor authentication for local and network access to privileged accounts and for network access to non-privileged accounts.

- **NIST SP 800-53 mapping:** IA-2(1), IA-2(2), IA-2(3)
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** No (3- or 5-point)

**IA.L2-3.5.4** — 3.5.4 — *1 point*

> Employ replay-resistant authentication mechanisms for network access to privileged and non-privileged accounts.

- **NIST SP 800-53 mapping:** IA-2(8), IA-2(9)
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**IA.L2-3.5.5** — 3.5.5 — *1 point*

> Prevent reuse of identifiers for a defined period.

- **NIST SP 800-53 mapping:** IA-4
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**IA.L2-3.5.6** — 3.5.6 — *1 point*

> Disable identifiers after a defined period of inactivity.

- **NIST SP 800-53 mapping:** IA-4(4)
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**IA.L2-3.5.7** — 3.5.7 — *1 point*

> Enforce a minimum password complexity and change of characters when new passwords are created.

- **NIST SP 800-53 mapping:** IA-5(1)
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**IA.L2-3.5.8** — 3.5.8 — *1 point*

> Prohibit password reuse for a specified number of generations.

- **NIST SP 800-53 mapping:** IA-5(1)
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**IA.L2-3.5.9** — 3.5.9 — *1 point*

> Allow temporary password use for system logons with an immediate change to a permanent password.

- **NIST SP 800-53 mapping:** IA-5(1)
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

**IA.L2-3.5.10** — 3.5.10 — *5 points*

> Store and transmit only cryptographically-protected passwords.

- **NIST SP 800-53 mapping:** IA-5(1)
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** No (3- or 5-point)

**IA.L2-3.5.11** — 3.5.11 — *1 point*

> Obscure feedback of authentication information.

- **NIST SP 800-53 mapping:** IA-6
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** Yes

### Incident Response (IR)

**IR.L2-3.6.1** — 3.6.1 — *5 points*

> Establish an operational incident-handling capability for organizational systems that includes preparation, detection, analysis, containment, recovery, and user response activities.

- **NIST SP 800-53 mapping:** IR-2, IR-4, IR-5, IR-6, IR-7
- **CIS Controls v8:** CIS 17
- **POA&M eligibility:** No (3- or 5-point)

**IR.L2-3.6.2** — 3.6.2 — *5 points*

> Track, document, and report incidents to designated officials and/or authorities both internal and external to the organization.

- **NIST SP 800-53 mapping:** IR-6
- **CIS Controls v8:** CIS 17
- **POA&M eligibility:** No (3- or 5-point)

**IR.L2-3.6.3** — 3.6.3 — *1 point*

> Test the organizational incident response capability.

- **NIST SP 800-53 mapping:** IR-3, IR-3(2)
- **CIS Controls v8:** CIS 17
- **POA&M eligibility:** Yes

### Maintenance (MA)

**MA.L2-3.7.1** — 3.7.1 — *3 points*

> Perform maintenance on organizational systems.

- **NIST SP 800-53 mapping:** MA-2
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** No (3- or 5-point)

**MA.L2-3.7.2** — 3.7.2 — *5 points*

> Provide controls on the tools, techniques, mechanisms, and personnel used to conduct system maintenance.

- **NIST SP 800-53 mapping:** MA-3, MA-3(1), MA-3(2)
- **CIS Controls v8:** CIS 4
- **POA&M eligibility:** No (3- or 5-point)

**MA.L2-3.7.3** — 3.7.3 — *1 point*

> Ensure equipment removed for off-site maintenance is sanitized of any CUI.

- **NIST SP 800-53 mapping:** MA-2
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** Yes

**MA.L2-3.7.4** — 3.7.4 — *3 points*

> Check media containing diagnostic and test programs for malicious code before the media are used in organizational systems.

- **NIST SP 800-53 mapping:** MA-3(2)
- **CIS Controls v8:** CIS 10
- **POA&M eligibility:** No (3- or 5-point)

**MA.L2-3.7.5** — 3.7.5 — *5 points*

> Require multifactor authentication to establish nonlocal maintenance sessions via external network connections and terminate such connections when nonlocal maintenance is complete.

- **NIST SP 800-53 mapping:** MA-4
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** No (3- or 5-point)

**MA.L2-3.7.6** — 3.7.6 — *1 point*

> Supervise the maintenance activities of maintenance personnel without required access authorization.

- **NIST SP 800-53 mapping:** MA-5
- **POA&M eligibility:** Yes

### Media Protection (MP)

**MP.L2-3.8.1** — 3.8.1 — *3 points*

> Protect (i.e., physically control and securely store) system media containing CUI, both paper and digital.

- **NIST SP 800-53 mapping:** MP-2, MP-4
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**MP.L2-3.8.2** — 3.8.2 — *3 points*

> Limit access to CUI on system media to authorized users.

- **NIST SP 800-53 mapping:** MP-2
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**MP.L2-3.8.3** — 3.8.3 — *5 points*

> Sanitize or destroy system media containing CUI before disposal or release for reuse.

- **NIST SP 800-53 mapping:** MP-6
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**MP.L2-3.8.4** — 3.8.4 — *1 point*

> Mark media with necessary CUI markings and distribution limitations.

- **NIST SP 800-53 mapping:** MP-3
- **POA&M eligibility:** Yes

**MP.L2-3.8.5** — 3.8.5 — *1 point*

> Control access to media containing CUI and maintain accountability for media during transport outside of controlled areas.

- **NIST SP 800-53 mapping:** MP-5
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** Yes

**MP.L2-3.8.6** — 3.8.6 — *1 point*

> Implement cryptographic mechanisms to protect the confidentiality of CUI stored on digital media during transport unless otherwise protected by alternative physical safeguards.

- **NIST SP 800-53 mapping:** MP-5(4)
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** Yes

**MP.L2-3.8.7** — 3.8.7 — *5 points*

> Control the use of removable media on system components.

- **NIST SP 800-53 mapping:** MP-7
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**MP.L2-3.8.8** — 3.8.8 — *3 points*

> Prohibit the use of portable storage devices when such devices have no identifiable owner.

- **NIST SP 800-53 mapping:** MP-7(1)
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**MP.L2-3.8.9** — 3.8.9 — *1 point*

> Protect the confidentiality of backup CUI at storage locations.

- **NIST SP 800-53 mapping:** CP-9
- **CIS Controls v8:** CIS 11
- **POA&M eligibility:** Yes

### Personnel Security (PS)

**PS.L2-3.9.1** — 3.9.1 — *3 points*

> Screen individuals prior to authorizing access to organizational systems containing CUI.

- **NIST SP 800-53 mapping:** PS-3
- **POA&M eligibility:** No (3- or 5-point)

**PS.L2-3.9.2** — 3.9.2 — *5 points*

> Ensure that organizational systems containing CUI are protected during and after personnel actions such as terminations and transfers.

- **NIST SP 800-53 mapping:** PS-4, PS-5
- **CIS Controls v8:** CIS 5
- **POA&M eligibility:** No (3- or 5-point)

### Physical Protection (PE)

**PE.L2-3.10.1** — 3.10.1 — *5 points*

> Limit physical access to organizational systems, equipment, and the respective operating environments to authorized individuals.

- **NIST SP 800-53 mapping:** PE-2, PE-5
- **POA&M eligibility:** No (3- or 5-point)

**PE.L2-3.10.2** — 3.10.2 — *5 points*

> Protect and monitor the physical facility and support infrastructure for organizational systems.

- **NIST SP 800-53 mapping:** PE-6
- **POA&M eligibility:** No (3- or 5-point)

**PE.L2-3.10.3** — 3.10.3 — *1 point*

> Escort visitors and monitor visitor activity.

- **NIST SP 800-53 mapping:** PE-3
- **POA&M eligibility:** No (1-point excluded per 32 CFR 170.21(a)(2)(iii))

**PE.L2-3.10.4** — 3.10.4 — *1 point*

> Maintain audit logs of physical access.

- **NIST SP 800-53 mapping:** PE-3
- **POA&M eligibility:** No (1-point excluded per 32 CFR 170.21(a)(2)(iii))

**PE.L2-3.10.5** — 3.10.5 — *1 point*

> Control and manage physical access devices.

- **NIST SP 800-53 mapping:** PE-3
- **POA&M eligibility:** No (1-point excluded per 32 CFR 170.21(a)(2)(iii))

**PE.L2-3.10.6** — 3.10.6 — *1 point*

> Enforce safeguarding measures for CUI at alternate work sites.

- **NIST SP 800-53 mapping:** PE-17
- **POA&M eligibility:** Yes

### Risk Assessment (RA)

**RA.L2-3.11.1** — 3.11.1 — *3 points*

> Periodically assess the risk to organizational operations (including mission, functions, image, or reputation), organizational assets, and individuals, resulting from the operation of organizational systems and the associated processing, storage, or transmission of CUI.

- **NIST SP 800-53 mapping:** RA-3
- **CIS Controls v8:** CIS 7
- **POA&M eligibility:** No (3- or 5-point)

**RA.L2-3.11.2** — 3.11.2 — *5 points*

> Scan for vulnerabilities in organizational systems and applications periodically and when new vulnerabilities affecting those systems and applications are identified.

- **NIST SP 800-53 mapping:** RA-5, RA-5(5)
- **CIS Controls v8:** CIS 7
- **POA&M eligibility:** No (3- or 5-point)

**RA.L2-3.11.3** — 3.11.3 — *1 point*

> Remediate vulnerabilities in accordance with risk assessments.

- **NIST SP 800-53 mapping:** RA-5
- **CIS Controls v8:** CIS 7
- **POA&M eligibility:** Yes

### Security Assessment (CA)

**CA.L2-3.12.1** — 3.12.1 — *5 points*

> Periodically assess the security controls in organizational systems to determine if the controls are effective in their application.

- **NIST SP 800-53 mapping:** CA-2
- **CIS Controls v8:** CIS 18
- **POA&M eligibility:** No (3- or 5-point)

**CA.L2-3.12.2** — 3.12.2 — *3 points*

> Develop and implement plans of action designed to correct deficiencies and reduce or eliminate vulnerabilities in organizational systems.

- **NIST SP 800-53 mapping:** CA-5
- **CIS Controls v8:** CIS 18
- **POA&M eligibility:** No (3- or 5-point)

**CA.L2-3.12.3** — 3.12.3 — *5 points*

> Monitor security controls on an ongoing basis to ensure the continued effectiveness of the controls.

- **NIST SP 800-53 mapping:** CA-7
- **CIS Controls v8:** CIS 18
- **POA&M eligibility:** No (3- or 5-point)

**CA.L2-3.12.4** — 3.12.4 — *1 point*

> Develop, document, and periodically update system security plans that describe system boundaries, system environments of operation, how security requirements are implemented, and the relationships with or connections to other systems.

- **NIST SP 800-53 mapping:** PL-2
- **POA&M eligibility:** No (1-point excluded per 32 CFR 170.21(a)(2)(iii))

### System and Communications Protection (SC)

**SC.L2-3.13.1** — 3.13.1 — *5 points*

> Monitor, control, and protect communications (i.e., information transmitted or received by organizational systems) at the external boundaries and key internal boundaries of organizational systems.

- **NIST SP 800-53 mapping:** SC-7
- **CIS Controls v8:** CIS 12, 13
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.2** — 3.13.2 — *5 points*

> Employ architectural designs, software development techniques, and systems engineering principles that promote effective information security within organizational systems.

- **NIST SP 800-53 mapping:** SA-8
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.3** — 3.13.3 — *1 point*

> Separate user functionality from system management functionality.

- **NIST SP 800-53 mapping:** SC-2
- **CIS Controls v8:** CIS 6
- **POA&M eligibility:** Yes

**SC.L2-3.13.4** — 3.13.4 — *1 point*

> Prevent unauthorized and unintended information transfer via shared system resources.

- **NIST SP 800-53 mapping:** SC-4
- **POA&M eligibility:** Yes

**SC.L2-3.13.5** — 3.13.5 — *5 points*

> Implement subnetworks for publicly accessible system components that are physically or logically separated from internal networks.

- **NIST SP 800-53 mapping:** SC-7
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.6** — 3.13.6 — *5 points*

> Deny network communications traffic by default and allow network communications traffic by exception (i.e., deny all, permit by exception).

- **NIST SP 800-53 mapping:** SC-7(5)
- **CIS Controls v8:** CIS 12
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.7** — 3.13.7 — *1 point*

> Prevent remote devices from simultaneously establishing non-remote connections with organizational systems and communicating via some other connection to resources in external networks (i.e., split tunneling).

- **NIST SP 800-53 mapping:** SC-7(7)
- **CIS Controls v8:** CIS 13
- **POA&M eligibility:** Yes

**SC.L2-3.13.8** — 3.13.8 — *3 points*

> Implement cryptographic mechanisms to prevent unauthorized disclosure of CUI during transmission unless otherwise protected by alternative physical safeguards.

- **NIST SP 800-53 mapping:** SC-8, SC-8(1)
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.9** — 3.13.9 — *1 point*

> Terminate network connections associated with communications sessions at the end of the sessions or after a defined period of inactivity.

- **NIST SP 800-53 mapping:** SC-10
- **POA&M eligibility:** Yes

**SC.L2-3.13.10** — 3.13.10 — *1 point*

> Establish and manage cryptographic keys for cryptography employed in organizational systems.

- **NIST SP 800-53 mapping:** SC-12
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** Yes

**SC.L2-3.13.11** — 3.13.11 — *5 points* Variable: 5 points if no encryption; 3 points if encryption is not FIPS-validated.

> Employ FIPS-validated cryptography when used to protect the confidentiality of CUI.

- **NIST SP 800-53 mapping:** SC-13
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.12** — 3.13.12 — *1 point*

> Prohibit remote activation of collaborative computing devices and provide indication of devices in use to users present at the device.

- **NIST SP 800-53 mapping:** SC-15
- **POA&M eligibility:** Yes

**SC.L2-3.13.13** — 3.13.13 — *1 point*

> Control and monitor the use of mobile code.

- **NIST SP 800-53 mapping:** SC-18
- **POA&M eligibility:** Yes

**SC.L2-3.13.14** — 3.13.14 — *1 point*

> Control and monitor the use of Voice over Internet Protocol (VoIP) technologies.

- **NIST SP 800-53 mapping:** SC-19
- **POA&M eligibility:** Yes

**SC.L2-3.13.15** — 3.13.15 — *5 points*

> Protect the authenticity of communications sessions.

- **NIST SP 800-53 mapping:** SC-23
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** No (3- or 5-point)

**SC.L2-3.13.16** — 3.13.16 — *1 point*

> Protect the confidentiality of CUI at rest.

- **NIST SP 800-53 mapping:** SC-28
- **CIS Controls v8:** CIS 3
- **POA&M eligibility:** Yes

### System and Information Integrity (SI)

**SI.L2-3.14.1** — 3.14.1 — *5 points*

> Identify, report, and correct system flaws in a timely manner.

- **NIST SP 800-53 mapping:** SI-2
- **CIS Controls v8:** CIS 7
- **POA&M eligibility:** No (3- or 5-point)

**SI.L2-3.14.2** — 3.14.2 — *5 points*

> Provide protection from malicious code at designated locations within organizational systems.

- **NIST SP 800-53 mapping:** SI-3
- **CIS Controls v8:** CIS 10
- **POA&M eligibility:** No (3- or 5-point)

**SI.L2-3.14.3** — 3.14.3 — *5 points*

> Monitor system security alerts and advisories and take action in response.

- **NIST SP 800-53 mapping:** SI-5
- **CIS Controls v8:** CIS 7
- **POA&M eligibility:** No (3- or 5-point)

**SI.L2-3.14.4** — 3.14.4 — *5 points*

> Update malicious code protection mechanisms when new releases are available.

- **NIST SP 800-53 mapping:** SI-3
- **CIS Controls v8:** CIS 10
- **POA&M eligibility:** No (3- or 5-point)

**SI.L2-3.14.5** — 3.14.5 — *3 points*

> Perform periodic scans of organizational systems and real-time scans of files from external sources as files are downloaded, opened, or executed.

- **NIST SP 800-53 mapping:** SI-3
- **CIS Controls v8:** CIS 10
- **POA&M eligibility:** No (3- or 5-point)

**SI.L2-3.14.6** — 3.14.6 — *5 points*

> Monitor organizational systems, including inbound and outbound communications traffic, to detect attacks and indicators of potential attacks.

- **NIST SP 800-53 mapping:** SI-4
- **CIS Controls v8:** CIS 13
- **POA&M eligibility:** No (3- or 5-point)

**SI.L2-3.14.7** — 3.14.7 — *3 points*

> Identify unauthorized use of organizational systems.

- **NIST SP 800-53 mapping:** SI-4
- **CIS Controls v8:** CIS 8
- **POA&M eligibility:** No (3- or 5-point)
