import os
from typing import List
from lib.file_utils import create_clean_folder, delete_folder, folder_exists

PROTOC_BIN_FOLDER = "./protobin/bin"
GRPC_FOLDER = "../grpc"
GO_FOLDER = "../grpc/go"
KOTLIN_FOLDER = "../grpc/kt"
KOTLIN_BUILDER_FOLDER = "./build"

TYPESCRIPT_FOLDER = "../grpc/ts"
TS_LIBRARY_VERSION = os.getenv('TS_LIBRARY_VERSION', "0.0.1")


def build_go():
    """
    Build the GO gRPC and Protobuf files on the gRPC folder.
    """
    create_clean_folder(GO_FOLDER)
    os.system(
        f"""
        export PATH="$PATH:$(go env GOPATH)/bin"

        {PROTOC_BIN_FOLDER}/protoc \
            --go_out={GO_FOLDER} --go_opt=paths=source_relative \
            --go-grpc_out={GO_FOLDER} --go-grpc_opt=paths=source_relative \
            proto-files/*.proto
        """
    )

    cwd = os.getcwd()

    os.rename(
        f"{os.path.split(cwd)[0]}/grpc/go/proto-files",
        f"{os.path.split(cwd)[0]}/grpc/go/user-management.proto",
    )

    # Change the current working directory.
    os.chdir(f"{os.path.split(cwd)[0]}/grpc/go/user-management.proto")

    os.system(
        "go mod init github.com/wcodesoft/user-management-service/grpc/go/user-management.proto"
    )
    os.system("go mod tidy")

    # Go back to previous directory.
    os.chdir(cwd)


def build_kotlin():
    """
    Build the Kotlin gRPC and Protobuf files on the gRPC folder.
    """
    create_clean_folder(KOTLIN_FOLDER)

    os.system("./gradlew build")
    generated_file = os.listdir(f"{KOTLIN_BUILDER_FOLDER}/libs")[0]
    os.system(f"mv {KOTLIN_BUILDER_FOLDER}/libs/{generated_file} {KOTLIN_FOLDER}")
    os.system(f"rm -rf {KOTLIN_BUILDER_FOLDER}")


def build_typescript():
    create_clean_folder(TYPESCRIPT_FOLDER)

    os.system(
        f"""
        {PROTOC_BIN_FOLDER}/protoc  --plugin=protoc-gen-grpc-web={PROTOC_BIN_FOLDER}/proto-gen-grpc-web \
            --js_out=import_style=commonjs,binary:{TYPESCRIPT_FOLDER} \
            --grpc-web_out=import_style=commonjs+dts,mode=grpcwebtext:{TYPESCRIPT_FOLDER} \
            proto-files/*.proto
        """
    )

    cwd = os.getcwd()

    # Change the current working directory.
    os.chdir(f"{os.path.split(cwd)[0]}/grpc/ts")
    os.system("mkdir user-management")
    os.system("mv proto-files user-management")
    os.chdir(f"{os.path.split(cwd)[0]}/grpc/ts/user-management")

    with open("package.json", "w") as f_out:
        f_out.write(f"""{{
  "name": "@wcodesoft/user-management",
  "version": "{TS_LIBRARY_VERSION}",
  "description": "",
  "main": "index.js",
  "scripts": {{
    "test": "echo 'Error: no test specified' && exit 1"
 }},
  "keywords": [],
  "author": "Wcodesoft",
  "license": "MIT",
  "dependencies": {{
    "@grpc/grpc-js": "^1.5.4",
    "@types/google-protobuf": "^3.15.5",
    "google-protobuf": "^3.19.4"
  }},
  "repository": {{
    "type": "git",
    "url": "https://github.com/wcodesoft/user-management-service.git"
  }}
}}
        """)

    os.system("npm install")

    # Go back to previous directory.
    os.chdir(cwd)


def build(languages: List[str]):
    """Build a module for all supported languages."""
    if not folder_exists(PROTOC_BIN_FOLDER):
        raise FileNotFoundError("Run setup before building the protos")

    if 'kt' in languages:
        print("Building protos for Kotlin.")
        build_kotlin()

    if 'go' in languages:
        print("Building protos for Go.")
        build_go()

    if 'ts' in languages:
        print("Building protos for Typescript.")
        build_typescript()


def clean_build():
    """
    Clean everything that was created by the build execution.
    """
    delete_folder(KOTLIN_FOLDER, TYPESCRIPT_FOLDER)
