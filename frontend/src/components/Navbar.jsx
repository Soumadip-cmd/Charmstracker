import React, { useState, useEffect } from 'react';
import { Menu, X } from 'lucide-react';

export const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
      setIsMobileMenuOpen(false);
    }
  };

  const navLinks = [
    { label: 'Home', id: 'hero' },
    { label: 'How It Works', id: 'how-it-works' },
    { label: 'Market', id: 'discover-market' },
    { label: 'Why Collectors', id: 'why-collectors' },
    { label: 'Contact', id: 'footer' }
  ];

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-smooth ${
        isScrolled ? 'bg-white/95 backdrop-blur-sm shadow-sm' : 'bg-white'
      }`}
      style={{ borderBottom: '1px solid #bcbcbc' }}
    >
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        <div className="flex items-center justify-between h-20">
          {/* Logo */}
          <button
            onClick={() => scrollToSection('hero')}
            className="flex items-center transition-smooth hover:opacity-75"
          >
            <img
              src="https://customer-assets.emergentagent.com/job_charm-value/artifacts/zr7y3387_image.png"
              alt="CharmTracker"
              className="h-12 w-auto"
            />
          </button>

          {/* Desktop Navigation */}
          <ul className="hidden lg:flex items-center gap-8 list-none m-0 p-0">
            {navLinks.map((link) => (
              <li key={link.id}>
                <button
                  onClick={() => scrollToSection(link.id)}
                  className="navigation-link relative text-[#333333] no-underline text-sm font-medium py-3 px-0 transition-smooth hover:text-[#c9a94d] after:content-[''] after:absolute after:bottom-2 after:left-0 after:w-0 after:h-[1px] after:bg-[#c9a94d] after:transition-slow hover:after:w-full"
                >
                  {link.label}
                </button>
              </li>
            ))}
          </ul>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="lg:hidden p-2 transition-smooth hover:bg-[#f6f5e8]"
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? (
              <X className="w-6 h-6 text-[#333333]" />
            ) : (
              <Menu className="w-6 h-6 text-[#333333]" />
            )}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="lg:hidden py-4 border-t border-[#bcbcbc]">
            <ul className="flex flex-col gap-2 list-none m-0 p-0">
              {navLinks.map((link) => (
                <li key={link.id}>
                  <button
                    onClick={() => scrollToSection(link.id)}
                    className="w-full text-left px-4 py-3 text-[#333333] text-sm font-medium transition-smooth hover:bg-[#f6f5e8] hover:text-[#c9a94d]"
                  >
                    {link.label}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </nav>
  );
};