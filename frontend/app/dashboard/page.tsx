'use client';

import React, { useState, useEffect, useRef } from 'react';

type Question = {
  id: number | string;
  message: string;
  status: 'pending' | 'answered' | 'escalated';
  created_at: string;
};

type Notification = {
  id: number | string;
  message: string;
};

type WsMessage =
  | { event: 'INITIAL_QUESTIONS'; data: Question[] }
  | { event: 'NEW_QUESTION'; data: Question }
  | { event: "QUESTION_UPDATED"; data: Question[] }
  | { event: "ADMIN_NOTIFICATION"; data: Notification };

const formatDate = (timestamp: string | number) => {
  const date = new Date(timestamp);
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const Dashboard: React.FC = () => {
  const token =
    typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  const isAuthenticated = Boolean(token);
  const [activeTab, setActiveTab] = useState<number>(1);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isClient, setIsClient] = useState<boolean>(false);
  const wsRef = useRef<WebSocket | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [questionText, setQuestionText] = useState('');

  // Notifications
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isNotifModalOpen, setIsNotifModalOpen] = useState(false);

  const mark_as_answered = (id: string | number) => {
    wsRef.current?.send(
      JSON.stringify({ event: 'MARK_QUESTION_AS_ANSWERED', data: { question_id: id } })
    );
  };
  const mark_as_escalated = (id: string | number) => {
    wsRef.current?.send(
      JSON.stringify({ event: 'MARK_QUESTION_AS_ESCALATED', data: { question_id: id } })
    );
  };

  useEffect(() => setIsClient(true), []);

  useEffect(() => {
    const wsUrl = token
      ? `ws://localhost:8000/ws/questions?token=${token}`
      : `ws://localhost:8000/ws/questions`;

    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => console.log('WebSocket connected');

    wsRef.current.onmessage = (event: MessageEvent) => {
      try {
        const message: WsMessage = JSON.parse(event.data);
        switch (message.event) {
          case 'INITIAL_QUESTIONS':
            setQuestions(message.data);
            break;
          case 'NEW_QUESTION':
            setQuestions(prev => [message.data, ...prev]);
            break;
          case 'QUESTION_UPDATED':
            setQuestions(message.data);
            break;
          case 'ADMIN_NOTIFICATION':
            setNotifications(prev => [message.data, ...prev]);
            break;
          default:
            console.warn('Unknown WS event', message);
        }
      } catch (err) {
        console.error('WS parse error', err);
      }
    };

    wsRef.current.onerror = error => console.error('WebSocket error', error);
    wsRef.current.onclose = () => console.log('WebSocket disconnected');

    return () => wsRef.current?.close();
  }, []);

  const handleCreateQuestion = () => {
    if (!questionText.trim()) return;
    wsRef.current?.send(JSON.stringify({ event: 'CREATE_QUESTION', data: { message: questionText } }));
    setQuestionText('');
    setIsModalOpen(false);
  };

  const renderTabContent = () => {
    let filteredQuestions = questions;
    if (activeTab === 2) filteredQuestions = questions.filter(q => q.status === 'answered');
    else if (activeTab === 3) filteredQuestions = questions.filter(q => q.status === 'escalated');

    return (
      <div className="overflow-x-auto rounded-lg shadow-md border border-gray-200">
        <table className="min-w-full bg-white">
          <thead className="bg-gray-100">
            <tr>
              <th className="text-left p-3 border-b">Question</th>
              <th className="text-left p-3 border-b">Status</th>
              <th className="text-left p-3 border-b">Created At</th>
              {activeTab === 1 && isAuthenticated && <th className="text-left p-3 border-b">Actions</th>}
            </tr>
          </thead>
          <tbody>
            {filteredQuestions.length > 0 ? (
              filteredQuestions.map((q, idx) => (
                <tr key={q.id ?? idx} className="hover:bg-gray-50 transition">
                  <td className="p-3 border-b">{q.message}</td>
                  <td className="p-3 border-b capitalize">
                    <span
                      className={`px-2 py-1 rounded text-white text-sm ${
                        q.status === 'pending'
                          ? 'bg-yellow-500'
                          : q.status === 'answered'
                          ? 'bg-green-500'
                          : 'bg-red-500'
                      }`}
                    >
                      {q.status}
                    </span>
                  </td>
                  <td className="p-3 border-b">{formatDate(q.created_at)}</td>
                  {activeTab === 1 && isAuthenticated && (
                    <td className="p-3 border-b">
                      <div className="flex gap-2">
                        <button
                          disabled={q.status === 'answered'}
                          onClick={() => mark_as_answered(q.id)}
                          className="px-3 py-1 text-sm bg-blue-500 text-white rounded disabled:opacity-50 hover:bg-blue-600 transition"
                        >
                          Answered
                        </button>
                        <button
                          disabled={q.status === 'escalated'}
                          onClick={() => mark_as_escalated(q.id)}
                          className="px-3 py-1 text-sm bg-red-500 text-white rounded disabled:opacity-50 hover:bg-red-600 transition"
                        >
                          Escalate
                        </button>
                      </div>
                    </td>
                  )}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={activeTab === 1 && isAuthenticated ? 4 : 3} className="text-center p-4 text-gray-500">
                  No questions found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <>
      {/* Notification Modal */}
      {isNotifModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-6">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Notifications</h2>
            <div className="max-h-64 overflow-y-auto divide-y divide-gray-200">
              {notifications.length > 0 ? (
                notifications.map((n, idx) => (
                  <div key={n.id ?? idx} className="p-3 hover:bg-gray-100 rounded transition">
                    {n.message}
                  </div>
                ))
              ) : (
                <div className="text-center p-4 text-gray-500">No notifications</div>
              )}
            </div>
            <div className="flex justify-end mt-4">
              <button
                onClick={() => setIsNotifModalOpen(false)}
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 transition"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create Question Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-lg w-full max-w-md p-6">
            <h2 className="text-xl font-bold mb-4 text-gray-800">Create Question</h2>
            <textarea
              value={questionText}
              onChange={e => setQuestionText(e.target.value)}
              placeholder="Type your question..."
              className="w-full border rounded p-3 min-h-[100px] focus:outline-none focus:ring-2 focus:ring-blue-400 transition"
            />
            <div className="flex justify-end space-x-3 mt-4">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateQuestion}
                className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
        {/* Header */}
        <header className="bg-white shadow-md p-4 flex justify-between items-center rounded-b-lg">
          <h1 className="text-2xl font-bold text-blue-700">Dashboard</h1>
          {isAuthenticated && (
            <div className="flex items-center space-x-4 relative">
              <span
                className="relative cursor-pointer font-medium text-gray-700 bg-gray-100 px-3 py-2 rounded-full shadow hover:bg-gray-200 transition"
                onClick={() => setIsNotifModalOpen(true)}
              >
                Notifications
                {notifications.length > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full px-1">
                    {notifications.length}
                  </span>
                )}
              </span>
            </div>
          )}
        </header>

        {/* Tabs */}
        <nav className="bg-white shadow-md mt-4 p-2 flex justify-between items-center rounded-lg">
          <div className="flex space-x-4">
            <button
              className={`px-4 py-2 rounded-lg font-medium ${
                activeTab === 1 ? 'bg-blue-500 text-white shadow-md' : 'bg-gray-200 text-gray-700'
              }`}
              onClick={() => setActiveTab(1)}
            >
              All Questions
            </button>
            <button
              className={`px-4 py-2 rounded-lg font-medium ${
                activeTab === 2 ? 'bg-blue-500 text-white shadow-md' : 'bg-gray-200 text-gray-700'
              }`}
              onClick={() => setActiveTab(2)}
            >
              Answered
            </button>
            <button
              className={`px-4 py-2 rounded-lg font-medium ${
                activeTab === 3 ? 'bg-blue-500 text-white shadow-md' : 'bg-gray-200 text-gray-700'
              }`}
              onClick={() => setActiveTab(3)}
            >
              Escalated
            </button>
          </div>
          <button
            onClick={() => setIsModalOpen(true)}
            className="bg-green-500 text-white px-4 py-2 rounded-lg shadow hover:bg-green-600 transition"
          >
            + Create Question
          </button>
        </nav>

        {/* Content */}
        <main className="p-6">{isClient && renderTabContent()}</main>
      </div>
    </>
  );
};

export default Dashboard;
