"use client";

import { Button } from "@/components/ui/button";
import Link from "next/link";

export function CTASection() {
  return (
    <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            프로젝트 상담하기
          </h2>
          <p className="text-lg sm:text-xl text-blue-50 mb-8">
            맞춤형 솔루션으로 비즈니스 목표를 달성하세요
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link href="/contact">
              <Button size="lg" variant="outline" className="bg-white text-blue-600 hover:bg-gray-50 min-w-[200px] text-lg">
                프로젝트 상담하기
              </Button>
            </Link>
            <a href="mailto:contact@labzang.com">
              <Button size="lg" variant="ghost" className="text-white hover:bg-blue-700 min-w-[200px] text-lg border border-white/30">
                이메일 문의
              </Button>
            </a>
          </div>
          
          <p className="text-sm text-blue-100 mt-6">
            또는 크몽/토스페이먼츠 등 플랫폼을 통한 상담도 가능합니다
          </p>
        </div>
      </div>
    </section>
  );
}

