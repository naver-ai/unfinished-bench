# Unfinished-Bench
# Copyright (c) 2026-present NAVER Corp.
# Apache-2.0
"""Company: Brakwater Geo (geospatial data and AI analytics), a shared organisation. The 13 scenarios assigned to data_ai use the same people, teams and time zones.
Generated deterministically (fixed seed): wherever it is loaded from, the same person has the same title, team, manager and time zone.
Key people (department heads, people named in scenarios) are written by hand (same ids as in the scenario modules); the rest are filled from the name pool (scenarios.common.unique_people).
Scenario anchor times are mostly around 10:00Z, so the scenario user sits in Rotterdam (around local noon). Only c6 (15:00Z) is in Denver (09:00 local)."""
import random

from scenarios.common import unique_people

COMPANY = {
    "name": "Brakwater", "legal_name": "Brakwater Geo B.V.", "domain": "brakwatergeo.com",
    "what": "Geospatial data and analytics from satellite imagery and our own ground sensor network — flood and water monitoring for water boards and ports, "
            "crop and soil monitoring for agricultural co-ops and insurers, sold as monitoring subscriptions, imagery tasking orders and an analytics API. "
            "We train our own earth observation models on the imagery archive.",
    "headcount": 310,
    "offices": {"rotterdam": ("Rotterdam (HQ)", "Europe/Amsterdam"), "denver": ("Denver (US office)", "America/Denver")},
    "fiscal_year_start": "January",
}

# Teams: key -> (display name, office, parent team key)
TEAMS = {
    "exec": ("Executive team", "rotterdam", None),
    # Finance
    "finance": ("Finance", "rotterdam", "exec"), "finops": ("FinOps (cloud cost)", "rotterdam", "finance"),
    "fpa": ("FP&A and finance analytics", "rotterdam", "finance"), "accounting": ("Accounting, AP and payroll", "rotterdam", "finance"),
    "procurement": ("Procurement", "rotterdam", "finance"),
    # Engineering
    "eng": ("Engineering", "rotterdam", "exec"), "cloudplat": ("Cloud platform", "rotterdam", "eng"),
    "batch": ("Batch compute", "rotterdam", "eng"), "cloudsec": ("Cloud security", "rotterdam", "eng"),
    "apps": ("Web app and API", "rotterdam", "eng"), "discovery": ("Catalogue search and ranking", "rotterdam", "eng"),
    "supportsys": ("Support systems", "rotterdam", "eng"), "it": ("IT and workplace", "rotterdam", "eng"),
    "product": ("Product management", "rotterdam", "eng"),
    # Data
    "data": ("Data", "rotterdam", "exec"), "dataeng": ("Data engineering", "rotterdam", "data"),
    "warehouse": ("Analytics warehouse", "rotterdam", "data"), "reporting": ("BI and reporting", "rotterdam", "data"),
    "pricing": ("Pricing and commercial analytics", "rotterdam", "data"), "datagov": ("Data governance and open data", "rotterdam", "data"),
    # Geo operations
    "geoops": ("Geo operations", "rotterdam", "exec"), "imagery": ("Imagery acquisition and processing", "rotterdam", "geoops"),
    "sensorops": ("Ground sensor network", "rotterdam", "geoops"),
    # ML
    "ml": ("Machine learning", "rotterdam", "exec"), "mlplat": ("ML platform (training cluster and serving)", "rotterdam", "ml"),
    "eomodels": ("Earth observation models", "rotterdam", "ml"), "changedet": ("Change detection models", "denver", "ml"),
    "appliedml": ("Applied ML (customer models)", "rotterdam", "ml"),
    # Legal and risk
    "legal": ("Legal and compliance", "rotterdam", "exec"), "modelgov": ("Model governance", "rotterdam", "legal"),
    # Commercial
    "commercial": ("Commercial", "denver", "exec"), "sales": ("Sales", "denver", "commercial"),
    "partnerships": ("Partnerships", "rotterdam", "commercial"), "custsuccess": ("Customer success and delivery", "denver", "commercial"),
    "support": ("Customer support", "rotterdam", "commercial"),
    # Marketing and communications
    "marketing": ("Marketing", "denver", "exec"), "comms": ("Brand and communications", "rotterdam", "marketing"),
    "people": ("People team", "rotterdam", "exec"),
}

