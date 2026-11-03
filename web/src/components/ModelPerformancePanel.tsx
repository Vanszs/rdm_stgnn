import React from 'react';
import { ModelMetrics } from '../types';

interface ModelPerformancePanelProps { metrics: ModelMetrics | null; }
const pct = (value: number | null | undefined) => (value === null || value === undefined ? '—' : `${(value * 100).toFixed(0)}%`);
const num = (value: number | null | undefined, digits = 2) => (value === null || value === undefined ? '—' : value.toFixed(digits));
const metric = (label: string, value: string, hint: string) => <div className="bg-[#0b1120] rounded-lg p-2 border border-white/10" title={hint}><div className="font-mono-data text-[9px] text-slate-400 font-semibold truncate">{label}</div><div className="font-mono-data text-base text-[#00f0ff] font-extrabold mt-0.5">{value}</div></div>;

export const ModelPerformancePanel: React.FC<ModelPerformancePanelProps> = ({ metrics }) => <div role="region" aria-label="Hasil uji model" className="w-full flex flex-col gap-3">
  <p className="font-mono-data text-[10px] text-[#849495]">Diuji pada data historis 2022–2025 di titik puncak • ambang hujan 2 mm/jam</p>
  {metrics === null && <p className="text-[10px] font-mono-data text-[#78520f]">Metrik tidak tersedia — server tidak terhubung.</p>}
  <div className="grid grid-cols-3 gap-2">
    {metric('RMSE (mm/jam)', num(metrics?.rmse), 'Rata-rata besar kesalahan. Makin kecil makin baik.')}
    {metric('CSI', pct(metrics?.csi), 'Persentase prakiraan hujan yang benar. Makin besar makin baik.')}
    {metric('FAR', pct(metrics?.far), 'Persentase peringatan hujan yang ternyata salah. Makin kecil makin baik.')}
  </div>
  <details className="text-[10px] font-mono-data text-[#b9cacb]">
    <summary className="cursor-pointer text-[#00f0ff]">Lihat detail angka</summary>
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 mt-2">
      {metric('MAE (mm/jam)', num(metrics?.mae), 'Rata-rata selisih absolut.')}
      {metric('CRPS', num(metrics?.crps, 3), 'Akurasi sebaran probabilitas. Makin kecil makin baik.')}
      {metric('Brier', num(metrics?.brierScore, 3), 'Akurasi probabilitas hujan. Makin kecil makin baik.')}
      {metric('Korelasi', num(metrics?.corr), 'Kesesuaian pola naik-turun. Makin dekat 1 makin baik.')}
      {metric('POD', pct(metrics?.pod), 'Persentase hujan nyata yang berhasil dideteksi.')}
    </div>
    <p className="mt-2 leading-relaxed">RMSE, MAE, CRPS, dan Brier: makin kecil makin baik. Korelasi, CSI, dan POD: makin besar makin baik. FAR: makin kecil makin baik.</p>
  </details>
</div>;
