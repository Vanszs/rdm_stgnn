# ML CORRECTNESS AUDIT — `core/`

Repo: `/home/vanszs/Documents/Skripsi_Bevan`
Tanggal: 2026-10-02
Metode: 10 subagent read-only (model DeepSeek) + verifikasi ulang manual oleh auditor utama untuk setiap temuan HIGH/MED. Setiap temuan di bawah sudah saya jalankan sendiri untuk membuktikannya — bukan hasil lapor-diri.

---

## RINGKASAN

| | Jumlah |
|---|---|
| Temuan VALID + DIPERBAIKI | 5 |
| Temuan VALID, TIDAK diperbaiki (butuh retrain / di luar batas) | 6 |
| Dugaan subagent yang **DITOLAK** setelah verifikasi | 3 |
| Diperiksa bersih (CHECKED-CLEAN) | 12 |

Tidak ada bukti checkpoint terlatih pada data bocor. Test core 20/20 lulus setelah semua perbaikan. E2E inferensi pada checkpoint nyata tetap sehat.

---

## 1. TEMUAN VALID YANG SUDAH DIPERBAIKI

### 1.1 `probabilistic_metrics.py:306` — reliability membuang prediksi `prob == 1.0` (HIGH)
```python
mask = (pred_probs >= bin_edges[i]) & (pred_probs < bin_edges[i + 1])   # [a,b)
```
Bin half-open → nilai tepat `1.0` tidak masuk bin mana pun dan **hilang diam-diam**. Ini kasus umum: prakiraan hujan lebat yang sangat percaya diri menghasilkan probabilitas eksedans = 1.0.

**Dibuktikan:** 5 titik, 3 dengan prob 1.0 → `bin_counts` menjumlah hanya **2 dari 5**. Diagram reliabilitas jadi overstate.
**Praktik benar** (Wilks 2019 §8.4.4): bin terakhir harus tertutup di kanan.
**Perbaikan:** bin terakhir memakai `<=`. Setelah fix: jumlah 5 dari 5.

### 1.2 `probabilistic_metrics.py:143-150,160-168` — observasi NaN diubah jadi "tidak hujan" (MED)
`NaN > threshold` bernilai `False`, sehingga observasi hilang dihitung sebagai **non-event** dan mengarang pasangan verifikasi.
**Dibuktikan:** `obs=[20,NaN,0]` → `brier=0.333`, `far=0.5` (seolah ada false alarm padahal tidak).
**Perbaikan:** loop Brier + `_contingency` melewati timestep NaN; Brier mengembalikan `nan` bila tak ada data valid. Konsisten dengan metrik deterministik yang sudah mem-`nan`-mask (`compute_rmse`/`compute_mae`).
**Setelah fix:** `brier` dengan NaN = 0.0 (hanya t valid dihitung), rel reliability membuang NaN.

### 1.3 Gap `wet_probability_threshold` — tiga jalur berbeda nilai (MED)
Perbaikan sebelumnya hanya mengubah **satu** tempat; verifikasi menemukan sisa:
| lokasi | sebelum | sekarang |
|---|---|---|
| `inference.py:116` | 0.6 ✅ (sudah) | 0.6 |
| `inference.py:297` | **0.5** | 0.6 |
| `run_eval_final.py:168` | **0.5** | 0.6 |
| `eval_rain_robust.py:201` | **0.5** | 0.6 |
PDF §3.8.4 menyebut ambang 0,6. Kini konsisten 0.6 di semua jalur.

---

## 2. TEMUAN VALID YANG **TIDAK** DIPERBAIKI (ditandai, bukan diabaikan)

### 2.1 `train.py:187-188` — bobot loss tidak spesifik-kanal (MED)
```python
weights[target_reference.abs() > 1.0] = 5.0
weights[target_reference.abs() > 3.0] = 10.0
```
`target_reference` adalah tensor z-score `[B,3]` (precip/wind/RH). Konsekuensi terukur pada data train MAIN:
- ambang `|z|>1` setara precip ≥ 0.73 mm/j, wind ≥ 5.88 m/s, RH ≥ **95.8 %** → "bobot ekstrem" sebenarnya menyala di 11.2 %/30.8 %/29.5 %.
- ambang `|z|>3` untuk RH setara ≥ **123 %** → **tidak mungkin tercapai** (maks 100), jadi cabang 10× untuk RH mati.
- `docs/KNOWLEDGE.md` menyebutnya "weight event hujan ekstrem" — tidak akurat; ia menaikkan bobot angin & kelembapan juga.

**Tidak diperbaiki:** mengubah bobot loss berarti mengubah perilaku model terlatih → butuh retrain. Catat sebagai keterbatasan/deskripsi yang perlu dikoreksi di naskah.

