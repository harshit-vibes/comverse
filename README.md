# Comverse

Commerce + Converse — WhatsApp & Instagram commerce platform built for Bharat.

## Overview

Comverse enables Indian SMBs (starting with catalog-based food businesses) to reduce platform dependency on Zomato/Swiggy by offering conversational commerce at 10% commission (vs 25-35% on aggregators), while solving payment collection and delivery.

**Founder:** Amit Chavan (amit.chavan90@gmail.com)

## Core Value Propositions

1. **Storefront on WhatsApp & Instagram** — no new app needed
2. **10% commission** vs 25-35% on aggregators
3. **Payment integration** — Razorpay UPI with T+1 settlements
4. **Last-mile delivery** — Shiprocket Quick, Shadowfax, Borzo
5. **Customer data ownership** — know who orders, preferences, frequency
6. **Hinglish AI agent** — handles full customer ordering journey
7. **Discovery tools** — QR codes, CTWA campaigns, Google My Business

## Target Market

- **Vertical:** Catalog-based food SMBs (cake shops, cafes, thali restaurants)
- **Phase 1:** Pune & suburbs
- **Phase 2:** Mumbai & Ahmedabad
- **ICP:** 50+ daily orders, 30-500 SKUs, currently on Zomato/Swiggy

## Architecture

No frontend — WhatsApp IS the interface.

| Component | Technology |
|-----------|-----------|
| Messaging | WhatsApp Cloud API (direct, no BSP) |
| AI Agent | Lyzr Agent Studio (Claude Sonnet 4.5) |
| Middleware | AWS Lambda |
| Database | Supabase (shared) |
| Catalog Sync | PetPooja → Comverse DB → Meta Commerce Catalog |
| Payments | Razorpay Route (Linked Accounts) |
| Delivery | Shiprocket Quick / Shadowfax / Borzo |
| Discovery | Google My Business API |

## Current Status

**Stage:** Idea → MVP

**Next step:** Founder sharing synthetic conversation samples (input/output JSON) to design and build the Lyzr agents that power the WhatsApp ordering flow.

## Timeline

| Phase | Period | Target |
|-------|--------|--------|
| Build & Launch | Month 1 | 5-7 pilot merchants |
| Scale | Month 2 | 10-13 paying merchants |
| Prove | Month 3 | 20-25 merchants, path to $10K MRR |
| Scale to 100 | Months 4-6 | 100 merchants, Mumbai + Ahmedabad |
