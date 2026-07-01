# HireLens AI

> **An explainable AI-powered resume screening engine that helps recruiters and job seekers understand candidate-job fit through transparent, multi-layer scoring.**

HireLens AI is a backend project built with FastAPI that analyzes resumes against job descriptions using an explainable hybrid scoring system. Instead of relying solely on keyword matching, it combines multiple scoring layers to provide transparent recommendations and actionable insights.

The long-term goal is to build an AI-assisted hiring intelligence platform that supports both recruiters and candidates through explainable decision-making.

---

# Why HireLens AI?

Most resume screening tools answer one question:

> **"Does this resume contain the required keywords?"**

HireLens AI is designed to answer much more:

* How well does the candidate fit the role?
* Which requirements are satisfied?
* Which important skills are missing?
* Why was this score assigned?
* Which parts of the resume actually provide evidence for those skills?
* What should recruiters validate during interviews?
* How can job seekers improve their resumes before applying?

Rather than replacing recruiters, HireLens AI is designed to become an explainable decision-support system.

---

# What Makes This Project Different?

Many ATS demo projects stop after simple keyword matching.

HireLens AI is being designed around three principles:

* **Explainable AI** — Every score should be understandable.
* **Multi-layer scoring** — No single metric decides the outcome.
* **Dual-user experience** — Separate outputs for recruiters and job seekers.

The scoring engine is modular, allowing each evaluation layer to be improved independently without affecting the overall architecture.

---

# Current Features

### Resume Processing

* Upload PDF and DOCX resumes
* Extract resume text
* Analyze raw resume text directly

### Job Description Understanding

* Detect technical skills from job descriptions
* Classify requirements into:

  * Must-have skills
  * Good-to-have skills
* Section-aware requirement extraction

### Explainable Resume Matching

* Weighted skill matching
* Must-have vs Good-to-have scoring
* TF-IDF semantic similarity
* Explainable score breakdown
* Recruiter-friendly recommendations
* Job seeker improvement suggestions

### Dual Analysis Modes

**Recruiter Mode**

* Match score
* Shortlisting recommendation
* Risk flags
* Hiring manager handoff
* Technical follow-up points
* Explainable scoring

**Job Seeker Mode**

* Resume readiness assessment
* Missing skills
* Resume improvement suggestions
* Resume bullet recommendations
* Explainable scoring

---

# Hybrid Explainable Scoring Engine

Instead of producing a single keyword percentage, HireLens AI combines multiple explainable scoring layers.

| Scoring Layer               | Weight |     Status     |
| --------------------------- | -----: | :------------: |
| Must-have skill coverage    |    50% |  ✅ Implemented |
| Good-to-have skill coverage |    20% |  ✅ Implemented |
| TF-IDF semantic similarity  |    15% |  ✅ Implemented |
| Skill evidence strength     |    10% | 🚧 In Progress |
| Resume quality analysis     |     5% |   🚧 Planned   |

Each layer contributes independently to the final score, making the decision process transparent and easy to interpret.

---

# Example API Output

The API returns more than just a percentage.

Example information includes:

* Detected job requirements
* Matched skills
* Missing skills
* Match score
* Score contribution of each scoring layer
* Recruiter recommendation
* Resume improvement suggestions
* Hiring manager handoff summary

---

# Technology Stack

## Backend

* Python
* FastAPI
* Pydantic

## AI & Analytics

* TF-IDF
* Cosine Similarity
* Weighted Skill Scoring
* Rule-based Requirement Extraction

## Resume Processing

* PDF Parsing
* DOCX Parsing

## Development Tools

* Git
* GitHub
* Swagger UI

---

# API Endpoints

## `POST /analyze`

Analyze resume text against a job description.

---

## `POST /analyze-file`

Upload a PDF or DOCX resume for analysis.

---

# Project Structure

```text
app/
├── main.py
├── schemas/
│   └── analysis_schema.py
├── services/
│   ├── file_parser_service.py
│   ├── matching_service.py
│   ├── report_service.py
│   └── requirement_service.py
```

---

# Project Roadmap

### Phase 1 — Core Resume Intelligence ✅

* Resume parsing
* Job requirement extraction
* Explainable scoring engine
* Recruiter reports
* Job seeker reports

---

### Phase 2 — Scoring Intelligence 🚧

* Skill evidence strength scoring
* Resume quality scoring
* Better requirement extraction
* Improved scoring calibration

---

### Phase 3 — Product Development

* Authentication
* Database integration
* Analysis history
* Recruiter dashboard
* Candidate comparison
* Analytics dashboard
* Interactive frontend

---

# Design Philosophy

Every recommendation produced by HireLens AI should answer one simple question:

> **"Why did the system reach this conclusion?"**

Instead of hiding the logic behind a single score, HireLens AI exposes the reasoning through explainable scoring layers so recruiters and candidates can understand every recommendation.

This focus on transparency is the core design principle behind the project.

---

# Current Status

🚧 **Actively Under Development**

The project is being built incrementally, with each scoring layer designed, implemented, tested, and documented before moving to the next stage.

Current focus:

* Skill Evidence Strength Engine
* Resume Quality Analysis
* Hybrid Scoring Engine v1.0

---

# Future Vision

The long-term vision is to evolve HireLens AI from a resume matching API into a comprehensive hiring intelligence platform that supports recruiters throughout the screening process while helping candidates understand and improve their job readiness.

---

# Author

**Ashwini Bhawalkar**

Backend Developer focused on building practical AI-powered developer tools using Python and FastAPI, with an interest in explainable AI systems, backend architecture, and product thinking.
