import { Link } from 'react-router-dom';
import { Github, Twitter, Linkedin, HandMetal } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="border-t border-white/10 bg-background/50 backdrop-blur-lg mt-24">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2">
            <Link to="/" className="flex items-center space-x-2 mb-4">
              <HandMetal className="w-6 h-6 text-primary" />
              <span className="text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-300">
                Gesture Bridge AI
              </span>
            </Link>
            <p className="text-gray-400 max-w-sm mb-6 leading-relaxed">
              Decoding the unspoken through real-time AI. We are building the future of accessible communication with advanced neural networks and seamless web interfaces.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-primary transition">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-400 transition">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="text-gray-400 hover:text-blue-500 transition">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
          
          <div>
            <h3 className="text-white font-semibold mb-4 tracking-wider uppercase text-sm">Product</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/translator" className="text-gray-400 hover:text-white transition">Live Translator</Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-gray-400 hover:text-white transition">Dashboard</Link>
              </li>
              <li>
                <Link to="/about" className="text-gray-400 hover:text-white transition">How it works</Link>
              </li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-white font-semibold mb-4 tracking-wider uppercase text-sm">Company</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/about" className="text-gray-400 hover:text-white transition">About Us</Link>
              </li>
              <li>
                <Link to="#" className="text-gray-400 hover:text-white transition">Privacy Policy</Link>
              </li>
              <li>
                <Link to="#" className="text-gray-400 hover:text-white transition">Terms of Service</Link>
              </li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-white/10 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} Gesture Bridge AI. All rights reserved.
          </p>
          <div className="flex space-x-4 mt-4 md:mt-0 text-sm text-gray-500">
            <span>Made with 💙 for Accessibility</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
