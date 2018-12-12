import os
import git

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
EMPTY_TREE_SHA   = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"

def versions(path, branch='master'):
    """
    Shows a timeseries of file changes.
    """

    repo = git.Repo(path)

    # Iterate through every commit for the given branch in the repository
    for commit in repo.iter_commits(branch):
        parent = commit.parents[0] if commit.parents else EMPTY_TREE_SHA
        diffs  = {
            diff.a_path: diff for diff in commit.diff(parent)
        }

        for objpath, stats in commit.stats.files.items():

            diff = diffs.get(objpath)

            # Path was renamed
            if not diff:
                for diff in diffs.values():
                    if diff.b_path == path and diff.renamed:
                        break

            stats.update({
                'object': os.path.join(path, objpath),
                'commit': commit.hexsha,
                'author': commit.author.email,
                'timestamp': commit.authored_datetime.strftime(DATE_TIME_FORMAT),
                'size': diff_size(diff),
                'type': diff_type(diff),
            })

            yield stats


def diff_size(diff):
    if diff.b_blob is None and diff.deleted_file:
        # Diff represents deleted content
        return diff.a_blob.size * -1

    if diff.a_blob is None and diff.new_file:
        # New file
        return diff.b_blob.size

    return diff.a_blob.size - diff.b_blob.size


def diff_type(diff):
    if diff.renamed: return 'R'
    if diff.deleted_file: return 'D'
    if diff.new_file: return 'A'
    return 'M'

if __name__ == '__main__':
    print("Do something")