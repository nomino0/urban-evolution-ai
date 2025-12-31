'use client';

import { useState, useEffect, useRef } from 'react';
import { useParams } from 'next/navigation';
import { Layers, Users, Building, TrendingUp, AlertTriangle, Sparkles } from 'lucide-react';
import dynamic from 'next/dynamic';

// Dynamically import Map component to avoid SSR issues with Leaflet
const MapViewer = dynamic(() => import('@/components/MapViewer'), { 
  ssr: false,
  loading: () => <div className="w-full h-full bg-gray-900 animate-pulse" />
});

// Mock data for cities
const CITY_DATA: any = {
  tunis: {
    name: 'Grand Tunis',
    population: '2.7M',
    density: '3,200/km²',
    growthRate: '+1.2%',
    bounds: [[0, 0], [15740, 28156]], // [height, width] from the tif
    layers: {
      2014: '/tiles/tunis/2014/{z}/{x}/{y}.png',
      2020: '/tiles/tunis/2020/{z}/{x}/{y}.png',
      2025: '/tiles/tunis/2025/{z}/{x}/{y}.png',
      2030: '/tiles/tunis/2030/{z}/{x}/{y}.png',
    }
  },
  // ... other cities
};

export default function CityPage() {
  const params = useParams();
  const cityId = params.id as string;
  const city = CITY_DATA[cityId] || CITY_DATA['tunis'];
  const [sliderPosition, setSliderPosition] = useState(50);
  const [selectedYearLeft, setSelectedYearLeft] = useState(2014);
  const [selectedYearRight, setSelectedYearRight] = useState(2025);
  const [isDragging, setIsDragging] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const clippingRef = useRef<HTMLDivElement>(null);
  const handleRef = useRef<HTMLDivElement>(null);
  const lastPercentageRef = useRef(50);
  
  // Manual offsets for alignment (x, y in pixels)
  const [offsets, setOffsets] = useState<Record<string, {x: number, y: number}>>({
    2014: { x: 0, y: 0 },
    2020: { x: 0, y: 0 },
    2025: { x: 0, y: 0 },
    2030: { x: 0, y: 0 },
  });

  const [showCalibration, setShowCalibration] = useState(false);

  const updateOffset = (year: string, dx: number, dy: number) => {
    setOffsets(prev => ({
      ...prev,
      [year]: { x: prev[year].x + dx, y: prev[year].y + dy }
    }));
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    setIsDragging(true);
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    setIsDragging(true);
  };

  useEffect(() => {
    const handleMove = (clientX: number) => {
      if (!containerRef.current) return;
      const rect = containerRef.current.getBoundingClientRect();
      const x = Math.max(0, Math.min(clientX - rect.left, rect.width));
      const percentage = (x / rect.width) * 100;
      
      // Direct DOM manipulation for performance (60fps)
      if (clippingRef.current) {
        clippingRef.current.style.width = `${percentage}%`;
      }
      if (handleRef.current) {
        handleRef.current.style.left = `${percentage}%`;
      }
      
      lastPercentageRef.current = percentage;
    };

    const handleMouseMove = (e: MouseEvent) => {
      if (!isDragging) return;
      e.preventDefault();
      handleMove(e.clientX);
    };

    const handleTouchMove = (e: TouchEvent) => {
      if (!isDragging) return;
      e.preventDefault();
      handleMove(e.touches[0].clientX);
    };

    const handleEnd = () => {
      setIsDragging(false);
      setSliderPosition(lastPercentageRef.current);
    };

    if (isDragging) {
      window.addEventListener('mousemove', handleMouseMove);
      window.addEventListener('mouseup', handleEnd);
      window.addEventListener('touchmove', handleTouchMove);
      window.addEventListener('touchend', handleEnd);
    }

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleEnd);
      window.removeEventListener('touchmove', handleTouchMove);
      window.removeEventListener('touchend', handleEnd);
    };
  }, [isDragging]);

  return (
    <div className="flex h-screen bg-black">
      {/* Main Viewer Container - Full Screen */}
      <div 
        ref={containerRef}
        className="flex-1 relative overflow-hidden group"
      >
        <MapViewer 
          leftLayer={city.layers[selectedYearRight]}
          rightLayer={city.layers[selectedYearLeft]}
          leftYear={selectedYearRight}
          rightYear={selectedYearLeft}
          sliderPosition={sliderPosition}
          bounds={city.bounds}
          maxZoom={7}
          leftOffset={offsets[selectedYearRight]}
          rightOffset={offsets[selectedYearLeft]}
          clippingRef={clippingRef}
        />

        {/* Visual Slider Handle */}
        <div 
          ref={handleRef}
          className="absolute top-0 bottom-0 w-1 bg-white cursor-ew-resize z-[1000] hover:w-1.5 transition-all"
          style={{ left: `${sliderPosition}%` }}
          onMouseDown={handleMouseDown}
          onTouchStart={handleTouchStart}
        >
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg text-black cursor-ew-resize hover:scale-110 transition-transform">
            <Layers size={16} />
          </div>
        </div>

        {/* Calibration Controls (Hidden by default) */}
        {showCalibration && (
          <div className="absolute top-4 left-4 z-[1003] bg-black/80 p-4 rounded-xl border border-red-500/50 text-white">
            <h3 className="text-xs font-bold text-red-400 mb-2">CALIBRATION MODE</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-xs mb-1">Left ({selectedYearLeft})</div>
                <div className="grid grid-cols-3 gap-1">
                  <button onClick={() => updateOffset(String(selectedYearLeft), 0, -1)} className="bg-white/10 p-1 hover:bg-white/20">↑</button>
                  <button onClick={() => updateOffset(String(selectedYearLeft), 0, -10)} className="bg-white/10 p-1 hover:bg-white/20">↑↑</button>
                  <button onClick={() => updateOffset(String(selectedYearLeft), 0, 1)} className="bg-white/10 p-1 hover:bg-white/20">↓</button>
                  <button onClick={() => updateOffset(String(selectedYearLeft), -1, 0)} className="bg-white/10 p-1 hover:bg-white/20">←</button>
                  <div className="text-center text-[10px]">{offsets[selectedYearLeft].x},{offsets[selectedYearLeft].y}</div>
                  <button onClick={() => updateOffset(String(selectedYearLeft), 1, 0)} className="bg-white/10 p-1 hover:bg-white/20">→</button>
                </div>
              </div>
              <div>
                <div className="text-xs mb-1">Right ({selectedYearRight})</div>
                <div className="grid grid-cols-3 gap-1">
                  <button onClick={() => updateOffset(String(selectedYearRight), 0, -1)} className="bg-white/10 p-1 hover:bg-white/20">↑</button>
                  <button onClick={() => updateOffset(String(selectedYearRight), 0, -10)} className="bg-white/10 p-1 hover:bg-white/20">↑↑</button>
                  <button onClick={() => updateOffset(String(selectedYearRight), 0, 1)} className="bg-white/10 p-1 hover:bg-white/20">↓</button>
                  <button onClick={() => updateOffset(String(selectedYearRight), -1, 0)} className="bg-white/10 p-1 hover:bg-white/20">←</button>
                  <div className="text-center text-[10px]">{offsets[selectedYearRight].x},{offsets[selectedYearRight].y}</div>
                  <button onClick={() => updateOffset(String(selectedYearRight), 1, 0)} className="bg-white/10 p-1 hover:bg-white/20">→</button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Controls Overlay */}
        <div className="absolute bottom-8 left-8 right-8 flex justify-between items-end pointer-events-none z-[1002]">
          <div className="bg-black/60 backdrop-blur-md p-4 rounded-xl border border-white/10 pointer-events-auto">
            <label className="block text-xs text-gray-400 mb-2">Left View</label>
            <div className="flex gap-2">
              {[2014, 2020, 2025, 2030].map((year) => (
                <button
                  key={year}
                  onClick={() => setSelectedYearLeft(year)}
                  className={`px-3 py-1 rounded-md text-sm transition-colors flex items-center gap-1 ${
                    selectedYearLeft === year ? 'bg-primary text-white' : 'bg-white/10 hover:bg-white/20'
                  }`}
                >
                  {year === 2030 && <Sparkles size={12} className="text-yellow-400" />}
                  {year}
                </button>
              ))}
            </div>
          </div>

          <div className="bg-black/60 backdrop-blur-md p-4 rounded-xl border border-white/10 pointer-events-auto">
            <label className="block text-xs text-gray-400 mb-2">Right View</label>
            <div className="flex gap-2">
              {[2014, 2020, 2025, 2030].map((year) => (
                <button
                  key={year}
                  onClick={() => setSelectedYearRight(year)}
                  className={`px-3 py-1 rounded-md text-sm transition-colors flex items-center gap-1 ${
                    selectedYearRight === year ? 'bg-purple-600 text-white' : 'bg-white/10 hover:bg-white/20'
                  }`}
                >
                  {year === 2030 && <Sparkles size={12} className="text-yellow-400" />}
                  {year}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Sidebar */}
      <div className="w-80 bg-transparent p-6 pt-28 overflow-y-auto z-20">
        <div className="flex justify-between items-center mb-2">
          <h1 className="text-3xl font-bold">{city.name}</h1>
          <button 
            onClick={() => setShowCalibration(!showCalibration)}
            className="text-xs text-gray-600 hover:text-white"
            title="Toggle Calibration"
          >
            ⚙️
          </button>
        </div>
        {/* ... stats ... */}
         <div className="flex items-center gap-2 text-green-400 mb-8">
          <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
          <span className="text-sm font-medium">Analysis Complete</span>
        </div>

        <div className="space-y-6">
          <div className="p-4 bg-white/5 rounded-xl border border-white/10">
            <div className="flex items-center gap-3 mb-2 text-gray-400">
              <Users size={18} />
              <span className="text-sm">Population</span>
            </div>
            <div className="text-2xl font-bold">{city.population}</div>
          </div>

          <div className="p-4 bg-white/5 rounded-xl border border-white/10">
            <div className="flex items-center gap-3 mb-2 text-gray-400">
              <Building size={18} />
              <span className="text-sm">Density</span>
            </div>
            <div className="text-2xl font-bold">{city.density}</div>
          </div>

          <div className="p-4 bg-white/5 rounded-xl border border-white/10">
            <div className="flex items-center gap-3 mb-2 text-gray-400">
              <TrendingUp size={18} />
              <span className="text-sm">Growth Rate</span>
            </div>
            <div className="text-2xl font-bold text-green-400">{city.growthRate}</div>
          </div>
        </div>
      </div>
    </div>
  );
}
