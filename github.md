# Git & GitHub — Complete Tutorial for Your Internship

---

## 1. What is Git and Why Does It Matter?

Imagine you are working on the Fins'AIght document intelligence pipeline at Natixis. You spend two days building a new RAG feature, and it breaks everything. Without Git, your only options are to manually undo hours of work or lose everything and start over. With Git, you type one command and your code is back to exactly where it was before you started.

This is the most basic use case of Git, but it barely scratches the surface. Git is a **version control system** — a tool that tracks every change ever made to your code, who made it, when they made it, and why. Every change is recorded permanently. Nothing is ever truly lost.

In a professional environment like Natixis, Git is not optional. Every line of code that goes into production passes through Git. Every collaboration between team members happens through Git. Every code review, every bug fix, every new feature — all of it is managed through Git. Not knowing Git at an internship is like showing up to an office without knowing how to use email.

**Git vs GitHub — the distinction**

These two words are often confused but they are different things. Git is the software that runs on your computer and tracks changes locally. GitHub is a website that hosts Git repositories online, making it possible for teams to collaborate. Git is the engine. GitHub is the garage where you park and share your work.

Other platforms do the same thing as GitHub — GitLab and Bitbucket are popular alternatives used in enterprise environments. At Natixis, they likely use one of these. But the concepts are identical — only the interface changes.

---

## 2. Core Concepts You Must Understand

Before learning any commands, you need to understand the mental model. Git has a specific way of thinking about code history that is different from anything else.

**Repository**

A repository (repo) is a folder whose history is tracked by Git. It contains all your project files plus a hidden `.git` folder where Git stores the complete history of every change ever made. When you initialize Git in a folder or clone a project from GitHub, you create a repository.

**Commit**

A commit is a snapshot of your code at a specific moment in time. Think of it like a photograph of your entire codebase. Every commit has a unique identifier (a long string called a hash like `a3f92b1`), a timestamp, an author, and a message describing what changed. The entire history of a project is a sequence of commits — you can travel back to any commit and see exactly what the code looked like at that moment.

A commit is not a backup of changes — it is a snapshot of the entire state of the project. This distinction matters because it means you can always reconstruct any version of your project from any commit.

**Staging area**

Before a change becomes a commit, it must pass through the staging area. The staging area is a preparation zone where you select exactly which changes to include in your next commit. This is important because you might have changed ten files but only want to commit five of them. The staging area gives you this control.

The workflow is: make changes → stage the changes you want → commit the staged changes. Changes not in the staging area are not included in the commit.

**Branch**

A branch is an independent line of development. When you create a branch, you get a copy of the codebase that you can modify without affecting anything else. When your work is ready, you merge the branch back into the main codebase.

Branches are the foundation of collaborative development. They let multiple people work on different features simultaneously without stepping on each other's work. At Natixis, you will almost certainly be working on a dedicated feature branch for every task.

**The HEAD**

HEAD is a pointer that tells Git where you currently are in the repository history. Usually HEAD points to the latest commit on your current branch. When you switch branches, HEAD moves. When you make a commit, HEAD moves forward. Understanding HEAD is important for navigating through history.

---

## 3. The Three States of a File

Every file in a Git repository exists in one of three states. Understanding this is fundamental to understanding how Git works.

**Modified** means you have changed the file since the last commit but have not told Git about it yet. The change exists only on your disk. Git knows the file has changed because it compares the current state to the last commit, but it has not done anything with that information.

**Staged** means you have told Git that you want this change to be included in the next commit. The file has been added to the staging area. It is ready to be committed but has not been committed yet.

**Committed** means the change has been permanently recorded in the repository history as a snapshot. It is now part of the project history and will be there forever unless you explicitly rewrite history (an advanced operation you should avoid).

The practical workflow is: you edit files (modified state) → you run `git add` to stage them (staged state) → you run `git commit` to record them permanently (committed state).

---

## 4. Setting Up Git

```bash
# install Git
# Mac
brew install git

# Linux
sudo apt install git

# Windows — download from https://git-scm.com

# verify installation
git --version
```

