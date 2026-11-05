# How to explain this project - ready to say

Say these lines as they are. Simple words are strong.

## 30-second version

"I made a Jenkins pipeline for a small shop app. Jenkins is like
a robot helper - when I press build, it does every step in order:
it gets the code, runs the tests, packs the app into one file,
and sends that file to three clouds - AWS, Azure, and GCP. If a
test fails, it stops and sends nothing."

## 1-minute version

"This project is about Jenkins, the automation tool. First I wrote
a tiny shop app in Python - it cleans messy orders and prints the
total sales. Then I wrote a Jenkinsfile. A Jenkinsfile is the list
of steps: Checkout, Build, Test, Package, then Deploy to AWS,
Deploy to Azure, and Deploy to GCP. The same packed file goes to
all three clouds, so all clouds get the same version. The deploys
run in dry-run mode: the scripts print exactly what they would do
and write a small log file, but they do not touch any real cloud
account, so it is free and safe. I also wrote Terraform code for
each cloud to create the storage bucket - that code is ready, but
I did not apply it. I tested everything locally: the app tests
pass, and each deploy script writes its dry-run log and will not
deploy the same version two times."

## 5 questions and answers

**Q1. What is Jenkins?**
A. "Jenkins is a robot helper. I give it a list of steps in a
Jenkinsfile, and it does them in order, the same way every time,
so no step is forgotten."

**Q2. What happens if a test fails?**
A. "The pipeline stops at the Test stage. The deploy stages never
run, so a broken app is never sent to any cloud."

**Q3. How do the 3 clouds differ here?**
A. "In this project, almost nothing differs on purpose: the same
artifact goes to a storage bucket in each cloud - S3 in AWS, Blob
storage in Azure, Cloud Storage in GCP. Only the address and the
command are different; each cloud has its own deploy script."

**Q4. Where are the passwords?**
A. "There are no passwords in the code at all. In a real run, the
owner adds the cloud logins inside Jenkins, with IDs like
aws-creds. The Jenkinsfile uses only the ID, never the secret."

**Q5. What is a dry-run?**
A. "A dry-run is a practice run. The script prints the exact
command it would run and writes a log that says 'simulated', but
it changes nothing in the cloud. It is how I tested the full
pipeline safely, with no cloud account and no cost."
