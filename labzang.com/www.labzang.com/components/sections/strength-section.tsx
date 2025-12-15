"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const strengths = [
  {
    title: "100% 직접 개발",
    description: "기획부터 배포까지 대표가 직접 개발하여 빠른 의사결정과 품질 관리가 가능합니다.",
    icon: "👨‍💻",
  },
  {
    title: "빠른 커뮤니케이션",
    description: "매일 피드백 & 빠른 대응으로 프로젝트 진행 상황을 실시간으로 공유합니다.",
    icon: "⚡",
  },
  {
    title: "완전한 커스터마이징",
    description: "고객의 요구사항을 기반으로 완전히 맞춤형 솔루션을 제공합니다.",
    icon: "🎨",
  },
];

export function StrengthSection() {
  return (
    <section className="py-20 bg-white">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-4">
            나의 강점
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            프리랜서 개발자로서의 전문성과 장점
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 lg:gap-8">
          {strengths.map((strength, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="text-5xl mb-4">{strength.icon}</div>
                <CardTitle>{strength.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base">
                  {strength.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}

