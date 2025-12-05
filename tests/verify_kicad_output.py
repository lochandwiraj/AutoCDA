import subprocess
from pathlib import Path
import json

class KiCadOutputVerifier:
    def __init__(self):
        self.output_dir = Path("output_api")
    
    def verify_netlist(self, netlist_path):
        """Verify netlist file is valid"""
        try:
            with open(netlist_path, 'r') as f:
                content = f.read()
            
            checks = {
                "file_exists": True,
                "not_empty": len(content) > 0,
                "has_components": "comp" in content.lower() or "part" in content.lower(),
                "has_nets": "net" in content.lower(),
                "valid_format": content.startswith("(") or content.startswith("<")
            }
            
            return {
                "valid": all(checks.values()),
                "checks": checks
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }
    
    def verify_all_outputs(self):
        """Verify all generated outputs"""
        results = []
        
        netlist_files = list(self.output_dir.glob("**/*.net"))
        
        for netlist in netlist_files:
            verification = self.verify_netlist(netlist)
            results.append({
                "file": str(netlist),
                "verification": verification
            })
        
        return results
    
    def generate_report(self):
        """Generate verification report"""
        results = self.verify_all_outputs()
        
        total = len(results)
        valid = sum(1 for r in results if r["verification"]["valid"])
        
        report = {
            "total_files": total,
            "valid_files": valid,
            "invalid_files": total - valid,
            "success_rate": (valid / total * 100) if total > 0 else 0,
            "details": results
        }
        
        # Save report
        report_file = Path("logs/kicad_verification_report.json")
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n{'='*50}")
        print("KICAD OUTPUT VERIFICATION REPORT")
        print(f"{'='*50}")
        print(f"Total files: {total}")
        print(f"Valid: {valid}")
        print(f"Invalid: {total - valid}")
        print(f"Success rate: {report['success_rate']:.1f}%")
        print(f"{'='*50}\n")
        
        return report

if __name__ == "__main__":
    verifier = KiCadOutputVerifier()
    verifier.generate_report()
