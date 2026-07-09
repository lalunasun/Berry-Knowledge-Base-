## 🌸 Overview
This project is an AI-assisted email memory and draft generation workflow designed to turn historical mailbox data into reusable contact knowledge.
The system extracts structured email records from Microsoft Graph, groups messages by external participant, builds AI-generated contact profiles from historical conversations, and uses those profiles to support context-aware draft replies inside an automation workflow.
The goal is not full auto-send, but faster, more consistent, and better-informed draft generation with human review in the loop.

## Design principle
Local pipeline = source of truth
SharePoint = published runtime knowledge base
Power Automate = live draft generation layer

## Core workflow 
- Mailbox backup layer
Keep a full mailbox backup as the raw archive and recovery source.

- Graph API extraction layer
Export structured email data from Microsoft Graph, mainly from:
Inbox
Sent Items

- Raw email normalization
Convert exported messages into a consistent raw email index with fields such as sender, recipients, subject, body, timestamps, direction, and message IDs.

- Grouping layer
Group emails by external participant email, so that each contact has a conversation bundle.

- AI profile generation layer
Use historical emails from each group to generate a structured ai_profile.json.

- Published knowledge layer
Push selected profiles to SharePoint for workflow usage.

- Draft generation layer
When a new email arrives, the workflow checks whether the sender already exists, loads the corresponding profile, and generates a context-aware draft reply.

---
```mermaid
flowchart TD
    A["Mailbox Backup Layer<br/>PST backup / recovery source"] --> B["Graph API Extraction"]
    B --> B1["Inbox"]
    B --> B2["Sent Items"]

    B1 --> C["Raw Email Normalization"]
    B2 --> C

    C --> C1["raw email index"]
    C --> C2["message IDs / sender / recipient / timestamps / direction / attachment flags"]

    C --> D["Grouping Layer"]
    D --> D1["group by external participant email"]
    D --> D2["conversation bundles"]

    D --> E["AI Profile Generation"]
    E --> E1["ai_input.json"]
    E --> E2["ai_input_masked.json"]
    E --> E3["ai_profile.json"]

    E --> F["Contact Master Index"]
    F --> F1["contact_email"]
    F --> F2["group_id"]
    F --> F3["contact type"]
    F --> F4["workflow route"]

    E --> G["Published Knowledge Layer"]
    F --> G
    G --> G1["SharePoint knowledge base"]

    G1 --> H["Power Automate Workflow"]
    H --> H1["identify sender"]
    H --> H2["load matching profile"]


    H --> H3["generate context-aware draft"]

    H3 --> I["Human Review before send"]
```