The very first thing you must do after installing Git is configure your identity. Every commit you make will be tagged with your name and email. At Natixis, use your professional email.

```bash
# set your identity — do this once on every machine you use
git config --global user.name "Kempsly Silencieux"
git config --global user.email "kempsly@natixis.com"

# set default branch name to main (modern standard)
git config --global init.defaultBranch main

# set your preferred editor for commit messages
git config --global core.editor "code --wait"   # VS Code
# or
git config --global core.editor "nano"           # nano (simpler)

# verify your configuration
git config --list
```

---

## 5. Creating and Cloning Repositories

```bash
# ── Option 1 — start a new project locally ───────────────────
mkdir finsaight-pipeline
cd finsaight-pipeline
git init
# Git creates a hidden .git folder — your repository now exists

# ── Option 2 — clone an existing repository from GitHub ──────
# this is what you will do at Natixis on day 1
git clone https://github.com/natixis/finsaight-pipeline.git
cd finsaight-pipeline

# clone into a specific folder name
git clone https://github.com/natixis/finsaight-pipeline.git my-folder

# check the current state of your repository
git status
# shows: which branch you are on
#        which files are modified
#        which files are staged
#        which files are untracked
```

---

## 6. Your First Commit — The Daily Workflow

This is the sequence you will repeat dozens of times every day at your internship.

```bash
# step 1 — check what has changed
git status

# step 2 — see the actual content of changes
git diff                    # shows unstaged changes
git diff --staged           # shows staged changes (what will be committed)

# step 3 — stage your changes
git add filename.py         # stage one specific file
git add folder/             # stage an entire folder
git add .                   # stage ALL changed files in the current directory
                            # use carefully — you might stage files you didn't mean to

# step 4 — commit with a meaningful message
git commit -m "Add PDF parser agent with PyMuPDF and pdfplumber support"

# ── what makes a good commit message ─────────────────────────
# BAD:  "fix", "update", "changes", "wip"
# GOOD: "Fix ChromaDB dimension mismatch in RAG pipeline"
#       "Add XGBoost anomaly detection agent with SHAP explainability"
#       "Refactor document loader to support .msg Outlook format"
#
# rule: the message should complete the sentence "This commit will..."
# "This commit will Fix ChromaDB dimension mismatch" ✓
# "This commit will fix" ✗

# step 5 — view your commit history
git log                     # full history with author, date, message
git log --oneline           # compact one-line per commit
git log --oneline --graph   # visual branch graph
git log --oneline -10       # last 10 commits only
```

---

## 7. Branches — The Most Important Concept for Teams

At your internship, you will almost never work directly on the `main` branch. Every new feature, every bug fix, every experiment gets its own branch. This protects the main codebase and makes collaboration possible.

```bash
# ── See all branches ──────────────────────────────────────────
git branch                  # local branches (* = current branch)
git branch -a               # all branches including remote

# ── Create a new branch ───────────────────────────────────────
git branch feature/pdf-parser      # creates branch but stays on current
git checkout -b feature/pdf-parser # creates AND switches to new branch
git switch -c feature/pdf-parser   # modern syntax (Git 2.23+)

# naming conventions used in professional teams:
# feature/description   → new feature
# fix/description       → bug fix
# hotfix/description    → urgent production fix
# chore/description     → maintenance (dependencies, configs)
# refactor/description  → code restructuring

# ── Switch between branches ───────────────────────────────────
git checkout main               # old syntax
git switch main                 # modern syntax

# ── Delete a branch ───────────────────────────────────────────
git branch -d feature/pdf-parser      # safe delete (only if merged)
git branch -D feature/pdf-parser      # force delete (even if not merged)

# ── See what branch you are on ───────────────────────────────
git status                      # first line always shows current branch
```

---

## 8. Merging Branches

When your feature is complete, you merge your branch back into `main`. There are two types of merges you need to understand.

