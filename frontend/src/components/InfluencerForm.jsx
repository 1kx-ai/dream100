import React from 'react';

const InfluencerForm = ({ currentInfluencer, onSubmit }) => {
  return (
    <form onSubmit={onSubmit}>
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
};

export default InfluencerForm;
