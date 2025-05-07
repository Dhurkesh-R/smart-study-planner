import React from 'react';
import PlannerForm from './components/PlannerForm';
import QuizGenerator from './components/QuizGenerator';
import SessionScheduler from './components/SessionScheduler';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-center">🧑‍🎓 Smart Study Planner</h1>
        <PlannerForm />
        <QuizGenerator />
        <SessionScheduler />
      </div>
    </div>
  );
};

export default App;
// // This is the main App component that serves as the entry point for the application. It imports and renders three components: PlannerForm, QuizGenerator, and SessionScheduler. The layout is styled using Tailwind CSS classes for a clean and modern look. The app is designed to help users plan their study sessions, generate quizzes, and schedule study events.