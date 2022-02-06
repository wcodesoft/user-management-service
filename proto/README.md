# Protos

All the protos definitions for the implemented service. 

Currently `Kotlin`, `Typescript` and `Go` are the languages being supported. More will be added in the future.

## Dependencies

First is necessary to install dependencies using the pip command:

```bash
pip install -r requirements.txt
```

It's necessary to have Go and Kotlin compilers and libraries installed on your laptop.

### Kotlin

Generation of `Kotlin` is made using gradle. We are wrapping everything with `gradle wrapper` so there is not 
much setup necessary for this language.

### Golang

To install `Go` on your system follow the instructions from the following link:
https://go.dev/doc/install

### Typescript

For using `Typescript` it's necessary to have `Node` installed on the system.

An easy way to install `Node` is installing `nvm` following the guide at https://github.com/nvm-sh/nvm.
After the installation is finishes run the command:

```bash
nvm install --lts
```

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

The result from the build can be found at folder `gprc`. If no argument is passed to this 
command the supported languages will be created. 

To select specific languages you need to add the `-l` with the language code you 
want to build the gRPC and protos:

```bash
python builder.py build -l ts -l go -l kt
```

### Clean

Clean all files that were generated or downloaded by the `build` execution.

```bash
python builder.py clean
```

## Usage

This section show how to use the libraries that are generated for the builder script
into your clients.

### Kotlin

The Kotlin library can be used from the `jar` generated or importing from a 
artifactory. 
 
An example of the usage on a `build.gradle.kts` file:

```bash
implementation("org.wcode.usermanagement:proto:0.0.1")
```

### Go

The script will create a full Go module. If deployed at **Github**, to use 
on a Go module you need to only update the imports definitions on the `go.mod` file.

```go
module service

go 1.17

require (
	github.com/wcodesoft/user-management-service/grpc/go/user-management.proto v0.0.0-20220116232709-17487c730313
	google.golang.org/grpc v1.43.0 //mandatory for using gRPC
	google.golang.org/protobuf v1.27.1 //mandatory for using gRPC
	...
)
``` 