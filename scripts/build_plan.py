#!/usr/bin/env python3
"""Generate plan.html for the Capsaicin Design Platform.

All task cards are rendered as STATIC HTML so the whole plan is visible even
when the page is shown as a static snapshot (no JS). JavaScript then layers on
click-to-update status + notes (saved per-browser) when it is allowed to run.

Update progress by editing STATUS below and re-running:  python3 build_plan.py
"""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "plan.html"

# ---- which tasks are complete / in-progress (baked into the static page) ----
STATUS = {
    "0.1":"done","0.2":"done","0.3":"done","0.4":"done","1.1":"done","1.2":"done",
    "0.5":"done","1.6":"done","2.1":"done","2.2":"done","2.3":"done","2.4":"done","2.5":"done",
    "3.1":"done","3.2":"done","3.3":"done","3.4":"done","3.5":"done","3.6":"done","3.7":"done",
    "4.1":"done","4.2":"done","4.3":"done","4.4":"done","4.5":"done",
    "1.3":"defer","1.4":"defer","1.5":"defer",
    "6.1":"done","6.2":"done","6.3":"done","6.4":"done","6.5":"done",
    "6.6":"done","6.7":"done","6.8":"done","6.9":"done","6.10":"done",
    "5.5":"done","5.6":"done","5.3":"done",
}

COMPUTE = {
    "local":  ("c-local",  "🖥️ Local"),
    "lambda": ("c-lambda", "☁️ GCP GPU"),
    "claude": ("c-claude", "🧠 Claude"),
    "wetlab": ("c-wetlab", "🧪 Wet-lab"),
    "mix":    ("c-mix",    "⚙️ Mixed"),
}
LABEL = {"todo": "● Not started", "prog": "▶ In progress",
         "block": "■ Blocked", "done": "✓ Done", "defer": "◇ Deferred"}

