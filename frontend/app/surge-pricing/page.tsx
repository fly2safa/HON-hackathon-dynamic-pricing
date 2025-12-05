'use client';

import Image from 'next/image';
import Link from 'next/link';
import SurgePricingComparison from '@/components/SurgePricingComparison';

export default function SurgePricingPage() {
  return (
    <main className="min-h-screen bg-black">
      {/* Header */}
      <header className="bg-black shadow-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-2 sm:py-3">
          <div className="flex items-center justify-between gap-2 sm:gap-4">
            <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-shrink">
              <Image 
                src="/images/honeygo-logo.png" 
                alt="HoneyGo Logo" 
                width={40} 
                height={40}
                className="rounded-lg flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10"
              />
              <div className="min-w-0">
                <h1 className="text-lg sm:text-xl md:text-2xl font-bold text-white truncate">
                  HoneyGo
                </h1>
                <p className="text-xs sm:text-sm text-gray-400 hidden sm:block">
                  AI-Powered Pricing
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2 sm:gap-4 lg:gap-6 flex-shrink-0">
              <nav className="flex items-center gap-2 sm:gap-3 lg:gap-4">
                <Link
                  href="/"
                  className="text-sm sm:text-base text-gray-300 hover:text-white transition-colors font-medium whitespace-nowrap"
                >
                  Pricing
                </Link>
                <Link
                  href="/surge-pricing"
                  className="text-sm sm:text-base text-white border-b-2 border-[#FF6A13] pb-0.5 sm:pb-1 transition-colors font-medium whitespace-nowrap"
                >
                  Surge
                </Link>
              </nav>
              <div className="text-right border-l border-gray-700 pl-2 sm:pl-4 lg:pl-6 hidden md:block">
                <p className="text-xs text-gray-400">Powered by</p>
                <p className="text-sm lg:text-base font-semibold text-[#FF6A13]">
                  Honeywell AI
                </p>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      <SurgePricingComparison />
    </main>
  );
}

