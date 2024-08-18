import React, { useState, useEffect } from 'react';

const ProjectForm = ({ onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    name: '',
    description: ''
  });

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="form-control">
      <div className="mb-4">
        <label htmlFor="name" className="label">
          <span className="label-text">Project Name</span>
        </label>
        <input
          type="text"
          id="name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          required
          className="input input-bordered w-full"
        />
      </div>
      <div className="mb-4">
        <label htmlFor="description" className="label">
          <span className="label-text">Description</span>
        </label>
        <textarea
          id="description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          rows="3"
          className="textarea textarea-bordered w-full"
        ></textarea>
      </div>
      <div className="mt-6">
        <button type="submit" className="btn btn-primary w-full">
          {initialData ? 'Update Project' : 'Create Project'}
        </button>
      </div>
    </form>
  );
};

export default ProjectForm;