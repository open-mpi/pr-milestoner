#!/usr/bin/env python3

"""
The script applies a milestone based off the MAJOR.MINOR version of the base
branch, if a milestone is not already applied. This way, a human-applied
milestone gets priority.

"""

import re
import os
import sys

from github import Github

# ==============================================================================

GITHUB_BASE_REF = os.environ.get('GITHUB_BASE_REF')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
GITHUB_REPOSITORY = os.environ.get('GITHUB_REPOSITORY')
PR_NUM = os.environ.get('PR_NUM')

# Sanity check
if (GITHUB_BASE_REF is None or
    GITHUB_TOKEN is None or
    GITHUB_REPOSITORY is None or
    PR_NUM is None):
    print("Error: this script is designed to run as a Github Action")
    exit(1)

# ==============================================================================

# Given a pullRequest and repo object, the function checks if a milestone has
# already been applied to the PR. If it has, exit successfully. If it hasn't,
# apply the milestone based on the MAJOR.MINOR version of the base branch with
# the closest deadline.
def ensureMilestones(pullRequest, repo):
    if pullRequest.milestone is not None:
        print(f"Milestone {pullRequest.milestone.title} already applied")
        return None
    print("No milestone on the PR")
    targetVersion = re.search(r"v\d+\.\d+\.", GITHUB_BASE_REF)
    if targetVersion is None:
        print(f"No matching milestone for '{GITHUB_BASE_REF}'")
        return None
    targetVersion = targetVersion.group(0)
    for milestone in repo.get_milestones(state="open"):
        if milestone.title.startswith(targetVersion):
            print(f"Setting milestone to '{milestone.title}'")
            pullRequest.edit(milestone=milestone)
            break
    return None

# ==============================================================================

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_REPOSITORY)
prNum = int(PR_NUM)
issue = repo.get_issue(prNum)
ensureMilestones(issue, repo)