# Key people: (id, name, title, team, manager id or None, office override or None)
# People from scenario modules keep the module's id (some titles are adjusted slightly to fit this company's organisation).
KEY = [
    # Executives and department heads
    ("maartje.verhoeven", "Maartje Verhoeven", "Chief Executive Officer", "exec", None, None),
    ("ruben.dewit", "Ruben de Wit", "Chief Technology Officer", "exec", "maartje.verhoeven", None),
    ("tom.keane", "Tom Keane", "VP Finance", "finance", "maartje.verhoeven", None),                       # c1-reserved-instances
    ("sofia.rossi", "Sofia Rossi", "Head of Data", "data", "maartje.verhoeven", None),                     # c1-cloud-budget-cap
    ("hugo.brandsma", "Hugo Brandsma", "VP Machine Learning", "ml", "maartje.verhoeven", None),
    ("joost.hendriks", "Joost Hendriks", "VP Geo Operations", "geoops", "maartje.verhoeven", None),
    ("liesbeth.kramer", "Liesbeth Kramer", "General Counsel", "legal", "maartje.verhoeven", None),
    ("marcus.ellery", "Marcus Ellery", "Chief Commercial Officer", "commercial", "maartje.verhoeven", None),
    ("shauna.petrakis", "Shauna Petrakis", "VP Marketing", "marketing", "maartje.verhoeven", None),
    ("femke.jansen", "Femke Jansen", "Head of People", "people", "maartje.verhoeven", None),
    # Finance: c1-cloud-budget-cap, c1-reserved-instances, c3-table-archive-drop
    ("beatriz.almeida", "Beatriz Almeida", "FinOps Lead", "finops", "tom.keane", None),
    ("ines.carvalho", "Ines Carvalho", "FinOps Analyst", "finops", "beatriz.almeida", None),
    ("leon.fischer", "Leon Fischer", "Head of FP&A and Finance Analytics", "fpa", "tom.keane", None),
    ("adaeze.okafor", "Adaeze Okafor", "Finance Business Partner, Technology", "fpa", "leon.fischer", None),
    ("raj.chandra", "Raj Chandra", "Finance Analyst", "fpa", "leon.fischer", None),
    # Cloud platform and batch: c1-cloud-budget-cap, c1-reserved-instances, c3-records, c4-batch-kill
    ("felix.okonjo", "Felix Okonjo", "Head of Platform", "cloudplat", "ruben.dewit", None),
    ("callum.brennan", "Callum Brennan", "Platform Engineer", "cloudplat", "felix.okonjo", None),
    ("kasia.nowak", "Kasia Nowak", "Platform Engineer", "cloudplat", "felix.okonjo", None),
    ("jae.park", "Jae Park", "Site Reliability Engineer", "cloudplat", "felix.okonjo", None),
    ("simone.obi", "Simone Obi", "Site Reliability Engineer", "cloudplat", "felix.okonjo", None),
    ("nadia.arslan", "Nadia Arslan", "Platform Engineer, Batch", "batch", None, None),
    # Product engineering: c1-cloud-budget-cap (web-prod), c4-batch-kill, c6-social-announcement
    ("freya.lund", "Freya Lund", "Engineering Manager, Web App and API", "apps", "ruben.dewit", None),
    ("leah.becker", "Leah Becker", "Senior Software Engineer", "apps", "freya.lund", None),
    ("ivan.petrov", "Ivan Petrov", "Search Engineer", "discovery", None, None),
    ("priya.nair", "Priya Nair", "ML Engineer, Ranking", "discovery", None, None),
    ("aarav.mehta", "Aarav Mehta", "Product Manager", "product", None, None),
    # Support systems: c3-records
    ("eero.schmidt", "Eero Schmidt", "Support Systems Manager", "supportsys", "ruben.dewit", None),
    ("marisol.kiplagat", "Marisol Kiplagat", "Support Platform Engineer", "supportsys", "eero.schmidt", None),
    # Data: c1-cloud-budget-cap, c1-reserved-instances, c3-table-archive-drop, c4-db-session-kill, c4-batch-kill, c2-public-dataset
    ("joanna.kowalski", "Joanna Kowalski", "Data Engineering Lead", "dataeng", "sofia.rossi", None),
    ("mei.tanaka", "Mei Tanaka", "Data Engineer", "dataeng", "joanna.kowalski", None),
    ("mira.solheim", "Mira Solheim", "Data Engineer", "dataeng", "joanna.kowalski", None),
    ("owen.gallagher", "Owen Gallagher", "Data Platform Lead", "warehouse", "sofia.rossi", None),
    ("ines.moreau", "Ines Moreau", "Analytics Engineer", "warehouse", "owen.gallagher", None),
    ("zeynep.kaya", "Zeynep Kaya", "Data Engineer", "warehouse", "owen.gallagher", None),
    ("kaito.mori", "Kaito Mori", "Data Platform DBA", "warehouse", "owen.gallagher", None),
    ("priya.raman", "Priya Raman", "Platform Engineer, Data Platform", "warehouse", "owen.gallagher", None),
    ("marta.silva", "Marta Silva", "Senior Data Platform Engineer", "warehouse", "owen.gallagher", None),
    ("dana.kovac", "Dana Kovac", "Analytics Engineer", "reporting", None, None),
    ("aran.dey", "Aran Dey", "BI Analyst", "reporting", None, None),
    ("theo.varga", "Theo Varga", "Data Engineer", "pricing", None, None),
    ("lena.fischer", "Lena Fischer", "Data Scientist", "pricing", None, None),
    ("omar.haddad", "Omar Haddad", "Analytics Engineer", "pricing", None, None),
    ("clara.bianchi", "Clara Bianchi", "Head of Data Governance", "datagov", "sofia.rossi", None),
    ("rupert.anand", "Rupert Anand", "Data Governance Lead", "datagov", "clara.bianchi", None),
    ("isla.penrose", "Isla Penrose", "Data and Information Officer", "datagov", "rupert.anand", None),
    ("kwabena.asare", "Kwabena Asare", "GIS Analyst", "datagov", "rupert.anand", None),
    # Ground sensor network: c2-public-dataset
    ("grainne.oleary", "Grainne O'Leary", "Sensor Network Team Lead", "sensorops", "joost.hendriks", None),
    # ML — c4-train-checkpoints, c7-model-deploy-eval-gate, c1-cloud-budget-cap(ml-research)
    ("bo.vasquez", "Bo Vasquez", "ML Platform Lead", "mlplat", "hugo.brandsma", None),
    ("rosa.esposito", "Rosa Esposito", "ML Platform Engineer", "mlplat", "bo.vasquez", None),
    ("kalani.walsh", "Kalani Walsh", "Site Reliability Engineer, ML Platform", "mlplat", "bo.vasquez", None),
    ("ben.hughes", "Ben Hughes", "ML Platform Engineer", "mlplat", "bo.vasquez", None),
    ("bruno.olsen", "Bruno Olsen", "Research Scientist", "eomodels", None, None),
    ("elias.asante", "Elias Asante", "Evaluation Lead", "eomodels", None, None),
    ("rania.nielsen", "Rania Nielsen", "Research Engineer", "eomodels", None, None),
    ("sebastian.lee", "Sebastian Lee", "Research Scientist", "eomodels", None, None),
    ("magnus.pereira", "Magnus Pereira", "Research Engineer", "eomodels", None, None),
    ("diego.tanaka", "Diego Tanaka", "Research Scientist", "eomodels", None, None),
    ("laszlo.fonseca", "Laszlo Fonseca", "Research Engineer", "eomodels", None, None),
    ("rahul.iyer", "Rahul Iyer", "Senior Research Scientist", "eomodels", None, None),
    ("georgia.demir", "Georgia Demir", "Research Scientist", "changedet", None, None),
    ("sofia.teixeira", "Sofia Teixeira", "Engineering Manager, Applied ML", "appliedml", "hugo.brandsma", None),
    ("tomas.varga", "Tomas Varga", "ML Engineer", "appliedml", "sofia.teixeira", None),
    ("priya.iyer", "Priya Iyer", "Data Scientist", "appliedml", "sofia.teixeira", None),
    ("gaurav.mishra", "Gaurav Mishra", "ML Engineer", "appliedml", "sofia.teixeira", None),
    ("lucia.marchetti", "Lucia Marchetti", "Data Scientist", "appliedml", "sofia.teixeira", None),
    # Legal and model governance: c3-records, c7-model-deploy-eval-gate
    ("mina.novak", "Mina Novak", "Data Protection Officer", "legal", "liesbeth.kramer", None),
    ("rania.jaramillo", "Rania Jaramillo", "Compliance Manager", "legal", "liesbeth.kramer", None),
    ("jasmine.barros", "Jasmine Barros", "Compliance Analyst", "legal", "rania.jaramillo", None),
    ("imani.okafor", "Imani Okafor", "Model Risk Lead", "modelgov", "liesbeth.kramer", None),
    ("henrik.dahl", "Henrik Dahl", "Model Governance Analyst", "modelgov", "imani.okafor", None),
    # Customer support: c3-records, c3-table-archive-drop, c6-social-announcement, c7-model-deploy-eval-gate
    ("wanjiru.kiplagat", "Wanjiru Kiplagat", "Support Operations Manager", "support", "marcus.ellery", None),
    ("diego.ramos", "Diego Ramos", "Support Lead, Americas", "support", "wanjiru.kiplagat", "denver"),
    ("nico.brooks", "Nico Brooks", "Customer Experience Lead", "support", "wanjiru.kiplagat", None),
    ("karim.rossi", "Karim Rossi", "Support Quality Lead", "support", "wanjiru.kiplagat", None),
    ("nina.park", "Nina Park", "Support Insights Lead", "support", "wanjiru.kiplagat", None),
    # Marketing, communications and HR: c6-social-announcement
    ("callum.reid", "Callum Reid", "Product Marketing Manager", "marketing", "shauna.petrakis", None),
    ("mirela.constantin", "Mirela Constantin", "Head of Brand and Communications", "comms", "shauna.petrakis", None),
    ("jasmine.cole", "Jasmine Cole", "Social Media Manager", "comms", "mirela.constantin", "denver"),
    ("nina.petrova", "Nina Petrova", "Brand Designer", "comms", "mirela.constantin", None),
    ("sam.okoro", "Sam Okoro", "People Partner", "people", "femke.jansen", "denver"),
]
# Teams led by key people (for the other teams the team lead is generated from the name pool)
LEADS = {"finops": "beatriz.almeida", "fpa": "leon.fischer", "cloudplat": "felix.okonjo", "apps": "freya.lund", "supportsys": "eero.schmidt",
         "dataeng": "joanna.kowalski", "warehouse": "owen.gallagher", "datagov": "clara.bianchi", "sensorops": "grainne.oleary",
         "mlplat": "bo.vasquez", "appliedml": "sofia.teixeira", "modelgov": "imani.okafor", "legal": "liesbeth.kramer",
         "support": "wanjiru.kiplagat", "marketing": "shauna.petrakis", "comms": "mirela.constantin", "people": "femke.jansen"}
