# Internal Ownership And Runtime Independence

This project is the Tandis Laboratory internal SENAITE LIMS build.

## What Is Ours

- The deployment repository: `arbaavahid-sketch/lims_backend`
- The SENAITE core fork used by this deployment:
  `arbaavahid-sketch/senaite.core`, branch `persian`
- Persian translations, RTL stylesheet, and Tandis-specific branding
- The local application image: `tandis/lims:latest`
- The local base image tag: `lims/senaite-base:2.x`

## What It Is Based On

The application remains a derivative work of SENAITE / SENAITE.CORE, which is
licensed under GPL-2.0. Keep the upstream license and attribution files intact.

## Runtime Independence

The Dockerfile uses the internal base image tag:

```dockerfile
FROM lims/senaite-base:2.x
```

This means normal rebuilds use the local/internal base tag instead of pulling
directly from `senaite/senaite:2.x`.

To refresh the internal base intentionally, pull or build the desired upstream
base, inspect it, then retag it:

```bash
docker tag senaite/senaite:2.x lims/senaite-base:2.x
docker tag senaite/senaite:2.x lims/senaite-base:2.x-YYYYMMDD
```

To rebuild the customized internal image:

```bash
docker compose build
docker compose up -d
```

To keep an offline backup of the runnable image:

```bash
docker save tandis/lims:latest -o backups/tandis-lims.tar
docker save lims/senaite-base:2.x -o backups/lims-senaite-base-2.x.tar
```

Restore later with:

```bash
docker load -i backups/lims-senaite-base-2.x.tar
docker load -i backups/lims-senaite-fa.tar
```

