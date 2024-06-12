## [OpenGrok](https://oracle.github.io/opengrok/)

> OpenGrok is a fast and usable source code search and cross reference engine.

### Setup OpenGrok using Docker

- Clone your code repo into `/src/opengrok/<repo>`
- Launch OpenGrok instance using docker image

```bash
docker run -d -e AVOID_PROJECTS=1 -e SYNC_PERIOD_MINUTES=60 -v /src/opengrok/<repo>:/opengrok/src -p 8080:8080 opengrok/docker:latest
```
