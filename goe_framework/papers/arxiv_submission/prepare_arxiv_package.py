"""
Prepare arXiv submission package
File: prepare_arxiv_package.py
Date: 2025-10-29
"""

import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def prepare_arxiv_package():
    """
    Create complete arXiv submission package following arXiv guidelines
    """
    print("=" * 80)
    print("PREPARANDO PACOTE PARA SUBMISSÃO AO ARXIV")
    print("=" * 80)
    
    # Diretórios (relative to current directory: arxiv_submission)
    arxiv_pkg_dir = Path("arxiv_package")
    output_dir = Path("arxiv_submission_package")
    
    # Criar diretório de saída
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    
    print(f"\n✓ Diretório de saída criado: {output_dir}")
    
    # 1. Copiar main.tex
    shutil.copy(arxiv_pkg_dir / "main.tex", output_dir / "main.tex")
    print("✓ Copiado: main.tex")
    
    # 2. Copiar references.bib (se existir)
    if Path("references.bib").exists():
        shutil.copy(Path("references.bib"), output_dir / "references.bib")
        print("✓ Copiado: references.bib")
    elif (arxiv_pkg_dir / "references.bib").exists():
        shutil.copy(arxiv_pkg_dir / "references.bib", output_dir / "references.bib")
        print("✓ Copiado: references.bib (do arxiv_package)")
    else:
        print("⚠ Aviso: references.bib não encontrado")
    
    # 3. Copiar pasta de figuras
    figures_src = arxiv_pkg_dir / "figures"
    figures_dst = output_dir / "figures"
    
    if figures_src.exists():
        shutil.copytree(figures_src, figures_dst)
        
        # Contar figuras PDF
        pdf_files = list(figures_dst.glob("*.pdf"))
        print(f"✓ Copiado: {len(pdf_files)} figuras PDF")
        
        # Remover PNGs (arXiv prefere PDF)
        png_files = list(figures_dst.glob("*.png"))
        for png in png_files:
            png.unlink()
        if png_files:
            print(f"✓ Removido: {len(png_files)} arquivos PNG (mantendo apenas PDF)")
    else:
        print("⚠ Aviso: pasta figures não encontrada")
    
    # 4. Criar arquivo README para o arXiv
    readme_content = f"""README for arXiv submission

Title: Geometrodynamics of Entropy: Fermion Mass Quantization and Cosmological Bounce
Author: Guilherme de Camargo
Date: {datetime.now().strftime("%Y-%m-%d")}

Files included:
- main.tex: Main LaTeX manuscript
- references.bib: Bibliography database
- figures/: Directory containing all figures in PDF format

Compilation instructions:
1. pdflatex main.tex
2. bibtex main
3. pdflatex main.tex
4. pdflatex main.tex

Expected output: main.pdf (45 pages)

All figures are in PDF format as recommended by arXiv.
Statistical validation results are integrated in the manuscript.

Contact: camargo@phiq.io
ORCID: 0009-0004-8913-9419
"""
    
    with open(output_dir / "README.txt", "w") as f:
        f.write(readme_content)
    print("✓ Criado: README.txt")
    
    # 5. Criar arquivo .zip para submissão
    zip_name = f"arxiv_submission_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = Path(".") / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in output_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(output_dir)
                zipf.write(file, arcname)
    
    zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB
    print(f"\n✓ Criado arquivo ZIP: {zip_name}")
    print(f"  Tamanho: {zip_size:.2f} MB")
    
    # 6. Gerar relatório de conteúdo
    print("\n" + "=" * 80)
    print("CONTEÚDO DO PACOTE")
    print("=" * 80)
    
    print("\n📄 Arquivos principais:")
    for item in sorted(output_dir.glob("*")):
        if item.is_file():
            size_kb = item.stat().st_size / 1024
            print(f"  - {item.name:40s} {size_kb:>8.1f} KB")
    
    if figures_dst.exists():
        print(f"\n📊 Figuras ({len(pdf_files)} PDFs):")
        for fig in sorted(pdf_files)[:10]:  # Mostrar apenas primeiras 10
            size_kb = fig.stat().st_size / 1024
            print(f"  - {fig.name:40s} {size_kb:>8.1f} KB")
        if len(pdf_files) > 10:
            print(f"  ... e mais {len(pdf_files) - 10} figuras")
    
    # 7. Verificações finais
    print("\n" + "=" * 80)
    print("VERIFICAÇÕES")
    print("=" * 80)
    
    checks = {
        "main.tex existe": (output_dir / "main.tex").exists(),
        "references.bib existe": (output_dir / "references.bib").exists(),
        "Pasta figures existe": (output_dir / "figures").exists(),
        "Figuras PDF presentes": len(pdf_files) > 0 if figures_dst.exists() else False,
        "Sem arquivos PNG": len(list(figures_dst.glob("*.png"))) == 0 if figures_dst.exists() else True,
        "ZIP criado": zip_path.exists(),
        "README incluído": (output_dir / "README.txt").exists(),
    }
    
    all_ok = True
    for check, status in checks.items():
        symbol = "✅" if status else "❌"
        print(f"  {symbol} {check}")
        if not status:
            all_ok = False
    
    # 8. Instruções finais
    print("\n" + "=" * 80)
    print("PRÓXIMOS PASSOS PARA SUBMISSÃO AO ARXIV")
    print("=" * 80)
    
    print(f"""
1. Revisar o conteúdo em: {output_dir}

2. Testar compilação localmente:
   cd {output_dir}
   pdflatex main.tex
   bibtex main
   pdflatex main.tex
   pdflatex main.tex

3. Submeter ao arXiv:
   - Acesse: https://arxiv.org/submit
   - Faça upload do arquivo: {zip_name}
   - Ou faça upload individual dos arquivos da pasta: {output_dir.name}

4. Metadados sugeridos:
   - Primary: hep-th (High Energy Physics - Theory)
   - Secondary: gr-qc (General Relativity and Quantum Cosmology)
   - Secondary: hep-ph (High Energy Physics - Phenomenology)

5. Abstract: Usar o abstract do main.tex

6. Comentários: "All figures in PDF format. Reproducible code available at GitHub."
""")
    
    print("=" * 80)
    if all_ok:
        print("✅ PACOTE PRONTO PARA SUBMISSÃO AO ARXIV!")
    else:
        print("⚠️ ATENÇÃO: Algumas verificações falharam. Revisar acima.")
    print("=" * 80)
    
    return output_dir, zip_path

if __name__ == "__main__":
    prepare_arxiv_package()

