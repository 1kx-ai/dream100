import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { contentsApi } from '../../services/contentsApi';

const ContentView = () => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [copySuccess, setCopySuccess] = useState('');
  const { id } = useParams();

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await contentsApi.getContent(id);
        setContent(response);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch content');
        setLoading(false);
      }
    };

    fetchContent();
  }, [id]);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(content.scraped_content);
      setCopySuccess('Copied!');
      setTimeout(() => setCopySuccess(''), 2000);
    } catch (err) {
      setCopySuccess('Failed to copy');
    }
  };

  if (loading) return <div className="loading loading-spinner loading-lg"></div>;
  if (error) return <div className="alert alert-error">{error}</div>;
  if (!content) return <div className="alert alert-warning">No content found</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="form-control">
        <label className="label">
          <span className="label-text font-bold">ID:</span>
        </label>
        <input type="text" value={content.id} className="input input-bordered" readOnly />
      </div>
      <div className="form-control">
        <label className="label">
          <span className="label-text font-bold">Views:</span>
        </label>
        <input type="text" value={content.views} className="input input-bordered" readOnly />
      </div>
      <div className="form-control md:col-span-2">
        <label className="label">
          <span className="label-text font-bold">Link:</span>
        </label>
        <a href={content.link} target="_blank" rel="noopener noreferrer" className="link link-primary">{content.link}</a>
      </div>
      <div className="form-control md:col-span-2">
        <label className="label">
          <span className="label-text font-bold">Scraped Content:</span>
          <button onClick={copyToClipboard} className="btn btn-sm btn-outline">
            {copySuccess || 'Copy'}
          </button>
        </label>
        <div className="p-2 bg-base-200 rounded-lg whitespace-pre-wrap">
          {content.scraped_content}
        </div>
      </div>
    </div>
  );
};

export default ContentView;
