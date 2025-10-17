import React from 'react';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <footer
      id="footer"
      className="py-12"
      style={{
        background: '#ffffff',
        borderTop: '2px solid #c9a94d'
      }}
    >
      <div className="max-w-[1400px] mx-auto px-6 lg:px-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          {/* Logo and Description */}
          <div className="col-span-1">
            <img
              src="https://customer-assets.emergentagent.com/job_charm-value/artifacts/zr7y3387_image.png"
              alt="CharmTracker"
              className="h-10 w-auto mb-4"
            />
            <p className="body-small" style={{ color: '#666666' }}>
              Real market data for James Avery charm collectors.
            </p>
          </div>

          {/* Navigation Links */}
          <div className="col-span-1">
            <h4 className="heading-3 mb-4">Quick Links</h4>
            <ul className="space-y-2 list-none m-0 p-0">
              {['Home', 'How It Works', 'Market', 'Why Collectors'].map((label, index) => (
                <li key={index}>
                  <button
                    onClick={() =>
                      scrollToSection(
                        label.toLowerCase().replace(/\s+/g, '-') === 'home'
                          ? 'hero'
                          : label.toLowerCase().replace(/\s+/g, '-')
                      )
                    }
                    className="body-regular transition-smooth hover:text-[#c9a94d]"
                    style={{ color: '#666666' }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.color = '#c9a94d';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.color = '#666666';
                    }}
                  >
                    {label}
                  </button>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div className="col-span-1">
            <h4 className="heading-3 mb-4">Legal</h4>
            <ul className="space-y-2 list-none m-0 p-0">
              {['About', 'Privacy', 'Terms', 'Contact'].map((label, index) => (
                <li key={index}>
                  <a
                    href="#"
                    className="body-regular transition-smooth hover:text-[#c9a94d]"
                    style={{ color: '#666666', textDecoration: 'none' }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.color = '#c9a94d';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.color = '#666666';
                    }}
                  >
                    {label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div
          className="pt-8 text-center"
          style={{
            borderTop: '1px solid #ebeade'
          }}
        >
          <p className="body-small" style={{ color: '#666666' }}>
            &copy; {currentYear} CharmTracker. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};