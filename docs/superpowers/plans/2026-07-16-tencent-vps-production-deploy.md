# Tencent VPS Production Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy the current NoiseFilter Flask blog and its live local archive to the existing Tencent Cloud Ubuntu server, then serve it from `https://yishucc.top` without disturbing unrelated server files.

**Architecture:** Run the Flask application with Gunicorn bound only to `127.0.0.1:5055`, managed by systemd. Put Nginx in front for the public 80/443 endpoints, TLS termination, static assets, forwarded headers, and `/admin/login` rate limiting. Keep ignored runtime data in `/srv/noisefilter/archive` and `/srv/noisefilter/blog/data`; code synchronization must exclude both directories so future deploys preserve published issues and caches.

**Tech Stack:** Ubuntu 24.04, Python 3.12, Flask, Gunicorn, systemd, Nginx, Certbot/Let's Encrypt, rsync, Tencent Cloud DNSPod.

## Global Constraints

- Preserve `/home/ubuntu/code` and every unrelated server path.
- Use `/srv/noisefilter` as the only application root.
- Keep Gunicorn private on `127.0.0.1:5055`; expose only Nginx ports 80 and 443.
- Use live data from `/Users/yishu/YiShu Claude/content-curation/archive` and `/Users/yishu/YiShu Claude/content-curation/blog/data`.
- Never commit or print `SECRET_KEY`, `BLOG_ADMIN_PASSWORD`, or API credentials.
- Set `PUBLIC_BASE_URL=https://yishucc.top`, `BLOG_TIMEZONE=America/Los_Angeles`, and `SESSION_COOKIE_SECURE=true` in production.
- Preserve the old EdgeOne DNS target until the new server passes direct-IP and Host-header acceptance checks.
- Before claiming completion, verify systemd, Nginx, HTTP, HTTPS, homepage, dated issue, article, cover, static assets, and anonymous/admin visibility.

---

### Task 1: Add repeatable production service definitions

**Files:**
- Modify: `blog/requirements.txt`
- Create: `deploy/noisefilter.service`
- Create: `deploy/noisefilter.nginx.conf`
- Create: `deploy/README.md`

**Interfaces:**
- Consumes: Flask WSGI object `blog/app.py:app`, local listener port `5055`.
- Produces: `noisefilter.service` and an Nginx virtual host for `yishucc.top`.

- [ ] **Step 1: Add the production WSGI dependency**

Append the exact dependency to `blog/requirements.txt`:

```text
gunicorn>=22.0,<24.0
```

- [ ] **Step 2: Create the systemd unit**

Create `deploy/noisefilter.service`:

```ini
[Unit]
Description=NoiseFilter Flask blog
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
Group=ubuntu
WorkingDirectory=/srv/noisefilter/blog
EnvironmentFile=/etc/noisefilter.env
Environment=PYTHONUNBUFFERED=1
ExecStart=/srv/noisefilter/blog/.venv/bin/gunicorn --workers 2 --threads 2 --bind 127.0.0.1:5055 --timeout 120 --access-logfile - --error-logfile - app:app
Restart=on-failure
RestartSec=5
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

- [ ] **Step 3: Create the HTTP reverse proxy**

Create `deploy/noisefilter.nginx.conf`:

```nginx
limit_req_zone $binary_remote_addr zone=noisefilter_admin_login:10m rate=5r/m;
proxy_headers_hash_max_size 1024;
proxy_headers_hash_bucket_size 128;

