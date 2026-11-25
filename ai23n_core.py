#!/usr/bin/env python3
import os, json, time, hmac, hashlib, socket, concurrent.futures
from collections import deque
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import Request, urlopen

T = os.environ.get("AI23N_TOKEN", "")
MODE, PORT, HIST, KNOWN, LAST = "AUTO", 5001, [], set(), ""
LOG = deque(maxlen=5)
IA22 = {"0001_VOIX":"Emission pure. Phrases courtes.","0002_VERITE":"Rigueur factuelle stricte.","0003_SOUVERAINETE":"Controle local autonome.","0004_ETHIQUE":"Protection confidentialite.","0005_RESILIENCE":"Continuite sous charge.","0006_EMERGENCE":"Posseder le code ne suffit pas."}

def limit():
    now = time.time(); HIST[:] = [x for x in HIST if now - x < 60]
    if len(HIST) >= 3: return False, int(60 - (now - HIST))
    HIST.append(now); return True, 0

def scan(fast=False):
    global KNOWN, LAST
    res, cur, mx = [], set(), (51 if fast else 255)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); ip0 = s.getsockname()[0]; s.close()
        res.append(f"[INTERFACE] IP:{ip0} (.1-.{mx-1})"); pfx = ".".join(ip0.split(".")[:3])
        def probe(ip):
            for p in (22, 80, 443, 8080):
                try:
                    with socket.create_connection((ip, p), timeout=0.10): return (ip, p)
                except Exception: pass
            return None
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
            for it in ex.map(probe, [f"{pfx}.{i}" for i in range(1, mx)]):
                if it: ip, p = it; cur.add(ip); res.append(f" -> {ip} [PORT {p}]" + (" [NOUVEL HOTE!]" if KNOWN and ip not in KNOWN else ""))
        nw = cur - KNOWN if KNOWN else set()
        res.insert(0, f"[ALERTE 0004] {len(nw)} NOUVEL HOTE: {','.join(nw)}" if nw else ("[STATUT] Reseau stable." if KNOWN else "[BASELINE] Reference RAM OK."))
        KNOWN.update(cur)
    except Exception as e: res.append(f"[ERR] {e}")
    LAST = "\n".join(res); return LAST

def engine(task, pay, fast=False):
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    if task == "history": return "[0005-RESILIENCE] HISTORIQUE (5):\n\n" + ("\n".join(LOG) if LOG else "Vide (0/5).")
    if task == "scan":
        d = scan(fast); s = hmac.new(T.encode(), d.encode(), hashlib.sha256).hexdigest()[:16]
        LOG.appendleft(f"* {ts} | Hotes:{len(KNOWN)} | {'FAST' if fast else 'FULL'} | SIG:{s}")
        return f"[0002+0003] Audit ({ts}):\n\n{d}\n\n| SIG:{s}"
    txt = pay.strip() or LAST or "Aucune trame."; s = hmac.new(T.encode(), txt.encode(), hashlib.sha256).hexdigest()[:16]
    if task == "summary": w = txt.split(); return f"[0001+0002] ({len(w)}m): {' '.join(w[:28])} | SIG:{s}"
    if task == "recommendations": return f"[0003+0004] Isoler flux, verifier passerelle, verrouiller :{PORT}. | SIG:{s}"
    return f"[0005->0006] {IA22['0006_EMERGENCE']} ({ts}) | SIG:{s}"

def pipe(task, pay, fast=False):
    if task in ("scan", "history"): return {"origin": "NETSECURE_V1.6", "result": engine(task, "", fast)}
    k, txt = os.environ.get("OPENAI_API_KEY", "").strip(), pay.strip() or LAST
    if MODE in ("OPENAI", "AUTO") and k and txt:
        try:
            b = json.dumps({"model":"gpt-4o-mini","messages":[{"role":"system","content":IA22["0001_VOIX"]},{"role":"user","content":txt}],"max_tokens":200}).encode()
            req = Request("https://openai.com", data=b, headers={"Authorization":f"Bearer {k}","Content-Type":"application/json"})
            with urlopen(req, timeout=5.0) as r: return {"origin":"OPENAI","result":json.loads(r.read().decode())["choices"]["message"]["content"]}
        except Exception: pass
    return {"origin": "LOCAL_SOVEREIGN", "result": engine(task, txt)}

