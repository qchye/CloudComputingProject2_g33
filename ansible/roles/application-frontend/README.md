# Develop frontend application locally

Prerequisite:

1. User context must be at the root of this repository

To build the docker image execute the following command:

``` bash
cd ansible/roles/application-frontend/files
docker build -f ./deployments/Dockerfile . --tag test
```

To run the docker image execute the following commands:

```bash
docker run -e FILE_TO_RUN=app.py -p 5000:5000 test
```

## PS: Please add all JS scripts/function to the [Static](ansible/roles/application-frontend/files/app/script) folder
