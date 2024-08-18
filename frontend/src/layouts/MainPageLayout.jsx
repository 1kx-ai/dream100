import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const MainPageLayout = ({ title, records, onAddNew, renderRecord, children }) => {
  const [currentProjectName, setCurrentProjectName] = useState('');

  return (
    <div className="min-h-screen bg-base-100">
      <div className="navbar bg-base-200 shadow-lg">
        <div className="flex-1">
          <h1 className="text-2xl font-bold">{title}</h1>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {children}

        <div className="flex justify-end mb-6">
          <button
            onClick={onAddNew}
            className="btn btn-primary"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 mr-2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Add New
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {records.map((record) => (
            <div key={record.id} className="card bg-base-200 shadow-xl hover:shadow-2xl transition-shadow duration-300">
              <div className="card-body">
                {renderRecord(record)}
              </div>
            </div>
          ))}
        </div>

        {records.length === 0 && (
          <div className="text-center py-12">
            <p className="text-xl text-base-content text-opacity-70">No records found. Add a new one to get started!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MainPageLayout;