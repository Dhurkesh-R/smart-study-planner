import React, { useState } from 'react';
import { generateQuiz } from '../api';

const QuizGenerator = () => {
  const [topic, setTopic] = useState('');
  const [question, setQuestion] = useState('');

  const handleGenerate = async () => {
    const res = await generateQuiz(topic);
    setQuestion(res.data.question);
  };

  const handleGenerateAgain = async () => {
    if (!topic) return;
    try {
      const response = await fetch("http://localhost:5000/generate-quiz", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic })
      });
      const data = await response.json();
      setQuestion(data.question); // ✅ fixed from setQuiz
    } catch (err) {
      console.error("Failed to fetch quiz:", err);
    }
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg mt-6">
      <h2 className="text-xl font-semibold mb-4">🧠 Generate Quiz</h2>
      <input
        className="w-full p-2 border border-gray-300 rounded mb-2"
        placeholder="Topic"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
      />
      <button
        onClick={handleGenerate}
        className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700"
      >
        Generate
      </button>

      {question && (
        <>
          <pre className="mt-4 p-3 bg-gray-100 rounded border border-gray-300 whitespace-pre-wrap">
            {question}
          </pre>
          <button
            onClick={handleGenerateAgain}
            className="mt-2 px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700"
          >
            🎡Generate Another Quiz
          </button>
        </>
      )}
    </div>
  );
};

export default QuizGenerator;
// This component allows users to input a topic and generate a quiz question based on that topic. It uses the `generateQuiz` API function to send the topic to the backend and display the generated question. The input field is styled, and the generated question is displayed in a styled box below the button.