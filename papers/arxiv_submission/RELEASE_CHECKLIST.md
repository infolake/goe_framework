# Release Checklist: v1.0 Public Release

**Repository**: GoE Framework - Geometrodynamics of Entropy  
**Target**: GitHub public release + Zenodo DOI + arXiv submission  
**Date**: October 29, 2025  
**Status**: 📋 Pre-release (ready for deployment)

---

## ✅ Pre-Release Completed

### Paper Preparation
- [x] **Abstract revised**: 4 calibrated parameters explicit (m₀⁽ˡ⁾, m₀⁽ᵘ⁾, m₀⁽ᵈ⁾, α)
- [x] **Glossary optimized**: 18 entries, calibrated vs derived marked
- [x] **Bibliography unified**: 60 refs in single `references.bib` (arXiv compliant)
- [x] **Proton spin prediction added**: §"Proton Spin Prediction: EIC-Testable Observable" (~40 lines LaTeX)
  - φ ≤ J_g(μ₀)/J_q(μ₀) ≤ φ² at μ₀ ~ 1 GeV
  - Falsification: ratio < 1.5 or > 2.8 excludes D₅
  - EIC timeline: ~2030-2035
- [x] **Code Capsule S4 created**: `proton_spin_prediction.py` (180 lines, figure generated)
- [x] **Paper compiled**: 50 pages, 865.5 KB, clean (1 benign warning)

### Repository Organization
- [x] **Root cleaned**: 7 redundant markdown files moved to `Goe_Toolkit_Arquivo`
- [x] **Logs archived**: 16 summary/log files → `arxiv_submission/archived_docs/`
- [x] **Scripts organized**: 4 Python scripts → `scripts_analysis/`
- [x] **Duplicates removed**: 
  - LaTeX aux files deleted (6 files)
  - `references_goldstandard_2025.bib` archived (superseded)
  - Duplicate `GoE_Toolkit/` subfolder removed
- [x] **Backups archived**: 2 zip files → `archived_docs/backups/`
- [x] **Professional README deployed**: `README_CLEAN.md` → `README.md` (250+ lines)
- [x] **Technical docs created**: `IMPLEMENTATION_SUMMARY.md` (8.6 KB)

### Repository Status
- [x] **Essential files**: 8 (main.tex/pdf, references.bib, sigma_moebius files, README, IMPLEMENTATION_SUMMARY)
- [x] **Organized directories**: 5 (archived_docs/, code_capsules/, figures/, scripts_analysis/, supplementary/)
- [x] **Items archived**: ~47 in `archived_docs/` (development artifacts preserved)
- [x] **No redundancies**: Portuguese files, logs, duplicates removed from main directory

---

## 📋 GitHub Release Steps

### 1. Pre-Release Verification (Do Now)

```powershell
# Navigate to repository root
Set-Location "D:\2025-Geometrodynamics_of_Entropy\Geometrodynamics_of_Entropy_Dark_Matter\01_camargo_goe_\GoE_Toolkit"

# Verify Git status
git status

# Check for uncommitted changes
git diff --stat

# Verify .gitignore excludes archives
Get-Content .gitignore | Select-String "archived_docs"
```

**Expected**:
- Clean working tree or only new organized files to commit
- `.gitignore` should include `archived_docs/` (optional, for cleaner public view)

### 2. Final Compilation Test

```powershell
Set-Location "papers\arxiv_submission"

# Test LaTeX compilation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Verify output
Test-Path main.pdf  # Should be True

# Test Code Capsule S4
python code_capsules\S4_proton_spin_prediction.py

# Verify figure generated
Test-Path figures\proton_spin_prediction_eic.pdf  # Should be True
```

**Expected**: 
- `main.pdf` generated successfully
- 0 undefined citations
- Figure generated in `figures/`

### 3. Git Commit (Clean Structure)

