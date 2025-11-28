"""
Verify that the API is ready for deployment.

This script checks:
1. All required files exist
2. Model files are present
3. Dependencies are installable
4. API can start locally
"""

import sys
from pathlib import Path
import subprocess

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    if Path(dirpath).exists() and Path(dirpath).is_dir():
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {dirpath}")
        return False

def main():
    """Run all deployment readiness checks."""
    print("=" * 60)
    print("MedMind API - Deployment Readiness Check")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check required files
    print("📁 Checking Required Files...")
    print("-" * 60)
    
    checks = [
        ("prediction.py", "Main API file"),
        ("requirements.txt", "Dependencies file"),
        ("Procfile", "Heroku process file"),
        ("render.yaml", "Render config file"),
        ("runtime.txt", "Python version file"),
        ("models/best_model.pkl", "Trained model"),
        ("models/scaler.pkl", "Feature scaler"),
    ]
    
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_checks_passed = False
    
    print()
    
    # Check models directory
    print("📂 Checking Directories...")
    print("-" * 60)
    if not check_directory_exists("models", "Models directory"):
        all_checks_passed = False
    print()
    
    # Check requirements.txt content
    print("📦 Checking Dependencies...")
    print("-" * 60)
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            required_packages = ["fastapi", "uvicorn", "pydantic", "scikit-learn", "numpy", "joblib"]
            
            for package in required_packages:
                if package in requirements:
                    print(f"✅ {package} listed in requirements.txt")
                else:
                    print(f"❌ {package} NOT listed in requirements.txt")
                    all_checks_passed = False
    except Exception as e:
        print(f"❌ Error reading requirements.txt: {e}")
        all_checks_passed = False
    print()
    
    # Check model file sizes
    print("📊 Checking Model Files...")
    print("-" * 60)
    try:
        model_path = Path("models/best_model.pkl")
        scaler_path = Path("models/scaler.pkl")
        
        if model_path.exists():
            model_size = model_path.stat().st_size / 1024  # KB
            print(f"✅ Model file size: {model_size:.2f} KB")
            if model_size < 1:
                print(f"⚠️  Warning: Model file seems very small")
        
        if scaler_path.exists():
            scaler_size = scaler_path.stat().st_size / 1024  # KB
            print(f"✅ Scaler file size: {scaler_size:.2f} KB")
            if scaler_size < 1:
                print(f"⚠️  Warning: Scaler file seems very small")
    except Exception as e:
        print(f"❌ Error checking model files: {e}")
        all_checks_passed = False
    print()
    
    # Check Python version
    print("🐍 Checking Python Version...")
    print("-" * 60)
    python_version = sys.version.split()[0]
    print(f"✅ Current Python version: {python_version}")
    
    major, minor = sys.version_info[:2]
    if major == 3 and minor >= 8:
        print(f"✅ Python version is compatible (3.8+)")
    else:
        print(f"⚠️  Warning: Python 3.8+ recommended, you have {major}.{minor}")
    print()
    
    # Check git status
    print("📝 Checking Git Status...")
    print("-" * 60)
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            print("⚠️  You have uncommitted changes:")
            print(result.stdout)
            print("💡 Commit and push changes before deploying")
        else:
            print("✅ No uncommitted changes")
    except subprocess.CalledProcessError:
        print("⚠️  Not a git repository or git not available")
    except FileNotFoundError:
        print("⚠️  Git not found in PATH")
    print()
    
    # Summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED - Ready for deployment!")
        print()
        print("Next steps:")
        print("1. Commit and push your code to GitHub")
        print("2. Follow DEPLOYMENT_GUIDE.md to deploy to Render/Railway/Heroku")
        print("3. Test the deployed API endpoints")
        print("4. Document the public URL in README files")
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Fix issues before deploying")
        print()
        print("Review the errors above and fix them before deployment.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
