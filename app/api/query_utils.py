import requests
import time

endpoint = "https://api.github.com/graphql"
interval_retry = 5
max_retries = 5

def create_query(params, query_template):
  q = query_template
  for k in params.keys():
      value = params[k]
      if type(value) == int:
          q = add_param_number(k, value, q)
      else:
          q = add_param_string(k, value, q)
  return q

def add_param_number(name, value, query):
    return query.replace(name, '%d' % value) 

def add_param_string(name, value, query):
    return query.replace(name, "null") if value == "" else query.replace(name, '"%s"' % value) 

def retry(status_code, query, token, sleep):
    next_sleep = sleep + interval_retry
    print("[WARN] GitHub API returned {}, Retrying after {} seconds...".format(status_code, next_sleep))
    retry_count = sleep/interval_retry
    if retry_count == max_retries:
        raise Exception("Exceed maximum retry")
    time.sleep(sleep)
    return execute_query(query, token, next_sleep)


def execute_query(query, token, sleep = 0):
    request = requests.post(endpoint, json = {'query': query}, headers = {
      'Content-Type': 'application/json',
      'Authorization': 'bearer ' + token
    })
    if  request.status_code == 200:
        return request.json()
    else:
        return retry(request.status_code, query, token, sleep)