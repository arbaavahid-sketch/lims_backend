#!/usr/bin/env bash
# Server-side backup of the SENAITE data volume (senaite_data).
#
# Creates a timestamped tar.gz under <repo>/backups and keeps the last
# KEEP_DAYS copies (rotation). Intended to run daily from cron on the VPS.
#
# One-off run:
#   cd ~/lims_backend && ./scripts/backup.sh
#
# Daily at 02:00 via cron (crontab -e):
#   0 2 * * * cd ~/lims_backend && ./scripts/backup.sh >> backups/backup.log 2>&1
#
# IMPORTANT: copy backups OFF the server too (a backup on the same box does
# not survive losing the box). See docs/VPS_DEPLOY.md.
set -euo pipefail

KEEP_DAYS="${KEEP_DAYS:-14}"
VOLUME="${VOLUME:-senaite_data}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$ROOT/backups"
mkdir -p "$BACKUP_DIR"

STAMP="$(date +%Y%m%d-%H%M)"
NAME="senaite-data-${STAMP}.tar.gz"

echo "[backup] $(date '+%F %T') creating ${NAME} ..."
docker run --rm \
  -v "${VOLUME}:/data:ro" \
  -v "${BACKUP_DIR}:/backup" \
  alpine tar czf "/backup/${NAME}" -C /data .

SIZE="$(du -h "${BACKUP_DIR}/${NAME}" | cut -f1)"
echo "[backup] done: ${BACKUP_DIR}/${NAME} (${SIZE})"

# Rotation: delete backups older than KEEP_DAYS days.
find "${BACKUP_DIR}" -name 'senaite-data-*.tar.gz' -type f -mtime +"${KEEP_DAYS}" -delete
echo "[backup] rotated, kept last ${KEEP_DAYS} days"
