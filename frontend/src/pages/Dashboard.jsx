import { useState, useContext, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { historyAPI } from '../api';
import { Trash2, Clock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const { user } = useContext(AuthContext);
  const navigate = useNavigate();
  const [history, setHistory] = useState([]);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }
    fetchHistory();
  }, [user]);

  const fetchHistory = async () => {
    try {
      const res = await historyAPI.getHistory();
      setHistory(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await historyAPI.deleteRecord(id);
      setHistory(history.filter(h => h._id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  if (!user) return null;

  return (
    <div className="min-h-screen pt-24 px-4 pb-12 max-w-4xl mx-auto">
      <div className="glass-panel p-8 mb-8 flex items-center gap-6">
        <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-primary to-blue-300 flex items-center justify-center text-3xl font-bold text-white shadow-lg">
          {user.username.charAt(0).toUpperCase()}
        </div>
        <div>
          <h1 className="text-3xl font-bold mb-1">Welcome back, {user.username}</h1>
          <p className="text-gray-400">{user.email}</p>
        </div>
      </div>

      <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
        <Clock className="text-primary" /> Saved Translations
      </h2>
      
      <div className="flex flex-col gap-4">
        {history.length === 0 ? (
          <div className="glass-panel p-8 text-center text-gray-500">
            No saved translations yet. Head over to the Translator to get started!
          </div>
        ) : (
          history.map((record) => (
            <div key={record._id} className="glass-panel p-6 flex justify-between items-center group">
              <div>
                <p className="text-lg font-mono mb-2">{record.sentence}</p>
                <p className="text-xs text-gray-500">{new Date(record.createdAt).toLocaleString()}</p>
              </div>
              <button 
                onClick={() => handleDelete(record._id)}
                className="p-2 text-red-500/50 hover:text-red-400 hover:bg-red-500/10 rounded transition opacity-0 group-hover:opacity-100"
              >
                <Trash2 size={20} />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;
