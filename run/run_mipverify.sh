cd "$(dirname "$0")"
. .env.d/openenv.sh
python3 -m dnnv $1 --network N $2 --mipverify --vnnlib
