import os
import sys
import time

import numpy as np
import pandas as pd

import bmlite as bm

def remove_file(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

def mod_sim(sim, sim_params, deg_param_sample, cyc_mode, run_mode):
    if cyc_mode.lower() == "discharge-chargecc":
        if run_mode.lower() == "discharge":
            if "cs0_c" in deg_param_sample:
                sim.ca.x_0 = sim_params["x0_c_dis"] * deg_param_sample["cs0_c"]
            else:
                sim.ca.x_0 = sim_params["x0_c_dis"]
            if "cs0_a" in deg_param_sample:
                sim.an.x_0 = sim_params["x0_a_dis"] * deg_param_sample["cs0_a"]
            else:
                sim.an.x_0 = sim_params["x0_a_dis"]
            C_rate = sim_params["C_dis"]
        elif run_mode.lower() == "chargecc":
            if "cs0_c_chcc" in deg_param_sample:
                sim.ca.x_0 = (
                    sim_params["x0_c_chcc"] * deg_param_sample["cs0_c_chcc"]
                )
            else:
                sim.ca.x_0 = sim_params["x0_c_chcc"]

            if "cs0_a_chcc" in deg_param_sample:
                sim.an.x_0 = (
                    sim_params["x0_a_chcc"] * deg_param_sample["cs0_a_chcc"]
                )
            else:
                sim.an.x_0 = sim_params["x0_a_chcc"]
            C_rate = sim_params["C_chcc"]
    elif cyc_mode.lower() in ["discharge", "chargecc", "rh"]:
        if "cs0_c" in deg_param_sample:
            sim.ca.x_0 = sim_params["x0_c"] * deg_param_sample["cs0_c"]
        else:
            sim.ca.x_0 = sim_params["x0_c"]
        if "cs0_a" in deg_param_sample:
            sim.an.x_0 = sim_params["x0_a"] * deg_param_sample["cs0_a"]
        else:
            sim.an.x_0 = sim_params["x0_a"]
        C_rate = None
    if cyc_mode.lower() in ["discharge", "chargecc"]:
        C_rate = sim_params["C"]
    if "ds_c" in deg_param_sample:
        sim.ca.Ds_deg = deg_param_sample["ds_c"]
    else:
        sim.ca.Ds_deg = 1.0
    if "ds_a" in deg_param_sample:
        sim.an.Ds_deg = deg_param_sample["ds_a"]
    else:
        sim.an.Ds_deg = 1.0
    if "i0_a" in deg_param_sample:
        sim.an.i0_deg = deg_param_sample["i0_a"]
    else:
        sim.an.i0_deg = 1.0
    if "i0_c" in deg_param_sample:
        sim.ca.i0_deg = deg_param_sample["i0_c"]
    else:
        sim.ca.i0_deg = 1.0

    if "eps_cbd_a" in deg_param_sample:
        sim.an.eps_CBD = (
            sim_params["eps_CBD_a"] * deg_param_sample["eps_cbd_a"]
        )
    else:
        sim.an.eps_CBD = sim_params["eps_CBD_a"]
    if "eps_cbd_c" in deg_param_sample:
        sim.ca.eps_CBD = (
            sim_params["eps_CBD_c"] * deg_param_sample["eps_cbd_c"]
        )
    else:
        sim.ca.eps_CBD = sim_params["eps_CBD_c"]
    if "eps_s_c" in deg_param_sample:
        sim.ca.eps_s = (
            sim.ca.eps_CBD
            + sim_params["eps_s_c"] * deg_param_sample["eps_s_c"]
        )
    else:
        sim.ca.eps_s = sim.ca.eps_CBD + sim_params["eps_s_c"]
    if "eps_s_a" in deg_param_sample:
        sim.an.eps_s = (
            sim.an.eps_CBD
            + sim_params["eps_s_a"] * deg_param_sample["eps_s_a"]
        )
    else:
        sim.an.eps_s = sim.an.eps_CBD + sim_params["eps_s_a"]
    if "ce" in deg_param_sample:
        sim.el.Li_0 = sim_params["ce"] * deg_param_sample["ce"]
    else:
        sim.el.Li_0 = sim_params["ce"]
    if "eps_el_a" in deg_param_sample:
        sim.an.eps_el = sim_params["eps_el_a"] * deg_param_sample["eps_el_a"]
    else:
        sim.an.eps_el = sim_params["eps_el_a"]
    if "eps_el_c" in deg_param_sample:
        sim.ca.eps_el = sim_params["eps_el_c"] * deg_param_sample["eps_el_c"]
    else:
        sim.ca.eps_el = sim_params["eps_el_c"]
    if "area" in deg_param_sample:
        sim.bat.area = sim_params["area"] * deg_param_sample["area"]
    else:
        sim.bat.area = sim_params["area"]
    if "l_a" in deg_param_sample:
        sim.an.thick = sim_params["L_a"] * deg_param_sample["l_a"]
    else:
        sim.an.thick = sim_params["L_a"]
    if "l_c" in deg_param_sample:
        sim.ca.thick = sim_params["L_c"] * deg_param_sample["l_c"]
    else:
        sim.ca.thick = sim_params["L_c"]

    if "rs_a" in deg_param_sample:
        sim.an.R_s = sim_params["Rs_a"] * deg_param_sample["rs_a"]
    else:
        sim.an.R_s = sim_params["Rs_a"]

    if "rs_c" in deg_param_sample:
        sim.ca.R_s = sim_params["Rs_c"] * deg_param_sample["rs_c"]
    else:
        sim.ca.R_s = sim_params["Rs_c"]

    if sim_params["model"].lower() == "p2d":
        if "l_s" in deg_param_sample:
            sim.sep.thick = sim_params["L_s"] * deg_param_sample["l_s"]
        else:
            sim.sep.thick = sim_params["L_s"]

        if "eps_el" in deg_param_sample:
            sim.sep.eps_el = sim_params["eps_el"] * deg_param_sample["eps_el"]
        else:
            sim.sep.eps_el = sim_params["eps_el"]

        if "p_l" in deg_param_sample:
            sim.sep.p_liq = sim_params["p_l"] * deg_param_sample["p_l"]
        else:
            sim.sep.p_liq = sim_params["p_l"]

        if "p_s_a" in deg_param_sample:
            sim.an.p_sol = sim_params["p_s_a"] * deg_param_sample["p_s_a"]
        else:
            sim.an.p_sol = sim_params["p_s_a"]

        if "p_l_a" in deg_param_sample:
            sim.an.p_liq = sim_params["p_l_a"] * deg_param_sample["p_l_a"]
        else:
            sim.an.p_liq = sim_params["p_l_a"]

        if "p_s_c" in deg_param_sample:
            sim.ca.p_sol = sim_params["p_s_c"] * deg_param_sample["p_s_c"]
        else:
            sim.ca.p_sol = sim_params["p_s_c"]

        if "p_l_c" in deg_param_sample:
            sim.ca.p_liq = sim_params["p_l_c"] * deg_param_sample["p_l_c"]
        else:
            sim.ca.p_liq = sim_params["p_l_c"]

        if "de" in deg_param_sample:
            sim.el.D_deg = deg_param_sample["de"]
        else:
            sim.el.D_deg = 1.0

        if "t0" in deg_param_sample:
            sim.el.t0_deg = deg_param_sample["t0"]
        else:
            sim.el.t0_deg = 1.0

        if "kappa" in deg_param_sample:
            sim.el.kappa_deg = deg_param_sample["kappa"]
        else:
            sim.el.kappa_deg = 1.0

        if "gamma" in deg_param_sample:
            sim.el.gamma_deg = deg_param_sample["gamma"]
        else:
            sim.el.gamma_deg = 1.0

    return sim, C_rate


def single_run(
    deg_param_sample,
    sim_params,
    count=None,
    nsim=None,
    parallel_env=None,
    run_mode=None,
):

    cyc_mode = sim_params["cyc_mode"]
    params_list = [
        deg_param_sample[key] for key in sim_params["deg_param_names"]
    ]
    param_string = from_param_list_to_str(params_list)

    bat_model = None
    if sim_params["model"] == "SPM":
        bat_model = "SPM"
        sim = bm.SPM.Simulation()
    elif sim_params["model"] == "P2D":
        bat_model = "P2D"
        sim = bm.P2D.Simulation()
    sim, C_rate = mod_sim(
        sim, sim_params, deg_param_sample, cyc_mode, run_mode=run_mode
    )
    # print_an(sim)
    # print_ca(sim)

    sim.pre()
    time_s = time.time()
    if cyc_mode.lower() in ["discharge", "chargecc", "discharge-chargecc"]:
        t_step = (3600 / abs(C_rate), 10000)
        t_step_init = (10 / abs(C_rate), 150)

        expr = bm.Experiment()
        if C_rate > 0:
            # Discharge
            phis_c_min = sim_params["vmin"]
            phis_c_max = np.inf
            lims = ("voltage_V", phis_c_min)
            expr.add_step(
                "current_C",
                C_rate,
                t_step,
                limits=lims,
                atol=1e-10,
                rtol=1e-8,
            )

        elif C_rate < 0:
            # Charge
            phis_c_min = -np.inf
            phis_c_max = sim_params["vmax"]
            lims = ("voltage_V", phis_c_max)
            expr.add_step(
                "current_C",
                C_rate,
                t_step,
                limits=lims,
                atol=1e-10,
                rtol=1e-8,
            )

        rootsol = None
        try:
            rootsol = sim.run(expr)
            assert rootsol.success
        except:
            for fact in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:
                try:
                    print(f"retrying with C = {C_rate*fact:.2f}")
                    expr_init = bm.Experiment()
                    expr_init.add_step(
                        "current_C",
                        C_rate * fact,
                        t_step_init,
                        limits=lims,
                        atol=1e-10,
                        rtol=1e-8,
                    )
                    sol_init = sim.run(expr_init)
                    assert sol_init.success
                    sim._sv0 = sol_init.y[0, :]
                    sim._svdot0 = sol_init.yp[0, :]
                    rootsol = sim.run(expr)
                    assert rootsol.success
                    break
                except:
                    # print(f"sim failed for {deg_param_sample}")
                    pass
            if rootsol is None:
                print(f"All sim failed for {deg_param_sample}")
            else:
                print(f"Restart succeeded for {deg_param_sample}")

    time_e = time.time()

    if parallel_env is None:
        if count is None or nsim is None:
            print(f"Elapsed time = {time_e-time_s:.2f}s")
        else:
            print(f"Elapsed time ({count+1}/{nsim}) = {time_e-time_s:.2f}s")
    else:
        if count is None or nsim is None:
            parallel_env.printAll(f"Elapsed time = {time_e-time_s:.2f}s")
        else:
            parallel_env.printAll(
                f"Elapsed time ({count+1}/{nsim}) = {time_e-time_s:.2f}s"
            )

    return params_list, rootsol



def from_param_list_to_str(params_list, params_name=None):
    param_string = ""
    if params_list is not None:
        if isinstance(params_list[0], str):
            params_list_val = [float(val) for val in params_list]
        else:
            params_list_val = params_list
        if params_name is None:
            for paramval in params_list_val:
                param_string += "_"
                param_string += f"{paramval:g}"
        else:
            for paramval, name in zip(params_list_val, params_name):
                param_string += f"_{name}_"
                param_string += f"{paramval:g}"
    return param_string


def from_param_list_to_dict(params_list, params):
    deg_dict = {}
    for ipar, name in enumerate(params["deg_param_names"]):
        if params_list is not None:
            if isinstance(params_list[0], str):
                deg_dict[name] = float(params_list[ipar])
            else:
                deg_dict[name] = params_list[ipar]
        else:
            deg_dict[name] = params["deg_" + name + "_ref"]
    return deg_dict


def from_param_list_to_str(params_list, params_name=None):
    param_string = ""
    if params_list is not None:
        if isinstance(params_list[0], str):
            params_list_val = [float(val) for val in params_list]
        else:
            params_list_val = params_list
        if params_name is None:
            for paramval in params_list_val:
                param_string += "_"
                param_string += f"{paramval:g}"
        else:
            for paramval, name in zip(params_list_val, params_name):
                param_string += f"_{name}_"
                param_string += f"{paramval:g}"
    return param_string


def from_param_list_to_dict(params_list, params):
    deg_dict = {}
    for ipar, name in enumerate(params["deg_param_names"]):
        if params_list is not None:
            if isinstance(params_list[0], str):
                deg_dict[name] = float(params_list[ipar])
            else:
                deg_dict[name] = params_list[ipar]
        else:
            deg_dict[name] = params["deg_" + name + "_ref"]
    return deg_dict


def read_list_param(
    folder_save=".", param_list_file="parameter_list.txt", parameter_list=[]
):
    param_list_file = os.path.join(folder_save, param_list_file)
    if not os.path.isfile(param_list_file):
        return parameter_list
    with open(param_list_file, "r+") as f:
        lines = f.readlines()
    for line in lines:
        parameter_list.append([float(entry) for entry in line.split()])
    return parameter_list


def read_list_sol(
    folder_save=".", sol_list_file="solution_list.txt", solution_list=[]
):
    sol_list_file = os.path.join(folder_save, sol_list_file)
    if not os.path.isfile(sol_list_file):
        return solution_list
    with open(sol_list_file, "r+") as f:
        lines = f.readlines()
    for line in lines:
        solution_list.append(line[:-1])
    return solution_list


def check_degparamdict(deg_param_dict, sim_params, parallel_env=None):
    for deg_param_name in sim_params["deg_param_names"]:
        try:
            assert (
                deg_param_dict[deg_param_name]
                >= sim_params["deg_" + deg_param_name + "_min"]
            )
            assert (
                deg_param_dict[deg_param_name]
                <= sim_params["deg_" + deg_param_name + "_max"]
            )
        except AssertionError:
            msg = f"ERROR: In dict {deg_param_dict}\n\tParameter {deg_param_name} = {deg_param_dict[deg_param_name]} out of bounds ({sim_params['deg_' + deg_param_name + '_min']}-{sim_params['deg_' + deg_param_name + '_max']})"
            if parallel_env is None:
                sys.exit(msg)
            else:
                parallel_env.printAll(msg)
                parallel_env.comm.Abort()


def check_degparamlist(deg_param_list, sim_params, parallel_env=None):
    for deg_val, deg_param_name in zip(
        deg_param_list, sim_params["deg_param_names"]
    ):
        try:
            assert deg_val >= sim_params["deg_" + deg_param_name + "_min"]
            assert deg_val <= sim_params["deg_" + deg_param_name + "_max"]

        except AssertionError:
            msg = f"ERROR: In list {deg_param_list}\n\tParameter {deg_param_name} = {deg_val} out of bounds ({sim_params['deg_' + deg_param_name + '_min']}-{sim_params['deg_' + deg_param_name + '_max']})"
            if parallel_env is None:
                sys.exit(msg)
            else:
                parallel_env.printAll(msg)
                parallel_env.comm.Abort()


def from_degparamlist_to_degparamdict(
    deg_param_list, sim_params, parallel_env=None
):
    check_degparamlist(deg_param_list, sim_params, parallel_env)
    deg_param_dict = {}
    for deg_param_val, deg_param_name in zip(
        deg_param_list, sim_params["deg_param_names"]
    ):
        deg_param_dict[deg_param_name] = deg_param_val
    check_degparamdict(deg_param_dict, sim_params, parallel_env)
    return deg_param_dict


def from_degparamdict_to_degparamlist(
    deg_param_dict, sim_params, parallel_env=None
):
    check_degparamdict(deg_param_dict, sim_params, parallel_env)
    deg_param_list = []
    for deg_param_name in sim_params["deg_param_names"]:
        deg_param_list.append(deg_param_dict[deg_param_name])
    check_degparamlist(deg_param_list, sim_params, parallel_env)
    return deg_param_list


def multi_run_ser(
    sim_params,
    param_list_file="parameter_list.txt",
    sol_list_file="solution_list.txt",
    bad_par_file="bad_par.txt",
    bad_sol_file="bad_sol.txt",
    save_separate_sols=False,
    save_combined_sols=True,
    folder_save=".",
    only_phi_CC=True,
    n_points_reduce=512,
):

    cyc_mode = sim_params["cyc_mode"]
    os.makedirs(folder_save, exist_ok=True)
    remove_file(os.path.join(folder_save, bad_par_file))
    remove_file(os.path.join(folder_save, bad_sol_file))
    remove_file(os.path.join(folder_save, "sols.pkl"))

    deg_parameter_list = read_list_param(
        folder_save=folder_save, param_list_file=param_list_file
    )
    solution_list = read_list_sol(
        folder_save=folder_save, sol_list_file=sol_list_file
    )

    nsim = len(solution_list)

    for count, (deg_param_entry, solution_entry) in enumerate(
        zip(deg_parameter_list, solution_list)
    ):
        if cyc_mode.lower() in ["discharge", "chargecc", "rh"]:
            params_list, root_sol = single_run(
                sim_params=sim_params,
                deg_param_sample=from_degparamlist_to_degparamdict(
                    deg_param_entry, sim_params, parallel_env=None
                ),
                count=count,
                nsim=nsim,
            )
        elif cyc_mode.lower() == "discharge-chargecc":
            for run_mode in ["discharge", "chargecc"]:
                params_list_i, root_sol_i = single_run(
                    sim_params=sim_params,
                    deg_param_sample=from_degparamlist_to_degparamdict(
                        deg_param_entry, sim_params, parallel_env=None
                    ),
                    run_mode=run_mode,
                    count=count,
                    nsim=nsim,
                )




def multi_run(
    sim_params,
    param_list_file="parameter_list.txt",
    sol_list_file="solution_list.txt",
    bad_par_file="bad_par.txt",
    bad_sol_file="bad_sol.txt",
    save_separate_sols=False,
    save_combined_sols=True,
    folder_save=".",
    parallel_env=None,
    only_phi_CC=True,
    n_points_reduce=512,
):

    cyc_mode = sim_params["cyc_mode"]

    multi_run_ser(
        sim_params=sim_params,
        param_list_file=param_list_file,
        sol_list_file=sol_list_file,
        bad_par_file=bad_par_file,
        bad_sol_file=bad_sol_file,
        folder_save=folder_save,
    )
