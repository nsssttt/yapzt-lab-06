# Lab 06 - CI for Pull Requests

This pipeline runs Python unit tests and checks for an approved review on pull requests into `develop`. The review check gates static analysis and the Cloc artifact.

```sh
python -m unittest discover -s tests -v
```

To exercise the workflow, open a pull request from a feature branch into `develop` and submit an independent approval. Reviewdog comments are enabled for same-repository pull requests. A push workflow also runs the tests after a merge.

To run the optional SonarQube job, configure the repository variable `SONAR_HOST_URL` and the Actions secret `SONAR_TOKEN` for your own server.
