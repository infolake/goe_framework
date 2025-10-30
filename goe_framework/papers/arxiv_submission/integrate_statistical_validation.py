#!/usr/bin/env python3
"""
Statistical Integration Script for main.tex
Filename: integrate_statistical_validation.py
Last Modified: 2025-01-27
Purpose: Automatically merge statistical validation content into main.tex
"""

import re
from pathlib import Path
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create backup of original file"""
    backup_path = filepath.parent / f"{filepath.stem}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}{filepath.suffix}"
    shutil.copy2(filepath, backup_path)
    print(f"Backup created: {backup_path}")
    return backup_path

def read_file(filepath):
    """Read file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def insert_after_introduction(content, patch_content):
    """Insert statistical summary after Introduction section"""
    # Find the end of Introduction section (before next \section)
    pattern = r'(\\section\{Introduction\}.*?)(\\section\{)'
    
    # Extract the statistical summary from patch
    summary_pattern = r'(\\subsection\{Statistical Validation and Robustness\}.*?% -+\s*\n% DERIVED)'
    match = re.search(summary_pattern, patch_content, re.DOTALL)
    if not match:
        print("Warning: Could not find statistical summary in patch")
        return content
    
    summary_text = match.group(1)
    
    # Insert before the next section
    def replacer(m):
        return m.group(1) + "\n\n" + summary_text + "\n\n" + m.group(2)
    
    new_content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        print("✓ Inserted statistical summary after Introduction")
    else:
        print("⚠ Could not insert summary - pattern not found")
    
    return new_content

def insert_derived_vs_adjusted(content, patch_content):
    """Insert derived vs adjusted table after fermion mass predictions section"""
    # Extract table from patch
    table_pattern = r'(% -+\s*\n% DERIVED VS ADJUSTED TABLE.*?% -+\s*\n)'
    match = re.search(table_pattern, patch_content, re.DOTALL)
    if not match:
        print("Warning: Could not find derived vs adjusted table in patch")
        return content
    
    table_text = match.group(1)
    
    # Insert after "Fermion Mass Predictions and Validation" section
    pattern = r'(\\section\{Fermion Mass Predictions and Validation\}.*?)(\\subsection\{Empirical Mass Spectrum\})'
    
    def replacer(m):
        return m.group(1) + "\n\n" + table_text + "\n\n" + m.group(2)
    
    new_content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        print("✓ Inserted derived vs adjusted table")
    else:
        print("⚠ Could not insert table - trying alternative location")
        # Try after topological origin section
        pattern2 = r'(\\subsection\{Topological Origin of All Physical Values.*?\}.*?)(\\subsubsection)'
        new_content = re.sub(pattern2, replacer, content, count=1, flags=re.DOTALL)
        if new_content != content:
            print("✓ Inserted table at alternative location")
    
    return new_content

def insert_comprehensive_validation(content, patch_content):
    """Insert comprehensive statistical validation section"""
    # Extract section from patch
    section_pattern = r'(% -+\s*\n% COMPREHENSIVE STATISTICAL VALIDATION SECTION.*?% -+\s*\n% FIGURES FOR)'
    match = re.search(section_pattern, patch_content, re.DOTALL)
    if not match:
        print("Warning: Could not find comprehensive validation section in patch")
        return content
    
    section_text = match.group(1)
    
    # Insert before "Bayesian MCMC Analysis" section
    pattern = r'()(\\section\{Bayesian MCMC Analysis)'
    
    def replacer(m):
        return m.group(1) + "\n\n" + section_text + "\n\n" + m.group(2)
    
    new_content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        print("✓ Inserted comprehensive validation section")
    else:
        print("⚠ Could not insert section - trying after fermion predictions")
        # Try after fermion mass predictions
        pattern2 = r'(\\section\{Fermion Mass Predictions and Validation\}.*?)(\\section\{)'
        new_content = re.sub(pattern2, replacer, content, count=1, flags=re.DOTALL)
        if new_content != content:
            print("✓ Inserted section after fermion predictions")
    
    return new_content

def insert_figures(content, patch_content):
    """Insert statistical validation figures"""
    # Extract figures from patch
    figures_pattern = r'(% -+\s*\n% FIGURES FOR STATISTICAL VALIDATION.*?% -+\s*\n% END OF)'
    match = re.search(figures_pattern, patch_content, re.DOTALL)
    if not match:
        print("Warning: Could not find figures in patch")
        return content
    
    figures_text = match.group(1)
    
    # Insert at the end of comprehensive validation section or before Discussion
    pattern = r'(\\section\{Discussion\})'
    
    def replacer(m):
        return figures_text + "\n\n" + m.group(1)
    
    new_content = re.sub(pattern, replacer, content, count=1, flags=re.DOTALL)
    
    if new_content != content:
        print("✓ Inserted figures before Discussion")
    else:
        print("⚠ Could not insert figures")
    
    return new_content

def update_abstract(content):
    """Update abstract with correct statistical numbers"""
    # Update MAPE values to match actual results
    content = re.sub(
        r'\\textbf\{2\.15\\% mean error for leptons\}',
        r'\\textbf{2.15\\% mean error for leptons (median MAPE 7.28\\% overall)}',
        content
    )
    
    print("✓ Updated abstract with correct statistics")
    return content

def main():
    """Main integration function"""
    print("="*80)
    print("INTEGRATING STATISTICAL VALIDATION INTO MAIN.TEX")
    print("="*80)
    
    # Paths
    main_tex_path = Path("goe_framework/papers/arxiv_submission/arxiv_package/main.tex")
    patch_path = Path("goe_framework/papers/arxiv_submission/statistical_validation_patch.tex")
    
    # Check files exist
    if not main_tex_path.exists():
        print(f"Error: {main_tex_path} not found")
        return
    
    if not patch_path.exists():
        print(f"Error: {patch_path} not found")
        return
    
    # Create backup
    backup_path = backup_file(main_tex_path)
    
    # Read files
    main_content = read_file(main_tex_path)
    patch_content = read_file(patch_path)
    
    # Apply transformations
    print("\nApplying transformations...")
    new_content = main_content
    new_content = insert_after_introduction(new_content, patch_content)
    new_content = insert_derived_vs_adjusted(new_content, patch_content)
    new_content = insert_comprehensive_validation(new_content, patch_content)
    new_content = insert_figures(new_content, patch_content)
    new_content = update_abstract(new_content)
    
    # Write updated file
    write_file(main_tex_path, new_content)
    
    # Summary
    print("\n" + "="*80)
    print("INTEGRATION COMPLETE")
    print("="*80)
    print(f"Original file backed up to: {backup_path}")
    print(f"Updated file: {main_tex_path}")
    print("\nChanges made:")
    print("  • Statistical summary added after Introduction")
    print("  • Derived vs Adjusted table inserted")
    print("  • Comprehensive validation section added")
    print("  • Figures for validation inserted")
    print("  • Abstract updated with correct statistics")
    print("\nNext steps:")
    print("  1. Review the updated main.tex")
    print("  2. Compile with pdflatex to check for errors")
    print("  3. Verify all figure references are correct")
    print("  4. Check cross-references and labels")

if __name__ == "__main__":
    main()

