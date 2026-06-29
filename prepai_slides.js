const PptxGenJS = require("pptxgenjs");

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // 13.3" x 7.5"

// ─── Design Tokens ─────────────────────────────────────────────
const DARK   = "0F172A"; // deep navy-slate
const ACCENT = "38BDF8"; // sky blue
const PURPLE = "7C3AED"; // purple / agent highlight
const GREEN  = "10B981"; // green / success
const LIGHT  = "F1F5F9"; // slide background (light slides)
const WHITE  = "FFFFFF";
const MUTED  = "94A3B8"; // secondary text on dark
const DARK_TEXT = "1E293B";

// helper: adds a faint grid of dots (decorative) on dark slides
function darkBg(slide) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: "100%", h: "100%", fill: { color: DARK }, line: { color: DARK } });
  // accent bar top-left
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.06, h: "100%", fill: { color: ACCENT }, line: { color: ACCENT } });
}

function lightBg(slide) {
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: "100%", h: "100%", fill: { color: LIGHT }, line: { color: LIGHT } });
  slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 0.06, h: "100%", fill: { color: PURPLE }, line: { color: PURPLE } });
}

function card(slide, x, y, w, h, fillColor) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h,
    fill: { color: fillColor || "1E293B" },
    line: { color: fillColor || "1E293B" },
    rectRadius: 0.12,
    shadow: { type: "outer", blur: 8, offset: 4, angle: 45, color: "000000", opacity: 0.25 }
  });
}

// ══════════════════════════════════════════════════════════════════
// SLIDE 1 — TITLE
// ══════════════════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  darkBg(slide);

  // Speaker Notes
  slide.addNotes("Good morning, everyone! I'm Aramish Farooq, a Computer Engineering student at San Jose State. Today, I'm really excited to share my week 1 project: PrepAI. PrepAI is an AI-powered interview coach built specifically to solve the biggest issues with mock interview tools today: generic questions and non-actionable feedback. In this presentation, I'll walk you through the core problem, the RAG and LangGraph agent architecture under the hood, how the live demo flow works, and then we'll jump straight into the demo. Let's get started.");

  // large glowing circle backdrop (decorative)
  slide.addShape(pptx.ShapeType.ellipse, { x: 7.8, y: -1.2, w: 5.5, h: 5.5, fill: { color: "1E3A5F", transparency: 40 }, line: { color: "1E3A5F", transparency: 40 } });
  slide.addShape(pptx.ShapeType.ellipse, { x: 9.0, y: -0.3, w: 3.2, h: 3.2, fill: { color: ACCENT, transparency: 75 }, line: { color: ACCENT, transparency: 75 } });

  // Pill tag: "Week 1 Intern Showcase"
  card(slide, 0.6, 0.55, 3.1, 0.42, "1E293B");
  slide.addText("⚡  WEEK 1 · INTERN SHOWCASE", {
    x: 0.62, y: 0.56, w: 3.06, h: 0.38,
    fontSize: 9, bold: true, color: ACCENT, align: "center", fontFace: "Segoe UI"
  });

  // Main Title
  slide.addText("PrepAI", {
    x: 0.6, y: 1.25, w: 7, h: 1.5,
    fontSize: 80, bold: true, color: WHITE, fontFace: "Segoe UI Black"
  });

  // Tagline
  slide.addText("Your AI-powered interview coach that knows who you are\nand adapts to how you're performing — in real time.", {
    x: 0.6, y: 2.75, w: 8.2, h: 1.0,
    fontSize: 18, color: MUTED, fontFace: "Segoe UI", lineSpacingMultiple: 1.4
  });

  // Separator line
  slide.addShape(pptx.ShapeType.rect, { x: 0.6, y: 3.85, w: 4.5, h: 0.03, fill: { color: ACCENT }, line: { color: ACCENT } });

  // Name + date
  slide.addText("Aramish Farooq   ·   San Jose State University", {
    x: 0.6, y: 4.0, w: 7, h: 0.4,
    fontSize: 14, color: WHITE, fontFace: "Segoe UI", bold: true
  });
  slide.addText("Summer 2025  ·  Friday June 27", {
    x: 0.6, y: 4.42, w: 7, h: 0.35,
    fontSize: 12, color: MUTED, fontFace: "Segoe UI"
  });

  // Tech stack pills (bottom-right)
  const pills = [
    { label: "LangGraph", color: PURPLE },
    { label: "ChromaDB RAG", color: "0F766E" },
    { label: "Claude API", color: "B45309" },
    { label: "Streamlit", color: "1D4ED8" },
  ];
  let px = 0.6;
  pills.forEach(p => {
    const w = p.label.length * 0.092 + 0.5;
    card(slide, px, 5.5, w, 0.38, p.color);
    slide.addText(p.label, { x: px + 0.05, y: 5.51, w: w - 0.1, h: 0.36, fontSize: 10, color: WHITE, fontFace: "Segoe UI", bold: true, align: "center" });
    px += w + 0.15;
  });
}

