# 🚀 Skyfly AI Voice Assistant — Business Lead Qualifier

An advanced AI-powered voice agent backend built for **Skyfly Technology**, using **FastAPI**, **SQLAlchemy**, and **Vapi**. This system automates client inquiries for Web Development, E-commerce solutions, and AI Voice Agent services.

---

## ✨ Features

- **Lead Capture** — Automatically collects customer name, interested service, and contact details via voice.
- **Service Specialization** — Trained to discuss Skyfly's core offerings:
    - Web Development (Custom SaaS & Branding)
    - E-commerce Solutions (Inventory & Performance Tracking)
    - AI Voice Agents & Software Development (New Service)
- **FastAPI Backend** — High-performance API that processes Vapi tool calls in real-time.
- **SQLite Database** — Securely stores lead information for follow-ups.

---

## 🏗️ Project Structure

```text
├── backend.py          # FastAPI server (Handles Vapi webhooks)
├── database.py         # SQLAlchemy models (Lead storage logic)
├── pyproject.toml      # Project dependencies (FastAPI, SQLAlchemy, etc.)
└── skyfly_leads.db     # Local SQLite database (Auto-generated)