import React from 'react';
import './App.css';
import {Flex, Text} from "rebass";

import FullScreenMap from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';

import gql from 'graphql-tag';
import { Query } from 'react-apollo';

require('dotenv').config();

const GET_SITES = gql`
  {
    sites {
      id
      modernName
      coordinates {
        x
        y
      }
    }
  }
`;

const Sites = ({ onDogSelected }) => (
  <Query query={GET_SITES}>
    {({ loading, error, data }) => {
      if (loading) return 'Loading...';
      if (error) return `Error! ${error.message}`;

      return (
        <select name="dog" onChange={onDogSelected}>
          {data.dogs.map(site => (
            <option key={site.id} value={site.modernName}>
              {site.breed}
            </option>
          ))}
        </select>
      );
    }}
  </Query>


const client = new ApolloClient();

const App: React.FC = () => {
  return (
      <ApolloProvider client={client}>
          <FullScreenMap>
              <Flex>
                  <Text>Welcome to Digmaps!</Text>
              </Flex>
          </FullScreenMap>
      </ApolloProvider>
  );
};

export default App;
