import os

import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_confirmation_to_user(user_email: str, user_name: str, project_name: str):
    """Send confirmation email to user who submitted the form"""
    try:
        resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": user_email,
                "subject": f"We received your enquiry — {project_name}",
                "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #333;">Thank you for contacting us!</h2>
                <p>Dear <strong>{user_name}</strong>,</p>
                <p>We have received your enquiry and our team will get back to you as soon as possible.</p>
                <p>We typically respond within <strong>24-48 hours</strong>.</p>
                <br>
                <p>Best regards,</p>
                <p><strong>{project_name} Team</strong></p>
                <hr style="border: 1px solid #eee; margin: 20px 0;">
                <p style="color: #999; font-size: 12px;">This is an automated message. Please do not reply to this email.</p>
            </div>
            """,
            }
        )
        return True
    except Exception as e:
        print(f"Failed to send user email: {e}")
        return False


def send_notification_to_admin(
    admin_email: str,
    user_name: str,
    user_email: str,
    user_phone: str,
    message: str,
    project_name: str,
    subject: str = None,
):
    """Send notification email to you when someone submits the form"""
    try:
        resend.Emails.send(
            {
                "from": "onboarding@resend.dev",
                "to": admin_email,
                "subject": f"New Enquiry from {user_name} — {project_name}",
                "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #e74c3c;">New Contact Form Submission</h2>
                <p><strong>Project:</strong> {project_name}</p>
                <hr style="border: 1px solid #eee;">
                <h3>Contact Details:</h3>
                <p><strong>Name:</strong> {user_name}</p>
                <p><strong>Email:</strong> {user_email}</p>
                <p><strong>Phone:</strong> {user_phone or 'Not provided'}</p>
                <p><strong>Subject:</strong> {subject or 'Not provided'}</p>
                <h3>Message:</h3>
                <p style="background: #f9f9f9; padding: 15px; border-radius: 5px;">{message or 'No message'}</p>
                <hr style="border: 1px solid #eee;">
                <p style="color: #999; font-size: 12px;">Reply directly to {user_email} to respond.</p>
            </div>
            """,
            }
        )
        return True
    except Exception as e:
        print(f"Failed to send admin email: {e}")
        return False