// ══════════════════════════════════════════════════════════════════
// SLIDE 2 — THE PROBLEM
// ══════════════════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  lightBg(slide);

  // Speaker Notes
  slide.addNotes("So, why did I build PrepAI? If you've ever tried preparing for a technical interview using standard AI tools like ChatGPT, you've probably run into these three major issues. First, the feedback is generic. It doesn't know what's actually on your resume, so it can't grill you on your specific project claims. Second, standard tools don't adapt. They don't react to how you're performing during the interview. And third, they don't give you any structured analytics or a roadmap to improve. You just get a wall of text. We wanted to solve these three pain points by creating a tool that actually listens, scores you dynamically on 6 core dimensions in real time, and constructs a personalized 30-day action plan.");

  slide.addText("The Problem", {
    x: 0.55, y: 0.4, w: 9, h: 0.65,
    fontSize: 36, bold: true, color: DARK_TEXT, fontFace: "Segoe UI Black"
  });
  slide.addText("Why interview prep today is fundamentally broken", {
    x: 0.55, y: 1.05, w: 9, h: 0.4,
    fontSize: 15, color: "64748B", fontFace: "Segoe UI"
  });

  // Three pain-point cards
  const problems = [
    { icon: "💀", title: "Generic Feedback", body: "Chatbots give the same canned advice to everyone.\nThey don't know your projects or your resume." },
    { icon: "🎯", title: "No Adaptation", body: "One-size-fits-all questions ignore how you're\nactually performing in real time." },
    { icon: "📊", title: "Zero Analytics", body: "You finish a mock interview with no data — no scores,\nno patterns, no actionable improvement plan." },
  ];

  problems.forEach((p, i) => {
    const x = 0.55 + i * 4.15;
    card(slide, x, 1.75, 3.9, 3.55, WHITE);
    // icon circle
    slide.addShape(pptx.ShapeType.ellipse, { x: x + 1.55, y: 2.0, w: 0.8, h: 0.8, fill: { color: "EDE9FE" }, line: { color: "EDE9FE" } });
    slide.addText(p.icon, { x: x + 1.55, y: 2.0, w: 0.8, h: 0.8, fontSize: 22, align: "center", valign: "middle" });
    slide.addText(p.title, { x: x + 0.15, y: 2.9, w: 3.6, h: 0.42, fontSize: 16, bold: true, color: DARK_TEXT, fontFace: "Segoe UI", align: "center" });
    slide.addText(p.body, { x: x + 0.15, y: 3.38, w: 3.6, h: 1.6, fontSize: 12, color: "475569", fontFace: "Segoe UI", align: "center", lineSpacingMultiple: 1.4 });
  });

  // Bottom stat
  card(slide, 0.55, 5.55, 12.2, 0.62, "EDE9FE");
  slide.addText("💡  77% of job seekers say interview anxiety is their #1 barrier — even when they're qualified.", {
    x: 0.7, y: 5.6, w: 12.0, h: 0.52,
    fontSize: 13, color: PURPLE, bold: true, fontFace: "Segoe UI", align: "center"
  });
}

