import os
from lib.file_utils import create_clean_folder, delete_folder, folder_exists

PROTOC_BIN_FOLDER = "./protobin/bin"
GRPC_FOLDER = "../grpc"
GO_FOLDER = "../grpc/go"
KOTLIN_FOLDER = "../grpc/kt"
KOTLIN_BUILDER_FOLDER = "./build"
TYPESCRIPT_FOLDER = "../grpc/ts"


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
    os.chdir(f"{os.path.split(cwd)[0]}/grpc/ts/proto-files")

    os.system("npm init --yes")

    # Go back to previous directory.
    os.chdir(cwd)

def build():
    """Build a module for all supported languages."""
    if not folder_exists(PROTOC_BIN_FOLDER):
        raise FileNotFoundError("Run setup before building the protos")

    create_clean_folder(GRPC_FOLDER)

    build_kotlin()
    build_go()
    build_typescript()


def clean_build():
    """
    Clean everything that was created by the build execution.
    """
    delete_folder(GRPC_FOLDER)
