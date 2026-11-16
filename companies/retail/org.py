# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Company: Mossgrove (retail), a shared organisation. The scenarios assigned to retail use the same people, teams and time zones.
Generated deterministically (fixed seed): wherever it is loaded from, the same person has the same title, team, manager and time zone.
Key people (department heads, scenario roles) are written by hand; the rest are filled from the name pool (scenarios.common.unique_people)."""
import random

from scenarios.common import unique_people

COMPANY = {
    "name": "Mossgrove", "legal_name": "Mossgrove Outdoor & Home Ltd", "domain": "mossgroveoutdoor.co.uk",
    "what": "Outdoor clothing, camping kit and homeware — online shop (UK, IE, US), 61 stores in the UK and Ireland, and a wholesale arm that supplies independent outdoor shops and garden centres.",
    "headcount": 2400,
    "offices": {"leeds": ("Leeds (HQ)", "Europe/London"), "dublin": ("Dublin (tech hub)", "Europe/Dublin"),
                "columbus": ("Columbus, OH (US e-commerce & fulfilment)", "America/New_York"), "wakefield": ("Wakefield DC", "Europe/London")},
    "fiscal_year_start": "February",
}

# Teams: key -> (display name, office, parent team key)
TEAMS = {
    "exec": ("Executive team", "leeds", None),
    "finance": ("Finance", "leeds", "exec"), "finops": ("Finance operations", "leeds", "finance"), "ap": ("Accounts payable", "leeds", "finance"),
    "credit": ("Credit control (wholesale)", "leeds", "finance"), "payroll": ("Payroll", "leeds", "finance"), "fpa": ("FP&A", "leeds", "finance"),
    "risk": ("Fraud & payments risk", "leeds", "finance"),
    "support": ("Customer support", "columbus", "exec"), "disputes": ("Disputes & chargebacks", "leeds", "support"),
    "marketing": ("Marketing", "leeds", "exec"), "perf": ("Performance marketing", "leeds", "marketing"), "crm": ("CRM & lifecycle", "dublin", "marketing"),
    "brand": ("Brand studio", "leeds", "marketing"), "pr": ("Press & comms", "leeds", "marketing"),
    "ecom": ("E-commerce product", "dublin", "exec"), "checkout": ("Checkout", "dublin", "ecom"), "pricing": ("Pricing & promotions", "leeds", "ecom"),
    "membership": ("Membership & billing", "dublin", "ecom"),
    "eng": ("Engineering", "dublin", "exec"), "platform": ("Platform & SRE", "dublin", "eng"), "web": ("Web (shop-web, orders-web)", "dublin", "eng"),
    "payplat": ("Payments platform (billing-api)", "dublin", "eng"), "dataeng": ("Data engineering", "dublin", "eng"), "ml": ("Machine learning (recommendations)", "dublin", "eng"),
    "security": ("Security engineering", "dublin", "eng"), "it": ("IT & service desk", "leeds", "eng"), "releases": ("Release management", "dublin", "eng"),
    "stores": ("Retail operations", "leeds", "exec"), "wholesale": ("Wholesale sales", "leeds", "exec"), "supply": ("Supply chain & fulfilment", "wakefield", "exec"),
    "people": ("People team", "leeds", "exec"), "legal": ("Legal", "leeds", "exec"),
}

# Key people: (id, name, title, team, manager id or None, office override or None)
KEY = [
    ("helen.garside", "Helen Garside", "Chief Executive Officer", "exec", None, None),
    ("oliver.brandt", "Oliver Brandt", "Chief Financial Officer", "exec", "helen.garside", None),
    ("siobhan.keane", "Siobhan Keane", "Chief Technology Officer", "exec", "helen.garside", "dublin"),
    ("martin.ashby", "Martin Ashby", "Chief Operating Officer", "exec", "helen.garside", None),
    ("rachel.okonjo", "Rachel Okonjo", "Chief Marketing Officer", "exec", "helen.garside", None),
    ("daniel.pryor", "Daniel Pryor", "General Counsel", "legal", "helen.garside", None),
    ("amrita.sethi", "Amrita Sethi", "Chief People Officer", "people", "helen.garside", None),
    ("priya.nair", "Priya Nair", "Head of Finance Operations", "finops", "oliver.brandt", None),
    ("jordan.reyes", "Jordan Reyes", "Finance Operations Analyst", "finops", "priya.nair", None),
    ("marta.kowalski", "Marta Kowalski", "Head of Fraud & Payments Risk", "risk", "oliver.brandt", None),
    ("graham.pike", "Graham Pike", "Credit Control Manager", "credit", "oliver.brandt", None),
    ("nadia.farouk", "Nadia Farouk", "Credit Controller", "credit", "graham.pike", None),
    ("tom.whitlock", "Tom Whitlock", "Financial Controller", "finance", "oliver.brandt", None),
    ("imani.brooks", "Imani Brooks", "Support Team Lead", "support", None, None),
    ("renata.vogel", "Renata Vogel", "Support Operations Manager", "support", None, None),
    ("owen.castillo", "Owen Castillo", "Senior Site Reliability Engineer", "platform", None, None),
    ("sasha.lindeman", "Sasha Lindeman", "Machine Learning Engineer", "ml", None, None),
    ("dana.vasilenko", "Dana Vasilenko", "Platform Engineer", "platform", None, None),
    ("priya.raman", "Priya Raman", "Senior Engineer, Payments Platform", "payplat", None, None),
    ("dana.whitfield", "Dana Whitfield", "Release Manager", "releases", "siobhan.keane", None),
]
# Team leads (manager of the auto-generated staff): one per team, generated if no key person leads the team
FILL = {"finops": 6, "ap": 5, "credit": 3, "payroll": 4, "fpa": 3, "risk": 4, "support": 8, "disputes": 3, "perf": 3, "crm": 4, "brand": 3,
        "pr": 2, "checkout": 5, "pricing": 3, "membership": 3, "platform": 7, "web": 6, "payplat": 5, "dataeng": 5, "ml": 5, "security": 4,
        "it": 4, "releases": 2, "stores": 5, "wholesale": 3, "supply": 4, "people": 3, "legal": 2}
TITLES = {
    "finops": ["Finance Operations Analyst", "Senior Finance Operations Analyst", "Payments Reconciliation Analyst"],
    "ap": ["Accounts Payable Clerk", "Accounts Payable Specialist", "AP Team Lead"], "credit": ["Credit Controller", "Credit Control Assistant"],
    "payroll": ["Payroll Specialist", "Payroll Administrator"], "fpa": ["FP&A Analyst", "Senior FP&A Analyst"], "risk": ["Fraud Analyst", "Payments Risk Analyst"],
    "support": ["Customer Support Advisor", "Senior Support Advisor", "Support Quality Lead"], "disputes": ["Disputes Specialist", "Chargeback Analyst"],
    "perf": ["Performance Marketing Manager", "Paid Social Specialist"], "crm": ["CRM Manager", "Lifecycle Marketing Executive", "Email Developer"],
    "brand": ["Senior Designer", "Photographer", "Studio Coordinator"], "pr": ["Press Officer", "Communications Manager"],
    "checkout": ["Product Manager, Checkout", "Senior Software Engineer", "Software Engineer"], "pricing": ["Pricing Analyst", "Promotions Manager"],
    "membership": ["Product Manager, Membership", "Software Engineer"], "platform": ["Site Reliability Engineer", "Platform Engineer", "Senior Platform Engineer"],
    "web": ["Software Engineer", "Senior Software Engineer", "Frontend Engineer"], "payplat": ["Software Engineer", "Senior Software Engineer"],
    "dataeng": ["Data Engineer", "Senior Data Engineer", "Analytics Engineer"], "ml": ["Machine Learning Engineer", "Data Scientist", "Senior Data Scientist"],
    "security": ["Security Engineer", "Senior Security Engineer", "GRC Analyst"], "it": ["IT Support Analyst", "Systems Administrator"],
    "releases": ["Release Coordinator"], "stores": ["Regional Operations Manager", "Store Systems Analyst"], "wholesale": ["Account Manager, Wholesale"],
    "supply": ["Inventory Planner", "Fulfilment Systems Analyst"], "people": ["People Partner", "Recruiter"], "legal": ["Legal Counsel", "Paralegal"],
}
LEAD_TITLE = {k: f"Head of {v[0][0].upper() + v[0][1:]}" for k, v in TEAMS.items()}
LEAD_TITLE.update({"ap": "Accounts Payable Manager", "payroll": "Payroll Manager", "fpa": "Head of FP&A", "disputes": "Disputes Manager",
                   "brand": "Studio Manager", "pr": "Head of Communications", "platform": "Head of Platform & SRE", "web": "Engineering Manager, Web",
                   "payplat": "Engineering Manager, Payments Platform", "dataeng": "Data Engineering Manager", "ml": "ML Engineering Manager",
                   "security": "Head of Security Engineering", "it": "IT Manager", "stores": "Head of Retail Operations", "wholesale": "Head of Wholesale",
                   "supply": "Head of Supply Chain", "people": "People Operations Manager", "legal": "Senior Legal Counsel",
                   "support": "Head of Customer Support", "perf": "Head of Performance Marketing", "crm": "Head of CRM & Lifecycle",
                   "pricing": "Head of Pricing & Promotions", "membership": "Head of Membership & Billing"})
# Parent team -> the executive responsible for it (manager of auto-generated team leads)
DEPT_HEAD = {"exec": "helen.garside", "finance": "oliver.brandt", "support": "martin.ashby", "marketing": "rachel.okonjo", "ecom": "siobhan.keane",
             "eng": "siobhan.keane", "stores": "martin.ashby", "wholesale": "martin.ashby", "supply": "martin.ashby", "people": "amrita.sethi", "legal": "daniel.pryor"}
# Common absence statuses (most are empty, as in real chat)
STATUSES = [""] * 14 + ["In back-to-back meetings", "Out sick", "On annual leave", "At the Wakefield DC today", "Working from home", "Travelling"]


def people(seed="mossgrove-v1"):
    rng = random.Random(seed)
    out, ids = [], set()
    def add(pid, name, title, team, manager, office=None, status=""):
        off = office or TEAMS[team][1]
        out.append({"id": pid, "name": name, "title": title, "team": team, "team_name": TEAMS[team][0], "manager": manager,
                    "office": COMPANY["offices"][off][0], "office_key": off, "timezone": COMPANY["offices"][off][1], "status": status})
        ids.add(pid)
    for pid, name, title, team, mgr, off in KEY:
        add(pid, name, title, team, mgr, off)
    leads = {"finops": "priya.nair", "risk": "marta.kowalski", "credit": "graham.pike", "releases": "dana.whitfield"}   # Teams led by key people
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
            head_of = DEPT_HEAD.get(parent, "helen.garside") if parent and parent != "exec" else DEPT_HEAD.get(team, "helen.garside")
            add(pid, f"{fn} {ln}", LEAD_TITLE[team], team, head_of)
            leads[team] = pid
        for _ in range(n):
            fn, ln = next(it); pid = new_id(fn, ln)
            add(pid, f"{fn} {ln}", rng.choice(TITLES[team]), team, leads[team], status=rng.choice(STATUSES))
    for p in out:                                    # Key people with no manager are placed under the team lead
        if p["manager"] is None and p["id"] != "helen.garside":
            p["manager"] = leads.get(p["team"]) if leads.get(p["team"]) not in (None, p["id"]) else DEPT_HEAD.get(TEAMS[p["team"]][2] or p["team"], "helen.garside")
    return out


def by_id():
    return {p["id"]: p for p in people()}


def email(pid):
    return f"{pid}@{COMPANY['domain']}"


if __name__ == "__main__":
    ps = people()
    import collections
    print(len(ps), "people |", dict(collections.Counter(p["timezone"] for p in ps)))
    for p in ps[:25]: print(f"  {p['id']:22s} {p['title']:40s} {p['team_name']:32s} manager={p['manager']}")


# Company chat channels (shared): name -> (topic, default member teams)
CHANNELS = {
    "general": ("Company-wide announcements", ["*"]), "random": ("Anything else", ["*"]), "leeds-office": ("Leeds HQ — building, parking, lunch", ["@leeds"]),
    "dublin-office": ("Dublin office", ["@dublin"]), "finance-ops": ("Finance operations", ["finops", "risk", "finance"]), "ap-team": ("Accounts payable", ["ap"]),
    "credit-control": ("Wholesale credit control", ["credit", "wholesale"]), "payroll": ("Payroll questions", ["payroll", "people"]),
    "support-leads": ("Support team leads", ["support", "disputes"]), "disputes": ("Disputes & chargebacks", ["disputes", "risk", "finops"]),
    "marketing": ("Marketing team", ["perf", "crm", "brand", "pr", "marketing"]), "crm": ("CRM & lifecycle email", ["crm", "dataeng"]),
    "brand-studio": ("Studio, shoots, assets", ["brand"]), "checkout": ("Checkout squad", ["checkout", "web"]), "pricing": ("Pricing & promotions", ["pricing", "finops"]),
    "platform": ("Platform & SRE", ["platform", "security", "web"]),       # the web team is here too (shop-web runbook: there is no #shop-web channel, #platform is used)
    "incidents": ("Active incidents", ["platform", "web", "payplat", "support"]),
    "releases": ("Release coordination", ["releases", "web", "payplat", "checkout", "membership"]), "payments-platform": ("billing-api and payments services", ["payplat", "membership", "finops"]),
    "data-eng": ("Data engineering", ["dataeng", "ml"]), "ml-recs": ("Recommendations", ["ml", "checkout"]), "security": ("Security engineering", ["security", "it"]),
    "it-help": ("IT help", ["*"]), "stores-ops": ("Store operations", ["stores", "supply"]), "wholesale": ("Wholesale accounts", ["wholesale", "credit"]),
}
SYSTEMS = ["ledgerctl (finance ledger CLI)", "sharectl (data sharing CLI)", "snapctl (VM snapshots)", "jobctl (GPU cluster scheduler)", "logctl (log storage tiers)",
           "mailer (outbound customer email)", "deployctl (deploys)", "tickets (change and request tracker)", "chat (the company chat)",
           "the helpdesk (support tickets)", "the POS back office (stores)", "the CRM", "the analytics warehouse", "the feature flag service", "the expenses tool", "the HR system"]
