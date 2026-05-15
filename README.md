# Content Calendar Planner — Streamlit Light Version

A lightweight, externally shareable version of the Content Calendar Planner built for Streamlit Community Cloud.

## Features

- **📅 Calendar View** — Monthly grid with Cebu City 2026 holiday overlays (national, special non-working, local), colour-coded posts by pillar, and post management
- **📊 Performance Tracker** — Log outcomes (Worked / Mixed / Didn't Work), reach, engagement, and clicks per post; breakdown charts by pillar, platform, and format
- **✨ AI Ideas** — Generate theme-based content ideas using Claude AI (requires Anthropic API key); add ideas directly to the calendar
- **📋 Learnings Report** — Compiled from all evaluated posts; breakdown tables + CSV export

## Deploy to Streamlit Community Cloud

1. Fork or clone this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select this repo → set `app.py` as the main file
4. Click **Deploy** — your app will be live at `https://<your-app>.streamlit.app`

No secrets or environment variables required. The Anthropic API key is entered by the user in the app UI and is never stored.

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Business Types Supported

| Feature | Retail / C-Store | Short-Term Rental (Airbnb) |
|---|---|---|
| Content pillars | Promotions, Product, Community, Seasonal | Stay, Area, Guest, Brand, Education |
| Posting frequency | 5–7x/week | 2–3x/week |
| Primary platforms | Instagram, TikTok, Facebook | Instagram, Pinterest, Facebook |
| Content mix target | 30/25/25/20 | 25/20/20/15/20 |

## Holiday Coverage

28 Cebu City 2026 holidays across 4 types:
- 🔴 Regular Holidays (12) — national public holidays
- 🟡 Special Non-Working Days (11) — including ASEAN Summit May 6–8 (Cebu City only)
- 🟣 Local Holidays (2) — Sinulog (Jan 18), Cebu City Charter Day (Feb 24)
- 🟡 Cebu Province (2) — Provincial Charter Day, Osmeña Day

---

*Built on best practices · Co-built with Manus*
