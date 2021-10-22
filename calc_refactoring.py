from git import Repo


def main():
    REPO_PATH = ''
    if not REPO_PATH:
        print('Configure repo path first')
        return

    repo = Repo.init(REPO_PATH)

    calculate_refactor_in_commits(repo)

    calculate_refactor_in_blob(repo)


def calculate_refactor_in_blob(repo):

    def _iterate_blob(blob, state):
        for data in repo.blame_incremental('master', blob.path):
            state['line_of_file'] += len(data.linenos)
            msg = data.commit.message.lower().strip()
            if 'refactor' in msg:
                state['line_refactor_count'] += len(data.linenos)
            if msg.startswith('refactor'):
                state['line_start_refactor_count'] += len(data.linenos)

    def _iterate_tree(tree, state):
        for entry in tree:
            if entry.type == 'tree':
                _iterate_tree(entry, state)
                continue
            _iterate_blob(entry, state)

    master = repo.commit('master')
    state = {
        'line_of_file': 0,
        'line_refactor_count': 0,
        'line_start_refactor_count': 0,
    }
    _iterate_tree(master.tree, state)

    print('Number of line %s' % state['line_of_file'])
    print('Number of line last with refactor commit %s' % state['line_refactor_count'])
    print('Number of line last with commit start with refactor %s' % state['line_start_refactor_count'])

    print('Number of line last with refactor commit percent %s' % (float(state['line_refactor_count']) / float(state['line_of_file']) * 100.0))
    print('Number of line last with commit start with refactor percent %s' % (float(state['line_start_refactor_count']) / float(state['line_of_file']) * 100.0))


def calculate_refactor_in_commits(repo):
    commits = repo.iter_commits('master')

    count = 0
    refactor_count = 0
    start_refactor_count = 0
    for commit in commits:
        count += 1
        msg = commit.message.lower().strip()
        if 'refactor' in msg:
            refactor_count += 1
        if msg.startswith('refactor'):
            start_refactor_count += 1

    print('count : %s' % count)
    print('refactor_count : %s' % refactor_count)
    print('start_refactor_count : %s' % start_refactor_count)

    print('refactor_count_percent : %s' % (float(refactor_count) / float(count) * 100.0))
    print('start_refactor_count : %s' % (float(start_refactor_count) / float(count) * 100.0))


if __name__ == '__main__':
    main()
