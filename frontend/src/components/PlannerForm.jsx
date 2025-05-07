import React, { useState } from 'react';
import { predictNextSession } from '../api';

const PlannerForm = () => {
  const [formData, setFormData] = useState({
    subject: '',
    time_spent: '',
    recall_score: ''
  });
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await predictNextSession(formData);
      setResult(res.data);
    } catch (err) {
      alert(err.response?.data?.error || 'Something went wrong');
    }
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg">
      <h2 className="text-xl font-semibold mb-4">📅 Predict Next Study Session</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input name="subject" className="w-full p-2 border border-gray-300 rounded" placeholder="Subject" onChange={handleChange} />
        <input name="time_spent" type="number" className="w-full p-2 border border-gray-300 rounded" placeholder="Time Spent (min)" onChange={handleChange} />
        <input name="recall_score" type="number" className="w-full p-2 border border-gray-300 rounded" placeholder="Recall Score (0-5)" onChange={handleChange} />
        <input name="previous_interval" type="number" className="w-full p-2 border border-gray-300 rounded" placeholder="Previous interval (No.of Days)" onChange={handleChange} />
        <button type="submit" className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">Predict</button>
      </form>

      {result && (
        <div className="mt-4 p-3 bg-green-100 border border-green-300 rounded">
          <p><strong>Message:</strong> {result.message}</p>
          <p><strong>Next Interval:</strong> {result.next_study_interval} days</p>
        </div>
      )}
    </div>
  );
};

export default PlannerForm;
// This component allows users to input their study data and get a prediction for their next study session. It uses the `predictNextSession` API function to send the data to the backend and display the result. The form includes fields for subject, time spent, and recall score, and it handles form submission and error handling. The result is displayed in a styled box below the form.