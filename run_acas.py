from mapleDNNsat import Solver
import glob
import itertools
import pdb
import os
import time
import subprocess
import random
import math
import multiprocessing as mp
from progress.bar import Bar

TIMEOUT = 10 * 60
TOTAL_CORES= mp.cpu_count()
JOB_CORES = 4
MEM_PER_JOB = 4
CWD = None


class Bab:
    cmd = f'bash {os.getcwd()}/run/run_bab.sh'

class ERAN:
    cmd = f'bash {os.getcwd()}/run/run_eran.sh'

class Marabou:
    cmd = f'bash {os.getcwd()}/run/run_marabou.sh'

class MIPVerify:
    cmd = f'bash {os.getcwd()}/run/run_mipverify.sh'

class Neurify:
    cmd = f'bash {os.getcwd()}/run/run_neurify.sh'

class nnenum:
    cmd = f'bash {os.getcwd()}/run/run_nnenum.sh'

class Planet:
    cmd = f'bash {os.getcwd()}/run/run_planet.sh'

class ReluPlex:
    cmd = f'bash {os.getcwd()}/run/run_reluplex.sh'

class verinet:
    cmd = f'bash {os.getcwd()}/run/run_verinet.sh'

class maple_gurobi:
    cmd = f'bash {os.getcwd()}/run/run_verinet.sh'

class maple_scip:
    cmd = f'bash {os.getcwd()}/run/run_verinet.sh'

class maple_cvc5:
    cmd = f'bash {os.getcwd()}/run/run_verinet.sh'


class Benchmark:
    id_iter = itertools.count()
    def __init__(self, dnn, vnnlib):
        self.dnn = dnn
        self.vnnlib = vnnlib
        self.bid = next(Benchmark.id_iter)

    def __str__(self) -> str:
        return f"({self.dnn},{self.vnnlib})"
    __repr__ = __str__

class Job:
    def __init__(self, benchmark, solver):
        self.benchmark   = benchmark
        self.solver      = solver
    def __str__(self) -> str:
        return f"({self.benchmark},{self.solver.__name__})"
    __repr__ = __str__

def run_command(command):
    start = time.time()
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    proc_stdout, proc_stderr = process.communicate()
    wall_time = time.time() - start
    proc_stdout = proc_stdout.decode('utf-8').strip()
    proc_stderr = proc_stderr.decode('utf-8').strip()
    out_lines = str(proc_stdout)
    err_lines = str(proc_stderr)
    return out_lines, err_lines, wall_time


def run_job(job):
    p = mp.current_process()
    pid = p._identity[0] - 1
    path = f"{CWD}/{job.solver.__name__}/{job.benchmark.bid}"
    os.makedirs(path)
    cmd = f'runexec --walltimelimit {TIMEOUT} --memlimit {MEM_PER_JOB*1000}MB '
    cores = pid if JOB_CORES == 1 else f'{pid *  JOB_CORES}-{(pid+1) * JOB_CORES - 1}'
    cmd += f'--cores {cores} '
    cmd += f'--output {path}/output.log '
    cmd += f"{job.solver.cmd} {job.benchmark.vnnlib} {job.benchmark.dnn}"
    
    out,err,wt = run_command(cmd)
    with open(f"{path}/out.txt", 'w') as file: file.write(out)
    with open(f"{path}/err.txt", 'w') as file: file.write(err)
    with open(f"{path}/wt.txt", 'w') as file: file.write(str(wt))

    return True

if __name__ == '__main__':
    net_files =  sorted([os.path.abspath(path) for path in glob.glob('vnncomp2021/benchmarks/acasxu/*.onnx')])
    prop_files = sorted([os.path.abspath(path) for path in glob.glob('vnncomp2021/benchmarks/acasxu/*.vnnlib')])
    benchmarks = [Benchmark(dnn=dnn,vnnlib=vnnlib) for dnn,vnnlib in itertools.product(net_files, prop_files)]
    solvers = [
        Bab,
        ERAN,
        Marabou,
        MIPVerify,
        Neurify,
        nnenum,
        Planet,
        ReluPlex,
        verinet,
        maple_gurobi,
        maple_scip,
        maple_cvc5,
    ]
    jobs = [Job(solver=solver,benchmark=benchmark) for solver, benchmark in itertools.product(solvers,benchmarks)]
    random.shuffle(jobs)
    n_processes = math.floor(TOTAL_CORES/JOB_CORES)
    CWD=f'data/{time.time()}'
    try:
        with mp.Pool(processes=n_processes) as pool:
            for _, res in enumerate(pool.imap_unordered(run_job, jobs, 1)):
                if res:
                    continue
                else:
                    print("Error processing job",flush=True)
    except KeyboardInterrupt:
        pass

