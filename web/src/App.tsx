import React, { useState, useEffect } from 'react';
import { NodeId, ActiveTab, HistoricalAnalog, DashboardLiveSnapshot, ModelMetrics } from './types';
import { TIMELINE_FRAMES, SAMPLE_NOWCAST } from './data/nodesData';
import { fetchDashboardLive } from './services/dashboardLive';
import { fetchModelMetrics } from './services/metricsService';
import { SideNav } from './components/SideNav';
import { TopAppBar } from './components/TopAppBar';
import { MapView } from './components/MapView';
import { TimelineScrubber } from './components/TimelineScrubber';
import { ForecastChart } from './components/ForecastChart';
import { ModelPerformancePanel } from './components/ModelPerformancePanel';
import { RetrievalAnalogsPanel } from './components/RetrievalAnalogsPanel';
import { NodeDetailModal } from './components/NodeDetailModal';
import { TopologyGraphOverlay } from './components/TopologyGraphOverlay';
import { X } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('forecast');
  const [selectedNodeId, setSelectedNodeId] = useState<NodeId>('MAIN');
  const [radarVisible, setRadarVisible] = useState(true);
  const [nodesVisible, setNodesVisible] = useState(true);
  const [isTopologyModalOpen, setIsTopologyModalOpen] = useState(false);
  const [activeNodeDetailId, setActiveNodeDetailId] = useState<NodeId | null>(null);
  const [selectedAnalog, setSelectedAnalog] = useState<HistoricalAnalog | null>(null);
  const [liveSnapshot, setLiveSnapshot] = useState<DashboardLiveSnapshot | null>(null);
  const [modelMetrics, setModelMetrics] = useState<ModelMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let controller: AbortController | undefined;
    const refresh = async () => {
      controller?.abort();
      controller = new AbortController();
      try {
        const [snapshot, metrics] = await Promise.all([
          fetchDashboardLive(controller.signal),
          fetchModelMetrics(controller.signal),
        ]);
        setLiveSnapshot(snapshot);
        setModelMetrics(metrics);
      } catch (error) {
        if ((error as DOMException).name !== 'AbortError') setLiveSnapshot(null);
      } finally {
        setIsLoading(false);
      }
    };
    void refresh();
    const timer = setInterval(() => void refresh(), 15 * 60_000);
    return () => { controller?.abort(); clearInterval(timer); };
  }, []);

  const dashboardFrame = liveSnapshot?.frame ?? TIMELINE_FRAMES[0];
  const nowcast = liveSnapshot?.nowcast ?? SAMPLE_NOWCAST;
  const dataStatus = liveSnapshot?.source === 'era5_h7'
    ? `Data ERA5 sampai ${liveSnapshot.frame.timeWib} (7 hari lalu)`
    : isLoading ? 'Menghubungkan ke server…' : liveSnapshot ? `Arsip data uji sampai ${liveSnapshot.frame.timeWib}` : 'Contoh data — server belum terhubung';

  return <div className="app-shell min-h-[100dvh] h-[100dvh] w-full overflow-hidden flex font-body select-text">
    <SideNav activeTab={activeTab} onSelectTab={setActiveTab} />
    <TopAppBar onSelectTab={setActiveTab} radarVisible={radarVisible} onToggleRadar={() => setRadarVisible((value) => !value)} nodesVisible={nodesVisible} onToggleNodes={() => setNodesVisible((value) => !value)} onOpenTopologyModal={() => setIsTopologyModalOpen(true)} />
    <main className="flex-1 relative md:ml-[72px] h-full flex flex-col pt-[64px]">
      {activeTab === 'forecast' && <div className="flex-1 p-6 overflow-y-auto"><div className="glass-panel-cyan p-6 space-y-8"><section><h2 className="font-headline text-lg font-bold text-[#dbfcff] mb-4 uppercase tracking-wider">Prakiraan 1 jam berikutnya</h2><ForecastChart nowcast={nowcast} windowRangeWib={dashboardFrame.windowRangeWib} /></section><section><RetrievalAnalogsPanel analogs={liveSnapshot?.analogs} onSelectAnalog={setSelectedAnalog} /></section></div></div>}
      {activeTab === 'map' && <div className="flex-1 flex flex-col h-full overflow-hidden relative"><div className="flex-1 relative z-0 p-3 md:p-4 pb-0"><MapView selectedNodeId={selectedNodeId} onSelectNode={setSelectedNodeId} currentFrame={dashboardFrame} radarVisible={radarVisible} nodesVisible={nodesVisible} onOpenNodeDetail={setActiveNodeDetailId} /></div>
        <div className={`absolute top-6 right-6 z-20 border px-3 py-1.5 text-[10px] font-mono-data font-semibold rounded shadow-xs ${liveSnapshot?.source === 'era5_h7' ? 'border-[#1f6056] bg-[#eef6ef] text-[#1f6056]' : 'border-[#a46b13] bg-[#fff8df] text-[#78520f]'}`}>{liveSnapshot?.source === 'era5_h7' ? 'ERA5 · 7 hari lalu' : liveSnapshot?.source === 'sample' ? 'Arsip data uji' : 'Contoh data'}</div>
        <div className="absolute bottom-6 left-0 right-0 px-6 z-20 pointer-events-auto flex justify-center"><TimelineScrubber nowWib={dashboardFrame.timeWib} validAtWib={nowcast.precipitation.validAtWib} dataStatus={dataStatus} isEra5={liveSnapshot?.source === 'era5_h7'} windowRangeWib={dashboardFrame.windowRangeWib} /></div></div>}
      {activeTab === 'eval' && <div className="flex-1 p-6 overflow-y-auto"><div className="glass-panel-cyan p-6"><h2 className="font-headline text-lg font-bold text-[#dbfcff] mb-4 uppercase tracking-wider">Hasil uji model</h2><ModelPerformancePanel metrics={modelMetrics} /></div></div>}
    </main>
    <TopologyGraphOverlay isOpen={isTopologyModalOpen} onClose={() => setIsTopologyModalOpen(false)} onSelectNode={(nodeId) => { setSelectedNodeId(nodeId); setActiveTab('map'); }} />
    <NodeDetailModal nodeId={activeNodeDetailId} frame={dashboardFrame} onClose={() => setActiveNodeDetailId(null)} />
    {selectedAnalog && <div className="fixed inset-0 z-50 bg-[#070d18]/80 backdrop-blur-sm flex items-center justify-center p-4"><div className="bg-[#070d18] w-full max-w-lg rounded-xl border border-[#00f0ff]/50 p-6 relative"><button onClick={() => setSelectedAnalog(null)} className="absolute top-4 right-4 p-1.5" aria-label="Tutup"><X className="w-4 h-4" /></button><h3 className="font-headline text-base font-bold text-[#00f0ff] mb-1 uppercase">{selectedAnalog.datetime}</h3><span className="font-mono-data text-xs text-[#fed639]">Jarak: {selectedAnalog.distanceL2?.toFixed(2) ?? '—'} (makin kecil makin mirip)</span><p className="text-sm text-[#dae2fd] my-4">{selectedAnalog.outcomeSummary}</p><button onClick={() => setSelectedAnalog(null)} className="px-4 py-2 rounded-lg bg-[#00f0ff] text-[#002022] font-mono-data text-xs font-bold">Tutup</button></div></div>}
  </div>;
}
