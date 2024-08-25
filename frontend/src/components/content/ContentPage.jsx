import React from 'react';
import { useParams } from 'react-router-dom';
import SingleRecordLayout from '../../layouts/SingleRecordLayout';
import ContentView from './ContentView';

const ContentPage = () => {
  const { id } = useParams();

  return (
    <SingleRecordLayout title={`Content #${id}`}>
      <ContentView />
    </SingleRecordLayout>
  );
};

export default ContentPage;
