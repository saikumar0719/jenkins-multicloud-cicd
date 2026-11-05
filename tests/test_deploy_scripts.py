import json
import os
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]

CLOUDS = {
    "aws": "deploy_aws.sh",
    "azure": "deploy_azure.sh",
    "gcp": "deploy_gcp.sh",
}


def run_script(script_path, workdir, log_dir):
    artifact = workdir / "dummy.tar.gz"
    artifact.write_bytes(b"demo artifact")
    env = dict(os.environ)
    env.update(
        {
            "DRY_RUN": "true",
            "VERSION": "9.9.9",
            "ARTIFACT": str(artifact),
            "LOG_DIR": str(log_dir),
        }
    )
    return subprocess.run(
        ["bash", str(script_path)],
        cwd=workdir,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )


def test_each_deploy_script_dry_run_and_duplicate_guard(tmp_path):
    for cloud, script_name in CLOUDS.items():
        workdir = tmp_path / cloud
        workdir.mkdir()
        log_dir = workdir / "logs"
        script = ROOT / "scripts" / script_name

        first = run_script(script, workdir, log_dir)
        assert first.returncode == 0, first.stderr

        log_file = log_dir / f"deploy-{cloud}.json"
        assert log_file.is_file()
        data = json.loads(log_file.read_text(encoding="utf-8"))
        assert data["cloud"] == cloud
        assert data["mode"] == "dry-run"
        assert data["status"] == "simulated"
        assert data["version"] == "9.9.9"

        second = run_script(script, workdir, log_dir)
        assert second.returncode == 0, second.stderr
        assert "already done, skipping" in second.stdout
