# GhostDNS.py
# Script para obter o cache DNS do sistema Windows e salvar em um arquivo JSON  
# Utiliza o comando ipconfig /displaydns para capturar o cache DNS
import subprocess
import json
import os
# Função para obter o cache DNS usando o comando ipconfig /displaydns
def obter_dns_cache():
    # Executa o comando ipconfig /displaydns
    resultado = subprocess.run(
        ["ipconfig", "/displaydns"],
        capture_output=True,
        text=True,
        shell=True
    )
# Processa a saída para extrair informações relevantes
    linhas = resultado.stdout.splitlines()
    registros = []
    registro_atual = {}

    for linha in linhas:
        linha = linha.strip()

        if linha.startswith("Nome do Registro"):
            if registro_atual:
                registros.append(registro_atual)
                registro_atual = {}
            registro_atual["nome_registro"] = linha.split(":", 1)[1].strip()

        elif ":" in linha:
            chave, valor = linha.split(":", 1)
            registro_atual[chave.strip()] = valor.strip()

    if registro_atual:
        registros.append(registro_atual)

    return registros
# Função para salvar os dados em um arquivo JSON
def salvar_em_json(dados):
    caminho = os.path.join(os.getcwd(), "dns_cache.json")
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    print(f"Arquivo salvo em: {caminho}")
# Execução principal
if __name__ == "__main__":
    dns_cache = obter_dns_cache()
    salvar_em_json(dns_cache)
