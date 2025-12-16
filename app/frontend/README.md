# 🎨 Urban Evolution AI - Frontend

Next.js 14 frontend for the Urban Evolution AI Platform.

## 🎯 Purpose

Interactive web dashboard for visualizing urban growth predictions and generating future scenarios.

## ✨ Features

- 🗺️ **Interactive Map**: Explore cities with building overlays and growth heatmaps
- ⏱️ **Timeline Slider**: Travel through time from 2020 to 2050
- 🎨 **Scenario Builder**: Generate future city scenarios with AI
- 💬 **AI Chat**: Interact with multi-agent system
- 📊 **Analytics Dashboard**: Visualize growth metrics and predictions
- 🌍 **City Comparison**: Compare cities side-by-side

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd app/frontend
npm install
```

### 2. Configure Environment

Create `.env.local`:

```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000

# Map Configuration
NEXT_PUBLIC_DEFAULT_CENTER_LAT=36.8065
NEXT_PUBLIC_DEFAULT_CENTER_LNG=10.1815
NEXT_PUBLIC_DEFAULT_ZOOM=12

# Feature Flags
NEXT_PUBLIC_ENABLE_CHAT=true
NEXT_PUBLIC_ENABLE_SCENARIOS=true

# Analytics (optional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

### 3. Start Development Server

```bash
npm run dev
```

Visit: http://localhost:3000

### 4. Build for Production

```bash
# Build
npm run build

# Start production server
npm start
```

## 📁 Structure

```
frontend/
├── src/
│   ├── app/                        # Next.js 14 App Router
│   │   ├── page.tsx               # Home page
│   │   ├── layout.tsx             # Root layout
│   │   ├── dashboard/             # Dashboard pages
│   │   │   └── page.tsx
│   │   ├── scenarios/             # Scenario pages
│   │   │   ├── page.tsx           # List scenarios
│   │   │   ├── create/
│   │   │   │   └── page.tsx       # Create scenario
│   │   │   └── [id]/
│   │   │       └── page.tsx       # View scenario
│   │   ├── chat/                  # Chat interface
│   │   │   └── page.tsx
│   │   └── api/                   # API routes (if needed)
│   │
│   ├── components/                 # React components
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── dialog.tsx
│   │   │   └── ...
│   │   ├── map/                   # Map components
│   │   │   ├── InteractiveMap.tsx
│   │   │   ├── BuildingLayer.tsx
│   │   │   ├── HeatmapLayer.tsx
│   │   │   └── MapControls.tsx
│   │   ├── timeline/              # Timeline components
│   │   │   └── TimeSlider.tsx
│   │   ├── scenario/              # Scenario components
│   │   │   ├── ScenarioBuilder.tsx
│   │   │   ├── PolicySelector.tsx
│   │   │   ├── ImageComparison.tsx
│   │   │   └── CostEstimator.tsx
│   │   ├── chat/                  # Chat components
│   │   │   ├── AgentChat.tsx
│   │   │   ├── MessageList.tsx
│   │   │   └── ChatInput.tsx
│   │   ├── analytics/             # Analytics components
│   │   │   ├── GrowthCharts.tsx
│   │   │   ├── PopulationChart.tsx
│   │   │   └── MetricsCard.tsx
│   │   └── layout/                # Layout components
│   │       ├── Header.tsx
│   │       ├── Sidebar.tsx
│   │       └── Footer.tsx
│   │
│   ├── lib/                       # Utilities & API client
│   │   ├── api-client.ts          # Axios/fetch wrapper
│   │   ├── utils.ts               # Helper functions
│   │   ├── constants.ts           # Constants
│   │   ├── types.ts               # TypeScript types
│   │   └── hooks/                 # Custom React hooks
│   │       ├── use-api.ts
│   │       ├── use-map.ts
│   │       └── use-websocket.ts
│   │
│   └── styles/
│       └── globals.css            # Global styles
│
├── public/                        # Static assets
│   ├── images/
│   ├── icons/
│   └── ...
│
├── tests/                         # Tests
│   ├── unit/
│   └── e2e/
│
├── package.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js
└── README.md
```

