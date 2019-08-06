import React from 'react';
import './App.css';
import {Box, Flex, Text} from "rebass";

import Map from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';
import { ApolloProvider as ApolloHooksProvider } from 'react-apollo-hooks';

import {useSitesQuery} from "./generated/graphql";

require('dotenv').config();


const SitesList = (props: any) => {
    const q = useSitesQuery({variables:{limit: 10}});
    return <pre>{JSON.stringify(q, null, 2)}</pre>
};


const client = new ApolloClient({uri: 'http://localhost/api/'});

const App: React.FC = () => {
  return (
      <ApolloProvider client={client}>
          <ApolloHooksProvider client={client}>
              <Flex>
                  <Box width={1/2}>
                  <Map height={1024}>
                      <Flex>
                          <Text>Welcome to Digmaps!</Text>
                      </Flex>
                  </Map>
                  </Box>
                  <Box width={1/2}>
                      <Text>Sites</Text>
                      <SitesList/>
                  </Box>
              </Flex>
          </ApolloHooksProvider>
      </ApolloProvider>
  );
};

export default App;
