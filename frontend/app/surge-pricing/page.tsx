'use client';

import Image from 'next/image';
import Link from 'next/link';
import SurgePricingComparison from '@/components/SurgePricingComparison';

export default function SurgePricingPage() {
  return (
    <main className="min-h-screen bg-black">
      {/* Header */}
      <header className="bg-black shadow-md sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-5">
              <Image 
                src="/images/honeygo-logo.png" 
                alt="HoneyGo Logo" 
                width={100} 
                height={100}
                className="rounded-lg"
              />
              <div>
                <h1 className="text-4xl font-bold text-white">
                  HoneyGo
                </h1>
                <p className="text-lg text-gray-400">
                  AI-Powered Pricing Platform
                </p>
              </div>
            </div>
            <div className="flex items-center gap-6">
              <nav className="flex items-center gap-4">
                <Link
                  href="/"
                  className="text-gray-300 hover:text-white transition-colors font-medium"
                >
                  Pricing
                </Link>
                <Link
                  href="/surge-pricing"
                  className="text-white border-b-2 border-[#FF6A13] pb-1 transition-colors font-medium"
                >
                  Surge Pricing
                </Link>
              </nav>
              <div className="text-right border-l border-gray-700 pl-6">
                <p className="text-sm text-gray-400">Powered by</p>
                <p className="text-xl font-semibold text-[#FF6A13]">
                  HoneyGo
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

