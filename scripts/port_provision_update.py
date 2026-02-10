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
    tecnologia = os.environ.get("TECNOLOGIA", "Java")
    accion = os.environ.get("ACCION", "apply")
    run_url = os.environ.get("RUN_URL", "")

    aws_region = os.environ.get("AWS_REGION", "")
    aws_account_id = os.environ.get("AWS_ACCOUNT_ID", "")
    ecr_repo = os.environ.get("ECR_REPO", cod or "")
    ecr_repository_url = os.environ.get("ECR_REPOSITORY_URL", "")

    if not port_url or not cod:
        print("ERROR: Missing PORT_WEBHOOK_URL or COD_SERVICIO", file=sys.stderr)
        return 2

    branch_identifier = f"{cod}"

    # estado de aprovisionamiento del microservicio
    if accion == "destroy":
        estado_aprov = "Sin Generar"     # o "Eliminado"
        build_status = "Pendiente"     # si mantienes branch, queda como pendiente
    else:
        estado_aprov = "Generado"
        build_status = "Pendiente"     # clave: NO es error, solo no desplegado

    payload = {
        "microservicio": {
            "cod_servicio": cod,
            "nombre_servicio": cod,
            "tecnologia": tecnologia,
            
        },
        "branch": {
            "codigo_branch": branch_identifier,
            "build_status": build_status,
            "cobertura": 0,
            "vulnerabilidades_altas": 0,
            "secretos_encontrados": 0,
            "url_pipeline": run_url,
            "estado_de_aprovisionamiento": estado_aprov
        }
    }

    # Crea/actualiza ECR entity en apply
    if accion != "destroy" and ecr_repository_url:
        payload["ecr_repository"] = {
            "identifier": f"ecr:{cod}",
            "repo_name": ecr_repo,
            "aws_region": aws_region,
            "aws_account_id": aws_account_id,
            "repository_uri": ecr_repository_url,
            "image_tag": "",
            "image_uri": "",
            "pushed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "branch_identifier": branch_identifier
        }

    print(f"Updating Port: {cod} estado_aprov={estado_aprov} build_status={build_status} ecr={bool(ecr_repository_url)}")
    post_json(port_url, payload)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
