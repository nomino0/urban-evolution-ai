import Aurora from '../../components/Aurora';
import { ArrowLeft, Brain, Globe, Layers, Zap } from 'lucide-react';
import Link from 'next/link';

export default function About() {
  return (
    <div className="relative w-full min-h-screen overflow-hidden bg-black text-white">
      <div className="absolute inset-0 z-0 opacity-30">
        <Aurora
          colorStops={["#00d2ff", "#3a7bd5", "#00d2ff"]}
          blend={0.5}
          amplitude={0.5}
          speed={0.2}
        />
      </div>
      
      <div className="relative z-10 container mx-auto px-6 pt-32 pb-20">
        <div className="max-w-5xl mx-auto">
          <Link href="/" className="inline-flex items-center gap-2 text-gray-400 hover:text-white mb-12 transition-colors group">
            <ArrowLeft size={20} className="group-hover:-translate-x-1 transition-transform" />
            Back to Home
          </Link>

          <div className="space-y-20">
            {/* Header */}
            <div className="text-center space-y-6">
              <h1 className="text-5xl md:text-7xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 pb-2">
                About Urban Evolution AI
              </h1>
              <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
                Empowering decision-makers with AI-driven insights to visualize, predict, and shape the future of our cities.
              </p>
            </div>

            {/* Mission Grid */}
            <div className="grid md:grid-cols-2 gap-8">
              <div className="p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 transition-colors">
                <Globe className="w-12 h-12 text-blue-400 mb-6" />
                <h3 className="text-2xl font-bold mb-4">Global Scale</h3>
                <p className="text-gray-400 leading-relaxed">
                  Analyzing satellite imagery from across the globe to understand urbanization patterns, density changes, and infrastructure development with pixel-level precision.
                </p>
              </div>
              <div className="p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 transition-colors">
                <Brain className="w-12 h-12 text-purple-400 mb-6" />
                <h3 className="text-2xl font-bold mb-4">Predictive AI</h3>
                <p className="text-gray-400 leading-relaxed">
                  Leveraging advanced deep learning models (LSTM, YOLOv11) to forecast future growth scenarios and simulate the impact of policy decisions.
                </p>
              </div>
            </div>

            {/* Technology Section */}
            <div className="relative p-10 rounded-3xl overflow-hidden border border-white/10 bg-gradient-to-br from-gray-900 to-black">
              <div className="absolute top-0 right-0 w-64 h-64 bg-blue-500/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
              
              <h2 className="text-3xl font-bold mb-8 relative z-10">Our Technology Stack</h2>
              
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 relative z-10">
                {[
                  { icon: Layers, title: "Change Detection", desc: "Sentinel-2 Multi-spectral Analysis" },
                  { icon: Zap, title: "Fast Inference", desc: "Groq LPU & Gemini Flash 2.5" },
                  { icon: Brain, title: "Deep Learning", desc: "PyTorch & TensorFlow Models" },
                  { icon: Globe, title: "Visualization", desc: "Interactive 3D WebGL Maps" },
                ].map((item, idx) => (
                  <div key={idx} className="p-6 rounded-2xl bg-white/5 border border-white/5 hover:border-white/20 transition-colors">
                    <item.icon className="w-8 h-8 text-gray-300 mb-4" />
                    <h4 className="font-bold mb-2">{item.title}</h4>
                    <p className="text-sm text-gray-500">{item.desc}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Team/Footer */}
            <div className="text-center pt-10 border-t border-white/10">
              <p className="text-gray-500">
                Built with ❤️ by the Urban Evolution AI Team.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
