import json
import os
import urllib.request

def post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req)

accion = os.environ.get("ACCION", "apply")
cod = os.environ.get("COD")
url = os.environ.get("PORT_WEBHOOK_URL")
run_url = os.environ.get("RUN_URL", "")

if accion == "destroy":
    estado = "Rechazado"
else:
    estado = "Generado"

payload = {
    "microservicio": {
        "cod_servicio": cod,
        "nombre_servicio": cod,
        "estado_de_aprovisionamiento": estado
    },
    "branch": {
        "codigo_branch": f"{cod}:main",
        "build_status": "Con errores",
        "cobertura": 0,
        "vulnerabilidades_altas": 0,
        "secretos_encontrados": 0,
        "url_pipeline": run_url
    }
}

post_json(url, payload)

print(f"Port actualizado → {cod} estado={estado}")
