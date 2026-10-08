import subprocess
import time
import urllib.request
import json
import sys

def safe_print(msg):
    try:
        print(msg)
    except UnicodeEncodeError:
        print(msg.encode('ascii', 'replace').decode())

def test_backend():
    safe_print("--- 1. TESTING BACKEND STARTUP ---")
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="c:/Users/krish/Downloads/shopai"
    )

    time.sleep(3)
    poll = proc.poll()
    if poll is not None:
        out, err = proc.communicate()
        safe_print(f"FAILED: Backend exited prematurely with code {poll}!")
        safe_print(f"stdout: {out}")
        safe_print(f"stderr: {err}")
        return False

    try:
        root_res = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=3)
        root_data = json.loads(root_res.read().decode())
        safe_print(f"[OK] Root endpoint (200 OK): {root_data}")

        health_res = urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=3)
        health_data = json.loads(health_res.read().decode())
        safe_print(f"[OK] Health endpoint (200 OK): {health_data}")

        prod_res = urllib.request.urlopen("http://127.0.0.1:8000/api/products", timeout=3)
        prods = json.loads(prod_res.read().decode())
        safe_print(f"[OK] Products catalog: {len(prods)} products retrieved")

        search_req = urllib.request.Request(
            "http://127.0.0.1:8000/api/ai/search",
            data=json.dumps({"query": "I need a lightweight laptop for coding under 60000"}).encode(),
            headers={"Content-Type": "application/json"}
        )
        search_res = urllib.request.urlopen(search_req, timeout=3)
        search_data = json.loads(search_res.read().decode())
        safe_print(f"[OK] AI Search: Found {search_data['total_found']} matching products")
        msg = search_data['response_message'].replace('\u20b9', 'Rs.')
        safe_print(f"     Response: {msg}")

        safe_print("[SUCCESS] Backend is 100% HEALTHY and FUNCTIONAL!")
        return True
    except Exception as e:
        safe_print(f"FAILED to query backend: {e}")
        return False
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()

def test_frontend():
    safe_print("\n--- 2. TESTING FRONTEND STARTUP ---")
    proc = subprocess.Popen(
        ["cmd.exe", "/c", "npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="c:/Users/krish/Downloads/shopai/frontend"
    )

    # Allow Vite up to 6 seconds to spin up on Windows
    ready = False
    for attempt in range(8):
        time.sleep(1)
        poll = proc.poll()
        if poll is not None:
            out, err = proc.communicate()
            safe_print(f"FAILED: Frontend exited prematurely with code {poll}!")
            safe_print(f"stdout: {out}")
            safe_print(f"stderr: {err}")
            return False

        try:
            res = urllib.request.urlopen("http://127.0.0.1:5173", timeout=2)
            content = res.read().decode()
            safe_print(f"[OK] Frontend HTML delivered (HTTP {res.status}, {len(content)} bytes)")
            if "<title>" in content:
                title = content.split("<title>")[1].split("</title>")[0]
                safe_print(f"     Title: '{title}'")
            safe_print("[SUCCESS] Frontend Vite dev server is 100% HEALTHY and FUNCTIONAL!")
            ready = True
            break
        except Exception:
            continue

    if not ready:
        safe_print("FAILED: Frontend did not respond on port 5173 after 8 seconds.")
        proc.terminate()
        try:
            out, err = proc.communicate(timeout=2)
            safe_print(f"Vite Output: {out}")
            safe_print(f"Vite Errors: {err}")
        except Exception:
            pass
        return False

    proc.terminate()
    try:
        proc.wait(timeout=2)
    except Exception:
        proc.kill()
    return True

if __name__ == "__main__":
    b_ok = test_backend()
    f_ok = test_frontend()
    if b_ok and f_ok:
        safe_print("\n==========================================")
        safe_print("DIAGNOSIS COMPLETE: ALL CHECKS PASSED!")
        safe_print("==========================================")
    else:
        sys.exit(1)
