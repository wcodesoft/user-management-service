import platform
import requests
from zipfile import ZipFile, ZipInfo
import os
from lib.file_utils import delete_folder, delete_file
from lib.check import check_go

PROTOC_BIN_FOLDER = "./protobin"
BUILD_FOLDER = "./build"

PROTO_VERSION = "3.19.2"
PROTO_REPO = "https://github.com/protocolbuffers/protobuf/releases"

PROTO_GRPC_WEB_VERSION = "1.3.1"
PROTO_GRPC_WEB_REPO = "https://github.com/grpc/grpc-web/releases"


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
    """
    Get the string representing the platform running the code.

    :return: the system string to download files from Protobuf git
    """
    system = platform.system()
    if system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "osx"
    else:
        raise SystemError("OS not supported!")


def download_file(url: str):
    """
    Download file from an url.

    Args:
        url address from the file to be downloaded.
    """
    r = requests.get(url)
    filename = url.split("/")[-1]
    open(filename, "wb").write(r.content)


def setup():
    """Initialize all necessary files.

    This will download and install all necessary files to build the libraries
    for Go and Kotlin.
    """
    system = get_platform()
    filename = f"protoc-{PROTO_VERSION}-{system}-x86_64"
    zip_file_name = f"{filename}.zip"
    url = f"{PROTO_REPO}/download/v{PROTO_VERSION}/{zip_file_name}"
    download_file(url)
    with ZipFileWithPermissions(zip_file_name, "r") as zip_ref:
        zip_ref.extractall("protobin")

    delete_file(zip_file_name)

    setup_go()
    setup_node()


def setup_go():
    """
    Check if all dependencies for Go are installed on the system. And install
    the necessary libraries.
    """
    if not check_go():
        raise SystemError("Install Go before proceeding.")

    os.system("go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest")
    os.system("go install google.golang.org/protobuf/cmd/protoc-gen-go@latest")


def setup_node():
    """
    Check if all dependencies for Typescript are installed on the system. And install
    the necessary libraries.
    """
    system = get_platform()
    if system == "mac":
        system = "darwin"

    filename = f"protoc-gen-grpc-web-{PROTO_GRPC_WEB_VERSION}-{system}-x86_64"
    url = f"{PROTO_GRPC_WEB_REPO}/download/{PROTO_GRPC_WEB_VERSION}/{filename}"
    download_file(url)

    os.system(f"chmod +x {filename}")
    os.system(f"mv {filename} ./protobin/bin/proto-gen-grpc-web")


def clean_setup():
    """
    Clean everything that was created by the setup execution.
    """
    delete_folder(PROTOC_BIN_FOLDER, BUILD_FOLDER)
