import { HeroSection } from "@/components/sections/hero-section";
import { StrengthSection } from "@/components/sections/strength-section";
import { ServicesSection } from "@/components/sections/services-section";
import { ProcessSection } from "@/components/sections/process-section";
import { CTASection } from "@/components/sections/cta-section";

export default function Home() {
  return (
    <main className="min-h-screen">
      <HeroSection />
      <StrengthSection />
      <ServicesSection />
      <ProcessSection />
      <CTASection />
    </main>
  );
}
