'use client';

import React, { useState } from 'react';
import DarkVeil from '../components/DarkVeil';
import FlowingMenu from '../components/FlowingMenu';
import { Globe } from '../components/ui/globe';
import * as Dialog from '@radix-ui/react-dialog';
import { X, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  const [isRequestOpen, setIsRequestOpen] = useState(false);

  const menuItems = [
    { link: '/city/tunis', text: 'Tunis', image: 'https://picsum.photos/600/400?random=1' },
    { link: '/city/manila', text: 'Manila', image: 'https://picsum.photos/600/400?random=2' },
    { link: '/city/copenhagen', text: 'Copenhagen', image: 'https://picsum.photos/600/400?random=3' },
    { 
      link: '#', 
      text: 'Request City', 
      image: 'https://picsum.photos/600/400?random=4',
      onClick: (e: React.MouseEvent) => {
        e.preventDefault();
        setIsRequestOpen(true);
      }
    }
  ];

  return (
    <div className="relative w-full min-h-screen overflow-x-hidden bg-black text-white">
      {/* Background DarkVeil */}
      <div className="absolute top-0 left-0 w-full h-screen z-0 pointer-events-none">
        <DarkVeil />
      </div>
      
      {/* Hero Section */}
      <div className="relative z-10 container mx-auto px-6 pt-32 pb-12 min-h-screen flex flex-col justify-center">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-8">
            
            
            <h1 className="text-6xl md:text-7xl font-bold tracking-tight leading-tight">
              Predicting <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-600">
                Urban Evolution
              </span>
            </h1>
            
            <p className="text-xl text-gray-300 max-w-xl leading-relaxed">
              An AI-powered platform that combines satellite imagery, predictive modeling, and generative AI to visualize the future of our cities. Explore scenarios, analyze growth, and make data-driven decisions.
            </p>
            
            <div className="flex flex-wrap gap-4">
              <button 
                onClick={() => document.getElementById('cities')?.scrollIntoView({ behavior: 'smooth' })}
                className="px-8 py-4 bg-white text-black rounded-full font-bold hover:bg-gray-200 transition-colors flex items-center gap-2"
              >
                Explore Cities <ArrowRight size={18} />
              </button>
              <Link href="/about" className="px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-full font-bold hover:bg-white/20 transition-colors">
                Learn More
              </Link>
            </div>
          </div>
          
          <div className="relative h-[600px] w-full flex items-center justify-center">
             <Globe className="top-10" />
          </div>
        </div>
      </div>

      {/* Cities Section */}
      <div id="cities" className="relative z-10 w-full min-h-screen flex flex-col items-center justify-center py-20 bg-black/20 backdrop-blur-sm">
        <div className="w-full h-[600px]">
          <FlowingMenu items={menuItems} />
        </div>
      </div>

      <Dialog.Root open={isRequestOpen} onOpenChange={setIsRequestOpen}>
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50" />
          <Dialog.Content className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-background p-8 rounded-xl shadow-2xl z-50 w-full max-w-md border border-white/10">
            <div className="flex justify-between items-center mb-6">
              <Dialog.Title className="text-2xl font-bold">Request New City</Dialog.Title>
              <Dialog.Close className="text-white/50 hover:text-white">
                <X />
              </Dialog.Close>
            </div>
            
            <div className="space-y-4">
              <p className="text-muted-foreground">
                Processing city evolution requires analyzing thousands of satellite tiles. 
                Please submit your request below.
              </p>
              
              <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
                <div>
                  <label className="block text-sm font-medium mb-2">City Name</label>
                  <input 
                    type="text" 
                    className="w-full p-3 rounded-lg bg-white/5 border border-white/10 focus:border-primary outline-none transition-colors"
                    placeholder="e.g., Tokyo"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Email</label>
                  <input 
                    type="email" 
                    className="w-full p-3 rounded-lg bg-white/5 border border-white/10 focus:border-primary outline-none transition-colors"
                    placeholder="your@email.com"
                  />
                </div>
                <button className="w-full py-3 bg-primary text-primary-foreground rounded-lg font-bold hover:opacity-90 transition-opacity">
                  Submit Request
                </button>
              </form>
            </div>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>
    </div>
  );
}