PHASES = [
 ("Phase 0", "Setup, Data & Landscape", "local + my own research", [
   ("0.1", "Compute environment", "miniforge + Python 3.11 bioconda env — core genomics toolchain installed (samtools, bcftools, bwa-mem2, minimap2, sra-tools, datasets, diamond, seqkit).", "—", ["miniforge","bioconda","mamba"], "local"),
   ("0.2", "Literature review", "Capsaicin biosynthesis, placental accumulation, peroxidase degradation, superhot genomics. I read the papers and build a cited knowledge base.", "PubMed, journals", ["Claude","WebSearch"], "claude"),
   ("0.3", "Patent / prior-art landscape", "I map existing IP so every design lands in open space; identify what is patentable vs. already claimed.", "USPTO, Google Patents", ["Claude","WebSearch"], "claude"),
   ("0.4", "Reference genome acquisition", "Downloaded 3 annotated Capsicum genomes: C. annuum UCD10Xv1.1 (RefSeq, 51,555 proteins), C. chinense habanero (34,974), C. baccatum PBC81 (35,853).", "NCBI Datasets", ["datasets","dataformat"], "local"),
   ("0.5", "Resequencing + RNA-seq ingest", "Pull pungency-panel resequencing reads and placenta RNA-seq (superhot vs mild).", "NCBI SRA / GEO", ["sra-tools","prefetch"], "local"),
 ]),
 ("Phase 1", "Comparative Genomics", "local — CPU + big RAM", [
   ("1.1", "Genome QC & indexing", "Validate, index, and standardize all assemblies for downstream alignment.", "assemblies", ["samtools","minimap2"], "local"),
   ("1.2", "Pathway gene family mapping", "Pun1/AT3 + pAMT identified by homology to curated references (AY819027 / O82521), not keyword — true orthologs resolved in all 3 species at 98-100% id; PAL, C4H, 4CL, HCT, COMT, KAS, FAT census complete.", "genomes + proteomes", ["DIAMOND","seqkit"], "local"),
   ("1.3", "Variant calling (pungency panel)", "Align resequencing reads, call SNPs/indels across mild→superhot accessions. RAM-heavy — ideal for this box.", "reads + ref", ["BWA-MEM2","GATK","bcftools"], "local"),
   ("1.4", "GWAS — heat vs genotype", "Associate Scoville / capsaicinoid phenotype with variants to find the causal loci.", "VCF + SHU traits", ["TASSEL","GEMMA"], "local"),
   ("1.5", "Selection & population scans", "Detect signatures of selection around pathway loci in superhots.", "VCF", ["vcftools","selscan"], "local"),
   ("1.6", "Superhot genome annotation", "Annotate the unpublished superhot assembly GCA_054135625.1 (3.09 Gb, chromosome-scale) by protein-homology — map Pun1/AT3, pAMT and the full pathway onto it and check each gene's integrity (intact ORF? functional pAMT?).", "superhot genome + pathway proteins", ["miniprot","seqkit"], "local"),
 ]),
 ("Phase 2", "Transcriptomics & Pathway Modeling", "local", [
   ("2.1", "RNA-seq quantification", "Quantify placenta expression across accessions.", "RNA-seq reads", ["STAR","Salmon"], "local"),
   ("2.2", "Differential expression", "Which pathway genes are cranked up in superhot placenta vs mild — the real throttles.", "counts", ["pydeseq2","edgeR"], "local"),
   ("2.3", "Co-expression network", "Find regulatory hubs / transcription factors governing the pathway (WGCNA).", "expression matrix", ["WGCNA"], "local"),
   ("2.4", "Metabolic flux modeling (FBA)", "Model the biosynthesis network to pinpoint rate-limiting steps and precursor bottlenecks.", "pathway model", ["COBRApy","Escher"], "local"),
   ("2.5", "Potency-ceiling & titer modeling", "How high can capsaicinoid titer actually go? Model the precursor-flux supercharging and accumulation needed to reach the ladder's top (D.N.R. ~13M SHU, near the 16M pure-capsaicin ceiling) and flag the limiting step for each setpoint.", "flux model + targets", ["COBRApy"], "local"),
 ]),
 ("Phase 3", "Structure & Enzyme Engineering", "GCP GPU (NVIDIA L4) — the heavy ML", [
   ("3.1", "Enzyme structure prediction", "Predict structures of capsaicin synthase (Pun1/AT3) + pAMT to locate the acyl-binding pocket around the catalytic H169 (HXXXD) and DFGWG motifs. Fold target staged: 04-structures/fold_target_Pun1.faa.", "protein seqs", ["ColabFold","ESMFold"], "lambda"),
   ("3.2", "Substrate docking", "Dock vanillylamine + acyl-CoA into the active site; map the specificity pocket.", "structures", ["AutoDock Vina","DiffDock"], "mix"),
   ("3.3", "MD simulation", "Simulate enzyme–substrate dynamics & stability of candidate mutants.", "docked complexes", ["GROMACS","OpenMM"], "lambda"),
   ("3.4", "Variant activity prediction", "Score mutations for higher catalytic efficiency with protein language models.", "sequences", ["ESM-1v","ESM2"], "lambda"),
   ("3.5", "De novo / redesigned enzyme", "Design an enzyme accepting new acyl tails → NEW-TO-NATURE capsaicinoids. The patentable crown jewel.", "active-site spec", ["RFdiffusion","ProteinMPNN"], "lambda"),
   ("3.6", "TRPV1 receptor design", "Model the human TRPV1 heat receptor; design molecules for tuned perceived burn.", "TRPV1 struct + ligands", ["ColabFold","Vina"], "mix"),
   ("3.7", "Capsaicinoid blend & burn-quality design", "Design the capsaicinoid profile per product (capsaicin · dihydrocapsaicin · novel analogs) so each heat level also delivers its signature burn — the sinus hit, the slow build, the chest wave — matching every product's marketing vibe, not just its SHU.", "profiles + TRPV1 kinetics", ["Vina","ESM2"], "mix"),
 ]),
 ("Phase 4", "Design Integration & Edit Strategy", "local", [
   ("4.1", "Multi-objective ranking", "Score candidate designs on heat × accumulation × plant viability × flavor; output a ranked portfolio mapped onto the 10-product heat ladder, not one champion.", "all prior results", ["Python","Optuna"], "local"),
   ("4.2", "CRISPR edit design", "Guides for peroxidase knockouts, promoter swaps, and pathway up-regulation; off-target screen.", "genome + targets", ["CRISPOR","Cas-OFFinder"], "local"),
   ("4.3", "Microbial chassis design", "Optional frontier route: port the pathway into yeast/E. coli to ferment capsaicin — no growing season.", "pathway + constructs", ["COBRApy","CAD tools"], "local"),
   ("4.4", "Final candidate dossier", "In-silico-validated design package: sequences, constructs, predicted phenotypes, build instructions.", "integrated", ["Python","report"], "local"),
   ("4.5", "Heat-ladder calibration — per-product recipes", "Lock each of the 10 products to its SHU setpoint (3.0M → 13M): a concrete edit / expression-dial / capsaicinoid-stack recipe per cultivar, engineered so the ten levels are distinct, monotonic, and reproducible batch-to-batch.", "ranked designs + targets", ["Python"], "local"),
 ]),
 ("Phase 5", "Validation & Publication", "partner lab + writing", [
   ("5.1", "Wet-lab validation (partner)", "Commission build + grow/ferment + HPLC Scoville measurement. Out of our compute scope — in the plan.", "designs → lab", ["PacBio HiFi","RNA-seq","HPLC"], "wetlab"),
   ("5.2", "Sequence & data deposit", "Engineered sequences → GenBank; code + datasets → Zenodo DOI. Timestamped authorship.", "final outputs", ["GenBank","Zenodo"], "local"),
   ("5.3", "Preprint + paper(s)", "bioRxiv preprint then peer review. 1–3 papers: comparative genomics · novel enzyme/molecule · the platform.", "everything", ["LaTeX","bioRxiv"], "mix"),
   ("5.4", "IP & naming", "Defensive publication + utility patents on novel enzymes/molecules; trademark the line name.", "—", ["counsel"], "mix"),
   ("5.5", "Analytics SOP — HPLC → SHU", "Standardized capsaicinoid HPLC assay + SHU conversion that feeds the Scoville tracker; per-batch QC so every product's measured heat is defensible and comparable.", "fruit extracts", ["HPLC","method"], "wetlab"),
   ("5.6", "Ultra-hot safety, handling & regulatory", "These products (3–13M SHU) are hotter than law-enforcement pepper spray. Food-safety, labeling, handling protocols, consumer warnings, and liability — the route to a compliant, insurable launch.", "product specs", ["reg","counsel"], "mix"),
   ("5.7", "Cultivar line stabilization & field trials", "Stabilize each graded line across generations; seed stock + replicated grow-outs to confirm the SHU ladder holds in real fruit, not just in silico.", "seed + plots", ["agronomy"], "wetlab"),
   ("5.8", "Public website — ScovilleSplice.farm", "Launch the Scoville Splice site: the product ladder, the science, the team, live results and press kit. The front door for customers, press, and investors.", "content + domain", ["web","hosting"], "mix"),
   ("5.9", "Social media presence", "Stand up and run Scoville Splice social channels (X, Instagram, TikTok, LinkedIn) to broadcast milestones, drops, and the brand.", "content calendar", ["social"], "mix"),
 ]),
 ("Phase 6", "Scoville Splice — The Product Line", "the 10 hottest peppers ever made", [
   ("6.1",  "Heat 01 — Verbal Warning",   "Entry heat. A sharp, stinging reminder that you are playing with fire.", "design → cultivar", ["line"], "mix"),
   ("6.2",  "Heat 02 — Kill Switch",       "One bite and everything shuts down. No warning, no warmup — just off.", "design → cultivar", ["line"], "mix"),
   ("6.3",  "Heat 03 — Hostile Agent",    "The capsaicin actively fights back against your palate.", "design → cultivar", ["line"], "mix"),
   ("6.4",  "Heat 04 — Containment Breach","The heat escapes the mouth and aggressively hits the sinuses and chest.", "design → cultivar", ["line"], "mix"),
   ("6.5",  "Heat 05 — System Shock",     "Adrenaline hits and endorphins flood the brain; the physical reaction is undeniable.", "design → cultivar", ["line"], "mix"),
   ("6.6",  "Heat 06 — Venom Protocol",   "The heat registers less like a food ingredient and more like a systematic biological attack.", "design → cultivar", ["line"], "mix"),
   ("6.7",  "Heat 07 — Level 4 Pathogen", "Requires extreme handling. A laboratory-grade biological hazard.", "design → cultivar", ["line"], "mix"),
   ("6.8",  "Heat 08 — Collateral Damage","Guaranteed to ruin your day, your digestive tract, and your ego.", "design → cultivar", ["line"], "mix"),
   ("6.9",  "Heat 09 — Extinction Protocol","2nd hottest. A world-ending, sensory-wiping heat. The scorched-earth option.", "design → cultivar", ["line"], "mix"),
   ("6.10", "Heat 10 — D.N.R. (Do Not Resuscitate)","World's hottest. The absolute limit of human endurance. You are entirely on your own.", "design → cultivar", ["line"], "mix"),
 ]),
]