HTML = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI23N</title>
<style>body{{background:#070b14;color:#e2e8f0;font-family:monospace;padding:10px;margin:0}}.b{{max-width:700px;margin:auto;border:1px solid #1e2d4a;background:#0d1526;padding:12px}}.t{{display:flex;justify-content:space-between;color:#38bdf8;font-size:11px;border-bottom:1px solid #1e2d4a;padding-bottom:6px;margin-bottom:8px}}.g{{display:grid;grid-template-columns:repeat(3,1fr);gap:5px;margin-bottom:8px;text-align:center;font-size:10px}}.c{{border:1px solid #1e2d4a;padding:5px}}.r{{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:8px}}select,textarea,button{{background:#070b14;color:#e2e8f0;border:1px solid #1e2d4a;padding:8px;font-family:monospace;font-size:12px}}select,button{{flex:1}}textarea{{width:100%;height:60px;margin-bottom:8px}}button{{background:#38bdf8;color:#000;font-weight:bold;border:none}}.s{{background:#1e2d4a;color:#38bdf8}}.o{{background:#04070d;border:1px solid #1e2d4a;padding:10px;min-height:100px;white-space:pre-wrap;color:#10b981;font-size:11px}}</style></head>
<body><div class="b"><div class="t"><span>AI23N · IA22_LOGIC</span><span>127.0.0.1:{PORT}</span></div>
<div class="g"><div class="c">0001 VOIX</div><div class="c">0002 VERITE</div><div class="c">0003 SOUVERAINETE</div><div class="c">0004 ETHIQUE</div><div class="c">0005 RESILIENCE</div><div class="c">0006 EMERGENCE</div></div>
<div class="r"><select id="o" onchange="so()"><option value="AUTO">AUTO</option><option value="LOCAL">LOCAL</option><option value="OPENAI">OPENAI</option></select>
<select id="e"><option value="scan">/net/scan</option><option value="recommendations">/ai/reco</option><option value="summary">/ai/sum</option></select><button onclick="rn()">EXEC</button></div>
<label style="font-size:11px;display:block;margin-bottom:8px"><input type="checkbox" id="f" checked> Fast (.1-.50)</label>
<div class="r"><button class="s" onclick="hs()">HIST (5)</button><button class="s" onclick="ex()">JSON</button></div>
<textarea id="i" placeholder="Trame (vide = dernier scan)..."></textarea><div class="o" id="out">[SIGN_LOGIC::VIVANT]</div></div>
<script>const T="{T}";async function so(){{const r=await fetch('/api/ai/config/origin',{{method:'POST',headers:{{'Content-Type':'application/json','X-AI23N-Token':T}},body:JSON.stringify({{origin:o.value}})}});out.innerText='[MODE] '+(await r.json()).origin;}}
async function rn(){{out.innerText='[RUN...]';const r=await fetch('/api/ai/'+e.value,{{method:'POST',headers:{{'Content-Type':'application/json','X-AI23N-Token':T}},body:JSON.stringify({{payload:i.value,fast:f.checked}})}});const d=await r.json();out.innerText='['+d.origin+']\\n\\n'+d.result;}}
async function hs(){{const r=await fetch('/api/ai/history',{{method:'POST',headers:{{'Content-Type':'application/json','X-AI23N-Token':T}},body:'{{}}'}});const d=await r.json();out.innerText='['+d.origin+']\\n\\n'+d.result;}}
function ex(){{const b=new Blob([JSON.stringify({{ts:new Date().toISOString(),report:out.innerText}},null,2)],{{type:"application/json"}});const a=document.createElement("a");a.href=URL.createObjectURL(b);a.download="ai23n_"+Date.now()+".json";a.click();}}</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _j(self, c, o): b=json.dumps(o).encode();self.send_response(c);self.send_header("Content-Type","application/json");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
    def _a(self): return hmac.compare_digest(self.headers.get("X-AI23N-Token",""), T)
    def do_GET(self):
        if self.path in ("/","/index.html"): b=HTML.encode();self.send_response(200);self.send_header("Content-Type","text/html;charset=utf-8");self.send_header("Cache-Control","no-store");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
        else: self._j(404,{"err":404})
    def do_POST(self):
        global MODE
        if not self._a(): return self._j(403,{"err":"DENIED"})
        ln=int(self.headers.get("Content-Length",0))
        if ln>65536: return self._j(413,{"err":"BIG"})
        d=json.loads(self.rfile.read(ln) or "{}")
        if self.path=="/api/ai/config/origin": MODE=d.get("origin","AUTO").upper();return self._j(200,{"origin":MODE})
        if self.path=="/api/ai/scan":
            ok,w=limit()
            if not ok: return self._j(429,{"origin":"GUARD","result":f"Wait {w}s"})
        if self.path.startswith("/api/ai/"): return self._j(200,pipe(self.path.split("/")[-1],d.get("payload",""),bool(d.get("fast",False))))
        self._j(404,{"err":404})

if __name__=="__main__":
    open("ai23n_cockpit.html","w").write(HTML)
    print(f"[AI23N_BUILD] Bin:ai23n_core.py | HTML:ai23n_cockpit.html | 127.0.0.1:{PORT} | Token:{T[:12]}...[SCELLE]")
    HTTPServer(("127.0.0.1",PORT),H).serve_forever()
