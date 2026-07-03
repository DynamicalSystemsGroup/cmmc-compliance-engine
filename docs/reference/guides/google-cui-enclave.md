## Part 1: Set up Google Workspace for CMMC for the CUI subset

### What you must buy

Only **Google Workspace Enterprise Plus** with the **Assured Controls Plus** add-on supports CMMC Level 2 for CUI. The cheaper Business and Enterprise Standard editions do not have the U.S. data residency and U.S. support-personnel restrictions that CUI requires.

- **Enterprise Plus license:** for every user who will handle CUI.
- **Assured Controls Plus:** add-on to enforce that CUI data stays in U.S. data centers and is only accessed by U.S.-based, background-checked Google support staff.
- **Assured Controls Plus is only available on Enterprise Plus**, so this is not optional.

### What you must configure

You are drawing a hard boundary inside your existing Workspace tenant. Here is the practical setup:

1. **Create a separate Google Workspace Organizational Unit (OU) called "CUI Enclave."**
    - Move only the CUI-handling users into this OU.
    - Leave everyone else in the standard OU.

2. **Turn off every non-FedRAMP-authorized service for the CUI OU.**
    - Google Workspace Core Services (Gmail, Drive, Docs, Sheets, Meet, Chat, etc.) are FedRAMP High authorized.
    - Many add-ons and Marketplace apps are **not**. If a CUI user can access it, it must be FedRAMP authorized.
    - In the Admin Console, go to Apps → Additional Google Services, and disable anything not on the authorized list for the CUI OU.

3. **Enable Assured Controls Plus for the CUI OU.**
    - This restricts data residency to the U.S. and limits Google support access.

4. **Enable Client-Side Encryption (CSE) for the CUI OU.**
    - CSE is available with Enterprise Plus.
    - It encrypts CUI in Gmail, Drive, Docs, Sheets, Meet, etc., so Google never holds the decryption key.
    - You must use a third-party key management partner (Google has validated partners) so you retain organizational control of the keys.
    - This directly addresses the high-weight NIST control **SC.L2-3.13.11 (FIPS-validated cryptography)** and **SC.L2-3.13.10 (key management)**.

5. **Enforce MFA with hardware security keys or TOTP for the CUI OU.**
    - Not just "available" — required for every CUI user.
    - This addresses **IA.L2-3.5.3 (MFA for privileged access)** and related controls.

6. **Restrict external sharing and configure Data Loss Prevention (DLP).**
    - Block external sharing of Drive files by the CUI OU.
    - Set DLP rules to detect and block CUI from leaving the boundary via email or Drive.

7. **Export audit logs to a FedRAMP-authorized SIEM.**
    - Workspace keeps logs for 180 days; CMMC requires 90 days online and 3 years archived.
    - Use the Reports API to export Admin, Drive, Gmail, Login, and SAML logs to a SIEM.
    - The SIEM itself must be FedRAMP Moderate or higher if it holds CUI-related log data.

8. **Document everything in the SSP.**
    - You need Google's Customer Responsibility Matrix (CRM), which shows which controls Google inherits and which you must implement.
    - Request this from your Google Workspace sales representative or Google Cloud representative.

### Important limitation: Google Workspace is NOT IL5

Google Workspace collaboration apps (Gmail, Drive, Meet, etc.) are authorized at **IL4**, not IL5. If the DAF contract (NV018) requires an IL5 platform, or if any work involves ITAR-controlled technical data, Google Workspace is **not sufficient** by itself. In that case, you would need:

- **Microsoft 365 GCC High** (the standard IL5/ITAR platform), or
- A separate Google Cloud infrastructure enclave built to IL5, with Workspace used only for non-IL5 collaboration.

For the DLA proposals (NV011, NV012), IL4 CUI is likely the ceiling, so Workspace with Assured Controls Plus is viable. For NV018, verify whether the topic truly requires IL5 collaboration or only IL5 hosting of the application workload.

---

## Part 2: Take stock of everything inside the CUI boundary

Since only a subset of your 20 people will handle CUI, you can limit the CMMC boundary to **that subset plus the systems they touch**. This reduces cost and complexity dramatically.