```bash
# ── Standard merge ────────────────────────────────────────────
# scenario: you finished feature/pdf-parser and want to merge into main

git switch main                          # first go to the target branch
git merge feature/pdf-parser            # merge your feature branch in
git branch -d feature/pdf-parser        # clean up — delete the branch

# Git creates a "merge commit" that combines both histories
# this preserves the full history of when the branch was created

# ── Merge conflicts ───────────────────────────────────────────
# a conflict happens when two branches changed the same line of the same file
# Git does not know which version to keep — it asks you to decide

# after a conflicting merge Git marks the files like this:
# <<<<<<< HEAD
# your version of the code
# =======
# the other branch's version
# >>>>>>> feature/pdf-parser

# to resolve:
# 1. open the conflicting files
# 2. manually edit them to keep what you want
# 3. remove the conflict markers (<<<, ===, >>>)
# 4. stage the resolved files
# 5. complete the merge

git add resolved_file.py
git commit -m "Merge feature/pdf-parser — resolve conflict in loader.py"

# ── Check for conflicts before merging ───────────────────────
git diff main...feature/pdf-parser     # see all differences between branches
```

---

## 9. Working with Remote Repositories (GitHub)

A remote repository is the version of your project hosted on GitHub or GitLab. The standard remote is named `origin` by convention.

```bash
# ── Connect local repo to GitHub ─────────────────────────────
git remote add origin https://github.com/username/repo.git
git remote -v                           # verify the connection

# ── Push your commits to GitHub ──────────────────────────────
git push origin main                    # push main branch
git push origin feature/pdf-parser     # push a feature branch

# first time pushing a new branch — set upstream tracking
git push -u origin feature/pdf-parser
# after this you can just type git push (no need to specify branch)

# ── Pull changes from GitHub ─────────────────────────────────
# your teammate pushed changes — you need to get them
git pull origin main                    # fetch + merge in one step
git pull                                # shorthand if upstream is set

# ── Fetch vs Pull ────────────────────────────────────────────
git fetch origin                        # download changes but don't apply them
                                        # lets you inspect before merging
git merge origin/main                   # then merge manually

# git pull = git fetch + git merge
# use git fetch when you want to review changes before applying them
# use git pull when you trust the changes and want them immediately
```

---

## 10. Pull Requests — How Professional Teams Review Code

A Pull Request (PR) is a formal request to merge your branch into main. It is the central workflow of professional software development. At Natixis, every change to the codebase will go through a Pull Request reviewed by a senior team member before it is merged.

**The Pull Request workflow**

You create a branch for your task, do your work, push the branch to GitHub, and then open a Pull Request from your branch into main. The PR shows all the changes you made — every line added or removed. Your teammates review the code, leave comments, ask questions, and request changes. You address the feedback, push additional commits to the same branch, and eventually a senior team member approves and merges the PR.

This process serves multiple purposes. It ensures code quality — a second pair of eyes almost always catches bugs and design issues. It spreads knowledge — reviewers learn what you built and you learn from their feedback. It creates documentation — the PR description and comments become a permanent record of why certain decisions were made.

```bash
# ── Standard PR workflow ──────────────────────────────────────

# 1. create your branch
git switch -c feature/rag-hybrid-search

# 2. do your work and commit regularly
git add .
git commit -m "Add BM25 retriever for keyword search"
git add .
git commit -m "Add FAISS semantic retriever"
git add .
git commit -m "Combine BM25 and FAISS in EnsembleRetriever"

# 3. push to GitHub
git push -u origin feature/rag-hybrid-search

# 4. go to GitHub and open a Pull Request
# → click "Compare & pull request"
# → write a clear description:
#   - what does this PR do?
#   - why was this change needed?
#   - how was it tested?
#   - any known issues or limitations?

# 5. address review comments
# your reviewer leaves a comment: "please add type hints to the search function"
# you make the change locally
git add search_service.py
git commit -m "Add type hints to hybrid search function per review"
git push      # this automatically updates the open PR

# 6. after approval — the reviewer merges the PR on GitHub

# 7. update your local main branch
git switch main
git pull
git branch -d feature/rag-hybrid-search    # clean up local branch
```

---

## 11. The `.gitignore` File

The `.gitignore` file tells Git which files and folders to never track. This is critical — you must never commit API keys, passwords, large data files, or generated files to a repository.

```bash
# create .gitignore in the root of your project
touch .gitignore
```

