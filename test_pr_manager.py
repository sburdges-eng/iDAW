#!/usr/bin/env python3
"""
Test suite for PR Manager

This script tests the PR manager functionality in a controlled environment.
"""

import os
import sys
import tempfile
import shutil
import subprocess
from pathlib import Path


class PRManagerTester:
    """Test harness for PR Manager."""
    
    def __init__(self):
        self.test_dir = None
        self.passed = 0
        self.failed = 0
        # Get the directory where this script is located
        self.script_dir = Path(__file__).parent.absolute()
        
    def setup_test_repo(self):
        """Create a temporary test repository."""
        print("🔧 Setting up test repository...")
        self.test_dir = tempfile.mkdtemp(prefix="pr_manager_test_")
        print(f"   Test directory: {self.test_dir}")
        
        os.chdir(self.test_dir)
        
        # Initialize git repo
        subprocess.run(["git", "init"], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
        
        # Create initial commit
        Path("README.md").write_text("# Test Repo\n")
        subprocess.run(["git", "add", "README.md"], check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
        
        print("✓ Test repository created")
        
    def cleanup(self):
        """Clean up test repository."""
        if self.test_dir and os.path.exists(self.test_dir):
            os.chdir("/")
            shutil.rmtree(self.test_dir)
            print(f"🧹 Cleaned up test directory")
    
    def test_import(self):
        """Test that pr_manager can be imported."""
        print("\n📦 Test: Import pr_manager module")
        try:
            sys.path.insert(0, str(self.script_dir))
            import pr_manager
            print("✓ Module imported successfully")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Failed to import: {e}")
            self.failed += 1
            return False
    
    def test_classes(self):
        """Test that required classes exist."""
        print("\n🏗️  Test: Check class definitions")
        try:
            import pr_manager
            
            # Check classes exist
            assert hasattr(pr_manager, 'MergeStatus')
            assert hasattr(pr_manager, 'PullRequest')
            assert hasattr(pr_manager, 'MergeResult')
            assert hasattr(pr_manager, 'PRManager')
            
            print("✓ All required classes defined")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Class check failed: {e}")
            self.failed += 1
            return False
    
    def test_pr_manager_init(self):
        """Test PRManager initialization."""
        print("\n🎯 Test: PRManager initialization")
        try:
            import pr_manager
            
            # Test basic init
            manager = pr_manager.PRManager()
            assert manager.repo_path == "."
            assert manager.dry_run == False
            assert manager.target_pr is None
            
            # Test with parameters
            manager2 = pr_manager.PRManager(
                repo_path="/tmp",
                dry_run=True,
                target_pr=42
            )
            assert manager2.repo_path == "/tmp"
            assert manager2.dry_run == True
            assert manager2.target_pr == 42
            
            print("✓ PRManager initializes correctly")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Initialization test failed: {e}")
            self.failed += 1
            return False
    
    def test_git_command(self):
        """Test git command execution."""
        print("\n💻 Test: Git command execution")
        try:
            import pr_manager
            
            self.setup_test_repo()
            manager = pr_manager.PRManager(repo_path=self.test_dir)
            
            # Test successful command
            exit_code, stdout, stderr = manager.run_git_command(
                ["status", "--porcelain"],
                check=False
            )
            assert exit_code == 0
            
            # Test current branch
            exit_code, stdout, stderr = manager.run_git_command(
                ["branch", "--show-current"],
                check=False
            )
            assert exit_code == 0
            assert stdout in ["master", "main"]
            
            print("✓ Git commands execute correctly")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Git command test failed: {e}")
            self.failed += 1
            return False
        finally:
            self.cleanup()
    
    def test_dataclasses(self):
        """Test dataclass creation."""
        print("\n📋 Test: Dataclass creation")
        try:
            import pr_manager
            
            # Create PullRequest
            pr = pr_manager.PullRequest(
                number=1,
                title="Test PR",
                head_ref="feature",
                base_ref="main",
                head_sha="abc123",
                mergeable=True,
                url="https://github.com/test/test/pull/1"
            )
            assert pr.number == 1
            assert pr.title == "Test PR"
            
            # Create MergeResult
            result = pr_manager.MergeResult(
                pr=pr,
                status=pr_manager.MergeStatus.SUCCESS,
                conflicting_files=[]
            )
            assert result.status == pr_manager.MergeStatus.SUCCESS
            assert len(result.conflicting_files) == 0
            
            print("✓ Dataclasses work correctly")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Dataclass test failed: {e}")
            self.failed += 1
            return False
    
    def test_merge_status_enum(self):
        """Test MergeStatus enum."""
        print("\n🔢 Test: MergeStatus enum")
        try:
            import pr_manager
            
            assert pr_manager.MergeStatus.SUCCESS.value == "success"
            assert pr_manager.MergeStatus.CONFLICT.value == "conflict"
            assert pr_manager.MergeStatus.ERROR.value == "error"
            
            print("✓ MergeStatus enum values correct")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Enum test failed: {e}")
            self.failed += 1
            return False
    
    def test_script_execution(self):
        """Test that the script can be executed."""
        print("\n🚀 Test: Script execution")
        try:
            pr_manager_path = self.script_dir / "pr_manager.py"
            result = subprocess.run(
                ["python3", str(pr_manager_path), "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            assert result.returncode == 0
            assert "PR Management Agent" in result.stdout
            assert "--dry-run" in result.stdout
            assert "--pr" in result.stdout
            
            print("✓ Script executes and shows help")
            self.passed += 1
            return True
        except Exception as e:
            print(f"✗ Script execution test failed: {e}")
            self.failed += 1
            return False
    
    def run_all_tests(self):
        """Run all tests."""
        print("="*60)
        print("PR Manager Test Suite")
        print("="*60)
        
        # Run tests
        self.test_import()
        self.test_classes()
        self.test_dataclasses()
        self.test_merge_status_enum()
        self.test_pr_manager_init()
        self.test_git_command()
        self.test_script_execution()
        
        # Print summary
        print("\n" + "="*60)
        print("Test Summary")
        print("="*60)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        total = self.passed + self.failed
        if total > 0:
            percentage = (self.passed / total) * 100
            print(f"📊 Success Rate: {percentage:.1f}%")
        print("="*60)
        
        return 0 if self.failed == 0 else 1


def main():
    """Main entry point."""
    tester = PRManagerTester()
    try:
        return tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        tester.cleanup()


if __name__ == "__main__":
    sys.exit(main())
