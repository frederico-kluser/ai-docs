#!/usr/bin/env python3
"""
Script para renomear arquivos no diretório para seguir a convenção de
caixa baixa e underscores em vez de hífens.
"""

import os
import sys
from pathlib import Path

def convert_filename(filename):
    """
    Converte o nome do arquivo para caixa baixa e substitui hífens por underscores.
    """
    # Primeiro, obter a extensão para preservá-la
    base_name, ext = os.path.splitext(filename)
    
    # Converter para caixa baixa
    base_name = base_name.lower()
    
    # Substituir hífens por underscores
    base_name = base_name.replace('-', '_')
    
    # Retornar o nome completo
    return f"{base_name}{ext}"

def main():
    # Obter o diretório do script ou o diretório passado como argumento
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Processando arquivos em: {directory}")
    
    # Lista de pares (nome_original, novo_nome) para mostrar ao usuário
    renamed_files = []
    
    # Primeiro passo: coletar todos os arquivos a serem renomeados
    for filename in os.listdir(directory):
        # Ignorar diretórios, arquivos ocultos e o próprio script
        if (os.path.isdir(os.path.join(directory, filename)) or 
            filename.startswith('.') or 
            filename == os.path.basename(__file__) or
            filename.endswith('.py')):
            continue
        
        # Calcular o novo nome
        new_filename = convert_filename(filename)
        
        # Verificar se o arquivo já está no formato correto
        is_correct_format = (
            filename == filename.lower() and  # já está em caixa baixa
            '-' not in filename              # não contém hífens
        )
        
        # Se o nome for diferente e não estiver no formato correto, adicionar à lista de renomeações
        if new_filename != filename or not is_correct_format:
            renamed_files.append((filename, new_filename))
    
    # Exibir preview das mudanças
    if renamed_files:
        print("\nAs seguintes renomeações serão feitas:")
        for old_name, new_name in renamed_files:
            print(f"{old_name} -> {new_name}")
        
        # No ambiente Claude Code, executamos automaticamente
        print("\nProsseguindo com a renomeação automaticamente...")
        
        # Verificar colisões potenciais de nome (caso sensível vs insensível)
        name_collisions = {}
        for old_name, new_name in renamed_files:
            lower_name = new_name.lower()
            if lower_name in name_collisions:
                print(f"AVISO: Potencial colisão de nome detectada: '{new_name}' e '{name_collisions[lower_name]}'")
            name_collisions[lower_name] = new_name
        
        # Criar lista temporária para arquivos que precisam ser renomeados com um nome temporário
        # para evitar colisões em sistemas de arquivos que não diferenciam maiúsculas de minúsculas
        temp_renames = []
        for old_name, new_name in renamed_files:
            if old_name.lower() == new_name.lower() and old_name != new_name:
                temp_name = f"{new_name}._temp_"
                temp_renames.append((old_name, temp_name, new_name))
        
        # Segundo passo: renomear os arquivos usando nomes temporários quando necessário
        for item in temp_renames:
            old_name, temp_name, final_name = item
            old_path = os.path.join(directory, old_name)
            temp_path = os.path.join(directory, temp_name)
            
            try:
                os.rename(old_path, temp_path)
                print(f"Renomeado (temp): {old_name} -> {temp_name}")
            except Exception as e:
                print(f"ERRO ao renomear temporariamente '{old_name}': {str(e)}")
        
        # Agora renomear os arquivos normais e os temporários para seus nomes finais
        for old_name, new_name in renamed_files:
            # Pular aqueles que foram renomeados temporariamente
            if any(old_name == item[0] for item in temp_renames):
                continue
                
            old_path = os.path.join(directory, old_name)
            new_path = os.path.join(directory, new_name)
            
            # Verificar se o novo nome já existe
            if os.path.exists(new_path) and old_path != new_path:
                print(f"ERRO: '{new_name}' já existe. Pulando renomeação de '{old_name}'.")
                continue
            
            try:
                os.rename(old_path, new_path)
                print(f"Renomeado: {old_name} -> {new_name}")
            except Exception as e:
                print(f"ERRO ao renomear '{old_name}': {str(e)}")
                
        # Finalmente, renomear os arquivos temporários para seus nomes finais
        for old_name, temp_name, final_name in temp_renames:
            temp_path = os.path.join(directory, temp_name)
            final_path = os.path.join(directory, final_name)
            
            # Verificar se o nome final já existe
            if os.path.exists(final_path):
                print(f"ERRO: '{final_name}' já existe. Mantendo nome temporário '{temp_name}'.")
                continue
                
            try:
                os.rename(temp_path, final_path)
                print(f"Renomeado (final): {temp_name} -> {final_name}")
            except Exception as e:
                print(f"ERRO ao finalizar renomeação '{temp_name}': {str(e)}")
        
        print("\nProcesso de renomeação concluído.")
    else:
        print("Nenhum arquivo precisa ser renomeado.")

if __name__ == "__main__":
    main()