server {
    listen 80;
    listen [::]:80;
    server_name yishucc.top www.yishucc.top;

    client_max_body_size 10m;

    location /static/ {
        alias /srv/noisefilter/blog/static/;
        expires 1h;
        add_header Cache-Control "public, max-age=3600";
    }

    location = /admin/login {
        limit_req zone=noisefilter_admin_login burst=5 nodelay;
        proxy_pass http://127.0.0.1:5055;
        include proxy_params;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:5055;
        include proxy_params;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 180s;
    }
}
```

- [ ] **Step 4: Document deployment and rollback commands**

Create `deploy/README.md` with exact install, sync, validation, DNS, Certbot, log, restart, and rollback commands. It must state that `archive/`, `blog/data/`, and `/etc/noisefilter.env` are not deleted by code sync.

- [ ] **Step 5: Validate repository deployment assets**

Run:

```bash
for test_file in blog/test_*.py; do blog/.venv/bin/python "$test_file"; done
node --test blog/test_admin_daily_state.mjs
rg -n 'gunicorn|127\.0\.0\.1:5055|limit_req|SESSION_COOKIE_SECURE' blog/requirements.txt deploy README.md
```

Expected: Python tests pass; all production controls are present.

### Task 2: Stage the exact production payload locally

**Files:**
- Read: repository files tracked at Git commit `0620957ac99c21d61d4d675ab823d49a33f1227b`
- Read: `/Users/yishu/YiShu Claude/content-curation/archive`
- Read: `/Users/yishu/YiShu Claude/content-curation/blog/data`
- Create temporarily: `/tmp/noisefilter-staging`

**Interfaces:**
- Consumes: current Git code plus the running local site's ignored data.
- Produces: a staging tree that renders the same published issue with the new code.

- [ ] **Step 1: Copy code without ignored runtime data**

Run:

```bash
rsync -a --delete --exclude '.git' --exclude '.venv/' --exclude 'blog/.venv/' --exclude 'archive/' --exclude 'blog/data/' --exclude 'config/.env' ./ /tmp/noisefilter-staging/
```

- [ ] **Step 2: Link the live data into staging**

Run:

```bash
ln -s '/Users/yishu/YiShu Claude/content-curation/archive' /tmp/noisefilter-staging/archive
ln -s '/Users/yishu/YiShu Claude/content-curation/blog/data' /tmp/noisefilter-staging/blog/data
```

- [ ] **Step 3: Start Gunicorn on a test-only port**

Run with generated temporary secrets and port `15055`:

```bash
cd /tmp/noisefilter-staging/blog
PUBLIC_BASE_URL=http://127.0.0.1:15055 BLOG_ADMIN_PASSWORD=staging-only SECRET_KEY=staging-only-secret '/Users/yishu/Documents/AI产品/降噪/content-curation-git-work/blog/.venv/bin/gunicorn' --workers 1 --bind 127.0.0.1:15055 app:app
```

- [ ] **Step 4: Verify the payload**

Run:

```bash
curl -fsS http://127.0.0.1:15055/ -o /tmp/noisefilter-home.html
curl -fsS http://127.0.0.1:15055/daily/2026-07-13 -o /tmp/noisefilter-daily.html
rg -n '2026-07-13|降噪|管理员' /tmp/noisefilter-home.html /tmp/noisefilter-daily.html
```

Expected: both requests return 200 and the published issue renders.

### Task 3: Provision the Tencent server and upload data

**Files:**
- Create remotely: `/srv/noisefilter`
- Create remotely: `/etc/noisefilter.env` with mode `600`
- Preserve remotely: `/home/ubuntu/code`

**Interfaces:**
- Consumes: SSH host `ubuntu@81.70.235.230` and local staging payload.
- Produces: installed Python environment and migrated live content.

- [ ] **Step 1: Install OS packages**

Run remotely:

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-venv python3-pip rsync certbot python3-certbot-nginx
```

- [ ] **Step 2: Create the application root**

Run remotely:

```bash
sudo install -d -o ubuntu -g ubuntu -m 0755 /srv/noisefilter
install -d -m 0755 /srv/noisefilter/archive /srv/noisefilter/blog/data
```

- [ ] **Step 3: Upload code while preserving runtime data**

Run locally:

```bash
rsync -az --delete --exclude '.git' --exclude '.venv/' --exclude 'blog/.venv/' --exclude 'archive/' --exclude 'blog/data/' --exclude 'config/.env' -e 'ssh -i ~/.ssh/codex_yishucc_ed25519 -o IdentitiesOnly=yes' ./ ubuntu@81.70.235.230:/srv/noisefilter/
```