CSS = """
  :root{
    --bg:#f7f6f3; --panel:#ffffff; --ink:#1c1a17; --muted:#6b6459;
    --line:#e6e2da; --accent:#c62828; --accent2:#e65100;
    --local:#2e7d32; --lambda:#1565c0; --claude:#6a1b9a; --wetlab:#8d6e63; --mix:#00838f;
    --todo:#9e9e9e; --prog:#e65100; --block:#c62828; --done:#2e7d32; --defer:#5c6bc0;
    --shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px rgba(0,0,0,.05);
    --radius:14px;
  }
  :root:not([data-theme="light"]){ @media (prefers-color-scheme:dark){
    --bg:#15130f; --panel:#201d18; --ink:#f0ece4; --muted:#a79f91;
    --line:#352f27; --accent:#ff6b5e; --accent2:#ffa040;
    --local:#66bb6a; --lambda:#64b5f6; --claude:#ce93d8; --wetlab:#bcaaa4; --mix:#4dd0e1; --defer:#7986cb;
    --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.3);
  }}
  :root[data-theme="dark"]{
    --bg:#15130f; --panel:#201d18; --ink:#f0ece4; --muted:#a79f91;
    --line:#352f27; --accent:#ff6b5e; --accent2:#ffa040;
    --local:#66bb6a; --lambda:#64b5f6; --claude:#ce93d8; --wetlab:#bcaaa4; --mix:#4dd0e1; --defer:#7986cb;
    --shadow:0 1px 3px rgba(0,0,0,.4),0 8px 24px rgba(0,0,0,.3);
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    line-height:1.5;padding:0 16px 80px}
  .wrap{max-width:1100px;margin:0 auto}
  header{padding:32px 0 8px}
  .kicker{letter-spacing:.18em;text-transform:uppercase;font-size:12px;color:var(--accent);font-weight:700}
  h1{font-size:30px;margin:6px 0 4px;line-height:1.1}
  .sub{color:var(--muted);font-size:15px;max-width:720px}
  .machine{margin:18px 0;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
    padding:14px 16px;box-shadow:var(--shadow);display:flex;flex-wrap:wrap;gap:18px;font-size:13px}
  .machine b{color:var(--ink)} .machine span{color:var(--muted)}
  .machine .warn{color:var(--accent)}
  .bar-wrap{margin:14px 0 6px;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
    padding:14px 16px;box-shadow:var(--shadow)}
  .bar-top{display:flex;justify-content:space-between;align-items:center;font-size:13px;color:var(--muted);margin-bottom:8px}
  .bar{height:10px;background:var(--line);border-radius:6px;overflow:hidden;display:flex}
  .bar i{display:block;height:100%}
  .legend{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0}
  .chip{font-size:12px;font-weight:600;padding:3px 10px;border-radius:999px;color:#fff;white-space:nowrap}
  .c-local{background:var(--local)} .c-lambda{background:var(--lambda)} .c-claude{background:var(--claude)}
  .c-wetlab{background:var(--wetlab)} .c-mix{background:var(--mix)}
  .phase{margin-top:28px}
  .phase-h{display:flex;align-items:baseline;gap:12px;border-bottom:2px solid var(--line);padding-bottom:6px;margin-bottom:14px;flex-wrap:wrap}
  .phase-h h2{font-size:20px;margin:0}
  .phase-h .tag{font-size:12px;color:var(--muted)}
  .phase-h .num{font-size:13px;font-weight:800;color:var(--accent);background:color-mix(in srgb,var(--accent) 12%,transparent);
    border-radius:8px;padding:2px 9px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:12px}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:14px;box-shadow:var(--shadow);
    display:flex;flex-direction:column;gap:8px;position:relative}
  .card .id{font-size:11px;font-weight:800;letter-spacing:.08em;color:var(--muted)}
  .card h3{margin:0;font-size:15px}
  .card p{margin:0;font-size:13px;color:var(--muted)}
  .card .row{font-size:12px;display:flex;gap:6px;flex-wrap:wrap}
  .card .row b{color:var(--ink);font-weight:600}
  .tool{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:11.5px;color:var(--ink);
    background:color-mix(in srgb,var(--line) 55%,transparent);padding:1px 6px;border-radius:5px}
  .foot{display:flex;justify-content:space-between;align-items:center;margin-top:4px;gap:8px}
  .status{border:none;cursor:pointer;font-weight:700;font-size:12px;color:#fff;border-radius:8px;padding:5px 12px;flex:1}
  .s-todo{background:var(--todo)} .s-prog{background:var(--prog)} .s-block{background:var(--block)} .s-done{background:var(--done)} .s-defer{background:var(--defer)}
  .note{flex:2;border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:8px;
    padding:5px 8px;font-size:12px;font-family:inherit}
  .note::placeholder{color:var(--muted)}
  .endpoint{margin-top:28px;background:linear-gradient(135deg,color-mix(in srgb,var(--accent) 14%,var(--panel)),var(--panel));
    border:1px solid var(--line);border-radius:var(--radius);padding:18px;box-shadow:var(--shadow)}
  .endpoint h2{margin:0 0 6px;font-size:19px}
  .endpoint ul{margin:8px 0 0;padding-left:18px;font-size:14px;color:var(--muted)}
  .toolbar{display:flex;gap:8px;align-items:center;margin:8px 0;flex-wrap:wrap}
  .btn{font-size:12px;border:1px solid var(--line);background:var(--panel);color:var(--ink);
    border-radius:8px;padding:6px 12px;cursor:pointer;font-weight:600}
  .meta{font-size:11px;color:var(--muted);margin-top:4px}
  footer{margin-top:40px;color:var(--muted);font-size:12px;text-align:center}
  ul.live{list-style:none;margin:10px 0 0;padding:0;font-size:13px;line-height:1.9}
  ul.live li{border-bottom:1px dashed var(--line);padding:4px 0}
  ul.live .lt{color:var(--muted);font-variant-numeric:tabular-nums;font-size:12px;margin-right:6px}
  .shu-wrap{margin-top:28px;background:var(--panel);border:1px solid var(--line);
    border-radius:var(--radius);padding:18px;box-shadow:var(--shadow)}
  .shu-wrap h2{margin:0 0 4px;font-size:19px}
  .shu-cap{font-size:12px;color:var(--muted);margin:0 0 14px}
  table.shu{width:100%;border-collapse:collapse;font-size:13px}
  table.shu th,table.shu td{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}
  table.shu th{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted);font-weight:700}
  table.shu td.num{font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap}
  .hlvl{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:7px;
    background:color-mix(in srgb,var(--accent) 16%,transparent);color:var(--accent);font-weight:800;font-size:12px}
  .pname{font-weight:700}
  .heatbar{position:relative;height:9px;border-radius:6px;background:color-mix(in srgb,var(--ink) 8%,transparent);overflow:hidden;min-width:80px}
  .heatbar>i{position:absolute;inset:0 auto 0 0;border-radius:6px;
    background:linear-gradient(90deg,#f6b73c,#e8541e,#c0141b)}
  input.shu-in{width:110px;border:1px solid var(--line);background:transparent;color:var(--ink);
    border-radius:7px;padding:5px 7px;font-size:12px;font-family:inherit;font-variant-numeric:tabular-nums;text-align:right}
  input.shu-note{width:100%;min-width:120px;border:1px solid var(--line);background:transparent;color:var(--ink);
    border-radius:7px;padding:5px 7px;font-size:12px;font-family:inherit}
  input.shu-in::placeholder,input.shu-note::placeholder{color:var(--muted)}
"""