// ══════════════════════════════════════════════════════════════════
// SLIDE 3 — ARCHITECTURE
// ══════════════════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  darkBg(slide);

  // Speaker Notes
  slide.addNotes("Let's look at the technical architecture. PrepAI is built on two core layers. First, we have the RAG knowledge layer. When you upload your resume or paste a job description, we parse the text and ingest it into a ChromaDB vector database. At runtime, our agents perform semantic search queries against this store so they have full context on your background.\nSecond, we orchestrate the conversation using LangGraph. We have a Profiler Agent that reads the resume to create a 'Player Card' detailing your skills and gaps. Next, the Interviewer Agent generates tailored questions based on your background and the target role. Then, we use a LangGraph stateful interrupt node to pause execution and wait for human input. Finally, when you submit, the Evaluator Agent scores your answer across 6 dimensions and outputs structured JSON containing your score, strengths, and weaknesses, looping back to the next question.");

  slide.addText("Under the Hood", {
    x: 0.55, y: 0.32, w: 12, h: 0.65,
    fontSize: 36, bold: true, color: WHITE, fontFace: "Segoe UI Black"
  });
  slide.addText("RAG Pipeline  +  LangGraph Multi-Agent Orchestration", {
    x: 0.55, y: 0.96, w: 12, h: 0.36,
    fontSize: 14, color: ACCENT, fontFace: "Segoe UI"
  });

  // ── Row 1: RAG Layer ──────────────────────────────────────────
  slide.addText("① RAG KNOWLEDGE LAYER", { x: 0.55, y: 1.52, w: 12, h: 0.3, fontSize: 10, bold: true, color: MUTED, fontFace: "Segoe UI" });

  const ragBoxes = [
    { label: "Resume PDF", sub: "Uploaded by user", color: "0F766E" },
    { label: "Job Description", sub: "URL / PDF / Text", color: "0F766E" },
    { label: "ChromaDB", sub: "Vector Store", color: PURPLE },
    { label: "RAG Retriever", sub: "Semantic search at runtime", color: PURPLE },
  ];
  ragBoxes.forEach((b, i) => {
    const x = 0.55 + i * 3.2;
    card(slide, x, 1.88, 3.0, 0.88, b.color);
    slide.addText(b.label, { x: x + 0.1, y: 1.92, w: 2.8, h: 0.44, fontSize: 14, bold: true, color: WHITE, fontFace: "Segoe UI", align: "center" });
    slide.addText(b.sub, { x: x + 0.1, y: 2.35, w: 2.8, h: 0.3, fontSize: 9, color: "BAE6FD", fontFace: "Segoe UI", align: "center" });
    // arrow between boxes
    if (i < 3) slide.addText("→", { x: x + 3.0, y: 2.1, w: 0.2, h: 0.42, fontSize: 16, color: MUTED, align: "center" });
  });

  // ── Row 2: Agent Layer ───────────────────────────────────────
  slide.addText("② LANGGRAPH AGENT PIPELINE", { x: 0.55, y: 3.1, w: 12, h: 0.3, fontSize: 10, bold: true, color: MUTED, fontFace: "Segoe UI" });

  const agents = [
    { emoji: "🔍", label: "Profiler Agent", sub: "Parses resume → builds Player Card (skills, projects, gaps)" },
    { emoji: "🎙️", label: "Interviewer Agent", sub: "Generates contextual, adaptive questions using RAG context" },
    { emoji: "👤", label: "Human Input Node", sub: "LangGraph interrupt — pauses for candidate to type answer" },
    { emoji: "📊", label: "Evaluator Agent", sub: "Scores on 6 dimensions, returns JSON with strength & weakness" },
  ];

  agents.forEach((a, i) => {
    const x = 0.55 + i * 3.2;
    card(slide, x, 3.45, 3.0, 2.6, "1E293B");
    slide.addText(a.emoji, { x: x + 1.1, y: 3.6, w: 0.8, h: 0.7, fontSize: 28, align: "center" });
    slide.addText(a.label, { x: x + 0.1, y: 4.33, w: 2.8, h: 0.4, fontSize: 12, bold: true, color: ACCENT, fontFace: "Segoe UI", align: "center" });
    slide.addText(a.sub, { x: x + 0.12, y: 4.78, w: 2.76, h: 1.1, fontSize: 9.5, color: "CBD5E1", fontFace: "Segoe UI", align: "center", lineSpacingMultiple: 1.35 });
    if (i < 3) slide.addText("→", { x: x + 3.0, y: 4.55, w: 0.2, h: 0.4, fontSize: 18, color: ACCENT, align: "center" });
  });

  // loop-back annotation
  slide.addShape(pptx.ShapeType.rect, { x: 12.68, y: 3.45, w: 0.02, h: 2.6, fill: { color: PURPLE }, line: { color: PURPLE } });
  slide.addText("↩  Loop until max turns", { x: 9.7, y: 6.2, w: 3.1, h: 0.3, fontSize: 9, color: PURPLE, fontFace: "Segoe UI", bold: true });
}