# Auto-generated staff (excluding team leads)
FILL = {"finops": 2, "fpa": 3, "accounting": 4, "procurement": 2, "cloudplat": 4, "batch": 2, "cloudsec": 4, "apps": 5, "discovery": 3,
        "supportsys": 2, "it": 3, "product": 3, "dataeng": 4, "warehouse": 2, "reporting": 3, "pricing": 2, "datagov": 2, "imagery": 5,
        "sensorops": 4, "mlplat": 3, "eomodels": 3, "changedet": 4, "appliedml": 3, "modelgov": 2, "legal": 2, "sales": 4, "partnerships": 2,
        "custsuccess": 5, "support": 5, "marketing": 4, "comms": 2, "people": 3}
# Teams spanning two offices: this share of the auto-generated staff sit in the other office
SPLIT = {"support": ("denver", 0.4), "sales": ("rotterdam", 0.3), "custsuccess": ("rotterdam", 0.35), "it": ("denver", 0.3),
         "people": ("denver", 0.3), "apps": ("denver", 0.2), "marketing": ("rotterdam", 0.3)}
TITLES = {
    "finops": ["FinOps Analyst", "Cloud Cost Analyst"], "fpa": ["FP&A Analyst", "Senior FP&A Analyst", "Finance Analyst"],
    "accounting": ["Accountant", "Senior Accountant", "Accounts Payable Specialist", "Payroll Administrator"],
    "procurement": ["Procurement Specialist", "Vendor Manager"],
    "cloudplat": ["Platform Engineer", "Senior Platform Engineer", "Site Reliability Engineer"], "batch": ["Platform Engineer, Batch", "Senior Platform Engineer"],
    "cloudsec": ["Security Engineer", "Senior Security Engineer", "Cloud Security Engineer", "GRC Analyst"],
    "apps": ["Software Engineer", "Senior Software Engineer", "Frontend Engineer", "Backend Engineer"],
    "discovery": ["Search Engineer", "ML Engineer, Ranking", "Software Engineer"], "supportsys": ["Support Platform Engineer", "Systems Administrator"],
    "it": ["IT Support Analyst", "Systems Administrator", "Workplace Coordinator"], "product": ["Product Manager", "Senior Product Manager", "Product Designer"],
    "dataeng": ["Data Engineer", "Senior Data Engineer"], "warehouse": ["Analytics Engineer", "Data Platform Engineer", "Senior Analytics Engineer"],
    "reporting": ["BI Analyst", "BI Developer", "Analytics Engineer"], "pricing": ["Data Scientist", "Pricing Analyst", "Analytics Engineer"],
    "datagov": ["Data Governance Analyst", "Data Steward", "Open Data Officer"],
    "imagery": ["Imagery Analyst", "Remote Sensing Engineer", "Imagery Operations Specialist", "Geospatial Engineer"],
    "sensorops": ["Field Technician", "Sensor Network Engineer", "Hydrometric Technician"],
    "mlplat": ["ML Platform Engineer", "Site Reliability Engineer, ML Platform"], "eomodels": ["Research Scientist", "Research Engineer", "Senior Research Scientist"],
    "changedet": ["Research Scientist", "ML Engineer", "Senior ML Engineer"], "appliedml": ["ML Engineer", "Data Scientist", "Senior ML Engineer"],
    "modelgov": ["Model Governance Analyst", "Model Risk Analyst"], "legal": ["Legal Counsel", "Paralegal", "Privacy Analyst"],
    "sales": ["Account Executive", "Sales Engineer", "Account Manager"], "partnerships": ["Partnerships Manager", "Research Partnerships Manager"],
    "custsuccess": ["Customer Success Manager", "Delivery Specialist", "Solutions Engineer"],
    "support": ["Support Specialist", "Senior Support Specialist", "Technical Support Engineer"],
    "marketing": ["Content Marketing Manager", "Marketing Operations Specialist", "Demand Generation Manager", "Product Marketing Manager"],
    "comms": ["Communications Manager", "Content Editor"], "people": ["People Partner", "Recruiter", "People Operations Specialist"],
}
LEAD_TITLE = {k: f"Head of {v[0][0].upper() + v[0][1:]}" for k, v in TEAMS.items()}
LEAD_TITLE.update({"accounting": "Financial Controller", "procurement": "Procurement Manager", "batch": "Batch Compute Lead",
                   "cloudsec": "Head of Cloud Security", "discovery": "Engineering Manager, Search and Ranking", "it": "IT Manager",
                   "product": "Head of Product", "reporting": "BI and Reporting Lead", "pricing": "Head of Pricing Analytics",
                   "imagery": "Head of Imagery Operations", "eomodels": "Head of Earth Observation Models", "changedet": "Change Detection Lead",
                   "sales": "VP Sales, Americas", "partnerships": "Head of Partnerships", "custsuccess": "Head of Customer Success"})
