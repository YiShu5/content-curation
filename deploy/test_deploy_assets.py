import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEPLOY = ROOT / "deploy"


class DeploymentAssetTests(unittest.TestCase):
    def test_gunicorn_is_a_bounded_blog_dependency(self):
        requirements = (ROOT / "blog" / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("gunicorn>=22.0,<24.0", requirements.splitlines())

    def test_systemd_runs_private_gunicorn_as_ubuntu(self):
        unit = (DEPLOY / "noisefilter.service").read_text(encoding="utf-8")
        self.assertIn("User=ubuntu", unit)
        self.assertIn("EnvironmentFile=/etc/noisefilter.env", unit)
        self.assertIn("--bind 127.0.0.1:5055", unit)
        self.assertNotIn("--bind 0.0.0.0", unit)

    def test_nginx_limits_admin_login_and_proxies_to_gunicorn(self):
        nginx = (DEPLOY / "noisefilter.nginx.conf").read_text(encoding="utf-8")
        self.assertIn("server_name yishucc.top www.yishucc.top;", nginx)
        self.assertIn("proxy_headers_hash_max_size 1024;", nginx)
        self.assertIn("proxy_headers_hash_bucket_size 128;", nginx)
        self.assertIn("limit_req zone=noisefilter_admin_login", nginx)
        self.assertIn("proxy_pass http://127.0.0.1:5055;", nginx)
        self.assertIn("proxy_set_header X-Forwarded-Proto $scheme;", nginx)

    def test_code_sync_excludes_git_pointer_and_runtime_data(self):
        readme = (DEPLOY / "README.md").read_text(encoding="utf-8")
        self.assertIn("--exclude '.git'", readme)
        self.assertIn("--exclude 'archive/'", readme)
        self.assertIn("--exclude 'blog/data/'", readme)
        self.assertIn("rg -q '<title>\u964d\u566a", readme)
        self.assertIn("curl --noproxy '*' --max-time 45 -fsS http://81.70.235.230/", readme)


if __name__ == "__main__":
    unittest.main()
