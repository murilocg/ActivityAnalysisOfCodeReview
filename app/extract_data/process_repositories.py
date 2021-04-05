
from app.api.query_repository import get_repositories
import app.extract_data.process_pull_requests as process_pull_requests
import app.csv_manager.state_manager_repo as sm
from app.utils.ProgressBar import ProgressBar

def map_repository(repo):
    return {
        "nome": repo['name'],
        "dono": repo['owner']['login'],
        "url": repo['url'],
        "id": repo['id']
    }

def start(repo_first, repo_limit, pr_first, token):
    
    initial_page_info, initial_index, initial_total = sm.load_repo_state()
    total = initial_total

    if total == repo_limit:
        print("{} repositories already processed".format(repo_limit))
        return
    
    progressbar = ProgressBar("Computing Repositories", repo_limit)
    progressbar.add(total)

    while total < repo_limit:
        page_info = initial_page_info
        data = get_repositories(repo_first, page_info['endCursor'], token)
        new_repositories = data['repositories']
        for repo_index in range(initial_index, len(new_repositories)):
            
            success = True
            repo = map_repository(new_repositories[repo_index])
            total_pull, success = process_pull_requests.start(repo, pr_first, token)

            if not success:
                sm.write_repo_state(repo_index, page_info['endCursor'], total)
                raise Exception("[ERROR] It's was not possible to compute the pull request for repository {}".format(repo['nome']))
            
            if total_pull > 0:
                total+=1
                progressbar.add(1)
                sm.write_repo_file(repo)
                sm.write_repo_state(repo_index + 1, page_info['endCursor'], total)
            else:
                sm.write_repo_state(repo_index + 1, page_info['endCursor'], total)
            
        page_info = data['page_info']

    progressbar.close()
    print("Task executed seccessfully!")