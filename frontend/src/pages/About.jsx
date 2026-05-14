import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  Network, Database, Cpu, Eye, Code, Smartphone, Globe, Shield, 
  Book, Heart, Users, ArrowRight, Zap, Lightbulb, 
  Server, Layout, Terminal, Wifi, Target, CheckCircle, Focus, Volume2
} from 'lucide-react';
import Footer from '../components/Footer';

const About = () => {
  return (
    <div className="min-h-screen bg-background relative overflow-hidden flex flex-col pt-24 font-sans text-gray-200">
      {/* Background glow effects */}
      <div className="absolute top-0 right-1/4 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[128px] pointer-events-none" />
      <div className="absolute bottom-1/4 left-1/4 w-[600px] h-[600px] bg-indigo-600/10 rounded-full blur-[150px] pointer-events-none" />

      {/* SECTION 1 — HERO SECTION */}
      <section className="max-w-6xl mx-auto px-4 py-20 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 text-primary-300 text-sm font-semibold mb-8 uppercase tracking-widest">
            <Users className="w-4 h-4" /> AI For Social Good
          </div>
          <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight leading-tight">
            Breaking Communication Barriers <br className="hidden md:block" />
            with <span className="text-transparent bg-clip-text bg-gradient-to-r from-primary via-blue-400 to-indigo-400">Artificial Intelligence</span>
          </h1>
          <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed mb-10">
            A production-ready platform leveraging neural networks and computer vision to translate American Sign Language into text and speech in real-time.
          </p>
          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link to="/translator" className="flex items-center justify-center gap-2 px-8 py-4 bg-primary text-white rounded-full font-bold hover:bg-blue-600 transition shadow-[0_0_20px_rgba(59,130,246,0.3)] hover:scale-105 duration-200">
              Experience the Tech <ArrowRight size={20} />
            </Link>
          </div>
        </motion.div>
      </section>

      {/* SECTION 2 — PROBLEM STATEMENT */}
      <section className="py-20 px-4 max-w-7xl mx-auto">
        <div className="glass-panel p-8 md:p-12 relative overflow-hidden border-red-500/20">
          <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-red-500 to-orange-500" />
          <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
            <Target className="text-red-400" /> The Communication Divide
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-4xl font-black text-red-400 mb-2">430M+</h3>
              <p className="text-gray-400 leading-relaxed">Individuals worldwide suffer from disabling hearing loss, relying heavily on visual languages.</p>
            </div>
            <div>
              <h3 className="text-4xl font-black text-orange-400 mb-2">1 in 1000</h3>
              <p className="text-gray-400 leading-relaxed">People are fluent in sign language, creating a massive dependency on human interpreters in public spaces.</p>
            </div>
            <div>
              <h3 className="text-4xl font-black text-yellow-400 mb-2">High Latency</h3>
              <p className="text-gray-400 leading-relaxed">Current digital solutions are often bulky, expensive, or lack true real-time conversational capabilities.</p>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 3 — OUR SOLUTION */}
      <section className="py-20 px-4 max-w-7xl mx-auto">
        <div className="glass-panel p-8 md:p-12 relative overflow-hidden border-green-500/20">
          <div className="absolute top-0 left-0 w-1.5 h-full bg-gradient-to-b from-green-400 to-emerald-600" />
          <div className="md:flex gap-12 items-center">
            <div className="flex-1 mb-8 md:mb-0">
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <CheckCircle className="text-green-400" /> Our Solution
              </h2>
              <p className="text-lg text-gray-300 leading-relaxed mb-6">
                We've built an AI-powered communication bridge that operates directly in the browser. Using standard webcams, the system performs <strong className="text-white">real-time sign prediction</strong>, <strong className="text-white">smart sentence generation</strong>, and <strong className="text-white">instant text-to-speech</strong>.
              </p>
              <ul className="space-y-4">
                <li className="flex items-center gap-3 text-gray-400"><Zap className="text-primary w-5 h-5"/> MediaPipe 21-point hand tracking</li>
                <li className="flex items-center gap-3 text-gray-400"><Cpu className="text-primary w-5 h-5"/> Convolutional Neural Network (CNN) Classifier</li>
                <li className="flex items-center gap-3 text-gray-400"><Volume2 className="text-primary w-5 h-5"/> Browser-native Speech Synthesis</li>
              </ul>
            </div>
            <div className="flex-1">
              <div className="aspect-video bg-black/40 rounded-xl border border-white/10 flex items-center justify-center p-6 relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-transparent" />
                <div className="text-center z-10">
                  <Focus className="w-16 h-16 text-primary mx-auto mb-4 opacity-80" />
                  <p className="text-white/60 font-mono tracking-widest text-sm">NO SPECIALIZED HARDWARE REQUIRED</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 4 — REAL-WORLD INSPIRATION */}
      <section className="py-24 px-4 bg-white/[0.02] border-y border-white/5 relative overflow-hidden">
        <div className="max-w-5xl mx-auto">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="glass-panel p-10 md:p-14 border-primary/30 relative"
          >
            <div className="absolute top-0 right-0 p-8 opacity-10">
              <Book className="w-32 h-32 text-primary" />
            </div>
            <div className="relative z-10">
              <div className="inline-flex items-center gap-2 text-primary-300 font-bold tracking-widest uppercase text-sm mb-4">
                <Lightbulb className="w-5 h-5" /> Real-World Inspiration
              </div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6 text-white">
                "Inclusive Governance in Karimnagar"
              </h2>
              <blockquote className="text-xl text-gray-300 italic border-l-4 border-primary pl-6 py-2 mb-8 leading-relaxed">
                Government officials in Karimnagar are proactively learning Indian Sign Language to improve direct communication with hearing-impaired citizens, demonstrating a massive real-world need for accessible communication in public offices.
              </blockquote>
              <p className="text-gray-400 leading-relaxed mb-6">
                This powerful initiative inspired our team. While human learning is invaluable, an AI-assisted translation system can instantly deploy this level of accessibility to <strong>every</strong> hospital, government office, and public space globally—acting as a tireless, 24/7 digital interpreter.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* SECTION 5 — OUR MISSION */}
      <section className="py-24 px-4 text-center max-w-4xl mx-auto">
        <Heart className="w-16 h-16 text-red-500 mx-auto mb-6" />
        <h2 className="text-4xl font-bold mb-6">Our Mission</h2>
        <p className="text-2xl text-gray-300 leading-relaxed font-light">
          To build AI for social good. We envision a world where the deaf community can interact seamlessly with the hearing world, free from friction, using technology that empowers rather than replaces human connection.
        </p>
      </section>

      {/* SECTION 6 — AI WORKFLOW */}
      <section className="py-20 px-4 bg-black/30">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">The AI Architecture Workflow</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-4 items-center">
            <WorkflowNode icon={<Eye />} title="Webcam Feed" />
            <WorkflowArrow />
            <WorkflowNode icon={<Focus />} title="MediaPipe Tracking" />
            <WorkflowArrow />
            <WorkflowNode icon={<Network />} title="Skeleton Render" />
            <WorkflowArrow />
            <WorkflowNode icon={<Cpu />} title="CNN Classification" />
            <WorkflowArrow />
            <WorkflowNode icon={<Shield />} title="Stabilization" />
            <WorkflowArrow />
            <WorkflowNode icon={<Book />} title="NLP Correction" />
            <WorkflowArrow />
            <WorkflowNode icon={<Volume2 />} title="Text-to-Speech" />
          </div>
        </div>
      </section>

      {/* SECTION 7 — TECH STACK */}
      <section className="py-24 px-4 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-16">Production Tech Stack</h2>
        <div className="grid md:grid-cols-3 gap-8">
          {/* Frontend */}
          <div className="glass-panel p-8 hover:border-blue-500/50 transition-colors duration-300">
            <Layout className="w-10 h-10 text-blue-400 mb-6" />
            <h3 className="text-2xl font-bold mb-4 text-white">Frontend</h3>
            <ul className="space-y-3 text-gray-400">
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-blue-500"/> React.js & Vite</li>
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-blue-500"/> Tailwind CSS</li>
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-blue-500"/> Framer Motion</li>
            </ul>
          </div>
          {/* Backend */}
          <div className="glass-panel p-8 hover:border-green-500/50 transition-colors duration-300">
            <Server className="w-10 h-10 text-green-400 mb-6" />
            <h3 className="text-2xl font-bold mb-4 text-white">Backend Proxy</h3>
            <ul className="space-y-3 text-gray-400">
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-green-500"/> Node.js & Express</li>
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-green-500"/> MongoDB (Mongoose)</li>
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-green-500"/> JWT Authentication</li>
            </ul>
          </div>
          {/* AI Core */}
          <div className="glass-panel p-8 hover:border-orange-500/50 transition-colors duration-300">
            <Terminal className="w-10 h-10 text-orange-400 mb-6" />
            <h3 className="text-2xl font-bold mb-4 text-white">AI Engine</h3>
            <ul className="space-y-3 text-gray-400">
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-orange-500"/> Python Flask API</li>
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-orange-500"/> TensorFlow / Keras</li>
              <li className="flex items-center gap-2"><CheckCircle className="w-4 h-4 text-orange-500"/> OpenCV & MediaPipe</li>
            </ul>
          </div>
        </div>
      </section>

      {/* SECTION 8 — KEY FEATURES */}
      <section className="py-20 px-4 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">Core Platform Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard title="Real-Time Recognition" desc="Processes webcam frames instantly to detect hand gestures without lag." />
            <FeatureCard title="AI Sentence Generation" desc="Intelligently builds cohesive sentences from individual character predictions." />
            <FeatureCard title="Live Skeleton Render" desc="Provides real-time visual feedback of the extracted hand landmarks." />
            <FeatureCard title="NLP Word Correction" desc="PyEnchant-powered engine auto-suggests corrections for misspelled words." />
            <FeatureCard title="Instant Text-To-Speech" desc="Converts generated sentences into audible speech for the hearing world." />
            <FeatureCard title="Stateless Architecture" desc="Bulletproof API design ensuring multiple users don't cross-contaminate predictions." />
          </div>
        </div>
      </section>

      {/* SECTION 9 — WHY MEDIAPIPE + CNN? */}
      <section className="py-24 px-4 max-w-5xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Technical Deep Dive: MediaPipe + CNN</h2>
          <p className="text-gray-400">Why we didn't just throw raw images into a neural network.</p>
        </div>
        <div className="glass-panel p-8 md:p-12">
          <div className="space-y-8 text-gray-300 leading-relaxed">
            <p>
              Directly feeding raw RGB webcam frames into a CNN introduces massive variance: different lighting, skin tones, backgrounds, and camera angles heavily degrade accuracy.
            </p>
            <p>
              <strong>The Solution:</strong> We use Google's <span className="text-primary font-bold">MediaPipe</span> as a highly optimized feature extractor. It instantly locates the hand and outputs 21 precise 3D (x, y, z) landmarks. 
            </p>
            <p>
              We then render these 21 landmarks as a clean, standardized "white skeleton on black background" image. By feeding <em>this isolated skeleton</em> into our <span className="text-primary font-bold">Convolutional Neural Network (CNN)</span>, we eliminate environmental noise entirely. This combination achieves incredibly high prediction accuracy while requiring a fraction of the computational power of a standard vision model.
            </p>
            <div className="bg-black/50 p-6 rounded-lg border border-white/5 flex flex-col md:flex-row items-center gap-6 mt-8">
              <div className="flex-1 text-center font-mono text-sm text-gray-500">RAW WEBCAM (NOISY)</div>
              <ArrowRight className="text-primary hidden md:block" />
              <div className="flex-1 text-center font-mono text-sm text-primary">MEDIAPIPE SKELETON (CLEAN)</div>
              <ArrowRight className="text-primary hidden md:block" />
              <div className="flex-1 text-center font-mono text-sm text-green-400">CNN PREDICTION (ACCURATE)</div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 10 — SOCIAL IMPACT */}
      <section className="py-24 px-4 bg-primary/5 border-y border-primary/10">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-12">Real-World Social Impact</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <ImpactNode icon={<Book />} title="Education" desc="Empowering deaf students in mainstream classrooms." />
            <ImpactNode icon={<Target />} title="Government" desc="Enabling inclusive communication in public offices." />
            <ImpactNode icon={<Heart />} title="Healthcare" desc="Facilitating direct patient-doctor dialogue." />
            <ImpactNode icon={<Users />} title="Customer Service" desc="Breaking barriers at retail and help desks." />
          </div>
        </div>
      </section>

      {/* SECTION 11 — TEAM MEMBERS */}
      <section className="py-24 px-4 max-w-7xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-16">Meet the Team</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
          <TeamMemberCard role="AI/ML Development" desc="Architecting CNN models and training the core gesture inference pipeline." />
          <TeamMemberCard role="Frontend Development" desc="Building the React UI, Framer Motion animations, and routing logic." />
          <TeamMemberCard role="Backend Development" desc="Developing the stateless Node.js proxy and secure MongoDB authentication." />
          <TeamMemberCard role="MediaPipe Integration" desc="Optimizing the 21-point hand tracking and skeleton normalization engine." />
          <TeamMemberCard role="UI/UX Design" desc="Designing the glassmorphism aesthetic and ensuring an accessible user experience." />
        </div>
      </section>

      {/* SECTION 12 — FUTURE ENHANCEMENTS */}
      <section className="py-24 px-4 bg-white/[0.02] border-y border-white/5">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">The Future Roadmap</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            <RoadmapCard icon={<Wifi />} title="WebSocket Streaming" desc="Moving from HTTP polling to persistent WebSockets for 30+ FPS tracking." />
            <RoadmapCard icon={<Network />} title="LSTM Transformers" desc="Transitioning from static CNNs to recurrent models for fluid, continuous signing." />
            <RoadmapCard icon={<Globe />} title="Multilingual NLP" desc="Expanding beyond ASL to support Indian (ISL) and British (BSL) sign languages." />
            <RoadmapCard icon={<Smartphone />} title="Mobile Native App" desc="Porting the engine to React Native for pocket-sized accessibility." />
          </div>
        </div>
      </section>

      {/* SECTION 13 — CTA SECTION */}
      <section className="py-24 px-4 text-center">
        <div className="max-w-4xl mx-auto glass-panel p-16 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-tr from-primary/20 via-transparent to-indigo-500/20" />
          <div className="relative z-10">
            <h2 className="text-4xl font-black mb-6 text-white">Join the Accessibility Revolution.</h2>
            <p className="text-xl text-gray-300 mb-10">
              Experience the power of real-time AI sign language translation today.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link to="/translator" className="px-8 py-4 bg-primary text-white rounded-full font-bold hover:bg-blue-600 transition shadow-[0_0_20px_rgba(59,130,246,0.4)]">
                Try Live Translator
              </Link>
              <Link to="/signup" className="px-8 py-4 bg-white/5 border border-white/20 text-white rounded-full font-bold hover:bg-white/10 transition">
                Create Free Account
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 14 — FOOTER */}
      <Footer />
    </div>
  );
};

