import os
import shutil


PROTOC_BIN_FOLDER = "./protobin/bin"
GRPC_FOLDER = "../grpc"
GO_FOLDER = "../grpc/go"
KOTLIN_FOLDER = "../grpc/kt"


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
            --go_out={GO_FOLDER} \
            --go-grpc_out={GO_FOLDER} \
            proto-files/user.proto
        """
    )

    with open(f"{GO_FOLDER}/user-management.proto/go.mod", "w") as go_mod:
        go_mod.write(
            """module usermanagement.proto

go 1.17

require (
	github.com/golang/protobuf v1.5.0
	google.golang.org/grpc v1.43.0
	google.golang.org/protobuf v1.27.1
)
        """
        )


def build_kotlin():
    """
    Build the Kotlin gRPC and Protobuf files on the gRPC folder.
    """
    create_clean_folder(KOTLIN_FOLDER)

    os.system(
        f"""
        export PATH="$PATH:$(go env GOPATH)/bin"

        {PROTOC_BIN_FOLDER}/protoc --plugin=protoc-gen-grpckt=./scripts/gen-grpc-kotlin.sh \
            --java_out={KOTLIN_FOLDER} --kotlin_out={KOTLIN_FOLDER} --grpckt_out={KOTLIN_FOLDER} \
            --proto_path=./proto-files/ \
            proto-files/user.proto
        """
    )

    meta_inf_folder = f"{KOTLIN_FOLDER}/META-INF"

    os.mkdir(meta_inf_folder)
    with open(f"{meta_inf_folder}/MANIFEST.MF", "w") as manifest_file:
        manifest_file.write(
            """Manifest-Version: 1.0
        Class-Path: lib-user-management-proto.jar
        Created-By: 0.0.3 (Wcode)
        """
        )

    os.system(
        f"jar cmvf {KOTLIN_FOLDER}/META-INF/MANIFEST.MF lib-user-management-proto.jar -C {KOTLIN_FOLDER} ."
    )


def build():
    if not folder_exists(PROTOC_BIN_FOLDER):
        raise Exception("Run setup before building the protos")

    create_clean_folder(GRPC_FOLDER)
    build_go()
    build_kotlin()


def clean_build():
    shutil.rmtree(GRPC_FOLDER)
