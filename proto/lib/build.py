import os
import shutil


PROTOC_BIN_FOLDER = "./protobin/bin"
GRPC_FOLDER = "./grpc"
GO_FOLDER = "./grpc/go"
KOTLIN_FOLDER = "./grpc/kt"


def folder_exists(folder_path: str) -> bool:
    return os.path.isdir(folder_path)


def create_clean_folder(folder_path: str):
    if folder_exists(folder_path):
        shutil.rmtree(folder_path)
    os.mkdir(folder_path)


def build_go():
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


def build_kotlin():
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

    # os.system(f"jar cvf lib-user-management-proto.jar -C {KOTLIN_FOLDER} .")


def build():
    if not folder_exists(PROTOC_BIN_FOLDER):
        raise Exception("Run setup before building the protos")

    create_clean_folder(GRPC_FOLDER)
    build_go()
    build_kotlin()


def clean_build():
    shutil.rmtree(GRPC_FOLDER)