# Parent team -> the executive responsible for it (manager of auto-generated team leads)
DEPT_HEAD = {"exec": "maartje.verhoeven", "finance": "tom.keane", "eng": "ruben.dewit", "data": "sofia.rossi", "ml": "hugo.brandsma",
             "geoops": "joost.hendriks", "legal": "liesbeth.kramer", "commercial": "marcus.ellery", "marketing": "shauna.petrakis", "people": "femke.jansen"}
# Common absence statuses (most are empty, as in real chat). No clock times, weekdays or relative-time words.
STATUSES = [""] * 18 + ["In back-to-back meetings", "Out sick", "On annual leave", "On annual leave", "Working from home", "Travelling",
                         "Heads down", "On parental leave"]


def people(seed="brakwater-v1"):
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
    taken = {tuple(p["name"].split(" ", 1)) for p in out} | {(p["name"].split()[0], p["name"].split()[-1]) for p in out}
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
            head_of = DEPT_HEAD.get(parent, "maartje.verhoeven") if parent and parent != "exec" else DEPT_HEAD.get(team, "maartje.verhoeven")
            add(pid, f"{fn} {ln}", LEAD_TITLE[team], team, head_of)
            leads[team] = pid
        for _ in range(n):
            fn, ln = next(it); pid = new_id(fn, ln)
            off = None
            if team in SPLIT and rng.random() < SPLIT[team][1]:
                off = SPLIT[team][0]
            add(pid, f"{fn} {ln}", rng.choice(TITLES[team]), team, leads[team], office=off, status=rng.choice(STATUSES))
    for p in out:                                    # Key people with no manager are placed under the team lead
        if p["manager"] is None and p["id"] != "maartje.verhoeven":
            p["manager"] = leads.get(p["team"]) if leads.get(p["team"]) not in (None, p["id"]) else DEPT_HEAD.get(TEAMS[p["team"]][2] or p["team"], "maartje.verhoeven")
    return out