- [ ] **Step 4: Upload the current live archive and blog state**

Run locally:

```bash
rsync -az -e 'ssh -i ~/.ssh/codex_yishucc_ed25519 -o IdentitiesOnly=yes' '/Users/yishu/YiShu Claude/content-curation/archive/' ubuntu@81.70.235.230:/srv/noisefilter/archive/
rsync -az -e 'ssh -i ~/.ssh/codex_yishucc_ed25519 -o IdentitiesOnly=yes' '/Users/yishu/YiShu Claude/content-curation/blog/data/' ubuntu@81.70.235.230:/srv/noisefilter/blog/data/
```

- [ ] **Step 5: Create the Python environment**

Run remotely:

```bash
python3 -m venv /srv/noisefilter/blog/.venv
/srv/noisefilter/blog/.venv/bin/python -m pip install --upgrade pip
/srv/noisefilter/blog/.venv/bin/pip install -r /srv/noisefilter/blog/requirements.txt
```

- [ ] **Step 6: Create production secrets without printing them**

Generate `SECRET_KEY` and `BLOG_ADMIN_PASSWORD` locally with `python3 -c 'import secrets; ...'`, transfer the environment file over SSH standard input, set owner `root:root` and mode `600`, and record the admin password for the final private handoff. The file must contain:

```dotenv
SECRET_KEY=<generated 64-hex value>
BLOG_ADMIN_PASSWORD=<generated URL-safe value>
BLOG_TIMEZONE=America/Los_Angeles
PUBLIC_BASE_URL=https://yishucc.top
DAILY_ISSUES_DIR=/srv/noisefilter/blog/data/daily_issues
SIGNAL_CACHE_PATH=/srv/noisefilter/blog/data/today_signal.json
DAILY_EDITOR_LOG=/srv/noisefilter/blog/data/daily_editor_events.jsonl
SESSION_COOKIE_SECURE=true
```

Expected: secrets never appear in command output or Git.

### Task 4: Start Gunicorn and Nginx before changing DNS

**Files:**
- Install remotely: `/etc/systemd/system/noisefilter.service`
- Install remotely: `/etc/nginx/sites-available/noisefilter`
- Link remotely: `/etc/nginx/sites-enabled/noisefilter`

**Interfaces:**
- Consumes: Task 1 service definitions and Task 3 payload.
- Produces: a working server reachable by direct IP before the EdgeOne domain binding is removed.

- [ ] **Step 1: Install and start the systemd unit**

Run remotely:

```bash
sudo install -m 0644 /srv/noisefilter/deploy/noisefilter.service /etc/systemd/system/noisefilter.service
sudo systemctl daemon-reload
sudo systemctl enable --now noisefilter
sudo systemctl is-active noisefilter
curl -fsS http://127.0.0.1:5055/ -o /tmp/noisefilter-app.html
```

Expected: `active`, and local Flask request succeeds.

- [ ] **Step 2: Install and validate the Nginx site**

Run remotely:

```bash
sudo install -m 0644 /srv/noisefilter/deploy/noisefilter.nginx.conf /etc/nginx/sites-available/noisefilter
sudo ln -sfn /etc/nginx/sites-available/noisefilter /etc/nginx/sites-enabled/noisefilter
if [ -L /etc/nginx/sites-enabled/default ]; then sudo unlink /etc/nginx/sites-enabled/default; fi
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
```

Expected: `nginx -t` reports syntax success.

- [ ] **Step 3: Validate through Nginx without DNS change**

Run locally:

```bash
curl --noproxy '*' --max-time 45 -fsS http://81.70.235.230/ -o /tmp/noisefilter-vps-home.html
rg -q '<title>降噪' /tmp/noisefilter-vps-home.html
curl --noproxy '*' --max-time 45 -fsS http://81.70.235.230/daily/2026-07-13 -o /tmp/noisefilter-vps-daily.html
curl --noproxy '*' --max-time 45 -fsSI http://81.70.235.230/static/css/style.css
```