```powershell
# Add organized files
git add papers/arxiv_submission/main.tex
git add papers/arxiv_submission/references.bib
git add papers/arxiv_submission/README.md
git add papers/arxiv_submission/IMPLEMENTATION_SUMMARY.md
git add papers/arxiv_submission/code_capsules/
git add papers/arxiv_submission/figures/
git add papers/arxiv_submission/scripts_analysis/

# Commit with descriptive message
git commit -m "v1.0: Clean repository for arXiv submission and public release

- Unified bibliography (60 refs in references.bib)
- Added proton spin prediction (3rd falsification route, EIC testable ~2035)
- Created Code Capsule S4 (EIC visualization)
- Organized repository structure (essential files + 5 directories)
- Professional README with comprehensive documentation
- Archived ~47 development artifacts

Papers ready:
- Paper 1 (main.tex): 50 pages, 3 falsification routes
- Paper 2 (sigma_moebius_arxiv.tex): Technical companion

Status: Ready for arXiv gr-qc submission + Zenodo DOI"
```

### 4. Create Annotated Tag

```powershell
# Create v1.0 tag
git tag -a v1.0 -m "v1.0: Initial Public Release - GoE Framework

Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce

Papers:
1. Main GoE Framework (50 pages)
   - Fermion masses: φ-scaling (2.15% leptons, 8.0% quarks)
   - Cosmological bounce: z_b ~ 3.6×10⁴ (consistent with CMB/BBN)
   - Proton spin: J_g/J_q ∈ [φ,φ²] at μ=1 GeV (EIC testable ~2035)

2. Sigma-Moebius Companion (technical derivation)

Reproducibility:
- Code Capsule S4: Proton spin EIC prediction
- All figures reproducible
- Statistical validation complete

Quality Metrics:
- Compilation: Clean (1 benign warning)
- Citations: 0 undefined (60 refs)
- Parameters: 4 calibrated explicit, 2 derived
- Falsification routes: 3 independent tests

Status: Ready for arXiv submission (gr-qc primary) + Zenodo archival"

# Verify tag created
git tag -l -n10 v1.0
```

### 5. Push to GitHub

```powershell
# Push commits
git push origin master

# Push tags
git push origin v1.0

# Verify on GitHub
# Open: https://github.com/infolake/goe_framework/releases
```

**Expected**:
- Tag `v1.0` visible on GitHub Releases page
- README.md displays cleanly with proper formatting
- All essential files visible in repository

---

## 📋 Zenodo DOI Steps

### 1. Link GitHub to Zenodo

1. Go to **Zenodo.org** → Sign in with GitHub account
2. Navigate to **Settings** → **GitHub** → **Sync now**
3. Find `goe_framework` repository in list
4. Toggle **ON** the repository switch

**Expected**: Green checkmark appears, repository linked

### 2. Create GitHub Release (Triggers Zenodo)

1. Go to **GitHub repository** → **Releases** → **Draft a new release**
2. **Tag version**: `v1.0` (select existing tag)
3. **Release title**: `v1.0: Initial Public Release - GoE Framework`
4. **Description**: Copy from tag message above
5. **Assets**: Optionally attach `main.pdf` (GitHub auto-includes source)
6. Click **Publish release**

**Expected**: Release appears on GitHub, Zenodo begins archival

### 3. Verify Zenodo Archival

1. Go to **Zenodo** → **Upload** → Check for new entry
2. Wait ~10-30 minutes for processing
3. Zenodo creates DOI badge: `10.5281/zenodo.XXXXXXX`
4. Copy DOI and badge markdown

**Expected**: 
- DOI generated (e.g., `10.5281/zenodo.8234567`)
- Badge markdown: `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)`

### 4. Add DOI Badge to README

```powershell
# Edit README.md (top of file)
Set-Location "papers\arxiv_submission"
# Add badge below title:
# [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

# Commit and push
git add README.md
git commit -m "Add Zenodo DOI badge to README"
git push origin master
```

---

## 📋 arXiv Submission Steps

### Paper 1: Main GoE Framework

**Category**: gr-qc (General Relativity and Quantum Cosmology) - PRIMARY  
**Secondary**: hep-ph (High Energy Physics - Phenomenology), hep-th (High Energy Physics - Theory), astro-ph.CO (Cosmology and Nongalactic Astrophysics)

#### 1. Prepare Submission Package

