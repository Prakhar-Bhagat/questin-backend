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
async def notify_venue_status_update(
    to_email: str,
    poc_name: str,
    new_status: str,
    community_name: str,
    community_contact_name: str | None = None,
    community_contact_email: str | None = None,
    community_contact_phone: str | None = None,
):
    subject_status = "Approved! 🎉" if new_status == "approved" else "Update"

    contact_block = ""
    if new_status == "approved" and any([community_contact_name, community_contact_email, community_contact_phone]):
        contact_block = f"""
        <div style="margin-top:24px;padding:16px;background:#f9f9f9;border-radius:8px;border:1px solid #eee;">
            <p style="font-weight:700;margin-bottom:8px;">Community contact details</p>
            {"<p>"+community_contact_name+"</p>" if community_contact_name else ""}
            {"<p><a href='mailto:"+community_contact_email+"'>"+community_contact_email+"</a></p>" if community_contact_email else ""}
            {"<p>"+community_contact_phone+"</p>" if community_contact_phone else ""}
        </div>
        <p style="margin-top:16px;color:#888;font-size:13px;">Reach out to them directly to coordinate dates and logistics.</p>
        """

    await send_email(
        to=to_email,
        subject=f"Questin — {subject_status} on your venue request for {community_name}",
        html=f"""
        <h2>Hi {poc_name},</h2>
        <p>Your venue request for <b>{community_name}</b> has been marked as <b>{new_status}</b>.</p>
        {contact_block}
        <p style="margin-top:24px;color:#888;font-size:13px;">Questions? Just reply to this email.</p>
        """
    )
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