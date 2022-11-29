挂载镜像命令：
sudo mount -o loop,offset=65536 /home/yaom/gem5-21.1.0.2/fs_image/disks/ubuntu-18.04-arm64-docker.img dirfs/

卸载镜像：
sudo umount dirfs

拷贝可执行文件到挂载的镜像下：
sudo cp gem5-21.1.0.2/testbench/hello dirfs/root/

交叉编译命令：
arm-linux-gcc -o testbench/hello testbench/hello.c -static