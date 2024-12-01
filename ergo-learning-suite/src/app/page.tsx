'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Brain, FileQuestion, Globe, Book, ChevronRight, ExternalLink } from 'lucide-react'

export default function ErgoEnhancedPoster() {
  const [activeCard, setActiveCard] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveCard((prev) => (prev + 1) % apps.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  const apps = [
    {
      icon: <FileQuestion className="w-20 h-20 text-yellow-300" />,
      title: "MCQ Maestro",
      description: "Generate tailored multiple-choice questions for any topic.",
      color: "from-yellow-400 to-orange-500",
      url: "https://your-streamlit-app-1.com",
    },
    {
      icon: <Globe className="w-20 h-20 text-cyan-300" />,
      title: "Web Insight Engine",
      description: "Scrape and synthesize cutting-edge information on any subject.",
      color: "from-cyan-400 to-blue-500",
      url: "https://your-streamlit-app-2.com",
    },
    {
      icon: <Brain className="w-20 h-20 text-fuchsia-300" />,
      title: "Memory Vault",
      description: "Store, summarize, and recall study materials with ease.",
      color: "from-fuchsia-400 to-purple-500",
      url: "https://your-streamlit-app-3.com",
    },
    {
      icon: <Book className="w-20 h-20 text-emerald-300" />,
      title: "RAG Scholar",
      description: "Access AI-powered, textbook-quality answers instantly.",
      color: "from-emerald-400 to-green-500",
      url: "https://your-streamlit-app-4.com",
    },
  ]

  return (
    <div className="bg-gray-900 text-white min-h-screen flex flex-col justify-between p-8 overflow-hidden relative">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-[url('/placeholder.svg?height=1080&width=1920')] opacity-10 bg-cover bg-center" />
      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 via-purple-500/20 to-pink-500/20" />

      {/* Header */}
      <header className="text-center mb-12 relative z-10">
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ duration: 0.8, type: "spring" }}
          className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full w-32 h-32 mx-auto mb-6 flex items-center justify-center"
        >
          <span className="text-5xl font-bold">ERGO</span>
        </motion.div>
        <motion.h1
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-6xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400"
        >
          ERGO Learning Suite
        </motion.h1>
        <motion.p
          initial={{ y: 50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.5 }}
          className="text-2xl text-gray-300 mt-4 max-w-3xl mx-auto"
        >
          Revolutionize Your Learning Journey with AI-Powered Educational Tools
        </motion.p>
      </header>

      {/* Main Content */}
      <main className="flex-grow flex items-center justify-center relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-6xl w-full">
          <AnimatePresence>
            {apps.map((app, index) => (
              <AppCard
                key={index}
                {...app}
                isActive={index === activeCard}
                onClick={() => setActiveCard(index)}
              />
            ))}
          </AnimatePresence>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center mt-12 relative z-10">
        <p className="text-gray-300 mb-6 text-xl max-w-3xl mx-auto">
          Empower your learning experience with ERGO's suite of AI-driven educational tools. 
          Unlock your potential and master any subject with unprecedented efficiency.
        </p>
        <motion.a
          href="https://your-main-streamlit-app.com"
          target="_blank"
          rel="noopener noreferrer"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="inline-block bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 text-white font-bold py-4 px-10 rounded-full text-xl hover:shadow-lg transition duration-300"
        >
          Launch ERGO Suite <ChevronRight className="inline-block ml-2" />
        </motion.a>
      </footer>
    </div>
  )
}

function AppCard({ icon, title, description, color, isActive, onClick, url }: { icon: React.ReactNode, title: string, description: string, color: string, isActive: boolean, onClick: () => void, url: string }) {
  return (
    <motion.div
      layout
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.8 }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={onClick}
      className={`bg-gradient-to-br ${color} rounded-3xl shadow-2xl p-8 cursor-pointer transition-all duration-300 transform ${
        isActive ? 'ring-4 ring-white scale-105' : ''
      }`}
    >
      <div className="flex flex-col items-center mb-6">
        {icon}
        <h2 className="text-3xl font-bold mt-4 text-center">{title}</h2>
      </div>
      <p className="text-lg text-center mb-6">{description}</p>
      <motion.a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="block w-full bg-white/20 hover:bg-white/30 text-white font-semibold py-2 px-4 rounded-full text-center transition duration-300"
      >
        Launch App <ExternalLink className="inline-block ml-2 w-4 h-4" />
      </motion.a>
    </motion.div>
  )
}
