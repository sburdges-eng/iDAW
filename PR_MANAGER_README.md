# PR Management Agent

An automated tool for managing pull requests in the iDAW repository.

## Overview

The PR Management Agent (`pr_manager.py`) automatically processes open pull requests by:

1. **Fetching** the latest changes from remote
2. **Attempting to merge** each PR into its target branch
3. **On successful merge:**
   - Completes the merge with a commit
   - Pushes the merge to the target branch
   - Deletes the source branch
4. **On merge conflicts:**
   - Does NOT merge (preserves safety)
   - Creates a `conflicts/{branch-name}` branch
   - Pushes the conflicting state for review
   - Comments on the PR listing conflicting files
   - Leaves the PR open for manual resolution

## Key Features

✅ **Safe** - Never force pushes, never auto-resolves conflicts  
✅ **Transparent** - Detailed logging of every action  
✅ **Preserves state** - Conflict branches keep original state  
✅ **Automated** - Can process all open PRs sequentially  
✅ **Flexible** - Dry-run mode and single-PR targeting  

## Requirements

- Python 3.7+
- Git
- GitHub CLI (`gh`) installed and authenticated
- `GH_TOKEN` or `GITHUB_TOKEN` environment variable set

### Installing GitHub CLI

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install gh

# Fedora/RHEL
sudo dnf install gh
```

**Windows:**
```bash
# Using winget
winget install --id GitHub.cli

# Using scoop
scoop install gh
```

### Authenticating GitHub CLI

```bash
gh auth login
```

Or set a personal access token:
```bash
export GH_TOKEN=your_token_here
```

## Usage

### Basic Usage

Process all open PRs:
```bash
python pr_manager.py
```

### Dry Run Mode

Simulate what would happen without making changes:
```bash
python pr_manager.py --dry-run
```

This is useful for:
- Testing the script
- Previewing which PRs would merge successfully
- Understanding potential conflicts before execution

### Process Specific PR

Target a single PR by number:
```bash
python pr_manager.py --pr 42
```

Combine with dry-run:
```bash
python pr_manager.py --dry-run --pr 42
```

### Help

```bash
python pr_manager.py --help
```

## Output Examples

### Successful Merge

```
🚀 PR Management Agent Starting...
============================================================
📡 Fetching latest changes from remote...
✓ Fetch completed successfully
📋 Fetching open pull requests...
✓ Found 2 open pull request(s)

============================================================
Processing PR #42: Add new feature
  Source: feature/new-thing → Target: main
============================================================
🔄 Checking out target branch: main
⬇️  Pulling latest changes on main
🔀 Attempting to merge feature/new-thing into main
✓ Merge succeeded without conflicts
📝 Completing merge...

✅ Handling successful merge for PR #42
⬆️  Pushing merge to origin/main
✓ Merge pushed successfully
🗑️  Deleting source branch: feature/new-thing
✓ Source branch feature/new-thing deleted
```

### Conflict Detection

```
============================================================
Processing PR #43: Update documentation
  Source: docs-update → Target: main
============================================================
🔄 Checking out target branch: main
⬇️  Pulling latest changes on main
🔀 Attempting to merge docs-update into main
⚠️  Merge conflicts detected
   Conflicting files (2):
     - README.md
     - docs/guide.md

⚠️  Handling merge conflicts for PR #43
🔄 Aborting conflicted merge...
🌿 Creating conflicts branch: conflicts/docs-update
⬆️  Pushing conflicts branch to remote
✓ Conflicts branch created: conflicts/docs-update
💬 Adding comment to PR about conflicts
✓ Comment added to PR
```

### Summary Report

```
============================================================
MERGE SUMMARY
============================================================

✅ Successfully merged and deleted (1):
  - PR #42: Add new feature
    Branch: feature/new-thing → main

⚠️  Moved to conflicts branch (1):
  - PR #43: Update documentation
    Branch: docs-update → conflicts/docs-update
    Conflicting files: README.md, docs/guide.md

