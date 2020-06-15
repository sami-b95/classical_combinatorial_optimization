import os
import subprocess
import tempfile


class BiqCrunchWrapper():
    def __init__(self, biqcrunch_dir):
        self.biqcrunch_dir = biqcrunch_dir
    
    def max_cut(self, g):
        # Define .lp and .bc filenames
        with tempfile.TemporaryDirectory() as tmp_dir_path:
            lp_filename = os.path.join(tmp_dir_path, "example.lp")
            bc_filename = os.path.join(tmp_dir_path, "example.bc")
            # Include quadratic terms
            binary_polynomial = " "
            for v, neighbours_v in g.items():
                for neighbour_v in neighbours_v:
                    if neighbour_v < v:
                        continue
                    binary_polynomial += f" - 2 x{v}*x{neighbour_v}"
            # Include linear terms
            binary_polynomial += "\n "
            for v, neighbours_v in g.items():
                binary_polynomial += f" + {len(neighbours_v)} x{v}"
            # Save file
            with open(lp_filename, "w") as lp_file:
                lp_file.write("Maximize\n\n")
                lp_file.write(binary_polynomial)
                lp_file.write("\n\nBinary\n\n")
                lp_file.write("  " + " ".join([f"x{v}" for v in g]))
                lp_file.write("\n\nEnd")
            # Convert LP to BC
            os.system(f"python3.7 {self.biqcrunch_dir}/tools/lp2bc.py {lp_filename} > {bc_filename}")
            # Execute BiqCrunch
            output = subprocess.check_output([f"{self.biqcrunch_dir}/problems/generic/biqcrunch", bc_filename, f"{self.biqcrunch_dir}/problems/max-cut/biq_crunch.param"])
            return int(str(output).split("Maximum value = ")[1].split("\\n")[0])