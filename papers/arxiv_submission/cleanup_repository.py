"""
Cleanup repository - Move internal control files to archive
File: cleanup_repository.py
Date: 2025-10-29
"""

from pathlib import Path
import shutil
from datetime import datetime

def cleanup_arxiv_submission():
    """
    Clean up arxiv_submission directory:
    1. Move internal reports to Goe_Toolkit_Arquivo
    2. Remove backup files
    3. Remove auxiliary LaTeX files
    4. Remove old ZIPs
    5. Keep only essentials
    """
    
    print("=" * 80)
    print("LIMPEZA DO REPOSITÓRIO")
    print("=" * 80)
    
    base_dir = Path(".")
    toolkit_dir = Path("../../../../../Goe_Toolkit_Arquivo/arxiv_internal_files")
    
    # Create toolkit archive directory
    toolkit_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n✓ Diretório de arquivo criado: {toolkit_dir}")
    
    # Files to move to toolkit (internal reports)
    reports_to_move = [
        "CLEANUP_SUMMARY.md",
        "FINAL_CORRECTIONS_APPLIED.md",
        "FINAL_STATUS.md",
        "MISSION_ACCOMPLISHED.md",
        "NUMERICAL_CONSISTENCY_FIXED.md",
        "PARAMETER_CORRECTION_SUMMARY.md",
        "STATISTICAL_INTEGRATION_REPORT.md",
        "IMPLEMENTATION_SUMMARY.md",
        "PACOTE_ARXIV_PRONTO.md",
        "RELEASE_CHECKLIST.md",
        "RESUMO_INTEGRACAO.md",
        "ARXIV_SUBMISSION_GUIDE.md",
    ]
    
    # Files to delete (backups and aux)
    files_to_delete = [
        "main_backup_*.tex",
        "main.aux",
        "main.bbl",
        "main.blg", 
        "main.log",
        "main.out",
        "*.aux",
        "*.log",
        "*.out",
        "*.blg",
        "*.bbl",
        "sigma_moebius_arxiv.*",
        "statistical_validation_patch.tex",
    ]
    
    # Old ZIPs to move
    old_zips = [
        "arxiv_submission_20251029_165836.zip",
        "arxiv_submission_20251029_174123.zip",
        "arxiv_submission_package.zip",
    ]
    
    moved_count = 0
    deleted_count = 0
    
    # Move reports
    print("\n" + "=" * 80)
    print("MOVENDO RELATÓRIOS INTERNOS PARA TOOLKIT")
    print("=" * 80)
    for report in reports_to_move:
        report_path = base_dir / report
        if report_path.exists():
            try:
                shutil.move(str(report_path), str(toolkit_dir / report))
                print(f"  ✓ Movido: {report}")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Erro ao mover {report}: {e}")
    
    # Move old ZIPs
    print("\n" + "=" * 80)
    print("MOVENDO ZIPs ANTIGOS PARA TOOLKIT")
    print("=" * 80)
    for zip_file in old_zips:
        zip_path = base_dir / zip_file
        if zip_path.exists():
            try:
                shutil.move(str(zip_path), str(toolkit_dir / zip_file))
                print(f"  ✓ Movido: {zip_file}")
                moved_count += 1
            except Exception as e:
                print(f"  ✗ Erro ao mover {zip_file}: {e}")
    
    # Delete backups and aux files
    print("\n" + "=" * 80)
    print("REMOVENDO BACKUPS E ARQUIVOS AUXILIARES")
    print("=" * 80)
    for pattern in files_to_delete:
        for file_path in base_dir.glob(pattern):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    print(f"  ✓ Removido: {file_path.name}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ✗ Erro ao remover {file_path.name}: {e}")
    
    # Clean arxiv_package
    print("\n" + "=" * 80)
    print("LIMPANDO arxiv_package/")
    print("=" * 80)
    
    arxiv_pkg = base_dir / "arxiv_package"
    
    # Move reports from arxiv_package
    for report_file in arxiv_pkg.glob("*_REPORT.md"):
        try:
            shutil.move(str(report_file), str(toolkit_dir / report_file.name))
            print(f"  ✓ Movido: arxiv_package/{report_file.name}")
            moved_count += 1
        except Exception as e:
            print(f"  ✗ Erro: {e}")
    
    for report_file in arxiv_pkg.glob("FIGURAS_*.md"):
        try:
            shutil.move(str(report_file), str(toolkit_dir / report_file.name))
            print(f"  ✓ Movido: arxiv_package/{report_file.name}")
            moved_count += 1
        except Exception as e:
            print(f"  ✗ Erro: {e}")
    
    # Remove backups from arxiv_package
    for backup in arxiv_pkg.glob("main_backup_*.tex"):
        try:
            backup.unlink()
            print(f"  ✓ Removido: arxiv_package/{backup.name}")
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ Erro: {e}")
    
    for backup in arxiv_pkg.glob("main.tex.pre_*"):
        try:
            backup.unlink()
            print(f"  ✓ Removido: arxiv_package/{backup.name}")
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ Erro: {e}")
    
    # Remove aux files from arxiv_package
    for aux_file in arxiv_pkg.glob("*.aux"):
        try:
            aux_file.unlink()
            print(f"  ✓ Removido: arxiv_package/{aux_file.name}")
            deleted_count += 1
        except Exception as e:
            pass
    
    for aux_file in arxiv_pkg.glob("*.log"):
        try:
            aux_file.unlink()
            print(f"  ✓ Removido: arxiv_package/{aux_file.name}")
            deleted_count += 1
        except Exception as e:
            pass
    
    for aux_file in arxiv_pkg.glob("*.out"):
        try:
            aux_file.unlink()
            print(f"  ✓ Removido: arxiv_package/{aux_file.name}")
            deleted_count += 1
        except Exception as e:
            pass
    
    for aux_file in arxiv_pkg.glob("*.bbl"):
        try:
            aux_file.unlink()
            deleted_count += 1
        except Exception as e:
            pass
    
    for aux_file in arxiv_pkg.glob("*.blg"):
        try:
            aux_file.unlink()
            deleted_count += 1
        except Exception as e:
            pass
    
    # Remove PNG files from figures (keep only PDFs)
    print("\n" + "=" * 80)
    print("REMOVENDO PNGs DAS FIGURAS (mantendo apenas PDFs)")
    print("=" * 80)
    
    for figures_dir in [base_dir / "figures", arxiv_pkg / "figures"]:
        if figures_dir.exists():
            for png_file in figures_dir.glob("*.png"):
                try:
                    png_file.unlink()
                    print(f"  ✓ Removido: {png_file.relative_to(base_dir)}")
                    deleted_count += 1
                except Exception as e:
                    print(f"  ✗ Erro: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("RESUMO DA LIMPEZA")
    print("=" * 80)
    print(f"\n  ✓ Arquivos movidos para toolkit: {moved_count}")
    print(f"  ✓ Arquivos removidos: {deleted_count}")
    print(f"\n  Toolkit archive: {toolkit_dir}")
    
    print("\n" + "=" * 80)
    print("ARQUIVOS ESSENCIAIS MANTIDOS")
    print("=" * 80)
    print("\n  ✓ main.tex (versão final)")
    print("  ✓ references.bib")
    print("  ✓ figures/ (apenas PDFs)")
    print("  ✓ arxiv_package/main.tex")
    print("  ✓ arxiv_package/main.pdf")
    print("  ✓ arxiv_package/figures/ (apenas PDFs)")
    print("  ✓ arxiv_submission_final_corrected.zip (PACOTE FINAL)")
    print("  ✓ SUBMIT_TO_ARXIV.md (guia de submissão)")
    print("  ✓ prepare_arxiv_package.py (script útil)")
    
    print("\n" + "=" * 80)
    print("✅ LIMPEZA CONCLUÍDA!")
    print("=" * 80)
    
    return moved_count, deleted_count

if __name__ == "__main__":
    moved, deleted = cleanup_arxiv_submission()
    print(f"\n✅ Total: {moved} movidos, {deleted} removidos")

