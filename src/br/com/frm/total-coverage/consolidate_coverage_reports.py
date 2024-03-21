import os
import glob
import xml.etree.ElementTree as ET


class ConsolidateCoverageReports:
    def extract_coverage_from_report(self, report_paths):
        covered = 0.0
        covered_lines =0
        covered_missed =0
        for report_path in report_paths:
            print(f"\n\n Path of reports {report_path}")
            tree = ET.parse(report_path)
            root = tree.getroot()
            for report_package in root.iter('package'):
                for report_class in report_package.iter('class'):
                    for report_method in report_class.iter('method'):
                        for report_counter in report_method.iter('counter'):
                            if report_counter.attrib['type'] == 'LINE':
                                covered_lines += float(report_counter.attrib['covered'])
                                covered_missed += float(report_counter.attrib['missed'])
        
        covered = covered_lines / (covered_lines + covered_missed) * 100

        return covered

    def consolidate_coverage_reports(self, report_directories):
        total_covered = 0
        total_missed = 0
        total_elements = 0

        # Encontrar todos os relatórios de cobertura no diretório
        coverage_reports =[]
        for report_directory in report_directories:
            reports_files = glob.glob(os.path.join(report_directory, '*.xml'))
            for report_file in reports_files:                        
                coverage_reports.append(report_file)

        coverage = self.extract_coverage_from_report(coverage_reports)
        total_covered += coverage
        total_missed += 100 - coverage
        total_elements += 100  # Total de linhas cobertas e não cobertas

        # Calcular a cobertura consolidada
        consolidated_coverage = 0
            
        if(total_covered> 0 and total_elements> 0): 
            consolidated_coverage = total_covered / total_elements * 100

        print("\nCobertura Consolidada:")
        print(f"Linhas Cobertas: {total_covered:.2f}%")
        print(f"Linhas Não Cobertas: {total_missed:.2f}%")
        print(f"Cobertura Total: {consolidated_coverage:.2f}%")