JS = """
const STATES=["todo","prog","block","done","defer"];
const LABEL={todo:"● Not started",prog:"▶ In progress",block:"■ Blocked",done:"✓ Done",defer:"◇ Deferred"};
const KEY="capsaicin_tracker_v1";
let store={};
try{store=JSON.parse(localStorage.getItem(KEY)||"{}")}catch(e){store={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(store))}catch(e){}}
function stFor(id,def){return (store[id]&&store[id].s)||def||"todo"}
function applyAll(){
  document.querySelectorAll('.status').forEach(function(b){
    var id=b.dataset.id, def=b.dataset.default, s=stFor(id,def);
    b.className='status s-'+s; b.textContent=LABEL[s];
    b.onclick=function(){
      var cur=stFor(id,def), n=STATES[(STATES.indexOf(cur)+1)%4];
      store[id]=store[id]||{}; store[id].s=n; save();
      b.className='status s-'+n; b.textContent=LABEL[n]; prog();
    };
  });
  document.querySelectorAll('.note').forEach(function(inp){
    var id=inp.dataset.id;
    if(store[id]&&store[id].n) inp.value=store[id].n;
    inp.oninput=function(){store[id]=store[id]||{}; store[id].n=inp.value; save();};
  });
}
function prog(){
  var all=document.querySelectorAll('.status'), done=0;
  all.forEach(function(b){if(b.classList.contains('s-done'))done++;});
  var pct=all.length?Math.round(done/all.length*100):0;
  document.getElementById('progressText').textContent=done+' / '+all.length+' tasks complete';
  document.getElementById('progressPct').textContent=pct+'%';
  document.getElementById('bar').innerHTML='<i style="width:'+pct+'%;background:var(--done)"></i>';
}
function resetAll(){if(confirm('Reset all status and notes?')){store={};save();applyAll();prog();}}
function toggleTheme(){
  var cur=document.documentElement.getAttribute('data-theme');
  var next=cur==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-theme',next);
  try{localStorage.setItem(KEY+'_theme',next)}catch(e){}
}
try{var th=localStorage.getItem(KEY+'_theme')||'dark';document.documentElement.setAttribute('data-theme',th)}catch(e){document.documentElement.setAttribute('data-theme','dark')}
applyAll(); prog();
"""


