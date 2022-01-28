# Protos

All the protos definitions for the implemented service. 

Currently `Kotlin` and `Go` are the languages being supported. More will be added in the future.

## Dependencies

First is necessary to install dependencies using the pip command:

```bash
pip install -r requirements.txt
```

It's necessary to have Go and Kotlin compilers and libraries installed on your laptop.

### Kotlin

Kotlin generation is made by using gradle. We are wrapping everything with `gradle wrapper` so there is not much setup necessary for this language.

### Golang

## Available commands

Execute the following commands on the same folder holding the `builder.py` file

### Setup

This will download all necessary files to build proto for all supported languages.

```bash
python builder.py setup
```

### Build

Will build the libraries for client and service for the supported languages.

```bash
python builder.py build
```

The result from the build can be found at folder `gprc`.

### Clean

Clean all files that were generated or downloaded by the `build` execution.

```bash
python builder.py clean
```