### Step 1: Name the people

Create a list of every DSG employee who will:

- Receive, create, edit, store, or send CUI.
- Administer systems that hold CUI.
- Support the CUI users (IT, security, help desk).
- Be named in the proposal as key personnel.

Mark everyone else as **out of scope** and document that they cannot access CUI systems.

### Step 2: List every device those people use

For each CUI user, list:

- Work laptop (make, model, serial number, OS version).
- Work phone or tablet.
- Any monitor, docking station, or peripheral used with CUI.
- Home office equipment if they will work remotely with CUI.

Do not let CUI users use personal devices for CUI. If a device is shared between CUI and non-CUI work, it is in scope.

### Step 3: List every account those people have

For each CUI user, list:

- Their Google Workspace account in the CUI OU.
- Any other cloud accounts (AWS, Azure, Google Cloud, GitHub, etc.) that can access CUI.
- Any shared or service accounts they administer.
- VPN or zero-trust access accounts.

### Step 4: List every application and service that touches CUI

Ask: where does CUI live, move, or get processed?

- **Email:** Gmail (CUI OU only).
- **File storage:** Google Drive (CUI OU only).
- **Documents:** Google Docs, Sheets, Slides.
- **Meetings:** Google Meet if CUI is discussed.
- **Code repositories:** GitHub/GitLab if CUI is in code or documentation.
- **Development environments:** cloud VMs, IDEs, databases.
- **Project management tools:** Jira, Asana, Linear.
- **Communication:** Slack, Teams, Google Chat.
- **Subcontractors or vendors:** anyone outside DSG who will see CUI.

If a service is not FedRAMP authorized and it touches CUI, it must be removed from the CUI boundary or replaced.

### Step 5: Map how CUI enters and exits

Draw a simple data flow diagram:

1. **Entry points:** Where does CUI come from? DoD portal, email from contracting officer, shared drive from prime contractor, uploaded dataset, etc.
2. **Processing:** Where is it used? Docs, spreadsheets, code, models, meetings.
3. **Storage:** Where does it rest? Drive, databases, cloud storage.
4. **Exit points:** Where does it go? Reports back to DoD, shared with subcontractor, archived, deleted.

Every arrow on this diagram is in scope.

### Step 6: Identify the network boundary

- Is CUI accessed from the office, home, or both?
- What network does the traffic travel over?
- Is there a VPN, zero-trust gateway, or VDI?
- Is Wi-Fi segmented or open?

If CUI users work from home, their home network and router are part of the boundary unless they use a VDI or corporate-managed device that prevents local storage.

### Step 7: Document physical locations

If CUI can be stored or viewed on a laptop, the physical location where that laptop is used matters. List:

- DSG office address.
- Approved remote work locations for CUI users.
- Any facility where CUI might be printed or discussed.

### Step 8: Put it all in the SSP

Your System Security Plan should have these sections:

- **CUI boundary statement:** who, what, where, and why.
- **Asset inventory:** devices, accounts, services, applications.
- **Network diagram:** CUI enclave, out-of-scope systems, data flows.
- **Data flow diagram:** entry, processing, storage, exit.
- **Roles and responsibilities:** who owns each control.
- **Evidence references:** screenshots, config exports, policy links.

---

## Practical short checklist for this week

1. Contact your Google Workspace sales rep and ask for:
    - Enterprise Plus pricing for CUI users.
    - Assured Controls Plus pricing.
    - The **Customer Responsibility Matrix (CRM)** for CMMC.
    - The **Google Workspace CMMC Implementation Guide**.

2. Create the **"CUI Enclave" OU** in your existing Workspace tenant and move the CUI users into it.

3. Disable all non-FedRAMP-authorized services for the CUI OU.

4. Make a list of the CUI users, their devices, and every app they use.

5. Decide whether IL5 or ITAR applies to any of the three proposals. If yes, begin evaluating Microsoft 365 GCC High instead of relying solely on Google Workspace.

6. Request a quote from a CMMC consultant or Google partner to validate the configuration, especially if no one at DSG has done this before.
