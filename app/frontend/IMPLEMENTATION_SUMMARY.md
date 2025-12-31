# Urban Evolution AI - Implementation Summary

This document outlines the key implementation details, architectural choices, and features added to the Urban Evolution AI frontend application during the recent development phase.

## 1. Frontend Architecture

The application is built using **Next.js 14** (App Router) with **TypeScript**, focusing on a high-performance, visually immersive user experience.

*   **Framework**: Next.js 14
*   **Styling**: Tailwind CSS with `clsx` and `tailwind-merge` for dynamic class management.
*   **Maps**: `react-leaflet` (Leaflet.js) for interactive tile maps.
*   **WebGL/3D**: `ogl` for custom shaders and `cobe` for the interactive globe.
*   **Icons**: `lucide-react`.

## 2. Key Components & Visual Effects

### DarkVeil Shader (`components/DarkVeil.tsx`)
We replaced the standard background with a custom WebGL shader named **DarkVeil**.
*   **Technology**: Built using `ogl` (a lightweight WebGL library).
*   **Effect**: A dynamic, flowing noise-based shader that reacts to time.
*   **Implementation**: Rendered on a full-screen canvas, positioned absolutely behind the content (`absolute top-0`). It provides a "high-end" dark aesthetic.

### Interactive Globe (`components/ui/globe.tsx`)
A 3D interactive globe visualization on the landing page.
*   **Technology**: `cobe`.
*   **Features**: Draggable, auto-rotating, and visually styled to match the dark theme.

### Dynamic Navigation (`components/NavBar.tsx`)
*   **Scroll Effect**: The navbar starts transparent and applies a blur/glassmorphism effect (`backdrop-blur-md`) when scrolled past 20px.
*   **Context Awareness**: It detects if the user is on a map page (`/city/*`) and expands to full width to maximize screen real estate for the map.

## 3. Map Visualization Engine (`components/MapViewer.tsx`)

The core of the application is the split-screen map viewer used to compare urban evolution over time.

*   **Split-Screen Comparison**: Implemented a custom slider that clips the top map layer (Right Map) to reveal the bottom layer (Left Map).
*   **Synchronization**: Custom `MapSync` component ensures both map instances stay perfectly aligned during zoom and pan operations.
*   **Zoom Constraints**:
    *   **Min Zoom**: Locked to level 3 to prevent zooming out too far.
    *   **Default Zoom**: Set to level 3 (2x zoomed in relative to initial state).
*   **Prediction Warning**: A dynamic overlay warns users to "Zoom in to see AI prediction details" if they select the year **2030** while at a low zoom level (< 6). This manages expectations for high-resolution ML outputs.

## 4. Machine Learning Integration

We integrated a custom segmentation pipeline to generate future prediction tiles.

### Tile Generation Pipeline
*   **Script**: `ml-pipeline/generate_tiles.py`
*   **Model**: Fine-tuned **SegFormer** (`nvidia/segformer-b0-finetuned-ade-512-512`) trained on OSM and ESRI data.
*   **Process**:
    1.  Loads satellite imagery for the target year (2030).
    2.  Runs semantic segmentation to classify land use (Water, Trees, Built Area, etc.).
    3.  Applies a specific color palette to the output masks.
    4.  Saves the processed tiles to `public/tiles/tunis/2030/`.
*   **Scope**: Currently generates tiles for zoom levels **6** and **7** to optimize processing time and storage.

## 5. Page Structure

*   **Landing Page (`app/page.tsx`)**:
    *   Features the DarkVeil background.
    *   Hero section with the 3D Globe.
    *   "Flowing Menu" for selecting cities (Tunis, Manila, Copenhagen).
*   **City Analysis Page (`app/city/[id]/page.tsx`)**:
    *   **Full Screen**: Removed margins and padding to create an immersive map experience.
    *   **Controls**:
        *   Year selectors for Left/Right views (2014, 2020, 2025, 2030).
        *   Sidebar with real-time statistics (Population, Density, Growth Rate).
        *   Hidden calibration tools for aligning map layers manually.

## 6. Recent Workflow
1.  **Visual Upgrade**: Moved from a standard UI to a "dark mode" aesthetic with custom shaders.
2.  **Map Optimization**: Fixed zoom levels and removed "gray space" borders for a full-screen experience.
3.  **ML Deployment**: Ran the SegFormer model inference locally to populate the 2030 prediction layer for specific zoom levels.