```powershell
Set-Location "papers\arxiv_submission"

# Create arXiv package directory
New-Item -ItemType Directory -Path "arxiv_package" -Force

# Copy essential files
Copy-Item main.tex arxiv_package\
Copy-Item references.bib arxiv_package\
Copy-Item -Recurse figures\ arxiv_package\

# Verify package
Get-ChildItem arxiv_package -Recurse
```

**Required files**:
- `main.tex` (source)
- `references.bib` (bibliography)
- `figures/` (all figures referenced in paper)

**Optional** (if requested by arXiv):
- `main.bbl` (pre-compiled bibliography)

#### 2. arXiv Upload

1. Go to **arxiv.org/submit**
2. **Login** with arXiv account (or create new)
3. **Upload Files**:
   - Upload `main.tex`
   - Upload `references.bib`
   - Upload all files in `figures/` (or zip `figures/` folder)
4. **Metadata**:
   - **Title**: Copy from `main.tex` title
   - **Authors**: Guilherme de Camargo (PHIQ.IO)
   - **Abstract**: Copy revised abstract (lines 59-104 of main.tex)
   - **Categories**:
     - PRIMARY: `gr-qc` (General Relativity and Quantum Cosmology)
     - SECONDARY: `hep-ph` (High Energy Physics - Phenomenology)
     - SECONDARY: `hep-th` (High Energy Physics - Theory)
     - SECONDARY: `astro-ph.CO` (Cosmology and Nongalactic Astrophysics)
   - **Comments**: "50 pages, 23 figures, 60 references. Reproducible code at github.com/infolake/goe_framework (DOI: 10.5281/zenodo.XXXXXXX)"
   - **MSC Class**: 83C45 (Quantum gravity), 83F05 (Cosmology)
   - **ACM Class**: (leave blank or G.1.10 if requested)
   - **Journal Reference**: (leave blank for preprint)
   - **DOI**: (leave blank, will be assigned by arXiv)
5. **Preview**: Verify compilation on arXiv server
6. **Submit**: Click "Submit" button

**Expected**:
- Submission accepted for moderation (~1-2 days)
- arXiv ID assigned: `arXiv:YYMM.NNNNN` (e.g., `arXiv:2510.12345`)
- Paper appears on arXiv within 24-48 hours

#### 3. Post-Submission

Once arXiv ID assigned:
1. Update `README.md` with arXiv link
2. Update paper citation to include arXiv ID
3. Share on social media (Twitter/X, LinkedIn, ResearchGate)
4. Email to relevant researchers (optional)

```powershell
# Update README with arXiv link
# Add to citation section:
# **arXiv**: [arXiv:YYMM.NNNNN](https://arxiv.org/abs/YYMM.NNNNN)

git add README.md
git commit -m "Add arXiv ID to README"
git push origin master
```

### Paper 2: Sigma-Moebius Companion

**Category**: hep-th (High Energy Physics - Theory) - PRIMARY  
**Secondary**: gr-qc (General Relativity and Quantum Cosmology)

**Timing**: Submit AFTER Paper 1 is accepted on arXiv (to cross-reference)

#### 1. Prepare Submission Package

```powershell
Set-Location "papers\arxiv_submission"

# Create separate package for companion paper
New-Item -ItemType Directory -Path "arxiv_package_sigma" -Force

# Copy files
Copy-Item sigma_moebius_arxiv.tex arxiv_package_sigma\
Copy-Item sigma_moebius_arxivNotes.bib arxiv_package_sigma\
# (no figures needed for this paper)

# Verify package
Get-ChildItem arxiv_package_sigma -Recurse
```

#### 2. arXiv Upload (Same process as Paper 1)

**Metadata differences**:
- **Title**: Copy from `sigma_moebius_arxiv.tex`
- **Categories**:
  - PRIMARY: `hep-th` (High Energy Physics - Theory)
  - SECONDARY: `gr-qc` (General Relativity and Quantum Cosmology)
- **Comments**: "Technical companion to arXiv:YYMM.NNNNN (Paper 1). Derivation of Σ-Möbius geometry."
- **Cross-reference**: In abstract, mention Paper 1 arXiv ID

---