// ══════════════════════════════════════════════════════════════════
// SLIDE 4 — LIVE DEMO FLOW
// ══════════════════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  lightBg(slide);

  // Speaker Notes
  slide.addNotes("Here's exactly what you'll see in the demo today. We'll start with an instant-start setup using a default resume and a Tesla ML Intern job description so we don't waste time typing. Once we click start, the Profiler Agent analyzes the resume. Then, the Interviewer Agent asks two highly specific questions about the projects listed on the resume. In the sidebar, you'll see live analytics update in real time after every answer, showing score bars color-coded from red to green, the lowest scoring dimension, and top patterns. Finally, once the session ends, a full 30-day action plan is generated dynamically. The entire end-to-end interview takes under 90 seconds.");

  slide.addText("What You'll See in the Demo", {
    x: 0.55, y: 0.38, w: 12, h: 0.65,
    fontSize: 36, bold: true, color: DARK_TEXT, fontFace: "Segoe UI Black"
  });
  slide.addText("A 2-question live interview — from cold start to scored report in under 90 seconds", {
    x: 0.55, y: 1.05, w: 12, h: 0.38,
    fontSize: 14, color: "64748B", fontFace: "Segoe UI"
  });

  // Step cards (horizontal flow)
  const steps = [
    { num: "01", icon: "⚡", title: "Instant Start", body: "Select default resume &\njob description (Tesla ML\nIntern). One click." },
    { num: "02", icon: "🤖", title: "Profiler Runs", body: "Agents read the resume\nand build a rich\ncandidate profile." },
    { num: "03", icon: "🎙️", title: "Adaptive Q&A", body: "Interviewer asks hyper-\nspecific questions about\nyour actual projects." },
    { num: "04", icon: "📊", title: "Live Analytics", body: "Score bars, lowest\ndimension tracker, and\npatterns update live." },
    { num: "05", icon: "🚀", title: "Action Plan", body: "30-day improvement\nplan generated from\nyour weakest scores." },
  ];

  steps.forEach((s, i) => {
    const x = 0.32 + i * 2.58;
    card(slide, x, 1.72, 2.4, 4.0, WHITE);
    // number badge
    slide.addShape(pptx.ShapeType.ellipse, { x: x + 0.9, y: 1.9, w: 0.6, h: 0.6, fill: { color: PURPLE }, line: { color: PURPLE } });
    slide.addText(s.num, { x: x + 0.9, y: 1.9, w: 0.6, h: 0.6, fontSize: 10, bold: true, color: WHITE, fontFace: "Segoe UI", align: "center", valign: "middle" });
    slide.addText(s.icon, { x: x + 0.6, y: 2.6, w: 1.2, h: 0.7, fontSize: 26, align: "center" });
    slide.addText(s.title, { x: x + 0.1, y: 3.38, w: 2.2, h: 0.44, fontSize: 13, bold: true, color: DARK_TEXT, fontFace: "Segoe UI", align: "center" });
    slide.addText(s.body, { x: x + 0.1, y: 3.85, w: 2.2, h: 1.6, fontSize: 11, color: "475569", fontFace: "Segoe UI", align: "center", lineSpacingMultiple: 1.35 });
    // connector arrow
    if (i < 4) slide.addText("›", { x: x + 2.4, y: 3.45, w: 0.18, h: 0.4, fontSize: 22, color: PURPLE, bold: true, align: "center" });
  });

  // Key features strip
  const features = ["✅  Default resume & JD for instant testing", "✅  6-dimension scoring bars (Red / Amber / Green)", "✅  Live sidebar report updates after each answer", "✅  30-day action plan on session end"];
  features.forEach((f, i) => {
    const x = 0.55 + i * 3.2;
    slide.addText(f, { x, y: 6.02, w: 3.1, h: 0.38, fontSize: 11, color: DARK_TEXT, fontFace: "Segoe UI" });
  });
}

