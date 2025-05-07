import React, { useState } from 'react';
import { scheduleStudySession } from '../api';

const SessionScheduler = () => {
  const [form, setForm] = useState({
    subject: '',
    start_time: '',
    duration_minutes: ''
  });

  const [link, setLink] = useState(null);

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await scheduleStudySession(form);
    setLink(res.data.event_link);
  };

  return (
    <div className="p-4 bg-white shadow rounded-lg mt-6">
      <h2 className="text-xl font-semibold mb-4">📆 Schedule Study Session</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input name="subject" placeholder="Subject" className="w-full p-2 border border-gray-300 rounded" onChange={handleChange} />
        <input name="start_time" type="datetime-local" className="w-full p-2 border border-gray-300 rounded" onChange={handleChange} />
        <input name="duration_minutes" placeholder="Duration (min)" className="w-full p-2 border border-gray-300 rounded" onChange={handleChange} />
        <button className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">Schedule</button>
      </form>

      {link && (
        <div className="mt-4 text-green-700">
          ✅ Scheduled! <a href={link} target="_blank" rel="noreferrer" className="underline">View Event</a>
        </div>
      )}
    </div>
  );
};

export default SessionScheduler;
// This component allows users to schedule a study session by providing the subject, start time, and duration. It uses the `scheduleStudySession` API function to send the data to the backend and display a link to the scheduled event. The form includes fields for subject, start time, and duration, and it handles form submission. The link to the scheduled event is displayed below the form after submission