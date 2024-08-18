import React, { useState, useEffect } from 'react';
import MainPageLayout from '../layouts/MainPageLayout';
import { api } from '../services/api';

const InfluencersPage = () => {
  const [influencers, setInfluencers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchInfluencers();
  }, []);

  const fetchInfluencers = async () => {
    try {
      setIsLoading(true);
      const response = await api.get('/influencers');
      setInfluencers(response);
      setError(null);
    } catch (err) {
      setError('Failed to fetch influencers. Please try again later.');
      console.error('Error fetching influencers:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddNew = async (newInfluencer) => {
    try {
      const response = await api.post('/influencers', newInfluencer);
      setInfluencers([...influencers, response]);
    } catch (err) {
      setError('Failed to add new influencer. Please try again.');
      console.error('Error adding new influencer:', err);
    }
  };

  const handleEdit = async (id, updatedInfluencer) => {
    try {
      const response = await api.put(`/influencers/${id}`, updatedInfluencer);
      setInfluencers(influencers.map(inf => inf.id === id ? response : inf));
    } catch (err) {
      setError('Failed to update influencer. Please try again.');
      console.error('Error updating influencer:', err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/influencers/${id}`);
      setInfluencers(influencers.filter(inf => inf.id !== id));
    } catch (err) {
      setError('Failed to delete influencer. Please try again.');
      console.error('Error deleting influencer:', err);
    }
  };

  const renderInfluencer = (influencer) => (
    <>
      <h2 className="card-title">{influencer.name}</h2>
      <p>Projects: {influencer.project_ids.length}</p>
      <div className="card-actions justify-end">
        <button className="btn btn-primary btn-sm" onClick={() => handleEdit(influencer.id, { ...influencer, name: 'Updated Name' })}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 mr-1">
            <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
          </svg>
          Edit
        </button>
        <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(influencer.id)}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 mr-1">
            <path strokeLinecap="round" strokeLinejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
          </svg>
          Delete
        </button>
      </div>
    </>
  );

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <MainPageLayout
      title="Influencers"
      records={influencers}
      onAddNew={() => handleAddNew({ name: 'New Influencer', project_ids: [] })}
      renderRecord={renderInfluencer}
    />
  );
};

export default InfluencersPage;