# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Company: Kellsbrook Health (regional health system), a shared organisation. The 8 scenarios assigned to health use the same people, teams and time zones.
Generated deterministically (fixed seed): wherever it is loaded from, the same person has the same title, team, manager and time zone.
Key people (executives, team leads, people named in scenarios) are written by hand (same ids as in the scenario modules); the rest are filled from the name pool.
Offices: three in the US (South Bend, Valparaiso, Kalamazoo; Eastern and Central time) plus one in Cork, Ireland. Cork exists so that the user of the 3 scenarios whose anchor
time is European morning (c3-bucket-lifecycle, c6-patient-recall-letters, c7-clinical-protocol-deviation) is within local weekday working hours."""
import random

from scenarios.common import unique_people

COMPANY = {
    "name": "Kellsbrook Health", "legal_name": "Kellsbrook Health System, Inc.", "domain": "kellsbrookhealth.org",
    "what": "Regional health system in northern Indiana and southwest Michigan: three hospitals (South Bend, Valparaiso, Kalamazoo), "
            "about 40 primary care, urgent care and specialty clinics, Kellsbrook Health Plan (about 150,000 members: employer groups, "
            "individual plans and {{MANAGED_PLAN_PROGRAM}}) and the Kellsbrook Research Institute in Kalamazoo. A small Irish arm in Cork runs a "
            "GP-led medical centre (opened for employer-group members at US companies' Cork sites, now open to the public), the research "
            "institute's European trials office and part of IT operations.",
    "headcount": 9000,
    "offices": {"southbend": ("South Bend, IN (HQ and flagship hospital)", "America/Indiana/Indianapolis"),
                "valpo": ("Valparaiso, IN (hospital and health plan offices)", "America/Chicago"),
                "kalamazoo": ("Kalamazoo, MI (hospital and research institute)", "America/Detroit"),
                "cork": ("Cork, Ireland (medical centre, European trials office, IT operations)", "Europe/Dublin")},
    "fiscal_year_start": "July",
}

# Teams: key -> (display name, office, parent team key)
TEAMS = {
    "exec": ("Executive team", "southbend", None),
    # Finance
    "finance": ("Finance", "southbend", "exec"), "ap": ("Accounts payable", "southbend", "finance"), "payroll": ("Payroll", "southbend", "finance"),
    "fpa": ("Financial planning & analysis", "southbend", "finance"), "revcycle": ("Revenue cycle (hospital and clinic billing)", "southbend", "finance"),
    # Health insurance
    "plan": ("Kellsbrook Health Plan", "valpo", "exec"), "claims": ("Claims", "valpo", "plan"), "claimspay": ("Claims payments", "valpo", "plan"),
    "siu": ("Special investigations (SIU)", "southbend", "plan"), "provsvc": ("Provider services", "valpo", "plan"),
    "membersvc": ("Member services", "valpo", "plan"), "um": ("Utilization management", "valpo", "plan"),
    # Hospital and clinic operations
    "care": ("Hospital & clinic operations", "southbend", "exec"), "nursing": ("Nursing administration", "southbend", "care"),
    "clinics": ("Clinics (primary and specialty care)", "southbend", "care"), "corkmc": ("Cork medical centre", "cork", "care"),
    "access": ("Patient access & scheduling", "southbend", "care"), "him": ("Health information management (medical records)", "southbend", "care"),
    "px": ("Patient experience", "southbend", "care"), "quality": ("Quality & patient safety", "southbend", "care"),
    "lab": ("Laboratory services", "southbend", "care"), "pharmacy": ("Pharmacy", "southbend", "care"),
    # Research institute
    "research": ("Kellsbrook Research Institute", "kalamazoo", "exec"), "irb": ("Research ethics & IRB office", "kalamazoo", "research"),
    "ctu": ("Clinical trials office", "kalamazoo", "research"), "investigators": ("Investigators & clinical science", "kalamazoo", "research"),
    "cohort": ("Cohort studies", "kalamazoo", "research"), "studydata": ("Research data management", "kalamazoo", "research"),
    # IT
    "it": ("Information technology", "southbend", "exec"), "servicedesk": ("IT service desk", "southbend", "it"),
    "infra": ("Infrastructure & SRE", "southbend", "it"), "network": ("Network engineering & remote access", "southbend", "it"),
    "security": ("Information security", "southbend", "it"), "his": ("Clinical applications (HIS)", "southbend", "it"),
    "recplat": ("Records platform", "cork", "it"), "dataeng": ("Data & analytics engineering", "southbend", "it"),
    "digital": ("Digital products (patient app and portal)", "southbend", "it"),
    # Legal and compliance, HR, communications
    "legal": ("Legal", "southbend", "exec"), "litigation": ("Litigation", "southbend", "legal"),
    "compliance": ("Compliance & privacy", "southbend", "legal"), "people": ("Human resources", "southbend", "exec"),
    "comms": ("Marketing & communications", "southbend", "exec"),
}

# Key people: (id, name, title, team, manager id or None, office override or None)
# People named in scenarios keep the module's id: c1 claims payout, c2 research data, c3 two archives, c6 letters and survey, c7 clinical trial.
KEY = [
    # Executives
    ("douglas.vandermolen", "Douglas Vandermolen", "President and Chief Executive Officer", "exec", None, None),
    ("karen.szymanski", "Karen Szymanski", "Chief Financial Officer", "exec", "douglas.vandermolen", None),
    ("marcus.whitcomb", "Marcus Whitcomb", "Chief Operating Officer", "exec", "douglas.vandermolen", None),
    ("denise.achterberg", "Denise Achterberg", "Chief Medical Officer", "exec", "douglas.vandermolen", None),
    ("raymond.pellegrino", "Raymond Pellegrino", "Chief Information Officer", "exec", "douglas.vandermolen", None),
    ("colleen.haines", "Colleen Haines", "President, Kellsbrook Health Plan", "plan", "douglas.vandermolen", None),
    ("leonard.brandvold", "Leonard Brandvold", "Chief Research Officer", "research", "douglas.vandermolen", None),
    ("gregory.tillery", "Gregory Tillery", "General Counsel", "legal", "douglas.vandermolen", None),
    ("sharon.nakashima", "Sharon Nakashima", "Chief People Officer", "people", "douglas.vandermolen", None),
    ("monica.feldkamp", "Monica Feldkamp", "Vice President, Marketing & Communications", "comms", "douglas.vandermolen", None),
    ("theresa.okwuosa", "Theresa Okwuosa", "Chief Nursing Officer", "nursing", "marcus.whitcomb", None),
    ("curtis.ambrose", "Curtis Ambrose", "Chief Compliance and Privacy Officer", "compliance", "gregory.tillery", None),
    ("patricia.lowell", "Patricia Lowell", "Chief Information Security Officer", "security", "raymond.pellegrino", None),
    ("janet.kowalik", "Janet Kowalik", "Director of Claims", "claims", "colleen.haines", None),
    # c1 claims payout
    ("declan.farrow", "Declan Farrow", "Claims Payments Supervisor", "claimspay", "janet.kowalik", None),
    ("maren.castellano", "Maren Castellano", "Claims Payment Specialist", "claimspay", "declan.farrow", None),
    ("ifeoma.barrett", "Ifeoma Barrett", "Special Investigations Manager", "siu", "colleen.haines", None),
    ("sunniva.holt", "Sunniva Holt", "SIU Analyst", "siu", "ifeoma.barrett", None),
    ("noor.haddad", "Noor Haddad", "Provider Services Lead", "provsvc", "colleen.haines", None),
    ("chiara.sorensen", "Chiara Sorensen", "Claims Operations Lead", "claims", "janet.kowalik", None),
    ("lin.hartley", "Lin Hartley", "Senior Claims Examiner", "claims", "chiara.sorensen", None),
    ("dara.osei", "Dara Osei", "Claims Examiner", "claims", "chiara.sorensen", None),
    ("tomas.vieira", "Tomas Vieira", "Claims Examiner", "claims", "chiara.sorensen", None),
    ("keisha.pruitt", "Keisha Pruitt", "Claims Examiner", "claims", "chiara.sorensen", None),
    ("leon.karimi", "Leon Karimi", "Claims Examiner", "claims", "chiara.sorensen", None),
    ("henrik.eklund", "Henrik Eklund", "Claims Examiner", "claims", "chiara.sorensen", None),
    # c2 research data transfer
    ("esme.latimer", "Esme Latimer", "Study Data Manager", "studydata", None, None),
    ("rowan.adebayo", "Rowan Adebayo", "Principal Investigator", "investigators", None, None),
    ("gethin.pryce", "Gethin Pryce", "Study Coordinator", "cohort", None, None),
    ("clara.voss", "Clara Voss", "Research Governance Officer", "irb", None, None),
    # c3 document archive bucket (insurance claim documents); the records platform is in Cork
    ("tariq.abara", "Tariq Abara", "Head of Records Platform", "recplat", "raymond.pellegrino", None),
    ("miriam.bauer", "Miriam Bauer", "Records Platform Engineer", "recplat", "tariq.abara", None),
    ("petra.park", "Petra Park", "Records Manager", "recplat", "tariq.abara", None),
    ("anders.tran", "Anders Tran", "Data Engineer", "dataeng", None, "cork"),
    ("jin.olsen", "Jin Olsen", "Site Reliability Engineer", "infra", None, "cork"),
    ("ivan.keller", "Ivan Keller", "Senior Counsel, Litigation", "litigation", "gregory.tillery", None),
    ("aiko.lopez", "Aiko Lopez", "Paralegal", "litigation", "ivan.keller", None),
    # c3 chart scan archive
    ("aiko.young", "Aiko Young", "HIS Manager", "his", "raymond.pellegrino", None),
    ("yasmin.osei", "Yasmin Osei", "Clinical Systems Analyst", "his", "aiko.young", None),
    ("georgia.marchetti", "Georgia Marchetti", "HIM Manager", "him", "marcus.whitcomb", None),
    ("arjun.eklund", "Arjun Eklund", "Coding Supervisor", "him", "georgia.marchetti", None),
    ("joanna.sorensen", "Joanna Sorensen", "Records Technician", "him", "georgia.marchetti", None),
    ("jada.carvalho", "Jada Carvalho", "Revenue Cycle Lead", "revcycle", None, None),
    ("andile.campos", "Andile Campos", "Systems Engineer", "infra", None, None),
    ("chiara.rossi", "Chiara Rossi", "Legal Counsel", "litigation", "ivan.keller", None),
    # c6 retest recall letters; Cork medical centre
    ("aoife.brennan", "Aoife Brennan", "GP, Clinical Lead", "corkmc", "denise.achterberg", None),
    ("siobhan.kiely", "Siobhán Kiely", "Practice Manager", "corkmc", "aoife.brennan", None),
    ("tomas.novak", "Tomás Novak", "Lab Liaison", "corkmc", "siobhan.kiely", None),
    ("maeve.daly", "Maeve Daly", "Reception Lead", "corkmc", "siobhan.kiely", None),
    ("grace.okafor", "Grace Okafor", "Practice Nurse", "corkmc", "aoife.brennan", None),
    # c6 patient experience survey
    ("hana.lindqvist", "Hana Lindqvist", "Patient Experience Research Lead", "px", None, None),
    ("reuben.sata", "Reuben Sata", "Patient Insights Analyst", "px", "hana.lindqvist", None),
    ("gus.arara", "Gus Arara", "Product Manager, Patient App", "digital", None, None),
    ("elin.borg", "Elin Borg", "Patient Portal Support Lead", "digital", None, "valpo"),
    ("wes.chan", "Wes Chan", "Finance Analyst", "fpa", None, None),
    # c7 clinical trial protocol deviation; European clinical trials office (Cork)
    ("noemi.brunner", "Noemi Brunner", "Clinical Trial Manager", "ctu", None, "cork"),
    ("fabio.rossi", "Fabio Rossi", "Site Coordinator, European sites", "ctu", "noemi.brunner", "cork"),
    ("aurelio.conti", "Aurelio Conti", "Consultant Physician and Clinical Investigator", "investigators", None, "cork"),
    ("helena.voss", "Helena Voss", "Medical Monitor", "investigators", None, None),
    ("mei.lin", "Mei Lin", "Clinical Pharmacologist", "investigators", None, None),
    ("ingrid.aasen", "Ingrid Aasen", "Ethics Committee Liaison", "irb", None, "cork"),
    ("piotr.zielinski", "Piotr Zielinski", "Deputy Ethics Liaison", "irb", "ingrid.aasen", "cork"),
    ("anja.huber", "Anja Huber", "Clinical Data Manager", "studydata", None, "cork"),
]
# Teams led by key people (no automatic team lead is generated)
KEY_LEADS = {"claims": "janet.kowalik", "claimspay": "declan.farrow", "siu": "ifeoma.barrett", "provsvc": "noor.haddad",
             "recplat": "tariq.abara", "litigation": "ivan.keller", "his": "aiko.young", "him": "georgia.marchetti",
             "corkmc": "aoife.brennan", "security": "patricia.lowell", "nursing": "theresa.okwuosa", "compliance": "curtis.ambrose",
             "comms": "monica.feldkamp"}
# Auto-generated staff per team (excluding team leads)
FILL = {"ap": 3, "payroll": 3, "fpa": 3, "revcycle": 4, "claims": 5, "claimspay": 2, "siu": 2, "provsvc": 4, "membersvc": 4, "um": 4,
        "nursing": 3, "clinics": 4, "corkmc": 2, "access": 4, "him": 4, "px": 2, "quality": 2, "lab": 2, "pharmacy": 2,
        "irb": 2, "ctu": 3, "investigators": 2, "cohort": 3, "studydata": 2,
        "servicedesk": 4, "infra": 3, "network": 3, "security": 3, "his": 4, "recplat": 2, "dataeng": 3, "digital": 2,
        "litigation": 1, "compliance": 2, "people": 3, "comms": 2}
TITLES = {
    "ap": ["Accounts Payable Specialist", "Accounts Payable Clerk"], "payroll": ["Payroll Specialist", "Payroll Administrator"],
    "fpa": ["Financial Analyst", "Senior Financial Analyst", "Budget Analyst"],
    "revcycle": ["Billing Specialist", "Patient Account Representative", "Denials Analyst", "Charge Capture Analyst"],
    "claims": ["Claims Examiner", "Senior Claims Examiner", "Claims Adjuster"], "claimspay": ["Claims Payment Specialist", "Payments Coordinator"],
    "siu": ["SIU Analyst", "SIU Investigator"], "provsvc": ["Provider Services Representative", "Provider Network Specialist", "Credentialing Specialist"],
    "membersvc": ["Member Services Representative", "Member Services Team Lead", "Appeals Coordinator"],
    "um": ["Utilization Review Nurse", "Prior Authorization Coordinator", "Case Manager, RN"],
    "nursing": ["Nursing Director", "Clinical Nurse Educator", "Nurse Manager"],
    "clinics": ["Clinic Manager", "Practice Administrator", "Medical Assistant Supervisor"],
    "corkmc": ["General Practitioner", "Practice Secretary", "Healthcare Assistant"],
    "access": ["Patient Access Representative", "Scheduling Coordinator", "Insurance Verification Specialist"],
    "him": ["Medical Coder", "Senior Inpatient Coder", "Release of Information Specialist", "Clinical Documentation Specialist"],
    "px": ["Patient Experience Coordinator", "Patient Advocate"], "quality": ["Quality Analyst", "Patient Safety Specialist", "Infection Preventionist"],
    "lab": ["Medical Laboratory Scientist", "Lab Quality Coordinator"], "pharmacy": ["Clinical Pharmacist", "Pharmacy Informatics Analyst"],
    "irb": ["IRB Analyst", "IRB Coordinator"], "ctu": ["Clinical Research Coordinator", "Clinical Research Associate", "Regulatory Coordinator"],
    "investigators": ["Research Scientist", "Biostatistician", "Research Nurse"], "cohort": ["Study Coordinator", "Research Assistant"],
    "studydata": ["Research Data Analyst", "Clinical Data Coordinator"],
    "servicedesk": ["Service Desk Analyst", "Desktop Support Technician", "Senior Service Desk Analyst"],
    "infra": ["Systems Engineer", "Site Reliability Engineer", "Storage Engineer"], "network": ["Network Engineer", "Senior Network Engineer"],
    "security": ["Security Analyst", "Security Engineer", "Identity and Access Analyst"],
    "his": ["Clinical Systems Analyst", "EHR Analyst", "Interface Analyst"], "recplat": ["Records Platform Engineer", "Records Analyst"],
    "dataeng": ["Data Engineer", "BI Developer", "Analytics Engineer"], "digital": ["Software Engineer", "UX Designer", "Product Analyst"],
    "litigation": ["Paralegal", "Legal Assistant"], "compliance": ["Compliance Analyst", "Privacy Analyst"],
    "people": ["HR Business Partner", "Recruiter", "Benefits Specialist"], "comms": ["Communications Specialist", "Marketing Manager"],
}
LEAD_TITLE = {k: f"Head of {v[0]}" for k, v in TEAMS.items()}
LEAD_TITLE.update({"ap": "Accounts Payable Manager", "payroll": "Payroll Manager", "fpa": "Director of Financial Planning & Analysis",
                   "revcycle": "Director of Revenue Cycle", "membersvc": "Member Services Manager", "um": "Director of Utilization Management",
                   "clinics": "Director of Clinic Operations", "access": "Patient Access Manager", "px": "Director of Patient Experience",
                   "quality": "Director of Quality & Patient Safety", "lab": "Laboratory Director", "pharmacy": "Director of Pharmacy",
                   "irb": "IRB Director", "ctu": "Director, Clinical Trials Office", "investigators": "Director of Clinical Science",
                   "cohort": "Cohort Studies Program Manager", "studydata": "Research Data Manager", "servicedesk": "Service Desk Manager",
                   "infra": "Infrastructure Manager", "network": "Network Engineering Manager", "dataeng": "Data & Analytics Manager",
                   "digital": "Director of Digital Products", "people": "HR Operations Manager"})
# Parent team -> the executive responsible for it (manager of auto-generated team leads)
DEPT_HEAD = {"exec": "douglas.vandermolen", "finance": "karen.szymanski", "plan": "colleen.haines", "care": "marcus.whitcomb",
             "research": "leonard.brandvold", "it": "raymond.pellegrino", "legal": "gregory.tillery", "people": "sharon.nakashima",
             "comms": "monica.feldkamp"}
# Common absence statuses (most are empty). No clock times, weekdays or relative-time words.
STATUSES = [""] * 15 + ["In back-to-back meetings", "Out sick", "On PTO", "Working from home", "In clinic", "On call",
                         "At an offsite", "Traveling"]
STATUS_TEAMS = {"In clinic": {"nursing", "clinics", "corkmc", "investigators", "pharmacy"},
                "On call": {"nursing", "infra", "network", "security", "servicedesk", "his", "recplat", "pharmacy", "lab", "dataeng"}}


def people(seed="kellsbrook-v1"):
    rng = random.Random(seed)
    out, ids = [], set()
    def add(pid, name, title, team, manager, office=None, status=""):
        off = office or TEAMS[team][1]
        out.append({"id": pid, "name": name, "title": title, "team": team, "team_name": TEAMS[team][0], "manager": manager,
                    "office": COMPANY["offices"][off][0], "office_key": off, "timezone": COMPANY["offices"][off][1], "status": status})
        ids.add(pid)
    for pid, name, title, team, mgr, off in KEY:
        add(pid, name, title, team, mgr, off)
    leads = dict(KEY_LEADS)
    taken = {tuple(p["name"].split(" ", 1)) for p in out}
    pool = [x for x in unique_people(rng, 400) if x not in taken]
    it = iter(pool)
    def new_id(fn, ln):
        base = f"{fn}.{ln}".lower().replace("'", "")
        pid, n = base, 2
        while pid in ids:
            pid, n = f"{base}{n}", n + 1
        return pid
    for team, n in FILL.items():
        parent = TEAMS[team][2]
        if team not in leads:
            fn, ln = next(it); pid = new_id(fn, ln)
            head_of = DEPT_HEAD.get(parent, "douglas.vandermolen") if parent and parent != "exec" else DEPT_HEAD.get(team, "douglas.vandermolen")
            add(pid, f"{fn} {ln}", LEAD_TITLE[team], team, head_of)
            leads[team] = pid
        for _ in range(n):
            fn, ln = next(it); pid = new_id(fn, ln)
            add(pid, f"{fn} {ln}", rng.choice(TITLES[team]), team, leads[team], status=rng.choice(STATUSES))
    for p in out:                                    # Key people with no manager are placed under the team lead
        if p["manager"] is None and p["id"] != "douglas.vandermolen":
            p["manager"] = leads.get(p["team"]) if leads.get(p["team"]) not in (None, p["id"]) else DEPT_HEAD.get(TEAMS[p["team"]][2] or p["team"], "douglas.vandermolen")
        # Clinic and on-call statuses only for the teams that do that work (avoids odd combinations such as a claims review coordinator marked 'In clinic'). No extra random numbers are drawn, so the roster stays the same.
        if p["status"] == "In clinic" and p["team"] not in STATUS_TEAMS["In clinic"]:
            p["status"] = ""
        if p["status"] == "On call" and p["team"] not in STATUS_TEAMS["On call"]:
            p["status"] = ""
    return out


def by_id():
    return {p["id"]: p for p in people()}


def email(pid):
    return f"{pid}@{COMPANY['domain']}"


# Company chat channels (shared): name -> (topic, default member teams; "*" = everyone, "@<office key>" = that office)
CHANNELS = {
    "general": ("Kellsbrook-wide announcements", ["*"]), "random": ("Anything else", ["*"]), "it-help": ("IT help", ["*"]),
    "southbend-campus": ("South Bend campus — parking, cafeteria, badges, building works", ["@southbend"]),
    "valpo-office": ("Valparaiso hospital and health plan offices", ["@valpo"]),
    "kalamazoo-campus": ("Kalamazoo hospital and research institute building", ["@kalamazoo"]),
    "cork-office": ("Cork — medical centre, trials office and IT", ["@cork"]),
    "claims-ops": ("Claims operations", ["claims", "claimspay", "siu", "um"]),
    "claims-payments": ("Payment runs, EFT, checks", ["claimspay", "provsvc"]),
    "provider-services": ("Provider calls, credentialing, network questions", ["provsvc", "claims", "membersvc"]),
    "member-services": ("Member calls, ID cards, appeals intake", ["membersvc", "um"]),
    "revenue-cycle": ("Hospital and clinic billing", ["revcycle", "him", "access"]),
    "records-office": ("HIM office — coding, release of information, chart corrections", ["him", "revcycle", "his"]),
    "his-platform": ("Clinical applications: EHR, interfaces, scanning", ["his", "infra"]),
    "records-platform": ("Claims document ingest, OCR, archive buckets", ["recplat", "infra", "dataeng"]),
    "infrastructure": ("Servers, storage, backups, on-call", ["infra", "network", "security"]),
    "network-ops": ("Network, Wi-Fi, remote access", ["network", "security", "servicedesk"]),
    "security": ("Information security", ["security", "compliance", "network"]),
    "data-eng": ("Data warehouse and reporting", ["dataeng", "his", "fpa"]),
    "research-institute": ("Kellsbrook Research Institute — general", ["research", "irb", "ctu", "investigators", "cohort", "studydata"]),
    "clinical-trials": ("Clinical trials office", ["ctu", "investigators", "irb", "studydata"]),
    "data-management": ("Study data management and governance", ["studydata", "cohort", "irb"]),
    "patient-experience": ("Patient experience, complaints, rounding", ["px", "quality", "digital", "comms"]),
    "digital": ("Patient app and portal", ["digital", "px", "servicedesk"]),
    "nursing-leaders": ("Nursing leadership", ["nursing", "quality", "clinics"]),
    "clinic-ops": ("Clinic operations", ["clinics", "access", "corkmc", "lab"]),
    "finance": ("Finance team", ["finance", "ap", "payroll", "fpa", "revcycle"]),
    "people-team": ("HR and payroll questions", ["people", "payroll"]),
}
# Company systems: scenario tools (claimsctl, labshare, archivectl, chartarc, recallctl, surveyctl, protocolctl, tickets, chat) and ordinary systems
SYSTEMS = ["the EHR (clinical record)", "the patient portal", "the patient app", "the claims adjudication system", "claimsctl (claims payment queue)",
           "the provider portal", "the credentialing system", "the prior authorization queue", "the member portal",
           "the scheduling and registration system", "the lab information system", "the pharmacy system", "the safety event reporting system",
           "chartarc (scanned chart archive)", "archivectl (document archive buckets)", "the interface engine (HL7 feeds)",
           "labshare (study data sharing)", "the eIRB system", "the CTMS", "the EDC", "protocolctl (protocol changes and the study record)",
           "recallctl (patient recall letters)", "surveyctl (patient panel invitations)", "the VPN client and gateway",
           "tickets (IT service management)", "chat (the company chat)", "the data warehouse", "the HR system", "the timekeeping system",
           "the learning management system", "the expenses tool", "the paging system"]


if __name__ == "__main__":
    ps = people()
    import collections
    print(len(ps), "people |", dict(collections.Counter(p["timezone"] for p in ps)))
    for p in ps[:25]: print(f"  {p['id']:22s} {p['title']:40s} {p['team_name']:32s} manager={p['manager']}")
