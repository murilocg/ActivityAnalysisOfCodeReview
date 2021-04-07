from app.api.query_pull_request import get_pull_requests
from datetime import datetime
from app.utils.ProgressBar import ProgressBar
import app.csv_manager.state_manager_pull as sm
import pandas as pd

def is_valid_pull_request(pull_request):
    reviews = pull_request['reviews']['totalCount']
    createdAt = datetime.strptime(pull_request['createdAt'], "%Y-%m-%dT%H:%M:%SZ")
    closedAt = datetime.strptime(pull_request['closedAt'], "%Y-%m-%dT%H:%M:%SZ")
    diff = closedAt - createdAt
    hours = diff.total_seconds() / 3600
    return reviews > 0 and hours >= 1

def map_pull_request(pr, repo):
    return {
        "repo": repo['url'],
        "fechado_em": pr['closedAt'],
        "estado": pr['state'],
        "reviews": pr['reviews']['totalCount'],
        "comentarios": pr['comments']['totalCount'],
        "participantes": pr['participants']['totalCount'],
        "tamanho": pr['additions'] + pr['deletions'],
        "descricao": len(pr['body']),
        "criado_em": pr['createdAt'],
        "id": pr['id']
    }

def import_pull(repo, repo_index, pr_first, token, page_info, total, max_prs):
    sucess = True
    progressbar = ProgressBar("Computing PRs", max_prs)
    progressbar.add(total)
    while page_info['hasNextPage']:
        try:
            data = get_pull_requests(repo['nome'], repo['dono'], pr_first, page_info['endCursor'], token)
            new_prs = data['pull_requests']
            size = len(new_prs)
            progressbar.add(size)
            total+=size
            page_info = data['page_info']
            sm.write_pull_file(repo['nome'], [map_pull_request(x, repo) for x in new_prs if is_valid_pull_request(x)])
            sm.write_pull_state(page_info['endCursor'], page_info['hasNextPage'], repo_index, total)
        except (Exception) as e:
            print(e)
            success = False
            break
    return sucess


def start(repo_limit, pr_first, token):
    df = pd.read_csv('tmp/repos/repositories.csv')
    page_info, total, repo_index = sm.load_pull_state()
    for index in range(repo_index, repo_limit):
        repo = df.iloc[index].to_dict()
        print("Processing PRS for repository {}".format(repo['nome']))
        max_prs = repo['pull_requests_closed'] + repo['pull_requests_merged']
        sucess = import_pull(repo, repo_index, pr_first, token, page_info, total, max_prs)
        if not sucess:
            break
        page_info['endCursor'] = ""
        page_indo['hasNextPage'] = True
        sm.write_pull_state(page_info['endCursor'], page_indo['hasNextPage'], repo_index + 1, 0)