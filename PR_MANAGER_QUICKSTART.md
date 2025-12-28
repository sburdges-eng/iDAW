# PR Manager Quick Start Guide

Get the PR management agent running in 5 minutes.

## Prerequisites Checklist

- [ ] Python 3.7+ installed
- [ ] Git installed and configured
- [ ] GitHub CLI (`gh`) installed
- [ ] Repository cloned locally

## Step 1: Install GitHub CLI

**macOS:**
```bash
brew install gh
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install gh
```

**Windows:**
```powershell
winget install --id GitHub.cli
```

## Step 2: Authenticate

```bash
gh auth login
```

Follow the prompts to authenticate with GitHub.

## Step 3: Set Environment Variable

**Option A: Use current auth**
```bash
export GH_TOKEN=$(gh auth token)
```

**Option B: Use personal access token**
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

## Step 4: Test with Dry Run

From the repository root:

```bash
python pr_manager.py --dry-run
```

You should see output like:
```
🔍 DRY RUN MODE - No changes will be made
============================================================
🚀 PR Management Agent Starting...
============================================================
📡 Fetching latest changes from remote...
✓ Fetch completed successfully
📋 Fetching open pull requests...
✓ Found X open pull request(s)
```

## Step 5: Process PRs

Once you're comfortable with the dry run output:

```bash
python pr_manager.py
```

## Common First-Time Issues

### "gh: command not found"
**Solution:** Install GitHub CLI (see Step 1)

### "GH_TOKEN environment variable not set"
**Solution:** Set the token (see Step 3)

### "Failed to fetch PRs: ... authentication required"
**Solution:** Run `gh auth login` again

### "Not a git repository"
**Solution:** Navigate to the repository root:
```bash
cd /path/to/iDAW
```

## Testing the Script

Run the test suite:
```bash
python test_pr_manager.py
```

Expected output:
```
✅ Passed: 7
❌ Failed: 0
📊 Success Rate: 100.0%
```

## Next Steps

1. **Automate with cron** (see PR_MANAGER_README.md)
2. **Set up GitHub Actions** (see .github/workflows/auto-merge-prs.yml)
3. **Customize conflict messages** (edit comment_on_pr() in pr_manager.py)

## Need Help?

- Read the full documentation: `PR_MANAGER_README.md`
- Check workflow file: `.github/workflows/auto-merge-prs.yml`
- Run tests: `python test_pr_manager.py`
- Open an issue in the repository

## Troubleshooting Commands

```bash
# Check gh is installed
gh --version

# Check gh auth status
gh auth status

# List current PRs
gh pr list

# View git remote
git remote -v

# Check current branch
git branch --show-current
```

## Success! What Now?

Once the script runs successfully:

1. Review the merge summary
2. Check merged PRs are closed
3. Verify conflict branches were created for conflicting PRs
4. Review PR comments on conflicted PRs

Happy merging! 🎉
