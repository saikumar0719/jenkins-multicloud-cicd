# Architecture - one picture in words

```
  You push code
       |
       v
   +--------+      +----------------- JENKINS -----------------+
   | GitHub | ---> | Checkout -> Build -> Test -> Package       |
   +--------+      |                    |                       |
                   |          (tests fail? STOP.               |
                   |           nothing is deployed)            |
                   +--------------------|----------------------+
                                        v
                                  one artifact
                             (shop-app.tar.gz + version)
                                        |
              +-------------------------+-------------------------+
              v                         v                         v
      Deploy to AWS             Deploy to Azure           Deploy to GCP
      S3 bucket                 Blob container            Cloud Storage bucket
      (dry-run here)            (dry-run here)            (dry-run here)
```

## In simple words

- GitHub keeps the code.
- Jenkins is the robot helper. It reads the `Jenkinsfile` and
  does every step in order, the same way, every time.
- The Test stage is a gate. If a test fails, the pipeline stops
  and the deploy stages never run.
- Package makes ONE packed file (the artifact). The same file is
  sent to all 3 clouds, so every cloud gets the same version.
- Each deploy script has a duplicate guard: if that version is
  already marked done for a cloud, it skips instead of doing
  the same work two times.

## Where Terraform fits

Terraform is the code that CREATES the cloud places first:
one storage bucket/container in each cloud (see the `terraform/`
folder, one sub-folder per cloud). Jenkins then PUTS the artifact
into those places. Terraform is code only in this project - it
was not run against any real cloud account.
