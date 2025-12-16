"use client";

import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";

const processes = [
  {
    step: 1,
    title: "상담 및 요구사항 분석",
    description: "프로젝트 목표와 요구사항을 상세히 파악합니다",
  },
  {
    step: 2,
    title: "기획/와이어프레임",
    description: "사용자 경험을 고려한 구조 설계 및 화면 구성",
  },
  {
    step: 3,
    title: "디자인 협의",
    description: "브랜드 아이덴티티에 맞는 디자인 컨셉 확정",
  },
  {
    step: 4,
    title: "개발",
    description: "최신 기술 스택을 활용한 안정적인 개발",
  },
  {
    step: 5,
    title: "테스트",
    description: "체계적인 QA를 통한 품질 보장",
  },
  {
    step: 6,
    title: "배포 및 유지보수",
    description: "배포 후 지속적인 모니터링 및 지원",
  },
];

export function ProcessSection() {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            개발 프로세스
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            체계적인 6단계 프로세스로 고품질 결과물을 제공합니다
          </p>
        </div>
        
        <div className="max-w-5xl mx-auto">
          {/* Desktop: 3 columns grid */}
          <div className="hidden md:grid md:grid-cols-3 gap-6 lg:gap-8">
            {processes.map((process, index) => (
              <div key={index} className="flex flex-col items-center text-center">
                <Badge className="mb-4 text-sm px-4 py-2">
                  STEP {process.step}
                </Badge>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {process.title}
                </h3>
                <p className="text-gray-600 text-sm">
                  {process.description}
                </p>
              </div>
            ))}
          </div>
          
          {/* Mobile: Vertical Timeline */}
          <div className="md:hidden space-y-6">
            {processes.map((process, index) => (
              <div key={index} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-sm">
                    {process.step}
                  </div>
                  {index < processes.length - 1 && (
                    <Separator orientation="vertical" className="h-16 my-2" />
                  )}
                </div>
                <div className="flex-1 pb-2">
                  <Badge className="mb-2 text-xs">
                    STEP {process.step}
                  </Badge>
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">
                    {process.title}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {process.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