### 2.2 `train.py:654-656` — validation loss adalah variabel acak Monte-Carlo (MED)
```python
noise = torch.randn_like(targets)
timesteps = torch.randint(0, DIFFUSION_TRAIN_TIMESTEPS, ...)
```
Diuji pada batch nyata, 6 undian: `[3.20, 3.82, 3.93, 2.52, 4.27, 4.24]`, std **0.62**. Early stopping / LR-plateau / pemilihan checkpoint terbaik semuanya berpijak pada angka acak ini (`early_stop_min_delta=0.0`).
**Praktik benar:** kunci satu pasangan `(noise, t)` per set validasi per epoch (generator ber-seed), agar perbandingan antar-epoch apple-to-apple.
**Tidak diperbaiki:** butuh retrain. `best_epoch` di checkpoint adalah argmax atas noise — perlu dicatat di naskah.

### 2.3 `train.py:699` — val non-finite bisa menyimpan checkpoint sampah (LOW)
Jika semua batch val non-finite (di-`continue`), `avg_val = 0.0` → memenuhi `improved` → tersimpan sebagai `best_val_loss=0.0`. Laten; tidak terjadi di checkpoint sekarang.

### 2.4 Reproducibility tidak lengkap (MED)
- `diffusion.py:258-269`: `use_amp = str(self.device) != 'cpu'` + `autocast('cuda')` → **GPU fp16, CPU fp32**. Seed sama + checkpoint sama, `--device` berbeda → angka ensemble berbeda. Meta mingguan mencatat `"device": "cuda"`, jadi re-run di CPU tidak bisa mereproduksi metrik yang dikirim.
- `train.py:332-333`: `allow_tf32=True` → mantissa turun, beda antar-generasi GPU.
- Repo tidak pernah memakai `torch.use_deterministic_algorithms` / `CUBLAS_WORKSPACE_CONFIG` (grep nol).
- `run_eval_final.py:390-396`: seed sekali di luar loop; angka skenario bergantung urutan & `num_ensemble` skenario sebelumnya (tidak ada reseed per skenario).
- **Tidak diperbaiki:** ini mengubah angka → di luar batas "tanpa retrain/ubah perilaku". Dicatat sebagai keterbatasan reprodusibilitas.

### 2.5 Jalur keluaran eval bisa menimpa / salah lokasi (MED)
`run_eval_final.py` menulis `"result_test/..."` relatif CWD; `core/result_test` tidak ada, sedangkan artefak ter-commit ada di `core/results/result_test/`. Re-run dari `core/` tidak mereproduksi lokasi ter-commit → metrik committed bisa basi tanpa jejak. `train.py:799` menimpa satu-satunya checkpoint tanpa run-id. **Tidak diperbaiki** (butuh keputusan struktur output).

### 2.6 Mismatch dimensi diffusion MLP vs PDF (HIGH, intrinsik)
Checkpoint & kode memakai `hidden_dim=128` (Time MLP `Linear(64,128)`, Down2 `Linear(64,128)`, Mid `Linear(128,128)`, Up `Linear(256,64)`). Sebagian tabel PDF (p079) terbaca 64-wide.
**Tidak diperbaiki:** mengubah lebar layer = arsitektur baru = retrain. Sudah dibahas di `docs/ALIGNMENT_PDF_CORE.md`; naskah perlu dikoreksi.

### 2.7 Checkpoint dilatih pra-perubahan split (MED, klaim vs artefak)
Bobot dilatih dengan batas split lama (613.480); sekarang kode memakai 613.560 (PDF). Selisih 80 baris → dampak numerik ≤1e-4 relatif, tapi **model belum pernah dilatih ulang pasca-perubahan**. Ini mismatch klaim-vs-artefak, bukan kebocoran. Ditandai; tidak retrain.

---

## 3. DUGAAN SUBAGENT YANG **DITOLAK** SETELAH VERIFIKASI

| Dugaan | Verdict | Bukti |
|---|---|---|
| `diffusion.py:159` — wet head dilatih dengan input berbeda dari saat dipakai (agent klaim HIGH) | **DITOLAK** (agent sendiri menurunkannya) | Diuji langsung: `forward(return_wet_logit=True)` vs `compute_wet_logit` → logit **identik** (0.0967065840959 keduanya). Divergensi struktural ada (satu lewat `emb` yang menyertakan `t_emb`), tapi `time_mlp` di-`sum` lalu diambil `wet_head(cond_emb)` pada kedua jalur sehingga numerik sama. Bukan bug perilaku. |
| Model pembanding tersisa (persistence/mlp) masih "aktif" | **DITOLAK** | Artefak lama masih ada di `core/results/result_test/` sebagai **hasil historis**, bukan kode. Tidak ada kode rival. |
| `eval_rain_robust.py` pemilihan minggu = data leakage | **SEBAGIAN BENAR, bukan leakage model** | Minggu dipilih dari label test (`eval_rain_robust.py:102-116`) → bias *protokol pelaporan*, bukan train/test leakage. Tidak diperbaiki; dicatat. |

