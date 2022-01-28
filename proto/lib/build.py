import os
import shutil

PROTOC_BIN_FOLDER = "./protobin/bin"
GRPC_FOLDER = "../grpc"
GO_FOLDER = "../grpc/go"
KOTLIN_FOLDER = "../grpc/kt"
KOTLIN_BUILDER_FOLDER = "./build"


def folder_exists(folder_path: str) -> bool:
    """
    Check if folder exists.

    Args:
        folder_path the path of the folder to look for.
    """
    return os.path.isdir(folder_path)


def create_clean_folder(folder_path: str):
    """
    Create a clean folder removing the old one if it exists.py

    Args:
        folder_path the path of the folder to look up.
    """
    if folder_exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)


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
            proto-files/user.proto
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


def build():
    """Build a module for all supported languages."""
    if not folder_exists(PROTOC_BIN_FOLDER):
        raise FileNotFoundError("Run setup before building the protos")

    create_clean_folder(GRPC_FOLDER)
    build_kotlin()
    build_go()


def clean_build():
    shutil.rmtree(GRPC_FOLDER)
