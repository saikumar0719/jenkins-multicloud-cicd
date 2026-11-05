# Running Jenkins locally

In simple words: Jenkins is a robot helper. You give it a list of
steps (the `Jenkinsfile` in the main folder). Every time you press
"Build", it does the steps in order and never forgets one.

## Start Jenkins (one time setup)

You need Docker installed. Then, from the main project folder:

```bash
docker compose -f jenkins/docker-compose.yml up -d
```

Open http://localhost:8080 in a browser. The first time, Jenkins
shows an unlock password - Docker prints it with:

```bash
docker logs sai-jenkins
```

Create your own admin user when Jenkins asks. (That login is yours;
it is never written in this project.)

## Useful plugins

The list in `plugins.txt` is short on purpose:
workflow-aggregator (runs pipelines), git (gets the code),
credentials-binding (uses saved logins safely),
pipeline-stage-view (shows the stages as boxes).
Install them under Manage Jenkins -> Plugins if they are missing.

## Make the pipeline job

1. New Item -> Pipeline -> OK.
2. Under Pipeline, choose "Pipeline script from SCM", Git,
   and give it this project folder / repository.
3. Script Path: `Jenkinsfile`.
4. Save, then press "Build Now".
5. Watch the stages: Checkout -> Build -> Test -> Package ->
   Deploy to AWS -> Deploy to Azure -> Deploy to GCP.
   The 3 deploy stages run in dry-run mode, so nothing is sent
   to any cloud and nothing costs money.

## Where the cloud logins go (real runs only)

Manage Jenkins -> Credentials -> add one credential for each cloud,
with exactly these IDs: `aws-creds`, `azure-creds`, `gcp-creds`.
The Jenkinsfile only uses the IDs - the secret values live only
inside Jenkins, never in code, never in GitHub.

## Stop Jenkins

```bash
docker compose -f jenkins/docker-compose.yml down
```
