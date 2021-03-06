import pandas as pd
from datetime import datetime

def transform(pull):
    createdAt = datetime.strptime(pull['criado_em'], "%Y-%m-%dT%H:%M:%SZ")
    closedAt = datetime.strptime(pull['fechado_em'], "%Y-%m-%dT%H:%M:%SZ")
    diff = closedAt - createdAt
    hours = int(diff.total_seconds() / 3600)
    return {
        "tamanho": pull['tamanho'],
        "tempo_de_analise": hours,
        "descricao": pull['descricao'],
        "interacoes": pull['comentarios'],
        "reviews": pull['reviews']
    }

def start(repo_limit):
    df = pd.read_csv('tmp/repos/repositories.csv')
    repo_names = [df.iloc[index].to_dict()['nome'] for index in range(0, repo_limit)]
    columns = ["comentarios", "descricao", "estado", "reviews", "tamanho"]
    files = []
    for name in repo_names:
        df = pd.read_csv('tmp/sampled_data/{}.csv'.format(name), usecols = ['criado_em', 'fechado_em', "comentarios", "descricao", "tamanho", "reviews"])
        files.append(pd.DataFrame([transform(row) for index, row in df.iterrows()]))
    df = pd.concat(files)
    df.to_csv('report.csv', index=False)