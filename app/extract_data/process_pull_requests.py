from app.api.query_pull_request import get_pull_requests
from datetime import datetime
from app.utils.ProgressBar import ProgressBar
import app.csv_manager.state_manager_pull as sm

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

def start(repo, pr_first, token):
    page_info, total, count = sm.load_pull_state()
    progressbar = ProgressBar("Computing PRs")
    progressbar.add(total)
    success = True
    print('Repository {}'.format(repo['nome']))
    while page_info['hasNextPage']:
        try:
            data = get_pull_requests(repo['nome'], repo['dono'], pr_first, page_info['endCursor'], token)
            page_info = data['page_info']
            new_prs = data['pull_requests']
            total_count = data['total_count']
            if total_count < 100:
                break
            progressbar.maximum = total_count
            progressbar.add(len(new_prs))
            pull_requests = [map_pull_request(x, repo) for x in new_prs if is_valid_pull_request(x)]
            count+=len(pull_requests)
            total+=len(new_prs)
            sm.write_pull_file(repo['nome'], pull_requests)
            sm.write_pull_state(page_info['endCursor'], page_info['hasNextPage'], total, count)
        except (Exception) as e:
            print(e)
            success = False
            break
    progressbar.close()
    if success:
        sm.delete_pull_state()
    return count, success