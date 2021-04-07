import pandas as pd

def start(repo_limit):
    df = pd.read_csv('tmp/repos/repositories.csv')
    repo_names = df.iloc[index].to_dict()['nome']for index in range(0, repo_limit)]
    df = pd.concat([pd.read_csv('tmp/pull_requests/{}.csv'.format(name)) for name in repo_names])
    df.to_csv('report.csv', index=False)
        