./build/X86/gem5.opt configs/example/se_dse.py \
-c "./MachSuit1/aes/aes/generate;./MachSuite2/aes/aes/generate;./MachSuite3/sort/merge/generate;./MachSuite4/sort/radix/generate" \
--ruby \
--num-cpus=${NUM_CPUS} --cpu-type=DerivO3CPU \
--caches --l2cache --num-l2caches=${NUM_CPUS} \
--network=garnet --topology=Mesh_XY --mesh-rows=2 \
--multicache --multi_l1cache "${L1_SIZE}" \
--multicache_l2 --multi_l2cache "${L2_SIZE}"


# --multicache --multi_l1cache "64kB;128kB;256kB;512kB" \
# --multicache_l2 --multi_l2cache "256kB;512kB;1MB;2MB"
#-c "./tests/test-progs/hello/bin/x86/linux/hello;./tests/test-progs/hello/bin/x86/linux/hello;./tests/test-progs/hello/bin/x86/linux/hello;./tests/test-progs/hello/bin/x86/linux/hello" \
# -c "./MachSuite-master/fft/strided/generate;./MachSuite-master/gemm/blocked/generate;./tests/test-progs/hello/bin/x86/linux/hello;./MachSuite-master/sort/merge/generate" \