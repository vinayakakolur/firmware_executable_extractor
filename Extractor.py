import os
import json
import argparse
import subprocess
from pathlib import Path

def find_elf_files(root_path):
    elf_files = []

    for root, _, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                result = subprocess.run(
                    ["file", file_path],
                    capture_output=True,
                    text=True
                )

                if "ELF" in result.stdout:
                    elf_files.append(file_path)

            except Exception:
                continue

    return elf_files

    def extract_metadata(file_path):

    result = subprocess.run(
        ["file", file_path],
        capture_output=True,
        text=True
    )

    output = result.stdout

    metadata = {
        "name": Path(file_path).name,
        "path": file_path,
        "size": os.path.getsize(file_path),
        "architecture": None,
        "bits": None,
        "endianness": None,
        "interpreter": None,
        "stripped": None
    }

    if "32-bit" in output:
        metadata["bits"] = 32
    elif "64-bit" in output:
        metadata["bits"] = 64

    if "LSB" in output:
        metadata["endianness"] = "LSB"

    elif "MSB" in output:
        metadata["endianness"] = "MSB"

    if "MIPS" in output:
        metadata["architecture"] = "MIPS"

    elif "ARM" in output:
        metadata["architecture"] = "ARM"

    elif "x86-64" in output:
        metadata["architecture"] = "x86_64"

    if "interpreter" in output:
        start = output.find("interpreter")
        metadata["interpreter"] = output[start:].split(",")[0].replace("interpreter ", "")

    metadata["stripped"] = "not stripped" not in output

    return metadata

    def save_json(data, filename="metadata.json"):

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(f"\nMetadata written to {filename}")

    def main():

    parser = argparse.ArgumentParser(
        description="Firmware Metadata Extractor"
    )

    parser.add_argument(
        "rootfs",
        help="Path to extracted firmware filesystem"
    )

    args = parser.parse_args()

    print("[+] Searching for ELF binaries...")

    elf_files = find_elf_files(args.rootfs)

    print(f"[+] Found {len(elf_files)} ELF files")

    metadata = []

    for elf in elf_files:
        metadata.append(extract_metadata(elf))

    save_json(metadata)

    if __name__ == "__main__":
    main()
