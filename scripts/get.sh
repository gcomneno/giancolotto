#!/bin/bash

# Determina la directory dello script
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Directory root del progetto (una directory sopra la directory dello script)
project_root="$(realpath "${script_dir}/..")"

# Percorso assoluto dello script principale
main_script="${project_root}/src/main.py"

# main.py
python.exe "$main_script"