## 📋 Timeline Summary

| Task | Timing | Status |
|------|--------|--------|
| **Pre-Release Verification** | Now | ⏳ Pending |
| **Final Compilation Test** | Now | ⏳ Pending |
| **Git Commit + Tag v1.0** | Same day | ⏳ Pending |
| **Push to GitHub** | Same day | ⏳ Pending |
| **Link GitHub to Zenodo** | Within 24h | ⏳ Pending |
| **Create GitHub Release** | Within 24h | ⏳ Pending |
| **Verify Zenodo DOI** | 10-30 min after release | ⏳ Pending |
| **Add DOI Badge to README** | After DOI assigned | ⏳ Pending |
| **arXiv Submission Paper 1** | Within 48h | ⏳ Pending |
| **arXiv Moderation** | 1-2 days | ⏳ Pending |
| **arXiv Paper 1 Published** | 2-3 days total | ⏳ Pending |
| **arXiv Submission Paper 2** | After Paper 1 acceptance | ⏳ Pending |
| **arXiv Paper 2 Published** | 2-3 days after submission | ⏳ Pending |

**TOTAL TIME**: ~5-7 days from now to both papers on arXiv

---

## 📋 Quality Checklist

### Paper 1 (Main GoE Framework)

#### Theoretical Soundness
- [x] 4 calibrated parameters explicit: m₀⁽ˡ⁾, m₀⁽ᵘ⁾, m₀⁽ᵈ⁾, α
- [x] 2 derived constants: φ (from pentagonal spectrum), selection rules (from D₅)
- [x] Abstract operational (not hyperbolic): τ = ln(S/S₀) resolution
- [x] Glossary clear: 18 entries, calibrated vs derived marked

#### Falsification Routes (3 Independent Tests)
- [x] **Route 1**: Fermion masses
  - φ-scaling validation: 2.15% leptons, 8.0% quarks
  - Statistical significance: P < 10⁻⁸⁸
  - Falsification: φ-violations outside error bars
  - Status: ✅ PASSED (tested)

- [x] **Route 2**: Cosmological bounce
  - Prediction: z_b ~ 3.6×10⁴
  - Consistency: CMB power spectrum, BBN constraints
  - Falsification: z_b ≠ 3.6×10⁴ by orders of magnitude
  - Status: ✅ Consistent (observational)

- [x] **Route 3**: Proton spin (NEW)
  - Prediction: φ ≤ J_g(μ₀)/J_q(μ₀) ≤ φ² at μ₀ ~ 1 GeV
  - Band: [1.618, 2.618] (~61.8% width)
  - Falsification: ratio < 1.5 or > 2.8 excludes D₅
  - Timeline: EIC 2030-2035
  - Status: ✅ Testable (future)

#### Technical Quality
- [x] Compilation: Clean (1 benign warning in `wheeler1990` publisher)
- [x] Citations: 0 undefined (60 refs in unified `references.bib`)
- [x] Figures: 23 (all generated, reproducible via Code Capsules)
- [x] Pages: 50 (appropriate length for foundational paper)
- [x] Size: 865.5 KB (within arXiv limits)

#### Reproducibility
- [x] Code Capsule S4: Proton spin EIC prediction (180 lines Python)
- [x] Figure generation: `proton_spin_prediction_eic.pdf` created successfully
- [x] Data sources: PDG 2023, EIC White Paper, STAR/COMPASS global fits
- [x] Random seeds: N/A (deterministic calculation)

#### Documentation
- [x] README.md: 250+ lines professional documentation
- [x] IMPLEMENTATION_SUMMARY.md: 8.6 KB technical details
- [x] Code comments: Complete in S4 script
- [x] Citation format: BibTeX provided

### Paper 2 (Sigma-Moebius Companion)

- [x] Technical derivation: Complete (sigma_moebius_arxiv.tex)
- [x] Compilation: Clean (359.6 KB PDF)
- [x] Cross-references: Paper 1 cited (to be updated with arXiv ID)
- [x] Separate submission: Ready after Paper 1 acceptance

---

## 📋 Troubleshooting

### Issue: Git push fails (authentication)

