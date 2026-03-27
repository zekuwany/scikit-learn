import subprocess
import os
import sys

# Configuration
REPO_URL = "https://github.com/zekuwany/scikit-learn.git"
REPO_NAME = "scikit-learn"
ENV_NAME = "r-reticulate"

def run_command(cmd, check=True):
    """Run shell command and print output"""
    print(f"\n>>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and check:
        print(result.stderr, file=sys.stderr)
    return result

def main():
    # 1. Activate conda environment
    print("=" * 50)
    print("🚀 Starting Automated Analysis")
    print("=" * 50)
    
    # Check if in conda environment
    if not os.environ.get("CONDA_DEFAULT_ENV") == ENV_NAME:
        print(f"⚠️  Please activate {ENV_NAME} first:")
        print(f"   conda activate {ENV_NAME}")
        print(f"   python run_analysis.py")
        return
    
    # 2. Clone or update repository
    if os.path.exists(REPO_NAME):
        print(f"\n📁 Repository exists, updating...")
        os.chdir(REPO_NAME)
        run_command("git pull")
    else:
        print(f"\n📥 Cloning repository...")
        run_command(f"git clone {REPO_URL}")
        os.chdir(REPO_NAME)
    
    # 3. Create analysis script in repository
    analysis_code = '''
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import json
from datetime import datetime

print("📊 Running Random Forest Analysis...")

# Generate data
X, y = make_classification(n_samples=1000, n_features=4, 
                           n_informative=2, n_redundant=0,
                           random_state=42)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train, y_train)

# Evaluate
accuracy = rf.score(X_test, y_test)
print(f"✓ Accuracy: {accuracy:.4f}")

# Save results
import os
os.makedirs("outputs", exist_ok=True)

results = {
    "timestamp": datetime.now().isoformat(),
    "accuracy": accuracy,
    "feature_importance": rf.feature_importances_.tolist()
}

with open("outputs/results.json", "w") as f:
    json.dump(results, f, indent=2)

joblib.dump(rf, "outputs/model.joblib")
print("✓ Results saved to outputs/")
print(f"✓ Model saved to outputs/model.joblib")
'''
    
    # Save analysis script
    with open("run_analysis.py", "w") as f:
        f.write(analysis_code)
    
    # 4. Run the analysis
    print("\n🔬 Running analysis...")
    run_command("python run_analysis.py")
    
    # 5. Show results
    if os.path.exists("outputs/results.json"):
        print("\n📈 Results:")
        run_command("type outputs\\results.json" if os.name == "nt" else "cat outputs/results.json")
    
    print("\n✅ Automation complete!")

if __name__ == "__main__":
    main()
