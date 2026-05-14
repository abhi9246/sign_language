import { Link, useNavigate } from 'react-router-dom';
import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { HandMetal } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="fixed w-full z-50 glass-panel border-x-0 border-t-0 rounded-none bg-background/50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="flex items-center space-x-2">
            <HandMetal className="w-8 h-8 text-primary" />
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-blue-300">
              Gesture Bridge AI
            </span>
          </Link>
          
          <div className="flex items-center space-x-6">
            <div className="hidden md:flex space-x-6 mr-4">
              <Link to="/" className="text-sm font-medium text-gray-300 hover:text-white transition">Home</Link>
              <Link to="/about" className="text-sm font-medium text-gray-300 hover:text-white transition">About</Link>
            </div>
            
            {user ? (
              <>
                <Link to="/translator" className="text-gray-300 hover:text-white transition">Translator</Link>
                <Link to="/dashboard" className="text-gray-300 hover:text-white transition">Dashboard</Link>
                <button 
                  onClick={handleLogout}
                  className="px-4 py-2 text-sm font-medium text-white bg-secondary border border-white/10 rounded-md hover:bg-white/10 transition"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-300 hover:text-white transition">Log in</Link>
                <Link to="/signup" className="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:bg-blue-600 transition shadow-[0_0_15px_rgba(59,130,246,0.5)]">
                  Sign up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
