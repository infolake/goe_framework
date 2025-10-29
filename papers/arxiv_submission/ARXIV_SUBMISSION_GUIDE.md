# arXiv Submission Guide - GoE Framework

**Paper:** Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce  
**Date:** October 29, 2025  
**Package:** `arxiv_submission_package.zip` (334.4 KB)  
**Status:** ✅ Ready for submission

---

## Package Verification

### ✅ Contents (16 files)

**Source Files:**
- ✅ `main.tex` (108.7 KB) - Main manuscript
- ✅ `references.bib` (15.9 KB) - Unified bibliography (60 references)

**Figures (14 PDFs):**
- ✅ `figures/cmb_power_spectrum_goe_ec.pdf` (34.4 KB)
- ✅ `figures/Ez_bounce.pdf` (42.2 KB)
- ✅ `figures/fig_bounce_hubble.pdf` (35.7 KB)
- ✅ `figures/fig_c5_spectrum.pdf` (23.5 KB)
- ✅ `figures/fig_coupling_strengths_generation.pdf` (33.8 KB)
- ✅ `figures/fig_fermion_masses.pdf` (32.2 KB)
- ✅ `figures/fig_Hz_bounce.pdf` (27.5 KB)
- ✅ `figures/fig_kk_tower.pdf` (30.9 KB)
- ✅ `figures/fig_LOOCV_phi.pdf` (26.6 KB)
- ✅ `figures/fig_ppc_gminus2.pdf` (29.5 KB)
- ✅ `figures/fig_proton_spin.pdf` (33.5 KB) ⭐ NEW - EIC prediction
- ✅ `figures/loocv_scatter.pdf` (41.3 KB)
- ✅ `figures/permutation_mape_hist.pdf` (40.4 KB)
- ✅ `figures/phi_sensitivity.pdf` (37.8 KB)

### ✅ Quality Checks

| Requirement | Status | Details |
|------------|--------|---------|
| **Source file** | ✅ Pass | main.tex included |
| **Bibliography** | ✅ Pass | references.bib (60 refs) |
| **Figures** | ✅ Pass | 14 PDFs in figures/ |
| **Format** | ✅ Pass | All figures in PDF |
| **Size** | ✅ Pass | 334.4 KB (< 10 MB limit) |
| **Auxiliary files** | ✅ Pass | No .aux, .log, .bbl |
| **Links** | ✅ Pass | Updated to goe_framework |
| **Compilation** | ✅ Pass | Clean LaTeX compilation |

---

## Submission Instructions

### Step 1: Prepare Metadata

Before uploading, prepare the following information:

**Title:**
```
Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce
```

**Authors:**
```
Guilherme de Camargo
```

**Affiliation:**
```
PHIQ.IO Research Group
```

**Abstract:** (Copy from main.tex lines 59-104)
```
The Geometrodynamics of Entropy (GoE) framework addresses fermion mass 
hierarchy and cosmological bounce through geometric quantization of a 
6-dimensional pentagonal topology. Using 4 calibrated parameters 
(m₀⁽ˡ⁾, m₀⁽ᵘ⁾, m₀⁽ᵈ⁾, α) and deriving the golden ratio φ from the 
pentagonal spectrum, the framework achieves 2.15% error for leptons 
and 8.0% for quarks (P < 10⁻⁸⁸). A cosmological bounce at z_b ≈ 3.6×10⁴ 
provides operational resolution to the problem of time via τ = ln(S/S₀). 
A new proton spin prediction (J_g/J_q ∈ [φ,φ²]) is testable at the EIC by 2035.
```

**Comments:**
```
50 pages, 14 figures, 60 references. Reproducible code at 
https://github.com/infolake/goe_framework (DOI: 10.5281/zenodo.XXXXXXX)
```

**Categories:**
- **Primary:** `gr-qc` (General Relativity and Quantum Cosmology)
- **Secondary:** 
  - `hep-ph` (High Energy Physics - Phenomenology)
  - `hep-th` (High Energy Physics - Theory)
  - `astro-ph.CO` (Cosmology and Nongalactic Astrophysics)

**MSC Classes (optional):**
- `83C45` (Quantum gravity)
- `83F05` (Cosmology)
- `81V05` (Quantum field theory)

---

### Step 2: Upload to arXiv

