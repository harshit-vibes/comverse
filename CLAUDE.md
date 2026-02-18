# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is Comverse

Commerce + Converse — WhatsApp & Instagram conversational commerce platform for Indian SMBs (catalog-based food businesses: cake shops, cafes, thali restaurants). Enables ordering via WhatsApp at 10% commission vs 25-35% on Zomato/Swiggy.

**Founder:** Amit Chavan (amit.chavan90@gmail.com)

## Message Flow Architecture

```
Customer (WhatsApp)
        │  sends message
        ▼
WhatsApp Cloud API  ──── webhook ──────►  Comverse Middleware Service
                                                    │
                                                    │  calls
                                                    ▼
                                            Lyzr Agent API
                                         (Claude Sonnet 4.5)
                                                    │
                                                    │  returns response
                                                    ▼
WhatsApp Cloud API  ◄──── reply ────────  Comverse Middleware Service
        │
        │  delivers
        ▼
Customer (WhatsApp)
```

Our service sits **downstream** of the WhatsApp Business API and **upstream** of Lyzr. It is the orchestration/integration layer.

## Tech Stack

| Layer | Technology | Hosting |
|-------|-----------|---------|
| Messaging channel | WhatsApp Cloud API (direct, no BSP) | Meta |
| AI Agent | Lyzr Agent Studio (Claude Sonnet 4.5) | Lyzr Platform |
| Middleware service | AWS Lambda (webhook handler + Lyzr caller) | AWS |
| Database | Supabase Postgres | Supabase (shared project: `mmgybsiqjdpsjypaahee`) |
| Merchant frontend | Next.js + shadcn/ui + Tailwind | Vercel |
| Catalog sync | PetPooja → Comverse DB → Meta Commerce Catalog | — |
| Payments | Razorpay Route (Linked Accounts, UPI, T+1) | Razorpay |
| Delivery | Shiprocket Quick / Shadowfax / Borzo | — |

**No app for customers** — WhatsApp IS the customer interface.

## Shared Infrastructure (lyzr-agentpreneur monorepo)

All projects in `lyzr-agentpreneur/` share a single Supabase project. See `../SETUP.md` for credentials and conventions. Comverse tables use a `cv_` prefix or a `comverse` schema to isolate from other projects.

## Frontend (Merchant Dashboard)

Located at `frontend/` — Next.js App Router, shadcn/ui, Tailwind, Zustand for state, Supabase Auth (SSR). Deployed to Vercel.

```bash
cd frontend
npm install
npm run dev        # dev server
npm run build      # production build
npm run lint       # ESLint
```

## Middleware Service (Webhook Handler)

Located at `service/` (to be scaffolded). AWS Lambda function that:
1. Receives WhatsApp webhook POST events
2. Verifies the webhook signature
3. Extracts message content and sender info
4. Calls Lyzr Agent API with conversation context
5. Sends Lyzr's response back via WhatsApp API

```bash
cd service
npm install
npm run dev        # local dev (e.g. via serverless-offline or plain node)
npm run deploy     # deploy to AWS Lambda
```

## Supabase

```bash
# Run from repo root or frontend/
npx supabase migration new <name>   # create migration
npx supabase db push                # push migrations
npx supabase functions deploy       # deploy edge functions
```

## Key Domain Concepts

- **Merchant**: Indian SMB owner onboarded on Comverse
- **Customer**: End-user ordering via WhatsApp
- **Catalog**: Product list synced from PetPooja to Meta Commerce Manager
- **Conversation session**: A WhatsApp thread mapped to an active Lyzr agent session
- **AI agent language**: Hinglish (Hindi + English mix), handles full ordering journey

## Phase 1 Scope (MVP)

- WhatsApp webhook → Lyzr agent inference → reply
- Catalog display via WhatsApp Product Messages
- Razorpay payment link generation in-chat
- Order record in Supabase
- Basic merchant dashboard (order list, status)
