# Evidence Images

All generated evidence images for the thesis, audit, and benchmark must be stored in:

```text
docs/bukti_highlight/
```

## Rules

1. Do not leave final evidence images in the repository root, `scratch/`, or `/tmp`.
2. Use descriptive filenames:
   - `eval_5_skenario.png`
   - `tabel_5_skenario_param.png`
   - `tabel_5_skenario_hasil.png`
   - `komparasi_waktu_full.png`
3. Every image must have a source note: script/command, data artifact, and date.
4. If an image supports a Markdown section, reference it with a relative path:
   ```markdown
   ![Komparasi waktu](../docs/bukti_highlight/komparasi_waktu_full.png)
   ```
5. Commit the image together with the Markdown that cites it.
6. Do not overwrite an existing evidence image unless the corresponding document is updated in the same commit.
7. Temporary benchmark logs and raw checkpoints remain outside `docs/bukti_highlight/` and must not be committed unless explicitly requested.

## Rationale

`docs/bukti_highlight/` is the single source of truth for visual evidence. Keeping images there prevents duplicate files, broken references, and unverifiable screenshots.
