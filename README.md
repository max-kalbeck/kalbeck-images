# kalbeck-images

Throw-away code repo to process kalbeck images.

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
