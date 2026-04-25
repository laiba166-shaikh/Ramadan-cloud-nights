# Container Security: Non-Root User Configuration

## What was changed

Both `backend/Dockerfile` and `frontend/Dockerfile` had the `useradd` command updated to explicitly set the login shell to `nologin`:

```dockerfile
# Before
useradd --uid 1001 --gid appgroup --no-create-home appuser

# After
useradd --uid 1001 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser
```

## Why `--shell /usr/sbin/nologin`

Without this flag, `useradd` assigns the default shell (`/bin/sh`). This means the account can be used for interactive sessions — for example via `docker exec ... su appuser`. Setting the shell to `nologin` blocks any interactive login attempt for this user.

## Why `useradd` over `adduser --system`

`adduser --system` achieves a similar result (it sets `nologin` implicitly), but it is a Debian/Ubuntu-only high-level wrapper. Using `useradd` with `--shell /usr/sbin/nologin` is:

- **Portable** — works on Alpine, Debian, RHEL, and any other Linux base image
- **Explicit** — the intent is visible in the flag itself, no knowledge of `adduser` Debian defaults required
- **Consistent** — `useradd` + `groupadd` is the standard low-level approach used across most container hardening guides

## `useradd --system` is not equivalent

`useradd` does have a `--system` flag, but it only selects a UID from the system range (< 1000) and disables password aging. It does **not** set the shell to `nologin`. It is not a substitute for `adduser --system`.

## Full non-root user pattern used

```dockerfile
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home --shell /usr/sbin/nologin appuser

WORKDIR /app
# ... COPY files ...
RUN chown -R appuser:appgroup /app

USER appuser
```

| Flag | Purpose |
|---|---|
| `--gid 1001` | Explicit group ID, avoids collision with host system groups |
| `--uid 1001` | Explicit user ID, avoids collision with host system users |
| `--no-create-home` | No home directory — unnecessary for a service account |
| `--shell /usr/sbin/nologin` | Blocks interactive login for this account |
| `chown -R` before `USER` | Must run as root before switching; non-root cannot chown |
| `USER appuser` | Ensures the container process (uvicorn) runs as non-root |
