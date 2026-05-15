"""
Business configurations and sample data for Retail (7-Eleven type) and Airbnb/STR.
"""

RETAIL_CONFIG = {
    "type": "retail",
    "label": "Retail / C-Store (7-Eleven type)",
    "tagline": "Drive foot traffic, highlight promotions, and build community around everyday moments.",
    "accent": "#C84B11",
    "accent_light": "#FEF0E7",
    "posting_frequency": "5–7x per week",
    "primary_platforms": ["Instagram", "TikTok", "Facebook"],
    "pillars": [
        {"id": "promo",     "name": "Promotions & Offers",   "color": "#EF4444", "target_pct": 30,
         "description": "Discounts, loyalty rewards, limited-time deals, and bundle offers.",
         "best_practice": "Lead with the value — put the discount or offer in the first line. Use urgency words like 'today only' or 'while stocks last.' Always include the expiry date.",
         "formats": ["Story", "Reel", "Image"],
         "examples": ["Buy 2 get 1 free on all energy drinks this weekend", "Loyalty members: 20% off all hot food today only"]},
        {"id": "product",   "name": "Product Spotlights",    "color": "#F97316", "target_pct": 25,
         "description": "Feature specific products, new arrivals, seasonal items, and bestsellers.",
         "best_practice": "Use close-up, well-lit product photography. Show the product in context — someone holding it, using it, or enjoying it. Avoid flat lay only.",
         "formats": ["Image", "Reel", "Carousel"],
         "examples": ["New arrival: Matcha Latte now in-store", "Staff pick of the week: Spicy Tuna Onigiri"]},
        {"id": "community", "name": "Community & Lifestyle",  "color": "#22C55E", "target_pct": 25,
         "description": "Customer shoutouts, behind-the-scenes, staff features, local community moments.",
         "best_practice": "Show real people. Feature staff, customers, and local community moments. Authenticity outperforms polish here — raw, relatable content wins.",
         "formats": ["Reel", "Story", "Image"],
         "examples": ["Meet the team: our night shift crew keeping Cebu fueled", "Customer shoutout: @username's go-to midnight snack run"]},
        {"id": "seasonal",  "name": "Seasonal & Occasions",  "color": "#8B5CF6", "target_pct": 20,
         "description": "Holiday tie-ins, local events, seasonal promotions, and occasion-based content.",
         "best_practice": "Plan 2 weeks ahead for major holidays. Tie product promotions directly to the occasion. Use local cultural references — Sinulog, Hari Raya, local fiestas.",
         "formats": ["Reel", "Story", "Carousel"],
         "examples": ["Sinulog 2026: fuel your festival with our Slurpee deals", "Chinese New Year: lucky snack bundles now available"]},
    ],
    "best_practices": [
        {"icon": "📅", "title": "Post Consistently", "desc": "5–7x per week minimum. Gaps in posting hurt algorithm reach. Use a content calendar to plan 2 weeks ahead."},
        {"icon": "🎬", "title": "Lead with Reels", "desc": "Reels get 3x more reach than static images on Instagram. Aim for 30–60 second Reels for product and promo content."},
        {"icon": "🏷️", "title": "Promo Cap at 30%", "desc": "Never exceed 30% promotional content. Audiences unfollow accounts that feel like ads. Balance with community and lifestyle."},
        {"icon": "📍", "title": "Geo-tag Every Post", "desc": "Always tag your store location. Local discovery is a major traffic driver for C-stores."},
        {"icon": "⏰", "title": "Post at Peak Hours", "desc": "Best times: 7–9am (morning commute), 12–1pm (lunch), 9–11pm (late night snack). Test and optimise per platform."},
    ],
    "cadence": [
        {"platform": "Instagram", "frequency": "1x daily", "best_times": "7am, 12pm, 9pm", "priority": "Primary"},
        {"platform": "TikTok",    "frequency": "3–5x per week", "best_times": "6pm–9pm", "priority": "Primary"},
        {"platform": "Facebook",  "frequency": "3–4x per week", "best_times": "12pm, 7pm", "priority": "Secondary"},
        {"platform": "Pinterest", "frequency": "Optional", "best_times": "Evening", "priority": "Optional"},
    ],
}

