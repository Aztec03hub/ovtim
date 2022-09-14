# ovtim
OMRON Visual Teach Interface Module

# IMPORTANT!
This is a fast, hard, and loose refactor. Some method and variable names will change to shortened versions. This repo is very much a work-in-progress. BE AWARE!  

Please see [NAMES_TO_CHANGE.md](https://github.com/Aztec03hub/ovtim/blob/main/NAMES_TO_CHANGE.md) for list of methods/functions/variables which still need to be changed.  

This uses Jinja2 for templating. In the spirit of *quick* refactoring, Jinja's template commenting delimiter was leveraged. Look for code blocks containing `{#` ... `#}` as this is commented code and needs to be refactored!

## Original Guide Via:
https://levelup.gitconnected.com/building-a-website-starter-with-fastapi-92d077092864

## To Install (First Time):
```shell
pip install -r requirements.txt
```

## To Run:
```shell
uvicorn app.main:app --reload --port 8080
```

## To Test:
NOTE: TESTS STILL NEED TO BE WRITTEN!  
From root directory, run `pytest -v`

## To Do:
Lots, god damnit.. lots. But we're gonna create great things, mark my words.  

Add a config file manager/package of some sort. Elegance is key.  

Rectify changed names.  

Split out any lingering code into self-contained modules or classes.  

Revamp the config manager (see above).  

FUCKING HELL, use something like SSE (Server-Sent Events) or another elegant solution for server <-> client message transport. Otherwise, there *is* `fastapi_socketio` ...  


## To Save Current Environment to `requirements.txt`:
```shell
pip list --format=freeze > requirements.txt
```