## 🗺️ Map Integration

### React Leaflet

```tsx
import { MapContainer, TileLayer } from 'react-leaflet';
import BuildingLayer from '@/components/map/BuildingLayer';

export default function InteractiveMap({ city }) {
  return (
    <MapContainer 
      center={[city.lat, city.lng]} 
      zoom={13}
      className="h-full w-full"
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <BuildingLayer cityId={city.id} />
    </MapContainer>
  );
}
```

## 📊 Data Fetching

### SWR for Data Fetching

```tsx
import useSWR from 'swr';
import { apiClient } from '@/lib/api-client';

export default function CityDashboard({ cityId }) {
  const { data, error, isLoading } = useSWR(
    `/api/cities/${cityId}`,
    apiClient.get
  );

  if (isLoading) return <Loading />;
  if (error) return <Error />;

  return <Dashboard city={data} />;
}
```

## 🎨 Styling

### Tailwind CSS + shadcn/ui

```tsx
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export default function ScenarioCard({ scenario }) {
  return (
    <Card className="p-6">
      <h3 className="text-2xl font-bold mb-4">{scenario.title}</h3>
      <p className="text-muted-foreground mb-4">{scenario.description}</p>
      <Button>View Details</Button>
    </Card>
  );
}
```

## 💬 WebSocket Chat

```tsx
import { useEffect, useState } from 'react';
import { useWebSocket } from '@/lib/hooks/use-websocket';

export default function AgentChat() {
  const { messages, sendMessage, isConnected } = useWebSocket('/api/chat/stream');
  const [input, setInput] = useState('');

  const handleSend = () => {
    sendMessage({ content: input, cityId: 'tunis' });
    setInput('');
  };

  return (
    <div>
      <MessageList messages={messages} />
      <ChatInput 
        value={input} 
        onChange={setInput} 
        onSend={handleSend}
        disabled={!isConnected}
      />
    </div>
  );
}
```

## 🧪 Testing

### Jest (Unit Tests)

```bash
# Run tests
npm test

# Run in watch mode
npm run test:watch

# Coverage
npm run test:coverage
```

### Playwright (E2E Tests)

```bash
# Run E2E tests
npm run test:e2e

# Run in UI mode
npm run test:e2e:ui
```

## 🎨 Component Library

We use **shadcn/ui** for components:

```bash
# Add new component
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
```

## 📱 Responsive Design

All components are responsive:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Responsive grid */}
</div>
```

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Production deployment
vercel --prod
```

### Netlify

```bash
# Build
npm run build

# Deploy with Netlify CLI
netlify deploy --prod
```

### Docker

```bash
# Build
docker build -t urban-evolution-frontend .

# Run
docker run -p 3000:3000 urban-evolution-frontend
```

## 🎯 Key Pages

### Home Page (`/`)
- Hero section
- Feature overview
- Call to action

### Dashboard (`/dashboard`)
- Interactive map
- Growth metrics
- Timeline slider

### Scenarios (`/scenarios`)
- List of generated scenarios
- Create new scenario
- Compare scenarios

### Chat (`/chat`)
- Multi-agent chat interface
- Real-time responses
- Conversation history

## 🐛 Troubleshooting

### Map Not Loading

```bash
# Install Leaflet CSS
# Add to app/layout.tsx:
import 'leaflet/dist/leaflet.css';
```

### API Connection Issues

```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend
```

### Build Errors

```bash
# Clear Next.js cache
rm -rf .next
npm run build
```

## 📚 Documentation

- **Next.js**: https://nextjs.org/docs
- **React Leaflet**: https://react-leaflet.js.org/
- **shadcn/ui**: https://ui.shadcn.com/
- **Tailwind CSS**: https://tailwindcss.com/docs

## 🎯 Next Steps

1. **Setup Environment**: Configure `.env.local`
2. **Start Backend**: Ensure backend is running
3. **Install Dependencies**: Run `npm install`
4. **Start Dev Server**: Run `npm run dev`
5. **Build Components**: Start with map component

Happy Building! 🚀
