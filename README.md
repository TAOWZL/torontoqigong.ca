# torontoqigong.ca

Static site for Toronto Qigong (Wuji Xuan Life Wellness Ltd.), 255 Broadview Ave.

- `src/pages.py`: page copy. `src/build.py`: template, schema, settings (NAP, noindex flag).
- `docs/`: the built site. GitHub Pages serves this folder.

Rebuild after any edit: `python3 src/build.py`, then commit `docs/`.

Launch: set `noindex` to `False` in `src/build.py`, rebuild, push. Then connect Search Console and submit at search.brave.com.