```
# .gitignore — standard template for a data science / ML project

# ── Environment and secrets ───────────────────────────────────
.env                        # API keys — NEVER commit this
.env.local
.env.production
*.key
secrets.json

# ── Python ────────────────────────────────────────────────────
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
.eggs/

# ── Virtual environments ──────────────────────────────────────
venv/
.venv/
env/
.conda/

# ── Jupyter Notebooks ────────────────────────────────────────
.ipynb_checkpoints/

# ── Data files (usually too large for Git) ───────────────────
*.csv
*.xlsx
*.parquet
*.pkl
*.h5
data/raw/
data/processed/

# ── ML Models (use MLflow or S3 instead) ─────────────────────
*.ubj
*.joblib
models/

# ── OS files ──────────────────────────────────────────────────
.DS_Store           # Mac
Thumbs.db           # Windows
*.swp               # Vim

# ── IDE files ────────────────────────────────────────────────
.vscode/settings.json
.idea/

# ── Logs and outputs ─────────────────────────────────────────
*.log
logs/
outputs/
```

---

## 12. Undoing Things — The Most Important Commands to Know

```bash
# ── Undo unstaged changes (dangerous — cannot be undone) ─────
git checkout -- filename.py     # old syntax
git restore filename.py         # modern syntax
# WARNING: this permanently discards your unsaved changes

# ── Unstage a file (safe — does not delete changes) ──────────
git restore --staged filename.py
# the changes are still there, they are just removed from staging

# ── Amend the last commit ─────────────────────────────────────
# you just committed but forgot to include a file or made a typo in the message
git add forgotten_file.py
git commit --amend -m "Corrected commit message"
# ONLY do this if you have NOT pushed yet — rewriting pushed history causes problems

# ── Undo the last commit but keep the changes ────────────────
git reset --soft HEAD~1
# commits are undone, changes go back to staging area
# useful when you committed too early

# ── Undo the last commit and unstage changes ─────────────────
git reset HEAD~1
# or
git reset --mixed HEAD~1
# commits are undone, changes go back to working directory (unstaged)

# ── Nuclear option — undo commit AND discard changes ─────────
git reset --hard HEAD~1
# WARNING: permanently deletes both the commit and the changes
# only use when you are absolutely sure you want to lose the work

# ── Safely undo a commit that has already been pushed ─────────
git revert HEAD
# creates a NEW commit that undoes the previous commit
# does not rewrite history — safe to use on shared branches
# this is the correct way to undo a pushed commit

# ── Go back to a specific commit to inspect ──────────────────
git checkout a3f92b1            # detached HEAD state — read only
git switch -                    # go back to where you were
```

---

## 13. Stashing — Saving Work Without Committing

```bash
# scenario: you are in the middle of a feature when your team lead asks you
# to urgently fix a bug on the main branch
# your work is not ready to commit but you need to switch branches

# ── Save your work in progress temporarily ───────────────────
git stash                       # stash all modified tracked files
git stash push -m "WIP: hybrid search retriever"   # with a description

# ── Switch to fix the bug ─────────────────────────────────────
git switch main
git switch -c fix/chromadb-version-conflict
# fix the bug, commit, push, PR

# ── Come back to your work ────────────────────────────────────
git switch feature/rag-hybrid-search
git stash pop                   # apply the most recent stash and remove it
git stash apply                 # apply but keep it in the stash list

# ── Manage multiple stashes ───────────────────────────────────
git stash list                  # see all stashes
git stash pop stash@{2}         # apply a specific stash
git stash drop stash@{0}        # delete a specific stash
git stash clear                 # delete all stashes
```

---

## 14. Rebasing — Keeping a Clean History