1. **Go to arXiv submission page:**
   ```
   https://arxiv.org/submit
   ```

2. **Login** with your arXiv account
   - If you don't have an account, register at: https://arxiv.org/user/register
   - Verify your email address

3. **Start new submission:**
   - Click **"Start New Submission"**
   - Select **"Upload Submission Files"**

4. **Upload the package:**
   - Click **"Choose File"**
   - Select: `arxiv_submission_package.zip`
   - Click **"Upload Files"**
   - Wait for processing (~5-10 minutes)

5. **Verify upload:**
   - arXiv will automatically detect:
     - ✅ Main file: `main.tex`
     - ✅ Bibliography: `references.bib`
     - ✅ Figures: 14 PDFs in `figures/`
   - Check for any warnings or errors

6. **Process files:**
   - arXiv will compile your paper automatically
   - Wait for compilation to complete
   - If errors occur, check the log and fix locally

---

### Step 3: Enter Metadata

1. **Title:**
   - Copy exact title from above

2. **Authors:**
   - Add author: `Guilherme de Camargo`
   - Affiliation: `PHIQ.IO Research Group`
   - Email: `camargo@phiq.io`
   - ORCID: `0009-0004-8913-9419`

3. **Abstract:**
   - Copy abstract from above (max 1920 characters)
   - Do NOT include LaTeX commands
   - Use plain text with Unicode symbols if needed

4. **Comments:**
   - Copy comments from above
   - Include GitHub link
   - Add Zenodo DOI when available

5. **Categories:**
   - **Primary:** Select `gr-qc` from dropdown
   - **Cross-lists:** Add `hep-ph`, `hep-th`, `astro-ph.CO`

6. **MSC Classes (optional but recommended):**
   - Enter: `83C45, 83F05, 81V05`

7. **Journal Reference:** (leave blank for preprint)

8. **DOI:** (leave blank, arXiv will assign one)

9. **Report Number:** (optional, leave blank)

10. **License:**
    - Recommended: `arXiv.org perpetual non-exclusive license`
    - This allows arXiv to distribute your paper

---

### Step 4: Preview and Submit

1. **Preview:**
   - Click **"Preview"**
   - arXiv will generate a PDF preview
   - **IMPORTANT:** Check carefully:
     - ✅ All figures appear correctly
     - ✅ All equations render properly
     - ✅ Bibliography is complete
     - ✅ No broken references
     - ✅ Links to GitHub are clickable
     - ✅ Abstract is correctly formatted

2. **Make corrections (if needed):**
   - If issues found, click **"Modify Submission"**
   - Re-upload corrected files
   - Preview again

3. **Submit:**
   - When satisfied with preview, click **"Submit"**
   - Confirm submission details
   - Click **"Confirm Submission"**

4. **Submission confirmation:**
   - You'll receive an email confirmation
   - arXiv will assign a submission ID
   - Paper enters moderation queue

---

## Post-Submission Process

### Moderation (1-2 business days)

1. **arXiv moderators review:**
   - Check scientific content
   - Verify appropriate category
   - Ensure no policy violations

2. **Possible outcomes:**
   - ✅ **Approved:** Paper scheduled for announcement
   - ⚠️ **Reclassified:** Moderator suggests different category
   - ❌ **On hold:** Moderator requests clarification
   - ❌ **Rejected:** Paper doesn't meet arXiv standards

3. **If on hold:**
   - Respond to moderator questions promptly
   - Provide requested clarifications
   - Address any concerns

### Announcement (after approval)

1. **Paper scheduled:**
   - Approved papers are scheduled for next announcement
   - Announcements happen daily at 20:00 EST (Mon-Fri)

2. **arXiv ID assigned:**
   - Format: `YYMM.NNNNN` (e.g., `2510.12345`)
   - This is your permanent identifier

3. **Paper goes live:**
   - Available at: `https://arxiv.org/abs/YYMM.NNNNN`
   - PDF at: `https://arxiv.org/pdf/YYMM.NNNNN.pdf`

4. **Update your materials:**
   - Add arXiv ID to README.md
   - Update paper citation with arXiv ID
   - Share on social media

---

## Expected Timeline

