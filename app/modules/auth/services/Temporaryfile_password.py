from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[4]))

from app.core.security import hash_password

print(hash_password("superadmin123"))