/* Sub-components */
const WorkflowNode = ({ icon, title }) => (
  <div className="flex flex-col items-center col-span-2 lg:col-span-1 text-center p-4">
    <div className="w-16 h-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center text-primary mb-4 shadow-lg shadow-primary/5">
      {icon}
    </div>
    <span className="text-sm font-semibold text-gray-300">{title}</span>
  </div>
);

const WorkflowArrow = () => (
  <div className="hidden lg:flex items-center justify-center col-span-1 text-gray-600">
    <ArrowRight />
  </div>
);

const FeatureCard = ({ title, desc }) => (
  <div className="glass-panel p-6 border-white/5 hover:border-primary/30 transition-colors">
    <h4 className="text-lg font-bold text-white mb-2">{title}</h4>
    <p className="text-sm text-gray-400 leading-relaxed">{desc}</p>
  </div>
);

const ImpactNode = ({ icon, title, desc }) => (
  <div className="text-center">
    <div className="w-16 h-16 mx-auto rounded-full bg-primary/20 flex items-center justify-center text-primary mb-6">
      {icon}
    </div>
    <h4 className="text-xl font-bold text-white mb-3">{title}</h4>
    <p className="text-gray-400 text-sm leading-relaxed">{desc}</p>
  </div>
);

const RoadmapCard = ({ icon, title, desc }) => (
  <div className="glass-panel p-8 border-t-4 border-t-primary/50 bg-black/20">
    <div className="text-primary mb-4">{icon}</div>
    <h4 className="text-lg font-bold text-white mb-3">{title}</h4>
    <p className="text-sm text-gray-400">{desc}</p>
  </div>
);

const TeamMemberCard = ({ role, desc }) => (
  <motion.div 
    whileHover={{ y: -10 }}
    className="glass-panel p-6 text-center border-white/10 hover:border-primary/50 transition-colors flex flex-col items-center"
  >
    <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-primary to-indigo-500 p-1 mb-6 shrink-0">
      <div className="w-full h-full rounded-full bg-background flex items-center justify-center overflow-hidden">
        <Users className="w-8 h-8 text-gray-500" />
      </div>
    </div>
    <h3 className="text-lg font-bold text-white mb-1">Team Member</h3>
    <p className="text-primary-400 font-medium text-sm mb-4 leading-snug">{role}</p>
    <p className="text-gray-400 text-xs leading-relaxed mb-6 flex-grow">
      {desc}
    </p>
    <div className="flex justify-center gap-3 mt-auto">
      <div className="w-7 h-7 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 cursor-pointer text-xs transition">in</div>
      <div className="w-7 h-7 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 cursor-pointer text-xs transition">gh</div>
    </div>
  </motion.div>
);

export default About;
