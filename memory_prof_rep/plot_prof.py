from prettyPlot.plotting import *
import os

def read_mprof_dat(filepath):
    memory = []
    timestamps = []
    cmdline = None

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("CMDLINE"):
                cmdline = line[len("CMDLINE"):].strip()
            elif line.startswith("MEM"):
                parts = line.split()
                if len(parts) == 3:
                    mem = float(parts[1])
                    ts = float(parts[2])
                    memory.append(mem)
                    timestamps.append(ts)

    return {
        'command': cmdline,
        'timestamps': np.array(timestamps)-timestamps[0],
        'memory_MB': np.array(memory)
    }

def make_filepaths(folder="dat_out"):
    filepaths = {}
    for i in range(4):
        filepaths[i] = []
        for rep in range(5):
            filepaths[i].append(os.path.join(folder,f"run{i+1}_{rep+1}.dat")) 
    return filepaths

def plotall(filepaths:dict, color_list=['k', 'r', 'b', 'g']):
    fig = plt.figure()
    for i in range(4):
        for ifile, file in enumerate(filepaths[i]):
            res = read_mprof_dat(file)
            if ifile==0:
               label = f"run {i+1}"
            else:
               label = None
            plt.plot(res["timestamps"], res["memory_MB"], color=color_list[i], linewidth=2, label=label)
    pretty_labels("time [s]", "memory [MB]", 16, fontname="Times", grid=True)
    pretty_legend(fontname="Times")
    plt.show()



if __name__ == "__main__":
    filepaths = make_filepaths(folder="dat_out")
    plotall(filepaths)






