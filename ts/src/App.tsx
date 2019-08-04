import React from 'react';
import './App.css';
import {Box, Flex, Text} from "rebass";

import Map from "./map"
import { ApolloProvider } from 'react-apollo';
import ApolloClient from 'apollo-boost';

import { Query } from 'react-apollo';
import {Sites, SitesVariables} from "./queries/types/Sites";
import siteQuery from "./queries/siteQuery";
import {useSitesQuery} from "./generated/graphql";

require('dotenv').config();

class SiteQuery extends Query<Sites, SitesVariables> {}

const SitesList = (props: any) => {
    const {data, error, loading} = useSitesQuery();
    const sdata = data;
    return (
      <SiteQuery
          client={props.client}
        query={siteQuery}
        variables={{limit: 10}}
      >
        {({ data }) => (
          <>
          <Text>{sdata} {error} {loading}</Text>
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
              <Box width={1/2}>
              <Map height={1024}>
                  <Flex>
                      <Text>Welcome to Digmaps!</Text>
                  </Flex>
              </Map>
              </Box>
              <Box width={1/2}>
                  <Text>Sites</Text>
                  <SitesList client={client}/>
              </Box>
          </Flex>
      </ApolloProvider>
  );
};

export default App;