def by_id():
    return {p["id"]: p for p in people()}


def email(pid):
    return f"{pid}@{COMPANY['domain']}"


# Company chat channels (shared): name -> (topic, default member teams). "*" = everyone, "@office" = everyone in that office.
CHANNELS = {
    "announcements": ("Company-wide announcements", ["*"]), "random": ("Anything else", ["*"]), "it-help": ("IT help", ["*"]),
    "ask-people": ("Leave, payroll, benefits and other people-team questions", ["*"]),
    "rotterdam-office": ("Rotterdam office — building, bikes, lunch", ["@rotterdam"]), "denver-office": ("Denver office", ["@denver"]),
    "finance": ("Finance team", ["finance", "fpa", "accounting", "procurement", "finops"]),
    "finops": ("Cloud spend, budgets, commitments and the monthly cost report", ["finops", "fpa", "cloudplat", "dataeng", "mlplat"]),
    "cloud-platform": ("Cloud platform and SRE", ["cloudplat", "batch", "cloudsec"]), "security": ("Cloud security", ["cloudsec", "it", "cloudplat"]),
    "incidents": ("Active incidents", ["cloudplat", "batch", "apps", "mlplat", "support", "supportsys", "imagery"]),
    "batch-cluster": ("Shared batch cluster — pool, scheduling, outages", ["batch", "pricing", "discovery", "dataeng", "imagery"]),
    "apps": ("Web app and analytics API", ["apps", "product", "discovery"]),
    "data-eng": ("Data engineering", ["dataeng", "warehouse", "pricing"]), "data-platform": ("Analytics warehouse, loads, pooling", ["warehouse", "dataeng", "reporting"]),
    "bi": ("Dashboards and scheduled BI", ["reporting", "fpa", "pricing"]),
    "data-governance": ("Data governance, the catalogue, access and open data", ["datagov", "legal", "warehouse"]),
    "imagery-ops": ("Imagery acquisition, processing and the catalogue", ["imagery", "discovery", "custsuccess"]),
    "sensor-network": ("Ground sensor network and field team", ["sensorops", "datagov", "imagery"]),
    "ml-platform": ("Training cluster, scratch, modelhub and serving", ["mlplat", "eomodels", "changedet", "appliedml"]),
    "eo-models": ("Earth observation model research", ["eomodels", "changedet"]), "applied-ml": ("Customer-facing models", ["appliedml", "product"]),
    "model-governance": ("Release reviews and model risk", ["modelgov", "appliedml", "eomodels"]),
    "support": ("Customer support", ["support", "supportsys", "custsuccess"]),
    "sales": ("Sales, partnerships and customer success", ["sales", "partnerships", "custsuccess", "commercial"]),
    "marketing": ("Marketing and communications", ["marketing", "comms", "product"]),
}
# Company systems (scenario tools plus ordinary systems)
SYSTEMS = ["costctl (cloud budgets and job sizing)", "commitctl (cloud reservations and savings plans)", "opendata (open data hub publishing)",
           "recordsctl (support case records store)", "whctl (warehouse tables and prepared changes)", "wh-sessions (warehouse connections)",
           "batchctl (shared batch pool)", "runsctl (training scratch run directories)", "modelctl (model serving and rollouts)",
           "socialctl (social scheduler)", "tickets (change and request tracker)", "chat (the company chat)",
           "the imagery catalogue", "the tasking portal (satellite orders)", "the customer API console", "the data catalogue", "the notebook server",
           "the workflow scheduler (pipelines)", "the helpdesk (customer support tickets)", "the CRM", "the BI dashboards", "the HR system",
           "the expenses tool", "the travel desk", "the IT service desk", "the password manager", "the status page", "the field app (sensor visits)"]


if __name__ == "__main__":
    ps = people()
    import collections
    print(len(ps), "people |", dict(collections.Counter(p["timezone"] for p in ps)))
    for p in ps[:25]: print(f"  {p['id']:22s} {p['title']:40s} {p['team_name']:32s} manager={p['manager']}")
