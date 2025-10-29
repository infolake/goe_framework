# GitHub Setup Guide - goe_framework

**Repository:** goe_framework  
**Status:** ✅ Git initialized locally, ready to push  
**Date:** October 29, 2025

---

## Current Status

✅ **Local Git repository initialized**
- Initial commit created: `58e4475`
- Branch: `master`
- Files: 39 (21,506 insertions)
- Structure: Clean and organized

---

## Step 1: Create GitHub Repository

### Option A: Via GitHub Web Interface

1. Go to **https://github.com/new**
2. **Repository name:** `goe_framework`
3. **Description:** "Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce"
4. **Visibility:** 
   - ✅ **Public** (recommended for arXiv/Zenodo)
   - ⚠️ Private (if you want to review first, can change later)
5. **Do NOT initialize with:**
   - ❌ README (we already have one)
   - ❌ .gitignore (we already have one)
   - ❌ LICENSE (we already have one)
6. Click **"Create repository"**

### Option B: Via GitHub CLI (if installed)

```bash
gh repo create goe_framework --public --source=. --remote=origin --push
```

---

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, GitHub will show you commands. Use these:

```bash
# Navigate to repository (if not already there)
cd D:\2025-Geometrodynamics_of_Entropy\Geometrodynamics_of_Entropy_Dark_Matter\01_camargo_goe_\goe_framework

# Add GitHub as remote origin
git remote add origin https://github.com/infolake/goe_framework.git

# Verify remote added
git remote -v
# Should show:
# origin  https://github.com/infolake/goe_framework.git (fetch)
# origin  https://github.com/infolake/goe_framework.git (push)

# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub (first time)
git push -u origin main
```

**Authentication:**
- If prompted for username/password:
  - **Username:** `infolake`
  - **Password:** Use **Personal Access Token** (NOT your GitHub password)
  - Generate token at: https://github.com/settings/tokens
  - Required scopes: `repo` (full control of private repositories)

---

## Step 3: Create Release Tag

```bash
# Create annotated tag v1.0
git tag -a v1.0 -m "v1.0: Initial Public Release - GoE Framework

Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce

Papers:
- Paper 1: Main GoE Framework (50 pages)
  * Fermion mass hierarchy: φ-scaling (2.15% leptons, 8.0% quarks)
  * Cosmological bounce: z_b ≈ 3.6×10⁴ (consistent with CMB/BBN)
  * Proton spin prediction: J_g/J_q ∈ [φ,φ²] (EIC testable ~2035)

- Paper 2: Sigma-Moebius companion (technical derivation)

Quality Metrics:
- Compilation: Clean (0 undefined citations)
- Parameters: 4 calibrated explicit, 2 derived
- Falsification routes: 3 independent tests
- Reproducibility: 100% (code capsules provided)

Files:
- 39 files total
- 8 paper files (tex/pdf/bib/docs)
- 3 computational notebooks
- 23 figures (reproducible)
- 1 code capsule (S4: proton spin EIC prediction)

Status: Ready for arXiv gr-qc submission + Zenodo DOI"

# Push tag to GitHub
git push origin v1.0

# Verify tag pushed
git tag -l
```

---

## Step 4: Create GitHub Release

### Via GitHub Web Interface:

1. Go to **https://github.com/infolake/goe_framework/releases**
2. Click **"Draft a new release"**
3. **Tag version:** Select `v1.0` (from dropdown)
4. **Release title:** `v1.0: Initial Public Release - GoE Framework`
5. **Description:** Copy from tag message above
6. **Attach files (optional):**
   - `papers/arxiv_submission/main.pdf` (865 KB)
   - `papers/arxiv_submission/sigma_moebius_arxiv.pdf` (360 KB)
7. **Set as latest release:** ✅ Checked
8. Click **"Publish release"**

### Via GitHub CLI (if installed):

```bash
gh release create v1.0 \
  --title "v1.0: Initial Public Release - GoE Framework" \
  --notes-file release_notes.txt \
  papers/arxiv_submission/main.pdf \
  papers/arxiv_submission/sigma_moebius_arxiv.pdf
```

