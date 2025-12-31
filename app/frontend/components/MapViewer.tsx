'use client';

import { useEffect, useRef, useMemo, useState } from 'react';
import { MapContainer, TileLayer, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

interface MapViewerProps {
  leftLayer: string;
  rightLayer: string;
  leftYear?: number;
  rightYear?: number;
  sliderPosition: number;
  bounds: [[number, number], [number, number]];
  maxZoom?: number;
  leftOffset?: { x: number, y: number };
  rightOffset?: { x: number, y: number };
  clippingRef?: React.RefObject<HTMLDivElement>;
}

// Component to synchronize two maps
function MapSync({ mapId, otherMapRef }: { mapId: string, otherMapRef: React.MutableRefObject<L.Map | null> }) {
  const map = useMap();

  useEffect(() => {
    if (!map) return;
    
    const handleMove = () => {
      if (otherMapRef.current) {
        const center = map.getCenter();
        const zoom = map.getZoom();
        const otherCenter = otherMapRef.current.getCenter();
        const otherZoom = otherMapRef.current.getZoom();
        
        if (center.lat !== otherCenter.lat || center.lng !== otherCenter.lng || zoom !== otherZoom) {
           otherMapRef.current.setView(center, zoom, { animate: false });
        }
      }
    };

    map.on('move', handleMove);
    return () => {
      map.off('move', handleMove);
    };
  }, [map, otherMapRef]);

  return null;
}

function ZoomMonitor({ onZoomChange }: { onZoomChange: (zoom: number) => void }) {
  const map = useMap();
  useEffect(() => {
    const handler = () => {
      onZoomChange(map.getZoom());
    };
    map.on('zoomend', handler);
    // Initial check
    onZoomChange(map.getZoom());
    return () => {
      map.off('zoomend', handler);
    };
  }, [map, onZoomChange]);
  return null;
}

// Component to handle map resizing
function MapResizer({ width }: { width: number }) {
  const map = useMap();
  useEffect(() => {
    if (width > 0) {
      map.invalidateSize();
    }
  }, [map, width]);
  return null;
}

export default function MapViewer({ leftLayer, rightLayer, leftYear, rightYear, sliderPosition, bounds, maxZoom = 7, leftOffset, rightOffset, clippingRef }: MapViewerProps) {
  const mapLeftRef = useRef<L.Map | null>(null);
  const mapRightRef = useRef<L.Map | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const [currentZoom, setCurrentZoom] = useState(3);

  useEffect(() => {
    if (!containerRef.current) return;
    
    const resizeObserver = new ResizeObserver((entries) => {
      for (let entry of entries) {
        setDimensions({
          width: entry.contentRect.width,
          height: entry.contentRect.height
        });
      }
    });
    
    resizeObserver.observe(containerRef.current);
    return () => resizeObserver.disconnect();
  }, []);
  
  // ... customCRS ...
  const customCRS = useMemo(() => {
    const factor = 1 / Math.pow(2, maxZoom);
    const crs = L.Util.extend({}, L.CRS.Simple, {
      transformation: new L.Transformation(factor, 0, factor, 0)
    });
    return crs;
  }, [maxZoom]);

  const leafletBounds = L.latLngBounds(
    L.latLng(bounds[0][0], bounds[0][1]), 
    L.latLng(bounds[1][0], bounds[1][1])
  );

  // Generate unique class names for offsets
  const leftClass = `layer-left-${Math.floor(Math.random() * 1000)}`;
  const rightClass = `layer-right-${Math.floor(Math.random() * 1000)}`;

  const showPredictionWarning = (leftYear === 2030 || rightYear === 2030) && currentZoom < 6;

  return (
    <div className="relative w-full h-full bg-black" ref={containerRef}>
      <style>{`
        .${leftClass} { transform: translate(${leftOffset?.x || 0}px, ${leftOffset?.y || 0}px); }
        .${rightClass} { transform: translate(${rightOffset?.x || 0}px, ${rightOffset?.y || 0}px); }
      `}</style>

      {showPredictionWarning && (
        <div className="absolute top-20 left-1/2 transform -translate-x-1/2 z-[1000] bg-black/80 text-white px-6 py-3 rounded-full border border-yellow-500/50 backdrop-blur-md flex items-center gap-3 shadow-2xl animate-in fade-in slide-in-from-top-4">
          <div className="w-2 h-2 rounded-full bg-yellow-500 animate-pulse" />
          <span className="font-medium text-sm">Zoom in to see AI prediction details</span>
        </div>
      )}

      {/* Left Map (Background) */}
      <MapContainer
        crs={customCRS}
        bounds={leafletBounds}
        maxBounds={leafletBounds}
        maxBoundsViscosity={1.0}
        zoom={3}
        minZoom={3}
        maxZoom={maxZoom}
        scrollWheelZoom={true}
        className="absolute inset-0 z-0 bg-black"
        ref={mapLeftRef}
        attributionControl={false}
      >
        <ZoomMonitor onZoomChange={setCurrentZoom} />
        <TileLayer
          url={leftLayer}
          noWrap={true}
          bounds={leafletBounds}
          tileSize={256}
          minZoom={0}
          maxZoom={maxZoom}
          className={`${leftLayer.includes('prediction') ? 'filter hue-rotate-180 contrast-125' : ''} ${leftClass}`}
        />
        <MapSync mapId="left" otherMapRef={mapRightRef} />
      </MapContainer>

      {/* Right Map (Foreground - Clipped) */}
      <div 
        ref={clippingRef}
        className="absolute inset-0 z-10 overflow-hidden pointer-events-none"
        style={{ width: `${sliderPosition}%` }}
      >
        <div 
          className="h-full pointer-events-auto"
          style={{ width: dimensions.width ? `${dimensions.width}px` : 'calc(100vw - 350px)' }}
        > 
          <MapContainer
            crs={customCRS}
            bounds={leafletBounds}
            maxBounds={leafletBounds}
            maxBoundsViscosity={1.0}
            zoom={3}
            minZoom={3}
            maxZoom={maxZoom}
            scrollWheelZoom={true}
            className="w-full h-full bg-transparent"
            ref={mapRightRef}
            zoomControl={false}
            attributionControl={false}
          >
            <MapResizer width={dimensions.width} />
            <TileLayer
              url={rightLayer}
              noWrap={true}
              bounds={leafletBounds}
              tileSize={256}
              minZoom={0}
              maxZoom={maxZoom}
              className={`${rightLayer.includes('prediction') ? 'filter hue-rotate-180 contrast-125' : ''} ${rightClass}`}
            />
            <MapSync mapId="right" otherMapRef={mapLeftRef} />
          </MapContainer>
        </div>
      </div>
    </div>
  );
}
