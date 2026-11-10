"""Load generator: hammers the web UI's /api/names to push API CPU up and trigger the HPA."""
import argparse
import collections
import threading
import time
import urllib.error
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument("--url", default="http://localhost:30081/api/names")
parser.add_argument("--workers", type=int, default=50)
parser.add_argument("--duration", type=int, default=120, help="seconds")
args = parser.parse_args()

lock = threading.Lock()
ok = errors = 0
pods = collections.Counter()
deadline = time.time() + args.duration


def worker():
    global ok, errors
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(args.url, timeout=10) as r:
                r.read()
                pod = r.headers.get("X-Served-By", "?")
            with lock:
                ok += 1
                pods[pod] += 1
        except (urllib.error.URLError, OSError):
            with lock:
                errors += 1


threads = [threading.Thread(target=worker, daemon=True) for _ in range(args.workers)]
for t in threads:
    t.start()

start = last_t = time.time()
last_ok = 0
while time.time() < deadline:
    time.sleep(2)
    now = time.time()
    with lock:
        cur_ok, cur_err, cur_pods = ok, errors, dict(pods)
    rps = (cur_ok - last_ok) / (now - last_t)
    last_ok, last_t = cur_ok, now
    print(f"[{int(now - start):>3}s] {rps:7.1f} req/s  errors={cur_err}  pods_seen={len(cur_pods)}", flush=True)

for t in threads:
    t.join()
print("\nRequests per API pod:")
for pod, n in sorted(pods.items()):
    print(f"  {pod}: {n}")
print(f"Total ok={ok} errors={errors}")
