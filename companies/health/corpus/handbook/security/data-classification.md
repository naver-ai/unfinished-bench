# Data classification

**Owner:** Information security  
**Last edited by:** Isaac Wagner  

This document defines the four data classes we use at Kellsbrook Health, with examples from our systems and the storage each class belongs in. When in doubt, classify at the higher (more restrictive) class. If you need help deciding, ask Information security in #security.

## Data classes

| Class | Definition | Examples |
|---|---|---|
| **Public** | Information that can be shared with anyone outside Kellsbrook without harm. | Marketing copy that has been approved for external use, press releases, job postings, the public portions of our website. |
| **Internal** | Information intended for Kellsbrook staff only. Not for external distribution without a business need. | Org charts, internal policies (including this handbook), meeting notes, internal project plans, most content in chat channels. |
| **Confidential** | Information that would cause harm if disclosed outside Kellsbrook or to staff without a need to know. Includes most personally identifiable information (PII) and most business-sensitive material. | Employee records in the HR system, payroll data, contracts under negotiation, financial reports before they are published, credentialing files, research protocols before publication. |
| **Restricted** | The most sensitive information. Disclosure would cause serious harm to patients, members, staff, or the organization. Includes protected health information (PHI) and other categories with legal or regulatory obligations. | PHI in the EHR, patient portal and patient app data, claims data in the claims adjudication system, member information in the member portal, safety event reports, study data that includes identifiers, eIRB submissions. |

## Labeling

- **Public** documents do not need a label, but if you add one, use `PUBLIC`.
- **Internal** documents should carry `INTERNAL` in the file name or in the document header.
- **Confidential** documents must carry `CONFIDENTIAL` in the file name or header, and should be stored in a location that restricts access (see the table below).
- **Restricted** documents must carry `RESTRICTED` in the file name or header. This is required, not optional.

For files, prefix the file name with the class, e.g. `RESTRICTED_claims-adjudication-runbook.docx`. For documents that live in a system that does not allow file name prefixes (like a wiki page), put the class in the title or at the top of the body.

## Storage by class

| Class | Where it belongs | Where it does NOT belong |
|---|---|---|
| **Public** | The public website, approved external channels. | Any internal-only repository, chat, or share. |
| **Internal** | Kellsbrook {{DOC_SHARING}}, the internal wiki, team drives, chat channels, email to Kellsbrook addresses. | Public websites, external file shares, personal cloud storage. |
| **Confidential** | Restricted-access {{DOC_SHARING}} sites, the HR system, the credentialing system, encrypted email for external recipients. | Unrestricted team drives, chat channels (even #general is too broad), personal devices. |
| **Restricted** | The EHR, the claims adjudication system, the member portal, the chart archive, the data warehouse (for rows containing PHI), the eIRB system, the CTMS, the EDC, encrypted email with a business need. | Anything outside the systems listed, including {{DOC_SHARING}}, team drives, chat, personal cloud storage, USB drives. |

A few notes that do not fit neatly in the table:

- The data warehouse is a mixed environment. Aggregated, de-identified data in the warehouse is **Internal** or **Confidential** depending on the content; any table or view that contains PHI is **Restricted** and must be treated as such.
- The interface engine carries HL7 feeds between systems. Logs and message bodies in the interface engine are **Restricted** if they contain PHI, which they usually do.
- The chart archive (scanned paper charts) and the records platform's document archive (claim documents, broker contract scans, OCR work files) hold scanned records. Anything there that is a medical record or a claim document is **Restricted**.
- Research study data in the EDC and in labshare is **Confidential** at minimum; if it contains direct identifiers or code keys, it is **Restricted**. Pseudonymised study data without the key is still **Confidential**.
- The Cork medical centre is a GP-led practice and handles the same classes of data as our US clinics. The same rules apply there, including for the research institute's European trials office.
- Payroll data is **Confidential**, not **Restricted**, even though it is sensitive. The EHR and claims systems contain PHI and are **Restricted**; payroll does not contain PHI.
- Contracts are **Confidential** until they are executed and approved for release; after that they may be **Internal** unless they contain pricing or other terms that remain sensitive.
- The paging system is used for clinical communication and may carry PHI; treat pages as **Restricted** when they contain patient information. Keep PHI out of pages where a non-PHI alternative exists.

## Handling by class

- **Public** and **Internal**: use normal care. Internal documents should not be forwarded outside Kellsbrook without checking with the owner.
- **Confidential**: only share with staff who need it for their work. When sending externally, use encrypted email or the approved file transfer method. Do not post in chat channels.
- **Restricted**: only share with staff who have a documented need to know, and only through the systems listed above. Never send restricted data through unencrypted email. Never copy restricted data to a laptop or phone unless the device is managed by Kellsbrook IT and the data is needed for the staff member's role.

## Exceptions

Exceptions to this classification scheme must be approved by Information security. Send the request to the team in #security with the document or data involved, the class you think it should be, and the reason. The team will confirm or propose a different class.