AIRBNB_CONFIG = {
    "type": "airbnb",
    "label": "Short-Term Rental / Airbnb",
    "tagline": "Drive bookings, build trust, and showcase the experience of staying with you.",
    "accent": "#00897B",
    "accent_light": "#E0F2F1",
    "posting_frequency": "2–3x per week",
    "primary_platforms": ["Instagram", "Pinterest", "Facebook"],
    "pillars": [
        {"id": "stay",      "name": "The Stay Experience",    "color": "#0EA5E9", "target_pct": 25,
         "description": "Property photos, room tours, amenities, unique features, and ambiance.",
         "best_practice": "Use natural light photography. Show the full guest journey — arrival, bedroom, bathroom, common areas, view. Video walkthroughs outperform static images for bookings.",
         "formats": ["Reel", "Carousel", "Image"],
         "examples": ["Morning light in our sea-view suite — wake up to this every day", "Full property walkthrough: 3BR villa with private pool in Cebu"]},
        {"id": "area",      "name": "Local Area & Guides",    "color": "#10B981", "target_pct": 20,
         "description": "Local restaurants, attractions, hidden gems, travel tips, and neighbourhood guides.",
         "best_practice": "Position yourself as the local expert. Guests book experiences, not just rooms. Share your personal recommendations — this builds trust and differentiates from hotels.",
         "formats": ["Carousel", "Reel", "Story"],
         "examples": ["Our top 5 hidden restaurants within 10 minutes of the property", "Weekend itinerary: the perfect 48 hours in Cebu City"]},
        {"id": "guest",     "name": "Guest Stories & Reviews", "color": "#F59E0B", "target_pct": 20,
         "description": "Guest testimonials, review highlights, before/after stays, and guest shoutouts.",
         "best_practice": "Always get permission before featuring guests. Screenshot 5-star reviews and turn them into graphics. Video testimonials convert 4x better than text reviews.",
         "formats": ["Story", "Image", "Reel"],
         "examples": ["'Best stay in Cebu' — thank you @username for this amazing review", "Guest highlight: a family reunion at our villa last weekend"]},
        {"id": "brand",     "name": "Brand & Host Story",     "color": "#EC4899", "target_pct": 15,
         "description": "Host introduction, property story, values, behind-the-scenes, and what makes you different.",
         "best_practice": "People book from people they trust. Show your face, tell your story, share why you host. Authenticity drives direct bookings and repeat guests.",
         "formats": ["Reel", "Story", "Image"],
         "examples": ["Why I started hosting: our family's story behind this property", "Behind the scenes: how we prepare for every guest arrival"]},
        {"id": "education", "name": "Travel Tips & Education", "color": "#6366F1", "target_pct": 20,
         "description": "Travel tips, packing guides, local event calendars, visa info, and seasonal advice.",
         "best_practice": "Educational content gets saved and shared — the highest-value engagement signals. Create 'save-worthy' posts like packing lists, local event guides, and travel hacks.",
         "formats": ["Carousel", "Reel", "Story"],
         "examples": ["Cebu travel checklist: everything you need to pack for a beach trip", "Best time to visit Cebu: month-by-month weather and events guide"]},
    ],
    "best_practices": [
        {"icon": "📸", "title": "Invest in Photography", "desc": "Professional photos increase bookings by up to 40%. Natural light, wide angles, and lifestyle shots outperform empty-room shots."},
        {"icon": "⭐", "title": "Reviews as Content", "desc": "Turn every 5-star review into a post. Guest social proof is your most powerful booking driver — more than any ad."},
        {"icon": "🗺️", "title": "Be the Local Expert", "desc": "Guests choose STRs over hotels for the local experience. Regular local guides and recommendations build a loyal following."},
        {"icon": "📅", "title": "Post Around Booking Windows", "desc": "Most bookings happen 4–8 weeks out. Increase posting frequency 6–8 weeks before peak seasons (holidays, fiestas, events)."},
        {"icon": "🔗", "title": "Always Include a Booking Link", "desc": "Every post should have a clear path to book. Use link-in-bio tools and include your Airbnb/direct booking URL in every caption."},
    ],
    "cadence": [
        {"platform": "Instagram", "frequency": "3–4x per week", "best_times": "8am, 6pm", "priority": "Primary"},
        {"platform": "Pinterest", "frequency": "5–7x per week", "best_times": "Evening", "priority": "Primary"},
        {"platform": "Facebook",  "frequency": "2–3x per week", "best_times": "12pm, 7pm", "priority": "Secondary"},
        {"platform": "TikTok",    "frequency": "1–2x per week", "best_times": "6pm–9pm", "priority": "Optional"},
    ],
}

CONFIGS = {"retail": RETAIL_CONFIG, "airbnb": AIRBNB_CONFIG}

PLATFORMS = ["Instagram", "TikTok", "Facebook", "Pinterest", "YouTube", "Twitter/X"]
FORMATS   = ["Reel", "Story", "Image", "Carousel", "Video", "Live", "Text"]
STATUSES  = ["Idea", "Draft", "Scheduled", "Published"]
OUTCOMES  = ["Worked ✅", "Mixed 🔶", "Didn't Work ❌"]

STATUS_COLORS = {
    "Idea":      "#F3F4F6",
    "Draft":     "#FEF9C3",
    "Scheduled": "#DBEAFE",
    "Published": "#DCFCE7",
}

