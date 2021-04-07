import app.csv_manager.state_manager_utils as sm
import math

base_path = 'tmp'
base_path_pull = '{}/pull_requests'.format(base_path)
path_pull_state = '{}/state.csv'.format(base_path_pull)

def write_pull_state(end_cursor, has_next_page, repo_index, total):
    sm.write_file(path_pull_state, [{ "end_cursor": end_cursor, "has_next_page": has_next_page, "total": total, "repo_index": repo_index}])

def write_pull_file(repo_name, pull_requests):
    sm.save(base_path_pull, repo_name, pull_requests)

def load_pull_state():
    state = sm.load_previous_state(base_path_pull)
    page_info = { "endCursor": "", "hasNextPage": True}
    total = 0
    repo_index = 0
    if any(state):
        page_info['endCursor'] = str(state['end_cursor']) if not state['end_cursor'] == "" and not math.isnan(state['end_cursor']) else "" 
        page_info['hasNextPage'] = state['has_next_page']
        total = int(state['total'])
        repo_index = int(state['repo_index'])
    return page_info, total, repo_index

def delete_pull_state():
    sm.delete_state(base_path_pull)