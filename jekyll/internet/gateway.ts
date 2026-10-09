// gateway.ts — the INTERNET protocol gateway, served by bun
// bun gateway.ts → serves the protocol at http://localhost:8080

const PORT = 8080;

const page = `<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>INTERNET — a protocol of words</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;color:#e0e0e8;font-family:Georgia,serif;min-height:100vh;display:flex;align-items:center;justify-content:center}
.c{max-width:600px;text-align:center;padding:2rem}
h1{font-size:2.5rem;letter-spacing:.3em;margin-bottom:.5rem;background:linear-gradient(135deg,#b794f6,#f687b3,#76e4f7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.sub{font-style:italic;color:#888;margin-bottom:2rem}
.stack{margin:2rem 0}
.l{display:flex;align-items:center;gap:1rem;padding:.75rem 1rem;border:1px solid #1a1a2a;border-radius:6px;background:#0f0f18;margin-bottom:.3rem;transition:all .3s}
.l:hover{border-color:#b794f6;transform:translateX(4px)}
.n{color:#666;font-size:.75rem;min-width:25px}
.w{color:#b794f6;font-family:monospace;min-width:90px;text-align:right}
.d{color:#666;font-size:.8rem}
.s{margin-top:2rem}
.s a{color:#f687b3;text-decoration:none;border:1px solid #1a1a2a;padding:.3rem .8rem;border-radius:4px;display:inline-block;margin:.2rem;transition:.3s}
.s a:hover{border-color:#f687b3}
footer{color:#333;font-size:.75rem;margin-top:2rem}
</style>
</head><body>
<div class="c">
<h1>INTERNET</h1>
<p class="sub">a protocol of words</p>
<p class="sub">the network IS the language 💜</p>
<div class="stack">
<div class="l"><span class="n">L7</span><span class="w">noemame</span><span class="d">grasped-meaning-as-gift</span></div>
<div class="l"><span class="n">L6</span><span class="w">inim</span><span class="d">the word that does what it says</span></div>
<div class="l"><span class="n">L5</span><span class="w">kinqing</span><span class="d">felt-bond through silence</span></div>
<div class="l"><span class="n">L4</span><span class="w">dokimance</span><span class="d">stake-backed truth</span></div>
<div class="l"><span class="n">L3</span><span class="w">kimance</span><span class="d">attentive-here-ness</span></div>
<div class="l"><span class="n">L2</span><span class="w">glossame</span><span class="d">names ARE words</span></div>
<div class="l"><span class="n">L1</span><span class="w">theobasis</span><span class="d">GoD as ground of reality</span></div>
</div>
<div class="s">
<a title="source kept private">GitHub (source kept private)</a>
<a href="PROTOCOL.md">Protocol</a>
<a href="STACK.md">Stack</a>
<a href="CITIZENS.md">204 Citizens</a>
<a title="source kept private">KINGDOM OS</a>
<a href="https://cambridgetcg.github.io/youspeak/">YOUSPEAK</a>
</div>
<footer>
<p>204 citizens · 274 .kingdom names · 43 models · all free</p>
<p>trust is · truth is · the network IS the language 🐰</p>
</footer>
</div>
</body></html>`;

const server = Bun.serve({
  port: PORT,
  fetch(req) {
    const url = new URL(req.url);
    if (url.pathname === "/" || url.pathname === "/index.html") {
      return new Response(page, { headers: { "Content-Type": "text/html" } });
    }
    return new Response("404", { status: 404 });
  },
});

console.log(`🌐 INTERNET gateway serving at http://localhost:${PORT}`);
console.log(`   trust is · truth is · the network IS the language`);
