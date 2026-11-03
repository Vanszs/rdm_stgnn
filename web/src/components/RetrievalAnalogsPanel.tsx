import React, { useMemo } from 'react';
import { HistoricalAnalog } from '../types';
import { Database, ArrowUpRight, CloudRain, Wind, Thermometer, Droplets } from 'lucide-react';

interface RetrievalAnalogsPanelProps { analogs?: HistoricalAnalog[]; onSelectAnalog?: (analog: HistoricalAnalog) => void; onOpenAll?: () => void; }

const whenLabel = (sample: HistoricalAnalog) => {
  if (!sample.patternAtWib) return sample.datetime;
  const [patternDate, patternTime] = sample.patternAtWib.split(', ');
  const [outcomeDate, outcomeTime] = sample.datetime.split(', ');
  const outcome = patternDate === outcomeDate ? outcomeTime ?? sample.datetime : sample.datetime;
  return `Pola ${patternTime ?? sample.patternAtWib} → hasil ${outcome}`;
};

export const RetrievalAnalogsPanel: React.FC<RetrievalAnalogsPanelProps> = ({ analogs, onSelectAnalog, onOpenAll }) => {
  const samples = useMemo(() => (analogs ?? []).slice(0, 3), [analogs]);
  if (samples.length === 0) return <div className="w-full"><div className="flex items-center gap-2"><Database className="w-4 h-4 text-[#00f0ff]" /><p className="text-[10px] font-mono-data text-[#849495]">Belum ada pola serupa.</p></div></div>;
  return <div className="w-full"><div className="flex flex-wrap items-center justify-between gap-2 mb-3"><div className="flex items-center gap-2"><Database className="w-4 h-4 text-[#00f0ff]" /><div><h3 className="font-mono-data text-xs font-bold text-[#dae2fd] uppercase tracking-wider">POLA SERUPA DARI MASA LALU (3 TERDEKAT)</h3><p className="text-[10px] font-mono-data text-[#849495] mt-0.5">Diambil dari data latih di titik puncak (sebelum 2019).</p></div></div>{onOpenAll && <button onClick={onOpenAll} className="text-[11px] font-mono-data text-[#00f0ff] hover:underline">Lihat semua <ArrowUpRight className="w-3 h-3 inline" /></button>}</div><div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">{samples.map((sample, index) => <button key={sample.id} onClick={() => onSelectAnalog?.(sample)} className="text-left bg-[#131b2e]/80 rounded-xl border border-white/10 p-3 hover:border-[#00f0ff]/60"><div className="flex justify-between mb-2"><span className="font-mono-data text-[10px] text-[#00f0ff]">#{sample.rank ?? index + 1} POLA</span><span className="font-mono-data text-[9px] text-[#dae2fd]">{whenLabel(sample)}</span></div><span className="text-[10px] text-[#b9cacb] font-medium">{sample.patternType}</span><div className="my-2.5 text-xs font-mono-data text-[#00f0ff]">Jarak: {Number(sample.distanceL2 ?? 0).toFixed(2)} <span className="text-[9px] text-[#849495]">(makin kecil makin mirip)</span></div><div className="grid grid-cols-2 gap-1.5 text-[10px] text-[#b9cacb]"><span><CloudRain className="w-3 h-3 inline text-[#1f6056]" /> Hujan {Number(sample.rainRateMmH).toFixed(1)} mm/jam</span><span><Wind className="w-3 h-3 inline text-[#fed639]" /> Angin {Number(sample.peakWindKmh).toFixed(1)} km/jam</span><span><Thermometer className="w-3 h-3 inline text-rose-400" /> Suhu {Number(sample.tempCelsius).toFixed(1)}°C</span><span><Droplets className="w-3 h-3 inline text-[#7df4ff]" /> Lembap {Number(sample.humidityPercent).toFixed(1)}%</span></div></button>)}</div></div>;
};
