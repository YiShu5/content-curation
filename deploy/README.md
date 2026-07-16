# NoiseFilter production deployment

Production runs on the existing Tencent Cloud Ubuntu server:

- public domain: `https://yishucc.top`
- server: `81.70.235.230`
- app root: `/srv/noisefilter`
- Gunicorn: `127.0.0.1:5055`
- service: `noisefilter.service`
- proxy: Nginx on ports 80 and 443

`archive/`, `blog/data/`, and `/etc/noisefilter.env` contain runtime state or
secrets. Code synchronization must always exclude them. Never commit them.

## First install

Run on the server:

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y nginx python3-venv python3-pip rsync certbot python3-certbot-nginx
sudo install -d -o ubuntu -g ubuntu -m 0755 /srv/noisefilter
install -d -m 0755 /srv/noisefilter/archive /srv/noisefilter/blog/data
```

Run from the repository on the deployment computer:

```bash
rsync -az --delete \
  --exclude '.git' --exclude '.venv/' --exclude 'blog/.venv/' \
  --exclude 'archive/' --exclude 'blog/data/' --exclude 'config/.env' \
  -e 'ssh -i ~/.ssh/codex_yishucc_ed25519 -o IdentitiesOnly=yes' \
  ./ ubuntu@81.70.235.230:/srv/noisefilter/
```

Upload the ignored live data separately. These commands do not delete remote
runtime files:

```bash
rsync -az \
  -e 'ssh -i ~/.ssh/codex_yishucc_ed25519 -o IdentitiesOnly=yes' \
  '/Users/yishu/YiShu Claude/content-curation/archive/' \
  ubuntu@81.70.235.230:/srv/noisefilter/archive/

rsync -az \
  -e 'ssh -i ~/.ssh/codex_yishucc_ed25519 -o IdentitiesOnly=yes' \
  '/Users/yishu/YiShu Claude/content-curation/blog/data/' \
  ubuntu@81.70.235.230:/srv/noisefilter/blog/data/
```

Create the virtual environment on the server:

```bash
python3 -m venv /srv/noisefilter/blog/.venv
/srv/noisefilter/blog/.venv/bin/python -m pip install --upgrade pip
/srv/noisefilter/blog/.venv/bin/pip install -r /srv/noisefilter/blog/requirements.txt
```

Generate production secrets on the server without printing them:

```bash
SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
BLOG_ADMIN_PASSWORD="$(python3 -c 'import secrets; print(secrets.token_urlsafe(18))')"
sudo env SECRET_KEY="$SECRET_KEY" BLOG_ADMIN_PASSWORD="$BLOG_ADMIN_PASSWORD" python3 -c 'import os; from pathlib import Path; Path("/etc/noisefilter.env").write_text("SECRET_KEY=" + os.environ["SECRET_KEY"] + "\nBLOG_ADMIN_PASSWORD=" + os.environ["BLOG_ADMIN_PASSWORD"] + "\nBLOG_TIMEZONE=America/Los_Angeles\nPUBLIC_BASE_URL=https://yishucc.top\nDAILY_ISSUES_DIR=/srv/noisefilter/blog/data/daily_issues\nSIGNAL_CACHE_PATH=/srv/noisefilter/blog/data/today_signal.json\nDAILY_EDITOR_LOG=/srv/noisefilter/blog/data/daily_editor_events.jsonl\nSESSION_COOKIE_SECURE=true\n")'
sudo chown root:root /etc/noisefilter.env
sudo chmod 600 /etc/noisefilter.env
unset SECRET_KEY BLOG_ADMIN_PASSWORD
```

Install and start the service and proxy:

```bash
sudo install -m 0644 /srv/noisefilter/deploy/noisefilter.service /etc/systemd/system/noisefilter.service
sudo install -m 0644 /srv/noisefilter/deploy/noisefilter.nginx.conf /etc/nginx/sites-available/noisefilter
sudo ln -sfn /etc/nginx/sites-available/noisefilter /etc/nginx/sites-enabled/noisefilter
if [ -L /etc/nginx/sites-enabled/default ]; then sudo unlink /etc/nginx/sites-enabled/default; fi
sudo systemctl daemon-reload
sudo systemctl enable --now noisefilter
sudo nginx -t
sudo systemctl enable --now nginx
sudo systemctl reload nginx
```

Before changing DNS, validate the prepared server from the deployment computer.
Use the raw IP for this stage: the existing EdgeOne domain binding can intercept
requests carrying `Host: yishucc.top` even when curl is given `--resolve`.

```bash
curl --noproxy '*' --max-time 45 -fsS http://81.70.235.230/ -o /tmp/noisefilter-vps-home.html
rg -q '<title>降噪' /tmp/noisefilter-vps-home.html
curl --noproxy '*' --max-time 45 -fsS http://81.70.235.230/daily/2026-07-13 -o /tmp/noisefilter-vps-daily.html
curl --noproxy '*' --max-time 45 -fsSI http://81.70.235.230/static/css/style.css
```

## DNS and TLS

After direct-IP checks pass, point the apex `@` A record to `81.70.235.230`.
Point `www` to the same address or make it a CNAME to `yishucc.top`. Then run:

```bash
sudo certbot --nginx -d yishucc.top -d www.yishucc.top --redirect --agree-tos --register-unsafely-without-email --non-interactive
sudo certbot renew --dry-run
```

## Routine code update

Run the same code `rsync` command, then on the server:

```bash
/srv/noisefilter/blog/.venv/bin/pip install -r /srv/noisefilter/blog/requirements.txt
sudo systemctl restart noisefilter
sudo systemctl is-active noisefilter
```

## Checks and logs

```bash
sudo systemctl is-active noisefilter nginx
sudo systemctl is-enabled noisefilter nginx
sudo journalctl -u noisefilter -n 100 --no-pager
sudo nginx -t
curl -fsS http://127.0.0.1:5055/ -o /tmp/noisefilter-app.html
```

## Rollback

The fastest public rollback is to restore the two previous DNS records for
`yishucc.top` and `www.yishucc.top`. The old EdgeOne target must be recorded
before the DNS change. The prepared VPS can remain running while DNS rolls
back; if it must be stopped, run:

```bash
sudo systemctl stop noisefilter nginx
```

Do not remove `/srv/noisefilter/archive`, `/srv/noisefilter/blog/data`, or
`/etc/noisefilter.env` during rollback.