```bash
# rebase is an alternative to merge for integrating changes
# instead of creating a merge commit, rebase replays your commits
# on top of the latest main branch

# scenario: you created a branch 3 days ago
# since then, 10 new commits were added to main by your teammates
# your branch is now "behind" main

# ── Option A — merge main into your branch (creates merge commit) ──
git switch feature/pdf-parser
git merge main
# creates a merge commit — history shows a branch and merge

# ── Option B — rebase your branch onto main (cleaner history) ──
git switch feature/pdf-parser
git rebase main
# Git takes your commits, temporarily removes them,
# fast-forwards your branch to the latest main,
# then replays your commits on top one by one
# result: your branch looks like it was created from the latest main
# history is perfectly linear — easier to read and debug

# ── Interactive rebase — clean up your commits before a PR ───
git rebase -i HEAD~4    # interactively edit the last 4 commits
# opens an editor where you can:
# pick   → keep the commit as-is
# squash → combine this commit with the previous one
# reword → change the commit message
# drop   → delete the commit entirely

# GOLDEN RULE: never rebase branches that have been pushed and shared
# rebasing rewrites history — if others have your branch, it breaks their copies
# only rebase your own local branches that no one else has
```

---

## 15. Tags — Marking Important Versions

```bash
# tags mark specific commits as important — usually version releases
# at Natixis, tags might mark when a model version was deployed to production

# ── Create a tag ─────────────────────────────────────────────
git tag v1.0.0                              # lightweight tag
git tag -a v1.0.0 -m "First production deployment — anomaly detection agent"
# -a = annotated tag (has message, author, date — preferred)

# ── Tag a specific past commit ────────────────────────────────
git tag -a v0.9.0 a3f92b1 -m "Pre-release version"

# ── Push tags to GitHub ───────────────────────────────────────
git push origin v1.0.0          # push a specific tag
git push origin --tags          # push all tags

# ── List and checkout tags ───────────────────────────────────
git tag                         # list all tags
git show v1.0.0                 # show tag details
git checkout v1.0.0             # go to the state of the code at that tag
```

---

## 16. Professional Git Workflow at an Internship

This is the complete workflow you will follow at Natixis from day one.

**Trunk-based development**

Most professional teams use trunk-based development or Gitflow. In trunk-based development, everyone works on short-lived feature branches (1-3 days maximum) that are merged into main frequently. This keeps the main branch always deployable and avoids long-running branches that diverge far from the main codebase.

**The daily routine**

Every morning you start by pulling the latest changes from main into your branch. This keeps your branch up to date with your teammates' work and reduces merge conflicts.

```bash
# morning routine — every single day
git switch main
git pull                        # get latest changes from teammates
git switch feature/your-feature
git rebase main                 # bring your branch up to date
```

Every evening before you leave you push your current work to GitHub, even if it is not finished. This backs up your work and lets teammates see your progress.

```bash
# evening routine — every single day
git add .
git commit -m "WIP: implement hybrid search — BM25 complete, FAISS in progress"
git push
```

**Commit frequency**

At an internship, commit often. A common mistake is working for 8 hours and making one massive commit at the end. Instead, commit every time you complete a logical unit of work — every function, every bug fix, every test added. Small commits are easier to review, easier to understand, and easier to revert if something goes wrong.

**Branch naming at Natixis**

Follow whatever convention your team uses. If you are not given a convention, use: `feature/TICKET-ID-short-description`. For example: `feature/FINS-42-pdf-parser-agent`. Including the ticket ID links your code to the task management system.

---

## 17. GitHub Features You Will Use Daily

**Issues**

Issues are the task management system built into GitHub. Every bug, feature request, and improvement is tracked as an issue. When you start work on an issue, you create a branch and reference the issue number in your commits and PR.

```bash
# reference an issue in a commit message
git commit -m "Fix ChromaDB dimension mismatch — closes #42"
# GitHub automatically closes issue #42 when this PR is merged
```

**GitHub Actions — CI/CD**

GitHub Actions is an automation system that runs automatically when you push code or open a PR. At Natixis, there will almost certainly be automated checks that run on every PR — tests, code linting, security scanning. You will see a green checkmark or red X on your PR indicating whether your code passed all checks.

If the checks fail, you must fix the issues before your PR can be merged. Common failure causes are failing tests, code style violations (PEP8 for Python), or security vulnerabilities in dependencies.

**GitHub Codespaces and Dev Containers**

Many enterprise teams provide a standardized development environment through Dev Containers or GitHub Codespaces. This ensures everyone uses the same Python version, the same libraries, and the same tools. If Natixis provides one, use it — it eliminates "works on my machine" problems.

