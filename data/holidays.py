"""
Cebu City 2026 Holidays — national, special non-working, local
Sources: Proclamation No. 1236, 1239 (ASEAN Summit), local ordinances
"""

HOLIDAYS_2026 = [
    # ── Regular / National Holidays ──────────────────────────────────────────
    {"date": "2026-01-01", "name": "New Year's Day",            "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-04-02", "name": "Maundy Thursday",           "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-04-03", "name": "Good Friday",               "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-04-09", "name": "Araw ng Kagitingan",        "type": "regular",              "scope": "national", "note": "Day of Valor"},
    {"date": "2026-05-01", "name": "Labor Day",                 "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-06-12", "name": "Independence Day",          "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-08-31", "name": "National Heroes Day",       "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-11-30", "name": "Bonifacio Day",             "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-12-25", "name": "Christmas Day",             "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-12-30", "name": "Rizal Day",                 "type": "regular",              "scope": "national", "note": None},
    {"date": "2026-06-26", "name": "Eid'l Fitr",                "type": "regular",              "scope": "national", "note": "Tentative — subject to moon sighting"},
    {"date": "2026-09-04", "name": "Eid'l Adha",                "type": "regular",              "scope": "national", "note": "Tentative — subject to moon sighting"},

    # ── Special Non-Working Days ──────────────────────────────────────────────
    {"date": "2026-01-28", "name": "Chinese New Year",          "type": "special-non-working",  "scope": "national", "note": "Year of the Horse"},
    {"date": "2026-02-25", "name": "EDSA People Power",         "type": "special-non-working",  "scope": "national", "note": "40th anniversary"},
    {"date": "2026-04-04", "name": "Black Saturday",            "type": "special-non-working",  "scope": "national", "note": None},
    {"date": "2026-08-21", "name": "Ninoy Aquino Day",          "type": "special-non-working",  "scope": "national", "note": None},
    {"date": "2026-11-01", "name": "All Saints' Day",           "type": "special-non-working",  "scope": "national", "note": None},
    {"date": "2026-11-02", "name": "All Souls' Day",            "type": "special-non-working",  "scope": "national", "note": None},
    {"date": "2026-12-08", "name": "Feast of the Immaculate Conception", "type": "special-non-working", "scope": "national", "note": None},
    {"date": "2026-12-24", "name": "Christmas Eve",             "type": "special-non-working",  "scope": "national", "note": None},
    {"date": "2026-12-31", "name": "New Year's Eve",            "type": "special-non-working",  "scope": "national", "note": None},

    # ── ASEAN Summit — Cebu City & Mandaue City only ─────────────────────────
    {"date": "2026-05-06", "name": "48th ASEAN Summit",         "type": "special-non-working",  "scope": "cebu-city", "note": "Cebu City & Mandaue City only (Proc. 1239)"},
    {"date": "2026-05-07", "name": "48th ASEAN Summit",         "type": "special-non-working",  "scope": "cebu-city", "note": "Cebu City & Mandaue City only (Proc. 1239)"},
    {"date": "2026-05-08", "name": "48th ASEAN Summit",         "type": "special-non-working",  "scope": "cebu-city", "note": "Cebu City & Mandaue City only (Proc. 1239)"},

    # ── Local Cebu City Holidays ──────────────────────────────────────────────
    {"date": "2026-01-18", "name": "Sinulog Festival",          "type": "local",                "scope": "cebu-city", "note": "Feast of the Santo Niño — biggest Cebu City holiday"},
    {"date": "2026-02-24", "name": "Cebu City Charter Day",     "type": "local",                "scope": "cebu-city", "note": "City of Cebu founding anniversary"},

    # ── Cebu Province ─────────────────────────────────────────────────────────
    {"date": "2026-08-06", "name": "Cebu Provincial Charter Day", "type": "special-non-working", "scope": "cebu-province", "note": "Province of Cebu founding anniversary"},
    {"date": "2026-09-09", "name": "Osmeña Day",                "type": "special-non-working",  "scope": "cebu-province", "note": "Sergio Osmeña Sr. birth anniversary"},
]

HOLIDAY_TYPE_CONFIG = {
    "regular":              {"label": "Regular Holiday",       "icon": "🔴", "color": "#FEE2E2", "border": "#EF4444", "text": "#991B1B"},
    "special-non-working":  {"label": "Special Non-Working",   "icon": "🟡", "color": "#FEF9C3", "border": "#EAB308", "text": "#713F12"},
    "local":                {"label": "Local Holiday",         "icon": "🟣", "color": "#F3E8FF", "border": "#A855F7", "text": "#6B21A8"},
    "special-working":      {"label": "Special Working Day",   "icon": "🟢", "color": "#DCFCE7", "border": "#22C55E", "text": "#14532D"},
}

def get_holidays_for_month(year: int, month: int) -> list:
    prefix = f"{year}-{str(month).zfill(2)}"
    return [h for h in HOLIDAYS_2026 if h["date"].startswith(prefix)]

def get_holidays_for_date(date_str: str) -> list:
    return [h for h in HOLIDAYS_2026 if h["date"] == date_str]
