import React from 'react';
import PropTypes from 'prop-types';

const SingleRecordLayout = ({ title, children }) => {
  return (
    <div className="container mx-auto p-4">
      <div className="card bg-base-100 shadow-xl">
        <div className="card-body">
          <h2 className="card-title text-2xl font-bold mb-4">{title}</h2>
          <div className="divider"></div>
          {children}
        </div>
      </div>
    </div>
  );
};

SingleRecordLayout.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
};

export default SingleRecordLayout