# GitHub Actions & CI/CD — Complete In-Depth Tutorial
> **The most comprehensive GitHub Actions and CI/CD reference** — every concept, every YAML field, and deployment pipelines for every major platform  
> Written for data scientists and ML engineers building production-grade CI/CD systems

---

## Table of Contents

### Part 1 — Fundamentals
1. [What is CI/CD and Why it Matters](#1-what-is-cicd-and-why-it-matters)
2. [What is GitHub Actions](#2-what-is-github-actions)
3. [Core Concepts](#3-core-concepts)
4. [Workflow YAML — Every Field Explained](#4-workflow-yaml--every-field-explained)
5. [Triggers — on: — Complete Reference](#5-triggers--on--complete-reference)
6. [Jobs — Complete Reference](#6-jobs--complete-reference)
7. [Steps — Complete Reference](#7-steps--complete-reference)
8. [Expressions and Contexts](#8-expressions-and-contexts)
9. [Environment Variables and Secrets](#9-environment-variables-and-secrets)

### Part 2 — Core Workflows
10. [Python CI Pipeline](#10-python-ci-pipeline)
11. [Testing — Unit, Integration, Coverage](#11-testing--unit-integration-coverage)
12. [Code Quality — Linting and Formatting](#12-code-quality--linting-and-formatting)
13. [Docker Build and Push](#13-docker-build-and-push)
14. [Matrix Builds](#14-matrix-builds)
15. [Caching Dependencies](#15-caching-dependencies)
16. [Artifacts — Saving Build Outputs](#16-artifacts--saving-build-outputs)
17. [Reusable Workflows](#17-reusable-workflows)
18. [Composite Actions](#18-composite-actions)

### Part 3 — ML/AI Specific Pipelines
19. [ML Model Training Pipeline](#19-ml-model-training-pipeline)
20. [Model Evaluation and Registry](#20-model-evaluation-and-registry)
21. [MLflow Integration](#21-mlflow-integration)
22. [Jupyter Notebook CI](#22-jupyter-notebook-ci)

### Part 4 — CD to Every Platform
23. [Deploy to AWS ECS](#23-deploy-to-aws-ecs)
24. [Deploy to AWS EKS (Kubernetes)](#24-deploy-to-aws-eks-kubernetes)
25. [Deploy to AWS Lambda (Serverless)](#25-deploy-to-aws-lambda-serverless)
26. [Deploy to Google Cloud Run](#26-deploy-to-google-cloud-run)
27. [Deploy to Google GKE](#27-deploy-to-google-gke)
28. [Deploy to Azure Container Apps](#28-deploy-to-azure-container-apps)
29. [Deploy to Azure AKS](#29-deploy-to-azure-aks)
30. [Deploy to DigitalOcean App Platform](#30-deploy-to-digitalocean-app-platform)
31. [Deploy to Heroku](#31-deploy-to-heroku)
32. [Deploy to Railway](#32-deploy-to-railway)
33. [Deploy to Kubernetes (Generic)](#33-deploy-to-kubernetes-generic)
34. [Deploy with Docker Compose (VPS/Self-hosted)](#34-deploy-with-docker-compose-vpsself-hosted)

### Part 5 — Advanced Topics
35. [Environments and Approval Gates](#35-environments-and-approval-gates)
36. [Self-Hosted Runners](#36-self-hosted-runners)
37. [GitHub Actions Security](#37-github-actions-security)
38. [Workflow Optimization and Performance](#38-workflow-optimization-and-performance)
39. [Notifications and Reporting](#39-notifications-and-reporting)
40. [Complete Production Pipeline](#40-complete-production-pipeline)
41. [Cheat Sheet](#41-cheat-sheet)

---

# PART 1 — FUNDAMENTALS

---

## 1. What is CI/CD and Why it Matters

### Continuous Integration (CI)

Continuous Integration is the practice of automatically building and testing your code every time a developer pushes a change. The goal is to catch bugs as early as possible — before they reach production.

Without CI, a team of 5 developers might work independently for a week, then try to merge everything at once. The merge causes conflicts, hidden bugs surface, and the team spends two days fixing integration problems. This is called "integration hell."

With CI, every push automatically:
- Runs all tests
- Checks code style
- Builds the Docker image
- Reports the result immediately

If anything breaks, the developer who caused it knows within minutes, while the context is still fresh.

### Continuous Delivery (CD)

Continuous Delivery extends CI by automatically deploying code that passes all tests to a staging environment. A human then decides whether to deploy to production.

### Continuous Deployment

Continuous Deployment goes one step further — every change that passes all tests is automatically deployed to production without human intervention. This requires very high test coverage and confidence.

### Why CI/CD Matters for ML Projects

ML projects benefit especially from CI/CD because:
- Model code changes frequently as experiments progress
- Data pipelines are complex and prone to silent failures
- Model performance must be tracked across versions
- Multiple environments (dev, staging, production) use different data
- Rollbacks must be fast when a new model degrades

A good ML CI/CD pipeline automatically:
- Tests all Python code and data transformations
- Trains models on schedule or on code changes
- Evaluates model metrics against thresholds
- Builds and pushes Docker images for serving
- Deploys to staging for validation
- Promotes to production after approval

---

## 2. What is GitHub Actions

GitHub Actions is GitHub's built-in CI/CD platform. It is event-driven — you define workflows that run automatically in response to events (push, pull request, schedule, manual trigger, etc.).

### Key Advantages

**Integrated with GitHub** — no separate CI server to configure. Everything lives in your repository.

**Free tier** — 2,000 minutes per month for public repos (unlimited), 2,000 minutes for private repos on the free plan.

**Marketplace** — over 20,000 pre-built actions for common tasks (deploy to AWS, send Slack messages, run tests, etc.)

**Matrix builds** — test across multiple Python versions, operating systems, or configurations in parallel.

**Self-hosted runners** — run workflows on your own servers (important for GPU training, large datasets, or private networks).

### How it Works

```
GitHub Event (push, PR, schedule)
         │
         ▼
   Workflow triggered
   (.github/workflows/ci.yml)
         │
         ▼
   Jobs run (in parallel or sequential)
   ┌─────────────┬─────────────┬─────────────┐
   │   test      │    lint     │    build    │
   └─────────────┴─────────────┴─────────────┘
         │
         ▼ (if all jobs pass)
   Deploy job runs
         │
         ▼
   Application deployed
```

### Workflow File Location

All workflow files live in `.github/workflows/` in your repository:

```
your-repo/
├── .github/
│   └── workflows/
│       ├── ci.yml           ← main CI pipeline
│       ├── cd.yml           ← deployment pipeline
│       ├── train-model.yml  ← ML training pipeline
│       └── nightly.yml      ← scheduled jobs
├── src/
├── tests/
└── Dockerfile
```

---

## 3. Core Concepts

### Workflow

A workflow is an automated process defined in a YAML file. A repository can have multiple workflows. Each workflow:
- Is triggered by one or more events
- Contains one or more jobs
- Runs on GitHub-hosted or self-hosted runners

### Event

An event is something that triggers a workflow. Common events:
- `push` — code is pushed to a branch
- `pull_request` — a PR is opened or updated
- `schedule` — a cron schedule
- `workflow_dispatch` — manual trigger from the GitHub UI
- `release` — a release is published

### Job

A job is a set of steps that run sequentially on the same runner. Jobs in a workflow run in parallel by default, but can be configured to run sequentially using `needs`.

### Step

A step is an individual task within a job. Steps run sequentially within a job. Each step either:
- Runs a shell command (`run: echo "hello"`)
- Uses an Action (`uses: actions/checkout@v4`)

### Action

An action is a reusable unit of code that performs a specific task. Actions can be:
- Official GitHub actions (`actions/checkout`, `actions/setup-python`)
- Community actions from the Marketplace
- Your own custom actions

### Runner

A runner is a server that executes the workflow. GitHub provides hosted runners:
- `ubuntu-latest` (most common, recommended)
- `windows-latest`
- `macos-latest`

You can also use self-hosted runners on your own infrastructure.

---

## 4. Workflow YAML — Every Field Explained

```yaml
# .github/workflows/complete-reference.yml

# ── Workflow name (shown in GitHub UI) ────────────────────────
name: Complete CI/CD Pipeline

# ── Run name (can use expressions for dynamic names) ──────────
run-name: "CI/CD triggered by ${{ github.actor }} on ${{ github.ref_name }}"

# ── Triggers ──────────────────────────────────────────────────
# covered in detail in Section 5
on:
  push:
    branches: [main, develop]

# ── Permissions ───────────────────────────────────────────────
# default permissions for all jobs in this workflow
# principle of least privilege — only grant what's needed
permissions:
  contents: read          # read repository contents
  packages: write         # push to GitHub Container Registry
  id-token: write         # for OIDC authentication (AWS, GCP, Azure)
  pull-requests: write    # comment on pull requests
  issues: write           # create/update issues
  deployments: write      # create deployments
  checks: write           # create check runs
  security-events: write  # upload SARIF security results

# ── Environment variables for all jobs ────────────────────────
env:
  PYTHON_VERSION: "3.10"
  NODE_VERSION: "18"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

# ── Default settings for all run steps ────────────────────────
defaults:
  run:
    shell: bash           # default shell
    working-directory: .  # default working directory

# ── Concurrency — prevent duplicate runs ──────────────────────
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
  # cancels any in-progress run of the same workflow on the same branch
  # prevents queue buildup from rapid pushes

# ── Jobs definition ───────────────────────────────────────────
jobs:
  my-job:
    name: My Job Name          # human-readable name in GitHub UI
    runs-on: ubuntu-latest     # runner type

    # environment for deployment jobs
    environment:
      name: production
      url: https://app.example.com

    # condition — only run if this is true
    if: github.ref == 'refs/heads/main'

    # job-level environment variables
    env:
      JOB_VAR: "job-level-value"

    # job-level permissions (overrides workflow-level)
    permissions:
      contents: read

    # time limit for the entire job
    timeout-minutes: 60

    # continue even if this job fails
    continue-on-error: false

    # depend on another job — runs after that job completes
    needs: [test, lint]

    # output values to other jobs
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}

    # matrix strategy (Section 14)
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
      - name: Step name       # optional but recommended
        id: my-step           # ID for referencing outputs later

        # run a shell command
        run: echo "Hello World"

        # multi-line command
        run: |
          echo "Line 1"
          echo "Line 2"
          python -m pytest tests/

        # use an action
        uses: actions/checkout@v4

        # with action inputs
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

        # step-level environment variables
        env:
          MY_SECRET: ${{ secrets.MY_SECRET }}

        # step-level condition
        if: success()

        # step-level timeout
        timeout-minutes: 10

        # continue if this step fails
        continue-on-error: false

        # working directory for this step
        working-directory: ./backend
```

---

## 5. Triggers — on: — Complete Reference

```yaml
on:

  # ── Push trigger ──────────────────────────────────────────────
  push:
    branches:
      - main
      - develop
      - "release/**"          # wildcard — all release/* branches
      - "!hotfix/**"          # exclude hotfix/* branches
    branches-ignore:
      - "dependabot/**"       # ignore dependabot branches
    tags:
      - "v*"                  # trigger on version tags
      - "v[0-9]+.[0-9]+.[0-9]+"
    tags-ignore:
      - "v*-beta"
    paths:
      - "src/**"              # only trigger if files in src/ changed
      - "requirements.txt"
      - "Dockerfile"
    paths-ignore:
      - "docs/**"             # don't trigger for docs changes
      - "*.md"
      - ".gitignore"

  # ── Pull request trigger ──────────────────────────────────────
  pull_request:
    branches: [main, develop]
    types:
      - opened             # PR opened
      - synchronize        # new commit pushed to PR
      - reopened           # PR reopened
      - ready_for_review   # PR marked ready (removed draft status)
      - labeled            # label added
      - unlabeled          # label removed
    paths:
      - "src/**"
      - "tests/**"

  # ── Pull request review trigger ───────────────────────────────
  pull_request_review:
    types: [submitted, dismissed]

  # ── Manual trigger ────────────────────────────────────────────
  workflow_dispatch:
    inputs:
      environment:
        description: "Target environment"
        required: true
        default: "staging"
        type: choice
        options:
          - staging
          - production
      version:
        description: "Version to deploy"
        required: false
        type: string
      debug:
        description: "Enable debug mode"
        required: false
        type: boolean
        default: false
      notify:
        description: "Notify on Slack"
        type: boolean
        default: true

  # ── Scheduled trigger (cron) ──────────────────────────────────
  schedule:
    # minute hour day-of-month month day-of-week
    - cron: "0 2 * * *"         # every day at 2am UTC
    - cron: "0 */6 * * *"       # every 6 hours
    - cron: "30 5 * * 1"        # every Monday at 5:30am
    - cron: "0 0 1 * *"         # first day of every month

  # ── Release trigger ───────────────────────────────────────────
  release:
    types:
      - published              # release published (not draft)
      - created
      - released
      - prereleased

  # ── Issue trigger ─────────────────────────────────────────────
  issues:
    types: [opened, closed, labeled]

  # ── Repository dispatch (external trigger via API) ────────────
  repository_dispatch:
    types: [deploy-command, train-model]

  # ── Another workflow completes ────────────────────────────────
  workflow_run:
    workflows: ["CI Pipeline"]
    types: [completed]
    branches: [main]

  # ── Merge queue ───────────────────────────────────────────────
  merge_group:
    types: [checks_requested]
```

---

## 6. Jobs — Complete Reference

```yaml
jobs:

  # ── Basic job ─────────────────────────────────────────────────
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "testing"

  # ── Job with dependencies ─────────────────────────────────────
  build:
    needs: [test]            # run after test completes successfully
    runs-on: ubuntu-latest
    steps:
      - run: echo "building"

  deploy-staging:
    needs: [build]
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploy staging"

  deploy-production:
    needs: [deploy-staging]  # sequential chain
    runs-on: ubuntu-latest
    steps:
      - run: echo "deploy production"

  # ── Job that always runs (cleanup, notifications) ─────────────
  notify:
    needs: [test, build]     # wait for both
    runs-on: ubuntu-latest
    if: always()             # run even if previous jobs failed
    steps:
      - run: echo "Sending notification"

  # ── Job with outputs ──────────────────────────────────────────
  build-image:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.tag.outputs.tag }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - id: tag
        run: echo "tag=$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
      - id: build
        run: echo "digest=sha256:abc123" >> $GITHUB_OUTPUT

  deploy:
    needs: [build-image]
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying ${{ needs.build-image.outputs.image-tag }}"

  # ── Different runner types ────────────────────────────────────
  test-linux:
    runs-on: ubuntu-latest

  test-ubuntu-specific:
    runs-on: ubuntu-22.04    # pin to specific Ubuntu version

  test-windows:
    runs-on: windows-latest

  test-mac:
    runs-on: macos-latest

  test-mac-arm:
    runs-on: macos-14        # Apple Silicon

  test-self-hosted:
    runs-on: [self-hosted, linux, x64]
    # runs on your own runner with these labels

  test-gpu:
    runs-on: [self-hosted, gpu, cuda]
    # runs on your GPU server

  # ── Services — sidecar containers ────────────────────────────
  test-with-db:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s

    steps:
      - run: |
          psql -h localhost -U test -d testdb -c "SELECT 1"
        env:
          PGPASSWORD: test

  # ── Container job — run job inside a container ────────────────
  test-in-container:
    runs-on: ubuntu-latest
    container:
      image: python:3.10-slim
      credentials:
        username: ${{ secrets.REGISTRY_USER }}
        password: ${{ secrets.REGISTRY_TOKEN }}
      env:
        INSIDE_CONTAINER: "true"
      volumes:
        - /data:/data
      options: --cpus 2
    steps:
      - run: python --version   # runs inside python:3.10-slim
```

---

## 7. Steps — Complete Reference

```yaml
steps:

  # ── Checkout repository ───────────────────────────────────────
  - name: Checkout code
    uses: actions/checkout@v4
    with:
      ref: ${{ github.sha }}      # specific commit
      fetch-depth: 0              # full history (needed for tags)
      token: ${{ secrets.GITHUB_TOKEN }}
      submodules: recursive       # include git submodules

  # ── Setup Python ──────────────────────────────────────────────
  - name: Set up Python
    uses: actions/setup-python@v5
    with:
      python-version: "3.10"
      python-version-file: ".python-version"   # read from file
      cache: "pip"                              # cache pip packages
      cache-dependency-path: "requirements.txt"

  # ── Setup Node.js ─────────────────────────────────────────────
  - name: Set up Node.js
    uses: actions/setup-node@v4
    with:
      node-version: "18"
      cache: "npm"

  # ── Cache ─────────────────────────────────────────────────────
  - name: Cache pip packages
    uses: actions/cache@v4
    with:
      path: ~/.cache/pip
      key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      restore-keys: |
        ${{ runner.os }}-pip-

  # ── Upload artifact ───────────────────────────────────────────
  - name: Upload test results
    uses: actions/upload-artifact@v4
    with:
      name: test-results
      path: reports/
      retention-days: 30
      if-no-files-found: error    # error | warn | ignore

  # ── Download artifact ─────────────────────────────────────────
  - name: Download model artifact
    uses: actions/download-artifact@v4
    with:
      name: trained-model
      path: models/

  # ── Set output variable ───────────────────────────────────────
  - name: Set version
    id: version
    run: |
      VERSION=$(python -c "import src; print(src.__version__)")
      echo "version=$VERSION" >> $GITHUB_OUTPUT
      echo "Version is $VERSION"

  # ── Use output from previous step ─────────────────────────────
  - name: Use version
    run: echo "Deploying version ${{ steps.version.outputs.version }}"

  # ── Conditional step ──────────────────────────────────────────
  - name: Deploy to production
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    run: ./deploy.sh production

  - name: Only on failure
    if: failure()
    run: echo "Something failed"

  - name: Only on success
    if: success()
    run: echo "Everything passed"

  - name: Always run
    if: always()
    run: echo "This always runs"

  - name: On specific event type
    if: github.event_name == 'workflow_dispatch' && inputs.debug == 'true'
    run: echo "Debug mode enabled"

  # ── Multi-line shell script ───────────────────────────────────
  - name: Run tests
    run: |
      set -e                    # exit on any error
      set -o pipefail           # pipes fail if any command fails
      echo "Installing dependencies..."
      pip install -r requirements.txt
      echo "Running tests..."
      python -m pytest tests/ -v --tb=short
      echo "Tests passed!"

  # ── Step with environment variables ──────────────────────────
  - name: Deploy
    run: ./deploy.sh
    env:
      API_KEY: ${{ secrets.API_KEY }}
      ENVIRONMENT: production
      DATABASE_URL: ${{ secrets.DATABASE_URL }}

  # ── Working directory ─────────────────────────────────────────
  - name: Build frontend
    working-directory: ./frontend
    run: npm run build

  # ── Using GitHub Script (JavaScript in workflows) ─────────────
  - name: Comment on PR
    uses: actions/github-script@v7
    with:
      script: |
        github.rest.issues.createComment({
          issue_number: context.issue.number,
          owner: context.repo.owner,
          repo: context.repo.repo,
          body: '✅ Tests passed! Ready for review.'
        })

  # ── Write to GitHub Summary ───────────────────────────────────
  - name: Write summary
    run: |
      echo "## Test Results 🧪" >> $GITHUB_STEP_SUMMARY
      echo "" >> $GITHUB_STEP_SUMMARY
      echo "| Test | Status |" >> $GITHUB_STEP_SUMMARY
      echo "|------|--------|" >> $GITHUB_STEP_SUMMARY
      echo "| Unit Tests | ✅ Pass |" >> $GITHUB_STEP_SUMMARY
      echo "| Integration | ✅ Pass |" >> $GITHUB_STEP_SUMMARY

  # ── Add to PATH ───────────────────────────────────────────────
  - name: Add to PATH
    run: echo "/custom/bin" >> $GITHUB_PATH

  # ── Set environment variable for subsequent steps ─────────────
  - name: Set env var
    run: echo "MY_VAR=hello" >> $GITHUB_ENV

  - name: Use env var
    run: echo $MY_VAR    # outputs: hello
```

---

## 8. Expressions and Contexts

### Contexts

Contexts are objects containing information about the workflow run.

```yaml
# github context — information about the event and repository
${{ github.sha }}              # full commit SHA
${{ github.ref }}              # branch/tag ref (refs/heads/main)
${{ github.ref_name }}         # branch/tag name (main)
${{ github.head_ref }}         # source branch of PR
${{ github.base_ref }}         # target branch of PR
${{ github.event_name }}       # push | pull_request | schedule | workflow_dispatch
${{ github.actor }}            # username who triggered the workflow
${{ github.repository }}       # owner/repo-name
${{ github.repository_owner }} # owner name
${{ github.run_id }}           # unique ID for this workflow run
${{ github.run_number }}       # incrementing run number
${{ github.workflow }}         # workflow name
${{ github.server_url }}       # https://github.com
${{ github.api_url }}          # https://api.github.com
${{ github.event.inputs.environment }}   # workflow_dispatch input

# env context — environment variables
${{ env.PYTHON_VERSION }}

# secrets context — repository secrets
${{ secrets.GITHUB_TOKEN }}    # automatic token, always available
${{ secrets.MY_SECRET }}       # your custom secret

# vars context — configuration variables (non-sensitive)
${{ vars.ENVIRONMENT }}

# runner context — information about the runner
${{ runner.os }}               # Linux | Windows | macOS
${{ runner.arch }}             # X64 | ARM64
${{ runner.temp }}             # temporary directory
${{ runner.tool_cache }}       # tool cache directory

# job context
${{ job.status }}              # success | failure | cancelled

# steps context — output from previous steps
${{ steps.STEP_ID.outputs.OUTPUT_NAME }}
${{ steps.STEP_ID.outcome }}    # success | failure | skipped

# needs context — output from dependency jobs
${{ needs.JOB_ID.outputs.OUTPUT_NAME }}
${{ needs.JOB_ID.result }}      # success | failure | cancelled | skipped

# inputs context — workflow_dispatch inputs
${{ inputs.environment }}

# matrix context
${{ matrix.python-version }}
```

### Expressions

```yaml
# comparison operators
${{ github.ref == 'refs/heads/main' }}
${{ github.ref != 'refs/heads/develop' }}
${{ github.run_number > 10 }}

# logical operators
${{ github.ref == 'refs/heads/main' && github.event_name == 'push' }}
${{ github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop' }}
${{ !contains(github.ref, 'hotfix') }}

# functions
${{ contains(github.ref, 'release') }}          # string contains
${{ startsWith(github.ref, 'refs/heads') }}     # string starts with
${{ endsWith(github.ref, 'main') }}             # string ends with
${{ format('Hello {0}!', github.actor) }}       # string format
${{ join(matrix.python-version, ', ') }}        # join array
${{ toJSON(github.event) }}                     # convert to JSON string
${{ fromJSON('{"key": "value"}').key }}         # parse JSON
${{ hashFiles('requirements.txt') }}            # hash of files
${{ hashFiles('**/package-lock.json') }}        # hash with glob

# status functions (for if: conditions)
${{ success() }}     # all previous steps succeeded
${{ failure() }}     # at least one previous step failed
${{ cancelled() }}   # workflow was cancelled
${{ always() }}      # always true (run regardless of status)
```

---

## 9. Environment Variables and Secrets

### Setting Secrets in GitHub

```
Repository → Settings → Secrets and variables → Actions → New repository secret

For organizations:
Organization → Settings → Secrets → New organization secret

For environments (production, staging):
Repository → Settings → Environments → [env name] → Add secret
```

### Types of Secrets

```yaml
# GITHUB_TOKEN — automatic, always available
# created automatically for each workflow run
# permissions defined by the 'permissions' key in workflow
${{ secrets.GITHUB_TOKEN }}

# Repository secrets — available to all workflows
${{ secrets.GROQ_API_KEY }}
${{ secrets.DATABASE_URL }}

# Environment secrets — only available when 'environment' is set in job
# example: production environment has different keys than staging
${{ secrets.API_KEY }}    # uses the correct one for the environment

# Organization secrets — available to multiple repos
${{ secrets.ORG_WIDE_SECRET }}
```

### Variables (Non-Sensitive)

```yaml
# configuration variables (non-sensitive, visible in logs)
# Repository → Settings → Secrets and variables → Variables
${{ vars.ENVIRONMENT }}
${{ vars.DEPLOY_REGION }}
${{ vars.IMAGE_REGISTRY }}
```

### Using Secrets Safely

```yaml
steps:
  # correct — pass as environment variable
  - name: Deploy
    run: ./deploy.sh
    env:
      API_KEY: ${{ secrets.API_KEY }}

  # WRONG — secret visible in command line and logs
  - name: Deploy (WRONG)
    run: ./deploy.sh --api-key ${{ secrets.API_KEY }}

  # mask a custom value from logs
  - name: Mask value
    run: |
      VALUE=$(generate_token)
      echo "::add-mask::$VALUE"
      echo "value=$VALUE" >> $GITHUB_OUTPUT
```

### OIDC — Keyless Authentication (Best Practice)

Instead of storing cloud credentials as long-lived secrets, use OIDC tokens to authenticate directly with cloud providers.

```yaml
# no secrets needed for AWS/GCP/Azure authentication!
permissions:
  id-token: write   # required for OIDC
  contents: read

steps:
  - name: Configure AWS credentials
    uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789:role/github-actions-role
      aws-region: eu-west-1
      # no AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY needed!
```

---

# PART 2 — CORE WORKFLOWS

---

## 10. Python CI Pipeline

```yaml
# .github/workflows/ci.yml
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.10"

jobs:
  # ── Install and cache dependencies ────────────────────────────
  install:
    name: Install Dependencies
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
          cache-dependency-path: |
            requirements.txt
            requirements-dev.txt

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Cache installed packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ runner.os }}-${{ hashFiles('requirements*.txt') }}

  # ── Lint and format ───────────────────────────────────────────
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install ruff black isort mypy

      - name: Ruff (lint)
        run: ruff check src/ tests/

      - name: Black (format check)
        run: black --check src/ tests/

      - name: isort (import order)
        run: isort --check-only src/ tests/

      - name: MyPy (type checking)
        run: mypy src/
        continue-on-error: true    # don't fail on type errors yet

  # ── Unit tests ────────────────────────────────────────────────
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip

      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            -v \
            --tb=short \
            --cov=src \
            --cov-report=xml:coverage.xml \
            --cov-report=html:htmlcov \
            --cov-fail-under=80 \
            --junitxml=test-results.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: false

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()    # upload even if tests fail
        with:
          name: test-results
          path: |
            test-results.xml
            htmlcov/
          retention-days: 7

  # ── Security scan ─────────────────────────────────────────────
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install safety and bandit
        run: pip install safety bandit

      - name: Check dependencies for vulnerabilities
        run: safety check -r requirements.txt
        continue-on-error: true

      - name: Run bandit (security linter)
        run: bandit -r src/ -f json -o bandit-results.json
        continue-on-error: true

      - name: Upload security results
        uses: actions/upload-artifact@v4
        with:
          name: security-results
          path: bandit-results.json

  # ── Summary ───────────────────────────────────────────────────
  ci-summary:
    name: CI Summary
    runs-on: ubuntu-latest
    needs: [lint, test, security]
    if: always()
    steps:
      - name: Write summary
        run: |
          echo "## CI Results 🚀" >> $GITHUB_STEP_SUMMARY
          echo "| Job | Status |" >> $GITHUB_STEP_SUMMARY
          echo "|-----|--------|" >> $GITHUB_STEP_SUMMARY
          echo "| Lint | ${{ needs.lint.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Tests | ${{ needs.test.result }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Security | ${{ needs.security.result }} |" >> $GITHUB_STEP_SUMMARY
```

---

## 11. Testing — Unit, Integration, Coverage

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install -r requirements-dev.txt

      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=src --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          flags: unit

  integration-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: testpassword
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install -r requirements-dev.txt

      - name: Run integration tests
        run: pytest tests/integration/ -v --cov=src --cov-report=xml
        env:
          DATABASE_URL: postgresql://postgres:testpassword@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379/0

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          flags: integration

  coverage-check:
    needs: [unit-tests, integration-tests]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install pytest pytest-cov

      - name: Run all tests with combined coverage
        run: |
          pytest tests/ \
            --cov=src \
            --cov-report=term-missing \
            --cov-fail-under=80
```

---

## 12. Code Quality — Linting and Formatting

```yaml
# .github/workflows/quality.yml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  python-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - name: Install tools
        run: pip install ruff black isort mypy pylint

      # Ruff — fast Python linter (replaces flake8, pylint, isort)
      - name: Ruff lint
        run: ruff check . --output-format=github

      # Black — code formatter
      - name: Black format check
        run: black --check --diff .

      # isort — import sorter
      - name: isort check
        run: isort --check-only --diff .

      # MyPy — static type checker
      - name: MyPy type check
        run: mypy src/ --ignore-missing-imports
        continue-on-error: true

      # Pylint — comprehensive linter
      - name: Pylint
        run: pylint src/ --fail-under=7.0
        continue-on-error: true

  # Auto-fix formatting on PRs
  auto-format:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"

      - run: pip install black isort ruff

      - name: Format code
        run: |
          black .
          isort .
          ruff check . --fix

      - name: Commit changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "style: auto-format with black, isort, ruff"
          branch: ${{ github.head_ref }}
```

---

## 13. Docker Build and Push

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ["v*"]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      # ── Setup Docker Buildx (multi-platform builds) ────────────
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      # ── Login to GitHub Container Registry ────────────────────
      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # ── Login to Docker Hub (if also pushing there) ───────────
      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # ── Extract metadata (tags and labels) ────────────────────
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
            kempsly/finsaight-api
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=sha-,format=short
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}
          # generates tags like:
          # ghcr.io/kempsly/finsaight-api:main
          # ghcr.io/kempsly/finsaight-api:sha-abc1234
          # ghcr.io/kempsly/finsaight-api:v1.2.3
          # ghcr.io/kempsly/finsaight-api:latest

      # ── Build and push ─────────────────────────────────────────
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: ${{ github.event_name != 'pull_request' }}   # don't push on PRs
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          platforms: linux/amd64,linux/arm64    # multi-arch build
          cache-from: type=gha                  # GitHub Actions cache
          cache-to: type=gha,mode=max
          build-args: |
            BUILD_DATE=${{ github.event.head_commit.timestamp }}
            VERSION=${{ github.sha }}
          target: production                    # multi-stage build target

      # ── Scan image for vulnerabilities ────────────────────────
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ steps.meta.outputs.version }}
          format: sarif
          output: trivy-results.sarif
          severity: CRITICAL,HIGH

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: trivy-results.sarif

      # ── Write summary ─────────────────────────────────────────
      - name: Write summary
        run: |
          echo "## Docker Build 🐳" >> $GITHUB_STEP_SUMMARY
          echo "**Image:** \`${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}\`" >> $GITHUB_STEP_SUMMARY
          echo "**Tags:**" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
          echo "${{ steps.meta.outputs.tags }}" >> $GITHUB_STEP_SUMMARY
          echo "\`\`\`" >> $GITHUB_STEP_SUMMARY
```

---

## 14. Matrix Builds

```yaml
# .github/workflows/matrix.yml
name: Matrix Tests

on: [push, pull_request]

jobs:
  test:
    name: "Python ${{ matrix.python-version }} on ${{ matrix.os }}"
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false    # continue other matrix jobs if one fails
      max-parallel: 6     # run max 6 jobs at once

      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12"]
        os: [ubuntu-latest, windows-latest, macos-latest]

        # exclude specific combinations
        exclude:
          - os: windows-latest
            python-version: "3.9"
          - os: macos-latest
            python-version: "3.9"

        # include additional specific combinations with extra variables
        include:
          - os: ubuntu-latest
            python-version: "3.10"
            coverage: true    # extra variable for this combination only
          - os: ubuntu-latest
            python-version: "3.11"
            experimental: true

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip

      - run: pip install -r requirements-dev.txt

      - name: Run tests
        run: pytest tests/ -v

      - name: Upload coverage
        if: matrix.coverage == true    # only for the combination that has coverage=true
        uses: codecov/codecov-action@v4

  # ── Dynamic matrix from a list ────────────────────────────────
  dynamic-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.set-matrix.outputs.matrix }}
    steps:
      - id: set-matrix
        run: |
          # generate matrix from file or API
          MATRIX='{"include":[{"env":"staging","url":"staging.example.com"},{"env":"prod","url":"prod.example.com"}]}'
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  deploy:
    needs: [dynamic-matrix]
    strategy:
      matrix: ${{ fromJSON(needs.dynamic-matrix.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ matrix.env }} at ${{ matrix.url }}"
```

---

## 15. Caching Dependencies

```yaml
# .github/workflows/cache.yml
name: Caching Best Practices

on: [push]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ── Python pip cache ──────────────────────────────────────
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip                                      # built-in cache
          cache-dependency-path: requirements*.txt        # hash these files

      # ── Manual cache (more control) ───────────────────────────
      - name: Cache pip manually
        uses: actions/cache@v4
        id: pip-cache
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-py310-pip-${{ hashFiles('requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-py310-pip-
            ${{ runner.os }}-py310-
            ${{ runner.os }}-

      - name: Install if cache miss
        if: steps.pip-cache.outputs.cache-hit != 'true'
        run: pip install -r requirements.txt

      # ── Node.js npm cache ─────────────────────────────────────
      - uses: actions/setup-node@v4
        with:
          node-version: "18"
          cache: npm
          cache-dependency-path: frontend/package-lock.json

      # ── Docker layer cache ────────────────────────────────────
      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v5
        with:
          context: .
          cache-from: type=gha
          cache-to: type=gha,mode=max

      # ── Model cache (ML specific) ─────────────────────────────
      - name: Cache ML models
        uses: actions/cache@v4
        with:
          path: ~/.cache/huggingface
          key: models-${{ hashFiles('model_requirements.txt') }}

      # ── Cache ML artifacts between runs ───────────────────────
      - name: Cache dataset
        uses: actions/cache@v4
        with:
          path: data/processed/
          key: dataset-${{ hashFiles('data/raw/**') }}-v1
          # cache is invalidated when raw data changes
```

---

## 16. Artifacts — Saving Build Outputs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build application
        run: python setup.py build

      # ── Upload single artifact ─────────────────────────────────
      - name: Upload build
        uses: actions/upload-artifact@v4
        with:
          name: dist-packages
          path: dist/
          retention-days: 30
          if-no-files-found: error    # error | warn | ignore
          compression-level: 6        # 0-9

      # ── Upload multiple artifacts ──────────────────────────────
      - name: Upload test results and coverage
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-reports-${{ github.run_number }}
          path: |
            reports/
            coverage.xml
            test-results.xml

  deploy:
    needs: [build]
    runs-on: ubuntu-latest
    steps:
      # ── Download artifact ──────────────────────────────────────
      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist-packages
          path: dist/

      # ── Download all artifacts ─────────────────────────────────
      - name: Download all artifacts
        uses: actions/download-artifact@v4
        with:
          path: artifacts/    # downloads all to artifacts/<name>/

      - name: Deploy
        run: ls dist/ && ./deploy.sh

  train-and-save-model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install -r requirements.txt

      - name: Train model
        run: python train.py --output models/

      # ── Save trained model as artifact ────────────────────────
      - name: Upload trained model
        uses: actions/upload-artifact@v4
        with:
          name: trained-model-${{ github.sha }}
          path: |
            models/model.ubj
            models/metadata.json
            models/feature_names.json
          retention-days: 90

  evaluate-model:
    needs: [train-and-save-model]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model-${{ github.sha }}
          path: models/

      - name: Evaluate model
        run: python evaluate.py
```

---

## 17. Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
# This workflow can be called by other workflows
name: Reusable Deploy Workflow

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
      replicas:
        required: false
        type: number
        default: 3
    secrets:
      KUBE_CONFIG:
        required: true
      API_KEY:
        required: false
    outputs:
      deployment-url:
        description: "The URL of the deployed application"
        value: ${{ jobs.deploy.outputs.url }}

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    outputs:
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - name: Deploy to ${{ inputs.environment }}
        id: deploy
        run: |
          echo "Deploying ${{ inputs.image-tag }} to ${{ inputs.environment }}"
          echo "url=https://${{ inputs.environment }}.example.com" >> $GITHUB_OUTPUT
        env:
          KUBE_CONFIG: ${{ secrets.KUBE_CONFIG }}
```

```yaml
# .github/workflows/cd.yml — calls the reusable workflow
name: CD

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.tag.outputs.tag }}
    steps:
      - uses: actions/checkout@v4
      - id: tag
        run: echo "tag=${{ github.sha }}" >> $GITHUB_OUTPUT

  deploy-staging:
    needs: [build]
    uses: ./.github/workflows/reusable-deploy.yml     # call reusable workflow
    with:
      environment: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
      replicas: 2
    secrets:
      KUBE_CONFIG: ${{ secrets.STAGING_KUBE_CONFIG }}

  deploy-production:
    needs: [deploy-staging]
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: production
      image-tag: ${{ needs.build.outputs.image-tag }}
      replicas: 5
    secrets:
      KUBE_CONFIG: ${{ secrets.PROD_KUBE_CONFIG }}
      API_KEY: ${{ secrets.PROD_API_KEY }}
```

---

## 18. Composite Actions

```yaml
# .github/actions/setup-ml-env/action.yml
# Custom composite action — reusable step sequence
name: Setup ML Environment
description: Set up Python environment for ML workflows

inputs:
  python-version:
    description: Python version to use
    required: false
    default: "3.10"
  install-gpu:
    description: Install GPU dependencies
    required: false
    default: "false"

outputs:
  cache-hit:
    description: Whether the cache was hit
    value: ${{ steps.cache.outputs.cache-hit }}

runs:
  using: composite
  steps:
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ inputs.python-version }}

    - name: Cache pip
      id: cache
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ml-env-${{ inputs.python-version }}-${{ hashFiles('requirements*.txt') }}

    - name: Install ML dependencies
      shell: bash
      run: |
        pip install --upgrade pip
        pip install -r requirements.txt
        if [ "${{ inputs.install-gpu }}" == "true" ]; then
          pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
        fi
```

```yaml
# Using the composite action in a workflow
steps:
  - uses: actions/checkout@v4

  - name: Setup ML environment
    uses: ./.github/actions/setup-ml-env
    with:
      python-version: "3.10"
      install-gpu: "false"
```

---

# PART 3 — ML/AI SPECIFIC PIPELINES

---

## 19. ML Model Training Pipeline

```yaml
# .github/workflows/train-model.yml
name: ML Model Training

on:
  push:
    paths:
      - "src/models/**"
      - "src/data/**"
      - "requirements.txt"
      - "train.py"
  schedule:
    - cron: "0 2 * * 1"    # retrain every Monday at 2am
  workflow_dispatch:
    inputs:
      model-type:
        description: Model type to train
        required: true
        default: xgboost
        type: choice
        options: [xgboost, lightgbm, catboost]
      dataset-version:
        description: Dataset version
        required: false
        default: latest

jobs:
  # ── Data validation ───────────────────────────────────────────
  validate-data:
    name: Validate Data
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install -r requirements.txt

      - name: Validate dataset schema
        run: python scripts/validate_data.py

      - name: Check data quality
        run: |
          python -c "
          import pandas as pd
          df = pd.read_csv('data/raw/dataset.csv')
          assert len(df) > 1000, 'Dataset too small'
          assert df.isnull().sum().sum() / len(df) < 0.1, 'Too many missing values'
          print(f'Dataset valid: {len(df)} rows')
          "

  # ── Train model ───────────────────────────────────────────────
  train:
    name: Train Model
    runs-on: ubuntu-latest
    needs: [validate-data]
    outputs:
      model-artifact: ${{ steps.upload.outputs.artifact-id }}
      auc-score: ${{ steps.train.outputs.auc }}

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install -r requirements.txt

      - name: Cache training data
        uses: actions/cache@v4
        with:
          path: data/processed/
          key: data-${{ hashFiles('data/raw/**') }}

      - name: Train model
        id: train
        run: |
          python train.py \
            --model-type ${{ inputs.model-type || 'xgboost' }} \
            --output-dir models/ \
            --dataset-version ${{ inputs.dataset-version || 'latest' }}

          # read metrics from output file
          AUC=$(python -c "import json; print(json.load(open('models/metrics.json'))['auc'])")
          echo "auc=$AUC" >> $GITHUB_OUTPUT
          echo "Trained model AUC: $AUC"
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          MLFLOW_EXPERIMENT_NAME: finsaight-credit-default

      - name: Upload model artifact
        id: upload
        uses: actions/upload-artifact@v4
        with:
          name: trained-model-${{ github.run_id }}
          path: |
            models/model.ubj
            models/metrics.json
            models/feature_names.json
            models/preprocessing.pkl
          retention-days: 90

      - name: Write training summary
        run: |
          echo "## Model Training Results 🤖" >> $GITHUB_STEP_SUMMARY
          echo "**Model Type:** ${{ inputs.model-type || 'xgboost' }}" >> $GITHUB_STEP_SUMMARY
          echo "**AUC Score:** ${{ steps.train.outputs.auc }}" >> $GITHUB_STEP_SUMMARY
          echo "**Artifact:** trained-model-${{ github.run_id }}" >> $GITHUB_STEP_SUMMARY

  # ── Evaluate model ────────────────────────────────────────────
  evaluate:
    name: Evaluate Model
    runs-on: ubuntu-latest
    needs: [train]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install -r requirements.txt

      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model-${{ github.run_id }}
          path: models/

      - name: Evaluate model
        run: |
          python evaluate.py \
            --model-path models/model.ubj \
            --test-data data/test/

      - name: Check metrics threshold
        run: |
          python -c "
          import json, sys
          metrics = json.load(open('models/metrics.json'))
          if metrics['auc'] < 0.75:
              print(f'AUC {metrics[\"auc\"]} below threshold 0.75 — failing')
              sys.exit(1)
          print(f'AUC {metrics[\"auc\"]} above threshold — passing')
          "

  # ── Deploy model ──────────────────────────────────────────────
  deploy-model:
    name: Deploy Model to Serving
    runs-on: ubuntu-latest
    needs: [evaluate]
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Download model
        uses: actions/download-artifact@v4
        with:
          name: trained-model-${{ github.run_id }}
          path: models/

      - name: Upload model to S3
        run: |
          aws s3 sync models/ s3://finsaight-models/production/latest/
          aws s3 sync models/ s3://finsaight-models/production/${{ github.sha }}/
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: eu-west-1
```

---

## 20. Model Evaluation and Registry

```yaml
# .github/workflows/model-registry.yml
name: Model Registry

on:
  workflow_run:
    workflows: ["ML Model Training"]
    types: [completed]
    branches: [main]

jobs:
  register-model:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install mlflow boto3

      - name: Register model in MLflow
        run: |
          python -c "
          import mlflow
          mlflow.set_tracking_uri('${{ secrets.MLFLOW_TRACKING_URI }}')

          # find the best run
          experiment = mlflow.get_experiment_by_name('finsaight-credit-default')
          runs = mlflow.search_runs(
              experiment_ids=[experiment.experiment_id],
              filter_string='metrics.auc > 0.80',
              order_by=['metrics.auc DESC'],
              max_results=1,
          )

          if len(runs) > 0:
              best_run_id = runs.iloc[0].run_id
              # register in model registry
              mlflow.register_model(
                  f'runs:/{best_run_id}/model',
                  'finsaight-credit-default'
              )
              print(f'Registered model from run {best_run_id}')
          "
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
```

---

## 21. MLflow Integration

```yaml
# .github/workflows/mlflow.yml
name: MLflow Experiment Tracking

on:
  push:
    paths: ["src/models/**", "train.py"]

jobs:
  experiment:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install mlflow xgboost scikit-learn

      - name: Run experiment with MLflow
        run: python train.py
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          MLFLOW_EXPERIMENT_NAME: ci-experiments
          MLFLOW_RUN_NAME: "ci-${{ github.sha }}"
          MLFLOW_TAGS_GIT_SHA: ${{ github.sha }}
          MLFLOW_TAGS_BRANCH: ${{ github.ref_name }}
          MLFLOW_TAGS_RUN_ID: ${{ github.run_id }}
```

---

## 22. Jupyter Notebook CI

```yaml
# .github/workflows/notebooks.yml
name: Jupyter Notebook CI

on:
  push:
    paths: ["notebooks/**"]

jobs:
  run-notebooks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - run: pip install jupyter nbconvert nbmake pytest

      - name: Execute notebooks
        run: |
          pytest --nbmake notebooks/ \
            --nbmake-timeout=120 \
            -v

      - name: Convert notebooks to HTML
        run: |
          jupyter nbconvert --to html notebooks/*.ipynb
          mkdir -p reports/notebooks
          mv notebooks/*.html reports/notebooks/

      - name: Upload notebook reports
        uses: actions/upload-artifact@v4
        with:
          name: notebook-reports
          path: reports/notebooks/
```

---

# PART 4 — CD TO EVERY PLATFORM

---

## 23. Deploy to AWS ECS

```yaml
# .github/workflows/deploy-ecs.yml
name: Deploy to AWS ECS

on:
  push:
    branches: [main]

env:
  AWS_REGION: eu-west-1
  ECR_REPOSITORY: finsaight-api
  ECS_SERVICE: finsaight-api-service
  ECS_CLUSTER: finsaight-cluster
  CONTAINER_NAME: api

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      # ── Authenticate with AWS via OIDC (no stored credentials) ─
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions-role
          aws-region: ${{ env.AWS_REGION }}

      # ── Login to Amazon ECR ────────────────────────────────────
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      # ── Build and push to ECR ──────────────────────────────────
      - name: Build, tag, and push image to ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      # ── Update ECS task definition ────────────────────────────
      - name: Download current task definition
        run: |
          aws ecs describe-task-definition \
            --task-definition finsaight-api \
            --query taskDefinition > task-definition.json

      - name: Fill in new image in task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}
          environment-variables: |
            GROQ_API_KEY=${{ secrets.GROQ_API_KEY }}
            ENVIRONMENT=production

      # ── Deploy to ECS ─────────────────────────────────────────
      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
          wait-for-minutes: 10

      - name: Summary
        run: |
          echo "## Deployed to ECS 🚀" >> $GITHUB_STEP_SUMMARY
          echo "**Image:** ${{ steps.build-image.outputs.image }}" >> $GITHUB_STEP_SUMMARY
          echo "**Cluster:** ${{ env.ECS_CLUSTER }}" >> $GITHUB_STEP_SUMMARY
          echo "**Service:** ${{ env.ECS_SERVICE }}" >> $GITHUB_STEP_SUMMARY
```

---

## 24. Deploy to AWS EKS (Kubernetes)

```yaml
# .github/workflows/deploy-eks.yml
name: Deploy to AWS EKS

on:
  push:
    branches: [main]

env:
  AWS_REGION: eu-west-1
  EKS_CLUSTER: finsaight-cluster
  ECR_REPOSITORY: finsaight-api
  NAMESPACE: finsaight

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions-eks-role
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push image
        id: build
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:latest .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      # ── Configure kubectl ─────────────────────────────────────
      - name: Update kubeconfig for EKS
        run: |
          aws eks update-kubeconfig \
            --name ${{ env.EKS_CLUSTER }} \
            --region ${{ env.AWS_REGION }}

      # ── Deploy to Kubernetes ──────────────────────────────────
      - name: Set image in deployment
        run: |
          kubectl set image deployment/finsaight-api \
            api=${{ steps.build.outputs.image }} \
            -n ${{ env.NAMESPACE }}

      - name: Wait for rollout
        run: |
          kubectl rollout status deployment/finsaight-api \
            -n ${{ env.NAMESPACE }} \
            --timeout=300s

      - name: Verify deployment
        run: |
          kubectl get pods -n ${{ env.NAMESPACE }}
          kubectl get svc -n ${{ env.NAMESPACE }}

      # ── Or use Helm ───────────────────────────────────────────
      - name: Deploy with Helm
        run: |
          helm upgrade --install finsaight ./charts/finsaight \
            --namespace ${{ env.NAMESPACE }} \
            --create-namespace \
            --set image.tag=${{ github.sha }} \
            --set image.repository=${{ steps.login-ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }} \
            --set replicaCount=3 \
            --wait \
            --timeout 5m0s \
            --atomic    # rollback on failure
```

---

## 25. Deploy to AWS Lambda (Serverless)

```yaml
# .github/workflows/deploy-lambda.yml
name: Deploy to AWS Lambda

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
          cache: pip

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions-lambda-role
          aws-region: eu-west-1

      # ── Option A — Deploy as container image ──────────────────
      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build and push Lambda container
        run: |
          docker build -f Dockerfile.lambda \
            -t ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.eu-west-1.amazonaws.com/finsaight-lambda:${{ github.sha }} .
          docker push ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.eu-west-1.amazonaws.com/finsaight-lambda:${{ github.sha }}

      - name: Update Lambda function
        run: |
          aws lambda update-function-code \
            --function-name finsaight-api \
            --image-uri ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.eu-west-1.amazonaws.com/finsaight-lambda:${{ github.sha }}

      - name: Wait for update
        run: |
          aws lambda wait function-updated \
            --function-name finsaight-api

      # ── Option B — Deploy as ZIP package ─────────────────────
      - name: Create deployment package
        run: |
          pip install -r requirements.txt -t package/
          cp -r src/ package/
          cp lambda_handler.py package/
          cd package && zip -r ../deployment.zip .

      - name: Deploy ZIP to Lambda
        run: |
          aws lambda update-function-code \
            --function-name finsaight-api \
            --zip-file fileb://deployment.zip

      # ── Option C — Serverless Framework ──────────────────────
      - name: Deploy with Serverless Framework
        run: |
          npm install -g serverless
          serverless deploy --stage production
        env:
          SERVERLESS_ACCESS_KEY: ${{ secrets.SERVERLESS_ACCESS_KEY }}
```

---

## 26. Deploy to Google Cloud Run

```yaml
# .github/workflows/deploy-cloudrun.yml
name: Deploy to Google Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: your-gcp-project-id
  REGION: europe-west1
  SERVICE_NAME: finsaight-api
  REGISTRY: europe-west1-docker.pkg.dev

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      # ── Authenticate with Google Cloud via OIDC ────────────────
      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/${{ secrets.GCP_PROJECT_NUMBER }}/locations/global/workloadIdentityPools/github-pool/providers/github-provider
          service_account: github-actions@${{ env.PROJECT_ID }}.iam.gserviceaccount.com

      # ── Set up gcloud CLI ─────────────────────────────────────
      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      # ── Configure Docker to use gcloud credentials ────────────
      - name: Configure Docker
        run: gcloud auth configure-docker ${{ env.REGISTRY }}

      # ── Build and push to Artifact Registry ───────────────────
      - name: Build and push image
        id: build
        run: |
          IMAGE="${{ env.REGISTRY }}/${{ env.PROJECT_ID }}/finsaight/${{ env.SERVICE_NAME }}:${{ github.sha }}"
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

      # ── Deploy to Cloud Run ───────────────────────────────────
      - name: Deploy to Cloud Run
        id: deploy
        uses: google-github-actions/deploy-cloudrun@v2
        with:
          service: ${{ env.SERVICE_NAME }}
          region: ${{ env.REGION }}
          image: ${{ steps.build.outputs.image }}
          flags: |
            --allow-unauthenticated
            --min-instances=1
            --max-instances=10
            --memory=2Gi
            --cpu=2
            --concurrency=80
            --timeout=300
          env_vars: |
            ENVIRONMENT=production
          secrets: |
            GROQ_API_KEY=groq-api-key:latest
            DATABASE_URL=database-url:latest

      - name: Show deployment URL
        run: |
          echo "## Deployed to Cloud Run ☁️" >> $GITHUB_STEP_SUMMARY
          echo "**URL:** ${{ steps.deploy.outputs.url }}" >> $GITHUB_STEP_SUMMARY
```

---

## 27. Deploy to Google GKE

```yaml
# .github/workflows/deploy-gke.yml
name: Deploy to GKE

on:
  push:
    branches: [main]

env:
  PROJECT_ID: your-gcp-project-id
  GKE_CLUSTER: finsaight-cluster
  GKE_ZONE: europe-west1
  REGISTRY: europe-west1-docker.pkg.dev
  IMAGE: finsaight-api
  NAMESPACE: finsaight

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
          service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2
        with:
          install_components: gke-gcloud-auth-plugin

      - name: Configure Docker
        run: gcloud auth configure-docker ${{ env.REGISTRY }}

      - name: Build and push
        id: build
        run: |
          IMAGE="${{ env.REGISTRY }}/${{ env.PROJECT_ID }}/finsaight/${{ env.IMAGE }}:${{ github.sha }}"
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

      - name: Get GKE credentials
        run: |
          gcloud container clusters get-credentials ${{ env.GKE_CLUSTER }} \
            --region ${{ env.GKE_ZONE }} \
            --project ${{ env.PROJECT_ID }}

      - name: Deploy to GKE
        run: |
          kubectl set image deployment/finsaight-api \
            api=${{ steps.build.outputs.image }} \
            -n ${{ env.NAMESPACE }}

          kubectl rollout status deployment/finsaight-api \
            -n ${{ env.NAMESPACE }} \
            --timeout=300s
```

---

## 28. Deploy to Azure Container Apps

```yaml
# .github/workflows/deploy-aca.yml
name: Deploy to Azure Container Apps

on:
  push:
    branches: [main]

env:
  AZURE_CONTAINER_APP: finsaight-api
  AZURE_RESOURCE_GROUP: finsaight-rg
  ACR_NAME: finsaightregistry
  IMAGE_NAME: finsaight-api

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      # ── Authenticate with Azure via OIDC ──────────────────────
      - name: Azure Login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      # ── Build and push to Azure Container Registry ────────────
      - name: Login to ACR
        run: |
          az acr login --name ${{ env.ACR_NAME }}

      - name: Build and push image
        id: build
        run: |
          IMAGE="${{ env.ACR_NAME }}.azurecr.io/${{ env.IMAGE_NAME }}:${{ github.sha }}"
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

      # ── Deploy to Azure Container Apps ────────────────────────
      - name: Deploy to Container Apps
        uses: azure/container-apps-deploy-action@v2
        with:
          appSourcePath: ${{ github.workspace }}
          acrName: ${{ env.ACR_NAME }}
          containerAppName: ${{ env.AZURE_CONTAINER_APP }}
          resourceGroup: ${{ env.AZURE_RESOURCE_GROUP }}
          imageToDeploy: ${{ steps.build.outputs.image }}
          environmentVariables: |
            ENVIRONMENT=production
            PORT=8000
```

---

## 29. Deploy to Azure AKS

```yaml
# .github/workflows/deploy-aks.yml
name: Deploy to AKS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Build and push to ACR
        id: build
        run: |
          az acr login --name ${{ secrets.ACR_NAME }}
          IMAGE="${{ secrets.ACR_NAME }}.azurecr.io/finsaight:${{ github.sha }}"
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

      - name: Get AKS credentials
        uses: azure/aks-set-context@v4
        with:
          resource-group: finsaight-rg
          cluster-name: finsaight-cluster

      - name: Deploy to AKS
        run: |
          kubectl set image deployment/finsaight-api \
            api=${{ steps.build.outputs.image }} \
            -n finsaight

          kubectl rollout status deployment/finsaight-api \
            -n finsaight --timeout=300s
```

---

## 30. Deploy to DigitalOcean App Platform

```yaml
# .github/workflows/deploy-digitalocean.yml
name: Deploy to DigitalOcean

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # ── Install doctl ─────────────────────────────────────────
      - name: Install doctl
        uses: digitalocean/action-doctl@v2
        with:
          token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}

      # ── Push to DigitalOcean Container Registry ───────────────
      - name: Login to DOCR
        run: doctl registry login --expiry-seconds 600

      - name: Build and push
        id: build
        run: |
          IMAGE="registry.digitalocean.com/finsaight/api:${{ github.sha }}"
          docker build -t $IMAGE .
          docker push $IMAGE
          echo "image=$IMAGE" >> $GITHUB_OUTPUT

      # ── Option A — Deploy to App Platform ─────────────────────
      - name: Deploy to App Platform
        run: |
          doctl apps create-deployment ${{ secrets.DIGITALOCEAN_APP_ID }}

      # ── Option B — Deploy to DOKS (Kubernetes) ────────────────
      - name: Save kubeconfig
        run: doctl kubernetes cluster kubeconfig save finsaight-cluster

      - name: Deploy to DOKS
        run: |
          kubectl set image deployment/finsaight-api \
            api=${{ steps.build.outputs.image }} \
            -n finsaight

          kubectl rollout status deployment/finsaight-api \
            -n finsaight --timeout=300s
```

---

## 31. Deploy to Heroku

```yaml
# .github/workflows/deploy-heroku.yml
name: Deploy to Heroku

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # ── Option A — Deploy with Heroku CLI ─────────────────────
      - name: Install Heroku CLI
        run: curl https://cli-assets.heroku.com/install.sh | sh

      - name: Login to Heroku
        run: |
          echo "${{ secrets.HEROKU_API_KEY }}" | heroku auth:token
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}

      - name: Deploy to Heroku
        run: |
          heroku git:remote -a finsaight-api
          git push heroku main
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}

      # ── Option B — Deploy with Docker ─────────────────────────
      - name: Deploy Docker to Heroku
        run: |
          docker login --username=_ \
            --password=${{ secrets.HEROKU_API_KEY }} \
            registry.heroku.com

          docker build -t registry.heroku.com/finsaight-api/web .
          docker push registry.heroku.com/finsaight-api/web

          heroku container:release web -a finsaight-api
        env:
          HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}

      # ── Option C — AkhileshNS/heroku-deploy action ────────────
      - name: Deploy to Heroku (action)
        uses: akhileshns/heroku-deploy@v3.13.15
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: finsaight-api
          heroku_email: kempsly@example.com
          usedocker: true
```

---

## 32. Deploy to Railway

```yaml
# .github/workflows/deploy-railway.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install Railway CLI
        run: npm install -g @railway/cli

      - name: Deploy to Railway
        run: railway up --detach
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

---

## 33. Deploy to Kubernetes (Generic)

```yaml
# .github/workflows/deploy-k8s.yml
# Works with any Kubernetes cluster
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      # ── Build and push image ──────────────────────────────────
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      # ── Configure kubectl ─────────────────────────────────────
      - name: Configure kubectl
        uses: azure/k8s-set-context@v4
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}
          # OR use service account token:
          # method: service-account
          # k8s-url: ${{ secrets.K8S_URL }}
          # k8s-secret: ${{ secrets.K8S_SECRET }}

      # ── Update image in deployment ────────────────────────────
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/finsaight-api \
            api=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n finsaight

          kubectl rollout status deployment/finsaight-api \
            -n finsaight \
            --timeout=300s

      # ── Or apply full manifests ───────────────────────────────
      - name: Apply Kubernetes manifests
        uses: azure/k8s-deploy@v5
        with:
          namespace: finsaight
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
            k8s/ingress.yaml
          images: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          strategy: canary    # canary | blue-green | basic
          percentage: 20      # start with 20% traffic
```

---

## 34. Deploy with Docker Compose (VPS/Self-hosted)

```yaml
# .github/workflows/deploy-vps.yml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      # ── Build and push image ──────────────────────────────────
      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest

      # ── Deploy via SSH ────────────────────────────────────────
      - name: Deploy to VPS via SSH
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          port: 22
          script: |
            set -e
            cd /opt/finsaight

            # pull latest image
            echo "${{ secrets.GITHUB_TOKEN }}" | \
              docker login ghcr.io -u ${{ github.actor }} --password-stdin
            docker pull ghcr.io/${{ github.repository }}:latest

            # update .env with current values
            cat > .env <<EOF
            GROQ_API_KEY=${{ secrets.GROQ_API_KEY }}
            DATABASE_URL=${{ secrets.DATABASE_URL }}
            ENVIRONMENT=production
            EOF

            # deploy with zero-downtime
            docker compose pull
            docker compose up -d --no-deps --force-recreate api

            # cleanup old images
            docker image prune -f

            # verify deployment
            sleep 10
            curl -f http://localhost:8000/health || exit 1
            echo "Deployment successful"

      # ── Deploy via rsync + SSH ────────────────────────────────
      - name: Copy files to VPS
        uses: burnett01/rsync-deployments@6.0.0
        with:
          switches: -avzr --delete --exclude='.env' --exclude='data/'
          path: .
          remote_path: /opt/finsaight
          remote_host: ${{ secrets.VPS_HOST }}
          remote_user: ${{ secrets.VPS_USER }}
          remote_key: ${{ secrets.VPS_SSH_KEY }}
```

---

# PART 5 — ADVANCED TOPICS

---

## 35. Environments and Approval Gates

```yaml
# Create environments in GitHub:
# Repository → Settings → Environments → New environment

# production environment with required reviewers:
# - add reviewers who must approve before deployment
# - add wait timer (e.g., 5 minutes after CI passes)
# - restrict to specific branches (main only)

jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    environment: staging    # auto-deploys (no approval)
    steps:
      - run: echo "Deploying to staging"

  integration-test:
    needs: [deploy-staging]
    runs-on: ubuntu-latest
    steps:
      - run: |
          sleep 10
          curl -f https://staging.finsaight.example.com/health

  deploy-production:
    needs: [integration-test]
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://finsaight.example.com   # shown in GitHub deployments
    # GitHub pauses here and waits for a reviewer to approve
    steps:
      - run: echo "Deploying to production"
```

---

## 36. Self-Hosted Runners

```yaml
# Register a self-hosted runner:
# Repository → Settings → Actions → Runners → New self-hosted runner
# Follow the instructions to download and configure the runner agent

# Use self-hosted runner in workflow
jobs:
  train-on-gpu:
    runs-on: [self-hosted, gpu, linux]
    # runs on your GPU server with these labels
    steps:
      - uses: actions/checkout@v4
      - run: python train.py --gpu

  # Mix GitHub-hosted and self-hosted
  build:
    runs-on: ubuntu-latest    # GitHub-hosted

  deploy:
    runs-on: [self-hosted, linux, production]    # self-hosted
```

```bash
# Install runner on your server
mkdir actions-runner && cd actions-runner

curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# configure (token from GitHub Settings)
./config.sh --url https://github.com/kempsly/machine_learning_tuto \
  --token YOUR_TOKEN \
  --labels gpu,linux,cuda \
  --name gpu-server-1

# run as service
sudo ./svc.sh install
sudo ./svc.sh start
```

---

## 37. GitHub Actions Security

```yaml
# ── Security best practices ───────────────────────────────────

# 1. Pin action versions to SHA (not tags)
# INSECURE — tags can be changed
uses: actions/checkout@v4

# SECURE — SHA cannot be changed
uses: actions/checkout@v4   # use @SHA for production
# Find SHA: click on tag in GitHub, copy full commit SHA

# 2. Minimal permissions
permissions:
  contents: read    # never use 'write-all'

# 3. Never print secrets
- run: echo ${{ secrets.API_KEY }}    # NEVER do this — masked but risky

# 4. Validate external inputs
- name: Validate input
  run: |
    INPUT="${{ github.event.inputs.environment }}"
    if [[ "$INPUT" != "staging" && "$INPUT" != "production" ]]; then
      echo "Invalid environment: $INPUT"
      exit 1
    fi

# 5. Use OIDC instead of long-lived credentials
permissions:
  id-token: write
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123:role/github-role
    aws-region: eu-west-1

# 6. CodeQL security scanning
- name: Initialize CodeQL
  uses: github/codeql-action/init@v3
  with:
    languages: python

- name: Analyze
  uses: github/codeql-action/analyze@v3
```

---

## 38. Workflow Optimization and Performance

```yaml
# ── Optimization techniques ───────────────────────────────────

# 1. Run jobs in parallel (default)
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    steps: [...]
  # lint and test run in PARALLEL

# 2. Cache aggressively
- uses: actions/setup-python@v5
  with:
    cache: pip    # built-in cache
    cache-dependency-path: requirements.txt

# 3. Skip unchanged code with paths filter
on:
  push:
    paths:
      - "src/**"
      - "tests/**"
    paths-ignore:
      - "docs/**"
      - "*.md"

# 4. Concurrency — cancel stale runs
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

# 5. Fail fast in matrix
strategy:
  fail-fast: true    # cancel remaining matrix jobs if one fails

# 6. Reuse workflows to avoid duplication
uses: ./.github/workflows/reusable-test.yml

# 7. Use ubuntu-latest (fastest runner)
runs-on: ubuntu-latest

# 8. Minimize checkout depth
- uses: actions/checkout@v4
  with:
    fetch-depth: 1    # only latest commit (faster)
    # use fetch-depth: 0 only when you need full history

# 9. Use Docker layer cache
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

---

## 39. Notifications and Reporting

```yaml
# .github/workflows/notify.yml

jobs:
  notify:
    runs-on: ubuntu-latest
    if: always()

    steps:
      # ── Slack notification ────────────────────────────────────
      - name: Notify Slack on success
        if: success()
        uses: slackapi/slack-github-action@v1.27.0
        with:
          channel-id: "deployments"
          payload: |
            {
              "text": "✅ Deployment to production succeeded",
              "attachments": [{
                "color": "good",
                "fields": [
                  {"title": "Repository", "value": "${{ github.repository }}", "short": true},
                  {"title": "Branch", "value": "${{ github.ref_name }}", "short": true},
                  {"title": "Commit", "value": "${{ github.sha }}", "short": false},
                  {"title": "Actor", "value": "${{ github.actor }}", "short": true}
                ]
              }]
            }
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}

      - name: Notify Slack on failure
        if: failure()
        uses: slackapi/slack-github-action@v1.27.0
        with:
          channel-id: "alerts"
          slack-message: "❌ Deployment FAILED — ${{ github.repository }} — ${{ github.run_id }}"
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}

      # ── PR comment with test results ──────────────────────────
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const body = `## CI Results

            | Check | Status |
            |-------|--------|
            | Tests | ${{ needs.test.result == 'success' && '✅ Pass' || '❌ Fail' }} |
            | Lint  | ${{ needs.lint.result == 'success' && '✅ Pass' || '❌ Fail' }} |
            | Build | ${{ needs.build.result == 'success' && '✅ Pass' || '❌ Fail' }} |

            [View run details](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });

      # ── Create GitHub deployment status ───────────────────────
      - name: Create deployment status
        uses: chrnorm/deployment-status@v2
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          deployment-id: ${{ steps.create-deploy.outputs.deployment_id }}
          state: ${{ job.status }}
          environment-url: https://finsaight.example.com
```

---

## 40. Complete Production Pipeline

```yaml
# .github/workflows/production-pipeline.yml
name: Complete Production Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  PYTHON_VERSION: "3.10"
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ═══════════════════════════════
  # STAGE 1 — CODE QUALITY (parallel)
  # ═══════════════════════════════
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install ruff black
      - run: ruff check src/ && black --check src/

  typecheck:
    name: Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install mypy -r requirements.txt
      - run: mypy src/ --ignore-missing-imports

  # ═══════════════════════════════
  # STAGE 2 — TESTS (parallel)
  # ═══════════════════════════════
  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: [lint]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/unit/ --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: [lint]
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/integration/ -v
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/testdb

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install safety bandit
      - run: safety check -r requirements.txt || true
      - run: bandit -r src/ -ll

  # ═══════════════════════════════
  # STAGE 3 — BUILD
  # ═══════════════════════════════
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}

    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,format=short
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ═══════════════════════════════
  # STAGE 4 — DEPLOY STAGING
  # ═══════════════════════════════
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build]
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.finsaight.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions-staging
          aws-region: eu-west-1

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name finsaight-staging --region eu-west-1

      - name: Deploy to staging
        run: |
          kubectl set image deployment/finsaight-api \
            api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-$(echo ${{ github.sha }} | head -c 7) \
            -n finsaight

          kubectl rollout status deployment/finsaight-api \
            -n finsaight --timeout=300s

  # ═══════════════════════════════
  # STAGE 5 — SMOKE TESTS
  # ═══════════════════════════════
  smoke-tests:
    name: Smoke Tests on Staging
    runs-on: ubuntu-latest
    needs: [deploy-staging]

    steps:
      - uses: actions/checkout@v4

      - name: Run smoke tests
        run: |
          sleep 30
          curl -f https://staging.finsaight.example.com/health
          curl -f https://staging.finsaight.example.com/docs
          python tests/smoke/test_api.py
        env:
          API_URL: https://staging.finsaight.example.com
          API_KEY: ${{ secrets.STAGING_API_KEY }}

  # ═══════════════════════════════
  # STAGE 6 — DEPLOY PRODUCTION (with approval)
  # ═══════════════════════════════
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [smoke-tests]
    environment:
      name: production              # requires approval
      url: https://finsaight.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::${{ secrets.AWS_ACCOUNT_ID }}:role/github-actions-production
          aws-region: eu-west-1

      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name finsaight-production --region eu-west-1

      - name: Deploy to production
        run: |
          kubectl set image deployment/finsaight-api \
            api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-$(echo ${{ github.sha }} | head -c 7) \
            -n finsaight

          kubectl rollout status deployment/finsaight-api \
            -n finsaight --timeout=300s

      - name: Tag release
        run: |
          git tag "release-$(date +%Y%m%d)-${{ github.run_number }}"
          git push origin --tags

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1.27.0
        with:
          channel-id: deployments
          slack-message: "✅ Deployed to production — ${{ github.sha }}"
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

---

## 41. Cheat Sheet

```yaml
# ── WORKFLOW STRUCTURE ────────────────────────────────────────
name: Workflow Name
on: [push, pull_request]
env:
  KEY: value
jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "hello"

# ── COMMON TRIGGERS ───────────────────────────────────────────
on:
  push:
    branches: [main]
    paths: ["src/**"]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * *"
  workflow_dispatch:
    inputs:
      env:
        type: choice
        options: [staging, production]
  release:
    types: [published]

# ── COMMON STEPS ──────────────────────────────────────────────
- uses: actions/checkout@v4
- uses: actions/setup-python@v5
  with:
    python-version: "3.10"
    cache: pip
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
- uses: actions/upload-artifact@v4
  with:
    name: results
    path: reports/
- uses: actions/download-artifact@v4
  with:
    name: results

# ── CONTEXTS ──────────────────────────────────────────────────
${{ github.sha }}              # commit SHA
${{ github.ref_name }}         # branch name
${{ github.actor }}            # who triggered
${{ github.repository }}       # owner/repo
${{ github.event_name }}       # push | pull_request | etc
${{ secrets.MY_SECRET }}       # secret value
${{ inputs.my_input }}         # workflow_dispatch input
${{ needs.JOB.outputs.KEY }}   # output from another job
${{ steps.STEP.outputs.KEY }}  # output from another step
${{ runner.os }}               # Linux | Windows | macOS
${{ matrix.python-version }}   # matrix variable

# ── COMMON CONDITIONS ─────────────────────────────────────────
if: github.ref == 'refs/heads/main'
if: github.event_name == 'push'
if: success()
if: failure()
if: always()
if: contains(github.ref, 'release')
if: github.event_name != 'pull_request'

# ── SET OUTPUTS ───────────────────────────────────────────────
- id: my-step
  run: echo "value=hello" >> $GITHUB_OUTPUT
- run: echo "MY_VAR=hello" >> $GITHUB_ENV      # env for next steps
- run: echo "path" >> $GITHUB_PATH             # add to PATH

# ── DOCKER PATTERN ────────────────────────────────────────────
- uses: docker/setup-buildx-action@v3
- uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
- uses: docker/metadata-action@v5
  id: meta
  with:
    images: ghcr.io/${{ github.repository }}
- uses: docker/build-push-action@v5
  with:
    push: true
    tags: ${{ steps.meta.outputs.tags }}
    cache-from: type=gha
    cache-to: type=gha,mode=max

# ── DEPLOYMENT PLATFORMS ──────────────────────────────────────
# AWS ECS
- uses: aws-actions/configure-aws-credentials@v4
- uses: aws-actions/amazon-ecr-login@v2
- uses: aws-actions/amazon-ecs-deploy-task-definition@v1

# AWS EKS
- run: aws eks update-kubeconfig --name CLUSTER --region REGION
- run: kubectl set image deployment/NAME container=IMAGE

# GCP Cloud Run
- uses: google-github-actions/auth@v2
- uses: google-github-actions/deploy-cloudrun@v2

# Azure Container Apps
- uses: azure/login@v2
- uses: azure/container-apps-deploy-action@v2

# Kubernetes (generic)
- uses: azure/k8s-set-context@v4
  with:
    kubeconfig: ${{ secrets.KUBE_CONFIG }}
- run: kubectl rollout status deployment/NAME

# VPS via SSH
- uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.VPS_HOST }}
    username: ${{ secrets.VPS_USER }}
    key: ${{ secrets.VPS_SSH_KEY }}
    script: |
      docker compose pull && docker compose up -d

# ── NOTIFICATIONS ─────────────────────────────────────────────
# Slack
- uses: slackapi/slack-github-action@v1.27.0
  with:
    channel-id: deployments
    slack-message: "✅ Deployed ${{ github.sha }}"
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}

# PR comment
- uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.createComment({
        issue_number: context.issue.number,
        owner: context.repo.owner,
        repo: context.repo.repo,
        body: '✅ All checks passed!'
      })
```

---

*GitHub Actions docs: https://docs.github.com/en/actions*  
*Workflow syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions*  
*Actions Marketplace: https://github.com/marketplace?type=actions*  
*GitHub Actions Security: https://docs.github.com/en/actions/security-guides*  
*OIDC with AWS: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services*  
*OIDC with GCP: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform*