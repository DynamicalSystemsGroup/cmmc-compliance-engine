# DLA26BZ03-NV011 — Topic Q&A

**Topic:** Digital Twin of the Organization for Enhanced Mission Readiness  
**Solicitation:** [DoD SBIR/STTR Topics](https://www.dodsbirsttr.mil/topics-app/)  
**Q&A Period:** 06/24/2026 – 07/22/2026  
**Primary End-User:** DLA Finance (J8)

---

## June 4, 2026

### Q1 — Will DLA provide a set of contract data for the proof-of-concept?

**Answer:** We are currently working with our Legal and Contracting to ensure the NDA we were planning to use is sufficient. The data is restricted and requires an NDA/Data Use restriction agreement before being shared.

---

## June 11, 2026

### Q2 — How can we get in contact with the TPOCs?

**Answer:** With this topic there are multiple groups that need to be involved in the coordination for answering technical questions. As such we are planning to hold set hours/times where the TPOCs are available and can answer questions. With the type of questions we are getting and information/data that needs to be provided an NDA/Data use agreement needs to be signed prior to releasing or sharing most of the information we are being asked. As such, please email the TPOCs to get the NDA/Data use agreement and once signed and returned a registration link will be provided. The current date/times we have available for the TPOCs and additional SMEs to help answer the questions are 06/23/2026 14:00-15:30 EST.

---

## June 30, 2026

### Q3 — NDA/Data Use Agreement process after the 06/23 session

**Question:** Referencing the 06/11/2026 response regarding TPOC availability and the NDA/Data Use Agreement required to access restricted topic information: the 06/23/2026 session has now passed. Could DLA please confirm the current process and point of contact for obtaining and executing the NDA/Data Use Agreement along with any subsequent steps to access the associated information? This access is needed to accurately scope our Phase I feasibility approach.

**Answer:** Response Pending

---

## July 1, 2026

### Q4 — Methodology vs. technical tool scope

**Question:** Given that DLA currently has no formal procedures for vendor economic dependency assessment, should Phase I proposals address the development of a repeatable methodology and documentation framework alongside the technical tool, or is the procedural development considered a separate workstream outside the scope of this topic?

**Answer:** Phase I proposals should focus primarily on demonstrating the technical feasibility of the automated tool itself rather than establishing a separate workstream to develop DLA's formal procedures or documentation frameworks. DLA will not be providing existing SOPs and expects the Phase I effort to focus on delivering a functional technical tool using the provided synthetic EBS data, SEC Edgar, and Sam.gov datasets. Proposers must still outline the underlying logic and methodology of their proposed software to prove the feasibility of automating SFFAS 47 compliance, but the formal development of DLA's internal standard operating procedures and organizational policy frameworks is a separate, government-led workstream outside the scope of this R&D Phase I.

---

### Q5 — Why SBIR instead of a sources sought for COTS?

**Question:** If the interest is in Commercial Off the Shelf (COTS) Dual Use, is there a reason DLA is going with a SBIR as opposed to a sources sought?

**Answer:** Our pursuit of Commercial Off-the-Shelf (COTS)/Dual Use solutions is structurally bound to the dual-use mandate of the SBIR program, which allows us to fund the crucial bridge between a private-sector commercial tool and DLA's unique defense requirements. By utilizing the SBIR program, DLA can financially support this "military adaptation" process during Phases I/II, enabling the contractor to build a highly sustainable, dual-use technology that not only solves critical logistical readiness challenges for the Warfighter but also remains commercially viable in the private sector for corporate supply chain risk management and financial compliance.

---

### Q6 — Why COTS instead of internally built?

**Question:** Is there a reason the TPOCs are going COTS versus internally built software?

**Answer:** This capability is a common requirement across many DoD components and federal agencies. Therefore, we are seeking to evaluate existing commercial-off-the-shelf (COTS)/Dual use and mature market solutions before incurring the high development and sustainment costs of building a custom government-owned system.

---

### Q7 — Audit-ready evidence packages

**Question:** For Phase I, would DLA value an audit-ready evidence package for each dependency finding that shows source data, calculation basis, public-data coverage gaps, AI-assisted judgments, human analyst attestation, and reviewer traceability, especially for privately held vendors where definitive revenue data may not be available?

**Answer:** Yes. We highly value any proposal that delivers robust, audit-ready evidence packages. Proving that the tool's outputs are explainable, traceable, and capable of satisfying rigorous audit scrutiny is a primary focus of our technical evaluations.

---

### Q8 — Golden dataset for DLA testing

**Question:** Are we expected to give you a golden dataset for your own testing?

**Answer:** Not for Phase I feasibility, just that it is possible and how. The Golden Dataset will not be provided, but once awarded in Phase I access to the necessary EBS data for one will be provided to enable. _(Corrected misstatement from the live Q&A.)_

---

### Q9 — TRL 7/8 vs. greenfield software

**Question:** Does the TRL 7/8 target for Phase I imply that DLA is not interested in Greenfield Software (i.e., a new solution)?

**Answer:** Greenfield solutions are not prohibited and will be fully evaluated. However, DLA maintains a strong preference for commercially mature/dual use technologies that can be rapidly integrated, as this significantly reduces transition timelines and costs.

---

### Q10 — Live EBS API or sample data only?

**Question:** Could you please confirm whether Phase I is expected to include an API connection with DLA EBS, or whether working with the provided sample data will be sufficient?

**Answer:** No live API connection to EBS is permitted during Phase I. Proposers must demonstrate feasibility strictly utilizing the provided sample contract data and public datasets.

---

### Q11 — Risk assessment by contract type

**Question:** I wanted to ask specifically about assessing risk based on contract type, the cost reimbursement versus fixed rate contracts. How do you anticipate risk being assessed differently depending on contract type or how would you recommend we think about that?

**Answer:** We recommend reviewing the Federal Acquisition Regulation (FAR) sections regarding contract types (e.g., cost-plus, fixed-price with progress payments). This will provide a solid foundation for defining how contract structures shift financial risk and how the scoring rubric should weight these variables.

---

### Q12 — Configurable dependency thresholds

**Question:** Is Phase I expected to deliver a single hardcoded dependency threshold, or should the framework allow analysts to adjust and test multiple threshold levels?

**Answer:** The framework must not use a single hardcoded threshold. To ensure long-term durability and flexibility across shifting policies, the tool must feature a configurable engine that allows analysts to dynamically input and test various threshold ranges.

---

### Q13 — TRL requirements for Phase I and Phase II

**Question:** Does DLA have a minimum Technology Readiness Level requirement for Phase I proposals, and what TRL is expected at the conclusion of Phase II?

**Answer:** DLA prefers solutions with a high baseline Technology Readiness Level (TRL 7 or 8) — specifically, commercially viable platforms that are dual use, requiring customization and integration rather than raw, greenfield software development.

---

### Q14 — Entity resolution on synthetic vs. real data

**Question:** If the EBS sample is synthetic and deliberately will not resolve to real SEC registrants or SAM.gov entities, does DLA expect the Phase I proof-of-concept to demonstrate the dependency logic on the synthetic set while demonstrating entity resolution and EDGAR/SAM retrieval separately against real public companies, or does DLA intend to seed the synthetic vendor records with names that correspond to real public filers so the full pipeline can run end-to-end against one dataset?

**Answer:** The representative Phase I EBS dataset is de-identified, meaning that to run a complete end-to-end demonstration, the proposer must demonstrate the ability to align and join these schemas programmatically. Proposers are expected to show how they can map index keys across both synthetic internal records and real public filings to construct a complete, synchronized data pipeline. As you advance through the phases, you will work closely with J6 to migrate these pipelines onto our secure networks and obtain an Authority to Operate (ATO). The ATO process typically takes 12 to 18 months to navigate, which should be factored into your Phase II transition schedule.

---

### Q15 — System owner for the tool's output

**Question:** Beyond the audit review that prompted this topic, is there a specific DLA finance office or directorate that will own the tool's output once it exists?

**Answer:** DLA Finance (J8) will be the primary system owner of the tool's output.

---

### Q16 — Private capital and SFFAS 47 reporting

**Question:** A lot of startups take venture capital and also there's PE backing different things like that. So for a non publicly traded company that does have other forms of capital coming from outside of contracts, does that change the health reporting within this accounting standard?

**Answer:** SFFAS 47 is a federal reporting standard that regulates what the federal reporting entity (DLA) must disclose regarding its related parties and dependent vendors. Private capital structures, venture backing, or private debt are outside the direct scope of SFFAS 47 disclosures, though they may be valuable secondary indicators of overall vendor financial health.

---

### Q17 — Vendor revenue denominator for non-public entities

**Question:** You clarified parent-level reporting and gross (not segmental) revenue. But the hard part remains: a vendor's total gross revenue comes from their 10-K, while the DLA-derived numerator comes from EBS. Does DLA expect the denominator (vendor total revenue) to come only from public filings, or is a vendor with no public filing simply scored as "indeterminate" with a confidence flag?

**Answer:** For SEC-registered public companies, the total gross revenue denominator must be extracted programmatically from their public 10-K filings. For privately held and foreign entities where public SEC filings do not exist, a core requirement of your Phase I feasibility study is to propose, test, and document alternative methodologies (such as web-scraping audited statements or integrating third-party APIs) to resolve this denominator and estimate risk.

---

### Q18 — Current manual processes

**Question:** Can you go deeper into the problem set? What manual processes does DLA have that it is looking to automate?

**Answer:** Currently, DLA Finance has no formalized, automated system to track related-party or dependent-vendor transactions, relying instead on small-scale, manual research. The goal of this SBIR topic is to evaluate the feasibility of building an automated, repeatable tool to execute this screening across our entire Working Capital Fund vendor pool.

---

### Q19 — Who adjudicates flagged dependencies?

**Question:** Once the tool produces a flag, who adjudicates it operationally — a J8 financial statement preparer or a supply chain risk analyst? Knowing the consumer shapes the evidence package we design.

**Answer:** The tool's output will be utilized in a dual-view environment. Operational adjudication will be a collaborative process between J8 Finance (for audit disclosure compliance) and J7 Acquisition/Procurement (for supply chain risk management).

---

### Q20 — Data formatting challenges

**Question:** Are the formatting challenges in the sample mostly entity-name normalization, or do they also include missing CAGE/DUNS, duplicate vendor records, or inconsistent units?

**Answer:** The sample EBS dataset includes realistic formatting discrepancies, such as inconsistent document numbering or duplicate names, which reflect standard data system transitions. While CAGE or DUNS numbers should be fully populated within the standard EBS Table _(specific table is CUI — sign NDA/Data use agreement to obtain the dataset and questions specific to the dataset)_, normal formatting challenges should be expected and handled.

---

### Q21 — The 10% concentration threshold

**Question:** Is the 10% concentration threshold measured against the vendor's total revenue, a business segment, or DLA obligations in a fiscal year, and does the tool need to handle multi-year trends or just a point-in-time snapshot?

**Answer:** The threshold is a point-of-time snapshot measured against the vendor's gross revenue. It does not measure obligations alone, as obligations do not directly equate to realized vendor revenue.

---

### Q22 — Usability vision

**Question:** How do you envision this? I know there's meant to be this data set at the end, but the actual usability of a program I assume is either going to be individual entities being run or bulk uploads and then mass outputs. Do you see this part of AI? I'm asking a little bit more about the estimated usability and what that looks like from your end.

**Answer:** The Phase I feasibility study will help shape the ultimate system's design. We anticipate the standard workflow will involve a large-scale batch upload of vendor datasets at scheduled reporting intervals, followed by point-of-time maintenance queries. The exact usability and system design options will be evaluated based on the results of your Phase I proposals.

---

### Q23 — Assessment level: entity vs. ultimate parent

**Question:** Should economic dependency be assessed at the contracting-entity level, the ultimate-parent level, or both? A subsidiary's DLA revenue may be immaterial to the parent that files the 10-K.

**Answer:** If a company reports at the parent level, disclosures are typically consolidated in their public SEC filings. Our primary focus is identifying dependency at this higher reporting level to ensure alignment with standard SFFAS 47 reporting entity requirements, which focus on gross consolidated revenue disclosures rather than microscopic segment breakdowns.

---

### Q24 — TRANSCOM integration

**Question:** How does this solution integrate into TRANSCOM?

**Answer:** There is currently no planned integration with TRANSCOM. If there is a specific technical or data-sharing requirement driving this question, please submit a formal clarification request through the DSIP portal.

---

### Q25 — Definition of success

**Question:** What does success look like? If this works, what changes for the operator on day one?

**Answer:** Success on day one means J8 Finance transitions from completely manual, ad-hoc research to an automated, standardized baseline. Analysts will have a dedicated compliance tool to generate, analyze, and justify SFFAS 47 dependency flags, establishing a reliable, auditable process for year-end reporting.

---

### Q26 — Canonical identifiers and entity resolution

**Question:** Is there a canonical identifier (CAGE, UEI, DUNS) populated in the provided dataset that we can rely on for matching DLA vendor records to SEC registrants and SAM.gov entities, or is fuzzy entity resolution itself part of what Phase I needs to demonstrate?

**Answer:** The sample DLA EBS dataset provided for Phase I is unclassified, de-identified representative data, meaning it will not naturally align line-by-line with real live public filings. Therefore, demonstrating a robust entity-resolution methodology — specifically identifying key index mapping layers (such as DUNS, CAGE, or EIN fields) and showing how to normalize, clean, and join these across disparate schemas — is a core technical requirement that Phase I proposals must address.

---

### Q27 — Related-party signals beyond revenue concentration

**Question:** For the related-party half of SFFAS 47, what signals in EBS or public data would DLA consider sufficient evidence of a control relationship, as opposed to just a revenue concentration ratio?

**Answer:** DLA is currently evaluating potential indicators of control and shared influence. While revenue concentration is our primary baseline filter, the exact rules and signals used to determine formal related-party status under SFFAS 47 will be defined and modeled based on the results of the Phase I feasibility study. Proposers are encouraged to consult the [official FASAB SFFAS 47 handbook](https://files.fasab.gov/pdffiles/handbook_sffas_47.pdf) to identify best-practice control and ownership signals.

---

### Q28 — Historical contract data

**Question:** Should the Phase I proposal address how the tool would handle historical contract data for prior fiscal years, or is the scope limited to current and prospective assessments?

**Answer:** The immediate scope of Phase I is limited to current, point-in-time financial assessments.

---

### Q29 — External data sources

**Question:** Which external public data sources are most relevant for Phase I — SEC EDGAR, SAM.gov, USASpending.gov, or a combination of all three?

**Answer:** The primary external sources of interest are SAM.gov and SEC EDGAR, combined with DLA's internal ERP (EBS) data. While USASpending.gov contains high-level downstream federal award data, it represents highly aggregated historical information that is less critical for the point-in-time, vendor-specific SFFAS 47 reviews required for this use case.

---

### Q30 — FOUO / CUI SAM.gov access

**Question:** Will DLA facilitate access to FOUO and/or sensitive (CUI) data from SAM.gov during Phase I?

**Answer:** SAM.gov registration data is publicly available, though certain fields require standard login credentials. DLA will not need to facilitate proprietary access for standard SAM.gov queries.

---

### Q31 — SOPs and process documentation

**Question:** What documentation that includes SOPs and process documentation will be provided?

**Answer:** DLA will not be providing existing SOPs or process maps. A key objective of your Phase I feasibility study is to suggest and model these very compliance workflows. The data and analytical outputs produced by the prototype will be used to help DLA J8 develop the Standard Operating Procedures required for the final system.

---

### Q32 — End user and requiring activity

**Question:** Who is the end user and the requiring activity behind this topic, and what triggered it being written now? Is there a specific program office or site waiting on a solution?

**Answer:** The requiring activity and primary end-user is DLA Finance (J8). The immediate operational trigger is the drive toward a clean, unqualified audit opinion. Further specific information is considered CUI and would only be available after NDA/Data use is signed or award.

---

### Q33 — DCAA / DCMA vendor data

**Question:** Will we have (or need) access to any DCAA or DCMA vendor data?

**Answer:** Phase I feasibility does not require access to DCAA or DCMA datasets. However, if your technical approach demonstrates a clear, justifiable requirement for this data (e.g., pulling data from MOCAS for contract administration), please document this justification within your technical proposal. DLA can evaluate facilitating read-only or extract-based access in later phases if technically necessary.

---

### Q34 — Anomaly detection scope

**Question:** Should anomalies be statistical, behavioral, financial, or supply-chain based? And should the model detect gradual changes or only sudden spikes?

**Answer:** Our primary focus is point-of-time compliance and risk assessment based on SFFAS 47 disclosures. Broad, multi-dimensional behavioral or supply-chain anomaly modeling is outside the primary scope of Phase I. However, identifying and mapping data gaps, such as sudden shifts or missing filings in historical records, is highly valuable and should be documented as part of the overall gap and feasibility analysis.

---

### Q35 — Output formats

**Question:** What output formats does DLA J8 require — for example an interactive dashboard for daily analyst use, a structured PDF for independent auditors, or data exports for financial reconciliation?

**Answer:** The primary requirement is an interactive dashboard capable of producing actionable insights to drive leadership decisions and audit analysis. While J8 is highly receptive to evaluating various proposed formats during Phase I, the focus should remain on delivering actionable information rather than static data reporting. We will evaluate the utility of different formats (e.g., structured PDFs, flat-file exports) during the feasibility review.

---

### Q36 — Data classification and security requirements

**Question:** What classification level will vendor financial and transaction data be handled at? Will the tool operate on a classified network (e.g., NIPRNet/SIPRNet), and are there FedRAMP, CMMC, or other compliance frameworks that must be met from day one?

**Answer:** All contract, financial, and transaction data utilized for this use case resides on unclassified networks (NIPRNet). For cloud-based processing, the solution must meet a minimum of DoD Impact Level 5 (IL-5) security requirements. Additionally, CMMC compliance is a contractual requirement for this topic; the awardee must achieve a minimum of CMMC Level 2 (Self-Attestation) prior to contract award, as it is a condition of the award.

---

### Q37 — Current related-party identification process

**Question:** What is DLA's current process for identifying related parties under SFFAS 47, and have prior audit findings identified specific gaps that this tool is expected to close?

**Answer:** The current process is manual and requires automation to expand the applicability to meet the requirements of SFFAS 47. Further background and information on this is considered CUI and would require an NDA/Data use agreement prior to sharing or can be shared after award.

---

### Q38 — Enterprise AI models and hosting

**Question:** Do you have any enterprise AI models or licenses already in place, and is there a preference for locally hosted inference versus external APIs, given data boundary and operating cost considerations?

**Answer:** DLA is actively prioritizing in-house, government-hosted cloud platforms for our enterprise AI capabilities. Our core cloud environments are hosted on _(CUI — available after signed NDA/Data use agreement)_. To facilitate rapid integration, DLA utilizes intermediate development platforms to support systems working toward an Authority to Operate (ATO).

---

### Q39 — Sample contract structures and schemas

**Question:** Will DLA provide any sample contract structures or metadata schemas during Phase I to ensure the prototype is architecturally compatible with DLA's internal systems?

**Answer:** Yes. De-identified sample contract structures, metadata schemas, and representative database tables reflecting DLA EBS views will be provided to Phase I awardees once requested and a standard NDA/Data Use is executed or after award.

---

### Q40 — Additional public data sources

**Question:** To clarify, for Phase I, would proposing to test the feasibility of including other public data sources be viewed negatively? In other words, should the Phase I proposal strictly limit to EDGAR, SAM.gov, and the provided DLA business data?

**Answer:** Proposing to test the feasibility of additional public data sources is within scope. However, we highly recommend prioritizing EDGAR, SAM.gov, and the provided DLA sample data, as these represent the core systems currently used by our team.

---

### Q41 — SFFAS 47 as the sole anchor

**Question:** Should we anchor the Phase I criteria strictly to SFFAS 47, or also draw on the related standards and frameworks the topic references?

**Answer:** The primary and non-negotiable anchor for this effort remains SFFAS 47. You may draw on the related accounting frameworks and standards referenced in the topic description to the extent that they enhance the tool's capacity to deliver the required SFFAS 47 outputs during Phase I.

---

### Q42 — Vendor self-reported data

**Question:** Is there a need/opportunity to use verifiable vendor reported data in addition to public or DLA data sources? This might be a way to fill some of those data gaps if we are allowed to ask vendors to participate.

**Answer:** We appreciate this thoughtful approach to addressing data coverage gaps. Proposing a mechanism for voluntary, secure vendor self-reporting is acceptable if it enhances the overall solution and complies with all security and explainability guidelines. However, please note that introducing direct vendor-reporting portals adds complexity regarding Cybersecurity Maturity Model Certification (CMMC) flow-down requirements. CMMC clauses are contractually required for any system handling CUI (with Level 2 self-attestation being the minimum requirement for systems processing sensitive data), which must be accounted for in your architecture.

---

### Q43 — Data access during Phase I

**Question:** To what extent will access be given to data for Phase I?

**Answer:** Performers will have unrestricted access to public datasets during Phase I. Access to internal DLA systems will be restricted to the provided, de-identified flat-file sample datasets; full or broad network access to production databases will not be granted. Direct integration and access to live internal datasets will be deferred to Phase II. The dataset is considered CUI and requires an NDA/Data use agreement.

---

### Q44 — Prohibited model types

**Question:** Are there prohibited model types (e.g., deep neural nets, LLMs, external APIs)?

**Answer:** There are no explicit prohibitions on model types, but there are strict security constraints. For API connections, proposers must account for safeguarding Controlled Unclassified Information (CUI). Data in transit represents a high-risk security vector; therefore, if your architecture connects to external systems (such as subcontractors or partner platforms), you must guarantee that the CUI-compliant data boundary is maintained end-to-end across all connectors. Regarding Large Language Models (LLMs), DLA J8 currently utilizes secure, government-tenant models, which represents our baseline platform standard. Specific models and IT infrastructure may be shared after NDA is signed and received or after award.

---

### Q45 — EBS scope vs. DIBBS

**Question:** For Phase I, should we focus on EBS financial and procurement views, or should DIBBS or other DLA procurement systems also be considered in scope?

**Answer:** For Phase I, the scope should be restricted to DLA EBS data alongside the public SEC EDGAR and SAM.gov datasets. While proposers may suggest incorporating DIBBS data if they believe it improves their solution, please note that the majority of critical contract data from DIBBS is already duplicated and natively stored within EBS.

---

### Q46 — Golden dataset expectations

**Question:** The topic asks for an established golden dataset. Do you have any expectations for how big it should be, what it should cover, or how the correct answers in it should be validated?

**Answer:** The dataset must be comprehensive enough to satisfy SFFAS 47 compliance testing. Specifically, the golden dataset should contain a large enough cohort of sample vendors to demonstrate that your feasibility model successfully flags dependent entities and handles various edge cases (such as data formatting gaps). Regarding validation, the outputs must feature absolute explainability and transparency to satisfy downstream financial auditors. The prototype must clearly demonstrate how and why it arrived at each determination, providing a visible audit trail that proves to SFFAS 47 auditors that DLA's economic-dependency evaluations are complete and sufficient.

---

### Q47 — Oral presentation format

**Question:** The solicitation references an oral presentation for highly acceptable proposals. Can you describe the format and whether the presenting team is expected to include technical and business personnel or primarily the PI?

**Answer:** The composition of the presentation team is entirely at the discretion of the offering vendor. Proposers should make their own business decision regarding which technical, management, or executive personnel best represent their proposed solution.

---

### Q48 — Evaluation weighting

**Question:** Can you confirm whether technical merit, commercialization potential, and team qualifications are weighted equally, or does DLA apply differential weighting for this topic?

**Answer:** Evaluations are not based on mathematical weights but on an assessment of the overall proposed technical approach. Consistent with other research and development solicitations, proposals are evaluated individually on their own technical merit rather than scored or ranked against one another.

---

### Q49 — Greatest technical challenges

**Question:** What do you see as the greatest technical challenges in this solicitation? Where are proposals most likely to fall short or where do you see Phase I performers not meeting the bar to transition to Phase II?

**Answer:** No answer was provided, as doing so would cross into defining specific technical solutions rather than clarifying government requirements.

---

### Q50 — Golden dataset contents

**Question:** What does DLA envision being included in the "established golden dataset"?

**Answer:** The golden dataset will be seeded by the representative, unclassified DLA sample contract data that is available upon request (following NDA execution). This internal dataset will be combined with corresponding entity registration records from SAM.gov and financial statement filings from the SEC EDGAR system to establish an end-to-end, multi-source reference baseline.

---

### Q51 — Private vendors without public filings

**Question:** For vendors that have no publicly available financial filings, such as privately held companies or foreign entities, does DLA expect the tool to document those as gaps with an explanation, identify an alternative data source, or exclude them from scope entirely?

**Answer:** The intent is to evaluate the feasibility of capturing financial data for these entities from alternative public sources, such as audited statements published on corporate websites. Any data coverage gaps must be fully documented and explained so they can be incorporated into the feasibility report or future requirements. For web-scraped or multi-source public data, the tool should implement a confidence score or data reliability index. While "something is better than nothing" for risk assessments, the system must clearly flag potential data gaps while displaying the retrieved alternative data from secondary sources.

---

### Q52 — Additional data sources beyond Phase I

**Question:** Is there an expectation or desire to leverage many additional or different sources of data?

**Answer:** The previously mentioned datasets (EBS, SEC EDGAR, SAM.gov) will be sufficient for Phase I feasibility, as they represent our core requirements. Once Phase I is complete, we may explore expanding the data scope. Phase I is focused on identifying available solutions and testing their initial implementation within the established schedule and budget. Decisions regarding follow-on data integrations will be determined based on DLA's evolving needs.

---

### Q53 — Operating environment

**Question:** What operating environment is the tool expected to be built for or deployed within? For example, should offerors assume a Government-hosted, or other approved restrictive environment?

**Answer:** The expectation for Phase I is that you will build and demonstrate the prototype within an offeror-hosted, CUI-compliant environment. Phase II will require migrating the solution into DLA's managed environment, architecture, and technology stack. Given the sensitivity of the vendor and contract data, the production environment will require a DoD Impact Level (IL) 5 or higher hosting authorization. Further DLA IT environment data is considered CUI and would have to be shared after NDA signed and received or after award.

---

### Q54 — Authoritative data systems

**Question:** The description calls for integration with DLA's business systems to identify significant vendor relationships. Which authoritative systems hold the contract and transaction data we'd draw on (EBS, EProcurement, the data lake / Advana), and at what stage would we get access to representative data?

**Answer:** The primary authoritative systems involved are SEC EDGAR, SAM.gov, and DLA's ERP system (EBS). Note that there are some discrepancies between standard ERP technical field names and DLA-specific labels. These differences will be visible in the sample dataset provided upon request once a signed NDA is executed. While systems like PIEE may be worth exploring, they are only applicable in Phase II. Access timelines for internal networks depend entirely on J6 IT security personnel, and while we work to facilitate this as quickly as possible, we cannot provide a definitive timetable at this stage. For specific ERP information, it will have to be shared after NDA is executed due to the CUI nature of the IT infrastructure.

---

### Q55 — Scope: economic dependency vs. related party

**Question:** Is the scope of this topic limited to economic dependency determination, or is it also about related party determination more broadly?

**Answer:** Broadly speaking, it encompasses related-party determinations, but we are specifically focused on how to determine the economic dependency component. Therefore, the primary focus of Phase I is demonstrating the technical feasibility of making that specific determination.

---

### Q56 — The 10% revenue threshold

**Question:** The topic mentions using something like the percentage of a vendor's revenue that comes from DLA. Is there a specific percentage threshold you have in mind, or is figuring out the right threshold part of what you want us to deliver in Phase I?

**Answer:** The threshold is primarily derived from commercial accounting standards. For example, the commercial accounting standard for segment reporting (FASB ASC 280) sets a 10% materiality threshold. Specifically, if a company derives 10% or more of its revenue from a single customer, that relationship must be disclosed as a "major customer" in their financial statements. DLA has adopted this same 10% baseline.

---

### Q57 — Phase II government development environment

**Question:** In Phase II a scalable prototype is requested to be developed in a government-approved development environment. Insight into what the capabilities and limitations of this development environment would prevent suboptimal choices in the proposal and Phase I work. Obvious examples are approved software (such as python packages) and internet access (for dynamic data collection). In Phase I will we be using the development environment? Or is any environment (desktop, US-cloud based, etc.) permitted?

**Answer:** Given that this information is designated as CUI, DLA will provide the necessary details about the government-approved development environment for Phase II only after the required Non-Disclosure Agreement (NDA) and Data Use Agreement are signed, and your capability to protect CUI data has been validated.
