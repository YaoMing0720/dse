./build/ARM/gem5.opt configs/example/se.py \
-c "/home/yaom/MachSuite/aes/aes/generate;/home/yaom/MachSuite/fft/strided/generate;/home/yaom/MachSuite/fft/transpose/generate;/home/yaom/MachSuite/md/knn/generate;/home/yaom/MachSuite/md/grid/generate;/home/yaom/MachSuite/sort/merge/generate;/home/yaom/MachSuite/sort/radix/generate;/home/yaom/MachSuite/nw/nw/generate;/home/yaom/testbench/a;/home/yaom/testbench/b;/home/yaom/testbench/c;/home/yaom/testbench/package;" \
--ruby \
--num-cpus=12 --cpu-type=DerivO3CPU \
--network=garnet \
--topology=CustomMesh \
--chi-config=/home/yaom/gem5-21.1.0.2/configs/example/noc_config/4x4.py  \
--num-l3caches=2 --l3_size=${LLC_SIZE} \
--num-dirs=2 \
--location="${LOCATION}" \
--router-latency=1
# -c "/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;/home/yaom/testbench/a;" \
