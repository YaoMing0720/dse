./build/ARM/gem5.opt \
configs/example/arm/ruby_fs.py \
--kernel=fs_image/binaries/vmlinux.arm64 \
--disk=fs_image/disks/ubuntu-18.04-arm64-docker.img \
--chi-config=./configs/example/noc_config/2x2.py \
--topology=Ring \
--num-cpus=4 \
--cpu=o3 \
--num-dirs=2 \
--num-l3caches=2 \
--network=garnet \
--router-latency=1