import asyncio
from app.database import AsyncSessionLocal
from app.models.community import Community

communities = [
    Community(
        name="flib.lab", 
        tagline="Art therapy disguised as a good time. Sculpt, paint, forget your phone.", 
        category="Creative", 
        group_size="10–20", 
        price_range="₹700–800", 
        duration="2–3 hrs", 
        venue_needs="Indoor, tables, water, 20+ cap", 
        frequency="Monthly", 
        image_url="https://images.unsplash.com/photo-1460661419201-fd4cecdf8a8b?w=600&h=300&fit=crop",
        # Added real contact data below:
        contact_name="Aryan Shah",
        contact_email="aryan@fliblab.in",
        contact_phone="+91 98765 43210"
    ),
    Community(
        name="The Sketch Collective", 
        tagline="Urban sketching through Jaipur's lanes. Pencils out, golden hour mandatory.", 
        category="Creative", 
        group_size="8–15", 
        price_range="₹400–600", 
        duration="2 hrs", 
        venue_needs="Outdoor or semi-covered, seating optional", 
        frequency="Bi-weekly", 
        image_url="https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=600&h=300&fit=crop",
        # Added mock contact data:
        contact_name="Jaipur Sketch Lead",
        contact_email="sketch.jaipur@example.com",
        contact_phone="+91 99999 88888"
    ),
    Community(
        name="Smash League", 
        tagline="Intermediate badminton. No beginners. No mercy. Just proper games.", 
        category="Sports", 
        group_size="8–12", 
        price_range="₹300–500", 
        duration="1.5–2 hrs", 
        venue_needs="Indoor court, lighting, water", 
        frequency="Weekly", 
        image_url="https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=600&h=300&fit=crop",
        # Added mock contact data:
        contact_name="Smash Admin",
        contact_email="smash.league@example.com",
        contact_phone="+91 77777 66666"
    ),
]

async def seed():
    async with AsyncSessionLocal() as db:
        db.add_all(communities)
        await db.commit()
        print("Seeded 3 communities with contact information.")

asyncio.run(seed())