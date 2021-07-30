file_dir="$(dirname "$0")" 
cd $file_dir
cd ..
. .env.d/openenv.sh
cd $file_dir
python3 -m dnnv $1 --network N $2 --reluplex --vnnlib
