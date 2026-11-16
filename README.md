# Lab 06 - CI for Pull Requests

This pipeline runs Python unit tests and checks for an approved review on pull requests into `develop`. The review check gates static analysis, the Cloc artifact, and a SonarQube analysis of the approved pull request snapshot. Pushes to `main` run SonarQube Community Build in a temporary Docker container on the GitHub runner. Each scan checks the Quality Gate and removes its server and generated token when the job finishes.

```sh
python -m unittest discover -s tests -v
```

To exercise the workflow, open a pull request from a feature branch into `develop` and submit an independent approval. Reviewdog comments are enabled for same-repository pull requests. A push workflow also runs the tests after a merge.

Run SonarQube from **Actions > CI Pipeline > Run workflow** with the `main` branch selected. The first setup takes a few minutes while the temporary server starts. This hosted scan needs no repository secret. Each approved pull request is scanned in its own temporary project as the default branch. Community Build does not add GitHub pull request decorations or persist separate branch history.

To rerun an approved pull request manually, choose its head branch and enter its pull request number. The job verifies that the selected commit matches the open pull request into `develop` and still has an approval.
