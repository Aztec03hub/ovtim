# ovtim
OMRON Visual Teach Interface Module

# IMPORTANT!
This is a fast, hard, and loose refactor. Some method and variable names will change to shortened versions. This repo is very much a work-in-progress. BE AWARE!

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
Lots, god damnit. Lots. But we're gonna create great things, mark my words.
Add a config file manager/package of some sort.

## To Save Current Environment to `requirements.txt`:
```shell
pip list --format=freeze > requirements.txt
```