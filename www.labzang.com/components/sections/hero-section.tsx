"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

export function HeroSection() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-purple-50 -z-10" />
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#8080800a_1px,transparent_1px),linear-gradient(to_bottom,#8080800a_1px,transparent_1px)] bg-[size:14px_24px] -z-10" />
      
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 text-center z-10">
        <div className="max-w-4xl mx-auto space-y-8">
          {/* Main Message */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 leading-tight">
            맞춤형 웹·앱 개발
            <br />
            <span className="text-blue-600">1인 개발 전문 Labzang</span>
          </h1>
          
          {/* Sub Message */}
          <p className="text-xl sm:text-2xl text-gray-600 font-medium">
            FastAPI · Next.js · AI 기반 시스템 개발
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
            <Link href="/portfolio">
              <Button size="lg" className="w-full sm:w-auto min-w-[200px] text-lg">
                포트폴리오 보기
              </Button>
            </Link>
            <Link href="/contact">
              <Button size="lg" variant="outline" className="w-full sm:w-auto min-w-[200px] text-lg">
                프로젝트 상담하기
              </Button>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}

