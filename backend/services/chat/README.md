# Chat Service

This service is responsible connecting users through websockets.
Mainly provides features for chatting
and searching users in the system

## It uses the following to start it up

- Bash script (.sh file)
- Command line option with poetry

## For Bash

```bash
   $ bash scripts/startup.sh
```

## For Poetry command line

```bash
   $ poetry run chat migrate && poetry run chat run
```
