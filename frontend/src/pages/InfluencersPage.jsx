import React, { useState, useEffect } from 'react';
import { influencersApi } from '../services/influencersApi';
import Modal from '../components/common/Modal';
import Table from '../components/common/Table';

const InfluencersPage = () => {
  const [influencers, setInfluencers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentInfluencer, setCurrentInfluencer] = useState(null);
  const [currentProjectId, setCurrentProjectId] = useState(null);
  const [currentProjectName, setCurrentProjectName] = useState('');

  useEffect(() => {
    const projectId = localStorage.getItem('currentProjectId');
    const projectName = localStorage.getItem('currentProjectName');
    setCurrentProjectId(projectId ? parseInt(projectId) : null);
    setCurrentProjectName(projectName || 'All Projects');
    fetchInfluencers(projectId);
  }, []);

  const fetchInfluencers = async (projectId = null) => {
    try {
      setIsLoading(true);
      const response = await influencersApi.getInfluencers(projectId);
      setInfluencers(response);
      setError(null);
    } catch (err) {
      setError('Failed to fetch influencers. Please try again later.');
      console.error('Error fetching influencers:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddNew = () => {
    setCurrentInfluencer(null);
    setIsModalOpen(true);
  };

  const handleEdit = (influencer) => {
    setCurrentInfluencer(influencer);
    setIsModalOpen(true);
  };

  const handleDelete = async (id) => {
    try {
      await influencersApi.deleteInfluencer(id);
      setInfluencers(influencers.filter(inf => inf.id !== id));
    } catch (err) {
      setError('Failed to delete influencer. Please try again.');
      console.error('Error deleting influencer:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const name = formData.get('name');

    const influencerData = {
      name,
      project_ids: currentProjectId ? [currentProjectId] : []
    };

    try {
      if (currentInfluencer) {
        const response = await influencersApi.updateInfluencer(currentInfluencer.id, influencerData);
        setInfluencers(influencers.map(inf => inf.id === currentInfluencer.id ? response : inf));
      } else {
        const response = await influencersApi.createInfluencer(influencerData);
        setInfluencers([...influencers, response]);
      }
      setIsModalOpen(false);
    } catch (err) {
      setError('Failed to save influencer. Please try again.');
      console.error('Error saving influencer:', err);
    }
  };

  const columns = [
    { key: 'id', label: 'ID' },
    { key: 'name', label: 'Name' },
    {
      key: 'actions',
      label: 'Actions',
      render: (_, influencer) => (
        <div className="flex space-x-2">
          <button className="btn btn-primary btn-sm" onClick={() => handleEdit(influencer)}>
            Edit
          </button>
          <button className="btn btn-ghost btn-sm" onClick={() => handleDelete(influencer.id)}>
            Delete
          </button>
        </div>
      ),
    },
  ];

  const renderForm = () => (
    <form onSubmit={handleSubmit}>
      <div className="form-control">
        <label className="label">
          <span className="label-text">Influencer Name</span>
        </label>
        <input
          type="text"
          name="name"
          defaultValue={currentInfluencer?.name || ''}
          placeholder="Enter influencer name"
          className="input input-bordered"
          required
        />
      </div>
      <div className="modal-action">
        <button type="submit" className="btn btn-primary">
          {currentInfluencer ? 'Update' : 'Create'} Influencer
        </button>
      </div>
    </form>
  );

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Influencers - {currentProjectName}</h1>
        <button onClick={handleAddNew} className="btn btn-primary">
          Add New Influencer
        </button>
      </div>

      {error && <div className="alert alert-error mb-4">{error}</div>}

      <Table
        data={influencers}
        columns={columns}
        itemsPerPage={10}
        loading={isLoading}
        showSearch={false}
        customClasses={{
          wrapper: 'shadow-lg',
          table: 'table-zebra',
          th: 'bg-primary text-primary-content',
          td: 'bg-base-100',
        }}
      />

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={currentInfluencer ? 'Edit Influencer' : 'Add New Influencer'}
      >
        {renderForm()}
      </Modal>
    </div>
  );
};

export default InfluencersPage;