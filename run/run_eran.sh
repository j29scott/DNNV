file_dir="$(dirname "$0")" 
cd $file_dir
cd ..
. .env.d/openenv.sh
cd $file_dirpython3 -m dnnv $1 --network N $2 --eran --vnnlib
