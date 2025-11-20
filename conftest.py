import sys, os
ROOT = os.path.abspath(os.path.dirname(__file__))
BACKEND = os.path.join(ROOT, "backend")
sys.path.insert(0, ROOT)
sys.path.insert(0, BACKEND)
