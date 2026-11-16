# Acceptable use

**Owner:** Cloud security  
**Last edited by:** Hamza Pereira  
**Applies to:** All employees, contractors, and interns using Brakwater systems and data.

## Purpose

This policy defines acceptable use of company systems, accounts, and data. It protects Brakwater's assets, our customers' data, and our reputation. It applies to all company-provided devices and services, and to personal devices when used for work.

## Scope

Covers use of company accounts and systems, monitoring, generative tools, and personal devices. Separate policies cover data classification, incident reporting, and access requests.

## Policy

1. **General use**
   1.1 Company systems and accounts are provided for work purposes. Incidental personal use is permitted if it does not interfere with your work, consume significant resources, or risk data.
   1.2 You may not use company systems for commercial activity outside Brakwater, for political campaigning, or for any activity that violates law or regulation.
   1.3 Accounts are issued to individuals. Do not share passwords, tokens, API keys, or sign-in sessions. Do not use another person's account.
   1.4 Use strong, unique passwords and store them in the password manager. Follow the guidance in handbook/it/passwords-and-mfa.md.

2. **Monitoring and privacy**
   2.1 Brakwater monitors company systems for security, operational, and compliance purposes. This includes network traffic, system logs, access logs, and file metadata. Do not assume any activity on company systems is private.
   2.2 The company does not routinely review the content of your chats, documents, or files, but may do so as part of an investigation, legal matter, or audit.
   2.3 Personal devices used for remote access may have monitoring software installed. If you are asked to install monitoring software, check with Cloud security before accepting.

3. **Generative tools**
   3.1 Only generative tools approved by Cloud security may be used for work. The approved list is in the IT service desk knowledge base; if a tool is not listed, it is not approved.
   3.2 Do not paste customer data, imagery, AOIs, or any data classified as confidential or restricted into a generative tool, even an approved one, unless the tool's approval explicitly covers that data class.
   3.3 Output from approved generative tools counts as company content. You are responsible for reviewing it for accuracy, bias, and policy compliance before use.
   3.4 Do not use generative tools to write code that will be deployed without review by a human with appropriate expertise.

4. **Personal devices**
   4.1 Personal devices may access company email, chat, and the customer API console through the approved remote access method. They may not be used to process or store imagery, sensor data, or customer AOIs unless the device is managed under the BYOD program.
   4.2 If you lose a personal device that has company access, report it to the IT service desk immediately, and to Cloud security if the device stores any restricted data.
   4.3 Personal devices used for work must have encryption enabled and a recent OS version. The IT service desk can help you check and configure this.

5. **Data handling**
   5.1 Follow the data classification policy in handbook/security/data-classification.md when storing, sending, or copying data.
   5.2 Do not download restricted data to unmanaged devices or personal cloud storage. Use the approved tools and destinations.
   5.3 When working with customer data, including imagery and sensor readings, follow the access rules in data-docs/governance/data-access.md.

6. **Systems and services**
   6.1 Use the approved systems for their intended purpose. For example, use the workflow scheduler for pipelines, not scheduled tasks on a notebook server.
   6.2 Do not install software on company devices without approval. If you need a tool, request it through the IT service desk.
   6.3 Do not disable or weaken the security settings on company devices, including anti-malware, disk encryption, or screen locks.

7. **Reporting**
   7.1 If you see something that may be a security issue, report it as described in handbook/security/incident-reporting.md.
   7.2 If you are unsure whether an action is allowed under this policy, ask Cloud security in #security, or the IT service desk.

8. **Enforcement**
   8.1 Violations of this policy may result in disciplinary action, up to and including termination of employment or contract.
   8.2 Cloud security may suspend access to a system immediately if there is reason to believe it has been compromised or used in violation of this policy.
