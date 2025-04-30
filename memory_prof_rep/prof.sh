rm -r dat_out
mkdir -p dat_out

mprof run --output dat_out/run1_1.dat main_p2d.py -i 1
mprof run --output dat_out/run2_1.dat main_p2d.py -i 2
mprof run --output dat_out/run3_1.dat main_p2d.py -i 3
mprof run --output dat_out/run4_1.dat main_p2d.py -i 4

mprof run --output dat_out/run1_2.dat main_p2d.py -i 1
mprof run --output dat_out/run2_2.dat main_p2d.py -i 2
mprof run --output dat_out/run3_2.dat main_p2d.py -i 3
mprof run --output dat_out/run4_2.dat main_p2d.py -i 4

mprof run --output dat_out/run1_3.dat main_p2d.py -i 1
mprof run --output dat_out/run2_3.dat main_p2d.py -i 2
mprof run --output dat_out/run3_3.dat main_p2d.py -i 3
mprof run --output dat_out/run4_3.dat main_p2d.py -i 4

mprof run --output dat_out/run1_4.dat main_p2d.py -i 1
mprof run --output dat_out/run2_4.dat main_p2d.py -i 2
mprof run --output dat_out/run3_4.dat main_p2d.py -i 3
mprof run --output dat_out/run4_4.dat main_p2d.py -i 4

mprof run --output dat_out/run1_5.dat main_p2d.py -i 1
mprof run --output dat_out/run2_5.dat main_p2d.py -i 2
mprof run --output dat_out/run3_5.dat main_p2d.py -i 3
mprof run --output dat_out/run4_5.dat main_p2d.py -i 4
