import React from 'react';
import { CloudRain, Wind, Droplets } from 'lucide-react';
import { NowcastDistribution, NowcastVariableSet } from '../types';

interface ForecastChartProps {
  nowcast: NowcastVariableSet;
  windowRangeWib?: string;
}

/**
 * One-step forecast panel: 50 ensemble members for 3 variables at a single horizon.
 * Rendered as a percentile band + observed marker, not a multi-step line.
 */
const ForecastChartComponent: React.FC<ForecastChartProps> = ({ nowcast, windowRangeWib }) => {
  const rows = [
    { key: 'precip', label: 'Curah hujan', icon: CloudRain, accent: '#1f6056', data: nowcast.precipitation },
    { key: 'wind', label: 'Kecepatan angin', icon: Wind, accent: '#b77817', data: nowcast.wind_speed },
    { key: 'humidity', label: 'Kelembapan', icon: Droplets, accent: '#2c7569', data: nowcast.relative_humidity },
  ];
  const validAt = nowcast.precipitation.validAtWib;

  return (
    <div className="w-full h-full flex flex-col gap-2">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-2 flex-wrap">
          <h3 className="font-mono-data text-xs font-bold text-[#b9cacb] uppercase tracking-wider">
            Prakiraan 1 jam berikutnya (30 kemungkinan)
          </h3>
          <span className="text-[10px] font-mono-data text-[#1f6056] bg-[#1f6056]/10 px-2 py-0.5 rounded border border-[#1f6056]/30">
            Target: {validAt}
          </span>
          {windowRangeWib && (
            <span className="text-[10px] font-mono-data text-amber-700 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/30">
              Data: 6 pembacaan jam terakhir ({windowRangeWib})
            </span>
          )}
        </div>
      </div>

      <div className="flex flex-col gap-2 flex-1 justify-center">
        {rows.map((row) => (
          <NowcastRow key={row.key} {...row} />
        ))}
      </div>

      <div className="flex flex-wrap items-center justify-between gap-x-4 gap-y-1.5 text-[10px] font-mono-data text-[#5f685e] pt-2 border-t border-[#d8d4c8]/50">
        <div className="flex items-center gap-3.5 flex-wrap">
          <span className="flex items-center gap-1.5 whitespace-nowrap text-[#5f685e]" title="P10–P90: 80% kemungkinan hasil model ada di rentang ini">
            <span className="w-4 h-1.5 rounded-full bg-[#5f685e]/25 border border-[#5f685e]/50 inline-block" />
            Rentang 80%
          </span>
          <span className="flex items-center gap-1.5 whitespace-nowrap text-[#5f685e]" title="P25–P75: 50% kemungkinan hasil model ada di rentang ini">
            <span className="w-3.5 h-2 rounded-full bg-[#5f685e]/60 border border-[#5f685e] inline-block" />
            Rentang 50%
          </span>
          <span className="flex items-center gap-1.5 whitespace-nowrap text-[#202720] font-semibold" title="P50: nilai tengah dari 30 kemungkinan hasil">
            <span className="w-1 h-3 rounded-xs bg-[#5f685e] inline-block" />
            Nilai tengah
          </span>
          <span className="flex items-center gap-1.5 whitespace-nowrap text-[#202720] font-semibold" title="Nilai yang terukur sekarang">
            <span className="w-2 h-2 rotate-45 bg-[#fed639] border border-[#202720] inline-block" />
            Nilai sekarang
          </span>
        </div>
      </div>
    </div>
  );
};

interface NowcastRowProps {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  accent: string;
  data: NowcastDistribution;
}

const NowcastRow: React.FC<NowcastRowProps> = ({ label, icon: Icon, accent, data }) => {
  const min = Math.min(data.p10, data.observedNow ?? data.p10);
  const max = Math.max(data.p90, data.observedNow ?? data.p90);
  const span = Math.max(0.01, max - min);
  const pct = (v: number) => Math.max(0, Math.min(100, ((v - min) / span) * 100));

  return (
    <div className="bg-[#0b1326]/40 border border-white/10 rounded-lg p-2.5">
      <div className="flex items-center justify-between mb-1.5">
        <div className="flex items-center gap-2">
          <Icon className="w-3.5 h-3.5" style={{ color: accent }} />
          <span className="font-mono-data text-[11px] font-bold text-[#dae2fd] uppercase tracking-wider">
            {label}
          </span>
          <span className="text-[9px] font-mono-data text-[#849495]">{data.unit}</span>
        </div>
        <div className="flex items-center gap-3 text-[10px] font-mono-data">
          <span className="text-[#849495]">
            Tengah <span className="font-bold text-[#dae2fd]">{data.p50}</span>
          </span>
        </div>
      </div>

      <div className="relative h-7 w-full">
        <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 h-2 bg-[#070d18] rounded-full border border-white/10" />

        <div
          className="absolute top-1/2 -translate-y-1/2 h-2 rounded-full border"
          style={{
            left: `${pct(data.p10)}%`,
            width: `${pct(data.p90) - pct(data.p10)}%`,
            background: `${accent}25`,
            borderColor: `${accent}50`,
          }}
        />

        <div
          className="absolute top-1/2 -translate-y-1/2 h-2 rounded-full border"
          style={{
            left: `${pct(data.p25)}%`,
            width: `${pct(data.p75) - pct(data.p25)}%`,
            background: `${accent}55`,
            borderColor: `${accent}90`,
          }}
        />

        <div className="absolute top-0 bottom-0 w-0.5" style={{ left: `${pct(data.p50)}%`, background: accent }} />

        {data.observedNow != null && (
          <>
            <div className="absolute top-0 bottom-0 w-px bg-[#fed639]" style={{ left: `${pct(data.observedNow)}%` }} />
            <div className="absolute -top-1 w-2 h-2 rotate-45 bg-[#fed639] border border-[#070d18]" style={{ left: `calc(${pct(data.observedNow)}% - 4px)` }} />
          </>
        )}
      </div>

      <div className="flex justify-between text-[9px] font-mono-data text-[#849495] mt-1">
        <span>{min.toFixed(1)}</span>
        <span>{data.observedNow != null ? `Sekarang: ${data.observedNow.toFixed(1)}` : `${data.samples.length} kemungkinan`}</span>
        <span>{max.toFixed(1)}</span>
      </div>
    </div>
  );
};

export const ForecastChart = React.memo(ForecastChartComponent);