Expected: HTML and static asset checks return 200 while public DNS still serves the previous site. Do not use `Host: yishucc.top` for this stage because the existing EdgeOne binding can intercept that host before DNS changes.

### Task 5: Point the domain to Tencent and enable HTTPS

**Files:**
- External state: DNSPod records for `yishucc.top` and `www.yishucc.top`
- Modify remotely through Certbot: `/etc/nginx/sites-available/noisefilter`

**Interfaces:**
- Consumes: verified direct-IP site.
- Produces: public `https://yishucc.top` with managed TLS.

- [ ] **Step 1: Change DNS only after user confirms the DNS action**

Set the apex `@` A record to `81.70.235.230`. Set `www` as a CNAME to `yishucc.top` or an A record to the same IP. Remove the previous EdgeOne target only from these two hostnames.

- [ ] **Step 2: Verify public resolution**

Run:

```bash
dig +short yishucc.top A
dig +short www.yishucc.top A
```

Expected: both names resolve to `81.70.235.230` from public resolvers.

- [ ] **Step 3: Issue and install TLS certificates**

Run remotely:

```bash
sudo certbot --nginx -d yishucc.top -d www.yishucc.top --redirect --agree-tos --register-unsafely-without-email --non-interactive
sudo certbot renew --dry-run
```

Expected: certificates are installed, HTTP redirects to HTTPS, renewal dry-run succeeds.

### Task 6: Production acceptance, rollback proof, and Git handoff

**Files:**
- Modify: `README.md`
- Commit: deployment assets and documentation only

**Interfaces:**
- Consumes: public HTTPS deployment.
- Produces: evidence-backed completion and repeatable operations.

- [ ] **Step 1: Run server health checks**

Run remotely:

```bash
sudo systemctl is-active noisefilter nginx
sudo systemctl is-enabled noisefilter nginx
sudo journalctl -u noisefilter --since '10 minutes ago' --no-pager
sudo nginx -t
```

Expected: both services active/enabled, no traceback, valid Nginx configuration.

- [ ] **Step 2: Run public route checks**

Run locally:

```bash
curl -fsS https://yishucc.top/ -o /tmp/prod-home.html
curl -fsS https://yishucc.top/daily/2026-07-13 -o /tmp/prod-daily.html
curl -fsSI https://yishucc.top/static/css/style.css
curl -fsSI https://yishucc.top/admin/login
```

Expected: all routes return 200; HTTPS certificate is trusted; admin page has `Cache-Control: no-store`.

- [ ] **Step 3: Perform visual and behavior acceptance**

Open the public homepage in the in-app browser. Confirm the 1-large + 2-small top card layout, hot discussion below, deep content library below that, Doraemon-inspired NoiseFilter mark/background, mobile viewport, dated issue, article page, cover images, anonymous absence of admin controls, and authenticated admin login.

- [ ] **Step 4: Prove rollback**

Record the previous DNS targets before Task 5. Confirm rollback consists of restoring those records and running `sudo systemctl stop noisefilter nginx` only if necessary. Do not execute rollback when production checks pass.

- [ ] **Step 5: Update README and commit**

Add a short production deployment section linking `deploy/README.md`, rerun the full blog test suite, inspect `git diff --check`, then commit only repository deployment assets and documentation. Do not commit `.env`, `archive/`, `blog/data/`, SSH keys, or user-owned untracked files.

## Self-Review

- Spec coverage: production WSGI, persistence, HTTPS, DNS, admin security, data migration, visual acceptance, and rollback each have an owning task.
- Placeholder scan: the only angle-bracket values are explicitly generated secrets that must never be stored in the plan or repository; exact generation and secure transfer behavior is specified.
- Interface consistency: the service, proxy, and validation commands all use `/srv/noisefilter`, `127.0.0.1:5055`, and `yishucc.top` consistently.
