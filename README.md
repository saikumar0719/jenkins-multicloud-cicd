# Jenkins Multi-Cloud CI/CD - one app, three clouds

## In plain language - the shop story

Think of a shop worker who is very careful. Every time new stock
comes in, this worker does the same steps, in the same order,
and never forgets one:

1. Take the goods in.
2. Check every item.
3. Pack them in one box.
4. Send the same box to the shop's 3 storage rooms.

**Jenkins is that worker, as software.** It is a robot helper.
You give it a list of steps in a file called a `Jenkinsfile`.
When you press "Build", Jenkins does the steps in order -
get the code, install, test, pack - and then sends the packed
app to all 3 clouds: **AWS, Azure, and GCP**.

In this project the "goods" are a tiny shop app (in `app/`):
it reads messy shop orders, cleans duplicates and bad amounts,
and prints the true total sales - the same story as the basic
data-pipeline project, in the smallest possible form.

## Pipeline order (the Jenkinsfile stages)

```
Checkout -> Build -> Test -> Package
         -> Deploy to AWS -> Deploy to Azure -> Deploy to GCP
```

The same artifact (one packed file, `shop-app.tar.gz`) goes to
all 3 clouds, so every cloud receives the same version.

## Honest status - read this first

**The Jenkins pipeline and the dry-run deploys were built and
tested locally. They were NOT run on real cloud accounts.**
No real cloud account, and no cloud login of any kind, exists
in this project. The deploy scripts run in dry-run mode by
default: they print exactly what they WOULD do and write a
small log file (`logs/deploy-<cloud>.json`). The Terraform in
`terraform/` is the real cloud setup code for each cloud -
code only, NOT applied, so nothing was created and nothing
was charged.

## Run everything locally - no cloud account needed

```bash
cd jenkins-multicloud-cicd
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

PYTHONPATH=. python -m pytest -q     # app, Jenkinsfile and deploy-script tests
python3 app/main.py                  # the shop app: raw 11 -> clean 8, total 10550.00

DRY_RUN=true bash scripts/deploy_aws.sh
DRY_RUN=true bash scripts/deploy_azure.sh
DRY_RUN=true bash scripts/deploy_gcp.sh
cat logs/deploy-aws.json logs/deploy-azure.json logs/deploy-gcp.json
```

Each dry-run log says its cloud, the version, `mode: dry-run`
and `status: simulated`.

## Run Jenkins itself locally (optional, needs Docker)

```bash
docker compose -f jenkins/docker-compose.yml up -d
```

Then open http://localhost:8080 and make a Pipeline job from
this project's `Jenkinsfile`. Full steps, in simple words, are
in `jenkins/README.md`.

## What a real cloud run would need

1. Your own accounts in AWS, Azure, and GCP.
2. The cloud logins added inside Jenkins (Manage Jenkins ->
   Credentials) with exactly these IDs: `aws-creds`,
   `azure-creds`, `gcp-creds`. Secrets live only in Jenkins -
   never in code, never in GitHub.
3. The Terraform applied once per cloud (`terraform/aws`,
   `terraform/azure`, `terraform/gcp`) to create the storage
   bucket/container the artifact goes into.
4. The matching CLI installed where Jenkins runs (`aws`, `az`,
   `gcloud`), and `DRY_RUN=false` set for the deploy stages.

Cost note: cloud storage costs money on real accounts. Dry-run
is free. On real accounts, keep the small storage in this
Terraform, delete old artifacts, and destroy what you no longer
need (`terraform destroy` in that cloud's folder).

## Design answers, grounded in the code

- **Re-running a failed stage:** Jenkins always restarts the
  job from the top; the stages are safe to repeat because the
  Package stage just rebuilds the same artifact, and each
  deploy script checks its version marker before doing work.
- **Duplicate handling:** a deploy script writes
  `logs/deploy-<cloud>.json` with the version it finished.
  If the same version is already there, it prints
  "already done, skipping" - the same version is never
  deployed twice to the same cloud.
- **Cost control:** dry-run is the default everywhere, the
  Terraform creates only one small storage bucket/container
  per cloud, and the destroy step above removes it all.
- **Data quality gating (the test gate):** the Deploy stages
  come after the Test stage in the Jenkinsfile. If any test
  fails, Jenkins stops the pipeline there and the deploy
  stages do not run at all - a broken app is never sent out.

## Words and explaining

- `docs/jenkins_words_simple.md` - 15 Jenkins/cloud words,
  each in one simple line.
- `docs/how_to_explain.md` - a 30-second and a 1-minute
  script, plus 5 interview questions and answers.
- `docs/architecture.md` - the whole picture in one diagram.

Run the local steps once before an interview, so your answers
come from doing the work, not from reading about it.