---

## 18. Git Best Practices for Your Internship

**Never commit secrets**

This cannot be overstated. API keys, database passwords, and credentials must never appear in any commit. If you accidentally commit a secret, you must immediately rotate (regenerate) the credential — even after you delete it from the repository, it is permanently in the commit history and could be found by anyone with access to the repo.

Use a `.env` file for all secrets and ensure `.env` is in your `.gitignore` before you make your first commit.

**Write meaningful commit messages**

Your commit history is your professional record. At the end of your internship, your team lead can look at your commit history and understand exactly what you worked on, how you approached problems, and how your thinking evolved. Generic messages like "fix" or "update" tell nothing. Specific messages like "Fix XGBoost SHAP incompatibility by switching to predict_proba callable" tell a professional story.

**Keep PRs small and focused**

A PR that changes 50 files across 10 different features is nearly impossible to review properly. A PR that changes 5 files to add one specific capability can be reviewed in 15 minutes. Smaller PRs get merged faster, get better reviews, and are easier to revert if something goes wrong. If your task is large, split it into multiple sequential PRs.

**Always pull before pushing**

Before pushing your work, always pull the latest changes from main. If you push without pulling, you might create unnecessary conflicts or push code that is incompatible with recent changes from teammates.

**Use `git status` constantly**

Running `git status` before and after every Git operation costs you nothing and prevents many mistakes. Make it a habit. It tells you exactly what state your repository is in at every moment.

---

## 19. Cheat Sheet — Commands You Will Use Every Day

```bash
# ── Setup (once per machine) ──────────────────────────────────
git config --global user.name "Your Name"
git config --global user.email "you@natixis.com"

# ── Start working ─────────────────────────────────────────────
git clone <url>                 # get a repo from GitHub
git init                        # create a new repo locally
git status                      # always know where you are

# ── Daily workflow ────────────────────────────────────────────
git pull                        # get latest changes
git switch -c feature/name      # create and switch to new branch
git add .                       # stage all changes
git add filename                # stage specific file
git commit -m "message"         # commit staged changes
git push                        # push to GitHub

# ── Branching ────────────────────────────────────────────────
git branch                      # list branches
git switch branch-name          # switch to branch
git switch -c new-branch        # create and switch
git branch -d branch-name       # delete branch (safe)
git merge branch-name           # merge branch into current

# ── History ───────────────────────────────────────────────────
git log --oneline               # compact history
git log --oneline --graph       # visual branch graph
git diff                        # see unstaged changes
git diff --staged               # see staged changes

# ── Undoing things ────────────────────────────────────────────
git restore filename            # discard unstaged changes
git restore --staged filename   # unstage a file
git commit --amend              # fix last commit (before push only)
git revert HEAD                 # safely undo pushed commit
git stash                       # save work in progress
git stash pop                   # restore saved work

# ── Remote ───────────────────────────────────────────────────
git remote -v                   # see remote connections
git fetch                       # download changes without applying
git pull                        # fetch + merge
git push -u origin branch-name # push branch for first time
git push                        # push subsequent times

# ── Inspection ───────────────────────────────────────────────
git show commit-hash            # see details of a specific commit
git blame filename              # see who last changed each line
git grep "search term"          # search through all tracked files
```

---

## 20. First Week Checklist at Natixis

By the end of your first week, you should have done all of the following.

You should have configured Git with your Natixis email and verified the configuration. You should have cloned the Fins'AIght repository and explored its branch structure and commit history. You should have created your first feature branch following the team's naming convention. You should have made at least one commit with a meaningful message. You should have pushed a branch and opened your first Pull Request, even if it is just adding your name to a contributor file. You should have confirmed that your `.env` file is in `.gitignore` before adding any API keys to it. You should have asked your team lead what branching workflow they use — Gitflow, trunk-based, or something else — and followed it from day one.

The goal in the first week is not to be perfect. It is to establish good habits. The engineers who progress fastest at internships are not necessarily the most technically brilliant — they are the ones who ask good questions, write clean code, and make their work easy for others to review and understand. Git is the primary tool through which that professionalism is expressed.
