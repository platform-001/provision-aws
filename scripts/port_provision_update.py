import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

def post_json(url: str, payload: dict) -> None:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"Port webhook status: {resp.status}")

def main() -> int:
    port_url = os.environ.get("PORT_WEBHOOK_URL")
    cod = os.environ.get("COD_SERVICIO")
    accion = os.environ.get("ACCION", "apply")
    url_action = os.environ.get("RUN_URL", "")
    aws_region = os.environ.get("AWS_REGION", "")
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID", "")
    ecr_repository_url = os.environ.get("ECR_REPOSITORY_URL", "")
    ecr_repository_arn = os.environ.get("ECR_REPOSITORY_ARN", "")

    if not port_url or not cod:
        print("ERROR: Missing PORT_WEBHOOK_URL or COD_SERVICIO", file=sys.stderr)
        return 2

    # estado de aprovisionamiento del microservicio
    if accion == "destroy":
        estado_aprov = "Sin Generar"     # o "Eliminado"
    else:
        estado_aprov = "Generado"

    payload = {
        "microservicio": {
            "identifier": cod,
            "ia_c": estado_aprov,
            "aws_region": aws_region,
            "aws_account_id": aws_account_id,
            "repository_url": ecr_repository_url,
            "repository_arn": ecr_repository_arn,
            "url_git_ia_c": url_action
        }
    }

    # Crea/actualiza ECR entity en apply
    if accion == "destroy" and ecr_repository_url:
        payload["microservicio"] = {
            "identifier": cod,
            "aws_region": "",
            "aws_account_id": "",
            "repository_url": "",
            "repository_arn": "",
            "pushed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),

        }

    print(f"Updating Port: {cod} estado_aprov={estado_aprov} ecr={bool(ecr_repository_url)}")
    post_json(port_url, payload)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
