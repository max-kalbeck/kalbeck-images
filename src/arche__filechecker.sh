#/bin/bash
echo "run filechecker"
rm -rf ${PWD}/kalbeck_2 && mkdir ${PWD}/kalbeck_2
docker run \
  --rm \
  --network="host" \
  -v ${PWD}/kalbeck_2:/reports \
  -v /home/csae8092/Schreibtisch/R_kalbeck_27373/kalbeck/kalbeck_2/splitted:/data \
  --entrypoint arche-filechecker \
  acdhch/arche-ingest \
  --overwrite --skipWarnings /data /reports
