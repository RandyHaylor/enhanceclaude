---
name: icloudpd-icloud-photo-backup
description: icloudpd CLI for downloading/syncing iCloud Photos. Use when user asks about icloudpd, iCloud photo backup, or syncing iCloud photos locally.
---

# icloudpd — iCloud Photos Downloader

CLI tool to download/sync iCloud Photos to local storage. v1.32.2. Open source, Python-based.

- GitHub: https://github.com/icloud-photos-downloader/icloud_photos_downloader
- Docs: https://icloud-photos-downloader.github.io/icloud_photos_downloader/
- Reference: https://icloud-photos-downloader.github.io/icloud_photos_downloader/reference.html

## Install

- **pip:** `pip install icloudpd` (Windows: add `--user`)
- **Docker:** `docker run -it --rm icloudpd/icloudpd:latest icloudpd --help`
- **npm:** `npx --yes icloudpd`
- **Arch:** `yay -S icloudpd-bin`
- **Snap:** `sudo snap install icloudpd`
- **Binary:** download from [GitHub Releases](https://github.com/icloud-photos-downloader/icloud_photos_downloader/releases/tag/v1.32.2)

## Modes

- **Copy** (default) — download only, iCloud untouched
- **Sync** — download + delete local files removed from iCloud (`--auto-delete`)
- **Move** — download + delete from iCloud (`--keep-icloud-recent-days N`)

Docs: https://icloud-photos-downloader.github.io/icloud_photos_downloader/mode.html

## Key Flags

| Flag | Purpose |
|---|---|
| `--username X` | Apple ID email; repeatable for multi-account |
| `--directory X` | Local download root |
| `--watch-with-interval X` | Continuous sync, interval in seconds |
| `--keep-icloud-recent-days X` | Move mode; delete from iCloud except last X days |
| `--auto-delete` | Sync mode; mirror iCloud deletions locally |
| `--recent X` | Process only X most recent assets |
| `--until-found X` | Stop after X consecutive already-downloaded assets |
| `--album X` | Specific album(s); repeatable |
| `--list-albums` | List available albums |
| `--library X` | Choose library (default: Personal Library) |
| `--skip-videos` | Skip video assets |
| `--skip-photos` | Skip photo assets |
| `--skip-live-photos` | Skip live photo assets |
| `--set-exif-datetime` | Write EXIF date if missing |
| `--folder-structure X` | Subfolder naming scheme |
| `--dry-run` | Preview changes, no downloads |
| `--auth-only` | Authenticate and exit |
| `--size X` | Asset size to download |
| `--domain cn` | Use `.cn` domain (mainland China) |
| `--password-provider X` | Password source: `parameter`, `keyring`, `console` |
| `--mfa-provider X` | MFA code source |
| `--cookie-directory X` | Custom auth token folder (default: `~/.pyicloud`) |

Full list: `icloudpd --help`

## Auth

- Supports 2FA via console prompt or web UI
- Store password in system keyring: `icloud --username X`
- Web UI for headless/NAS: https://icloud-photos-downloader.github.io/icloud_photos_downloader/webui.html
- **Not compatible with** Advanced Data Protection (ADP) — must disable ADP
- Hardware keys (FIDO) not supported
- Clear `~/.pyicloud` to reset auth state
- Docs: https://icloud-photos-downloader.github.io/icloud_photos_downloader/authentication.html

## Common Recipes

```bash
# One-time download of everything
icloudpd --directory ~/icloud-photos --username user@example.com

# Continuous sync every hour
icloudpd --directory ~/icloud-photos --username user@example.com --watch-with-interval 3600

# Move mode: download all, keep only last 30 days in iCloud
icloudpd --directory ~/icloud-photos --username user@example.com --keep-icloud-recent-days 30

# Download specific album
icloudpd --directory ~/icloud-photos --username user@example.com --album "Vacation 2024"

# Docker with timezone
docker run -it --rm -v $(pwd)/Photos:/data -e TZ=America/New_York \
  icloudpd/icloudpd:latest icloudpd --directory /data --username user@example.com --watch-with-interval 3600

# Dry run to preview
icloudpd --directory ~/icloud-photos --username user@example.com --dry-run

# Auth-only (pre-authenticate, useful for automation)
icloudpd --username user@example.com --auth-only
```

## Gotchas

- First run may fail with `Bad Request (400)` — Apple needs 5–10 min to prepare; retry
- `--keep-icloud-recent-days` uses photo *creation* date, not upload date
- Assets excluded by filters (e.g. `--skip-videos`) are never deleted from iCloud
- Too-short `--watch-with-interval` may trigger Apple throttling
- Windows Docker: use `%cd%` or full path instead of `$(pwd)`; Linux containers only
