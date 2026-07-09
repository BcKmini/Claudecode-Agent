<script setup>
import NavBar from './components/NavBar.vue'
import HeroSection from './components/HeroSection.vue'
import StatsSection from './components/StatsSection.vue'
import PipelineSection from './components/PipelineSection.vue'
import AgentsSection from './components/AgentsSection.vue'
import ToolsSection from './components/ToolsSection.vue'
import QuickStartSection from './components/QuickStartSection.vue'
import FooterSection from './components/FooterSection.vue'
</script>

<template>
  <div class="bg-glow" aria-hidden="true"></div>
  <NavBar />
  <main>
    <HeroSection />
    <StatsSection />
    <PipelineSection />
    <AgentsSection />
    <ToolsSection />
    <QuickStartSection />
  </main>
  <FooterSection />
</template>

<style scoped>
.bg-glow {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: -1;
  background:
    radial-gradient(ellipse 60% 40% at 50% -5%, rgba(217, 119, 87, 0.13), transparent 65%),
    radial-gradient(ellipse 45% 35% at 88% 42%, rgba(192, 132, 252, 0.06), transparent 60%),
    radial-gradient(ellipse 50% 40% at 8% 78%, rgba(217, 119, 87, 0.05), transparent 60%);
}
</style>
