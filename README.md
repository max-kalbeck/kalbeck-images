# kalbeck-images

Throw-away code repo to process kalbeck images.

## issues

### Seiten herausgeschnitten?

* kalbeck_2__0041_a.tif -> 14. März
* kalbeck_2__0041_b.tif -> 17. März

### doppelt gescannt

* kalbeck_2__0063_a.tif sameAs kalbeck_2__0064_a.tif
* kalbeck_2__0063_b.tif sameAs kalbeck_2__0064_b.tif

## compress

copied from <https://github.com/acdh-oeaw/arche-curationTools/blob/master/tif_lzw.sh>

```bash
./src/compress_tiffs.sh orig-files
```

## split

written by <https://chatgpt.com/>

```bash
uv run src/split_pages.py orig-files/  --output split/ --threshold 6600 --margin 80
```
