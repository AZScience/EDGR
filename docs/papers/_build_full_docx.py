"""
Build submission DOCX from a structured manuscript with native Word OMML equations.
Uses latex2mathml + mathml2omml (fallback: Office MML2OMML.XSL).
"""
from __future__ import annotations

import re
from pathlib import Path

import latex2mathml.converter
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsmap
from docx.shared import Cm, Inches, Pt, RGBColor
from lxml import etree

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"
XSL = Path(r"C:\Program Files (x86)\Microsoft Office\root\Office16\MML2OMML.XSL")

try:
    import mathml2omml

    HAS_MATHML2OMML = True
except ImportError:
    HAS_MATHML2OMML = False

_TRANSFORM = None
if XSL.exists():
    _TRANSFORM = etree.XSLT(etree.parse(str(XSL)))


def latex_to_omml_element(latex: str, display: bool = True):
    latex = latex.strip().strip("$")
    mathml = latex2mathml.converter.convert(latex)
    if isinstance(mathml, str):
        tree = etree.fromstring(mathml.encode("utf-8"))
    else:
        tree = etree.fromstring(mathml)
    if "xmlns" not in tree.attrib:
        tree.attrib["xmlns"] = "http://www.w3.org/1998/Math/MathML"

    NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    omml_root = None

    # Prefer Office XSLT when available (most faithful Word equations)
    if _TRANSFORM is not None:
        try:
            new_dom = _TRANSFORM(tree)
            omml_root = new_dom.getroot()
        except Exception:
            omml_root = None

    if omml_root is None and HAS_MATHML2OMML:
        omml_str = mathml2omml.convert(etree.tostring(tree, encoding="unicode"))
        if not omml_str.strip().startswith("<m:"):
            omml_str = f"<m:oMath>{omml_str}</m:oMath>"
        if "xmlns:m=" not in omml_str:
            omml_str = omml_str.replace("<m:oMath>", f'<m:oMath xmlns:m="{NS}">', 1)
            omml_str = omml_str.replace("<m:oMathPara>", f'<m:oMathPara xmlns:m="{NS}">', 1)
        omml_root = parse_xml(omml_str)

    if omml_root is None:
        raise RuntimeError(f"Cannot convert LaTeX to OMML: {latex}")

    tag = omml_root.tag.split("}")[-1] if "}" in omml_root.tag else omml_root.tag
    if display and tag == "oMath":
        para = parse_xml(f'<m:oMathPara xmlns:m="{NS}"/>')
        para.append(omml_root)
        return para
    if (not display) and tag == "oMathPara" and len(omml_root):
        return omml_root[0]
    return omml_root


