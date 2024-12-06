# !/usr/bin/env python3
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import asyncio

# -------- CONFIGURATION --------
DATABASE_URL = "mysql+pymysql://root:root@localhost/Python_email_Files"
EMAIL_SENDER = "rakeshbarthipaka@gmail.com"
EMAIL_PASSWORD = "hfzf cxnb xajq tntk"  # Replace this with your actual app password
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# Database setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# -------- DATABASE MODELS --------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

# -------- EMAIL SENDING FUNCTION --------
async def send_email(to_email, subject, body):
    try:
        # Create email message
        message = MIMEMultipart()
        message["From"] = EMAIL_SENDER
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "html"))

        # Send email using aiosmtplib
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=EMAIL_SENDER,
            password=EMAIL_PASSWORD,
        )
        print(f"Email successfully sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# -------- DISCOUNT EMAIL FUNCTION --------
async def send_discount_email():
    db = SessionLocal()
    email_count = 0
    try:
        users = db.query(User).all()
        for user in users:
            subject = "Exclusive 50% Discount Just for You!"
            body = f"""
            <p>Hello {user.name},</p>
            <p>We are excited to announce an exclusive <strong>50% discount</strong> offer on our services! 🎉</p>
            <p>Don't miss out—this special deal is available for a limited time only.</p>
            <p>Visit our website to claim your discount and enjoy premium benefits at half the price!</p>
            <p>Best regards,<br>The Team</p>
            """
            await send_email(user.email, subject, body)
            email_count += 1
        print(f"Total emails sent: {email_count}")
    finally:
        db.close()
# import aiocron
# @aiocron.crontab("*/5 * * * *")
async def scheduled_task():
    print("Running scheduled task...")
    await send_discount_email()