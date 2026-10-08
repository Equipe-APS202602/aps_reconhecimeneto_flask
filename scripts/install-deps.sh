#!/usr/bin/env bash
# Script para instalar cada dependência individualmente (Linux/macOS)
set -euo pipefail

packages=(
  Flask
  opencv-contrib-python
  mysql-connector-python
  python-dotenv
  "Flask-Login"
  bcrypt
)

for p in "${packages[@]}"; do
  echo "Instalando $p..."
  python3 -m pip install "$p" --upgrade
done

echo "Todas as dependências foram instaladas com sucesso."
