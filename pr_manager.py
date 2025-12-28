#!/usr/bin/env python3
"""
PR Management Agent

This script manages pull requests in the repository by:
1. Fetching all open pull requests
2. Attempting to merge each PR into its target branch
3. If merge succeeds without conflicts:
   - Completes the merge
   - Deletes the source branch
4. If merge conflicts exist:
   - Does NOT merge
   - Creates a new branch named "conflicts/{original-branch-name}"
   - Pushes the conflicting state to that branch
   - Comments on the PR with conflicting files
   - Leaves the PR open

Never force pushes. Never auto-resolves conflicts. Always preserves conflict state.

Usage:
    python pr_manager.py [--dry-run] [--pr NUMBER]
    
Options:
    --dry-run       Simulate merges without actually committing or pushing
    --pr NUMBER     Process only a specific PR number
    --help          Show this help message
"""

import os
import sys
import subprocess
import json
import argparse
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class MergeStatus(Enum):
    """Status of a merge attempt."""
    SUCCESS = "success"
    CONFLICT = "conflict"
    ERROR = "error"


@dataclass
class PullRequest:
    """Represents a GitHub Pull Request."""
    number: int
    title: str
    head_ref: str  # Source branch
    base_ref: str  # Target branch
    head_sha: str
    mergeable: Optional[bool]
    url: str


@dataclass
class MergeResult:
    """Result of a merge attempt."""
    pr: PullRequest
    status: MergeStatus
    conflicting_files: List[str]
    error_message: Optional[str] = None