**Solution**:
```powershell
# Configure Git credentials
git config --global user.name "Guilherme de Camargo"
git config --global user.email "camargo@phiq.io"

# Use GitHub Personal Access Token
# Go to GitHub → Settings → Developer settings → Personal access tokens
# Generate token with 'repo' scope
# Use token as password when pushing
```

### Issue: Zenodo not creating DOI

**Possible causes**:
1. Repository not toggled ON in Zenodo settings → Check sync
2. Release not published (draft) → Publish release on GitHub
3. Zenodo processing delay → Wait 30 min, then check Zenodo uploads

**Solution**: Manually upload to Zenodo if auto-sync fails:
1. Download GitHub release zip
2. Go to Zenodo → Upload → New upload
3. Upload zip, fill metadata, publish

### Issue: arXiv compilation fails

**Common causes**:
1. Missing figure files → Verify all `\includegraphics` paths exist
2. Bibliography errors → Test `bibtex main` locally first
3. Custom macros undefined → Add all `\newcommand` to preamble

**Solution**: 
- Use arXiv's "View log" to see error
- Test locally: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- If persistent, upload `main.bbl` pre-compiled

### Issue: arXiv rejects submission (policy)

**Possible reasons**:
1. Not original research → GoE is original, should not occur
2. Excessive self-promotion → Abstract is scientific, not promotional
3. Inappropriate category → gr-qc is correct primary for quantum cosmology

**Solution**: 
- If rejected, respond to moderator explaining scientific contribution
- Emphasize 3 falsification routes and statistical validation
- Provide GitHub link for reproducibility

---

## 📋 Post-Release Actions

### Immediate (Within 1 week)

- [ ] Monitor arXiv comments/questions
- [ ] Share preprint on social media:
  - Twitter/X: Tag @arxiv, #QuantumGravity, #Cosmology
  - LinkedIn: Post with summary and link
  - ResearchGate: Upload PDF and share
- [ ] Email to collaborators/interested researchers (optional)
- [ ] Update ORCID profile with preprint

### Short-term (Within 1 month)

- [ ] Identify target journal for peer review:
  - Physical Review D (comprehensive, high impact)
  - Journal of Cosmology and Astroparticle Physics (JCAP)
  - Classical and Quantum Gravity
  - Physics Letters B (if condensed to 6 pages)
- [ ] Prepare cover letter for journal submission
- [ ] Identify potential reviewers (suggest 3-5 experts)

### Long-term (Within 3-6 months)

- [ ] Respond to reviewer comments
- [ ] Revise paper based on feedback
- [ ] Prepare for EIC experimental tests (contact EIC collaboration)
- [ ] Develop Paper 3 (QCD corrections, neutrino masses, dark sector)
- [ ] Apply for research grants/funding

---

## 📋 Success Criteria

**v1.0 Release successful if**:
- ✅ GitHub tag v1.0 created and pushed
- ✅ Zenodo DOI generated and badge added to README
- ✅ arXiv Paper 1 published (gr-qc category)
- ✅ arXiv Paper 2 published (hep-th category)
- ✅ Code reproducible (S4 script runs successfully)
- ✅ Documentation complete (README + IMPLEMENTATION_SUMMARY)

**Release quality indicators**:
- GitHub stars/forks (measure interest)
- arXiv abstract views/downloads (measure reach)
- Citations in other preprints (measure impact)
- Requests for collaboration (measure relevance)

---

## 📞 Contact & Support

**Author**: Guilherme de Camargo  
**Email**: camargo@phiq.io  
**ORCID**: [0009-0004-8913-9419](https://orcid.org/0009-0004-8913-9419)  
**Institution**: PHIQ.IO (Independent Research)

**For questions about**:
- GitHub release: Open issue on repository
- arXiv submission: Email camargo@phiq.io
- Technical details: See IMPLEMENTATION_SUMMARY.md
- Code reproducibility: See code_capsules/README.md

---

**Generated**: October 29, 2025, 02:45 UTC  
**Version**: 1.0  
**Status**: ✅ Repository ready for deployment

**Next immediate action**: Run Pre-Release Verification (Section 1 above)
