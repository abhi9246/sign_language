import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight, Bot, Zap, Globe, Camera, Focus, FileText, Volume2, Shield, Heart } from 'lucide-react';
import Footer from '../components/Footer';

const Landing = () => {
  return (
    <div className="min-h-screen bg-background relative overflow-hidden flex flex-col">
      {/* Background glow effects */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[128px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[128px] pointer-events-none" />

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center max-w-5xl mx-auto"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-primary-300 text-sm font-medium mb-8">
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse"></span>
            Real-Time Translation Engine v2.0
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8 leading-tight">
            AI-Powered Real-Time <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-blue-400 to-indigo-400">
              Sign Language Translator
            </span>
          </h1>
          <p className="text-xl text-gray-400 mb-10 max-w-3xl mx-auto leading-relaxed">
            Break down communication barriers instantly. Our advanced neural networks translate American Sign Language into text and speech directly from your webcam, ensuring accessibility for everyone.
          </p>
          
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link to="/translator" className="flex items-center gap-2 px-8 py-4 bg-primary text-white rounded-full font-semibold hover:bg-blue-600 transition shadow-[0_0_20px_rgba(59,130,246,0.4)] hover:shadow-[0_0_30px_rgba(59,130,246,0.6)] hover:scale-105 duration-200">
              Start Translating <ArrowRight size={20} />
            </Link>
            <Link to="/about" className="px-8 py-4 bg-white/5 border border-white/10 text-white rounded-full font-semibold hover:bg-white/10 transition">
              Learn More
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Live Demo Preview Section */}
      <section className="py-12 px-4 max-w-7xl mx-auto w-full">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="glass-panel p-4 md:p-8 relative overflow-hidden"
        >
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-indigo-500" />
          <div className="flex flex-col md:flex-row gap-6">
            <div className="flex-1 bg-black/50 rounded-xl aspect-video relative flex items-center justify-center border border-white/5">
              <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1620619560416-2eb962f99a5e?q=80&w=640&auto=format&fit=crop')] bg-cover bg-center opacity-40 blur-[2px]" />
              <div className="z-10 text-center">
                <Camera className="w-12 h-12 text-white/50 mx-auto mb-2" />
                <p className="text-white/70 font-medium">Live Webcam Feed</p>
              </div>
              <div className="absolute top-4 left-4 bg-black/60 px-3 py-1 rounded text-xs text-white flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" /> REC
              </div>
            </div>
            
            <div className="flex-1 flex flex-col gap-6">
              <div className="bg-black/30 rounded-xl p-6 border border-white/5 flex-1 flex flex-col justify-center items-center">
                <p className="text-sm text-gray-500 uppercase tracking-widest mb-2">AI Detection</p>
                <div className="text-6xl font-black text-white">HELLO</div>
              </div>
              <div className="bg-black/30 rounded-xl p-6 border border-white/5">
                <p className="text-sm text-gray-500 uppercase tracking-widest mb-2 flex justify-between">
                  <span>Generated Sentence</span>
                  <Volume2 className="w-4 h-4 text-primary" />
                </p>
                <p className="font-mono text-xl text-blue-300">HELLO WORLD_</p>
                <div className="flex gap-2 mt-4">
                  <span className="px-3 py-1 bg-primary/20 text-primary-300 rounded-full text-xs">HELLO</span>
                  <span className="px-3 py-1 bg-primary/20 text-primary-300 rounded-full text-xs">HELP</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-24 px-4 max-w-7xl mx-auto w-full">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Cutting-Edge Capabilities</h2>
          <p className="text-gray-400 max-w-2xl mx-auto">Our platform combines multiple AI models to deliver a seamless, accessible translation experience.</p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-6">
          <FeatureCard 
            icon={<Focus className="w-8 h-8 text-primary"/>}
            title="Real-Time Detection"
            desc="Web-optimized MediaPipe tracking captures 21 hand landmarks instantly with ultra-low latency."
          />
          <FeatureCard 
            icon={<Bot className="w-8 h-8 text-blue-400"/>}
            title="CNN Prediction"
            desc="A highly optimized Convolutional Neural Network decodes hand geometries into text characters."
          />
          <FeatureCard 
            icon={<FileText className="w-8 h-8 text-indigo-400"/>}
            title="Smart Auto-Correct"
            desc="Built-in pyenchant dictionaries provide live autocomplete suggestions for misspelled words."
          />
          <FeatureCard 
            icon={<Volume2 className="w-8 h-8 text-purple-400"/>}
            title="Text-to-Speech"
            desc="Synthesize your generated sentences into clear, audible speech at the click of a button."
          />
          <FeatureCard 
            icon={<Shield className="w-8 h-8 text-green-400"/>}
            title="Secure Accounts"
            desc="Save your translated sentences to a secure dashboard history for future reference."
          />
          <FeatureCard 
            icon={<Zap className="w-8 h-8 text-yellow-400"/>}
            title="Stateless API"
            desc="Robust backend architecture ensuring high stability and zero prediction bleeding between requests."
          />
        </div>
      </section>

      {/* How It Works (Workflow) */}
      <section className="py-24 px-4 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">How The AI Works</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">A look under the hood at our translation pipeline.</p>
          </div>
          
          <div className="flex flex-col md:flex-row justify-between items-center gap-4 relative">
            {/* Connecting Line */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-0.5 bg-gradient-to-r from-primary/10 via-primary/50 to-primary/10 -z-10" />
            
            <WorkflowStep num="1" title="Capture" desc="Webcam Feed" />
            <WorkflowStep num="2" title="Track" desc="MediaPipe Skeleton" />
            <WorkflowStep num="3" title="Analyze" desc="CNN Inference" />
            <WorkflowStep num="4" title="Correct" desc="Language NLP" />
            <WorkflowStep num="5" title="Output" desc="Speech & Text" />
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-24 px-4 max-w-7xl mx-auto w-full text-center">
        <div className="inline-flex items-center justify-center p-4 bg-primary/10 rounded-full mb-6">
          <Heart className="w-10 h-10 text-primary" />
        </div>
        <h2 className="text-3xl md:text-4xl font-bold mb-6">Empowering Accessibility</h2>
        <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed mb-12">
          We believe communication is a fundamental human right. Gesture Bridge AI bridges the gap between the deaf community and the hearing world, providing an educational, scalable, and instant translation solution.
        </p>
      </section>

      {/* CTA Section */}
      <section className="py-24 px-4">
        <div className="max-w-5xl mx-auto glass-panel p-12 text-center relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-indigo-600/20" />
          <div className="relative z-10">
            <h2 className="text-4xl font-bold mb-6">Ready to break the silence?</h2>
            <p className="text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
              Join us in making communication universal. Try the live translator instantly from your browser.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/translator" className="px-8 py-4 bg-white text-background rounded-full font-bold hover:bg-gray-200 transition shadow-xl hover:scale-105 duration-200">
                Try Live Translation
              </Link>
              <Link to="/signup" className="px-8 py-4 bg-transparent border border-white/20 text-white rounded-full font-semibold hover:bg-white/10 transition">
                Create Account
              </Link>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
};

const FeatureCard = ({ icon, title, desc }) => (
  <motion.div 
    whileHover={{ y: -5 }}
    className="glass-panel p-8 bg-white/[0.02] border-white/5 hover:border-white/20 transition-colors"
  >
    <div className="mb-6 p-3 bg-white/5 rounded-xl inline-block">{icon}</div>
    <h3 className="text-xl font-bold mb-3">{title}</h3>
    <p className="text-gray-400 leading-relaxed">{desc}</p>
  </motion.div>
);

const WorkflowStep = ({ num, title, desc }) => (
  <div className="flex flex-col items-center bg-background p-4 rounded-xl">
    <div className="w-12 h-12 rounded-full bg-primary/20 border border-primary text-primary flex items-center justify-center font-bold text-xl mb-4 shadow-[0_0_15px_rgba(59,130,246,0.3)]">
      {num}
    </div>
    <h4 className="font-bold text-white mb-1">{title}</h4>
    <p className="text-sm text-gray-500">{desc}</p>
  </div>
);

export default Landing;
