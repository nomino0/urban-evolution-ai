'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Home, Info, Map } from 'lucide-react';
import { useEffect, useState } from 'react';

export default function NavBar() {
  const [scrolled, setScrolled] = useState(false);
  const pathname = usePathname();
  const isMapPage = pathname?.startsWith('/city/');

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      scrolled ? 'bg-black/50 backdrop-blur-md py-6 border-b border-white/5' : 'bg-transparent py-10'
    }`}>
      <nav className={`${isMapPage ? 'w-full px-6' : 'container mx-auto px-6'} flex items-center justify-between`}>
        <Link href="/" className="flex items-center gap-2 text-white font-bold text-xl tracking-wider hover:opacity-80 transition-opacity">
          <Map className="text-primary" />
          <span>URBAN<span className="text-primary">EVO</span></span>
        </Link>
        
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2 text-white/80 hover:text-white transition-colors">
            <Home size={18} />
            <span className="font-medium">Home</span>
          </Link>
          
          <Link href="/about" className="flex items-center gap-2 text-white/80 hover:text-white transition-colors">
            <Info size={18} />
            <span className="font-medium">About</span>
          </Link>
        </div>
      </nav>
    </div>
  );
}