def tool_spans(tools):
    return " ".join('<span class="tool">%s</span>' % escape(t) for t in tools)


def card(t):
    tid, name, what, data, tools, compute = t
    cclass, cname = COMPUTE[compute]
    st = STATUS.get(tid, "todo")
    return (
        '<div class="card">'
        '<div class="id">%s · <span class="chip %s" style="font-size:10px;padding:1px 7px">%s</span></div>'
        '<h3>%s</h3><p>%s</p>'
        '<div class="row"><b>Data:</b> %s</div>'
        '<div class="row">%s</div>'
        '<div class="foot">'
        '<button class="status s-%s" data-id="%s" data-default="%s">%s</button>'
        '<input class="note" data-id="%s" placeholder="notes…">'
        '</div></div>'
    ) % (tid, cclass, cname, escape(name), escape(what), escape(data),
         tool_spans(tools), st, tid, st, LABEL[st], tid)


def phase(p):
    num, title, tag, tasks = p
    cards = "\n".join(card(t) for t in tasks)
    return (
        '<div class="phase"><div class="phase-h">'
        '<span class="num">%s</span><h2>%s</h2><span class="tag">%s</span></div>'
        '<div class="grid">%s</div></div>'
    ) % (num, escape(title), escape(tag), cards)


total = sum(len(p[3]) for p in PHASES)
done = sum(1 for p in PHASES for t in p[3] if STATUS.get(t[0]) == "done")
pct = round(done / total * 100)

