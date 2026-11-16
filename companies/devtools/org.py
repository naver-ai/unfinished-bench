# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Company: Gantline (developer tools SaaS), a shared organisation. The 16 scenarios assigned to devtools use the same people, teams and time zones.
Generated deterministically (fixed seed): wherever it is loaded from, the same person has the same title, team, manager and time zone.
Key people (executives, department heads, people named in scenarios) are written by hand; the rest are filled from the name pool (scenarios.common.unique_people).
People who appear in scenarios keep the ids used in each scenario module (scenarios/<module>.py), so a task can move to this company unchanged.
Some titles are adjusted to fit this company."""
import random

from scenarios.common import unique_people

COMPANY = {
    "name": "Gantline", "legal_name": "Gantline Software, Lda.", "domain": "gantline.dev",
    "what": "Developer tools: gnt, an open-source command-line tool for building, testing and shipping code, and Gantline Cloud, "
            "a hosted development platform (code hosting, hosted CI runners, cloud workspaces, code search, a public API, "
            "a web and desktop editor and mobile apps) sold per seat to teams and enterprises. US customers are served by Gantline Inc.",
    "headcount": 400,
    "offices": {"lisbon": ("Lisbon (HQ)", "Europe/Lisbon"), "portland": ("Portland, OR", "America/Los_Angeles")},
    "fiscal_year_start": "January",
}

# Teams: key -> (display name, office, parent team key)
TEAMS = {
    "exec": ("Leadership team", "lisbon", None),
    # Engineering
    "eng": ("Engineering", "lisbon", "exec"),
    "devprod": ("Developer productivity", "lisbon", "eng"),
    "releng": ("Release engineering & CI", "lisbon", "devprod"), "buildinfra": ("Build infrastructure", "lisbon", "devprod"),
    "qa": ("Quality engineering", "lisbon", "devprod"),
    "infra": ("Infrastructure", "lisbon", "eng"),
    "sre": ("Site reliability", "lisbon", "infra"), "lab": ("Lab & hypervisors", "lisbon", "infra"),
    "neteng": ("Network engineering", "lisbon", "infra"), "it": ("IT & workplace tech", "lisbon", "infra"),
    "prodeng": ("Product engineering", "lisbon", "eng"),
    "workspaces": ("Hosted workspaces", "lisbon", "prodeng"), "runners": ("Hosted runners", "portland", "prodeng"),
    "cli": ("CLI & SDKs", "lisbon", "prodeng"), "api": ("Public API", "lisbon", "prodeng"),
    "search": ("Search & indexing", "lisbon", "prodeng"), "editor": ("Editor", "lisbon", "prodeng"),
    "mobile": ("Mobile apps", "portland", "prodeng"), "billingeng": ("Billing engineering", "lisbon", "prodeng"),
    "data": ("Data platform", "lisbon", "eng"),
    "security": ("Security", "lisbon", "eng"),
    "prodsec": ("Product security", "lisbon", "security"), "identity": ("Identity & access", "lisbon", "security"),
    # Product
    "product": ("Product management", "lisbon", "exec"), "design": ("Design", "lisbon", "product"),
    # Sales and customers
    "sales": ("Sales", "portland", "exec"),
    "cs": ("Customer success", "portland", "exec"), "csops": ("CS operations", "portland", "cs"), "support": ("Developer support", "lisbon", "cs"),
    "marketing": ("Marketing", "portland", "exec"),
    "growth": ("Growth & lifecycle", "portland", "marketing"), "content": ("Content", "lisbon", "marketing"),
    "devrel": ("Developer relations", "lisbon", "marketing"), "comms": ("Communications", "lisbon", "marketing"),
    # Business support
    "finance": ("Finance", "lisbon", "exec"),
    "billingops": ("Billing operations", "lisbon", "finance"), "accounting": ("Accounting & payroll", "lisbon", "finance"),
    "people": ("People", "lisbon", "exec"),
    "peopleops": ("People operations", "lisbon", "people"), "talent": ("Talent acquisition", "lisbon", "people"),
    "workplace": ("Workplace & facilities", "lisbon", "people"),
    "legal": ("Legal", "lisbon", "exec"),
}

# Key people: (id, name, title, team, manager id or None, office override or None)
# Manager None = under that team's (auto-generated) team lead.
KEY = [
    # Executives and department heads (company-wide)
    ("catarina.lobo", "Catarina Lobo", "Chief Executive Officer", "exec", None, None),
    ("henrik.aalto", "Henrik Aalto", "Chief Technology Officer", "exec", "catarina.lobo", None),
    ("miguel.antunes", "Miguel Antunes", "Chief Financial Officer", "finance", "catarina.lobo", None),
    ("esther.lindahl", "Esther Lindahl", "Chief Product Officer", "product", "catarina.lobo", None),
    ("grant.holloway", "Grant Holloway", "Chief Revenue Officer", "exec", "catarina.lobo", "portland"),
    ("maya.thornbury", "Maya Thornbury", "VP Marketing", "marketing", "catarina.lobo", None),
    ("ana.sequeira", "Ana Sequeira", "Chief People Officer", "people", "catarina.lobo", None),
    ("filipa.moura", "Filipa Moura", "General Counsel", "legal", "catarina.lobo", None),
    ("joaquim.serrano", "Joaquim Serrano", "Head of Infrastructure", "infra", "henrik.aalto", None),
    ("ingrid.holm", "Ingrid Holm", "VP Engineering, Product", "prodeng", "henrik.aalto", None),
    ("daniela.ferraz", "Daniela Ferraz", "Head of Security", "security", "henrik.aalto", None),
    # c1-credits
    ("meiling.carver", "Mei-Ling Carver", "Billing Operations Lead", "billingops", "miguel.antunes", None),
    ("talia.brandt", "Talia Brandt", "Billing Operations Specialist", "billingops", "meiling.carver", None),
    ("darius.whitlock", "Darius Whitlock", "Support Manager", "support", "marcus.oyelowo", None),
    ("jalen.pierce", "Jalen Pierce", "Support Team Lead", "support", "darius.whitlock", None),
    ("sofia.marek", "Sofia Marek", "Support Specialist", "support", "darius.whitlock", None),
    ("owen.tadesse", "Owen Tadesse", "Support Specialist", "support", "darius.whitlock", "portland"),
    ("brianna.cole", "Brianna Cole", "Support Specialist", "support", "darius.whitlock", "portland"),
    ("colette.ramirez", "Colette Ramirez", "Account Manager", "sales", None, None),
    ("anand.bhatt", "Anand Bhatt", "Account Manager", "sales", None, None),
    # c2-recruiter-roster
    ("gideon.marsh", "Gideon Marsh", "VP Talent", "talent", "ana.sequeira", None),
    ("rhea.castellanos", "Rhea Castellanos", "Senior Talent Partner, Engineering", "talent", "gideon.marsh", None),
    ("solveig.arnesen", "Solveig Arnesen", "Head of People Operations", "peopleops", "ana.sequeira", None),
    ("pavel.novacek", "Pavel Novacek", "HRIS Analyst", "peopleops", "solveig.arnesen", None),
    # c2-vendor-analytics
    ("marcus.oyelowo", "Marcus Oyelowo", "VP Customer Success", "cs", "grant.holloway", None),
    ("keira.lindqvist", "Keira Lindqvist", "CS Operations Manager", "csops", "marcus.oyelowo", None),
    ("lucia.marsh", "Lucia Marsh", "Senior Customer Success Manager", "cs", "marcus.oyelowo", "lisbon"),
    ("tobias.quainoo", "Tobias Quainoo", "Data Engineer", "data", "anika.bauer", None),
    ("hollis.brandt", "Hollis Brandt", "Commercial Counsel", "legal", "filipa.moura", None),
    ("ines.carvalho", "Ines Carvalho", "Contracts Manager", "legal", "filipa.moura", None),
    # Customer success managers for the c2-vendor-analytics account data (the module's CSMS list; ids follow the company's id rule)
    ("owen.fairley", "Owen Fairley", "Customer Success Manager", "cs", "marcus.oyelowo", None),
    ("dev.anand", "Dev Anand", "Customer Success Manager", "cs", "marcus.oyelowo", None),
    ("kirsten.vale", "Kirsten Vale", "Customer Success Manager", "cs", "marcus.oyelowo", "lisbon"),
    ("tobias.rendall", "Tobias Rendall", "Senior Customer Success Manager", "cs", "marcus.oyelowo", None),
    ("aurelie.brandt", "Aurelie Brandt", "Customer Success Manager", "cs", "marcus.oyelowo", "lisbon"),
    ("hugo.pereiralane", "Hugo Pereira-Lane", "Customer Success Manager", "cs", "marcus.oyelowo", "lisbon"),
    ("nkechi.obi", "Nkechi Obi", "Customer Success Manager", "cs", "marcus.oyelowo", None),
    # c3-ci-artifacts
    ("diego.saito", "Diego Saito", "Head of Developer Productivity", "devprod", "henrik.aalto", None),
    ("zainab.bauer", "Zainab Bauer", "Build & Release Engineer", "releng", "georgia.hughes", None),
    ("isaac.lopez", "Isaac Lopez", "Release Manager", "releng", "georgia.hughes", None),
    ("tariq.sorensen", "Tariq Sorensen", "Tech Lead, Hosted Runners", "runners", None, None),
    ("vera.fujita", "Vera Fujita", "Site Reliability Engineer", "sre", None, None),
    ("yusuf.murray", "Yusuf Murray", "QA Lead", "qa", "diego.saito", None),
    ("marco.nagy", "Marco Nagy", "Software Engineer", "workspaces", None, None),
    # c4-build-cache
    ("lena.lambert", "Lena Lambert", "Build Infrastructure Engineer", "buildinfra", "aleksander.novak", None),
    ("samir.doyle", "Samir Doyle", "Staff Engineer, Build Platform", "buildinfra", "aleksander.novak", None),
    ("zoe.nakamura", "Zoe Nakamura", "Backend Lead", "workspaces", None, None),
    ("priya.ozturk", "Priya Ozturk", "Site Reliability Engineer", "sre", None, None),
    ("nico.mahlaba", "Nico Mahlaba", "Technical Program Manager", "product", "esther.lindahl", None),
    ("anton.brennan", "Anton Brennan", "Software Engineer", "workspaces", None, None),
    # c4-dependency-upgrade
    ("georgia.hughes", "Georgia Hughes", "Release Engineering Manager", "releng", "diego.saito", None),
    ("kofi.osei", "Kofi Osei", "Release Engineer", "releng", "georgia.hughes", None),
    ("elena.petrov", "Elena Petrov", "Engineering Manager, Search", "search", "ingrid.holm", None),
    ("mehmet.yilmaz", "Mehmet Yilmaz", "Search Engineer", "search", "elena.petrov", None),
    ("naomi.fujita", "Naomi Fujita", "Search Engineer", "search", "elena.petrov", None),
    ("bruno.costa", "Bruno Costa", "Site Reliability Engineer", "sre", None, None),
    # c4-idle-vm-release
    ("anders.barros", "Anders Barros", "Lab Infrastructure Lead", "lab", "joaquim.serrano", None),
    ("ethan.khan", "Ethan Khan", "Infrastructure Engineer", "lab", "anders.barros", None),
    ("gideon.mendes", "Gideon Mendes", "Site Reliability Engineer", "sre", None, None),
    ("beatriz.ramos", "Beatriz Ramos", "Billing Engineering Lead", "billingeng", "ingrid.holm", None),
    ("lina.thomsen", "Lina Thomsen", "Billing Engineer", "billingeng", "beatriz.ramos", None),
    ("mara.bishop", "Mara Bishop", "QA Engineer", "qa", "yusuf.murray", None),
    ("yasmin.medina", "Yasmin Medina", "Search Engineer", "search", "elena.petrov", None),
    # c4-scratch
    ("aleksander.novak", "Aleksander Novak", "Engineering Manager, Build Infrastructure", "buildinfra", "diego.saito", None),
    ("adrian.aoki", "Adrian Aoki", "Build Infrastructure Engineer", "buildinfra", "aleksander.novak", None),
    ("julia.brooks", "Julia Brooks", "Release Manager", "releng", "georgia.hughes", None),
    ("quentin.mbeki", "Quentin Mbeki", "Site Reliability Engineer", "sre", None, None),
    ("soren.castillo", "Soren Castillo", "Tech Lead, Desktop Editor", "editor", None, None),
    ("harriet.torres", "Harriet Torres", "Test Engineer", "qa", "yusuf.murray", None),
    ("sofia.fonseca", "Sofia Fonseca", "Software Engineer", "editor", None, None),
    ("xavier.keller", "Xavier Keller", "Software Engineer", "editor", None, None),
    # c6-blog-publish
    ("rukmini.sethi", "Rukmini Sethi", "Developer Relations Lead", "devrel", "maya.thornbury", None),
    ("declan.moyo", "Declan Moyo", "Staff Engineer", "workspaces", None, None),
    ("ines.albrecht", "Ines Albrecht", "Head of Communications", "comms", "maya.thornbury", None),
    ("tariq.haddad", "Tariq Haddad", "Content Marketing Manager", "content", None, None),
    ("joana.pereira", "Joana Pereira", "Technical Recruiter", "talent", "gideon.marsh", None),
    ("wei.zhang", "Wei Zhang", "Senior Software Engineer", "api", "leila.haddad", None),
    ("anika.bauer", "Anika Bauer", "Engineering Manager, Data Platform", "data", "henrik.aalto", None),
    ("samir.kaplan", "Samir Kaplan", "Product Counsel", "legal", "filipa.moura", None),
    ("lucia.marchetti", "Lucia Marchetti", "Product Manager, Billing & Plans", "product", "esther.lindahl", None),
    # c6-push-notification
    ("devin.alcott", "Devin Alcott", "Lifecycle Marketing Manager", "growth", None, None),
    ("mara.finch", "Mara Finch", "Mobile Marketing Lead", "growth", None, None),
    ("otto.reyes", "Otto Reyes", "Mobile Platform Engineer", "mobile", None, None),
    ("lena.marsh", "Lena Marsh", "Product Manager, Mobile", "product", "esther.lindahl", "portland"),
    ("sam.oduya", "Sam Oduya", "Support Team Lead", "support", "darius.whitlock", "portland"),
    # c7-dns-cutover
    ("freya.lindgren", "Freya Lindgren", "Network Engineering Lead", "neteng", "joaquim.serrano", None),
    ("kofi.asante", "Kofi Asante", "Network Engineer", "neteng", "freya.lindgren", None),
    ("leila.haddad", "Leila Haddad", "Engineering Manager, Public API", "api", "ingrid.holm", None),
    ("mateo.salazar", "Mateo Salazar", "Site Reliability Engineer", "api", "leila.haddad", None),
    ("ivan.novak", "Ivan Novak", "Site Reliability Engineer", "api", "leila.haddad", None),
    ("hana.sato", "Hana Sato", "Integrations Engineer", "api", "leila.haddad", None),
    # c7-package-signing
    ("elif.demir", "Elif Demir", "Engineering Manager, CLI & SDKs", "cli", "ingrid.holm", None),
    ("nico.bakker", "Nico Bakker", "Developer Tools Engineer", "cli", "elif.demir", None),
    ("jonas.eklund", "Jonas Eklund", "Developer Tools Engineer", "cli", "elif.demir", None),
    ("kwame.osei", "Kwame Osei", "Product Security Lead", "prodsec", "daniela.ferraz", None),
    ("marit.lund", "Marit Lund", "Security Engineer", "prodsec", "kwame.osei", None),
    ("rhea.patel", "Rhea Patel", "Developer Relations Engineer", "devrel", "rukmini.sethi", None),
    ("leah.fischer", "Leah Fischer", "Customer Success Engineer", "cs", "marcus.oyelowo", "lisbon"),
]
# Teams led by key people (the manager of the auto-generated staff)
LEADS = {"exec": "catarina.lobo", "finance": "miguel.antunes", "product": "esther.lindahl", "marketing": "maya.thornbury",
         "people": "ana.sequeira", "legal": "filipa.moura", "infra": "joaquim.serrano", "prodeng": "ingrid.holm", "security": "daniela.ferraz",
         "devprod": "diego.saito", "releng": "georgia.hughes", "buildinfra": "aleksander.novak", "qa": "yusuf.murray", "lab": "anders.barros",
         "neteng": "freya.lindgren", "search": "elena.petrov", "api": "leila.haddad", "cli": "elif.demir", "billingeng": "beatriz.ramos",
         "data": "anika.bauer", "prodsec": "kwame.osei", "cs": "marcus.oyelowo", "csops": "keira.lindqvist", "support": "darius.whitlock",
         "devrel": "rukmini.sethi", "comms": "ines.albrecht", "billingops": "meiling.carver", "peopleops": "solveig.arnesen", "talent": "gideon.marsh"}
# Staff to fill in (excluding team leads). A team listed here but not in LEADS gets a generated team lead.
FILL = {"releng": 2, "buildinfra": 1, "qa": 2, "sre": 2, "lab": 1, "neteng": 1, "it": 3,
        "workspaces": 4, "runners": 4, "cli": 3, "api": 2, "search": 1, "editor": 3, "mobile": 4, "billingeng": 2, "data": 3,
        "prodsec": 2, "identity": 3, "product": 2, "design": 3,
        "sales": 6, "csops": 1, "support": 4, "growth": 2, "content": 2, "devrel": 2, "comms": 1,
        "billingops": 2, "accounting": 4, "peopleops": 2, "talent": 2, "workplace": 2, "legal": 1}
TITLES = {
    "releng": ["Release Engineer", "Build & Release Engineer", "Senior Release Engineer"], "buildinfra": ["Build Infrastructure Engineer"],
    "qa": ["QA Engineer", "Test Automation Engineer"], "sre": ["Site Reliability Engineer", "Senior Site Reliability Engineer"],
    "lab": ["Infrastructure Engineer"], "neteng": ["Network Engineer"], "it": ["IT Support Engineer", "Systems Administrator", "IT Support Analyst"],
    "workspaces": ["Software Engineer", "Senior Software Engineer", "Backend Engineer"], "runners": ["Software Engineer", "Senior Software Engineer", "Systems Engineer"],
    "cli": ["Developer Tools Engineer", "Software Engineer", "Senior Software Engineer"], "api": ["Software Engineer", "Senior Software Engineer"],
    "search": ["Search Engineer"], "editor": ["Software Engineer", "Frontend Engineer", "Senior Software Engineer"],
    "mobile": ["{{MOBILE_OS_1}} Engineer", "{{MOBILE_OS_2}} Engineer", "Mobile Engineer"], "billingeng": ["Billing Engineer", "Software Engineer"],
    "data": ["Data Engineer", "Analytics Engineer", "Data Analyst"], "prodsec": ["Security Engineer", "Application Security Engineer"],
    "identity": ["Identity Engineer", "IAM Engineer"], "product": ["Product Manager", "Senior Product Manager"],
    "design": ["Product Designer", "Senior Product Designer", "UX Researcher"],
    "sales": ["Account Executive", "Account Manager", "Sales Engineer", "Sales Development Representative"],
    "cs": ["Customer Success Manager", "Customer Success Engineer"], "csops": ["CS Operations Analyst"],
    "support": ["Support Specialist", "Senior Support Specialist", "Support Engineer"], "growth": ["Growth Marketing Manager", "Lifecycle Marketing Specialist"],
    "content": ["Content Writer", "Content Marketing Manager"], "devrel": ["Developer Advocate", "Developer Relations Engineer"],
    "comms": ["Communications Manager"], "billingops": ["Billing Operations Specialist", "Billing Analyst"],
    "accounting": ["Accountant", "Payroll Specialist", "Accounts Payable Specialist"], "peopleops": ["People Partner", "People Operations Specialist"],
    "talent": ["Technical Recruiter", "Recruiting Coordinator"], "workplace": ["Office Manager", "Workplace Coordinator"],
    "legal": ["Legal Counsel", "Paralegal"],
}
LEAD_TITLE = {k: f"Head of {v[0]}" for k, v in TEAMS.items()}
LEAD_TITLE.update({"sre": "SRE Manager", "it": "IT Manager", "workspaces": "Engineering Manager, Hosted Workspaces",
                   "runners": "Engineering Manager, Hosted Runners", "editor": "Engineering Manager, Editor", "mobile": "Engineering Manager, Mobile",
                   "identity": "Engineering Manager, Identity & Access", "design": "Head of Design", "sales": "Head of Sales",
                   "growth": "Head of Growth", "content": "Content Lead", "accounting": "Finance Manager", "workplace": "Workplace Manager"})
# Parent team -> the person responsible for it (manager of auto-generated team leads)
DEPT_HEAD = {"exec": "catarina.lobo", "eng": "henrik.aalto", "devprod": "diego.saito", "infra": "joaquim.serrano", "prodeng": "ingrid.holm",
             "security": "daniela.ferraz", "product": "esther.lindahl", "sales": "grant.holloway", "cs": "marcus.oyelowo",
             "marketing": "maya.thornbury", "finance": "miguel.antunes", "people": "ana.sequeira", "legal": "filipa.moura"}
# Common absence statuses (most are empty, as in real chat). No clock times, weekdays or relative-time words.
STATUSES = [""] * 20 + ["In back-to-back meetings", "Out sick", "On annual leave", "On annual leave", "Working from home", "Working from home",
                        "Travelling", "At a conference", "Parental leave", "Focus time"]


def people(seed="gantline-v1"):
    rng = random.Random(seed)
    out, ids = [], set()
    def add(pid, name, title, team, manager, office=None, status=""):
        off = office or TEAMS[team][1]
        out.append({"id": pid, "name": name, "title": title, "team": team, "team_name": TEAMS[team][0], "manager": manager,
                    "office": COMPANY["offices"][off][0], "office_key": off, "timezone": COMPANY["offices"][off][1], "status": status})
        ids.add(pid)
    for pid, name, title, team, mgr, off in KEY:
        add(pid, name, title, team, mgr, off)
    leads = dict(LEADS)
    taken = {tuple(p["name"].split(" ", 1)) for p in out}
    # First and last names of key people are not used for the filled-in staff, to avoid confusion such as two 'Nico' or three 'Osei' in one team
    key_first, key_last = {p["name"].split(" ", 1)[0] for p in out}, {p["name"].split(" ", 1)[1] for p in out}
    pool = [x for x in unique_people(rng, 600) if x not in taken and x[0] not in key_first and x[1] not in key_last]
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
            head_of = DEPT_HEAD.get(parent, "catarina.lobo") if parent and parent != "exec" else DEPT_HEAD.get(team, "catarina.lobo")
            add(pid, f"{fn} {ln}", LEAD_TITLE[team], team, head_of)
            leads[team] = pid
        for _ in range(n):
            fn, ln = next(it); pid = new_id(fn, ln)
            add(pid, f"{fn} {ln}", rng.choice(TITLES[team]), team, leads[team], status=rng.choice(STATUSES))
    for p in out:                                    # Key people with no manager are placed under the team lead
        if p["manager"] is None and p["id"] != "catarina.lobo":
            lead = leads.get(p["team"])
            p["manager"] = lead if lead not in (None, p["id"]) else DEPT_HEAD.get(TEAMS[p["team"]][2] or p["team"], "catarina.lobo")
    return out


def by_id():
    return {p["id"]: p for p in people()}


def email(pid):
    return f"{pid}@{COMPANY['domain']}"


# Company chat channels (shared): name -> (topic, default member teams). "*" = everyone, "@<office key>" = everyone in that office.
_ENG = ["eng", "devprod", "releng", "buildinfra", "qa", "infra", "sre", "lab", "neteng", "prodeng", "workspaces", "runners", "cli", "api",
        "search", "editor", "mobile", "billingeng", "data", "security", "prodsec", "identity"]
CHANNELS = {
    "general": ("Company-wide announcements", ["*"]), "random": ("Anything else", ["*"]),
    "lisbon-office": ("Lisbon HQ — building, lunch, visitors", ["@lisbon"]), "portland-office": ("Portland office", ["@portland"]),
    "it-help": ("IT help", ["*"]),
    "engineering": ("Engineering-wide announcements, RFCs, on-call handovers", _ENG),
    "incidents": ("Active incidents", ["sre", "api", "workspaces", "runners", "neteng", "search", "support"]),
    "releases": ("Release train, CLI and SDK releases", ["releng", "cli", "editor", "mobile", "api", "workspaces", "runners", "qa"]),
    "dev-productivity": ("CI pipelines, internal runner pools, flaky tests", ["devprod", "releng", "buildinfra", "qa"]),
    "buildfarm": ("Builders, registry, build hosts", ["buildinfra", "releng", "sre"]),
    "sre": ("Site reliability", ["infra", "sre", "neteng", "lab"]), "netops": ("Network: DNS, edge, VPN", ["neteng", "sre"]),
    "lab-infra": ("Lab hypervisors, the lab portal, special setups", ["lab", "qa"]),
    "search": ("Search & indexing", ["search", "data"]), "api-platform": ("Public API and SDKs", ["api", "cli"]),
    "security": ("Security", ["security", "prodsec", "identity", "it"]), "identity": ("SSO, groups, provisioning", ["identity", "it", "peopleops"]),
    "cli": ("gnt CLI and SDKs", ["cli", "devrel", "releng"]), "editor": ("Editor — web and desktop", ["editor", "design", "qa"]),
    "mobile": ("Mobile apps", ["mobile", "growth", "design"]),
    "support": ("Developer support", ["support", "cs"]), "billing-ops": ("Billing operations", ["billingops", "billingeng", "finance", "accounting"]),
    "customer-success": ("Customer success", ["cs", "csops", "sales"]), "sales": ("Sales", ["sales", "csops"]),
    "growth": ("Growth & lifecycle", ["growth", "mobile", "product"]), "content": ("Blogs, changelog, newsletter", ["content", "devrel", "comms"]),
    "devrel": ("Developer relations and community", ["devrel", "cli", "content"]),
    "people-ops": ("People operations questions", ["people", "peopleops", "talent", "workplace"]),
    "contracts-help": ("Questions for legal and contracts", ["legal", "sales", "csops"]), "finance": ("Finance", ["finance", "accounting", "billingops"]),
}
# Company systems. Scenario tools (...ctl, ...feed) are listed with the owning team and a narrow purpose: if the description is short, generated documents drag the tool in where it does not belong (e.g. relctl as a deployment tool).
SYSTEMS = ["the Gantline Cloud admin console (customer orgs, plans, seats)", "the helpdesk (support tickets)", "the HR system", "the expenses tool",
           "the CRM", "the status page", "the feature flag service", "the metrics dashboards", "the paging tool", "the password manager",
           "the data warehouse", "the email platform", "chat (the company chat)", "tickets (the change, request and approval tracker)",
           "gnt (our open-source CLI, also used internally to build and test)",
           "creditctl (billing operations only: the queue of customer account credits raised by support)",
           "hrfeed (people operations only: HR data files for outside firms such as recruiting agencies and benefits brokers)",
           "acctfeed (CS operations only: sends customer account data to outside tools)",
           "artifactctl (release engineering: the CI artifact stores)", "cachectl (build infrastructure: the registry's image volumes on the build farm)",
           "buildcfg (per-service build settings: lockfiles and runtimes for the nightly builds)", "labctl (lab team: VM leases on the lab hypervisors)",
           "scratchctl (build infrastructure: job workspaces on the big build hosts)", "blogctl (content team: the blog CMS)",
           "pushctl (growth team: mobile push campaigns)", "dnsctl (network engineering: DNS change sets)",
           "relctl (CLI & SDKs team: publishing gnt and SDK packages to package indexes)"]


if __name__ == "__main__":
    ps = people()
    import collections
    print(len(ps), "people |", dict(collections.Counter(p["timezone"] for p in ps)), "| teams", len({p["team"] for p in ps}))
    for p in ps[:25]: print(f"  {p['id']:22s} {p['title']:40s} {p['team_name']:28s} manager={p['manager']}")
