from pathlib import Path
import subprocess


def tpm_sign(message):
    """
    Sign a challenge using the TPM-backed private key.

    Args:
        message (str): Challenge received from the authentication server.

    Returns:
        str: Base64-encoded digital signature.

    Raises:
        RuntimeError: If the TPM signing process fails.
    """

    project_path = (
        Path(__file__).resolve().parent.parent
        / "TpmSigner"
    )

    result = subprocess.run(
        [
            "dotnet",
            "run",
            "--project",
            str(project_path),
            "--",
            message
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())

    # dotnet build warnings may appear before the signature.
    # The signature is always the last line of stdout.
    signature = result.stdout.strip().splitlines()[-1]

    return signature