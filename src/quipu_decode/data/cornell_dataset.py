#!/usr/bin/env python3
"""
QUIPU-DECODE Framework v1.0 - Cornell University Dataset Integration
Tools for accessing and converting Cornell University quipu database

Cornell University Quipu Database:
https://courses.cit.cornell.edu/quipu/contents.htm

This module provides tools to:
1. Access the Cornell online database
2. Parse quipu data from HTML pages
3. Convert to QUIPU-DECODE JSON format
4. Validate converted data
5. Integrate with framework analysis
"""

import requests
import re
import json
import logging
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
from bs4 import BeautifulSoup
import urllib.parse

# PDF processing
try:
    from pdfminer.high_level import extract_text
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFTextExtractionNotAllowed
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logging.warning("PDF processing libraries not available. Install pdfminer.six for PDF parsing.")


class CornellQuipuParser:
    """
    Parser for Cornell University quipu database

    This class handles parsing of quipu data from the Cornell University
    online database and conversion to QUIPU-DECODE format.
    """

    def __init__(self):
        """Initialize the Cornell parser"""
        self.base_url = "https://courses.cit.cornell.edu/quipu/"
        self.logger = logging.getLogger(__name__)

        # Known quipu catalog from Cornell
        self.quipu_catalog = self._load_quipu_catalog()

    def _load_quipu_catalog(self) -> Dict[str, str]:
        """Load the quipu catalog from Cornell"""
        # This would typically fetch from the Cornell website
        # For now, using known catalog data
        return {
            "k001": "https://courses.cit.cornell.edu/quipu/k001.htm",
            "k002": "https://courses.cit.cornell.edu/quipu/k002.htm",
            # Add more as needed from the actual catalog
        }

    def fetch_quipu_data(self, quipu_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch quipu data from Cornell database

        Args:
            quipu_id: Cornell quipu identifier (e.g., 'k001')

        Returns:
            Parsed quipu data or None if not found
        """
        if quipu_id not in self.quipu_catalog:
            self.logger.error(f"Quipu {quipu_id} not found in Cornell catalog")
            return None

        url = self.quipu_catalog[quipu_id]

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            return self._parse_quipu_html(response.text, quipu_id)

        except Exception as e:
            self.logger.error(f"Failed to fetch quipu {quipu_id}: {e}")
            return None

    def _parse_quipu_html(self, html_content: str, quipu_id: str) -> Dict[str, Any]:
        """
        Parse quipu data from Cornell HTML page

        Args:
            html_content: HTML content from Cornell page
            quipu_id: Quipu identifier

        Returns:
            Parsed quipu data in QUIPU-DECODE format
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract basic information
        title = soup.find('title')
        title_text = title.get_text() if title else f"Quipu {quipu_id.upper()}"

        # Initialize quipu data structure
        quipu_data = {
            'quipu_id': f"CORNELL_{quipu_id.upper()}",
            'collection_info': {
                'source': 'Cornell University',
                'catalog_number': quipu_id.upper(),
                'url': self.quipu_catalog[quipu_id],
                'title': title_text
            },
            'primary_cord': {},
            'pendant_cords': [],
            'materials': [],
            'colors': [],
            'knot_types': [],
            'hierarchy_levels': 1,
            'total_knots': 0,
            'total_cords': 0,
            'archaeological_context': {
                'source': 'Cornell University Database',
                'reference': title_text
            }
        }

        # Parse main content
        content = soup.find('body')
        if content:
            # Extract text content and parse structured data
            text_content = content.get_text()

            # Parse measurements, materials, colors from text
            quipu_data.update(self._parse_text_content(text_content))

            # Parse any tabular data
            tables = soup.find_all('table')
            if tables:
                quipu_data.update(self._parse_table_data(tables))

        return quipu_data

    def _parse_text_content(self, text: str) -> Dict[str, Any]:
        """Parse structured information from text content"""
        parsed_data = {}

        # Common patterns in Cornell descriptions
        patterns = {
            'materials': r'materials?\s*:?\s*([^\n\r]+)',
            'colors': r'colors?\s*:?\s*([^\n\r]+)',
            'knots': r'knots?\s*:?\s*([^\n\r]+)',
            'cords': r'cords?\s*:?\s*([^\n\r]+)',
            'length': r'length\s*:?\s*([^\n\r]+)',
            'width': r'width\s*:?\s*([^\n\r]+)',
            'provenance': r'provenance\s*:?\s*([^\n\r]+)',
            'site': r'site\s*:?\s*([^\n\r]+)',
            'period': r'period\s*:?\s*([^\n\r]+)',
            'culture': r'culture\s*:?\s*([^\n\r]+)'
        }

        for field, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                parsed_data[field] = matches[0].strip()

        return parsed_data

    def _parse_table_data(self, tables: List) -> Dict[str, Any]:
        """Parse tabular data from Cornell pages"""
        table_data = {}

        for table in tables:
            # Simple table parsing - would need customization for Cornell format
            rows = table.find_all('tr')
            if len(rows) > 1:
                # Assume first row is headers
                headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])]

                # Parse data rows
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) == len(headers):
                        for i, (header, cell) in enumerate(zip(headers, cells)):
                            value = cell.get_text().strip()
                            if value:
                                if header not in table_data:
                                    table_data[header] = []
                                table_data[header].append(value)

        return table_data

    def convert_to_quipu_format(self, cornell_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert Cornell data to QUIPU-DECODE format

        Args:
            cornell_data: Raw data from Cornell parser

        Returns:
            Standardized QUIPU-DECODE format
        """
        # Map Cornell fields to QUIPU-DECODE format
        converted = {
            'quipu_id': cornell_data['quipu_id'],
            'collection_info': cornell_data['collection_info'],
            'archaeological_context': cornell_data.get('archaeological_context', {})
        }

        # Convert materials
        if 'materials' in cornell_data:
            materials_text = cornell_data['materials']
            converted['materials'] = [m.strip() for m in materials_text.split(',') if m.strip()]

        # Convert colors
        if 'colors' in cornell_data:
            colors_text = cornell_data['colors']
            converted['colors'] = [c.strip() for c in colors_text.split(',') if c.strip()]

        # Convert measurements
        measurements = {}
        for field in ['length', 'width', 'thickness', 'weight']:
            if field in cornell_data:
                try:
                    # Extract numeric value
                    value_match = re.search(r'(\d+\.?\d*)', cornell_data[field])
                    if value_match:
                        measurements[field] = float(value_match.group(1))
                except (ValueError, AttributeError):
                    pass

        if measurements:
            converted['dimensions'] = measurements

        # Convert structural information
        if 'knots' in cornell_data:
            converted['total_knots'] = self._extract_numeric_value(cornell_data['knots'])

        if 'cords' in cornell_data:
            converted['total_cords'] = self._extract_numeric_value(cornell_data['cords'])

        # Set default hierarchy levels (would need more sophisticated parsing)
        converted['hierarchy_levels'] = 2

        # Create basic primary cord (placeholder)
        converted['primary_cord'] = {
            'material': converted['materials'][0] if converted['materials'] else 'cotton',
            'color': converted['colors'][0] if converted['colors'] else 'natural',
            'length': measurements.get('length', 30.0)
        }

        # Create basic pendant cords (placeholder structure)
        converted['pendant_cords'] = []
        if converted['total_cords'] > 1:
            for i in range(1, min(converted['total_cords'], 10)):  # Limit to 10 for basic structure
                converted['pendant_cords'].append({
                    'position': i,
                    'material': converted['materials'][0] if converted['materials'] else 'cotton',
                    'color': converted['colors'][i % len(converted['colors'])] if converted['colors'] else 'natural',
                    'length': measurements.get('length', 30.0) * 0.6,
                    'knots': []
                })

        # Set knot types based on available information
        converted['knot_types'] = ['single_knot']  # Default

        return converted

    def _extract_numeric_value(self, text: str) -> int:
        """Extract numeric value from text"""
        match = re.search(r'(\d+)', text)
        return int(match.group(1)) if match else 0

    def download_quipu_collection(self, output_dir: str = "data/cornell",
                                quipu_ids: Optional[List[str]] = None) -> List[str]:
        """
        Download multiple quipus from Cornell database

        Args:
            output_dir: Directory to save converted data
            quipu_ids: List of quipu IDs to download (if None, download all)

        Returns:
            List of saved file paths
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_files = []

        if quipu_ids is None:
            quipu_ids = list(self.quipu_catalog.keys())

        for quipu_id in quipu_ids:
            self.logger.info(f"Downloading quipu {quipu_id}")

            # Fetch data
            cornell_data = self.fetch_quipu_data(quipu_id)
            if cornell_data is None:
                continue

            # Convert to QUIPU-DECODE format
            converted_data = self.convert_to_quipu_format(cornell_data)

            # Save as JSON
            output_file = output_path / f"cornell_{quipu_id}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(converted_data, f, indent=2, ensure_ascii=False)

            saved_files.append(str(output_file))

        self.logger.info(f"Downloaded {len(saved_files)} quipus to {output_dir}")
        return saved_files

    def parse_quipu_pdf(self, pdf_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        Parse quipu data from Cornell PDF file

        Args:
            pdf_path: Path to Cornell PDF file

        Returns:
            Parsed quipu data in QUIPU-DECODE format
        """
        if not PDF_AVAILABLE:
            self.logger.error("PDF processing not available. Install pdfminer.six.")
            return None

        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            self.logger.error(f"PDF file not found: {pdf_path}")
            return None

        try:
            # Extract text from PDF
            text_content = extract_text(str(pdf_path))

            # Ensure text_content is a string
            if isinstance(text_content, list):
                text_content = ' '.join(text_content)

            # Parse the extracted text
            return self._parse_pdf_text(text_content, pdf_path.stem)

        except Exception as e:
            self.logger.error(f"Failed to parse PDF {pdf_path}: {e}")
            return None

    def _parse_pdf_text(self, text_content: str, quipu_id: str) -> Dict[str, Any]:
        """
        Parse text extracted from Cornell PDF

        Args:
            text_content: Text extracted from PDF
            quipu_id: Quipu identifier (e.g., 'as10')

        Returns:
            Parsed quipu data
        """
        # Cornell PDF format patterns
        cornell_data = {
            'quipu_id': f'CORNELL_{quipu_id.upper()}',
            'collection_info': {
                'source': 'Cornell University',
                'catalog_number': quipu_id.upper(),
                'url': f'https://courses.cit.cornell.edu/quipu/data/{quipu_id.lower()}.pdf',
                'format': 'PDF'
            },
            'primary_cord': {},
            'pendant_cords': [],
            'materials': [],
            'colors': [],
            'knot_types': [],
            'hierarchy_levels': 1,
            'total_knots': 0,
            'total_cords': 0,
            'archaeological_context': {
                'source': 'Cornell University Database',
                'reference': quipu_id.upper(),
                'extraction_method': 'PDF text extraction'
            }
        }

        # Clean and normalize text
        if not isinstance(text_content, str):
            text_content = str(text_content)
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]

        # Parse Cornell-specific format
        cornell_data.update(self._parse_cornell_format(lines))

        # Convert to QUIPU-DECODE format
        return self.convert_to_quipu_format(cornell_data)

    def _parse_cornell_format(self, lines: List[str]) -> Dict[str, Any]:
        """
        Parse Cornell-specific quipu description format

        Args:
            lines: Text lines from PDF

        Returns:
            Parsed Cornell data
        """
        parsed_data = {}

        # Cornell format patterns
        patterns = {
            'tag': r'TAG\s*[:\-]?\s*([A-Z0-9]+)',
            'provenance': r'PROVENANCE\s*[:\-]?\s*([^\n\r]+)',
            'material': r'MATERIAL\s*[:\-]?\s*([^\n\r]+)',
            'colors': r'COLORS?\s*[:\-]?\s*([^\n\r]+)',
            'knots': r'KNOTS?\s*[:\-]?\s*([^\n\r]+)',
            'cords': r'CORDS?\s*[:\-]?\s*([^\n\r]+)',
            'length': r'LENGTH\s*[:\-]?\s*([^\n\r]+)',
            'width': r'WIDTH\s*[:\-]?\s*([^\n\r]+)',
            'thickness': r'THICKNESS\s*[:\-]?\s*([^\n\r]+)',
            'observations': r'OBSERVATIONS?\s*[:\-]?\s*([^\n\r]+)',
            'construction': r'CONSTRUCTION\s*[:\-]?\s*([^\n\r]+)'
        }

        # Extract information using patterns
        for line in lines:
            for field, pattern in patterns.items():
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    parsed_data[field] = match.group(1).strip()

        # Extract numerical values
        numerical_data = self._extract_numerical_data(lines)
        parsed_data.update(numerical_data)

        # Extract structural information
        structural_data = self._extract_structural_data(lines)
        parsed_data.update(structural_data)

        return parsed_data

    def _extract_numerical_data(self, lines: List[str]) -> Dict[str, Any]:
        """Extract numerical measurements from Cornell PDF"""
        numerical = {}

        # Look for measurements in various formats
        measurement_patterns = [
            (r'(\d+\.?\d*)\s*cm', 'length_cm'),
            (r'(\d+\.?\d*)\s*mm', 'length_mm'),
            (r'(\d+)\s*cords?', 'total_cords'),
            (r'(\d+)\s*knots?', 'total_knots'),
            (r'(\d+)\s*pendants?', 'pendant_count'),
            (r'(\d+)\s*levels?', 'hierarchy_levels')
        ]

        combined_text = ' '.join(lines)

        for pattern, field in measurement_patterns:
            match = re.search(pattern, combined_text, re.IGNORECASE)
            if match:
                try:
                    numerical[field] = float(match.group(1))
                except ValueError:
                    numerical[field] = int(match.group(1))

        return numerical

    def _extract_structural_data(self, lines: List[str]) -> Dict[str, Any]:
        """Extract structural information from Cornell description"""
        structural = {}

        # Look for cord descriptions
        cord_info = []
        in_cord_section = False

        for line in lines:
            # Look for cord markers (common in Cornell format)
            if re.search(r'P\d+', line) or re.search(r'CORD\s*\d+', line, re.IGNORECASE):
                in_cord_section = True
                cord_info.append(line)
            elif in_cord_section and line.strip():
                cord_info.append(line)

        structural['cord_descriptions'] = cord_info

        # Extract colors and materials
        all_text = ' '.join(lines)

        # Color extraction
        color_matches = re.findall(r'\b(red|blue|yellow|green|brown|black|white|natural|cream|gray|purple|orange)\b', all_text, re.IGNORECASE)
        if color_matches:
            structural['colors'] = list(set(color_matches))

        # Material extraction
        material_matches = re.findall(r'\b(cotton|wool|fiber|thread|yarn|string|cord)\b', all_text, re.IGNORECASE)
        if material_matches:
            structural['materials'] = list(set(material_matches))

        return structural

    def extract_text_from_pdf(self, pdf_path: Union[str, Path]) -> Optional[str]:
        """
        Extract text from PDF file using pdfminer

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text or None if extraction fails
        """
        if not PDF_AVAILABLE:
            return None

        try:
            text = extract_text(str(pdf_path))
            return text
        except Exception as e:
            self.logger.error(f"Failed to extract text from PDF: {e}")
            return None

    def batch_parse_cornell_pdfs(self, pdf_directory: Union[str, Path],
                                output_directory: Union[str, Path]) -> List[str]:
        """
        Parse multiple Cornell PDF files in batch

        Args:
            pdf_directory: Directory containing Cornell PDFs
            output_directory: Directory to save converted JSON files

        Returns:
            List of successfully parsed files
        """
        pdf_dir = Path(pdf_directory)
        output_dir = Path(output_directory)
        output_dir.mkdir(parents=True, exist_ok=True)

        if not pdf_dir.exists():
            self.logger.error(f"PDF directory not found: {pdf_dir}")
            return []

        # Find all PDF files
        pdf_files = list(pdf_dir.glob("*.pdf"))
        self.logger.info(f"Found {len(pdf_files)} PDF files to process")

        successful_parses = []

        for pdf_file in pdf_files:
            self.logger.info(f"Processing {pdf_file.name}")

            # Parse PDF
            quipu_data = self.parse_quipu_pdf(pdf_file)
            if quipu_data is None:
                continue

            # Save as JSON
            output_file = output_dir / f"{pdf_file.stem}_parsed.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(quipu_data, f, indent=2, ensure_ascii=False)

            successful_parses.append(str(output_file))

        self.logger.info(f"Successfully parsed {len(successful_parses)}/{len(pdf_files)} PDFs")
        return successful_parses


def validate_cornell_conversion(quipu_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate converted Cornell data against QUIPU-DECODE requirements

    Args:
        quipu_data: Converted quipu data

    Returns:
        Validation results
    """
    validation = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'completeness_score': 0.0
    }

    # Check required fields
    required_fields = [
        'quipu_id', 'primary_cord', 'pendant_cords',
        'materials', 'colors', 'hierarchy_levels', 'total_knots', 'total_cords'
    ]

    present_fields = 0
    for field in required_fields:
        if field in quipu_data and quipu_data[field]:
            present_fields += 1
        else:
            validation['errors'].append(f"Missing required field: {field}")

    validation['completeness_score'] = present_fields / len(required_fields)

    if validation['errors']:
        validation['is_valid'] = False

    # Check data types and ranges
    if 'hierarchy_levels' in quipu_data:
        if not isinstance(quipu_data['hierarchy_levels'], int) or quipu_data['hierarchy_levels'] < 1:
            validation['errors'].append("Invalid hierarchy_levels")

    if 'total_knots' in quipu_data:
        if not isinstance(quipu_data['total_knots'], int) or quipu_data['total_knots'] < 0:
            validation['errors'].append("Invalid total_knots")

    # Warnings for incomplete data
    if validation['completeness_score'] < 0.8:
        validation['warnings'].append("Low completeness score")

    if not quipu_data.get('archaeological_context'):
        validation['warnings'].append("Missing archaeological context")

    return validation


def example_cornell_integration():
    """Example of integrating Cornell data with QUIPU-DECODE framework"""
    print("Cornell University Quipu Database Integration Example")
    print("=" * 60)

    # Initialize parser
    parser = CornellQuipuParser()

    # Download sample quipus
    print("Downloading sample quipus from Cornell...")
    downloaded_files = parser.download_quipu_collection("data/cornell_sample", ["k001", "k002"])

    print(f"Downloaded {len(downloaded_files)} quipus")

    # Validate and analyze
    from quipu_decode.core import QuipuAnalyzer

    analyzer = QuipuAnalyzer()

    for file_path in downloaded_files:
        print(f"\nAnalyzing {file_path}")

        # Load and validate
        with open(file_path, 'r', encoding='utf-8') as f:
            quipu_data = json.load(f)

        validation = validate_cornell_conversion(quipu_data)
        print(f"  Validation: {'PASS' if validation['is_valid'] else 'FAIL'}")
        print(f"  Completeness: {validation['completeness_score']:.1%}")

        if validation['errors']:
            print(f"  Errors: {validation['errors']}")

        if validation['warnings']:
            print(f"  Warnings: {validation['warnings']}")

        # Run analysis if valid
        if validation['is_valid']:
            try:
                results = analyzer.analyze_from_data(quipu_data)
                print(f"  Reliability: {results.reliability_score:.3f}")
                print(f"  Complexity: {results.complexity_index:.3f}")
                print(f"  Classification: {results.functional_classification}")
            except Exception as e:
                print(f"  Analysis failed: {e}")

    print("\nCornell integration example completed!")


if __name__ == "__main__":
    example_cornell_integration()
