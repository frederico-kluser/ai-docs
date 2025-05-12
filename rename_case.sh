#!/bin/bash

# Files with uppercase to rename
files_to_rename=(
  "Automatizando_Investimentos_B3_Guia_Desenvolvedores_React.md"
  "Educacao_IA_Brasil_Cursos_EAD_Comparativo.md"
  "Frameworks_React_IA_Voz_Interfaces.md"
)

for file in "${files_to_rename[@]}"; do
  lowercase=$(echo "$file" | tr '[:upper:]' '[:lower:]')
  if [ "$file" != "$lowercase" ]; then
    echo "Renaming $file to $lowercase"
    git mv -f "$file" "$lowercase"
  fi
done