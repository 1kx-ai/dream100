import React from 'react';
import { Link } from 'react-router-dom';

// ... other imports and component code ...

// Inside your search results rendering
{searchResults.map((result) => (
  <div key={result.content.id}>
    <h3>
      <Link to={`/content/${result.content.id}`}>{result.content.link}</Link>
    </h3>
    {/* Other content details */}
  </div>
))}

// ... rest of the component code ...
