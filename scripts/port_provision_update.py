import json
import os
import sys
import urllib.request

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
    port_url = os.environ.get("PORT_WEBHOOK_URL_INFRA")
    cod = os.environ.get("COD_SERVICIO")
    tecnologia = os.environ.get("TECNOLOGIA", "Java")
    run_url = os.environ.get("RUN_URL", "")

    if not port_url or not cod:
        print("ERROR: Missing PORT_WEBHOOK_URL or COD_SERVICIO", file=sys.stderr)
        return 2

    # Outputs de infra
    ecr_repo = os.environ.get("ECR_REPO", "")
    ecr_repo_arn = os.environ.get("ECR_REPO_ARN", "")
    apprunner_arn = os.environ.get("APP_RUNNER_SERVICE_ARN", "")
    apprunner_url = os.environ.get("APP_RUNNER_URL", "")

    # Regla simple de estado:
    # - si existe ECR -> Aprobado (o Generado)
    # - si además existe App Runner -> Generado
    estado = "Solicitado"
    if ecr_repo:
        estado = "Aprobado"
    if apprunner_arn:
        estado = "Generado"

    payload = {
        "microservicio": {
            "cod_servicio": cod,
            "nombre_servicio": cod,
            "tecnologia": tecnologia,
            "estado_de_aprovisionamiento": estado
            # Si quieres guardar outputs, crea properties en el blueprint y mapea aquí:
            # "ecr_repo": ecr_repo,
            # "apprunner_url": apprunner_url,
        },
        "branch": {
            "codigo_branch": f"{cod}:main",
            "build_status": "Con errores",  # el deploy real lo pondrá "Desplegado"
            "cobertura": 0,
            "vulnerabilidades_altas": 0,
            "secretos_encontrados": 0,
            "url_pipeline": run_url
        }
    }

    print(f"Updating Port: cod_servicio={cod} estado={estado} ecr={ecr_repo} apprunner={bool(apprunner_arn)}")
    post_json(port_url, payload)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
