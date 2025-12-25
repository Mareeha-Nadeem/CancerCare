# 📧 Email Notification System - Setup Guide

## ✅ What Was Implemented

### 1. Email Service (`core/email_service.py`)
- SMTP email sending (Gmail/Outlook compatible)
- HTML email templates
- Async email delivery
- Statistics tracking

### 2. Email Templates
**Prediction Report Email:**
- Professional HTML design
- Color-coded risk levels (High=Red, Medium=Yellow, Low=Green)
- Includes confidence score
- Personalized recommendations
- Call-to-action button

**Appointment Notification Email:**
- Appointment details (doctor, date, time)
- Location information
- Important notes and reminders
- Professional formatting

### 3. Database Updates
- Added `email` field to Patient model
- Email validation support
- Backward compatible

## 🔧 Setup Instructions

### Step 1: Configure Email Settings

Add to your `.env` file:

```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=CancerCare Lab
```

**For Gmail Users:**
1. Go to Google Account Settings
2. Security → 2-Step Verification → App Passwords
3. Generate app password for "Mail"
4. Use that password (not your regular Gmail password)

**For Outlook/Other:**
- SMTP_SERVER: smtp-mail.outlook.com (Outlook)
- SMTP_PORT: 587
- Update credentials accordingly

### Step 2: Update Database

The email field has been added to the Patient model. Run:

```bash
python -c "from core.models import Base; from core.db_config import engine; Base.metadata.create_all(engine)"
```

### Step 3: Test Email Sending

```python
from core.email_service import email_service

# Test email
email_service.send_prediction_report(
    patient_email="patient@example.com",
    patient_name="John Doe",
    risk_level="High",
    confidence=0.87,
    recommendations="Immediate consultation recommended."
)
```

## 📨 How It Works

### Automatic Emails Sent When:

1. **Prediction Completed:**
   - Patient receives detailed risk assessment
   - Color-coded results
   - Personalized recommendations
   - Link to view full report

2. **Appointment Scheduled:**
   - Confirmation email sent
   - Appointment details
   - Location and timing
   - Preparation instructions

### Email Flow:

```
Lab Tech Action
     ↓
Email Service (async)
     ↓
SMTP Server (Gmail/Outlook)
     ↓
Patient's Email Inbox
```

## 📋 Email Template Features

### Prediction Report:
- ✅ Professional header with gradient
- ✅ Risk level box (color-coded)
- ✅ Confidence percentage
- ✅ Detailed recommendations
- ✅ Next steps guidance
- ✅ CTA button to portal
- ✅ Footer with timestamp

### Appointment Notification:
- ✅ Appointment details card
- ✅ Doctor information
- ✅ Date and time
- ✅ Location details
- ✅ Important notes
- ✅ Professional footer

## 🎨 Email Design

### Colors:
- High Risk: #ff006e (Pink/Red)
- Medium Risk: #ffbe0b (Orange)
- Low Risk: #00ff88 (Green)
- Primary: #00d9ff (Cyan)
- Background: #f5f5f5 (Light Gray)

### Layout:
- Responsive design
- Max-width: 600px
- Mobile-friendly
- Professional typography

## 📊 Statistics Tracking

View email statistics:

```python
from core.email_service import email_service

stats = email_service.get_statistics()
print(stats)
# {
#     'emails_sent': 10,
#     'emails_failed': 1,
#     'success_rate': 90.91
# }
```

## 🔐 Security Notes

1. **Never commit credentials** to version control
2. Use **App Passwords**, not regular passwords
3. Store credentials in `.env` file only
4. Add `.env` to `.gitignore`

## ✉️ Testing Without SMTP

If you don't have SMTP configured, emails will fail silently but the app continues to work. The service logs:
- ✅ Email sent successfully
- ❌ Email failed (with error message)

## 🚀 Integration Points

### In Prediction Service:
```python
from core.email_service import email_service

# After prediction
if patient.email:
    email_service.send_prediction_report(
        patient_email=patient.email,
        patient_name=patient.name,
        risk_level=result['risk_level'],
        confidence=result['confidence'],
        recommendations="..."
    )
```

### In Appointment Service:
```python
# After booking
if patient.email:
    email_service.send_appointment_notification(
        patient_email=patient.email,
        patient_name=patient.name,
        doctor_name=doctor.name,
        appointment_date=appointment.appointment_date
    )
```

## 📱 Next Steps

1. **Configure SMTP** in `.env`
2. **Add email input** to patient forms (updating now...)
3. **Test email sending**
4. **Monitor email statistics**

## ⚡ Features

- ✅ Async email sending (non-blocking)
- ✅ HTML + Plain text versions
- ✅ Professional templates
- ✅ Error handling
- ✅ Statistics tracking
- ✅ Queue management
- ✅ Threaded delivery

**Email system is ready to use!** Just add SMTP credentials to `.env` file.
