# icloudpd iCloud Photo Backup

**Type:** skill | **Version:** 1.0.0 | **OS:** linux, macos, windows

Download and sync iCloud Photos to local storage using the icloudpd CLI. Covers install, auth, sync modes, and Docker usage.

## Tags
icloud, photos, backup, sync, cli, icloudpd, macos

## Overview
Reference skill for icloudpd v1.32.2, an open-source Python CLI that downloads and syncs iCloud Photos to local storage. Covers three sync modes (copy, sync, move), key flags, authentication including 2FA and headless/NAS setups, multi-platform install options, and common recipes. Includes gotchas such as the 400 error on first run and ADP incompatibility.

## Try These Prompts
- Download all my iCloud photos to ~/icloud-photos
- Set up icloudpd to sync iCloud photos every hour
- How do I use icloudpd in Docker on a NAS?
- I want to move photos off iCloud and keep only the last 30 days there

## Use Cases
- Backing up iCloud Photos to local or NAS storage
- Continuous sync with watch mode for home servers
- Moving photos off iCloud to reclaim storage
- Headless/automated photo archiving in Docker

## Additional Requirements
Install via pip, npx, Docker, Snap, or binary. Not compatible with Apple Advanced Data Protection (ADP) — must be disabled. Stores auth tokens in ~/.pyicloud by default.

---
*Part of the [EnhanceClaude](https://enhanceclaude.com) AI tools collection.*
