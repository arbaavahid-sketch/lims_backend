# SENAITE Local Runbook

This runbook records the routine commands for the internal SENAITE LIMS
deployment in `D:\Git\lims_backend`.

## Start And Stop

Start or resume the local system:

```powershell
cd D:\Git\lims_backend
docker compose up -d
```

Check container status:

```powershell
docker compose ps
```

Stop the local system without deleting data:

```powershell
docker compose stop
```

Restart after configuration or template changes:

```powershell
docker compose restart senaite
```

Rebuild the customized image:

```powershell
docker compose build
docker compose up -d
```

## Local URLs

- Application: `http://localhost:8080/senaite`
- Login redirect smoke check: `http://localhost:8080/senaite/login`

Use a normal GET request for smoke checks. Avoid treating `HEAD /senaite` as the
main health check because the current Waitress/Zope stack can log a
hop-by-hop-header assertion for HEAD requests even when browser GET access is
working.

## Smoke Checks

Run these after startup:

```powershell
docker compose ps
curl.exe -L -s -o NUL -w "%{http_code} %{url_effective}" http://localhost:8080/senaite
docker compose logs --tail=180 senaite
```

Expected baseline:

- `docker compose ps` shows service `senaite` running.
- The curl command returns `200 http://localhost:8080/senaite/login`.
- Logs show `Ready to handle requests`.
- No new startup traceback appears after the latest GET smoke check.

## Logs

Show recent logs:

```powershell
docker compose logs --tail=180 senaite
```

Follow logs while testing:

```powershell
docker compose logs -f senaite
```

Known log notes from the Phase 0 baseline:

- `HEAD /senaite` can trigger a Waitress assertion about a `Connection`
  hop-by-hop header. Use GET-based checks for normal health validation.
- A report render request for missing UID `9c445f328b3748ec834046d099eed50f`
  previously returned 500. Treat this as a report/sample-data follow-up unless
  it recurs with valid samples.

## Data Volume

The SENAITE data volume is external and named `senaite_data`.

Confirm the configured volume:

```powershell
docker compose config --volumes
```

Expected output:

```text
senaite_data
```

## Backup

Create a dated backup of the persistent volume before imports, schema changes,
or large configuration updates:

```powershell
cd D:\Git\lims_backend
docker run --rm -v senaite_data:/data -v ${PWD}\backups:/backup alpine `
  tar czf /backup/senaite-data-YYYYMMDD-HHMM.tar.gz -C /data .
```

Replace `YYYYMMDD-HHMM` with the actual date and time, for example
`20260706-0645`.

Also consider saving the runnable images before production changes:

```powershell
docker save lims/senaite-fa:latest -o backups/lims-senaite-fa-YYYYMMDD.tar
docker save lims/senaite-base:2.x -o backups/lims-senaite-base-2.x-YYYYMMDD.tar
```

## Restore Drill

Restore into a non-production test volume first whenever possible:

```powershell
docker volume create senaite_data_restore_test
docker run --rm -v senaite_data_restore_test:/data -v ${PWD}\backups:/backup alpine `
  tar xzf /backup/senaite-data-YYYYMMDD-HHMM.tar.gz -C /data
```

To restore the real `senaite_data` volume, stop the app first and make sure the
backup file is the intended one:

```powershell
docker compose stop
docker run --rm -v senaite_data:/data -v ${PWD}\backups:/backup alpine `
  tar xzf /backup/senaite-data-YYYYMMDD-HHMM.tar.gz -C /data
docker compose up -d
```

Then rerun the smoke checks.

## Before Each Roadmap Item

1. Run the smoke checks.
2. Check whether the work touches persistent data.
3. If it touches data, create a volume backup first.
4. Make the smallest change needed.
5. Verify through code and, where relevant, the running SENAITE instance.
6. Update the roadmap or a task note with what changed and what remains open.
