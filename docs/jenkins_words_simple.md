# Jenkins words in simple words

Each word: what it means, then an example from this project.

- **Jenkins** - a robot helper that does a list of steps in order, every time - in this project it builds, tests, packs and "deploys" the shop app.
- **CI** - checking new code automatically, again and again (Continuous Integration) - Jenkins runs the tests every time the job runs.
- **CD** - sending the checked app to where it will be used (Continuous Delivery/Deployment) - the 3 deploy stages at the end of the pipeline.
- **Pipeline** - the full list of steps, from start to finish - Checkout to the last Deploy stage.
- **Stage** - one big step inside the pipeline - "Test" is one stage.
- **Job** - one saved Jenkins task you can run with a button - the pipeline job you make from this Jenkinsfile.
- **Build** - getting the code ready and installing what it needs - the Build stage runs `pip install`.
- **Test** - automatic checks that the work is correct - pytest checks the shop app cleans orders and adds totals right.
- **Artifact / package** - the one packed file that is sent out - `shop-app.tar.gz`, made in the Package stage.
- **Deploy** - putting the artifact where it will be used - copying it to a bucket in AWS, Azure, or GCP.
- **Agent** - the computer Jenkins does the work on - `agent any` means "any free computer is fine".
- **Jenkinsfile** - the file that holds the pipeline list - the `Jenkinsfile` in the main folder of this project.
- **Credential** - a login saved safely inside Jenkins, used by ID only - `aws-creds` is an ID; the real secret is never in code.
- **Dry-run** - a practice run that prints what it WOULD do and changes nothing - all deploys here are dry-runs by default, so they are free and safe.
- **Cloud** - other computers, owned by a company, that you rent - AWS (Amazon), Azure (Microsoft), and GCP (Google) are the 3 clouds here.
