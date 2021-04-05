import app.extract_data.process_repositories as process_repositories
import os

def main(repo_first, repo_limit, pr_first, token):
    if not os.path.exists('tmp'):
        os.mkdir('tmp')
    process_repositories.start(repo_first, repo_limit, pr_first, token)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Create a ArcHydro schema')
    parser.add_argument('--t', metavar='path', required=True, help='Authentication token to Gihtub API')
    parser.add_argument('--rf', metavar='path', required=True, help='How many repositories retrieve per query')
    parser.add_argument('--rl', metavar='path', required=True, help='Maximum number of repositories that will be analyzed')
    parser.add_argument('--pf', metavar='path', required=True, help='How many pull requests retrieve per query')
    args = parser.parse_args()
    main(repo_first=int(args.rf.strip()), repo_limit=int(args.rl.strip()), pr_first=int(args.pf.strip()), token=args.t.strip())