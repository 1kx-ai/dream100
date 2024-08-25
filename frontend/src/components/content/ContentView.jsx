import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { contentsApi } from '../services/contentsApi';

const ContentView = () => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
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

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!content) return <div>No content found</div>;

  return (
    <div className="content-view">
      <h1>Content Details</h1>
      <div>
        <strong>ID:</strong> {content.id}
      </div>
      <div>
        <strong>Link:</strong> <a href={content.link} target="_blank" rel="noopener noreferrer">{content.link}</a>
      </div>
      <div>
        <strong>Views:</strong> {content.views}
      </div>
      <div>
        <strong>Scraped Content:</strong>
        <pre>{content.scraped_content}</pre>
      </div>
    </div>
  );
};

export default ContentView;