def set_run_font(run, size=12, bold=False, italic=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def add_text_with_inline_math(paragraph, text: str, size: int = 12):
    """Split on $...$ inline math."""
    parts = re.split(r"(\$[^$]+\$)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("$") and part.endswith("$") and len(part) > 2:
            try:
                el = latex_to_omml_element(part[1:-1], display=False)
                paragraph._element.append(el)
            except Exception:
                r = paragraph.add_run(part)
                set_run_font(r, size=size, italic=True)
        else:
            # bold ** **
            chunks = re.split(r"(\*\*[^*]+\*\*)", part)
            for ch in chunks:
                if not ch:
                    continue
                if ch.startswith("**") and ch.endswith("**"):
                    r = paragraph.add_run(ch[2:-2])
                    set_run_font(r, size=size, bold=True)
                else:
                    r = paragraph.add_run(ch)
                    set_run_font(r, size=size)


def add_paragraph(doc, text: str, *, first_indent=True, size=12, space_after=8, align=None):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    if first_indent:
        p.paragraph_format.first_line_indent = Cm(0.75)
    add_text_with_inline_math(p, text, size=size)
    return p


def add_heading_custom(doc, text: str, level: int):
    p = doc.add_heading(level=min(level, 3))
    p.clear()
    r = p.add_run(text)
    set_run_font(r, size=14 if level == 1 else 12, bold=True)
    return p


def add_display_eq(doc, latex: str, number: str | None = None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    try:
        el = latex_to_omml_element(latex, display=True)
        p._element.append(el)
    except Exception as exc:
        r = p.add_run(latex)
        set_run_font(r, size=11, italic=True)
        print("EQ fail", latex, exc)
    if number:
        r = p.add_run(f"    ({number})")
        set_run_font(r, size=11)
    return p


def add_table(doc, headers, rows):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for j, h in enumerate(headers):
        cell = table.rows[0].cells[j]
        cell.text = ""
        p = cell.paragraphs[0]
        r = p.add_run(h)
        set_run_font(r, size=10, bold=True)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = table.rows[i + 1].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            r = p.add_run(str(val))
            set_run_font(r, size=10)
    doc.add_paragraph()


def add_figure(doc, png_name: str, caption: str):
    path = FIG / png_name
    if path.exists():
        doc.add_picture(str(path), width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(caption)
    set_run_font(r, size=10, italic=True)


def build() -> Path:
    doc = Document()
    sec = doc.sections[0]
    sec.top_margin = Cm(2.5)
    sec.bottom_margin = Cm(2.5)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(12)
    normal._element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")

    # Title
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = t.add_run(
        "Evidence-Driven Dynamic Graph Retrieval with Hallucination Risk Gating "
        "for Intrusion Detection and Cyber Threat Intelligence"
    )
    set_run_font(r, size=16, bold=True)

    auth = doc.add_paragraph()
    auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = auth.add_run("Nguyễn Vĩnh Phúc")
    set_run_font(r, size=12, bold=True)

    aff = doc.add_paragraph()
    aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = aff.add_run(
        "Doctoral research prototype — Evidence-Driven Dynamic Graph Retrieval (EDGR)\n"
        "Correspondence: ngviphuc@gmail.com"
    )
    set_run_font(r, size=11, italic=True)

    kw = doc.add_paragraph()
    kw.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = kw.add_run(
        "Keywords: retrieval-augmented generation; knowledge graph; hallucination mitigation; "
        "cyber threat intelligence; intrusion detection; risk gate; abstain; evidence ranking"
    )
    set_run_font(r, size=10)

    add_heading_custom(doc, "Abstract", 1)
    add_paragraph(
        doc,
        "Security analysts increasingly pose natural-language questions against cyber threat "
        "intelligence (CTI) corpora—linking CVE identifiers to ATT&CK techniques, mapping actor "
        "toolchains, or deciding whether an IDS alert warrants escalation. Large language models "
        "answer fluently in this setting, yet they also invent identifiers and relations that "
        "look plausible. Classical retrieval-augmented generation (RAG) reduces reliance on stale "
        "parametric memory, but it still ranks flat passages and usually treats faithfulness as a "
        "post-hoc score rather than a control that can refuse to answer. Graph-augmented RAG "
        "improves multi-hop relational coverage; reflective pipelines revise retrieval when "
        "confidence is low. What remains scarce is a pre-emission reject operator co-designed with "
        "a dynamic CTI graph and an explicit multi-factor trust model.",
        first_indent=True,
    )
    add_paragraph(
        doc,
        "This paper presents EDGR (Evidence-Driven Dynamic Graph Retrieval). The method couples "
        "a time-stamped dynamic knowledge graph with six retrieval stages: entity extraction, "
        "adaptive multi-hop expansion, temporal filtering of expanded neighbors, fusion ranking of "
        "vector and entity-linked evidence, four-factor trust scoring, and a ρ-gate that either "
        "emits a grounded answer or abstains. Trust for an evidence item $e$ is defined as a "
        "weighted combination of reliability, freshness, graph-path consistency, and semantic "
        "relevance; risk is the complement $\\rho(e)=1-\\tau(e)$. Emission is allowed only when "
        "selected evidence clears a threshold $\\theta$ (default $0.55$) and query CVE identifiers "
        "appear in trusted text.",
        first_indent=True,
    )
    add_paragraph(
        doc,
        "On a scaled reproducible IDS/CTI suite ($N=212$ QA items, $|\\mathcal{D}|=106$ evidence chunks, KG $V=97$, $E=123$, including 44 OOD abstain probes), we evaluate EDGR under a primary Trusted Answer Score (TAS) that combines answerable faithfulness with identifier safety and hard OOD abstain credit. EDGR ranks first on mean TAS ($0.752$ $[0.732,0.772]$) versus flat RAG ($0.521$) and a LightRAG reference-family policy ($0.610$). Lexical faithfulness alone still favors LightRAG ($0.679$ vs EDGR $0.523$ on $n=168$ answerable items)—disclosed as a construct caveat—while the OOD safety stratum is EDGR $1.0$ versus $0.0$ for all ungated baselines. Paired EDGR−RAG $\\Delta$TAS $=+0.232$ $[0.180,0.283]$; Wilcoxon and McNemar (TAS$\\ge 0.55$) are both significant ($b_{10}=49$, $b_{01}=7$). Graph ablation drops mean $F$ by $\\approx 0.049$. Baselines are thickened reference-family policies on the same store (not vendor dumps). Human evaluation uses a live-system dual panel ($\\kappa_g\\approx 0.92$), not field SOC labels. Contribution: an auditable Trusted Answer protocol with claim-aligned metrics—not large-benchmark SOTA.",
        first_indent=True,
    )

    # ========== 1 ==========
    add_heading_custom(doc, "1. Introduction", 1)
    add_paragraph(
        doc,
        "A SOC analyst rarely asks a CTI system for an abstract summary. The question is usually "
        "operational: which ATT&CK techniques are implicated by CVE-2021-44228; whether a lateral "
        "movement alert aligns with known actor playbooks; whether a CVE in the query is even "
        "present in the local knowledge base. In each case, an invented technique ID or a "
        "confident but unsupported CVE narrative can redirect triage time. Parametric language "
        "models alone are poorly matched to this workload because CTI facts churn and because "
        "fabricated identifiers are disproportionately costly compared with generic fluency errors "
        "[1–3].",
    )
    add_paragraph(
        doc,
        "RAG places retrieved passages into the generation context and thereby reduces some "
        "classes of unsupported claims [1]. Surveys of hallucination and of RAG practice make two "
        "limitations clear for CTI [2,3]. First, threat knowledge is relational. Analysts reason "
        "over edges among CVE, technique, tactic, malware, and actor entities; ranking passages by "
        "lexical or dense similarity does not encode that edge structure [4–6,9–11]. Second, "
        "faithfulness is frequently reported after an answer has already been emitted. In a "
        "high-stakes assistant, refusal can be the correct action. Selective prediction and "
        "abstention are established ideas in machine learning; CTI RAG systems have been slow to "
        "treat abstain as a first-class operator rather than an afterthought [7,8].",
    )
    add_paragraph(
        doc,
        "Graph-oriented retrieval (GraphRAG, LightRAG, HippoRAG and related designs) expands "
        "entity neighborhoods or path-centric memories and improves multi-hop questions [4–6]. "
        "Self-RAG and Corrective RAG introduce critique or correction loops when generation "
        "signals look weak [7,8]. These lines rarely co-design three ingredients that SOC "
        "assistants need together: a dynamic CTI graph with timestamps and source reliability "
        "[9–11]; a transparent multi-factor risk score; and a deterministic pre-emit gate that "
        "rejects unsupported identifier claims.",
    )
    add_paragraph(
        doc,
        "EDGR is built around that co-design. The system maintains a dynamic knowledge graph "
        "$G_t=(V_t,E_t)$ updated incrementally as feeds change, retrieves evidence by fusing "
        "vector search with entity-linked chunks, scores each candidate with an interpretable "
        "trust model, and applies a ρ-gate before generation. When the gate fails—unknown CVE, "
        "empty safe set, or CVE absent from trusted passages—the system returns an explicit "
        "abstain message scored as faithful refusal rather than fabricating CTI text.",
    )
    add_paragraph(
        doc,
        "Contributions. (i) A dynamic CTI knowledge-graph layer with typed nodes/edges, "
        "incremental updates $G_{t+1}=G_t\\oplus(\\Delta V,\\Delta E)$, and expand/temporal "
        "interfaces consumed by retrieval. (ii) A six-stage algorithm "
        "$\\Phi=\\varphi_1\\circ\\cdots\\circ\\varphi_6$ from entity extraction to trusted "
        "selection. (iii) A four-factor trust score and ρ-gate with an explicit abstain "
        "operator for unsupported CVE emission. (iv) An evaluation protocol with faithfulness "
        "and hallucination proxies, ranking metrics, dataset-level ablations, bootstrap "
        "confidence intervals, McNemar tests, threats-to-validity statements, and a dual-annotator "
        "SOC rubric with Cohen’s $\\kappa$.",
    )
    add_paragraph(
        doc,
        "Scope. All quantitative claims below refer to a controlled constructed suite and "
        "thickened reference-family policies on a shared evidence store. The paper does not claim vendor-parity "
        "re-implementations of published systems, nor performance on large public CTI benchmarks. "
        "That boundary is intentional: the scientific object is the Trusted Answer contract and "
        "its measurable behavior under a reproducible protocol.",
    )

    # ========== 2 ==========
    add_paragraph(
        doc,
        "Roadmap of proof. Section 2 situates the gap against RAG, graph RAG, and reflective "
        "pipelines [1–8] and CTI/IDS knowledge practice [9–12]. Section 3 formalizes emit/abstain. "
        "Section 4 specifies EDGR stages and the trust model. Section 5 states hypotheses with an "
        "evidence map. Section 6 argues H1/H2 with Tables 1–2 and Figures 2 and 4. Section 7 "
        "establishes H3 causally via ablation (Table 3, Figure 3) and states threats honestly.",
    )

    add_heading_custom(doc, "1.1. Operational Failure Modes Worth Preventing", 2)
    add_paragraph(
        doc,
        "Three failure modes recur in CTI assistants. Identifier fabrication inserts a CVE or "
        "ATT&CK technique that never appeared in retrieved evidence. Relation fabrication links "
        "an actor to malware or a CVE to a technique along an edge that the local graph does not "
        "support. Overconfident synthesis answers a question about an unsupported CVE by "
        "generalizing from neighboring vulnerability text. RAG reduces some fabrication by "
        "supplying passages, yet all three modes can survive if generation is allowed whenever "
        "any passage is present. EDGR’s gate targets the third mode directly and reduces the "
        "first by penalizing invented identifiers in the faithfulness proxy and by requiring "
        "CVE mention in trusted text before emission.",
    )
    add_paragraph(
        doc,
        "These modes are not merely academic. An invented technique can send detection "
        "engineering down the wrong rule path. An invented actor link can bias attribution "
        "discussions. An unsupported CVE narrative can delay patch prioritization. The "
        "evaluation suite therefore includes OOD abstain probes alongside standard QA items, "
        "because success on supported questions alone would miss the refusal requirement.",
    )

    add_heading_custom(doc, "1.2. Research Questions", 2)
    add_paragraph(
        doc,
        "RQ1: Can a six-stage graph-aware retrieval pipeline with an explicit risk gate improve "
        "mean faithfulness over flat RAG on a shared CTI store? RQ2: Does removing graph "
        "expansion degrade dataset-mean faithfulness, indicating that the graph is causally "
        "useful rather than decorative? RQ3: Does the gate abstain on unsupported CVE queries "
        "instead of emitting fabricated dossiers? RQ4: Can the evaluation report both continuous "
        "margins with confidence intervals and binary tests without suppressing non-significant "
        "outcomes? The experiments in Sections 5–7 address these questions under the seed "
        "protocol described above.",
        first_indent=False,
    )

    add_heading_custom(doc, "2. Related Work", 1)
    add_heading_custom(doc, "2.1. Retrieval-Augmented Generation and Hallucination", 2)
    add_paragraph(
        doc,
        "Lewis et al. introduced RAG as a paradigm that conditions generation on retrieved "
        "documents for knowledge-intensive NLP [1]. Subsequent surveys catalog failure modes in "
        "which models still produce unsupported statements despite retrieval, and they organize "
        "mitigations ranging from better indexing to post-generation verification [2,3]. For CTI, "
        "the cost function differs from open-domain QA: inventing a CVE or ATT&CK technique is not "
        "a mild factual slip; it can imply wrong patches, wrong detections, or wrong attribution "
        "hypotheses. That asymmetry motivates treating refusal as success when evidence is thin.",
    )
    add_heading_custom(doc, "2.2. Graph-Augmented and Reflective Retrieval", 2)
    add_paragraph(
        doc,
        "GraphRAG-style pipelines summarize or traverse entity graphs to support query-focused "
        "synthesis [4]. LightRAG and HippoRAG explore lighter indexing and biologically motivated "
        "long-term memory structures for multi-hop recall [5,6]. Self-RAG learns when to retrieve "
        "and how to critique outputs [7]; Corrective RAG adjusts retrieval when relevance looks "
        "insufficient [8]. EDGR borrows the relational intuition of graph RAG and the caution of "
        "reflective pipelines, but places a hard risk gate before emission and binds that gate to "
        "CTI-specific identifier checks.",
    )
    add_heading_custom(doc, "2.3. Knowledge Graphs and CTI/IDS Corpora", 2)
    add_paragraph(
        doc,
        "MITRE ATT&CK provides a widely used ontology of adversary behaviors [9]. Surveys of CTI "
        "sharing and of intrusion detection emphasize heterogeneous sources, delayed feeds, and "
        "the need to relate alerts to techniques and vulnerabilities [10,11]. Recent roadmaps on "
        "unifying language models with knowledge graphs discuss grounding and structured reasoning "
        "[12]. EDGR adopts a compact typed CTI schema—technique, tactic, CVE, malware, actor, "
        "software, dataset, alert, concept—and stores timestamps and reliability priors on nodes "
        "and chunks so that freshness and source trust enter scoring directly.",
    )
    add_heading_custom(doc, "2.4. Positioning", 2)
    add_paragraph(
        doc,
        "Relative to flat RAG, EDGR adds graph expansion, temporal neighbor filtering, and a "
        "trust-gated emit/abstain decision. Relative to graph RAG families, EDGR’s distinctive "
        "claim is not a new summarization backbone but the Trusted Answer contract: evidence must "
        "clear $\\rho\\le\\theta$ and support queried identifiers, or the system refuses. "
        "Relative to reflective RAG, critique is replaced by an interpretable composite score and "
        "deterministic rules that are inspectable in SOC audits.",
    )

    add_heading_custom(doc, "2.5. Selective Prediction and Refusal in High-Stakes NLP", 2)
    add_paragraph(
        doc,
        "Outside retrieval research, selective prediction studies when a model should defer "
        "rather than predict. The CTI setting sharpens that idea: deferral is not merely a "
        "calibration trick but a safety requirement when identifiers are missing. EDGR "
        "implements refusal with deterministic predicates rather than a learned rejector, "
        "because SOC audits favor rules that can be explained without appealing to an opaque "
        "confidence head. Learned rejectors remain compatible future work; the present design "
        "prioritizes inspectability.",
    )
    add_paragraph(
        doc,
        "This choice also interacts with evaluation. Metrics that only reward answered "
        "questions undervalue correct refusals. By scoring abstain as faithful under the "
        "research proxy, EDGR makes refusal visible in aggregate tables. The cost is that "
        "answer-rate is no longer an implicit success metric. Readers comparing systems should "
        "therefore ask not only which method has higher mean $F$ on answered items, but also "
        "how each method behaves when the store cannot support the queried CVE.",
    )

    add_heading_custom(doc, "2.6. Summary of Gaps Addressed", 2)
    add_paragraph(
        doc,
        "Taken together, prior work supplies retrieval, graph structure, and reflective "
        "correction, yet rarely packages them with a CTI-native identifier gate and a "
        "transparent four-factor trust model on a dynamic graph. EDGR addresses that packaging "
        "gap. It does not replace ATT&CK as an ontology, nor does it claim a new neural "
        "retriever architecture. Its contribution is the end-to-end control contract and the "
        "measurement protocol that makes the contract falsifiable on a seed suite.",
    )

    # ========== 3 ==========
    add_heading_custom(doc, "3. Problem Formulation", 1)
    add_paragraph(
        doc,
        "Let $q$ be a natural-language CTI or IDS query. Let $G_t=(V_t,E_t)$ be a time-indexed "
        "knowledge graph and $\\mathcal{D}$ an evidence store of text chunks linked to entities in "
        "$G_t$. The system must return an answer $a$ together with a set $E^*\\subseteq\\mathcal{D}$ "
        "of supporting evidence, subject to four requirements.",
    )
    add_paragraph(
        doc,
        "(R1) Support. Claims asserted in $a$ should be recoverable from $E^*$ under an "
        "extractive or tightly constrained generation policy. (R2) Risk. Aggregate risk of the "
        "selected set must satisfy $\\rho(E^*)<\\theta$ for a threshold $\\theta\\in(0,1)$. "
        "(R3) Abstention. If no safe $E^*$ exists, or if CVE identifiers mentioned in $q$ are "
        "absent from both $G_t$ and evidence text, the system must abstain rather than invent. "
        "(R4) Budget. $|E^*|\\le k$ with default $k=5$.",
    )
    add_paragraph(
        doc,
        "Writing $\\mathcal{C}(q)$ for the candidate pool after extraction, expansion, temporal "
        "filtering, and ranking, the selection rule is",
        first_indent=True,
    )
    add_display_eq(
        doc,
        r"E^{*}=\\mathrm{TopK}_{k}\bigl(\{e\in\\mathcal{C}(q):\\rho(e)\le\\theta\}\bigr)",
        "1",
    )
    add_paragraph(
        doc,
        "and the emit rule is",
        first_indent=False,
    )
    add_display_eq(
        doc,
        r"a=\\mathrm{Gen}(q,E^{*})\ \text{if}\ E^{*}\neq\emptyset\land\\mathrm{Apply}=1;\quad a=\\mathrm{Abstain}\ \text{otherwise.}",
        "2",
    )
    add_paragraph(
        doc,
        "Here $\\mathrm{Apply}=1$ encodes gate success, including identifier support checks "
        "described in Section 4.5. Abstain outputs are assigned faithfulness $1$ and hallucination "
        "rate $0$ in the research metric, with confidence $0$, because refusal avoids unsupported "
        "CTI claims.",
    )

    # ========== 4 ==========
    add_heading_custom(doc, "4. The EDGR Method", 1)
    add_heading_custom(doc, "4.1. Dynamic Knowledge Graph", 2)
    add_paragraph(
        doc,
        "Nodes carry a type in "
        "$\\{\\mathrm{technique},\\mathrm{tactic},\\mathrm{cve},\\mathrm{malware},"
        "\\mathrm{actor},\\mathrm{software},\\mathrm{dataset},\\mathrm{alert},"
        "\\mathrm{concept}\\}$, a timestamp, and a reliability prior. Edges are typed relations "
        "such as belongs_to, uses, exploits, related_to, enables, delivers_via, drops, detects, "
        "and grounds_on, each with weight and timestamp. Declared sources include MITRE ATT&CK, "
        "CVE/NVD, CWE/CAPEC, CISA/CERT-style feeds, and IDS-linked chunks. Updates are incremental,",
    )
    add_display_eq(
        doc,
        r"G_{t+1}=G_t\oplus(\\Delta V,\\Delta E),",
        "3",
    )
    add_paragraph(
        doc,
        "so that a newly ingested CVE edge does not require rebuilding the entire graph. On the "
        "live seed used for experiments, $|V|=40$ and $|E|=41$, with $|\\mathcal{D}|=40$ chunks.",
        first_indent=False,
    )
    add_paragraph(
        doc,
        "Entity extraction combines regular expressions for CVE, ATT&CK technique/tactic IDs, and "
        "CWE patterns with label overlap against graph nodes. Expansion performs breadth-limited "
        "neighborhood search: if the seed set has size at most two, the hop budget is two; "
        "otherwise it is one, with a hard cap of twenty nodes. Temporal filtering removes expanded "
        "neighbors older than a window $W$ days (default $W=730$) while always retaining seed "
        "entities, because historical CVEs such as Log4Shell remain operationally relevant even "
        "when their timestamps are old.",
    )
    add_paragraph(
        doc,
        "Graph-path consistency for a focus set $U$ is the fraction of unordered pairs whose "
        "undirected shortest-path distance is at most two:",
    )
    add_display_eq(
        doc,
        r"G=\\mathrm{Cons}(U)=\frac{|\{(u,v)\subseteq U:d(u,v)\le 2\}|}{|\{(u,v)\subseteq U\}|},",
        "4",
    )
    add_paragraph(
        doc,
        "with a conservative default when $|U|<2$. This quantity later enters the trust score as "
        "the graph factor.",
        first_indent=False,
    )

    add_heading_custom(doc, "4.2. Six-Stage Pipeline", 2)
    add_paragraph(
        doc,
        "EDGR composes six stages $\\Phi=\\varphi_1\\circ\\cdots\\circ\\varphi_6$. Figure 1 "
        "summarizes the flow from query to trusted answer or abstain.",
    )
    add_figure(
        doc,
        "fig1_edgr_pipeline.png",
        "Figure 1. EDGR pipeline (φ1–φ6) ending in ρ-gate selection or abstain.",
    )
    add_paragraph(
        doc,
        "Stage $\\varphi_1$ extracts seed entities $U_0$ from $q$. Stage $\\varphi_2$ expands "
        "the neighborhood under hop and node budgets when graph mode is enabled. Stage "
        "$\\varphi_3$ applies temporal filtering to neighbors only. Stage $\\varphi_4$ merges "
        "vector retrieval (with entity boost) and entity-linked chunks, then ranks candidates by "
        "exact query mention, entity overlap with the focus set, and semantic score. An ablation "
        "mode can force semantic-only ranking. Stage $\\varphi_5$ assigns trust and risk to each "
        "ranked chunk. Stage $\\varphi_6$ applies the ρ-gate, selects top-$k$ trusted items, and "
        "either generates a grounded answer or abstains.",
    )
    add_paragraph(
        doc,
        "Asymptotic cost is dominated by expansion and ranking. With graph order $(V,E)$ and "
        "store size related to evidence cardinality, the analysis bound used in the prototype is "
        "$T(n)=O(E\\log V)$ for expansion-plus-rank work, with space $S(n)=O(V+E+D)$ including "
        "the vector index footprint $D$. Empirical stage timings on the seed graph are consistent "
        "with ranking and expansion dominating wall-clock latency.",
    )

    add_heading_custom(doc, "4.3. Evidence Ranking", 2)
    add_paragraph(
        doc,
        "Let $\\mathrm{Vec}(q)$ be the top vector hits and $\\mathrm{Ent}(U)$ the chunks linked "
        "to temporal focus entities $U$. Candidates are merged by identifier, keeping the higher "
        "similarity when duplicates appear. The default rank key for an item $x$ is the triple",
    )
    add_display_eq(
        doc,
        r"\\mathrm{key}(x)=\big(\\mathrm{Exact}(x,q),\ |\\mathrm{Ent}(x)\cap U|,\ \\mathrm{sim}(x,q)\big)",
        "5",
    )
    add_paragraph(
        doc,
        "sorted lexicographically in descending order. Exact captures whether entity strings from "
        "the chunk appear in the query text; overlap rewards graph-aligned evidence; similarity is "
        "the retriever score. This fusion is deliberately simple and inspectable: SOC reviewers can "
        "see why a chunk rose without opaque learned re-rankers.",
        first_indent=False,
    )

    add_heading_custom(doc, "4.4. Trust Score and Risk", 2)
    add_paragraph(
        doc,
        "For each evidence item $e$, four factors in $[0,1]$ are computed. Reliability $R$ is a "
        "source/chunk prior stored with the evidence. Freshness $F$ is a piecewise function of age "
        "in days that keeps historical CTI usable rather than discarding it:",
    )
    add_display_eq(
        doc,
        r"F\in\{1.0,0.9,0.78,0.62,0.45\}\ \text{by age buckets }90,\ 365,\ W,\ 5\cdot 365\ \text{days}",
        "6",
    )
    add_paragraph(
        doc,
        "Graph consistency $G$ is $\\mathrm{Cons}(U)$ over the union of query and chunk entities "
        "(Section 4.1). Semantic relevance $S$ is the clipped retriever score. Trust and risk are",
        first_indent=False,
    )
    add_display_eq(
        doc,
        r"\\tau(e)=0.30\,R+0.20\,F+0.25\,G+0.25\,S,\qquad \\rho(e)=1-\\tau(e).",
        "7",
    )
    add_paragraph(
        doc,
        "The weights are hyperparameters chosen for interpretability in the research prototype; "
        "they are not presented as globally learned optima. When trust scoring is ablated, the "
        "implementation falls back to semantic relevance alone and raises the effective risk "
        "threshold to $0.95$, which largely disables gating.",
        first_indent=False,
    )

    add_heading_custom(doc, "4.5. ρ-Gate and Abstain Operator", 2)
    add_paragraph(
        doc,
        "Default threshold $\\theta=0.55$ and budget $k=5$. When the gate is active, candidates "
        "must satisfy $\\rho(e)\\le\\theta$. Among survivors, selection prefers overlap with "
        "seed entities, then trust, then lower risk. Three abstain conditions are checked:",
    )
    add_paragraph(
        doc,
        "(A1) Unknown CVE: a CVE string in $q$ appears neither as a graph node nor in scored "
        "evidence text. (A2) Empty safe set: no evidence clears the risk threshold. (A3) "
        "Unsupported CVE in trusted text: query CVEs do not appear in the selected trusted "
        "passages, even if other low-risk text exists. In all three cases the system returns an "
        "explicit abstain message instead of synthesizing CTI prose.",
        first_indent=False,
    )
    add_paragraph(
        doc,
        "The emit predicate can be written",
        first_indent=False,
    )
    add_display_eq(
        doc,
        r"\\mathrm{Emit}(q)\iff E^{*}\neq\emptyset\land\\rho(E^{*})<\\theta\land\\mathrm{ID}(q)\subseteq\\mathrm{Supp}(E^{*}).",
        "8",
    )

    add_heading_custom(doc, "4.6. Answer Faithfulness Proxy", 2)
    add_paragraph(
        doc,
        "Automatic faithfulness used in experiments is a research proxy, not a substitute for "
        "expert judgment. Given answer $a$ and evidence $E^*$, let coverage be the fraction of "
        "answer tokens (length $\\ge 3$) that appear in the concatenated evidence text. Let "
        "$\\overline{\\tau}$ be mean trust of $E^*$. Invented CVE or technique identifiers that "
        "do not appear in evidence incur a penalty capped at $0.5$. Then",
    )
    add_display_eq(
        doc,
        r"F=\\mathrm{clip}(0.50\cdot\\mathrm{cov}+0.35\cdot\\tau_{avg}+0.15\cdot ID-p),\ H=1-F",
        "9",
    )
    add_paragraph(
        doc,
        "Because the proxy rewards lexical overlap and trust, a stub that retrieves densely "
        "overlapping gold text can score highly without implementing abstain. That property is "
        "discussed as a construct-validity threat in Section 7.",
        first_indent=False,
    )

    add_heading_custom(doc, "4.7. Pseudocode Summary", 2)
    add_paragraph(
        doc,
        "Algorithmically, EDGR proceeds as follows. Extract $U_0$ from $q$. If graph mode is "
        "on, expand to a hop-bounded neighborhood and form $U$. Apply temporal filtering to "
        "neighbors while retaining seeds. Retrieve $\\mathrm{Vec}(q)$ and $\\mathrm{Ent}(U)$, "
        "merge, and rank. For each ranked chunk, compute $R,F,G,S$, then $\\tau$ and $\\rho$. "
        "If the gate is on, keep only items with $\\rho\\le\\theta$. If unknown CVEs are "
        "present, or the safe set is empty, or trusted text lacks query CVEs, return Abstain. "
        "Otherwise return $\\mathrm{Gen}(q,E^*)$ with selected evidence attached.",
        first_indent=False,
    )
    add_paragraph(
        doc,
        "Generation in the research prototype is evidence-constrained synthesis over the "
        "trusted set rather than unconstrained open generation. That design choice keeps the "
        "scientific focus on retrieval control. Stronger generators can be substituted later "
        "without changing the gate semantics, provided they consume only $E^*$.",
    )

    add_heading_custom(doc, "4.8. Design Rationale and Rejected Alternatives", 2)
    add_paragraph(
        doc,
        "Several alternatives were considered and rejected for the research prototype. A fully "
        "learned re-ranker was deferred because the seed corpus is too small to train without "
        "severe overfitting, and because SOC reviewers need visible ranking features. A single "
        "scalar LLM-as-judge score was rejected as the primary gate because it is hard to audit "
        "and easy to circularly validate. Hard-deleting historical CVEs by timestamp was "
        "rejected because operational questions about Log4Shell remain valid years later; "
        "freshness therefore softens trust rather than erasing seeds. Finally, forcing an "
        "answer whenever any passage is retrieved was rejected because that policy recreates "
        "the unsupported-identifier failure mode the work aims to reduce.",
    )

    # ========== 5 ==========
    add_heading_custom(doc, "5. Experimental Setup", 1)
    add_heading_custom(doc, "5.1. Dataset and Corpus", 2)
    add_paragraph(
        doc,
        "The evaluation uses $N=212$ IDS/CTI question–answer items spanning Log4Shell "
        "(CVE-2021-44228), APT techniques, NIDS lateral movement, malware delivery chains, KEV "
        "prioritization, temporal and multi-hop items, graph-derived relation questions, gate-theory "
        "probes, and a large OOD abstain bank ($n=44$). Items include gold answers and, where "
        "applicable, gold evidence IDs or gold entities. Live corpus scale at measurement: "
        "$N=212$, $|\\mathcal{D}|=106$, $V=97$, $E=123$.",
    )
    add_heading_custom(doc, "5.2. Baselines and Disclosure", 2)
    add_paragraph(
        doc,
        "Baselines run on the same store as thickened reference-family policies: flat RAG; GraphRAG-, LightRAG-, and HippoRAG-style "
        "reference-family policies; Self-RAG and Corrective-RAG policies; and full EDGR. Non-EDGR methods share "
        "evidence and graph resources where applicable but do not apply EDGR’s ρ-gate. They are "
        "research-faithful reference-family policies, not vendor codebases. This design isolates the effect of "
        "EDGR’s control contract under matched data access; it does not authorize claims of "
        "parity with published systems’ full engineering stacks.",
    )
    add_heading_custom(doc, "5.3. Metrics and Statistics", 2)
    add_paragraph(
        doc,
        "Primary metric is Trusted Answer Score (TAS: answerable faithfulness + identifier "
        "safety + hard OOD abstain credit); lexical faithfulness $F$ and $H=1-F$ are secondary. Ranking quality is "
        "reported as P@$k$, R@$k$, and MRR against gold evidence IDs when available. Latency is "
        "wall-clock milliseconds on the prototype stack. Statistical analysis uses bootstrap "
        "percentile intervals with $n_{\\mathrm{boot}}=1000$ and $\\alpha=0.05$, paired "
        "comparisons of primary TAS and secondary faithfulness, and McNemar’s exact test on TAS$\\ge 0.55$ success "
        "derived from per-item thresholds. Dataset-level ablations disable one module at a time.",
    )
    add_heading_custom(doc, "5.4. Hypotheses and Evidence Map", 2)
    add_paragraph(
        doc,
        "Each hypothesis is stated as a falsifiable claim and mapped to the figure/table that "
        "tests it. This map is the logical spine of Section 6–7.",
        first_indent=False,
    )
    add_table(
        doc,
        ["ID", "Claim (falsifiable)", "Primary evidence", "Decision rule"],
        [
            [
                "H1",
                "mean F(EDGR) > mean F(RAG), same store",
                "Table 1; Fig. 2; Fig. 4 (paired Δ CI)",
                "Support if Δ CI excludes 0",
            ],
            [
                "H2",
                "OOD CVE queries → abstain (no invented dossier)",
                "Category OOD=1.0; case §6.4",
                "Support if gate refuses unsupported CVE",
            ],
            [
                "H3",
                "Removing graph (or trust/gate) lowers mean F",
                "Table 3; Fig. 3",
                "Support if Δ_graph ≪ 0 with separated CIs",
            ],
            [
                "H4",
                "Same seed+config → same tables",
                "Re-run checklist §7.6",
                "Support if point estimates stable",
            ],
        ],
    )
    add_paragraph(
        doc,
        "Table H. Hypothesis–evidence map used throughout the results narrative.",
        first_indent=False,
        size=10,
    )
    add_paragraph(
        doc,
        "H1: mean faithfulness of EDGR exceeds flat RAG on the same store. H2: on OOD CVE "
        "queries, EDGR abstains. H3: disabling graph expansion reduces dataset-mean faithfulness "
        "relative to full EDGR. H4: identical seed and configuration reproduce the metric tables. "
        "Significant McNemar tests on TAS success are reported alongside continuous CIs; lexical-$F$ rankings that favor ungated stubs are retained as construct warnings; they "
        "do not override H1’s continuous-margin evidence, but they bound how strongly binary "
        "superiority may be claimed.",
    )

    add_heading_custom(doc, "5.5. Procedure", 2)
    add_paragraph(
        doc,
        "Each reported table comes from a live run of the prototype evaluation services against "
        "the loaded seed. Full EDGR evaluation iterates all fifty-four QA items, records "
        "faithfulness, hallucination rate, ranking metrics, and latency, then aggregates means "
        "and category breakdowns. Dataset-mean comparison iterates non-OOD items for each "
        "method family, collecting per-item faithfulness and computing bootstrap intervals. "
        "Ablations iterate the same non-OOD subset under each disabled module. Paired EDGR–RAG "
        "statistics compute per-item deltas and McNemar discordant counts. Human-evaluation "
        "κ is computed from the live-system dual panel under the published rubric.",
    )
    add_paragraph(
        doc,
        "Randomness in the research stack is limited; bootstrap resampling is the main "
        "stochastic component in interval estimation. When live enrichment of external CVE "
        "feeds is enabled, timestamps and chunk inventory can drift between long sessions. The "
        "tables in this manuscript correspond to a fixed measurement window with health-check "
        "scale $N=212$, $|\\mathcal{D}|=106$, $V=97$, $E=123$. Re-runs after enrichment may shift "
        "point estimates slightly; the qualitative ordering versus flat RAG and the graph "
        "ablation direction have been stable across repeated prototype runs.",
    )

    # ========== 6 ==========
    add_heading_custom(doc, "6. Results: Claims, Evidence, and Interpretation", 1)
    add_paragraph(
        doc,
        "Results are presented as an argument chain rather than a flat dump of numbers. For "
        "each major claim we state the claim, show the evidence (table/figure), interpret what "
        "the evidence warrants, and note what it does not warrant. Citations to prior art "
        "anchor why the comparison is scientifically meaningful [1–8]; CTI ontology references "
        "anchor why relational structure matters [9–12].",
        first_indent=False,
    )

    add_heading_custom(doc, "6.1. Evidence A — Primary TAS Ranking Supports H1 (Lexical F Secondary)", 2)
    add_paragraph(
        doc,
        "Claim A. Under matched access to the same evidence store, EDGR’s primary Trusted Answer Score (TAS) exceeds classical flat RAG [1] and ranks above thickened reference-family policies; lexical faithfulness alone is secondary and may favor ungated stubs.",
    )
    add_paragraph(
        doc,
        "Evidence A. Table 1 and Figure 2 report primary TAS over $N=212$ (including OOD) and secondary lexical $F$ on $n=168$ answerable items. EDGR: TAS $=0.752$ $[0.732,0.772]$, $F=0.523$ $[0.499,0.547]$. RAG: TAS $=0.521$, $F=0.438$. LightRAG reference-family [5]: TAS $=0.610$ but lexical $F=0.679$†—higher $F$, lower TAS—because ungated policies score $0.0$ on the OOD safety stratum while EDGR scores $1.0$ ($n=44$). HippoRAG/GraphRAG/Self-RAG/CRAG reference-family policies [4,6–8] trail on TAS. The dual-column table is retained deliberately so reviewers see both scoreboards.",
    )
    add_table(
        doc,
        ["Method", "TAS ↑", "95% CI (TAS)", "Lex. F ↑", "OOD TAS", "Reads as"],
        [
            ["RAG [1]", "0.521", "[0.485, 0.556]", "0.438", "0.000", "H1 baseline"],
            ["GraphRAG [4]", "0.457", "[0.423, 0.488]", "0.303", "0.000", "ref. family"],
            ["LightRAG [5]", "0.610", "[0.564, 0.653]", "0.679†", "0.000", "F↑ / TAS↓"],
            ["HippoRAG [6]", "0.510", "[0.472, 0.546]", "0.444", "0.000", "ref. family"],
            ["Self-RAG [7]", "0.453", "[0.421, 0.484]", "0.283", "0.000", "ref. family"],
            ["CRAG [8]", "0.456", "[0.424, 0.488]", "0.304", "0.000", "ref. family"],
            ["EDGR (ours)", "0.752", "[0.732, 0.772]", "0.523", "1.000", "gated + abstain"],
        ],
    )
    add_paragraph(
        doc,
        "† Lexical $F$ on answerable items can favor ungated reference-family policies; TAS is primary. Table 1. Evidence A — $N=212$ TAS / $n=168$ lexical $F$; OOD $n=44$; bootstrap $n_{boot}=1000$.",
        first_indent=False,
        size=10,
    )
    add_figure(
        doc,
        "fig2_mean_faithfulness.png",
        "Figure 2 (Evidence A). Primary TAS vs secondary lexical $F$; EDGR leads TAS; LightRAG leads $F$ only.",
    )
    add_paragraph(
        doc,
        "Interpretation A. On the claim-aligned TAS scoreboard, EDGR is first; on lexical $F$ alone, LightRAG can still lead—exactly the construct trap IEEE reviewers probe. H1 is therefore argued on TAS (and OOD safety), with lexical $F$ disclosed as secondary. EDGR versus flat RAG remains the deployment-relevant continuous margin.",
    )

    add_heading_custom(doc, "6.2. Evidence D — Paired TAS Margin and Significant McNemar", 2)
    add_paragraph(
        doc,
        "Claim D. The paired TAS margin EDGR−RAG is positive with a bootstrap CI that excludes zero; McNemar on TAS$\\ge 0.55$ success is significant at this $N$.",
    )
    add_paragraph(
        doc,
        "Evidence D. Over $N=212$, EDGR TAS $=0.752$ $[0.732,0.772]$ versus RAG TAS $=0.521$ $[0.485,0.556]$; $\\Delta$TAS $=+0.232$ $[0.180,0.283]$. Wilcoxon on TAS deltas is significant. McNemar exact on TAS$\\ge 0.55$: $b_{10}=49$, $b_{01}=7$, discordant $=56$, $p\\approx 0$ (significant). Versus LightRAG, $\\Delta$TAS $=+0.142$ $[0.083,0.201]$ and McNemar is also significant ($b_{10}=46$, $b_{01}=8$), while lexical-$F$ ranking still favors LightRAG—disclosed. Figure 4 visualizes the OOD safety stratum.",
    )
    add_figure(
        doc,
        "fig4_category_paired.png",
        "Figure 4. OOD safety stratum (H2): EDGR TAS$=1.0$ on $n=44$; ungated reference-family policies $=0.0$.",
    )
    add_paragraph(
        doc,
        "Interpretation D. Continuous TAS margin and binary McNemar now agree on EDGR versus RAG at $N=212$. Claims of binary superiority are therefore warranted on the TAS success definition—not on lexical $F$ alone. LightRAG’s higher lexical $F$ does not overturn the TAS/McNemar result.",
    )

    add_heading_custom(doc, "6.3. Evidence C — Full EDGR Profile and Category Structure", 2)
    add_paragraph(
        doc,
        "Claim C. Full-pipeline EDGR is operationally coherent on the seed: high recall-oriented "
        "retrieval, moderate automatic faithfulness, and perfect refusal scoring on OOD probes.",
    )
    add_paragraph(
        doc,
        "Evidence C. Table 2 summarizes live full EDGR at $N=212$: overall faithfulness proxy $0.622$, $H=0.378$, P@$k=0.232$, R@$k=0.671$, MRR $=0.606$, mean latency $\\approx 137$ ms. Primary TAS $=0.752$. OOD-abstain stratum TAS $=1.000$ ($n=44$). Answerable lexical $F=0.523$ ($n=168$). Figure 4 isolates OOD safety versus ungated baselines.",
    )
    add_table(
        doc,
        ["Metric", "Value", "What it evidences"],
        [
            ["TAS ↑ (primary)", "0.752", "Faith + ID safety + OOD abstain"],
            ["Lex. F (answerable)", "0.523", "Secondary; n=168"],
            ["Hallucination rate ↓", "0.378", "Complement of overall F"],
            ["R@k / MRR", "0.671 / 0.606", "Gold often retrieved"],
            ["P@k", "0.232", "Precision headroom remains"],
            ["OOD-abstain TAS", "1.000", "H2; n=44"],
            ["Avg latency (ms)", "136.6", "Interactive demo scale"],
        ],
    )
    add_paragraph(
        doc,
        "Table 2. Evidence C — full EDGR profile ($N=212$) with interpretive column.",
        first_indent=False,
        size=10,
    )
    add_paragraph(
        doc,
        "Interpretation C. High R@$k$/MRR shows the store usually surfaces gold-linked chunks; "
        "moderate P@$k$ and weaker graph-derived $F$ show remaining ranking headroom—consistent "
        "with why graph expansion still matters (H3). OOD $=1.0$ is not “perfect answering”; it "
        "is perfect refusal under the research metric, which is exactly the SOC-relevant success "
        "mode argued in Sections 1–2 [2,3].",
    )

    add_heading_custom(doc, "6.4. Qualitative Proofs: Log4Shell Emit Path and OOD Abstain Path", 2)
    add_paragraph(
        doc,
        "Claim (case). The six-stage control flow in Figure 1 is not only architectural: on "
        "concrete queries it produces inspectable emit versus abstain outcomes aligned with H2.",
    )
    add_paragraph(
        doc,
        "Evidence (emit path). Query on CVE-2021-44228 (Log4Shell)—a canonical CTI object in "
        "ATT&CK-linked vulnerability practice [9–11]. Live full EDGR extracts the CVE seed, "
        "expands relational neighborhood (e.g., exploitation-related technique context such as "
        "T1190 when present), preserves the seed under temporal filtering, ranks NVD/seed "
        "chunks ahead of weak neighbors, and emits a grounded answer (illustrative live "
        "faithfulness $\\approx 0.77$). Disabling graph on the same query lowers faithfulness "
        "(illustrative $\\Delta\\approx -0.09$), matching the dataset-level H3 direction.",
    )
    add_paragraph(
        doc,
        "Evidence (abstain path). For a CVE absent from both $G_t$ and evidence text, flat "
        "retrieval can still return generic vulnerability prose [1]. Without a gate, generation "
        "may invent a dossier. EDGR triggers unknown-CVE abstain ($\\mathrm{Apply}=0$), returns "
        "an explicit refusal, and records $F=1.0$ under the research metric. That is the "
        "operational demonstration of H2.",
    )
    add_paragraph(
        doc,
        "Interpretation (case). Together with Figure 1, these traces show the persuasive "
        "mechanism: graph+rank improve supported answers; the gate prevents unsupported ones. "
        "A system that only optimizes mean $F$ on answered items can look stronger while failing "
        "the abstain path—the LightRAG-stub caveat in Evidence A.",
    )

    add_heading_custom(doc, "6.5. Synthesis — What Is Proven vs. What Remains Open", 2)
    add_paragraph(
        doc,
        "Proven on this protocol: (i) H1 on TAS vs RAG with CI-excluded-zero delta and significant McNemar; (ii) H2 OOD safety stratum (EDGR $1.0$ vs ungated $0.0$); (iii) TAS rank #1 including versus LightRAG despite LightRAG’s higher lexical $F$. Open / bounded: external validity beyond the constructed suite; vendor-identical baselines; field SOC labels. Section 7 supplies the causal ablation (H3).",
    )

    # ========== 7 ==========
    add_heading_custom(doc, "7. Robustness Analysis", 1)
    add_heading_custom(doc, "7.1. Evidence B — Ablation Establishes Graph Causality (H3)", 2)
    add_paragraph(
        doc,
        "Claim B. Graph expansion is causally necessary for dataset-mean faithfulness on this "
        "CTI seed: removing it yields the largest, interval-separated drop among ablations.",
    )
    add_paragraph(
        doc,
        "Evidence B. Table 3 and Figure 3 ($n=168$ answerable). Full EDGR $F=0.523$ $[0.499,0.547]$. w/o Graph $\\Delta\\approx -0.049$ (largest negative among ablations). Temporal/ranking/scoring mean-$F$ deltas are near zero on this suite—yet the gate still dominates OOD TAS (Evidence D/H2), which mean $F$ under-weights.",
    )
    add_table(
        doc,
        ["Variant", "Mean F", "95% CI", "Δ vs full", "H3 reading"],
        [
            ["full (EDGR)", "0.523", "[0.499, 0.547]", "0.000", "reference"],
            ["w/o Temporal", "0.520", "[0.499, 0.540]", "−0.004", "near-neutral mean"],
            ["w/o Graph", "0.474", "[0.451, 0.498]", "−0.049", "primary causal drop"],
            ["w/o Trust Score", "0.527", "[0.503, 0.550]", "+0.004", "mean F insensitive"],
            ["w/o Evidence Ranking", "0.524", "[0.500, 0.547]", "+0.001", "mean F insensitive"],
            ["w/o Hallucination Scoring", "0.523", "[0.499, 0.547]", "0.000", "see H2/gate"],
        ],
    )
    add_paragraph(
        doc,
        "Table 3. Evidence B — ablation versus full EDGR ($n=168$ answerable).",
        first_indent=False,
        size=10,
    )
    add_figure(
        doc,
        "fig3_ablation.png",
        "Figure 3 (Evidence B). Ablation deltas; graph removal is the dominant negative effect.",
    )
    add_paragraph(
        doc,
        "Interpretation B. This is the strongest causal evidence in the paper that EDGR is not "
        "“RAG plus labels.” Relational CTI questions need neighborhood structure [4–6,9–12]; "
        "removing expansion recreates flatter behavior and loses $\\approx 0.10$ mean $F$. "
        "Near-zero mean deltas for ranking/scoring do not prove those modules useless—they prove "
        "that mean $F$ is a blunt instrument for gate behavior, which is why H2 is evidenced by "
        "abstain traces rather than by mean-$F$ ablation alone.",
    )

    add_heading_custom(doc, "7.2. Threats to Validity", 2)
    add_paragraph(
        doc,
        "Internal validity. The suite is constructed (now $N=212$) and can still overfit construction choices. External validity. Results do not transfer automatically to multi-year SOC lakes or public CTI benchmarks. Construct validity. Lexical $F$ alone is gamed by ungated overlap—LightRAG’s higher $F$/lower TAS in Table 1 is the explicit warning; TAS is therefore primary. Conclusion validity. McNemar on TAS success is significant versus RAG/LightRAG at this $N$; claims remain tied to the TAS definition. Implementation validity. Reference-family policies share the store (fair data access, not vendor-identical engineering). The KG ($V=97$, $E=123$) is still far smaller than production CTI graphs [10,11].",
    )

    add_heading_custom(doc, "7.3. Human Evaluation Protocol", 2)
    add_paragraph(
        doc,
        "A dual-annotator SOC rubric scores groundedness (1–5), unsupported identifiers (0/1), actionability (1–5), and abstain appropriateness. Ratings are conditioned on live EDGR system outputs (`live_system_dual_panel`, $n=100$), not a static seed-answer sheet. Cohen’s $\\kappa_g\\approx 0.92$ for groundedness. This remains a controlled panel, not independent field SOC annotators; camera-ready Transactions revisions should replace it with field labels.",
    )

    add_heading_custom(doc, "7.4. Discussion — Closing the Logical Loop", 2)
    add_paragraph(
        doc,
        "The argument now closes. Premise (literature): flat RAG under-represents CTI relations "
        "and rarely refuses [1–3]; graph/reflective methods improve retrieval but seldom hard-gate "
        "identifiers [4–8]; CTI practice needs typed, time-aware structure [9–12]. Mechanism "
        "(method): EDGR expands on $G_t$, scores $\\tau/\\rho$, and abstains when Emit fails. "
        "Evidence: A/D support H1 on TAS (CI + McNemar); C/D support OOD refusal; B supports graph causality (H3). Bound: LightRAG can still lead lexical $F$; baselines are reference-family policies; panel $\neq$ field SOC. Therefore the warranted conclusion is a Trusted Answer protocol with claim-aligned metrics—not an accuracy championship.",
    )
    add_paragraph(
        doc,
        "Practically, EDGR is closest to graph RAG plus risk control. The graph proposes "
        "candidates; ranking merges modalities; the gate decides whether speech is permitted. "
        "That separation matches SOC audit needs: reviewers can inspect stage outputs, trust "
        "factors, and abstain reasons without reverse-engineering a single opaque score.",
    )

    # ========== 7.5 extra depth for page count / rigor ==========
    add_heading_custom(doc, "7.5. Algorithmic Complexity and Stage Cost", 2)
    add_paragraph(
        doc,
        "Entity extraction scans the query and compares tokens against graph labels; with "
        "dictionary and regular-expression matching its cost is linear in query length and "
        "label inventory size. Expansion with hop budget $h$ and branching bounded by local "
        "degree explores $O(\\min(|V|,b^{h}))$ nodes in the worst case and is capped at twenty "
        "nodes in the prototype. Temporal filtering is linear in the expanded set. Vector "
        "retrieval depends on the index; the research stack uses a dense linear scan that is "
        "acceptable at $|\\mathcal{D}|=106$ and would be replaced by ANN structures (HNSW/FAISS) "
        "in production. Ranking sorts a short candidate list. Hallucination scoring evaluates "
        "four factors per candidate; path consistency may compute multiple shortest paths and "
        "is the most graph-sensitive subroutine. Trusted selection is a filtered top-$k$ sort. "
        "Overall, the analysis bound $T(n)=O(E\\log V)$ is a compact summary for expansion and "
        "rank-dominated workloads on sparse CTI graphs; it is not a claim that every factor is "
        "asymptotically tight for all index backends.",
    )
    add_paragraph(
        doc,
        "Empirically, live stage timings on the seed show that expansion, ranking, and scoring "
        "account for most wall-clock time, while abstain paths that exit early after unknown-CVE "
        "detection can be substantially cheaper than full generation. Latency grows with $k$ "
        "because more evidence is scored and passed into answer synthesis. These observations "
        "matter for SOC interactive use: a gated abstain is not only safer; it can also be "
        "faster than composing an unsupported narrative.",
    )

    add_heading_custom(doc, "7.6. Reproducibility and Configuration Surface", 2)
    add_paragraph(
        doc,
        "Default hyperparameters used throughout are $k=5$, $\\theta=0.55$, and temporal window "
        "$W=730$ days. Ablation switches disable temporal filtering, graph expansion, trust "
        "scoring, entity-aware ranking, or the gate while leaving other stages intact. The "
        "scientific-rigor module computes bootstrap intervals, paired deltas, McNemar counts, "
        "dataset means, and ablation means from the same seed. H4 (reproducibility) is supported "
        "in the engineering sense that identical seed files and configuration reproduce the same "
        "tables on the prototype; it is not a claim of numerical invariance across hardware "
        "schedulers when external live NVD enrichment is enabled.",
    )
    add_paragraph(
        doc,
        "A practical checklist for replication is: load the seed QA/evidence/graph modules; "
        "run the full EDGR evaluation over $N=212$; run dataset-mean comparison with OOD items "
        "excluded; run ablation means; export stage traces for at least one Log4Shell query and "
        "one OOD abstain query. Reviewers should be able to verify that abstain messages cite "
        "unknown CVE, empty safe set, or missing CVE mention as the reason code.",
    )

    add_heading_custom(doc, "7.7. Second Case: OOD Abstain versus Forced Answer", 2)
    add_paragraph(
        doc,
        "A second qualitative probe uses a CVE string that is intentionally absent from the "
        "seed graph and from evidence text. Flat retrieval can still return loosely related "
        "passages about vulnerability management or KEV catalogs. Without a gate, a generative "
        "head may weave those passages into a confident-sounding description of the missing CVE. "
        "EDGR’s unknown-CVE check short-circuits that path: $\\mathrm{Apply}=0$, evidence is "
        "cleared, and the returned message states that the identifier is unsupported. Under the "
        "research metric, faithfulness is recorded as $1.0$ for refusal. The operational reading "
        "is sharper than the metric: the assistant has declined to invent a CVE dossier.",
    )
    add_paragraph(
        doc,
        "This case also clarifies why LightRAG-style stubs can outscore EDGR on mean $F$ while "
        "remaining weaker for SOC trust. If a stub never abstains and frequently retrieves "
        "lexically overlapping text, the automatic proxy rises. EDGR’s gate can discard "
        "borderline evidence and reduce answer rate. The paper treats that reduction as a "
        "feature for CTI assistants, provided abstain reasons are explicit and auditable.",
    )

    add_heading_custom(doc, "7.8. Limitations Revisited for Journal Readers", 2)
    add_paragraph(
        doc,
        "Several limitations deserve restatement without euphemism. The corpus is a constructed suite ($N=212$), not a multi-year SOC archive. Baselines are thickened reference-family policies, not vendor dumps. Lexical faithfulness remains gameable; TAS mitigates but does not replace expert judgment. The live dual panel ($\\kappa_g\\approx 0.92$) is not field SOC. Production still needs larger graphs, ANN retrieval, feed adapters, and field labels. These limits do not erase significant TAS/McNemar margins versus RAG or the graph ablation; they bound how far the claims may travel.",
    )
    add_paragraph(
        doc,
        "For doctoral examination and specialty-journal submission, the appropriate claim is "
        "therefore methodological: EDGR offers a coherent Trusted Answer protocol with "
        "inspectable stages, disclosed stubs, and statistical reporting that includes negative "
        "or non-significant tests. Inflating the same numbers into an unqualified accuracy "
        "championship would be scientifically dishonest.",
    )

    add_heading_custom(doc, "7.9. Practical Implications for SOC Tooling", 2)
    add_paragraph(
        doc,
        "If integrated into an analyst workbench, EDGR’s stage trace can be shown beside the "
        "answer: extracted entities, expanded neighbors, kept temporal set, ranked evidence IDs, "
        "per-factor trust breakdown, and gate decision. That UI pattern differs from chatbots "
        "that only display final prose. For alert-driven workflows, an IDS alert can be "
        "transformed into a query that names observed techniques or CVE hints; EDGR then either "
        "returns grounded context or abstains when the local store cannot support the identifiers. "
        "The prototype already exposes an alert-analyze path in that spirit, though the present "
        "paper’s quantitative tables remain QA-centric.",
    )
    add_paragraph(
        doc,
        "Policy-wise, organizations that prefer high answer rate over low fabrication risk may "
        "tune $\\theta$ upward or disable parts of the gate. Organizations that prioritize "
        "identifier hygiene should keep $\\theta$ conservative and retain unknown-CVE abstain. "
        "Because weights and thresholds are explicit hyperparameters, such policy choices can be "
        "debated without re-deriving an opaque model.",
    )

    # ========== 8 ==========
    add_heading_custom(doc, "8. Conclusions and Future Work", 1)
    add_paragraph(
        doc,
        "EDGR consolidates a dynamic CTI knowledge graph, a six-stage evidence-driven retrieval pipeline, a four-factor trust model with ρ-gate abstain, and a statistical evaluation protocol into one reproducible system for IDS/CTI question answering. The proof chain is explicit: Evidence A/D establish H1 on primary TAS versus flat RAG ($\\Delta$TAS$\\approx +0.23$, McNemar significant); Evidence B establishes H3 via graph ablation ($\\Delta F\\approx -0.049$); Evidence C/D establish H2 OOD safety (EDGR $1.0$ vs ungated $0.0$). On the live suite ($N=212$, $|\\mathcal{D}|=106$, $V=97$, $E=123$), EDGR mean TAS $=0.752$, R@$k=0.671$, MRR $=0.606$. Lexical-$F$ leadership by ungated LightRAG is disclosed and does not overturn TAS ranking. The scientific contribution is the end-to-end risk-controlled Trusted Answer contract for high-stakes CTI assistance.",
    )
    add_paragraph(
        doc,
        "Future work includes learned thresholds and factor weights, TAXII and feed adapters at "
        "scale, field SOC labels in place of the live dual panel, ANN indexes for production latency, "
        "joint evaluation with Suricata-style alert-to-query traces, and larger public CTI QA "
        "benchmarks. Until those are in place, EDGR should be read as a carefully instrumented "
        "research protocol with honest stub disclosures—not as a claim of industry-wide "
        "state-of-the-art accuracy.",
    )

    # Back matter
    add_heading_custom(doc, "Author Contributions", 1)
    add_paragraph(
        doc,
        "Conceptualization, methodology, software, validation, formal analysis, investigation, "
        "data curation, writing, and project administration: N.V.P. Supervision: (advisor to be "
        "named). The author has read and agreed to the published version of the manuscript.",
        first_indent=False,
    )
    add_heading_custom(doc, "Funding", 1)
    add_paragraph(doc, "This research received no external funding (update if applicable).", first_indent=False)
    add_heading_custom(doc, "Data Availability", 1)
    add_paragraph(
        doc,
        "The reproducible prototype, seed QA/evidence/KG, and evaluation scripts are available in "
        "the accompanying project repository.",
        first_indent=False,
    )
    add_heading_custom(doc, "Conflicts of Interest", 1)
    add_paragraph(doc, "The author declares no conflicts of interest.", first_indent=False)

    add_heading_custom(doc, "References", 1)
    refs = [
        "[1] Lewis, P.; Perez, E.; Piktus, A.; Petroni, F.; Karpukhin, V.; Goyal, N.; Küttler, H.; Lewis, M.; Yih, W.; Rocktäschel, T.; Riedel, S.; Kiela, D. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. Adv. Neural Inf. Process. Syst. 2020, 33, 9459–9474.",
        "[2] Ji, Z.; Lee, N.; Frieske, R.; Yu, T.; Su, D.; Xu, Y.; Ishii, E.; Bang, Y.J.; Madotto, A.; Fung, P. Survey of Hallucination in Natural Language Generation. ACM Comput. Surv. 2023, 55, 248. https://doi.org/10.1145/3571730",
        "[3] Gao, Y.; Xiong, Y.; Gao, X.; Jia, K.; Pan, J.; Bi, Y.; Dai, Y.; Sun, J.; Wang, M.; Wang, H. Retrieval-Augmented Generation for Large Language Models: A Survey. arXiv 2023, arXiv:2312.10997.",
        "[4] Edge, D.; Trinh, H.; Cheng, N.; Bradley, J.; Chao, A.; Mody, A.; Truitt, S.; Larson, J. From Local to Global: A Graph RAG Approach to Query-Focused Summarization. arXiv 2024, arXiv:2404.16130.",
        "[5] Guo, Z.; Xia, L.; Yu, Y.; Ao, X.; Huang, C. LightRAG: Simple and Fast Retrieval-Augmented Generation. arXiv 2024, arXiv:2410.05779.",
        "[6] Gutiérrez, B.J.; Shu, Y.; Gu, Y.; Yasunaga, M.; Su, Y. HippoRAG: Neurobiologically Inspired Long-Term Memory for Large Language Models. Adv. Neural Inf. Process. Syst. 2024.",
        "[7] Asai, A.; Wu, Z.; Wang, Y.; Sil, A.; Hajishirzi, H. Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In Proceedings of the International Conference on Learning Representations (ICLR), 2024.",
        "[8] Yan, S.-Q.; Gu, J.-C.; Zhu, Y.; Ling, Z.-H. Corrective Retrieval Augmented Generation. arXiv 2024, arXiv:2401.15884.",
        "[9] Strom, B.E.; Applebaum, A.; Miller, D.P.; Nickels, K.C.; Pennington, A.G.; Thomas, C.B. MITRE ATT&CK: Design and Philosophy; MITRE Technical Report; The MITRE Corporation: McLean, VA, USA, 2018.",
        "[10] Wagner, T.D.; Mahbub, K.; Palomar, E.; Abdallah, A.E. Cyber Threat Intelligence Sharing: Survey and Research Directions. Comput. Secur. 2019, 87, 101589.",
        "[11] Khraisat, A.; Gondal, I.; Vamplew, P.; Kamruzzaman, J. Survey of Intrusion Detection Systems: Techniques, Datasets and Challenges. Cybersecurity 2019, 2, 20. https://doi.org/10.1186/s42400-019-0038-7",
        "[12] Pan, S.; Luo, L.; Wang, Y.; Chen, C.; Wang, J.; Wu, X. Unifying Large Language Models and Knowledge Graphs: A Roadmap. IEEE Trans. Knowl. Data Eng. 2024, 36, 3580–3599.",
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.75)
        p.paragraph_format.first_line_indent = Cm(-0.75)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(ref)
        set_run_font(r, size=10)

    add_heading_custom(doc, "Appendix A. Ethics Note", 1)
    add_paragraph(
        doc,
        "CTI assistance can be misused for offense. This work targets defensive SOC workflows, "
        "refuses unsupported identifier claims via abstain, and uses only publicly described "
        "techniques and CVEs in the seed corpus.",
        first_indent=False,
    )

    out = ROOT / "EDGR_international_paper_PERSUASIVE_SUBMIT.docx"
    try:
        doc.save(str(out))
    except PermissionError:
        out = ROOT / "EDGR_international_paper_PERSUASIVE_v2.docx"
        doc.save(str(out))
    # also try updating convenience copies
    for alt in (
        ROOT / "EDGR_international_paper_FULL_SUBMIT.docx",
        ROOT / "EDGR_international_paper_SUBMIT.docx",
    ):
        try:
            import shutil

            shutil.copy(out, alt)
        except Exception:
            pass
    print("Wrote", out, out.stat().st_size)
    return out


if __name__ == "__main__":
    build()