OUTCOME_COLORS = {
    "Worked ✅":      {"bg": "#DCFCE7", "text": "#166534", "icon": "✅"},
    "Mixed 🔶":       {"bg": "#FEF9C3", "text": "#713F12", "icon": "🔶"},
    "Didn't Work ❌": {"bg": "#FEE2E2", "text": "#991B1B", "icon": "❌"},
}

SAMPLE_POSTS_RETAIL = [
    {"id": "r1",  "date": "2026-05-01", "title": "Weekend Flash Sale",         "platform": "Instagram", "format": "Story",    "pillar": "promo",     "caption": "This weekend only: Buy any 2 drinks, get 1 FREE! 🔥 Valid May 1–3 only. Don't miss out!", "cta": "Visit us in-store", "status": "Published", "outcome": "Worked ✅",      "reach": 4200, "engagement": 380, "clicks": 95,  "notes": "High story views, strong swipe-up rate"},
    {"id": "r2",  "date": "2026-05-02", "title": "New Arrival: Matcha Latte",  "platform": "Instagram", "format": "Image",    "pillar": "product",   "caption": "New in store: Matcha Latte 🍵 Smooth, creamy, and the perfect afternoon pick-me-up.", "cta": "Try it today", "status": "Published", "outcome": "Mixed 🔶",        "reach": 2100, "engagement": 145, "clicks": 32,  "notes": "Good reach but lower engagement than expected"},
    {"id": "r3",  "date": "2026-05-05", "title": "3AM Snack Run Reel",         "platform": "TikTok",    "format": "Reel",     "pillar": "community", "caption": "POV: It's 3AM and you need snacks 🌙 We're always here for you. #7Eleven #LateNight", "cta": "Tag a friend who needs this", "status": "Published", "outcome": "Worked ✅", "reach": 18500, "engagement": 2100, "clicks": 0, "notes": "Viral format — relatable late-night content"},
    {"id": "r4",  "date": "2026-05-06", "title": "ASEAN Summit Special",       "platform": "Instagram", "format": "Story",    "pillar": "seasonal",  "caption": "Welcome to Cebu, world leaders! 🇵🇭 Fuel your ASEAN week with our special bundle deals.", "cta": "In-store only", "status": "Published", "outcome": "Worked ✅", "reach": 5600, "engagement": 490, "clicks": 0, "notes": "Timely local content — strong local reach"},
    {"id": "r5",  "date": "2026-05-09", "title": "Loyalty Member Spotlight",   "platform": "Facebook",  "format": "Image",    "pillar": "community", "caption": "Shoutout to our most loyal customer this month! 🏆 You've earned 500 points — keep it up!", "cta": "Join our loyalty program", "status": "Published", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r6",  "date": "2026-05-12", "title": "Top 5 Lunchbox Snacks",      "platform": "Instagram", "format": "Carousel", "pillar": "product",   "caption": "School's back! Here are our top 5 lunchbox snacks under ₱50 each 🎒", "cta": "Shop in-store", "status": "Scheduled", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r7",  "date": "2026-05-14", "title": "Customer Shoutout",          "platform": "Instagram", "format": "Story",    "pillar": "community", "caption": "Thank you @cebu_foodie for this amazing review! You made our day ❤️", "cta": "Share your experience", "status": "Draft", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r8",  "date": "2026-05-16", "title": "Ramadan Special Bundles",    "platform": "Facebook",  "format": "Image",    "pillar": "seasonal",  "caption": "Ramadan Mubarak! 🌙 Special iftar snack bundles available now. Perfect for breaking fast.", "cta": "Available in-store", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r9",  "date": "2026-05-19", "title": "Slurpee Day Countdown",      "platform": "TikTok",    "format": "Reel",     "pillar": "promo",     "caption": "7.11 is coming! 🥤 Mark your calendars for FREE Slurpee Day. Who's joining us?", "cta": "Save the date", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r10", "date": "2026-05-21", "title": "Staff Pick of the Week",     "platform": "Instagram", "format": "Image",    "pillar": "product",   "caption": "This week's staff pick: Spicy Tuna Onigiri 🍙 Our team can't stop eating these!", "cta": "Try it before it sells out", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r11", "date": "2026-05-23", "title": "Meet the Team",              "platform": "Instagram", "format": "Reel",     "pillar": "community", "caption": "Meet the faces behind your favourite store! 👋 Our night shift crew keeping Cebu fueled 24/7.", "cta": "Come say hi", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "r12", "date": "2026-05-26", "title": "Summer Essentials Promo",    "platform": "Instagram", "format": "Carousel", "pillar": "seasonal",  "caption": "Beat the Cebu heat ☀️ Our summer essentials: sunscreen, cold drinks, and snacks. All in one stop.", "cta": "Shop now", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
]

SAMPLE_POSTS_AIRBNB = [
    {"id": "a1",  "date": "2026-05-02", "title": "Morning View Reel",           "platform": "Instagram", "format": "Reel",     "pillar": "stay",      "caption": "Wake up to this every morning ☀️ Our sea-view suite in Cebu City — now available for June bookings.", "cta": "Link in bio to book", "status": "Published", "outcome": "Worked ✅",      "reach": 8900, "engagement": 920, "clicks": 145, "notes": "Best performing post this month — sunrise content works"},
    {"id": "a2",  "date": "2026-05-04", "title": "Top 5 Hidden Restaurants",    "platform": "Instagram", "format": "Carousel", "pillar": "area",      "caption": "Our top 5 hidden restaurants within 10 minutes of the property 🍜 Saved by 400+ guests!", "cta": "Save this post", "status": "Published", "outcome": "Worked ✅",      "reach": 12400, "engagement": 1850, "clicks": 89, "notes": "Carousel saves are very high — educational content wins"},
    {"id": "a3",  "date": "2026-05-07", "title": "ASEAN Week in Cebu",          "platform": "Facebook",  "format": "Image",    "pillar": "area",      "caption": "Cebu is in the spotlight this week! 🌏 ASEAN Summit 2026 — explore the city while world leaders meet here.", "cta": "Book your stay", "status": "Published", "outcome": "Mixed 🔶",        "reach": 3200, "engagement": 210, "clicks": 28, "notes": "Reach was good but low booking intent"},
    {"id": "a4",  "date": "2026-05-09", "title": "Guest Review Spotlight",      "platform": "Instagram", "format": "Story",    "pillar": "guest",     "caption": "'Best stay in Cebu City — the view is unreal and the host is incredibly helpful!' ⭐⭐⭐⭐⭐", "cta": "Book now — link in bio", "status": "Published", "outcome": "Worked ✅", "reach": 5100, "engagement": 430, "clicks": 67, "notes": "Review stories drive direct bookings"},
    {"id": "a5",  "date": "2026-05-11", "title": "Property Walkthrough Video",  "platform": "Instagram", "format": "Reel",     "pillar": "stay",      "caption": "Full walkthrough of our 3BR villa with private pool 🏊 Perfect for families and groups.", "cta": "Check availability", "status": "Scheduled", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a6",  "date": "2026-05-14", "title": "Weekend Itinerary Guide",     "platform": "Instagram", "format": "Carousel", "pillar": "education", "caption": "The perfect 48 hours in Cebu City 🗺️ Our guest-tested itinerary from arrival to departure.", "cta": "Save for your trip", "status": "Draft", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a7",  "date": "2026-05-16", "title": "Host Story: Why We Host",     "platform": "Instagram", "format": "Reel",     "pillar": "brand",     "caption": "Why did we start hosting? Our family's story behind this property and what it means to us 🏡", "cta": "Book a stay with us", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a8",  "date": "2026-05-19", "title": "Cebu Packing Checklist",      "platform": "Pinterest", "format": "Image",    "pillar": "education", "caption": "Everything you need to pack for a Cebu beach trip ✅ Save this before your trip!", "cta": "Save this pin", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a9",  "date": "2026-05-21", "title": "Family Reunion Feature",      "platform": "Facebook",  "format": "Image",    "pillar": "guest",     "caption": "A beautiful family reunion at our villa last weekend 👨‍👩‍👧‍👦 Thank you for choosing us for this special moment!", "cta": "Enquire for group bookings", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a10", "date": "2026-05-23", "title": "Sinulog 2027 Early Bird",     "platform": "Instagram", "format": "Story",    "pillar": "seasonal",  "caption": "Sinulog 2027 is 8 months away — and our calendar is already filling up 🎉 Book early for the best rates.", "cta": "Book now", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a11", "date": "2026-05-26", "title": "Sunset Terrace Reel",         "platform": "Instagram", "format": "Reel",     "pillar": "stay",      "caption": "Our terrace at golden hour 🌅 The kind of view that makes you never want to leave.", "cta": "Book your sunset stay", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
    {"id": "a12", "date": "2026-05-28", "title": "Local Market Guide",          "platform": "Pinterest", "format": "Carousel", "pillar": "area",      "caption": "The best local markets in Cebu City 🛒 Our guide to fresh produce, street food, and hidden finds.", "cta": "Save for your trip", "status": "Idea", "outcome": None, "reach": None, "engagement": None, "clicks": None, "notes": None},
]

SAMPLE_POSTS = {"retail": SAMPLE_POSTS_RETAIL, "airbnb": SAMPLE_POSTS_AIRBNB}