---

## Step 5: Link to Zenodo (Generate DOI)

### 5.1 Link GitHub Repository to Zenodo

1. Go to **https://zenodo.org/** → Sign in with GitHub
2. Navigate to **Settings** → **GitHub**
3. Click **"Sync now"** to refresh repository list
4. Find `goe_framework` in the list
5. Toggle **ON** the repository switch (should turn green)

### 5.2 Verify Zenodo Integration

1. Wait ~10-30 minutes for Zenodo to process
2. Go to **Zenodo** → **Upload** → Check for new entry
3. Zenodo should automatically create:
   - Archive of v1.0 release
   - Persistent DOI: `10.5281/zenodo.XXXXXXX`
   - DOI badge for README

### 5.3 Add DOI Badge to README

Once Zenodo generates DOI (e.g., `10.5281/zenodo.8234567`):

```bash
# Edit README.md (line 3)
# Replace:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

# With actual DOI:
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8234567.svg)](https://doi.org/10.5281/zenodo.8234567)

# Commit and push
git add README.md
git commit -m "Add Zenodo DOI badge"
git push origin main
```

---

## Step 6: Verify Repository Setup

### Check GitHub Repository:

- [ ] Repository visible at `https://github.com/infolake/goe_framework`
- [ ] README.md displays correctly with badges
- [ ] All 39 files visible in repository
- [ ] Release v1.0 created
- [ ] Tag v1.0 visible in tags list
- [ ] Repository is **Public** (for Zenodo/arXiv linking)

### Check Zenodo:

- [ ] Repository appears in Zenodo GitHub integration
- [ ] DOI badge generated
- [ ] Archive created for v1.0

### Local Verification:

```bash
# Check remote connection
git remote -v

# Check current branch
git branch

# Check tags
git tag -l

# Check commit log
git log --oneline --graph

# Check repository status
git status
```

---

## Troubleshooting

### Issue: Push fails with authentication error

**Solution:**
```bash
# Generate Personal Access Token (PAT) at:
# https://github.com/settings/tokens

# When prompted for password, use PAT instead

# Or configure credential helper:
git config --global credential.helper wincred
```

### Issue: Remote already exists

**Solution:**
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/infolake/goe_framework.git
```

### Issue: Branch named 'master' but GitHub uses 'main'

**Solution:**
```bash
# Rename local branch to main
git branch -M main

# Push to main
git push -u origin main
```

### Issue: Zenodo not creating DOI

**Possible causes:**
1. Repository not toggled ON in Zenodo settings
2. Release not published (still in draft)
3. Processing delay (wait 30 minutes)

**Solution:**
- Check Zenodo → GitHub settings
- Ensure release is **published** (not draft)
- Wait and check Zenodo uploads page

---

## Next Steps After GitHub Setup

1. ✅ **GitHub repository created and synced**
2. ✅ **Release v1.0 published**
3. ⏳ **Zenodo DOI generated** (wait 10-30 min)
4. ⏳ **Update README with DOI badge**
5. ⏳ **Submit to arXiv** (see RELEASE_CHECKLIST.md)

---

## Summary of Commands

```bash
# One-time setup
cd goe_framework
git remote add origin https://github.com/infolake/goe_framework.git
git branch -M main
git push -u origin main

# Create and push tag
git tag -a v1.0 -m "v1.0: Initial Public Release"
git push origin v1.0

# Future updates
git add .
git commit -m "Description of changes"
git push origin main
```

---

## Repository Information

**Local Path:**
```
D:\2025-Geometrodynamics_of_Entropy\Geometrodynamics_of_Entropy_Dark_Matter\01_camargo_goe_\goe_framework
```

**GitHub URL:**
```
https://github.com/infolake/goe_framework
```

**Zenodo DOI (after generation):**
```
https://doi.org/10.5281/zenodo.XXXXXXX
```

**arXiv ID (after submission):**
```
https://arxiv.org/abs/YYMM.NNNNN
```

---

**Created:** October 29, 2025  
**Status:** ✅ Ready to push to GitHub  
**Next:** Create GitHub repository and execute Step 2 above
