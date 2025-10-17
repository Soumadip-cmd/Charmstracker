import "./App.css";
import { Routes, Route } from "react-router-dom";
import { Navbar } from "./components/Navbar";
import { Hero } from "./components/Hero";
import { HowItWorks } from "./components/HowItWorks";
import { DiscoverMarket } from "./components/DiscoverMarket";
import { MarketDataTable } from "./components/MarketDataTable";
import { WhyCollectors } from "./components/WhyCollectors";
import { Footer } from "./components/Footer";
import { Browse } from "./pages/Browse";
import { CharmDetail } from "./pages/CharmDetail";

// Landing Page Component
const LandingPage = () => (
  <>
    <Hero />
    <HowItWorks />
    <DiscoverMarket />
    <MarketDataTable />
    <WhyCollectors />
  </>
);

function App() {
  return (
    <div className="App">
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/browse" element={<Browse />} />
        <Route path="/charm/:id" element={<CharmDetail />} />
      </Routes>
      <Footer />
    </div>
  );
}

export default App;