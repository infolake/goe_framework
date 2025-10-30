#!/usr/bin/env python3
"""
MCMC Files Analysis and Organization Script
Filename: analyze_root_mcmc_files.py
Last Modified: 2025-01-27
Purpose: Analyze all MCMC files in root directory, evaluate results quality and importance
"""

import numpy as np
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
from scipy import stats

class MCMCAnalyzer:
    """Analyze MCMC results and organize by quality and importance"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.mcmc_files = {}
        self.analysis_results = {}
        
    def find_mcmc_files(self) -> Dict[str, List[str]]:
        """Find all MCMC-related files in root directory"""
        files = {
            'data': [],
            'plots': [],
            'scripts': [],
            'metadata': []
        }
        
        # Search for files in root
        for file_path in self.root_dir.iterdir():
            if file_path.is_file():
                name_lower = file_path.name.lower()
                if 'mcmc' in name_lower:
                    ext = file_path.suffix.lower()
                    if ext in ['.npz', '.npy']:
                        files['data'].append(str(file_path))
                    elif ext in ['.png', '.jpg', '.pdf']:
                        files['plots'].append(str(file_path))
                    elif ext == '.py':
                        files['scripts'].append(str(file_path))
                    elif ext in ['.json', '.txt', '.md']:
                        files['metadata'].append(str(file_path))
        
        return files
    
    def analyze_npz_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze NPZ file containing MCMC results"""
        try:
            data = np.load(filepath)
            analysis = {
                'file': filepath,
                'type': 'npz',
                'keys': list(data.keys()),
                'size_mb': os.path.getsize(filepath) / (1024 * 1024),
                'data_info': {}
            }
            
            for key in data.keys():
                array = data[key]
                if hasattr(array, 'shape'):
                    analysis['data_info'][key] = {
                        'shape': array.shape,
                        'dtype': str(array.dtype),
                        'size': array.size,
                        'mean': float(np.mean(array)) if array.size > 0 else None,
                        'std': float(np.std(array)) if array.size > 0 else None,
                        'min': float(np.min(array)) if array.size > 0 else None,
                        'max': float(np.max(array)) if array.size > 0 else None
                    }
                else:
                    analysis['data_info'][key] = {
                        'value': str(array),
                        'type': type(array).__name__
                    }
            
            # Quality assessment
            analysis['quality_score'] = self._assess_quality_npz(analysis)
            analysis['importance_score'] = self._assess_importance_npz(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'file': filepath,
                'type': 'npz',
                'error': str(e),
                'quality_score': 0,
                'importance_score': 0
            }
    
    def analyze_npy_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze NPY file containing MCMC results"""
        try:
            array = np.load(filepath)
            analysis = {
                'file': filepath,
                'type': 'npy',
                'shape': array.shape,
                'size_mb': os.path.getsize(filepath) / (1024 * 1024),
                'dtype': str(array.dtype),
                'size': array.size,
                'mean': float(np.mean(array)) if array.size > 0 else None,
                'std': float(np.std(array)) if array.size > 0 else None,
                'min': float(np.min(array)) if array.size > 0 else None,
                'max': float(np.max(array)) if array.size > 0 else None
            }
            
            # Quality assessment
            analysis['quality_score'] = self._assess_quality_npy(analysis)
            analysis['importance_score'] = self._assess_importance_npy(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'file': filepath,
                'type': 'npy',
                'error': str(e),
                'quality_score': 0,
                'importance_score': 0
            }
    
    def analyze_plot_file(self, filepath: str) -> Dict[str, Any]:
        """Analyze plot file"""
        try:
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            analysis = {
                'file': filepath,
                'type': 'plot',
                'format': Path(filepath).suffix.lower(),
                'size_mb': size_mb,
                'exists': True
            }
            
            # Quality assessment based on file properties
            analysis['quality_score'] = self._assess_quality_plot(analysis)
            analysis['importance_score'] = self._assess_importance_plot(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'file': filepath,
                'type': 'plot',
                'error': str(e),
                'quality_score': 0,
                'importance_score': 0
            }
    
    def _assess_quality_npz(self, analysis: Dict) -> float:
        """Assess quality score for NPZ file (0-10 scale)"""
        score = 0.0
        
        # Check for expected keys
        expected_keys = ['posterior', 'best_params', 'chain', 'log_prob']
        found_keys = [k for k in expected_keys if k in analysis.get('keys', [])]
        
        # Score based on key presence
        score += len(found_keys) * 1.5
        
        # Score based on data size
        if analysis.get('size_mb', 0) > 0:
            score += min(analysis['size_mb'] / 10, 2.0)  # Max 2 points for size
        
        # Score based on sample count
        if 'posterior' in analysis.get('data_info', {}):
            posterior_info = analysis['data_info']['posterior']
            if posterior_info.get('size', 0) > 10000:
                score += 2.0
            elif posterior_info.get('size', 0) > 1000:
                score += 1.0
        
        # Check for statistics
        if 'best_params' in analysis.get('data_info', {}):
            score += 1.0
        
        return min(score, 10.0)
    
    def _assess_importance_npz(self, analysis: Dict) -> float:
        """Assess importance score for NPZ file (0-10 scale)"""
        score = 0.0
        filename = Path(analysis['file']).name.lower()
        
        # High importance keywords
        if 'large' in filename or 'complete' in filename:
            score += 3.0
        if 'g2' in filename or 'muon' in filename:
            score += 3.0
        if 'hadron' in filename:
            score += 2.0
        if 'final' in filename or 'best' in filename:
            score += 2.0
        
        # Importance based on sample size
        if 'posterior' in analysis.get('data_info', {}):
            size = analysis['data_info']['posterior'].get('size', 0)
            if size > 100000:
                score += 2.0
            elif size > 10000:
                score += 1.0
        
        return min(score, 10.0)
    
    def _assess_quality_npy(self, analysis: Dict) -> float:
        """Assess quality score for NPY file (0-10 scale)"""
        score = 0.0
        
        # Score based on data size
        size = analysis.get('size', 0)
        if size > 100000:
            score += 3.0
        elif size > 10000:
            score += 2.0
        elif size > 1000:
            score += 1.0
        
        # Score based on file size
        if analysis.get('size_mb', 0) > 1:
            score += 1.0
        
        # Check for reasonable statistics
        if analysis.get('std') is not None and analysis['std'] > 0:
            score += 1.0
        
        return min(score, 10.0)
    
    def _assess_importance_npy(self, analysis: Dict) -> float:
        """Assess importance score for NPY file (0-10 scale)"""
        score = 0.0
        filename = Path(analysis['file']).name.lower()
        
        # High importance keywords
        if 'large' in filename or 'complete' in filename:
            score += 3.0
        if 'bootstrap' in filename and '1m' in filename:
            score += 3.0
        if 'posterior' in filename:
            score += 2.0
        
        # Importance based on sample size
        size = analysis.get('size', 0)
        if size > 100000:
            score += 2.0
        elif size > 10000:
            score += 1.0
        
        return min(score, 10.0)
    
    def _assess_quality_plot(self, analysis: Dict) -> float:
        """Assess quality score for plot file (0-10 scale)"""
        score = 0.0
        
        # Score based on file size (larger = more detailed)
        size_mb = analysis.get('size_mb', 0)
        if size_mb > 1:
            score += 2.0
        elif size_mb > 0.5:
            score += 1.0
        
        # Prefer PNG/PDF over JPG
        if analysis.get('format') == '.png':
            score += 1.0
        elif analysis.get('format') == '.pdf':
            score += 1.5
        
        if analysis.get('exists'):
            score += 1.0
        
        return min(score, 10.0)
    
    def _assess_importance_plot(self, analysis: Dict) -> float:
        """Assess importance score for plot file (0-10 scale)"""
        score = 0.0
        filename = Path(analysis['file']).name.lower()
        
        # High importance keywords
        if 'complete' in filename or 'final' in filename:
            score += 3.0
        if 'diagnostic' in filename:
            score += 2.0
        if 'corner' in filename:
            score += 2.0
        if 'best_fit' in filename:
            score += 2.0
        if 'g2' in filename or 'muon' in filename:
            score += 2.0
        
        return min(score, 10.0)
    
    def analyze_all_files(self) -> Dict[str, Any]:
        """Analyze all MCMC files found"""
        files = self.find_mcmc_files()
        results = {
            'data_files': [],
            'plot_files': [],
            'summary': {}
        }
        
        print("="*80)
        print("ANALYZING MCMC FILES IN ROOT DIRECTORY")
        print("="*80)
        
        # Analyze data files
        print(f"\nFound {len(files['data'])} data files (.npz, .npy)")
        for filepath in files['data']:
            print(f"  Analyzing: {filepath}")
            if filepath.endswith('.npz'):
                analysis = self.analyze_npz_file(filepath)
            else:
                analysis = self.analyze_npy_file(filepath)
            results['data_files'].append(analysis)
        
        # Analyze plot files
        print(f"\nFound {len(files['plots'])} plot files")
        for filepath in files['plots']:
            print(f"  Analyzing: {filepath}")
            analysis = self.analyze_plot_file(filepath)
            results['plot_files'].append(analysis)
        
        # Generate summary
        results['summary'] = self._generate_summary(results)
        
        return results
    
    def _generate_summary(self, results: Dict) -> Dict[str, Any]:
        """Generate summary statistics"""
        summary = {
            'total_data_files': len(results['data_files']),
            'total_plot_files': len(results['plot_files']),
            'high_quality_data': [],
            'high_importance_data': [],
            'high_quality_plots': [],
            'high_importance_plots': [],
            'categories': {
                'critical': [],
                'important': [],
                'supporting': [],
                'low_priority': []
            }
        }
        
        # Classify data files
        for analysis in results['data_files']:
            quality = analysis.get('quality_score', 0)
            importance = analysis.get('importance_score', 0)
            combined = quality + importance
            
            if quality >= 7:
                summary['high_quality_data'].append(analysis['file'])
            if importance >= 7:
                summary['high_importance_data'].append(analysis['file'])
            
            # Categorize
            if combined >= 14:
                summary['categories']['critical'].append(analysis['file'])
            elif combined >= 10:
                summary['categories']['important'].append(analysis['file'])
            elif combined >= 6:
                summary['categories']['supporting'].append(analysis['file'])
            else:
                summary['categories']['low_priority'].append(analysis['file'])
        
        # Classify plot files
        for analysis in results['plot_files']:
            quality = analysis.get('quality_score', 0)
            importance = analysis.get('importance_score', 0)
            combined = quality + importance
            
            if quality >= 7:
                summary['high_quality_plots'].append(analysis['file'])
            if importance >= 7:
                summary['high_importance_plots'].append(analysis['file'])
            
            # Categorize
            if combined >= 14:
                summary['categories']['critical'].append(analysis['file'])
            elif combined >= 10:
                summary['categories']['important'].append(analysis['file'])
            elif combined >= 6:
                summary['categories']['supporting'].append(analysis['file'])
            else:
                summary['categories']['low_priority'].append(analysis['file'])
        
        return summary
    
    def print_report(self, results: Dict):
        """Print detailed analysis report"""
        print("\n" + "="*80)
        print("MCMC FILES ANALYSIS REPORT")
        print("="*80)
        
        # Data files
        print("\n" + "-"*80)
        print("DATA FILES (.npz, .npy)")
        print("-"*80)
        
        data_files = sorted(results['data_files'], 
                           key=lambda x: x.get('quality_score', 0) + x.get('importance_score', 0),
                           reverse=True)
        
        for i, analysis in enumerate(data_files, 1):
            print(f"\n{i}. {Path(analysis['file']).name}")
            print(f"   Quality Score: {analysis.get('quality_score', 0):.1f}/10")
            print(f"   Importance Score: {analysis.get('importance_score', 0):.1f}/10")
            print(f"   Combined Score: {analysis.get('quality_score', 0) + analysis.get('importance_score', 0):.1f}/20")
            
            if 'error' in analysis:
                print(f"   ERROR: {analysis['error']}")
            else:
                if analysis['type'] == 'npz':
                    print(f"   Keys: {analysis.get('keys', [])}")
                    print(f"   Size: {analysis.get('size_mb', 0):.2f} MB")
                    for key, info in analysis.get('data_info', {}).items():
                        if 'shape' in info:
                            print(f"     {key}: shape={info['shape']}, mean={info.get('mean', 'N/A')}")
                else:
                    print(f"   Shape: {analysis.get('shape', 'N/A')}")
                    print(f"   Size: {analysis.get('size_mb', 0):.2f} MB")
                    print(f"   Mean: {analysis.get('mean', 'N/A')}")
                    print(f"   Std: {analysis.get('std', 'N/A')}")
        
        # Plot files
        print("\n" + "-"*80)
        print("PLOT FILES (.png, .pdf)")
        print("-"*80)
        
        plot_files = sorted(results['plot_files'],
                           key=lambda x: x.get('quality_score', 0) + x.get('importance_score', 0),
                           reverse=True)
        
        for i, analysis in enumerate(plot_files, 1):
            print(f"\n{i}. {Path(analysis['file']).name}")
            print(f"   Quality Score: {analysis.get('quality_score', 0):.1f}/10")
            print(f"   Importance Score: {analysis.get('importance_score', 0):.1f}/10")
            print(f"   Combined Score: {analysis.get('quality_score', 0) + analysis.get('importance_score', 0):.1f}/20")
            print(f"   Format: {analysis.get('format', 'N/A')}")
            print(f"   Size: {analysis.get('size_mb', 0):.2f} MB")
        
        # Summary by category
        print("\n" + "="*80)
        print("ORGANIZATION BY IMPORTANCE AND QUALITY")
        print("="*80)
        
        summary = results['summary']
        categories = summary['categories']
        
        print("\n🔴 CRITICAL (Combined Score ≥ 14/20):")
        for filepath in categories['critical']:
            print(f"   • {Path(filepath).name}")
        
        print("\n🟡 IMPORTANT (Combined Score ≥ 10/20):")
        for filepath in categories['important']:
            print(f"   • {Path(filepath).name}")
        
        print("\n🟢 SUPPORTING (Combined Score ≥ 6/20):")
        for filepath in categories['supporting']:
            print(f"   • {Path(filepath).name}")
        
        print("\n⚪ LOW PRIORITY (Combined Score < 6/20):")
        for filepath in categories['low_priority']:
            print(f"   • {Path(filepath).name}")
        
        print("\n" + "="*80)
        print("SUMMARY STATISTICS")
        print("="*80)
        print(f"Total Data Files: {summary['total_data_files']}")
        print(f"Total Plot Files: {summary['total_plot_files']}")
        print(f"High Quality Data Files: {len(summary['high_quality_data'])}")
        print(f"High Importance Data Files: {len(summary['high_importance_data'])}")
        print(f"High Quality Plots: {len(summary['high_quality_plots'])}")
        print(f"High Importance Plots: {len(summary['high_importance_plots'])}")
        
    def save_report(self, results: Dict, output_file: str = "mcmc_analysis_report.json"):
        """Save analysis report to JSON file"""
        # Convert numpy types to Python types for JSON serialization
        def convert_to_json(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert_to_json(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_json(item) for item in obj]
            return obj
        
        json_results = convert_to_json(results)
        
        with open(output_file, 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print(f"\nReport saved to: {output_file}")


def main():
    """Main execution function"""
    analyzer = MCMCAnalyzer(root_dir=".")
    results = analyzer.analyze_all_files()
    analyzer.print_report(results)
    analyzer.save_report(results, "mcmc_analysis_report.json")
    
    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)


if __name__ == "__main__":
    main()