| Event | Time | Notes |
|-------|------|-------|
| **Upload** | Day 0 | Immediate |
| **Compilation** | ~10 min | Automatic |
| **Preview** | Day 0 | Review carefully |
| **Submit** | Day 0 | After preview approval |
| **Moderation** | 1-2 days | Business days only |
| **Approval** | Day 1-2 | If no issues |
| **Announcement** | Next 20:00 EST | Mon-Fri only |
| **Live on arXiv** | Day 1-3 | Public access |

**Total time:** 1-3 business days from submission to publication

---

## After Publication

### 1. Update GitHub Repository

```bash
# Update README.md with arXiv ID
# Replace placeholder badges with actual IDs

# Commit and push
git add README.md
git commit -m "Add arXiv ID: YYMM.NNNNN"
git push origin main
```

### 2. Update Zenodo DOI

- Zenodo will automatically archive the GitHub release
- Add arXiv ID to Zenodo metadata
- Update README with Zenodo DOI badge

### 3. Share Paper

**Social Media:**
- Twitter/X: Tag @arxiv, #QuantumGravity, #Cosmology, #ParticlePhysics
- LinkedIn: Professional network announcement
- ResearchGate: Upload and share

**Email:**
- Notify colleagues and collaborators
- Share with relevant research groups
- Contact EIC collaboration (for proton spin prediction)

**Communities:**
- Physics Forums
- Reddit: r/Physics, r/Cosmology
- Stack Exchange: Physics

### 4. Prepare Journal Submission

**Target Journals:**
1. **Physical Review D** (comprehensive, high impact)
   - Sections: Particles, Fields, Gravitation, Cosmology
   - Impact Factor: ~5.0

2. **Journal of Cosmology and Astroparticle Physics (JCAP)**
   - Focus: Cosmology and astroparticle physics
   - Impact Factor: ~5.3

3. **Classical and Quantum Gravity**
   - Focus: Quantum gravity, cosmology
   - Impact Factor: ~3.1

4. **Physics Letters B** (if condensed to 6 pages)
   - Rapid communication format
   - Impact Factor: ~4.4

**Preparation:**
- Wait 1-2 weeks for arXiv feedback
- Address any comments from community
- Prepare cover letter highlighting:
  - 3 falsification routes
  - Statistical significance (P < 10⁻⁸⁸)
  - EIC testability (~2035)
  - Complete reproducibility

---

## Troubleshooting

### Upload Issues

**Problem:** ZIP file rejected
- **Solution:** Ensure ZIP contains only main.tex, references.bib, and figures/
- **Check:** No auxiliary files (.aux, .log, .bbl)

**Problem:** Compilation fails
- **Solution:** Test locally first: `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
- **Check:** All \includegraphics paths point to figures/ directory

**Problem:** Missing figures
- **Solution:** Ensure all figure files are in figures/ subdirectory
- **Check:** File names match exactly (case-sensitive)

### Moderation Issues

**Problem:** Wrong category suggested
- **Response:** Politely explain why gr-qc is appropriate (quantum cosmology + gravity)
- **Evidence:** Wheeler-DeWitt equation, geometric quantization

**Problem:** Insufficient originality claim
- **Response:** Highlight:
  - Novel geometric framework (6D pentagonal topology)
  - 3 independent falsification routes
  - EIC testable prediction (not in literature)
  - Statistical validation (P < 10⁻⁸⁸)

**Problem:** Overlap with existing work
- **Response:** Clarify differences:
  - Not just phenomenology (geometric derivation)
  - φ derived, not fitted
  - Bounce without exotic matter
  - Proton spin prediction unique

---

## Contact Information

**arXiv Help:**
- Email: help@arxiv.org
- Help pages: https://info.arxiv.org/help/

**Author Contact:**
- Guilherme de Camargo
- Email: camargo@phiq.io
- ORCID: 0009-0004-8913-9419
- GitHub: https://github.com/infolake/goe_framework

---

## Version History

**v1.0** (October 29, 2025)
- Initial submission package created
- 50 pages, 14 figures, 60 references
- 3 falsification routes included
- Links corrected to goe_framework
- Package verified and ready

---

**Package Location:**
```
papers/arxiv_submission/arxiv_submission_package.zip
```

**Size:** 334.4 KB (0.33 MB)

**Status:** ✅ Ready for submission to arXiv gr-qc

**Next Step:** Go to https://arxiv.org/submit and begin upload
