import resend
import asyncio
from functools import partial
from app.config import settings

resend.api_key = settings.RESEND_API_KEY

async def send_email(to: str, subject: str, html: str):
    try:
        # In sandbox mode, Resend only allows sending to your own address
        recipient = to if settings.ENVIRONMENT == "production" else settings.NOTIFY_EMAIL
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            partial(resend.Emails.send, {
                "from": settings.FROM_EMAIL,
                "to": recipient,
                "subject": f"[DEV → {to}] {subject}",
                "html": html,
            })
        )
    except Exception as e:
        print(f"[email error] {e}")

# --- Notification emails to you ---

async def notify_access_request(name: str, email: str, about: str, user_type: str):
    await send_email(
        to=settings.NOTIFY_EMAIL,
        subject=f"[Questin] New {user_type} access request — {name}",
        html=f"""
        <h3>New access request</h3>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Type:</b> {user_type}</p>
        <p><b>About:</b> {about}</p>
        <hr/>
        <p>Approve or reject via the admin API.</p>
        """
    )

async def notify_venue_request(poc: str, phone: str, community_id: int, dates: str, capacity: str, revenue: str, notes: str | None):
    await send_email(
        to=settings.NOTIFY_EMAIL,
        subject=f"[Questin] Venue request for community #{community_id} — {poc}",
        html=f"""
        <h3>New venue request</h3>
        <p><b>POC:</b> {poc}</p>
        <p><b>Phone:</b> {phone}</p>
        <p><b>Community ID:</b> {community_id}</p>
        <p><b>Preferred dates:</b> {dates}</p>
        <p><b>Capacity:</b> {capacity}</p>
        <p><b>Revenue model:</b> {revenue}</p>
        <p><b>Notes:</b> {notes or "—"}</p>
        """
    )

async def notify_pitch(community_name: str, organizer: str, email: str, category: str, description: str):
    await send_email(
        to=settings.NOTIFY_EMAIL,
        subject=f"[Questin] New community pitch — {community_name}",
        html=f"""
        <h3>New pitch</h3>
        <p><b>Community:</b> {community_name}</p>
        <p><b>Organizer:</b> {organizer} ({email})</p>
        <p><b>Category:</b> {category}</p>
        <p><b>Description:</b> {description}</p>
        """
    )

async def notify_waitlist(email: str):
    await send_email(
        to=settings.NOTIFY_EMAIL,
        subject=f"[Questin] New waitlist signup — {email}",
        html=f"<p>{email} just joined the waitlist.</p>"
    )


# --- User-facing emails ---

async def send_access_approved(to_email: str, name: str, token: str):
    access_link = f"{settings.FRONTEND_URL}?token={token}"
    await send_email(
        to=to_email,
        subject="You're in — Questin catalogue access",
        html=f"""
        <h2>You've been approved, {name}.</h2>
        <p>Click the link below to access the Questin community catalogue:</p>
        <p><a href="{access_link}" style="background:#CDFF00;color:#0A0A0A;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:700;display:inline-block;">Open catalogue →</a></p>
        <p style="color:#888;font-size:12px;margin-top:24px;">This link is personal to you. Valid for 7 days.</p>
        """
    )

async def send_access_rejected(to_email: str, name: str):
    await send_email(
        to=to_email,
        subject="Questin — update on your access request",
        html=f"""
        <h2>Hey {name},</h2>
        <p>Thanks for your interest in Questin. We reviewed your request and we're not moving forward at this time.</p>
        <p>If you think this was a mistake or want to reapply, just reply to this email.</p>
        """
    )