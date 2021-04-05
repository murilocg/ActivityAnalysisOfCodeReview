import app.csv_manager.state_manager_utils as sm
import math

base_path = 'tmp'
base_path_repo = '{}/repos'.format(base_path)
path_repo_state = '{}/state.csv'.format(base_path_repo)

def write_repo_state(repo_index, end_cursor, total):
    sm.write_file(path_repo_state, [{ "repo_index": repo_index, "end_cursor": end_cursor, "total": total}])

def write_repo_file(repo):
    sm.save(base_path_repo, 'repositories', [repo])

def load_repo_state():
    state = sm.load_previous_state(base_path_repo)
    page_info = { "endCursor": ""}
    repo_index = 0
    total = 0
    if(any(state)):
        page_info['endCursor'] = state['end_cursor'] if not math.isnan(state['end_cursor']) else "" 
        repo_index = int(state['repo_index'])
        total = int(state['total'])
    return page_info, repo_index, total