# ---- live Phase 3.1 results panel (reads a plain status file we append to) ----
def live_panel():
    f = Path(__file__).resolve().parent.parent / "03-results" / "phase3.1_status.txt"
    if not f.exists():
        return ""
    rows = [l.rstrip() for l in f.read_text().splitlines() if l.strip()]
    if not rows:
        return ""
    items = []
    for l in rows:
        # format: STATE | time | message       (STATE in done/prog/todo/block)
        parts = [p.strip() for p in l.split("|", 2)]
        if len(parts) == 3:
            st, t, msg = parts
        else:
            st, t, msg = "prog", "", l
        dot = {"done":"✓","prog":"▶","todo":"•","block":"■"}.get(st, "▶")
        col = {"done":"var(--done)","prog":"var(--prog)","todo":"var(--muted)","block":"var(--block)"}.get(st,"var(--prog)")
        items.append(f'<li><span style="color:{col};font-weight:800">{dot}</span> '
                     f'<span class="lt">{t}</span> {msg}</li>')
    return ('<div class="endpoint" style="border-color:var(--prog)">'
            '<h2>🧬 Live run log</h2>'
            '<ul class="live">' + "\n".join(items) + '</ul></div>')

# ---- Scoville (SHU) tracker for the 10 Scoville Splice products ----
# Target SHU = design goals (ascending ladder). Measured SHU is entered as wet-lab
# HPLC data comes in and persists in the browser (same localStorage as task notes).
SCOVILLE = [
    ("6.1",  "01", "Verbal Warning",        3000000),
    ("6.2",  "02", "Kill Switch",            3600000),
    ("6.3",  "03", "Hostile Agent",         4300000),
    ("6.4",  "04", "Containment Breach",    5100000),
    ("6.5",  "05", "System Shock",          6000000),
    ("6.6",  "06", "Venom Protocol",         7000000),
    ("6.7",  "07", "Level 4 Pathogen",      8200000),
    ("6.8",  "08", "Collateral Damage",     9500000),
    ("6.9",  "09", "Extinction Protocol",  11000000),
    ("6.10", "10", "D.N.R. (Do Not Resuscitate)", 13000000),
]
def scoville_section():
    mx = max(s[3] for s in SCOVILLE)
    rows = []
    for tid, lvl, name, target in SCOVILLE:
        pct = round(target / mx * 100)
        rows.append(
            '<tr>'
            f'<td><span class="hlvl">{lvl}</span></td>'
            f'<td class="pname">{name}</td>'
            f'<td class="num">{target:,}</td>'
            f'<td><div class="heatbar"><i style="width:{pct}%"></i></div></td>'
            f'<td class="num"><input class="note shu-in" data-id="shu-{tid}-measured" placeholder="— SHU"></td>'
            f'<td><input class="note shu-note" data-id="shu-{tid}-notes" placeholder="trial / HPLC batch / status…"></td>'
            '</tr>')
    return (
        '<div class="shu-wrap">'
        '<h2>🌶️ Scoville Scale Tracker — the 10 Scoville Splice products</h2>'
        '<p class="shu-cap">Target SHU = design goal for each heat level. Enter <b>Measured SHU</b> '
        'as wet-lab HPLC results come in — values save in your browser. '
        'Reference anchors: jalape&ntilde;o ~5,000 · habanero ~350,000 · '
        'Carolina Reaper ~1,640,000 · Pepper X ~2,690,000 · pure capsaicin ~16,000,000.</p>'
        '<table class="shu"><thead><tr>'
        '<th>Heat</th><th>Product</th><th>Target SHU</th><th>Target ladder</th>'
        '<th>Measured SHU</th><th>Notes</th>'
        '</tr></thead><tbody>' + "\n".join(rows) + '</tbody></table></div>')