============================================================
```

## Workflow Integration

### GitHub Actions

Create `.github/workflows/auto-merge-prs.yml`:

```yaml
name: Auto-merge PRs

on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:  # Manual trigger

jobs:
  merge-prs:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          
      - name: Install GitHub CLI
        run: |
          type -p gh > /dev/null || sudo apt-get install gh -y
          
      - name: Run PR Manager
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          python pr_manager.py
```

### Manual Cron Job

Add to crontab:
```bash
0 */6 * * * cd /path/to/iDAW && GH_TOKEN=your_token python pr_manager.py >> pr_manager.log 2>&1
```

## How It Works

### 1. Fetch Phase
- Runs `git fetch --all --prune`
- Ensures all remote branches are up-to-date locally

### 2. PR Discovery Phase
- Uses `gh pr list` to fetch open PRs
- Extracts: number, title, source branch, target branch, HEAD SHA

### 3. Merge Attempt Phase
For each PR:
- Checks out the target branch
- Pulls latest changes
- Attempts merge with `git merge --no-ff --no-commit`
- Checks for conflicts

### 4. Success Path
- Commits the merge
- Pushes to target branch
- Deletes source branch with `git push origin --delete`

### 5. Conflict Path
- Aborts the merge
- Creates `conflicts/{branch}` from source branch
- Pushes conflicts branch
- Comments on PR with file list
- Returns to target branch

## Safety Guarantees

1. **No Force Push** - Never uses `--force` or `--force-with-lease`
2. **No Auto-Resolve** - Never modifies conflicting files
3. **Preserves State** - Conflicts branch = exact copy of source
4. **Rollback Safe** - Original branches remain until successfully merged
5. **Audit Trail** - Comprehensive logging of every action

## Troubleshooting

### "gh: command not found"
Install GitHub CLI (see Requirements section)

### "GH_TOKEN environment variable not set"
```bash
export GH_TOKEN=$(gh auth token)
# or
export GITHUB_TOKEN=your_personal_access_token
```

### "Failed to fetch PRs"
Ensure `gh` is authenticated:
```bash
gh auth status
gh auth refresh
```

### "Not a git repository"
Run from the repository root:
```bash
cd /path/to/iDAW
python pr_manager.py
```

### Permission Errors
Ensure your GitHub token has:
- `repo` scope (full repository access)
- `write:packages` if using GitHub Packages
- `workflow` if triggering workflows

## Advanced Usage

### Filtering PRs Before Processing

```bash
# Only process PRs with specific label
gh pr list --label "ready-to-merge" --json number -q '.[].number' | while read pr; do
  python pr_manager.py --pr $pr
done
```

### Integration with CI/CD

The script returns exit codes:
- `0` - Success (all PRs processed)
- `1` - Error (failed to process one or more PRs)

Use in scripts:
```bash
if python pr_manager.py; then
  echo "All PRs processed successfully"
else
  echo "Some PRs failed to process"
  exit 1
fi
```

### Custom Conflict Comment

Edit the `comment_on_pr()` method in `pr_manager.py` to customize the message posted on conflicting PRs.

## Architecture

```
PRManager
├── run()                          # Main orchestrator
├── fetch_all()                    # Git fetch
├── get_open_prs_from_cli()       # PR discovery via gh CLI
├── attempt_merge()                # Merge attempt with conflict detection
├── handle_successful_merge()      # Push & delete on success
├── handle_conflicted_merge()      # Create conflicts branch
├── comment_on_pr()                # Add PR comment
└── print_summary()                # Final report
```

## Contributing

To modify the PR manager:

1. Test changes with `--dry-run` first
2. Add new features as separate methods
3. Maintain comprehensive logging
4. Never compromise safety guarantees

## License

Same as the parent iDAW project (MIT).

## Support

For issues or questions:
- Open an issue in the iDAW repository
- Tag `@sburdges-eng`
- Include the full output from `--dry-run` mode
