import React from 'react';
import './App.css';
import {Box, Flex, Text} from "rebass";

import Map from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';

import { Query } from 'react-apollo';
import {Sites} from "./queries/types/Sites";
import siteQuery from "./queries/siteQuery";

require('dotenv').config();

class SiteQuery extends Query<Sites> {}

const SitesList = () => {
    return (
      <SiteQuery
        query={siteQuery}
      >
        {({ data }) => (
          <>
           <h1>Sites</h1>
           <code>
            <pre>{JSON.stringify(data, null, 2)}</pre>
           </code>
          </>
         )}
      </SiteQuery>
    )
};


const client = new ApolloClient({uri: 'http://localhost/api/'});

const App: React.FC = () => {
  return (
      <ApolloProvider client={client}>
          <Flex>
              <Box width={1/12}> Left </Box>
              <Box width={5/6}>
                  <Map height={1024}>
                      <Flex>
                          <Text>Welcome to Digmaps!</Text>
                      </Flex>
                  </Map>
              </Box>
              <Box width={1/12}> Right </Box>
          </Flex>
      </ApolloProvider>
  );
};

export default App;
