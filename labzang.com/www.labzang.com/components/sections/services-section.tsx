"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const services = [
  {
    title: "웹사이트 개발",
    description: "기업/포트폴리오/예약/커머스 등 다양한 웹사이트 개발",
    icon: "🌐",
  },
  {
    title: "앱 개발",
    description: "Flutter 기반 Android/iOS 크로스 플랫폼 앱 개발",
    icon: "📱",
  },
  {
    title: "관리자 대시보드",
    description: "FastAPI + Next.js 기반의 효율적인 관리 시스템 구축",
    icon: "📊",
  },
  {
    title: "AI 기능 탑재",
    description: "RAG, 자동요약, 데이터 분석 등 AI 기능 통합",
    icon: "🤖",
  },
  {
    title: "MSA 기반 서비스",
    description: "마이크로서비스 아키텍처 기반 확장 가능한 시스템 구축",
    icon: "🏗️",
  },
  {
    title: "유지보수/기능추가",
    description: "배포 후 지속적인 유지보수 및 기능 개선 서비스",
    icon: "🔧",
  },
];

export function ServicesSection() {
  return (
    <section className="py-20 bg-gray-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            제공 서비스
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            웹·앱 개발부터 AI 통합까지 다양한 서비스를 제공합니다
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {services.map((service, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="text-4xl mb-4">{service.icon}</div>
                <CardTitle>{service.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  {service.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