// ══════════════════════════════════════════════════════════════════
// SLIDE 5 — WHAT I BUILT + WHAT'S NEXT
// ══════════════════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  darkBg(slide);

  // Speaker Notes
  slide.addNotes("To wrap up, during this first week I built the RAG pipeline with ChromaDB, a 3-agent LangGraph system with human-in-the-loop state interrupts, a 6-dimension scoring rubric with color score bars, a live-updating sidebar, and dynamic action plans. The trickiest part was definitely setting up the state management and interrupts in LangGraph. Looking ahead, I plan to expand this with deeper study guides, a voice mode so you can speak your answers naturally, multi-role selection, persistent user history, and a production cloud deployment. Thank you for your time, and I'd love to jump straight into a live demo!");

  slide.addText("Week 1: Built & Learned", {
    x: 0.55, y: 0.32, w: 12, h: 0.65,
    fontSize: 36, bold: true, color: WHITE, fontFace: "Segoe UI Black"
  });

  // Left column — What I built
  card(slide, 0.55, 1.25, 6.1, 4.95, "1E293B");
  slide.addText("🏗️  What I Shipped", { x: 0.75, y: 1.42, w: 5.7, h: 0.4, fontSize: 16, bold: true, color: ACCENT, fontFace: "Segoe UI" });

  const built = [
    "RAG pipeline — ChromaDB ingestion + semantic retrieval",
    "3-agent LangGraph graph — Profiler, Interviewer, Evaluator",
    "Stateful multi-turn interview with human-in-the-loop node",
    "6-dimension scoring rubric with colored score bars",
    "Live report sidebar + 30-day action plan generator",
    "PDF/URL resume & JD ingestion in the Streamlit UI",
  ];
  built.forEach((b, i) => {
    slide.addText(`→  ${b}`, { x: 0.75, y: 2.0 + i * 0.55, w: 5.7, h: 0.48, fontSize: 11.5, color: "CBD5E1", fontFace: "Segoe UI", lineSpacingMultiple: 1.2 });
  });

  // Right column — What's Next
  card(slide, 6.95, 1.25, 6.1, 4.95, "1E293B");
  slide.addText("🔭  What's Next", { x: 7.15, y: 1.42, w: 5.7, h: 0.4, fontSize: 16, bold: true, color: GREEN, fontFace: "Segoe UI" });

  const next = [
    { t: "Deeper action plan — study guide per weak dimension", c: GREEN },
    { t: "Voice mode — speak answers, get spoken feedback", c: GREEN },
    { t: "Multi-role support (SWE, PM, Data Science)", c: "FBBF24" },
    { t: "User accounts + persistent session history", c: "FBBF24" },
    { t: "Production deployment on cloud (Vercel + FastAPI)", c: "FB923C" },
  ];
  next.forEach((n, i) => {
    slide.addShape(pptx.ShapeType.ellipse, { x: 7.15, y: 2.04 + i * 0.56, w: 0.2, h: 0.2, fill: { color: n.c }, line: { color: n.c } });
    slide.addText(n.t, { x: 7.45, y: 2.0 + i * 0.56, w: 5.4, h: 0.48, fontSize: 11.5, color: "CBD5E1", fontFace: "Segoe UI" });
  });

  // Bottom thank-you banner
  card(slide, 0.55, 6.42, 12.2, 0.7, PURPLE);
  slide.addText("🙏  Thank you for watching! Let's do a live demo →", {
    x: 0.65, y: 6.47, w: 12.0, h: 0.6,
    fontSize: 18, bold: true, color: WHITE, fontFace: "Segoe UI", align: "center"
  });
}

// ── Save ──────────────────────────────────────────────────────────
const outPath = "PrepAI_Intern_Week1_Presentation.pptx";
pptx.writeFile({ fileName: outPath })
  .then(() => console.log(`✅  Saved: ${outPath}`))
  .catch(err => console.error("Error:", err));
