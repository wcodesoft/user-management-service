import platform
import requests
from zipfile import ZipFile, ZipInfo
import os
import shutil

PROTOC_BIN_FOLDER = "./protobin"
PROTO_VERSION = "3.19.2"
PB_REL = "https://github.com/protocolbuffers/protobuf/releases"
KOTLIN_GRPC_FILE = "protoc-gen-grpc-kotlin-1.2.0-jdk7.jar"
KOTLIN_GRPC_URL = f"https://repo1.maven.org/maven2/io/grpc/protoc-gen-grpc-kotlin/1.2.0/{KOTLIN_GRPC_FILE}"


from zipfile import ZipFile, ZipInfo


class ZipFileWithPermissions(ZipFile):
    """Custom ZipFile class handling file permissions."""

    def _extract_member(self, member, targetpath, pwd):
        if not isinstance(member, ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)

        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(targetpath, attr)
        return targetpath


def get_platform() -> str:
    system = platform.system()
    if system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "osx"
    else:
        raise Exception("OS not supported!")


def download_file(url: str):
    r = requests.get(url)
    filename = url.split("/")[-1]
    open(filename, "wb").write(r.content)


def setup():
    system = get_platform()
    filename = f"protoc-{PROTO_VERSION}-{system}-x86_64"
    zipFileName = f"{filename}.zip"
    url = f"{PB_REL}/download/v{PROTO_VERSION}/{zipFileName}"
    download_file(url)
    with ZipFileWithPermissions(zipFileName, "r") as zip_ref:
        zip_ref.extractall("protobin")

    os.remove(zipFileName)

    os.system("go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest")
    os.system("go install google.golang.org/protobuf/cmd/protoc-gen-go@latest")

    download_file(KOTLIN_GRPC_URL)
    os.rename(f"./{KOTLIN_GRPC_FILE}", f"./scripts/{KOTLIN_GRPC_FILE}")


def clean_setup():
    shutil.rmtree(PROTOC_BIN_FOLDER)
    os.remove(f"./scripts/{KOTLIN_GRPC_FILE}")