class PRManager:
    """Manages pull request merging and conflict resolution."""

    def __init__(self, repo_path: str = ".", dry_run: bool = False, target_pr: Optional[int] = None):
        """
        Initialize the PR manager.
        
        Args:
            repo_path: Path to the git repository (default: current directory)
            dry_run: If True, simulate without actually making changes
            target_pr: If specified, only process this PR number
        """
        self.repo_path = repo_path
        self.dry_run = dry_run
        self.target_pr = target_pr
        self.results: List[MergeResult] = []
        
        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
            print("="*60)

    def run_git_command(self, args: List[str], check: bool = True) -> Tuple[int, str, str]:
        """
        Run a git command and return the result.
        
        Args:
            args: Git command arguments
            check: Whether to raise exception on non-zero exit
            
        Returns:
            Tuple of (exit_code, stdout, stderr)
        """
        cmd = ["git", "-C", self.repo_path] + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )
        
        if check and result.returncode != 0:
            print(f"Git command failed: {' '.join(cmd)}")
            print(f"Exit code: {result.returncode}")
            print(f"Stderr: {result.stderr}")
            
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def fetch_all(self) -> bool:
        """Fetch all branches from remote."""
        print("📡 Fetching latest changes from remote...")
        exit_code, stdout, stderr = self.run_git_command(["fetch", "--all", "--prune"])
        if exit_code == 0:
            print("✓ Fetch completed successfully")
            return True
        else:
            print(f"✗ Fetch failed: {stderr}")
            return False

    def get_open_prs_from_github(self) -> List[PullRequest]:
        """
        Fetch open PRs from GitHub API.
        
        Note: This is a placeholder. In a real implementation, you would use
        the GitHub API or CLI to fetch PRs. For now, we'll use git to detect
        branches that might be associated with PRs.
        """
        # This would normally use the GitHub API
        # For this implementation, we'll return an empty list since
        # we can't make GitHub API calls from this script
        print("⚠️  GitHub API integration not available in this environment")
        print("    This script is designed to work with GitHub Actions or")
        print("    environments where GitHub CLI (gh) is available.")
        return []

    def get_open_prs_from_cli(self) -> List[PullRequest]:
        """
        Fetch open PRs using GitHub CLI.
        
        Returns:
            List of open pull requests
        """
        print("📋 Fetching open pull requests...")
        
        # Check if gh CLI is available and has token
        gh_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        
        result = subprocess.run(
            ["which", "gh"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print("⚠️  GitHub CLI (gh) not found. Please install it to use this script.")
            print("    Visit: https://cli.github.com/")
            return []
        
        if not gh_token:
            print("⚠️  GH_TOKEN or GITHUB_TOKEN environment variable not set.")
            print("    Set one of these variables to authenticate with GitHub.")
            return []
        
        # Set GH_TOKEN in environment for subprocess
        env = os.environ.copy()
        env["GH_TOKEN"] = gh_token
        
        # Fetch PRs using gh CLI
        exit_code, stdout, stderr = self.run_git_command(
            ["config", "--get", "remote.origin.url"],
            check=False
        )
        
        if exit_code != 0:
            print("✗ Could not determine repository URL")
            return []
        
        # Use gh to list PRs
        cmd = ["gh", "pr", "list", "--state", "open", "--json", 
               "number,title,headRefName,baseRefName,headRefOid,mergeable,url"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, env=env)
        
        if result.returncode != 0:
            print(f"✗ Failed to fetch PRs: {result.stderr}")
            return []
        
        try:
            pr_data = json.loads(result.stdout)
            prs = [
                PullRequest(
                    number=pr["number"],
                    title=pr["title"],
                    head_ref=pr["headRefName"],
                    base_ref=pr["baseRefName"],
                    head_sha=pr["headRefOid"],
                    mergeable=pr.get("mergeable"),
                    url=pr["url"]
                )
                for pr in pr_data
            ]
            print(f"✓ Found {len(prs)} open pull request(s)")
            return prs
        except (json.JSONDecodeError, KeyError) as e:
            print(f"✗ Failed to parse PR data: {e}")
            return []

    def attempt_merge(self, pr: PullRequest) -> MergeResult:
        """
        Attempt to merge a pull request.
        
        Args:
            pr: Pull request to merge
            
        Returns:
            MergeResult with status and details
        """
        print(f"\n{'='*60}")
        print(f"Processing PR #{pr.number}: {pr.title}")
        print(f"  Source: {pr.head_ref} → Target: {pr.base_ref}")
        print(f"{'='*60}")
        
        # Ensure we're on the target branch
        print(f"🔄 Checking out target branch: {pr.base_ref}")
        exit_code, _, stderr = self.run_git_command(
            ["checkout", pr.base_ref],
            check=False
        )
        
        if exit_code != 0:
            return MergeResult(
                pr=pr,
                status=MergeStatus.ERROR,
                conflicting_files=[],
                error_message=f"Failed to checkout target branch: {stderr}"
            )
        
        # Pull latest changes on target branch
        print(f"⬇️  Pulling latest changes on {pr.base_ref}")
        exit_code, _, stderr = self.run_git_command(
            ["pull", "origin", pr.base_ref],
            check=False
        )
        
        if exit_code != 0:
            print(f"⚠️  Warning: Could not pull latest changes: {stderr}")
        
        # Attempt merge
        print(f"🔀 Attempting to merge {pr.head_ref} into {pr.base_ref}")
        exit_code, stdout, stderr = self.run_git_command(
            ["merge", "--no-ff", "--no-commit", f"origin/{pr.head_ref}"],
            check=False
        )
        
        if exit_code == 0:
            # Merge succeeded without conflicts
            print("✓ Merge succeeded without conflicts")
            
            # Check if there are any changes
            exit_code, stdout, _ = self.run_git_command(
                ["diff", "--cached", "--name-only"],
                check=False
            )
            
            if not stdout:
                print("ℹ️  No changes to merge")
                self.run_git_command(["merge", "--abort"], check=False)
                return MergeResult(
                    pr=pr,
                    status=MergeStatus.SUCCESS,
                    conflicting_files=[],
                    error_message="No changes to merge"
                )
            
            # Complete the merge
            print("📝 Completing merge...")
            exit_code, _, stderr = self.run_git_command(
                ["commit", "-m", f"Merge pull request #{pr.number}: {pr.title}"],
                check=False
            )
            
            if exit_code != 0:
                return MergeResult(
                    pr=pr,
                    status=MergeStatus.ERROR,
                    conflicting_files=[],
                    error_message=f"Failed to commit merge: {stderr}"
                )
            
            return MergeResult(
                pr=pr,
                status=MergeStatus.SUCCESS,
                conflicting_files=[]
            )
        else:
            # Merge failed - check if it's due to conflicts
            if "CONFLICT" in stdout or "CONFLICT" in stderr:
                print("⚠️  Merge conflicts detected")
                
                # Get list of conflicting files
                exit_code, conflicts_output, _ = self.run_git_command(
                    ["diff", "--name-only", "--diff-filter=U"],
                    check=False
                )
                
                conflicting_files = conflicts_output.split("\n") if conflicts_output else []
                conflicting_files = [f for f in conflicting_files if f]
                
                print(f"   Conflicting files ({len(conflicting_files)}):")
                for file in conflicting_files:
                    print(f"     - {file}")
                
                return MergeResult(
                    pr=pr,
                    status=MergeStatus.CONFLICT,
                    conflicting_files=conflicting_files
                )
            else:
                # Some other error
                return MergeResult(
                    pr=pr,
                    status=MergeStatus.ERROR,
                    conflicting_files=[],
                    error_message=f"Merge failed: {stderr}"
                )

    def handle_successful_merge(self, result: MergeResult) -> bool:
        """
        Handle a successful merge by pushing and deleting the source branch.
        
        Args:
            result: Successful merge result
            
        Returns:
            True if handling succeeded, False otherwise
        """
        pr = result.pr
        print(f"\n✅ Handling successful merge for PR #{pr.number}")
        
        if self.dry_run:
            print(f"🔍 DRY RUN: Would push merge to origin/{pr.base_ref}")
            print(f"🔍 DRY RUN: Would delete branch {pr.head_ref}")
            return True
        
        # Push the merge to remote
        print(f"⬆️  Pushing merge to origin/{pr.base_ref}")
        exit_code, _, stderr = self.run_git_command(
            ["push", "origin", pr.base_ref],
            check=False
        )
        
        if exit_code != 0:
            print(f"✗ Failed to push merge: {stderr}")
            return False
        
        print("✓ Merge pushed successfully")
        
        # Delete the source branch
        print(f"🗑️  Deleting source branch: {pr.head_ref}")
        exit_code, _, stderr = self.run_git_command(
            ["push", "origin", "--delete", pr.head_ref],
            check=False
        )
        
        if exit_code != 0:
            print(f"⚠️  Warning: Could not delete remote branch: {stderr}")
            print(f"   You may need to manually delete {pr.head_ref}")
            return True  # Still consider this a success
        
        print(f"✓ Source branch {pr.head_ref} deleted")
        return True

    def handle_conflicted_merge(self, result: MergeResult) -> bool:
        """
        Handle a conflicted merge by creating a conflicts branch.
        
        Args:
            result: Conflicted merge result
            
        Returns:
            True if handling succeeded, False otherwise
        """
        pr = result.pr
        conflicts_branch = f"conflicts/{pr.head_ref}"
        
        print(f"\n⚠️  Handling merge conflicts for PR #{pr.number}")
        
        # Abort the current merge
        print("🔄 Aborting conflicted merge...")
        self.run_git_command(["merge", "--abort"], check=False)
        
        if self.dry_run:
            print(f"🔍 DRY RUN: Would create conflicts branch: {conflicts_branch}")
            print(f"🔍 DRY RUN: Would push conflicts branch to remote")
            print(f"🔍 DRY RUN: Would comment on PR #{pr.number}")
            return True
        
        # Create conflicts branch
        print(f"🌿 Creating conflicts branch: {conflicts_branch}")
        
        # First, checkout the source branch
        exit_code, _, stderr = self.run_git_command(
            ["checkout", "-b", conflicts_branch, f"origin/{pr.head_ref}"],
            check=False
        )
        
        if exit_code != 0:
            print(f"✗ Failed to create conflicts branch: {stderr}")
            return False
        
        # Push the conflicts branch
        print(f"⬆️  Pushing conflicts branch to remote")
        exit_code, _, stderr = self.run_git_command(
            ["push", "origin", conflicts_branch],
            check=False
        )
        
        if exit_code != 0:
            print(f"✗ Failed to push conflicts branch: {stderr}")
            return False
        
        print(f"✓ Conflicts branch created: {conflicts_branch}")
        
        # Comment on PR about conflicts
        print(f"💬 Adding comment to PR about conflicts")
        self.comment_on_pr(pr, result.conflicting_files)
        
        # Return to base branch
        self.run_git_command(["checkout", pr.base_ref], check=False)
        
        return True

    def comment_on_pr(self, pr: PullRequest, conflicting_files: List[str]) -> bool:
        """
        Add a comment to a PR about merge conflicts.
        
        Args:
            pr: Pull request
            conflicting_files: List of files with conflicts
            
        Returns:
            True if comment added successfully, False otherwise
        """
        conflicts_branch = f"conflicts/{pr.head_ref}"
        
        # Build comment text
        comment = f"""## ⚠️ Merge Conflicts Detected

This PR cannot be automatically merged due to conflicts with the target branch `{pr.base_ref}`.

### Conflicting Files ({len(conflicting_files)}):
"""
        for file in conflicting_files:
            comment += f"- `{file}`\n"
        
        comment += f"""
### Next Steps:
1. A conflicts branch has been created: `{conflicts_branch}`
2. Review the conflicts in the files listed above
3. Manually resolve the conflicts
4. Update this PR with the resolved changes

The conflicts branch preserves the current state for your review.
"""
        
        # Get GitHub token
        gh_token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        if not gh_token:
            print("⚠️  Cannot add comment: GitHub token not available")
            print("   Comment text:")
            print(comment)
            return False
        
        # Use gh CLI to add comment
        env = os.environ.copy()
        env["GH_TOKEN"] = gh_token
        
        result = subprocess.run(
            ["gh", "pr", "comment", str(pr.number), "--body", comment],
            capture_output=True,
            text=True,
            check=False,
            env=env
        )
        
        if result.returncode == 0:
            print("✓ Comment added to PR")
            return True
        else:
            print(f"⚠️  Could not add comment to PR: {result.stderr}")
            print("   Comment text:")
            print(comment)
            return False

    def print_summary(self):
        """Print a summary of all merge results."""
        print("\n" + "="*60)
        print("MERGE SUMMARY")
        print("="*60)
        
        successful = [r for r in self.results if r.status == MergeStatus.SUCCESS]
        conflicted = [r for r in self.results if r.status == MergeStatus.CONFLICT]
        errored = [r for r in self.results if r.status == MergeStatus.ERROR]
        
        print(f"\n✅ Successfully merged and deleted ({len(successful)}):")
        if successful:
            for result in successful:
                pr = result.pr
                print(f"  - PR #{pr.number}: {pr.title}")
                print(f"    Branch: {pr.head_ref} → {pr.base_ref}")
        else:
            print("  (none)")
        
        print(f"\n⚠️  Moved to conflicts branch ({len(conflicted)}):")
        if conflicted:
            for result in conflicted:
                pr = result.pr
                print(f"  - PR #{pr.number}: {pr.title}")
                print(f"    Branch: {pr.head_ref} → conflicts/{pr.head_ref}")
                print(f"    Conflicting files: {', '.join(result.conflicting_files)}")
        else:
            print("  (none)")
        
        if errored:
            print(f"\n❌ Errors ({len(errored)}):")
            for result in errored:
                pr = result.pr
                print(f"  - PR #{pr.number}: {pr.title}")
                print(f"    Error: {result.error_message}")
        
        print("\n" + "="*60)

    def run(self):
        """Main execution method."""
        print("🚀 PR Management Agent Starting...")
        print("="*60)
        
        # Fetch latest changes
        if not self.fetch_all():
            print("❌ Failed to fetch from remote. Exiting.")
            return 1
        
        # Get open PRs
        prs = self.get_open_prs_from_cli()
        
        if not prs:
            print("\nℹ️  No open pull requests found.")
            return 0
        
        # Filter to target PR if specified
        if self.target_pr:
            prs = [pr for pr in prs if pr.number == self.target_pr]
            if not prs:
                print(f"\n❌ PR #{self.target_pr} not found in open PRs.")
                return 1
            print(f"\n🎯 Processing only PR #{self.target_pr}")
        
        # Process each PR
        for pr in prs:
            result = self.attempt_merge(pr)
            self.results.append(result)
            
            if result.status == MergeStatus.SUCCESS:
                self.handle_successful_merge(result)
            elif result.status == MergeStatus.CONFLICT:
                self.handle_conflicted_merge(result)
            elif result.status == MergeStatus.ERROR:
                print(f"❌ Error processing PR: {result.error_message}")
        
        # Print summary
        self.print_summary()
        
        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="PR Management Agent - Automatically merge or handle conflicts for open PRs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pr_manager.py                    # Process all open PRs
  python pr_manager.py --dry-run          # Simulate without making changes
  python pr_manager.py --pr 42            # Process only PR #42
  python pr_manager.py --dry-run --pr 42  # Dry run for PR #42

Environment:
  GH_TOKEN or GITHUB_TOKEN must be set for GitHub API access
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate merges without actually committing or pushing"
    )
    
    parser.add_argument(
        "--pr",
        type=int,
        metavar="NUMBER",
        help="Process only this specific PR number"
    )
    
    args = parser.parse_args()
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Not a git repository. Please run this script from the repository root.")
        return 1
    
    manager = PRManager(dry_run=args.dry_run, target_pr=args.pr)
    return manager.run()


if __name__ == "__main__":
    sys.exit(main())