HTML = """<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Capsaicin Design Platform</title>
<style>%s</style>
</head>
<body>
<div class="wrap">
<header>
  <div class="kicker">Scoville Splice · ScovilleSplice.farm · Computational Design Program</div>
  <h1>The Capsaicin Design Platform</h1>
  <div class="sub">An in-silico program to design the hottest &mdash; and most <em>novel</em> &mdash; capsaicinoids and the peppers (or microbes) that make them. From first analysis to published papers, tracked end to end.</div>
  <div class="machine">
    <span><b>🖥️ Local:</b> Mac Pro Rack · 28-core Xeon W / 56 threads · <b>768 GB RAM</b> · 5.1 TB free</span>
    <span class="warn"><b>GPUs:</b> 4× AMD W6800X (128 GB VRAM) — <b>CUDA-only ML runs on GCP</b></span>
    <span><b>☁️ GCP GPU:</b> NVIDIA L4 (g2-standard-8, us-central1) — spun up per-job</span>
    <span><b>🧠 Claude:</b> literature &amp; patent synthesis (me)</span>
  </div>
</header>

<div class="bar-wrap">
  <div class="bar-top"><span id="progressText">%d / %d tasks complete</span><span id="progressPct">%d%%</span></div>
  <div class="bar" id="bar"><i style="width:%d%%;background:var(--done)"></i></div>
  <div class="toolbar">
    <button class="btn" onclick="resetAll()">Reset all status</button>
    <button class="btn" onclick="toggleTheme()">Toggle light/dark</button>
    <span class="meta">Click a status pill to cycle Not started → In progress → Blocked → Done. Saved in this browser.</span>
  </div>
</div>

<div class="legend">
  <span class="chip c-local">🖥️ Local Mac Pro</span>
  <span class="chip c-lambda">☁️ GCP GPU (NVIDIA L4)</span>
  <span class="chip c-claude">🧠 Claude (me)</span>
  <span class="chip c-mix">⚙️ Mixed</span>
  <span class="chip c-wetlab">🧪 Wet-lab (partner)</span>
</div>

%s

%s

<div class="endpoint">
  <h2>🏁 The Finish Line — Publication & Credit</h2>
  <p class="sub">No DNA patent needed to own the invention. Credit is locked in by:</p>
  <ul>
    <li><b>Preprint (bioRxiv) + peer-reviewed paper(s)</b> — likely 1 platform paper, possibly up to 3.</li>
    <li><b>GenBank / NCBI deposit</b> of every engineered sequence under your name + date.</li>
    <li><b>Zenodo DOI</b> for all code and datasets — permanent, citable provenance.</li>
    <li><b>Defensive publication</b> to establish prior art (blocks others) + <b>utility patents</b> on novel enzymes &amp; new-to-nature molecules.</li>
    <li><b>Trademark the cultivar/line name</b> — how "Carolina Reaper" &amp; "Pepper X" are actually owned.</li>
  </ul>
</div>

%s

<footer>Capsaicin Design Platform · tracker v2 (static-rendered) · updated 2026-10-09 · a living document.</footer>
</div>
<script>%s</script>
</body>
</html>
""" % (CSS, done, total, pct, pct, "\n".join(phase(p) for p in PHASES), live_panel(), scoville_section(), JS)

OUT.write_text(HTML, encoding="utf-8")
print("wrote", OUT)
print("tasks:", total, "| done:", done, "| pct:", pct)
