---
name: typographic-hierarchy
description: "Format documentation, READMEs, and structured text using header hierarchy where each level stands alone. Use when creating docs, research notes, summaries, or when user requests 'scannable,' 'well-structured,' 'skimmable,' or 'readable at multiple depths' output. Applies to markdown, technical specs, and any hierarchical text formatting."
---

# Typographic Hierarchy

*Typographic hierarchy means glancers get the concept, skimmers get the cliff notes, and readers get the details. Nail this, and your design can finally match your ambition.*

# Definition

Typographic hierarchy is the strategic organization of text elements to guide a reader’s eye, establishing a clear order of importance (headline, subhead, body) to make content navigable and engaging. It uses contrast in size, weight, color, and spacing to prioritize information, turning dense text into structured, accessible information. 

## Why Hierarchy Matters

Structure information so users can:
* Quickly understand the big picture (glance at largest elements)
* Get the overall purpose and key points (skim medium-sized elements)
* Rapidly dial into specific details they need (read full content)

This creates efficient cognitive navigation where people stop at exactly the depth of detail they need without reading everything.

## Core Principle

**Headers should tell the complete story on their own.** Someone scanning headers should walk away with the essential message without reading body text.

**Avoid long lists of equally-weighted items.** If you have many points at the same visual level, group them under fewer, broader categories so readers can grasp the structure at a glance. Books use parts to organize chapters - be creative with your medium's conventions.

**For longer material with many sections and sub sections, consider listing the top level sections as a table of contents or whatever is similar if it fits in the medium**

Information is structured for three reading depths:
- **Glancers** (Largest text/graphics/headers only): Understand the concept and subject matter
- **Skimmers** (Medium and larger text/graphics/headers tell the brief story): Get the full story and key takeaways  
- **Readers** (Full content): Access supporting details and nuance

**Apply the principle, don't worship it.** What "meaningful" looks like depends entirely on your medium. Technical docs, marketing copy, academic papers, slides—they all have different conventions. Work WITH those conventions to make headers clearer, not AGAINST them to force some ideal. If it feels forced or unnatural, you've missed the point.

## Here's Typical Typographic Hierarchy in Practice

*Note: The specific formatting (===, ---, ###, or bold/size) is just one implementation. Use whatever visual hierarchy makes sense for your medium - the principle is that larger/bolder text carries higher-level meaning.*

```
YARD MAINTENANCE
================

Neglected leaves kill turf and harbor pests
--------------------------------------------

Thick leaf layers block sunlight and cause rot within weeks
- Wet leaves trap moisture against grass, creating fungal growth
- Decomposing layers harbor ticks, mold, and disease vectors
  - Lyme disease risk increases in yards with persistent leaf litter (CDC)

Match tool to yard size, not price tag
- Under 1/4 acre — a 30" fan rake is all you need
- Over 1/4 acre — leaf blower saves hours; corded is fine near outlets
- Tarps beat bags every time for hauling to the curb

Mow height matters more than mower quality
-------------------------------------------

Cool-season grass needs 3-4 inches, never cut more than 1/3 of blade
- Taller grass shades roots, retains moisture, crowds out weeds
- Cutting too short stresses the plant and invites disease

Dull blades tear grass and create entry points for infection
- Sharpen every 20-25 hours of use
- Torn tips turn brown within days and become fungal infection sites
```

**What a glancer gets**: Yard maintenance covers leaves and mowing

**What a skimmer gets**: Neglected leaves damage lawns and attract pests; tool choice depends on yard size. Mow height beats equipment quality; dull blades cause disease.

**What a reader gets**: All the supporting facts, measurements, and techniques

## Here's an Excerpt from a Tech Manual

It's still a tech manual, but influenced by typographic hierarchy its flow is improved while remaining professional:

```
**SYSTEM INSTALLATION**

**1. Prerequisites**

1.1 Server requirements
    • Ubuntu 22.04 LTS or later
    • 16GB RAM minimum (32GB recommended)
    • 100GB available disk space

1.2 Network configuration
    • Static IP address assigned
    • Ports 443, 8080, 5432 accessible
    • DNS records configured for domain

**2. Installation**

Step 1 — Install dependencies
    Run: sudo apt update
    Install PostgreSQL 15 and Node.js 20 LTS

Step 2 — Configure database
    Create application database and user
    Apply schema migrations from /migrations directory

Step 3 — Deploy application
    Clone repository to /opt/application
    Run: npm ci --production
    Run: systemctl start app.service
```

**What a glancer gets**: Installation has prerequisites and installation steps

**What a skimmer gets**: Need Ubuntu with specific resources, install dependencies, configure database, deploy

**What a reader gets**: Exact commands and configuration details
