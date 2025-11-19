import os
import pydoc
from datetime import datetime

os.environ.setdefault("PYTHONPATH", os.getcwd())

modules = [
    "main",
    "db.db",
    "auxiliar.auxiliar",

    "model.exame",
    "repository.exame_repository",
    "services.exame_service",
    "routes.exame_routes",

    "model.usuario",
    "repository.usuario_repository",
    "services.usuario_service",
    "routes.usuario_routes",

    "services.google_services.google_service",
    "services.google_services.envio_email",
    "services.google_services.envio_drive",

    "model.cliente",
    "repository.cliente_repository",
    "services.cliente_service",
    "routes.cliente_routes",

    "model.atendimento",
    "repository.atendimento_repository",
    "services.atendimento_service",
    "routes.atendimento_routes"
]

out_path = "pydoc.md"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(f"# Pydoc gerado em {datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
    for m in modules:
        f.write("\n---\n\n")
        f.write(f"## Módulo: {m}\n\n")
        try:
            # CORREÇÃO AQUI — usar renderer válido
            doc = pydoc.render_doc(m, renderer=pydoc.plaintext)
            f.write(doc + "\n")
        except Exception as e:
            f.write(f"Erro ao gerar pydoc para {m}: {e}\n")