---

## 4. CHECKED-CLEAN (diverifikasi, bukan diasumsikan)

**Leakage (semua bersih):**
- Statistik normalisasi **hanya** dari train: `train.py:354` + `:85,:107`. Nol `val_df`/`test_df` menyentuh `.mean()/.std()`.
- FAISS DB **hanya** dari train: `train.py:454-457` (`train_features_norm[:-1]`, `train_targets_norm[1:]`); rebuild `inference.py:199,216-219`.
- `precipitation_lag1` dibuat **setelah** sort kronologis: `ingest.py:216-219` (sort lalu `groupby.shift(1).fillna(0.0)`). Direproduksi: `np.allclose` ke kolom tersimpan = True, semua diff = 3600s.
- Split tidak tumpang tindih: runtime check → 0 timestamp overlap; 122712/26304/35064 ts = 613560/131520/175320 baris.
- Tidak ada test yang dipakai untuk memilih apa pun; val dipakai untuk early-stop/LR/kalibrasi threshold (praktik standar).

**Metrik:**
- **CRPS = bentuk fair/unbiased Hersbach** (`:100-106`). Dibandingkan numerik dengan referensi pairwise pada n∈{2,3,5,10,50} → identik 6 desimal (n=5: 0.666274 = fair, bukan biased 0.763730). n=1 → MAE (benar).
- **Brier** = mean((p−o)²), p = fraksi ensemble > threshold → benar (Brier 1950).
- **POD/FAR/CSI** tabel kontingensi hit/miss/FA saling eksklusif & lengkap; kasus tak terdefinisi → NaN, bukan 0.
- **Pearson** dijaga terhadap varians nol (`:50` mask<3, `:53` guard).

**Training:**
- Gradien mengalir ke **STGNN dan denoiser**: `train.py:508` `list(st_gnn.parameters()) + list(diff_model.parameters())`, satu AdamW (`:509`). Backward nyata: **0/51 parameter dengan `grad is None`**; `pos_embedding` juga menerima gradien.
- Mode train/eval benar; dropout hanya di `TemporalAttention`/GAT dan mati saat eval.
- `loss = noise_loss + wet_loss_weight*wet_loss` (`:589`) dengan 0.7 — cocok checkpoint.
- Early stopping murni dari val; tidak ada test loader di `train.py`.
- `ReduceLROnPlateau(mode="min")` di-step sekali per epoch dengan `avg_val`.

**Inference:**
- Denormalisasi: z-score inverse → `expm1` **hanya** precipitation → clamp fisik (0–60 mm, wind ≥0, RH 0–100) di ruang mm/j.
- Rain gate memakai threshold dari checkpoint + guard anti-degenerat (skip bila semua kering).
- `eval()` sebelum sampling; ensemble independen (`torch.randn` per call); median untuk prediksi titik.

**Preprocessing:** log1p hanya precipitation; epsilon konsisten di jalur forward; fallback fitur degenerat benar; tak ada `fillna` yang menyembunyikan data selain lag-1 awal (didokumentasikan).

---

## 5. VERIFIKASI AKHIR

- Test core: **20/20 lulus** setelah semua perbaikan.
- E2E pada checkpoint nyata: kunci `precipitation`/`wind_speed`/`relative_humidity`, `raw (8,3)` finite.
- Ambang wet kini konsisten **0.6** di keempat jalur.
- Bukti numerik semua perbaikan metrik direproduksi sebelum & sesudah.

## 6. UTANG TEKNIS YANG TERCATAT

1. Bobot loss tidak spesifik-kanal (§2.1) — deskripsi di naskah perlu dikoreksi atau loss diubah + retrain.
2. Validation loss non-deterministik (§2.2) — pertimbangkan fixed val draw saat retrain berikutnya.
3. Reprodusibilitas CPU vs CUDA berbeda (§2.4) — catat `amp`/device di metadata, atau pin presisi.
4. Test yang hilang & bernilai tertinggi: **tidak ada test yang menyentuh `src.train`**, sehingga batas anti-leakage (`_build_precomputed_retrieval` `strict_past`, `temporal_split`) tak terjaga. Usulan: `test_strict_past_retrieval_never_returns_future`.
