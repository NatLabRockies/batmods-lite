import argparse
import os
import time

import util.parallel as parallel_env
from util.sim_setup import make_params
from util.sol_gen import multi_run

PARAMPRED_EXP = "default_exp" 

parser = argparse.ArgumentParser(description="dataset generator")
parser.add_argument(
    "-i",
    "--index",
    type=int,
    metavar="",
    required=True,
)
args, unknown = parser.parse_known_args()

assert args.index <= 4
assert args.index >= 1

sim_params = make_params(os.path.join(PARAMPRED_EXP, "p2d_discharge_highdim.yaml"), parallel_env=parallel_env)
time_s = time.time()
multi_run(
    sim_params=sim_params,
    parallel_env=parallel_env,
    folder_save=f"data_p2d_discharge_highdim{args.index}",
    n_points_reduce=256,
)
time_e = time.time()
time.sleep(2)
parallel_env.printRoot(f"Total Elapsed {time_e-time_s:.2f}s")
