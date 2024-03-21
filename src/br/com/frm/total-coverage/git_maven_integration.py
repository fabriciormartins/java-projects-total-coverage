import shutil
import subprocess
import re
import os
from datetime import datetime, timedelta
from consolidate_coverage_reports import ConsolidateCoverageReports

   
projects_directories = []

# Lendo lista de Repositórios e Executando o clone do Git
def clone_repositories_of_file(arquivo_repositorios, diretorio_destino):
    if(os.path.getsize(arquivo_repositorios) ==0):
        path_repositories = os.listdir(diretorio_destino)
        for path in path_repositories:
               projects_directories.append(f"{diretorio_destino}/{path}")
        return
    with open(arquivo_repositorios, 'r') as f:
        for linha in f:
            url_repositorio = linha.strip()  # Remover espaços em branco e caracteres de nova linha
            repositorie_name = extract_repositorie_name(url_repositorio)
            print(repositorie_name)
            clone_repositorie(url_repositorio, f"{diretorio_destino}/{repositorie_name}")

def clone_repositorie(url_repositorio, diretorio_destino):
    git_clone_command = ["git", "clone", "-b", "develop", url_repositorio, diretorio_destino]
    try:
        if os.path.exists(diretorio_destino):
            subprocess.run(["git", "pull"], check=True, cwd=diretorio_destino)
            print(f"{diretorio_destino} já existia, foi atualizado")
            projects_directories.append(diretorio_destino)
            return
        
        print(f"\n Clonando repositório {url_repositorio}")
        subprocess.run(git_clone_command, check=True)
        print(f"\nRepositório {url_repositorio} clonado com sucesso!")
        projects_directories.append(diretorio_destino)
    except subprocess.CalledProcessError as e:
        print(f"\nErro ao clonar o repositório {url_repositorio}:", e)


def extract_repositorie_name(url_repositorio):
    # Expressão regular para extrair o nome do projeto da URL do repositório
    padrao = r'.*/(.*?)(?:\.git)?$'  # O padrão busca o último segmento na URL, antes do .git, se presente
    
    # Procurar por correspondências na URL do repositório
    correspondencia = re.search(padrao, url_repositorio)
    
    if correspondencia:
        return correspondencia.group(1)
    else:
        return None
# Executando o comando do Maven
def run_tests(caminho_projeto):
    maven_compile_command = ["mvn", "test", "-U", "-q"]
    try:
        target_path = f"{caminho_projeto}/target"
        if(is_modified_last_one_hour(target_path)):
            print(f"\n\n\t {target_path} has files with not change")
            return
                
        print(f"\n Executando testes projeto {caminho_projeto}")
        subprocess.run(maven_compile_command, check=True, cwd=caminho_projeto)
        print("\n Testes do projeto executados com sucesso!")
    except subprocess.CalledProcessError as e:
      print(f"\n Erro ao executar testes do projeto: {caminho_projeto}", e)

def execute_maven_test_in_repositories():
    for project_directory in projects_directories:
        run_tests(project_directory)

def consolidate_coverages():
    project_directorie_reports = []
    for project_directory in projects_directories:
        project_directorie_reports.append( f"{project_directory}/target/site/jacoco/")
        print(f"\n\n Search for results of coverage in {project_directorie_reports}")

    if len(project_directorie_reports) > 0:
        consolidate_reports = ConsolidateCoverageReports()
        consolidate_reports.consolidate_coverage_reports(project_directorie_reports)

def is_modified_last_one_hour(path:str):
    if not os.path.exists(path=path) or len(os.listdir(path=path))==0:
        return False

     # Obtém a data de modificação do diretório
    data_modificacao = datetime.fromtimestamp(os.path.getmtime(path))
    
    # Calcula a diferença entre a data atual e a data de modificação
    diferenca = datetime.now() - data_modificacao
    
    # Verifica se a diferença é menor que 2 horas
    return diferenca < timedelta(hours=2)

def remove_repositorie_files():
      shutil.rmtree(diretorio_destino)

arquivo_repositorios = "repositories"
diretorio_destino = "repositories_files"

clone_repositories_of_file(arquivo_repositorios, diretorio_destino)
execute_maven_test_in_repositories()
consolidate_coverages()
# remove_repositorie_files()
